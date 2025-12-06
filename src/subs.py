from datetime import timedelta

from faststream.rabbit import RabbitQueue, RabbitRouter

from src.archive import get_video_from_archive
from src.bot import TGBot
from src.config import settings
from src import log
from src.schemas import Digest, Storyline
from src.utils import delete_file

router = RabbitRouter()


@router.subscriber(RabbitQueue(name="storyline_notification", durable=True))
async def storyline_handler(storyline: Storyline) -> None:
    log.info(f"Received storyline: {storyline.model_dump()}")

    url = (
        f"{storyline.source.archive_url}/embed.html?dvr=true&token={storyline.source.archive_token}"
        f"&from={storyline.start_time.timestamp()}&&autoplay=false&muted=false"
    )

    start_time_normal, end_time_normal = map(
        lambda dt: (dt + timedelta(hours=3)).strftime("%H:%M:%S"),
        (storyline.start_time, storyline.end_time),
    )

    video_path = await get_video_from_archive(
        storyline.source.archive_url,
        storyline.source.archive_token,
        int(storyline.start_time.timestamp()),
        int(storyline.end_time.timestamp()),
    )

    caption = (
        (
            f"<b>Новость с канала {storyline.source.title}</b>\n\n"
            f"<b>{storyline.title}</b>\n"
            f"<a href='{url}'>{start_time_normal}-{end_time_normal}</a>\n\n"
            f"<b>Краткая выжимка</b>: {storyline.summary}\n\n"
        )
        + (
            (
                f"<blockquote expandable><b>Краткая выжимка</b>: "
                f"{storyline.summary_ru}</blockquote>\n\n"
            )
            if storyline.summary_ru
            else ""
        )
        + (
            f"<b>Температура</b>: {storyline.temperature}\n\n"
            + " ".join(f"#{tag}" for tag in storyline.tags)
        )
    )

    bot = TGBot(storyline.to_chat_id)
    await bot.send_video_from_file(video_path)
    await bot.send_message(caption)
    log.info(f"Sent storyline notification: {caption}")
    delete_file(video_path)


@router.subscriber(RabbitQueue(name="digest_notification", durable=True))
async def digest_handler(digest: Digest) -> None:
    log.info(f"Received digest: {digest.model_dump()}")

    start_time_normal, end_time_normal = map(
        lambda dt: (dt + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M"),
        (digest.start_time, digest.end_time),
    )

    caption = (
        f"<b>Дайджест №{digest.id} от {digest.end_time.strftime('%d.%m.%Y')}</b>\n\n"
        f"<b>{digest.title}</b>\n"
        f"({start_time_normal}-{end_time_normal})\n\n"
        f"{digest.summary}\n\n"
        f"{' '.join(f'#{tag.title} ({tag.quantity})' for tag in digest.tags[:10])}"
    )

    bot = TGBot(digest.to_chat_id)
    await bot.send_message(caption)
    log.info(f"Sent digest notification: {caption}")
