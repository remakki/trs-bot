from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

from src.config import settings


class TGBot:
    def __init__(self, chat_id: int | str):
        self._chat_id = chat_id
        self.bot = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    async def send_message(self, text: str, chat_id: int | str | None = None) -> None:
        await self.bot.send_message(chat_id=chat_id or self._chat_id, text=text)

    async def send_video_from_file(
        self, video_path: str, caption: str | None = None, chat_id: int | str | None = None
    ) -> None:
        video = FSInputFile(video_path)
        await self.bot.send_video(chat_id=chat_id or self._chat_id, video=video, caption=caption)
