# 🚀 LearnMate AI

> **An AI-powered personalized learning platform that helps students organize their learning, stay consistent, track progress, and receive intelligent study guidance.**

---

# 📖 About

Learning today is fragmented.

Students switch between multiple apps for notes, planning, AI assistance, revision, and progress tracking.

- 📒 Notion for notes
- 📅 Google Calendar for scheduling
- 🤖 ChatGPT for doubts
- 📹 YouTube for learning
- 📊 Excel for tracking

**LearnMate AI aims to unify the entire learning experience into one intelligent platform.**

The long-term vision is to build an AI mentor that understands how a student learns, predicts performance, identifies weak concepts, and recommends the next best learning path.

---

# 🎯 Vision

LearnMate AI is being built as a production-grade AI learning platform while documenting the complete engineering journey from backend development to Machine Learning and Agentic AI.

The platform will eventually allow students to:

- 📚 Organize Subjects, Topics & Tasks
- 📝 Create personalized study plans
- 📈 Track learning progress
- 🎯 Build daily study streaks
- 🧠 Detect weak concepts
- 🤖 Receive AI-powered recommendations
- 📊 Predict academic performance using Machine Learning
- 💬 Learn with a personal AI Mentor

---

# ✨ Current Features

## ✅ Backend

- FastAPI Backend
- PostgreSQL Database
- SQLAlchemy ORM
- Layered Architecture
- Automatic Database Initialization
- Swagger API Documentation
- Database Session Management

## ✅ Implemented

- Subject Create API
- Duplicate Subject Validation
- PostgreSQL Integration
- SQLAlchemy Models
- Database Relationships
- Dependency Injection

---

# 🚧 Currently Working On

- Subject Read API
- Subject Update API
- Subject Delete API
- Topic CRUD
- Task CRUD

---

# 🗺️ Development Roadmap

## ✅ Version 1 — Backend Foundation

- [x] FastAPI Setup
- [x] PostgreSQL Integration
- [x] SQLAlchemy ORM
- [x] Database Sessions
- [x] Subject Create API
- [x] Swagger Documentation

---

## 🚧 Version 2 — Complete Backend

- [ ] Subject CRUD
- [ ] Topic CRUD
- [ ] Task CRUD
- [ ] User Authentication (JWT)
- [ ] User-specific Data
- [ ] Progress Tracking

---

## 🔮 Version 3 — AI Features

- [ ] AI Mentor
- [ ] Recommendation Engine
- [ ] Daily Study Planner
- [ ] Analytics Dashboard
- [ ] File Upload
- [ ] Notes Management

---

## 🤖 Version 4 — Machine Learning

- [ ] Student Performance Prediction
- [ ] Personalized Recommendations
- [ ] Weak Topic Detection
- [ ] Learning Pattern Analysis

---

## 🚀 Version 5 — Agentic AI

- [ ] RAG
- [ ] Vector Database
- [ ] Long-Term Memory
- [ ] Multi-Agent Study Assistant
- [ ] Autonomous Learning Planner

---

# 🏗️ Backend Architecture

```
Client
    │
    ▼
FastAPI Router
    │
    ▼
Service Layer
    │
    ▼
SQLAlchemy ORM
    │
    ▼
PostgreSQL
```

---

# 🗄️ Database Architecture

```
User
 │
 └── Subject
        │
        └── Topic
               │
               └── Task
```

> Authentication and User ownership will be introduced in Version 2.

---

# 📂 Project Structure

```
LearnMate-AI/

├── backend/
│   ├── app/
│   │
│   ├── api/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   │
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## Version Control

- Git
- GitHub

## Future Stack

- React
- Tailwind CSS
- Scikit-learn
- LangGraph
- Vector Database
- RAG
- Agentic AI

---

# 🌐 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome Endpoint |
| POST | `/subjects` | Create Subject |

> More endpoints will be added as development progresses.

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/ADxSD-143/LearnMate-AI.git
```

## Move into project

```bash
cd LearnMate-AI/backend
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 🎯 Why This Project?

This project serves two purposes:

1. Build an intelligent AI-powered learning platform.
2. Learn production-level Backend Development, Machine Learning, and Agentic AI by building a real-world software product from scratch.

Instead of building isolated tutorial projects, LearnMate AI evolves continuously while documenting the complete engineering journey.

---

# 👨‍💻 Developer

**Aditya Narayan**

B.Tech Computer Science & Engineering

IIIT Bhubaneswar

---

# ⭐ Support

If you find this project interesting, consider giving it a ⭐ on GitHub.

It motivates further development and helps others discover the project.

---

> 🚀 **Learn smarter. Learn consistently. Learn with AI.**
