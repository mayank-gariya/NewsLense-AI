from datetime import datetime

from fastapi import HTTPException
from app.clients.news_client import NewsClient
from app.repositories.news_repository import NewsRepository
from app.utils.logger import logger
from app.services.ai_service import AIService
from app.clients.article_client import ArticleClient

from app.config.ai import QA_CONFIDENCE_THRESHOLD

class NewsService:

    def __init__(self):
        self.news_client = NewsClient()
        self.news_repository = NewsRepository()
        self.ai_service = AIService()
        self.article_client = ArticleClient()
        
    async def get_latest_news(
        self,
        page: int,
        limit: int
    ):
        logger.info("Reading latest news from MongoDB")

        articles = await self.news_repository.get_article(
            page,
            limit
        )

        for article in articles:
            article["id"] = str(article["_id"])
            del article["_id"]

        return articles
    
    async def refresh_news(self):
        logger.info("Refreshing News Cache")
        articles = await self.news_client.get_latest_news(
            page=1,
            limit=10
        )
        
        inserted = 0

        for article in articles:
            existing = await self.news_repository.get_article_by_url(
                article["url"]
            )
            
            if existing:
                continue

            article["fetched_at"] = datetime.now()
            
            full_content = self.article_client.extract_article(
                article["url"]
            )

            # Use extracted article if available
            if full_content:
                article["content"] = full_content
            
            logger.info(
                    f"Extracted article length: {len(full_content) if full_content else 0}"
            )

            article["ai"] = {
                "summary": None,
                "sentiment": None,
                "topic": None,
                "entities": None,
                "keywords": None,
                "embedding": None,
                "processed_at": None,
                "question_answers": []
            }

            await self.news_repository.save_article(article)
            inserted += 1

        return {
            "inserted": inserted,
            "received": len(articles)
        }
        
    async def search_news(self, query: str, page: int, limit: int):
        logger.info(f"Searching: {query}")
        return await self.news_client.search_news(query, page, limit)

    async def get_news_by_category(self, category: str, page: int, limit: int):
        logger.info(f"Category: {category}")
        return await self.news_client.get_news_by_category(category, page, limit)
        
    async def generate_summary(
            self,
            article_id: str
        ):

        article = await self.news_repository.get_article_by_id(
            article_id
        )

        if article is None:
            raise HTTPException(
                    status_code=404,
                    detail="Article not found"
                )

        ai_data = article.get("ai", {})

        summary = ai_data.get("summary")
        
        if summary:
            return summary["value"]

        text = article.get("content") or article.get("description") or article.get('title')

        summary = self.ai_service.generate_summary(text)

        await self.news_repository.update_article(
            article_id,
            {
                "ai.summary": {
                    "value": summary,
                    "generated_at": datetime.now(),
                    "model": "DistilBART"
                },
                "ai.processed_at": datetime.now()
            }
        )
        
        return summary
    
    async def generate_sentiment(self,article_id:str):
        article = await self.news_repository.get_article_by_id(article_id=article_id)
        
        if article is None:
            raise HTTPException(
                status_code=404
            )
        
        ai_data = article.get('ai',{})
        
        sentiment = ai_data.get('sentiment')
        if sentiment:
            return sentiment['value']
        
        text = (
            article.get('content')
            or article.get('description')
            or article.get('title')
        )
        
        sentiment = self.ai_service.analyze_sentiment(text)
        
        await self.news_repository.update_article(
            article_id,
                {
                    'ai.sentiment':{
                        'value':sentiment,
                        'generated_at':datetime.now(),
                        'model':'DistilBERT'
                    },
                    'ai.processed_at':datetime.now()
                }
            )
        
        return sentiment
    
    async def generate_topic(self,article_id:str):
        article = await self.news_repository.get_article_by_id(article_id=article_id)
        
        if article is None:
            raise HTTPException(
                status_code=404
            )
        
        ai_data = article.get('ai',{})
        
        if ai_data.get('topic'):
            return ai_data['topic']['value']
        
        text = (
            article.get('content')
            or article.get('description')
            or article.get('title')
        )
        
        topic = self.ai_service.classify_topic(text)
        
        await self.news_repository.update_article(
            article_id,
                {
                    "ai.topic": {
                        "value": topic,
                        "generated_at": datetime.now(),
                        "model": "facebook/bart-large-mnli"
                    },
                    'ai.processed_at':datetime.now()
                }
            )
        
        return topic
    
    async def generate_entities(
        self,
        article_id: str
    ):

        article = await self.news_repository.get_article_by_id(
            article_id
        )

        if article is None:
            raise HTTPException(
                status_code=404
            )

        ai_data = article.get("ai", {})

        entities_data = ai_data.get("entities")
        if entities_data:
            return entities_data["value"]
        text = (
            article.get("content")
            or article.get("description")
            or article.get("title")
        )

        entities = self.ai_service.extract_entities(text)

        await self.news_repository.update_article(
            article_id,
            {
                "ai.entities": {
                    "value": entities,
                    "generated_at": datetime.now(),
                    "model": "spaCy"
                },
                "ai.processed_at": datetime.now()
            }
        )

        return entities
    
    async def generate_keywords(
        self,
        article_id:str
    ):
        article = await self.news_repository.get_article_by_id(
            article_id
        )

        if article is None:
            raise HTTPException(
                status_code=404
            )

        ai_data = article.get("ai", {})

        keyword_data = ai_data.get("keywords")
        
        if keyword_data:
            return keyword_data["value"]

        text = (
            article.get("content")
            or article.get("description")
            or article.get("title")
        )

        keywords = self.ai_service.extract_keywords(text)

        await self.news_repository.update_article(
            article_id,
            {
                "ai.keywords": {
                    "value": keywords,
                    "generated_at": datetime.now(),
                    "model": "YAKE + spaCy"
                },
                "ai.processed_at": datetime.now()
            }
        )

        return keywords
    
    async def generate_question_answer(
        self,
        article_id:str,
        question:str
    ):
        article = await self.news_repository.get_article_by_id(
        article_id
        )


        if article is None:
            raise HTTPException(
                status_code=404,
                detail="Article not found"
            )
        
        qa_cache = (
            article
            .get('ai',{})
            .get('question_answers',[])
        )
        
        for item in qa_cache:
            if (
                item['question'].strip().lower() == question.strip().lower()
            ):
                return {
                    **item,
                    'cached':True
                }
        
        contex = (
            article.get('content')
            or article.get("description")
            or article.get("title")
        )
        
        if not contex:
            raise HTTPException(
            status_code=400,
            detail="Article has no content."
        )
            
        result = self.ai_service.answer_question(question=question,context=contex)
        
        if result["confidence"] < QA_CONFIDENCE_THRESHOLD:
            return {
                "question": question,
                "answer": (
                    "I couldn't find enough "
                    "information in this article."
                ),
                "confidence": result["confidence"],
                "cached": False
            }
            
        qa_data = {
            "question": question,
            "answer": result["answer"],
            "confidence": result["confidence"],
            "generated_at": datetime.now(),
            "model": "deepset/roberta-base-squad2"
        }
        
        await self.news_repository.append_question_answer(article_id=article_id,qa_data=qa_data)
        
        return {
            **qa_data,
            'cached':False
        }