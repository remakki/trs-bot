import os

import aiofiles
import aiohttp

from src import log


async def get_video_from_archive(base_url: str, token: str, start_time: int, end_time: int) -> str:
    dur = min(100, end_time - start_time)
    ENDPOINT = f"{base_url}/archive-{start_time}-{dur}.mp4?token={token}"
    save_path = f"data/{start_time}-{dur}.mp4"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(ENDPOINT, ssl=False) as response:
                response.raise_for_status()
                async with aiofiles.open(save_path, "wb") as f:
                    while chunk := await response.content.read(1024 * 1024):
                        await f.write(chunk)
        except aiohttp.ClientError as e:
            log.error(f"Error downloading video: {e}")
            raise
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise

    return save_path
