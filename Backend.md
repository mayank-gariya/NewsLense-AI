# 🏗️ NewsLens AI Backend Architecture

## Overview

The NewsLens AI backend is built using **FastAPI** and follows a layered architecture to keep the code modular, maintainable, scalable, and easy to extend.

Instead of placing all business logic inside routes, every component has a single responsibility.

The architecture follows this flow:

<img width="889" height="404" alt="image" src="https://github.com/user-attachments/assets/04f7458a-f7fa-4994-8553-d1a61ec4f21e" />


For AI features the flow becomes:

<img width="1064" height="583" alt="image" src="https://github.com/user-attachments/assets/7a6bbed5-6110-4f30-b0f0-918652d417fe" />

---

# 📂 Project Structure

<img width="925" height="625" alt="image" src="https://github.com/user-attachments/assets/06c31b14-399d-4b72-be86-bfc8424466aa" />

```
backend/
│├──  Procfile
|├── runtime.txt
|├── requirements.txt
|
|├── app/
│
├── routes/
│ ├── auth.py
│ ├── news.py
│ └── users.py
| └── router.py
│
├── services/
│ ├── auth_service.py
│ ├── news_service.py
│ └── ai_service.py
│
├── repositories/
│ ├── news_repository.py
│ └── user_repository.py
│
├── ai/
│ ├── inference/
│ ├── keyword_extractor.py
│ ├── topic_classifier.py
│ ├── summarizer.py
│ ├── sentiment.py
│ └── question_answer.py
|
│├── nlp /
|└── keyword_extractor.py
|└── ner.py
|└── preprocessing.py
|└── ranking.py
|└── stopwords.py
|└── manager.py
|
├── clients/
│ ├── huggingface_client.py
│ └── gnews_client.py
│
├── dependencies/
│ └── auth.py
│
├── schemas/
|└── auth.py
|└── news.py
│
├── utils/
│└── helper.py
|└── jwt.py
|└── logger.py
|└── password.py
|
├── config/
│└── database.py
|└── endpoints.py
|└── settings.py
|└── ai.py
└── main.py

```

---

# 🚀 Request Flow

Whenever a request reaches the backend it follows a specific lifecycle.

<img width="926" height="512" alt="image" src="https://github.com/user-attachments/assets/4034b5fa-9754-45f2-814b-e163a40f7cae" />

Each layer has only one responsibility.

---

# 📌 Routes Layer

The Routes layer only receives HTTP requests.

Responsibilities:

- Request validation
- Calling the correct service
- Returning responses
- Dependency Injection

Routes never communicate directly with MongoDB.

Example:

```

GET /news/latest

↓

news_service.get_latest_news()

```

---

# 🔐 Dependency Layer

Authentication is handled separately using Dependency Injection.

Responsibilities:

- Verify JWT Token
- Decode Token
- Identify Current User
- Protect Routes
- Admin Authorization

<img width="771" height="316" alt="image" src="https://github.com/user-attachments/assets/5cd7b28d-7d77-447b-8e91-bdbed678f9c3" />


This keeps authentication reusable across every endpoint.

---

# ⚙️ Service Layer

The Service layer contains the application's business logic.

Responsibilities:

- News Processing
- AI Operations
- Authentication Logic
- Validation
- Caching
- Error Handling

The service decides **how** data should be processed.

It never directly communicates with the client.

---

# 🗄 Repository Layer

Repositories communicate with MongoDB.

Responsibilities:

- Insert Documents
- Update Documents
- Delete Documents
- Search Documents
- Database Queries

Instead of writing database logic everywhere, it is centralized here.

```

Service

↓

Repository

↓

MongoDB

```

---

# 🤖 AI Service

The AI Service coordinates all NLP features.

<img width="945" height="683" alt="image" src="https://github.com/user-attachments/assets/14c731ac-baa6-4a29-9090-c3b58b0990bf" />


The AI Service never calls Hugging Face directly.

---

# 🧠 Inference Layer

Every NLP task has its own inference class.

Example:

```

SentimentInference

TopicClassifier

QuestionAnswer

Summarizer

NERExtractor

KeywordExtractor

```

Each class performs only one AI task.

This follows the **Single Responsibility Principle**.

---

# 🌐 Hugging Face Client

Instead of repeating HTTP requests everywhere, one reusable client handles all inference requests.

```

AI Service

↓

SentimentInference

↓

HuggingFaceClient

↓

Hugging Face API

```

Responsibilities:

- Authorization
- API Requests
- Timeouts
- Error Handling
- Response Parsing

---

# 📰 News Client

The News Client communicates with the external GNews API.

Responsibilities:

- Fetch Latest News
- Search Articles
- Category News
- Refresh Database

After fetching data, articles are stored inside MongoDB.

Future AI requests use MongoDB instead of repeatedly calling GNews.

---

# 💾 Caching Strategy

Expensive AI operations are cached.

Example:

<img width="630" height="581" alt="image" src="https://github.com/user-attachments/assets/206d5d04-3515-4c21-8b63-2d901b28de5b" />


This greatly reduces inference cost and improves speed.

Cached Features

- Summary
- Question Answering
- Sentiment
- Topic
- Keywords
- Named Entities

---

# 🔑 Authentication Flow

<img width="1007" height="405" alt="image" src="https://github.com/user-attachments/assets/6def0fde-908e-40f9-8b4e-f236aef98d82" />


---

# 📦 MongoDB Collections

## Users

Stores:

- Username
- Email
- Password Hash
- Role

---

## News

Stores:

- Title
- Description
- Content
- Source
- Image
- URL
- Published Date

AI Metadata

```

ai

├── summary

├── sentiment

├── topic

├── keywords

├── entities

└── question_answers

```

---

# 🔄 AI Processing Flow

Exactly the same pipeline is used for:

- Sentiment
- Topic
- Question Answering
- Keywords
- NER

---

# 📚 Technologies Used

## Backend

- FastAPI
- Uvicorn

## Database

- MongoDB
- Motor

## Authentication

- JWT
- Passlib
- OAuth2

## AI

- Hugging Face Inference API
- Transformers

Models Used

- facebook/bart-large-cnn
- deepset/roberta-base-squad2
- cardiffnlp/twitter-roberta-base-sentiment-latest
- facebook/bart-large-mnli
- dslim/bert-base-NER

## Validation

- Pydantic

## Deployment

- Render

---

# 📐 Design Principles

The backend follows several software engineering principles:

- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection
- Repository Pattern
- Service Layer Pattern
- Modular Design
- Reusable Components
- Clean Architecture

---

# 🎯 Benefits of this Architecture

- Easy to maintain
- Easy to debug
- Easy to extend
- Scalable
- Reusable
- Testable
- Production-ready
- Clean separation between business logic and database operations

---

# 👨‍💻 Author

**Mayank Gariya**

Machine Learning Engineer | Backend Developer

**Project:** NewsLens AI

Built using FastAPI, MongoDB, Hugging Face Transformers, and Streamlit.
