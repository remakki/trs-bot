import structlog
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.config import settings
from src.logging import configure as configure_logging
from src.subs import router

configure_logging()

logger = structlog.get_logger('faststream')

broker = RabbitBroker(
    settings.RABBITMQ_URL,
    log_level=20,
    logger=logger,
    log_fmt=None,
)
app = FastStream(
    broker,
    title="Notification Service",
    version="0.0.1",
)
broker.include_router(router)
