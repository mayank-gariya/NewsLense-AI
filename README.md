# 📰 NewsLens AI

An AI-powered news platform that leverages cutting-edge Natural Language Processing to analyze, summarize, and understand news articles in real-time. NewsLens AI combines a robust FastAPI backend with an intuitive Streamlit frontend to deliver intelligent news analysis.

---

## 🎯 Overview

NewsLens AI is a complete AI news platform that combines:
- **Intelligent News Analysis** using pre-trained Hugging Face models
- **Secure Authentication** with JWT-based authorization
- **Real-time Processing** with async FastAPI backend
- **Modern UI** built with Streamlit

Key Features:
- ✨ **Article Summarization** - Generate concise summaries
- 💭 **Sentiment Analysis** - Understand article tone and emotion
- 🏷️ **Topic Classification** - Automatically categorize news
- 🔍 **Named Entity Recognition** - Extract key entities
- ⚡ **Keyword Extraction** - Identify important terms
- ❓ **Question Answering** - Get answers from articles
- 🔐 **User Authentication** - Secure login system
- 💾 **Data Persistence** - MongoDB-backed storage

---

## 🏗️ Architecture Overview

### System Architecture

The application follows a **layered architecture** pattern:

```
Client (Streamlit Frontend)
          ↓
    HTTP/REST API
          ↓
Routes Layer (Validation & Routing)
          ↓
Service Layer (Business Logic)
          ↓
Repository Layer (Data Access)
          ↓
MongoDB Database
```

---

## 🖥️ Backend

### Overview

The backend is built with **FastAPI**, a modern, fast Python web framework for building APIs. It implements a clean, layered architecture with clear separation of concerns.

### Backend Stack

| Component | Technology | Badge |
|-----------|-----------|-------|
| **Framework** | FastAPI | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) |
| **Server** | Uvicorn | ![Uvicorn](https://img.shields.io/badge/Uvicorn-FFFFFF?style=for-the-badge&logo=python&logoColor=black) |
| **Language** | Python 3.10+ | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Database** | MongoDB | ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white) |
| **Async Driver** | Motor | ![Motor](https://img.shields.io/badge/Motor-47A248?style=for-the-badge&logo=mongodb&logoColor=white) |

### Backend Features

#### 🔐 Authentication & Security
- JWT token-based authentication (HS256 signature)
- OAuth2 with Password Bearer scheme
- Role-based access control (RBAC)
- Password hashing with Passlib (bcrypt)
- Protected endpoints with dependency injection

| Badge |
|-------|
| ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white) |
| ![OAuth2](https://img.shields.io/badge/OAuth2-4285F4?style=for-the-badge&logo=oauth&logoColor=white) |
| ![Passlib](https://img.shields.io/badge/Passlib-000000?style=for-the-badge&logo=python&logoColor=white) |

#### 🤖 AI & NLP Processing

Pre-trained models from Hugging Face:

| Model | Task | Parameters |
|-------|------|-----------|
| **facebook/bart-large-cnn** | Abstractive Summarization | 406M |
| **deepset/roberta-base-squad2** | Question Answering | 110M |
| **cardiffnlp/twitter-roberta-base-sentiment** | Sentiment Analysis | 110M |
| **facebook/bart-large-mnli** | Topic Classification | 406M |
| **dslim/bert-base-NER** | Named Entity Recognition | 110M |

| Badge |
|-------|
| ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black) |
| ![Transformers](https://img.shields.io/badge/Transformers-FF6B6B?style=for-the-badge&logo=pytorch&logoColor=white) |

#### 📊 Data Validation
- Pydantic schemas for request validation
- Type hints for static analysis
- Structured JSON responses

| Badge |
|-------|
| ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=python&logoColor=white) |

### Backend Architecture Components

**Request Processing Pipeline:**
```
Routes Layer
  ↓ (Validate & Route)
Service Layer
  ↓ (Business Logic)
Repository Layer
  ↓ (Database Operations)
MongoDB
```

**Key Layers:**

1. **Routes** - HTTP endpoint handlers, validation, dependency injection
2. **Services** - Business logic, AI orchestration, caching
3. **Repositories** - Data persistence, CRUD operations
4. **AI Service** - NLP model coordination, inference management
5. **Clients** - External API integration (Hugging Face, GNews)

### Response Times (Performance Targets)

| Operation | Cached | Uncached |
|-----------|--------|----------|
| Fetch Latest News | 50ms | 2000ms |
| Search Articles | 100ms | 3000ms |
| Get Summary | 100ms | 1500ms |
| Sentiment Analysis | 50ms | 500ms |
| NER Extraction | 50ms | 400ms |
| Topic Classification | 50ms | 700ms |

---

## 🎨 Frontend

### Overview

The frontend is built with **Streamlit**, enabling rapid development of interactive web applications with minimal code. It provides an intuitive interface for news browsing and AI-powered analysis.

### Frontend Stack

| Component | Technology | Badge |
|-----------|-----------|-------|
| **Framework** | Streamlit | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |
| **HTTP Client** | Requests | ![Requests](https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white) |
| **Configuration** | Python Dotenv | ![Dotenv](https://img.shields.io/badge/Dotenv-ECD53F?style=for-the-badge&logo=python&logoColor=black) |
| **Styling** | CSS | ![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white) |

### Frontend Features

#### 🔑 Authentication
- Secure login/registration system
- Session state management
- Protected pages with auth checks
- Token-based communication with backend

#### 📰 News Browsing
- Latest news feed
- Search functionality
- Article filtering and sorting
- Responsive layout

#### 🧠 AI Analysis Interface
- Real-time article summarization
- Sentiment analysis visualization
- Topic classification display
- Keyword extraction and highlighting
- Named entity recognition results
- Question answering interface

#### 💾 Session Management
- User session persistence
- Authentication state tracking
- Secure token storage
- Session timeout handling

### UI Components

- Navigation bar with authentication status
- Article cards with rich metadata
- Analysis results dashboard
- User profile management
- Settings and preferences panel

---

## 🔧 Technology Stack Summary

### Full Stack Overview

```
┌─────────────────────────────────────┐
│      Frontend (Streamlit)           │
│  ┌─────────────────────────────────┐│
│  │ • Session Management            ││
│  │ • News Browse Interface          ││
│  │ • AI Analysis Display            ││
│  │ • Authentication UI              ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
              ↓ (HTTP/REST)
┌─────────────────────────────────────┐
│    Backend (FastAPI + Uvicorn)      │
│  ┌─────────────────────────────────┐│
│  │ Routes Layer                     ││
│  │ Service Layer (Business Logic)   ││
│  │ AI Service (NLP Orchestration)   ││
│  │ Repository Layer                 ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
              ↓ (Async)
┌─────────────────────────────────────┐
│      MongoDB (NoSQL Database)        │
│  • Users Collection                 │
│  • News Collection                  │
│  • AI Analysis Cache                │
└─────────────────────────────────────┘
              ↓ (API)
┌─────────────────────────────────────┐
│    External Services                │
│  • Hugging Face Inference API       │
│  • GNews API                        │
└─────────────────────────────────────┘
```

### Complete Tech Stack Badges

#### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-FFFFFF?style=for-the-badge&logo=python&logoColor=black)

#### Database
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Motor](https://img.shields.io/badge/Motor-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

#### Frontend
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)

#### AI/ML
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Transformers](https://img.shields.io/badge/Transformers-FF6B6B?style=for-the-badge&logo=pytorch&logoColor=white)

#### Security
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![OAuth2](https://img.shields.io/badge/OAuth2-4285F4?style=for-the-badge&logo=oauth&logoColor=white)

#### Data Validation
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=python&logoColor=white)

#### Deployment
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Streamlit Cloud](https://img.shields.io/badge/Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

#### Testing
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

---

## 📦 Dependencies

### Backend Dependencies

Core framework and async support:
- **fastapi** - Modern web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation

Database:
- **motor** - Async MongoDB driver
- **pymongo** - MongoDB connection

Authentication:
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **bcrypt** - Cryptographic hashing

AI/NLP:
- **huggingface_hub** - HF model access
- **transformers** - NLP models
- **spacy** - Advanced NLP

Data processing:
- **requests** - HTTP client
- **numpy** - Numerical computing
- **email-validator** - Email validation

### Frontend Dependencies

- **streamlit** - Web app framework
- **requests** - HTTP client
- **python-dotenv** - Environment variables

---

## 🚀 Getting Started

### Backend Setup

```bash
# Install dependencies
pip install -r Backend/requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run development server
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Install dependencies
pip install -r Frontend/requirements.txt

# Set environment variables
cp .env.example .env

# Run Streamlit app
streamlit run app.py
```

---

## 📊 AI Processing Pipeline

**Unified NLP Pipeline for All Tasks:**

```
Input Article
    ↓
Preprocessing (Text cleaning, Tokenization)
    ↓
Model Inference (Load model, Forward pass)
    ↓
Postprocessing (Score normalization, Formatting)
    ↓
Structured Output (JSON)
    ↓
Cache (7-day TTL)
```

---

## 🎓 Key Learnings

This project encompasses:

- ✅ Building production-grade FastAPI applications
- ✅ MongoDB integration and data modeling
- ✅ JWT authentication and authorization
- ✅ AI/NLP model integration and inference
- ✅ Async Python programming
- ✅ Streamlit frontend development
- ✅ Cloud deployment (Render, Streamlit Cloud)
- ✅ Layered architecture design
- ✅ Error handling and logging
- ✅ Caching strategies

---

## 🌟 Architecture Principles

- **Separation of Concerns** - Each layer has distinct responsibilities
- **Single Responsibility** - Each class has one reason to change
- **Dependency Injection** - Loose coupling, easy testing
- **Repository Pattern** - Centralized data access
- **Service Layer Pattern** - Reusable business logic
- **Modular Design** - Independent, composable components

---

## 📚 Documentation

- [Backend Architecture](Backend.md) - Detailed backend design and API documentation
- [Future Enhancements](Future.md) - Planned improvements and upgrades
- [Learning Journey](learnings.md) - Development insights and key learnings

---

## 📋 Project Status

- **Status**: Active Development
- **Created**: 2026
- **Language Composition**: Python (86.5%), CSS (13.5%)
- **License**: MIT

---

## 👨‍💻 Author

**Mayank Gariya**  
Machine Learning Engineer | Backend Developer

---

## 🔗 Live Application & Links

- **Frontend (Streamlit)**: https://newslense-ai-bzpym6waagrduossyc9epa.streamlit.app/
- **Backend API**: https://backend-q23l.onrender.com
- **API Docs (Swagger)**: https://backend-q23l.onrender.com/docs
- **API Docs (ReDoc)**: https://backend-q23l.onrender.com/redoc
- **Repository**: https://github.com/mayank-gariya/NewsLense-AI

---

## 📝 License

This project is licensed under the MIT License.

---

**Last Updated**: 2026  
**Maintained**: NewsLens AI Team
