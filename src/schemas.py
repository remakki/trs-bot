from datetime import datetime

from pydantic import BaseModel


class Source(BaseModel):
    id: int
    title: str
    archive_url: str
    archive_token: str


class Storyline(BaseModel):
    id: int
    title: str
    summary: str
    summary_ru: str | None = None
    temperature: str
    start_time: datetime
    end_time: datetime
    to_chat_id: str

    tags: list[str]

    source: Source


class DigestTag(BaseModel):
    title: str
    quantity: int


class Digest(BaseModel):
    id: int
    title: str
    summary: str
    type: str
    start_time: datetime
    end_time: datetime
    created_at: datetime | None = None
    to_chat_id: str

    tags: list[DigestTag]
