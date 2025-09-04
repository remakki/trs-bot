from datetime import datetime

from faststream.rabbit import RabbitQueue, RabbitRouter

from src.archive import get_video_from_archive
from src.bot import TGBot
from src.config import settings
from src.log import log
from src.utils import delete_file

router = RabbitRouter()


@router.subscriber(RabbitQueue(name=settings.RABBITMQ_QUEUE, durable=True))
async def handler(message: dict) -> None:
    log.info(f"Received message: {message}")
    start_time, end_time = map(int, map(float, message["time_range"].split("-")))

    url = (
        f"{message['archive_url']}/embed.html?dvr=true&token={message['archive_token']}"
        f"&from={start_time}&&autoplay=false&muted=false"
    )

    start_time_normal, end_time_normal = map(
        lambda time: datetime.fromtimestamp(time).strftime("%H:%M:%S"),
        (start_time, end_time),
    )

    video_path = await get_video_from_archive(
        message["archive_url"], message["archive_token"], start_time, end_time
    )

    caption = (
        f"<b>News</b>\n\n"
        f"<a href='{url}'>{start_time_normal}-{end_time_normal}</a>\n\n"
        f"<b>Summary</b>: {message['summary']}\n\n"
        f"<tg-spoiler><b>Краткая выжимка</b>: "
        f"{message['summary_ru']}</tg-spoiler>\n\n"
        f"<b>Temperature</b>: {message['temperature']}\n\n"
        + " ".join(f"#{tag}" for tag in message["tags"])
    )

    bot = TGBot()
    await bot.send_video_from_file(message["chat_id"], video_path)
    await bot.send_message(message["chat_id"], caption)
    log.info(f"Sent message: {message}")
    delete_file(video_path)
