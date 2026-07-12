from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user , get_current_admin
from app.schemas.news import NewsArticle
from app.services.news_service import NewsService
from fastapi import Body

router = APIRouter()

news_service = NewsService()

@router.get("/latest", response_model=list[NewsArticle])
async def latest_news(
    page: int = 1,
    limit: int = 10,
    current_user=Depends(get_current_user),
):
    return await news_service.get_latest_news(
        page,
        limit,
    )
    
@router.post("/refresh")
async def refresh_news(
    current_user=Depends(get_current_admin)
):
    return await news_service.refresh_news()

@router.get("/search", response_model=list[NewsArticle])
async def search_news(
    q: str,
    page: int = 1,
    limit: int = 10,
    current_user=Depends(get_current_user),
):
    return await news_service.search_news(
        q,
        page,
        limit,
    )


@router.get("/category/{category}", response_model=list[NewsArticle])
async def category_news(
    category: str,
    page: int = 1,
    limit: int = 10,
    current_user=Depends(get_current_user),
):
    return await news_service.get_news_by_category(
        category,
        page,
        limit,
    )
    
@router.get('/summary/{article_id}')
async def summarize_article(article_id: str,current_user=Depends(get_current_user)):
    summary = await news_service.generate_summary(article_id)
    
    return {
        'summary':summary
    }
    
@router.get("/sentiment/{article_id}")
async def generate_sentiment(
    article_id:str,
    current_user=Depends(get_current_user)
):
    return await news_service.generate_sentiment(article_id)

@router.get("/topic/{article_id}")
async def classify_topic(
    article_id:str,
    current_user=Depends(get_current_user)
):
    return await news_service.generate_topic(article_id)

@router.get("/entities/{article_id}")
async def get_entities(
    article_id:str,
    current_user=Depends(get_current_user)
):
    return await news_service.generate_entities(article_id)

@router.get("/keywords/{article_id}")
async def get_keywords(
    article_id: str,
    current_user=Depends(get_current_user)
):
    return await news_service.generate_keywords(article_id)

@router.post('/question-answer/{article_id}')
async def question_answer(
    article_id: str,
    question: str = Body(embed=True),
    current_user=Depends(get_current_user)
):
    return await news_service.generate_question_answer(
        article_id,
        question
    )
