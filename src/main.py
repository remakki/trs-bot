import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.config import settings
from src.handler import router

broker = RabbitBroker(settings.RABBITMQ_URL)
app = FastStream(broker)
broker.include_router(router)


async def main() -> None:
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
