from bson import ObjectId
from app.config.database import db
from bson.errors import InvalidId
from datetime import datetime

class NewsRepository:

    async def save_articles(self, articles: list):
        if articles:
            await db.articles.insert_many(articles)

    async def get_article(
        self,
        page: int,
        limit: int
    ):
        skip = (page - 1) * limit
        return await (
            db.articles
            .find()
            .sort("published_at", -1)
            .skip(skip)
            .limit(limit)
            .to_list(length=limit)
        )

    async def get_latest_articles(self, limit: int = 10):
        return await (
            db.articles
            .find()
            .sort("cached_at", -1)
            .limit(limit)
            .to_list(length=limit)
        )

    async def get_article_by_url(self, url: str):
        return await db.articles.find_one({"url": url})

    async def save_article(self, article: dict):
        result = await db.articles.insert_one(article)
        return result.inserted_id

    async def get_article_by_id(self, article_id: str):
        try:
            return await db.articles.find_one(
                {"_id": ObjectId(article_id)}
            )
        except InvalidId:
            return None
    
    async def update_article(
        self,
        article_id: str,
        update_data: dict
    ):
        await db.articles.update_one(
            {"_id": ObjectId(article_id)},
            {
                "$set": update_data
            }
        )
    
    async def append_question_answer(
        self,
        article_id:str,
        qa_data:dict
    ):
        await db.articles.update_one(
                    {
            "_id": ObjectId(article_id)
            },
            {
                "$push": {
                    "ai.question_answers": qa_data
                },
                "$set": {
                    "ai.processed_at": datetime.now()
                }
            }
        )