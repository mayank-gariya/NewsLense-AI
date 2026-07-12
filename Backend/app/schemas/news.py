from pydantic import BaseModel


class NewsArticle(BaseModel):
    id: str
    title: str
    description: str | None = None
    content: str | None = None
    url: str
    image: str | None = None
    source: str | None = None
    published_at: str | None = None