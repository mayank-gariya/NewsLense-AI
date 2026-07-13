from fastapi import FastAPI
from app.routes.router import router
from app.config.database import db

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {
        "application": {
            "name": "NewsLens AI",
            "description": "AI-powered News Intelligence Platform built with FastAPI, MongoDB, Hugging Face Transformers, and Streamlit.",
            "version": "1.5.8",
            "status": "Running ✅",
            "environment": "Production"
        },

        "developer": {
            "name": "Mayank Gariya",
            "role": "Machine Learning Engineer | Backend Developer"
        },

        "technology_stack": {
            "backend": "FastAPI",
            "database": "MongoDB",
            "authentication": "JWT Authentication",
            "frontend": "Streamlit",
            "ai_models": [
                "facebook/bart-large-cnn",
                "deepset/roberta-base-squad2",
                "cardiffnlp/twitter-roberta-base-sentiment-latest",
                "facebook/bart-large-mnli",
                "dslim/bert-base-NER"
            ],
            "nlp_features": [
                "Summarization",
                "Question Answering",
                "Sentiment Analysis",
                "Topic Classification",
                "Named Entity Recognition",
                "Keyword Extraction"
            ]
        },

        "project": {
            "news_source": "GNews API",
            "metadata": [
                "Title",
                "Description",
                "Content",
                "Source",
                "Published At",
                "URL",
                "Image URL"
            ]
        },

        "documentation": {
            "Swagger UI": "/docs",
            "ReDoc": "/redoc"
        },

        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "🚀 Welcome to NewsLens AI Backend API"
    }
