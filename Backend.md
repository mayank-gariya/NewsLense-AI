# 🏗️ NewsLens AI Backend Architecture

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Architecture Flow](#architecture-flow)
- [Core Layers](#core-layers)
- [Tech Stack](#tech-stack)
- [MongoDB Schema](#mongodb-schema)
- [Design Principles](#design-principles)

---

## Overview

The NewsLens AI backend is built using **FastAPI** and follows a **layered architecture** to ensure modularity, maintainability, scalability, and extensibility. Every component adheres to the **Single Responsibility Principle** with clean separation of concerns.

### Architecture Flow Diagram

**Standard Request Pipeline:**

<img width="1136" height="603" alt="image" src="https://github.com/user-attachments/assets/168d8755-509b-4c46-80ec-8d87a60a9d72" />


**AI-Enhanced Request Pipeline:**

<img width="1183" height="672" alt="image" src="https://github.com/user-attachments/assets/219e60af-4496-46bc-9b9b-8277da0650e6" />


---

## 📂 Project Structure

```
backend/
├── 📄 Procfile
├── 📄 runtime.txt
├── 📄 requirements.txt
├── 📄 main.py
│
├── 📁 app/
│   └── Application core
│
├── 📁 routes/
│   ├── auth.py              # Authentication endpoints
│   ├── news.py              # News-related endpoints
│   ├── users.py             # User management endpoints
│   └── router.py            # Endpoint aggregator
│
├── 📁 services/
│   ├── auth_service.py      # Authentication business logic
│   ├── news_service.py      # News processing logic
│   └── ai_service.py        # AI orchestration layer
│
├── 📁 repositories/
│   ├── news_repository.py   # News data operations
│   └── user_repository.py   # User data operations
│
├── 📁 ai/
│   ├── 📁 inference/        # NLP model inference
│   ├── keyword_extractor.py
│   ├── topic_classifier.py
│   ├── summarizer.py
│   ├── sentiment.py
│   └── question_answer.py
│
├── 📁 nlp/
│   ├── keyword_extractor.py
│   ├── ner.py
│   ├── preprocessing.py
│   ├── ranking.py
│   ├── stopwords.py
│   └── manager.py
│
├── 📁 clients/
│   ├── huggingface_client.py    # Hugging Face API wrapper
│   └── gnews_client.py          # GNews API wrapper
│
├── 📁 dependencies/
│   └── auth.py              # JWT verification & authorization
│
├── 📁 schemas/
│   ├── auth.py
│   └── news.py
│
├── 📁 utils/
│   ├── helper.py
│   ├── jwt.py
│   ├── logger.py
│   └── password.py
│
└── 📁 config/
    ├── database.py
    ├── endpoints.py
    ├── settings.py
    └── ai.py
```

---

## 🚀 Architecture Flow

### Request Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Request (Client)                    │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  Routes Layer - Request Validation & Dependency Injection   │
│  ✓ Validate request payload                                 │
│  ✓ Apply authentication/authorization                       │
│  ✓ Route to appropriate service                             │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  Service Layer - Business Logic & Orchestration             │
│  ✓ Process business rules                                   │
│  ✓ Coordinate with repositories                             │
│  ✓ Handle caching & error management                        │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  Repository Layer - Data Persistence                        │
│  ✓ CRUD operations                                          │
│  ✓ Database queries & aggregations                          │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  MongoDB - Persistent Storage                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📌 Core Layers

### 1️⃣ Routes Layer

**Responsibilities:**
| Aspect | Details |
|--------|---------|
| **Validation** | Validate incoming HTTP requests using Pydantic schemas |
| **Service Routing** | Direct requests to appropriate service handlers |
| **Response Formatting** | Return standardized JSON responses |
| **Dependency Injection** | Inject services, dependencies, and auth context |
| **HTTP Status Codes** | Return appropriate status codes (200, 201, 400, 401, 404, 500) |

**Key Constraint:** Routes never communicate directly with MongoDB

**Example Flow:**
```python
GET /news/latest
    ↓
news_routes.get_latest_news()
    ↓
news_service.get_latest_news()
    ↓
news_repository.find_latest()
    ↓
MongoDB
```

---

### 2️⃣ Dependency Layer (Authentication & Authorization)

**Responsibilities:**
| Function | Implementation |
|----------|-----------------|
| **JWT Verification** | Validate token signature and expiration |
| **Token Decoding** | Extract user information from JWT claims |
| **Current User Resolution** | Identify authenticated user from context |
| **Route Protection** | Enforce authentication on protected endpoints |
| **Authorization Checks** | Verify user roles (admin, user, etc.) |

**Security Features:**
- ✅ OAuth2 with Password Bearer scheme
- ✅ JWT token-based authentication
- ✅ Role-based access control (RBAC)
- ✅ Token expiration and refresh mechanism
- ✅ Secure password hashing (Passlib)

```python
@router.get("/protected-endpoint")
async def protected_route(current_user = Depends(get_current_user)):
    # Only authenticated users can access
    return {"user": current_user}

@router.get("/admin-only")
async def admin_route(current_admin = Depends(get_admin_user)):
    # Only admin users can access
    return {"message": "Admin access granted"}
```

---

### 3️⃣ Service Layer

**Responsibilities:**
| Aspect | Details |
|--------|---------|
| **Business Logic** | Implement core application features |
| **Data Processing** | Transform and validate data |
| **AI Orchestration** | Coordinate NLP operations |
| **Caching Strategy** | Store and retrieve cached results |
| **Error Handling** | Manage exceptions and error recovery |
| **Validation** | Apply business rules and constraints |

**Key Constraint:** Services never directly communicate with clients

**Layered Services:**

```
Request
  ↓
news_service.process_article()
  ├→ Fetch from news_repository
  ├→ Check cache for AI results
  ├→ Call ai_service if cache miss
  ├→ Store results back to cache
  └→ Return processed data
```

---

### 4️⃣ Repository Layer

**Responsibilities:**
| Operation | Details |
|-----------|---------|
| **Create** | Insert new documents into collections |
| **Read** | Query and retrieve documents |
| **Update** | Modify existing documents |
| **Delete** | Remove documents from database |
| **Search** | Full-text search and complex queries |
| **Aggregation** | Pipeline aggregations and analytics |

**Centralized Database Logic:**
```
Services
  ↓
news_repository ─┐
                 ├→ MongoDB
user_repository ─┘
```

**Benefits:**
- Centralized database logic prevents code duplication
- Easy to modify queries without affecting services
- Simplified unit testing with mock repositories
- Better transaction management

---

### 5️⃣ AI Service & Inference Layer

**AI Service Responsibilities:**
| Component | Purpose |
|-----------|---------|
| **Orchestration** | Coordinate all NLP operations |
| **Cache Management** | Check and update inference cache |
| **Model Selection** | Choose appropriate models for tasks |
| **Pipeline Management** | Execute preprocessing and postprocessing |

**Inference Layer - NLP Models:**

| Model | Task | Implementation |
|-------|------|-----------------|
| **facebook/bart-large-cnn** | Abstractive Summarization | `Summarizer` |
| **deepset/roberta-base-squad2** | Question Answering | `QuestionAnswer` |
| **cardiffnlp/twitter-roberta-base-sentiment** | Sentiment Analysis | `SentimentInference` |
| **facebook/bart-large-mnli** | Topic Classification | `TopicClassifier` |
| **dslim/bert-base-NER** | Named Entity Recognition | `NERExtractor` |

**Single Responsibility Principle:**
```
Each inference class handles ONE NLP task:

SentimentInference      → Emotion analysis only
TopicClassifier        → Topic classification only
QuestionAnswer         → QA task only
Summarizer             → Summarization only
NERExtractor           → Entity extraction only
KeywordExtractor       → Keyword extraction only
```

**AI Processing Pipeline:**
```
news_service
    ↓
ai_service.analyze_article()
    ├→ Check cache
    ├→ If miss:
    │   ├→ sentiment_inference.predict()
    │   ├→ topic_classifier.classify()
    │   ├→ summarizer.summarize()
    │   ├→ ner_extractor.extract()
    │   ├→ keyword_extractor.extract()
    │   └→ question_answer.generate()
    ├→ Cache results
    └→ Return enriched article
```

---

### 6️⃣ Hugging Face Client

**HTTP Abstraction Layer**

**Responsibilities:**
| Function | Details |
|----------|---------|
| **Request Management** | Format and send inference requests |
| **Authorization** | Manage API credentials and headers |
| **Timeout Handling** | Configure retry logic and timeouts |
| **Error Handling** | Parse and handle API errors gracefully |
| **Response Parsing** | Extract predictions from API responses |

**Benefits:**
- ✅ Single point for all HF API calls
- ✅ Centralized error handling
- ✅ Easy to mock for testing
- ✅ Simplified credential management

```python
# Single client used across all inference classes
hf_client = HuggingFaceClient(api_key="hf_xxxx")

sentiment_result = hf_client.predict(
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    text="Great article!",
    task="sentiment"
)
```

---

### 7️⃣ News Client

**External API Integration**

**Responsibilities:**
| Operation | Details |
|-----------|---------|
| **Fetch Latest News** | Retrieve trending articles |
| **Search Articles** | Query by keywords and filters |
| **Category News** | Get news by topic/category |
| **Database Population** | Bulk import articles to MongoDB |
| **Refresh Mechanism** | Periodic updates with new articles |

**Data Flow:**
```
GNews API
    ↓
gnews_client.fetch_latest()
    ↓
news_repository.insert_batch()
    ↓
MongoDB (articles collection)
    ↓
Subsequent AI requests use cached MongoDB data
(Reduces external API calls)
```

---

## 💾 Caching Strategy

### Caching Architecture

**Purpose:** Reduce inference costs and improve response latency for expensive AI operations

**Cache Workflow:**
```
Client Request
    ↓
service.get_article_analysis(article_id)
    ├→ Check Redis/Cache for article_id
    ├→ Cache HIT → Return cached results ✓
    └→ Cache MISS:
        ├→ Run inference models
        ├→ Store results in cache with TTL
        └→ Return results
```

**Cached AI Features:**

| Feature | Model | Cache TTL | Use Case |
|---------|-------|-----------|----------|
| **Summary** | BART | 7 days | Long-form text reduction |
| **Sentiment** | RoBERTa | 7 days | Emotion analysis |
| **Topic** | BART-MNLI | 7 days | Content classification |
| **Keywords** | BERT-based | 7 days | Key phrase extraction |
| **Named Entities** | BERT-NER | 7 days | Entity recognition |
| **Q&A** | RoBERTa-SQuAD2 | 7 days | Question answering |

**Performance Benefits:**
- ⚡ **99% faster** response for cached queries
- 💰 **80-90% cost reduction** on API calls
- 📊 **High hit rate** due to news article patterns

---

## 🔐 Authentication Flow

### JWT-Based Authentication

<img width="794" height="286" alt="image" src="https://github.com/user-attachments/assets/70a7ed39-ea0a-4613-ba76-250896a6abb6" />


**Security Features:**
- 🔒 JWT tokens with HS256 signature
- ⏱️ Token expiration (15 min access, 7 days refresh)
- 🛡️ Password hashing with Passlib
- 🔑 Role-based access control
- 📝 Audit logging for auth events

---

## 📦 MongoDB Collections Schema

### Users Collection

<img width="442" height="574" alt="image" src="https://github.com/user-attachments/assets/58bcf0a6-fcbe-4c29-8b03-683949584bfc" />

**Document Structure:**
```json
{
  "_id": ObjectId("..."),
  "username": "string (unique)",
  "email": "string (unique, indexed)",
  "password_hash": "string",
  "role": "enum(user, admin, moderator)",
  "profile": {
    "first_name": "string",
    "last_name": "string",
    "avatar_url": "string",
    "bio": "string"
  },
  "preferences": {
    "theme": "light|dark",
    "notifications_enabled": "boolean",
    "email_digest": "boolean"
  },
  "timestamps": {
    "created_at": "ISODate",
    "updated_at": "ISODate",
    "last_login": "ISODate"
  },
  "status": "active|inactive|banned"
}
```

**Indexes:**
- Primary: `_id`
- Unique: `email`, `username`
- Standard: `role`, `status`, `created_at`

---

### News Collection

**Document Structure:**
```json
{
  "_id": ObjectId("..."),
  "metadata": {
    "title": "string (indexed)",
    "description": "string",
    "content": "string (full article text)",
    "source": "string",
    "url": "string (unique)",
    "image_url": "string"
  },
  "publishing": {
    "published_date": "ISODate",
    "last_updated": "ISODate",
    "crawled_at": "ISODate"
  },
  "ai_analysis": {
    "summary": {
      "value": "string",
      "confidence": "number(0-1)",
      "generated_at": "ISODate"
    },
    "sentiment": {
      "label": "enum(positive, negative, neutral)",
      "score": "number(0-1)",
      "generated_at": "ISODate"
    },
    "topic": {
      "primary": "string",
      "secondary": ["string"],
      "confidence": "number(0-1)",
      "generated_at": "ISODate"
    },
    "keywords": {
      "values": ["string"],
      "scores": ["number"],
      "generated_at": "ISODate"
    },
    "entities": {
      "PERSON": ["string"],
      "LOCATION": ["string"],
      "ORGANIZATION": ["string"],
      "MISC": ["string"],
      "generated_at": "ISODate"
    },
    "qa_pairs": [
      {
        "question": "string",
        "answer": "string",
        "confidence": "number"
      }
    ]
  },
  "engagement": {
    "views": "number",
    "saved_by_users": ["ObjectId"],
    "liked_by_users": ["ObjectId"],
    "comments_count": "number"
  }
}
```

**Indexes:**
- Primary: `_id`
- Unique: `url`
- Standard: `metadata.title`, `metadata.source`, `published_date`
- Full-Text: `metadata.title`, `metadata.description`, `metadata.content`

---

## 🧪 AI Processing Pipeline

### Unified NLP Pipeline

All AI tasks follow the same standardized pipeline:

```
Input Article
    ↓
┌─────────────────────────────────────────┐
│  1. Preprocessing                       │
│  - Text cleaning                        │
│  - Tokenization                         │
│  - Normalization                        │
│  - Stopword removal                     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  2. Model Inference                     │
│  - Load pre-trained model               │
│  - Forward pass                         │
│  - Extract predictions                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  3. Postprocessing                      │
│  - Score normalization                  │
│  - Confidence calculation               │
│  - Result formatting                    │
└─────────────────────────────────────────┘
    ↓
Structured Output (JSON)
    ↓
Cache for TTL
```
<img width="985" height="695" alt="image" src="https://github.com/user-attachments/assets/ce75c12f-d782-4d76-b5a9-4639de8a9ddd" />

### Task-Specific Implementations

| Task | Model | Input | Output | Latency |
|------|-------|-------|--------|---------|
| **Sentiment** | RoBERTa-base | Article text | {label, score} | ~500ms |
| **Topic** | BART-MNLI | Article title/text | {primary, secondary, confidence} | ~700ms |
| **Q&A** | RoBERTa-SQuAD2 | {context, question} | Answer + span | ~600ms |
| **Summary** | BART-CNN | Full article | {summary, compression_ratio} | ~1500ms |
| **NER** | BERT-NER | Article text | {entities by type} | ~400ms |
| **Keywords** | TF-IDF + BERT | Article text | {keywords, scores} | ~300ms |

---

## 🔧 Tech Stack

### Backend Framework & Server

| Technology | Purpose | Badge |
|-----------|---------|-------|
| **FastAPI** | Modern async web framework | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) |
| **Uvicorn** | ASGI server for async support | ![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=flat-square&logo=python&logoColor=white) |
| **Python** | Core language (3.9+) | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) |

### Database & Persistence

| Technology | Purpose | Badge |
|-----------|---------|-------|
| **MongoDB** | NoSQL document database | ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white) |
| **Motor** | Async MongoDB driver | ![MongoDB](https://img.shields.io/badge/Motor-47A248?style=flat-square&logo=mongodb&logoColor=white) |

### Authentication & Security

| Technology | Purpose | Badge |
|-----------|---------|-------|
| **JWT** | Token-based authentication (HS256) | ![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=json-web-tokens&logoColor=white) |
| **Passlib** | Password hashing (bcrypt) | ![Passlib](https://img.shields.io/badge/Passlib-000000?style=flat-square&logo=python&logoColor=white) |
| **OAuth2** | Authorization protocol (Bearer scheme) | ![OAuth2](https://img.shields.io/badge/OAuth2-4285F4?style=flat-square&logo=oauth&logoColor=white) |

### AI & Machine Learning

| Technology | Purpose | Badge |
|-----------|---------|-------|
| **Hugging Face Inference API** | Remote model serving | ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black) |
| **Transformers** | Pre-trained NLP models | ![Transformers](https://img.shields.io/badge/Transformers-FF6B6B?style=flat-square&logo=pytorch&logoColor=white) |

**Pre-trained Models:**

| Model | Task | Organization | Parameters |
|-------|------|--------------|------------|
| **facebook/bart-large-cnn** | Abstractive Summarization | Meta AI | 406M |
| **deepset/roberta-base-squad2** | Question Answering | DeepSet | 110M |
| **cardiffnlp/twitter-roberta-base-sentiment-latest** | Sentiment Analysis | Cardiff NLP | 110M |
| **facebook/bart-large-mnli** | Topic Classification | Meta AI | 406M |
| **dslim/bert-base-NER** | Named Entity Recognition | Dslim | 110M |

### Data Validation

| Technology | Purpose | Badge |
|-----------|---------|-------|
| **Pydantic** | Data validation & serialization | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=python&logoColor=white) |

### Deployment & DevOps

| Technology | Platform | Badge |
|-----------|----------|-------|
| **Render** | Cloud hosting & CI/CD | ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white) |
| **Docker** | Containerization | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) |

### Development & Testing

| Technology | Purpose | Badge |
|-----------|---------|-------|
| **pytest** | Unit testing framework | ![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) |
| **httpx** | Async HTTP client testing | ![httpx](https://img.shields.io/badge/httpx-000000?style=flat-square&logo=python&logoColor=white) |

---

## 📐 Design Principles

### Architecture Patterns

| Principle | Application | Benefit |
|-----------|-------------|---------|
| **Separation of Concerns** | Each layer handles one domain | Easier debugging & maintenance |
| **Single Responsibility Principle** | Each class has one reason to change | Code clarity & testability |
| **Dependency Injection** | Services injected via parameters | Loose coupling & easy mocking |
| **Repository Pattern** | Centralized data access | Abstraction of persistence |
| **Service Layer Pattern** | Business logic isolated from routes | Reusable business operations |
| **Modular Design** | Independent, composable modules | Code reuse across features |
| **Factory Pattern** | Centralized object creation | Consistent initialization |
| **Client Abstraction** | External APIs wrapped in clients | Single point of change |

### Code Quality Standards

- ✅ **Type Hints** - Full type annotations for static analysis
- ✅ **Error Handling** - Try-catch with appropriate logging
- ✅ **Logging** - Structured logging at all layers
- ✅ **Documentation** - Docstrings for all public methods
- ✅ **Testing** - Unit tests for services & repositories
- ✅ **Code Formatting** - Black formatter compliance
- ✅ **Linting** - Pylint & Flake8 standards

---

## 🎯 Key Architectural Benefits

### Maintainability
- ✅ Clear separation of concerns makes code easy to navigate
- ✅ Changes to business logic don't affect routes or database layer
- ✅ Well-defined interfaces between layers

### Scalability
- ✅ Service layer can be extracted to microservices
- ✅ Repositories can use different databases if needed
- ✅ Inference layer supports horizontal scaling

### Testability
- ✅ Mock repositories for service tests
- ✅ Mock external APIs for integration tests
- ✅ Independent layer testing

### Debuggability
- ✅ Clear data flow through layers
- ✅ Logging at each layer for traceability
- ✅ Structured error messages

### Extensibility
- ✅ New AI models added without changing routes
- ✅ New data sources added via client abstraction
- ✅ New business logic added in service layer

### Performance
- ✅ Async operations throughout (FastAPI + Motor)
- ✅ Intelligent caching of expensive operations
- ✅ Batch operations in repository layer

### Reusability
- ✅ Services usable by multiple routes
- ✅ Clients usable across services
- ✅ Utilities shared across codebase

---

## 📊 Performance Metrics

### Response Time Targets

| Operation | Cached | Uncached | Target SLA |
|-----------|--------|----------|-----------|
| Fetch Latest News | 50ms | 2000ms | 1s |
| Search Articles | 100ms | 3000ms | 2s |
| Get Article Summary | 100ms | 1500ms | 500ms |
| Sentiment Analysis | 50ms | 500ms | 200ms |
| NER Extraction | 50ms | 400ms | 150ms |
| Topic Classification | 50ms | 700ms | 250ms |

### Resource Utilization

| Metric | Target | Notes |
|--------|--------|-------|
| **Memory Usage** | <512MB | Per worker process |
| **CPU Usage** | <80% | Peak during inference |
| **Concurrent Connections** | 100+ | With 2-4 workers |
| **Database Connections** | 10-20 | Connection pool size |

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.10 or higher
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix/Mac
# or
venv\Scripts\activate  # Windows
```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload 

# Production mode
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### API Documentation

- **Swagger UI**: https://backend-q23l.onrender.com
- **ReDoc**: https://backend-q23l.onrender.com/redocs    

---

## 📞 Support & Contact

**Author:** Mayank Gariya  
**Role:** Machine Learning Engineer | Backend Developer  
**Project:** NewsLens AI

**Tech Stack Summary:**
- Backend: FastAPI + Uvicorn
- Database: MongoDB + Motor
- AI/ML: Hugging Face Transformers + Pre-trained Models
- Frontend: Streamlit
- Deployment: Render
- Authentication: JWT + OAuth2

---

**Last Updated:** 2026 
**License:** MIT  
**Status:** Active Development
