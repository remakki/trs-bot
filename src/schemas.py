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
    summary_ru: str
    temperature: str
    start_time: datetime
    end_time: datetime

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

    tags: list[DigestTag]
