from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    LOG_LEVEL: str = "INFO"

    BOT_TOKEN: str

    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    CHANNEL_ID: str

    @property
    def RABBITMQ_URL(self):
        return (
            f"amqp://{self.RABBITMQ_USERNAME}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )


settings = Settings()
