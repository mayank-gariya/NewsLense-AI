import httpx
from fastapi import HTTPException

from app.config.settings import settings
from app.config.endpoint import GNEWS_ENDPOINTS


class NewsClient:

    async def _make_request(self, endpoint: str, params: dict) -> dict:
        """Centralized HTTP request handler with error handling."""
        url = settings.news_base_url + endpoint
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=503,
                detail="News provider is unavailable."
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Unable to fetch news."
            )

    def _normalize_articles(self, data: dict) -> list:
        """Transform raw API response into a consistent article format."""
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "url": article.get("url"),
                "image": article.get("image"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt")
            })
        return articles

    async def get_latest_news(
        self,
        page: int = 1,
        limit: int = 10
    ) -> list:
        params = {
            "apikey": settings.news_api_key,
            "lang": "en",
            "page": page,
            "max": limit
        }
        data = await self._make_request(GNEWS_ENDPOINTS["latest"], params)
        return self._normalize_articles(data)

    async def search_news(
        self,
        query: str,
        page: int = 1,
        limit: int = 10
    ) -> list:
        params = {
            "apikey": settings.news_api_key,
            "q": query,
            "lang": "en",
            "page": page,
            "max": limit
        }
        data = await self._make_request(GNEWS_ENDPOINTS["search"], params)
        return self._normalize_articles(data)

    async def get_news_by_category(
        self,
        category: str,
        page: int = 1,
        limit: int = 10
    ) -> list:
        params = {
            "apikey": settings.news_api_key,
            "category": category,
            "lang": "en",
            "page": page,
            "max": limit
        }
        data = await self._make_request(GNEWS_ENDPOINTS["category"], params)
        return self._normalize_articles(data)