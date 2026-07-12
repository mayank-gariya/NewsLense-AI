import requests
from typing import List, Dict, Any
import random
import json
from src.utils.helpers import format_published_date

class GNewsClient:
    BASE_URL = "https://gnews.io/api/v4"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.use_mock = not api_key

    def _make_request(self, endpoint: str, params: Dict) -> List[Dict[str, Any]]:
        """Make API request or return mock data if no key."""
        if self.use_mock:
            return self._get_mock_news()

        params["apikey"] = self.api_key
        try:
            response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            # Transform to our schema
            return [
                {
                    "title": a.get("title", ""),
                    "description": a.get("description"),
                    "content": a.get("content"),
                    "url": a.get("url", "#"),
                    "image": a.get("image"),
                    "source": a.get("source", {}).get("name", "Unknown"),
                    "published_at": a.get("publishedAt"),
                }
                for a in articles
            ]
        except Exception as e:
            print(f"API error: {e}")
            return self._get_mock_news()

    def get_top_headlines(self, category: str = "general", max_results: int = 20) -> List[Dict]:
        params = {
            "category": category,
            "max": max_results,
            "lang": "en",
            "country": "us"
        }
        return self._make_request("top-headlines", params)

    def search_news(self, query: str, max_results: int = 20) -> List[Dict]:
        params = {
            "q": query,
            "max": max_results,
            "lang": "en"
        }
        return self._make_request("search", params)

    def _get_mock_news(self) -> List[Dict]:
        """Return placeholder articles for design preview."""
        mock_data = [
            {
                "title": "Global summit agrees on new AI safety framework",
                "description": "Leaders announced a joint framework focused on transparency, risk assessment, and international cooperation.",
                "content": "Leaders from 30 countries signed the accord...",
                "url": "#",
                "image": "https://placehold.co/600x400/1A1F2B/7C3AED?text=AI+Summit",
                "source": "Tech Chronicle",
                "published_at": "2026-07-09T10:30:00Z"
            },
            {
                "title": "Electric vehicle demand rises across major markets",
                "description": "Analysts say lower battery costs and government incentives are accelerating EV adoption worldwide.",
                "content": "Sales of electric vehicles jumped 40% in Q2...",
                "url": "#",
                "image": "https://placehold.co/600x400/1A1F2B/22D3EE?text=EV+Surge",
                "source": "Auto Insider",
                "published_at": "2026-07-09T08:15:00Z"
            },
            {
                "title": "Amex revamps Delta Miles card: Check out",
                "description": "The new card offers enhanced travel benefits and bonus miles for frequent flyers.",
                "content": "American Express announced a major overhaul...",
                "url": "#",
                "image": "https://placehold.co/600x400/1A1F2B/7C3AED?text=Amex+Delta",
                "source": "Finance Today",
                "published_at": "2026-07-08T14:45:00Z"
            },
            {
                "title": "The attacks came a day after the US hit Iran",
                "description": "Escalating tensions in the Middle East raise global concerns.",
                "content": "Military analysts warn of further retaliation...",
                "url": "#",
                "image": "https://placehold.co/600x400/1A1F2B/22D3EE?text=World+News",
                "source": "Global Report",
                "published_at": "2026-07-08T11:20:00Z"
            },
            {
                "title": "Worker pays out $25 million to a fake news outlet",
                "description": "A costly mistake highlights the dangers of misinformation.",
                "content": "The worker fell for a sophisticated phishing scheme...",
                "url": "#",
                "image": "https://placehold.co/600x400/1A1F2B/7C3AED?text=Fake+News",
                "source": "Business Times",
                "published_at": "2026-07-07T19:00:00Z"
            },
            {
                "title": "Iran stars facing 'last dance' in Asian Cup",
                "description": "Veteran players aim for glory in what may be their final tournament.",
                "content": "The Iranian national team is under pressure...",
                "url": "#",
                "image": "https://placehold.co/600x400/1A1F2B/22D3EE?text=Asian+Cup",
                "source": "Sports Daily",
                "published_at": "2026-07-07T16:30:00Z"
            }
        ]
        # Shuffle and return
        random.shuffle(mock_data)
        return mock_data