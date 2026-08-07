<div align="center">

# 🚀 LearnMate AI

### *Your Personal AI Learning Companion*

An AI-powered personalized learning platform that helps students **learn smarter, stay consistent, track progress, receive intelligent study recommendations, and connect with the right learning partners.**

---

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)
![License](https://img.shields.io/badge/License-MIT-green)

> **Learn smarter. Learn consistently. Learn with AI.**

</div>

---

# 📖 About

Modern students use different applications for different purposes.

- 📒 Notion for notes
- 📅 Google Calendar for planning
- 📹 YouTube for learning
- 🤖 ChatGPT for doubts
- 📊 Excel for progress tracking
- 📁 Google Drive for resources

Everything is scattered.

LearnMate AI aims to combine all of these into a single intelligent platform.

Instead of being another task manager, LearnMate AI is designed to become an AI-powered learning ecosystem that understands every student's learning journey and continuously helps them improve.

---

# 🎯 Vision

The vision is to build a production-grade AI learning platform that combines:

- Backend Engineering
- Artificial Intelligence
- Machine Learning
- Recommendation Systems
- Data Analytics
- Agentic AI

Eventually, LearnMate AI should be capable of acting as a personal mentor that guides students from their first semester to internships, placements, higher studies, and lifelong learning.

---

# 🌟 Core Features

## 📚 Learning Management

- Subject Management
- Topic Management
- Task Management
- Daily Planner
- Smart Revision Scheduler
- Learning Goals
- Progress Tracking
- Learning Streaks

---

## 🤖 AI Features

- AI Mentor
- AI Doubt Assistant
- Personalized Study Roadmaps
- Smart Revision Recommendations
- Resource Recommendation
- Automatic Weak Topic Detection
- AI-generated Study Plans

---

## 📊 Machine Learning

- Student Performance Prediction
- Personalized Recommendation Engine
- Productivity Prediction
- Learning Pattern Analysis
- Consistency Score
- Weak Subject Detection

---

## 👥 Social Learning

### 🤝 1-to-1 Peer Learning

One of the core features of LearnMate AI.

Instead of randomly connecting students, the system intelligently recommends the **best study partner** based on:

- Current Subjects
- Learning Goals
- Skill Level
- Interests
- Preferred Learning Style
- Availability
- Progress
- Consistency

Examples:

- Learning Python? → Match with another Python learner.
- Preparing for DSA Interviews? → Connect with someone solving similar problems.
- Learning Machine Learning? → Find students at a similar level.

Future versions may also support:

- Study Groups
- Mentor Matching
- Pair Programming
- Live Collaborative Sessions

---

# ✨ Current Progress

## ✅ Completed

### Backend

- FastAPI Backend
- PostgreSQL Integration
- SQLAlchemy ORM
- Layered Architecture
- Database Session Management
- Automatic Table Creation
- Dependency Injection
- Swagger Documentation

### APIs

- Subject Create API
- Subject Validation
- Duplicate Subject Prevention

---

## 🚧 In Progress

- Subject CRUD
- Topic CRUD
- Task CRUD
- User Authentication
- JWT Authentication
- User-specific Subjects

---

## 🔮 Planned

- Daily Planner
- AI Mentor
- Recommendation Engine
- Analytics Dashboard
- Machine Learning Models
- React Frontend
- Mobile Application

---

# 🗺️ Development Roadmap

## ✅ Version 1 — Backend Foundation

- [x] FastAPI
- [x] PostgreSQL
- [x] SQLAlchemy
- [x] Swagger
- [x] Subject Create API
- [x] Layered Architecture

---

## 🚧 Version 2 — Complete Backend

- [ ] Subject CRUD
- [ ] Topic CRUD
- [ ] Task CRUD
- [ ] JWT Authentication
- [ ] User Management
- [ ] Progress Tracking

---

## 🚀 Version 3 — AI Features

- [ ] AI Mentor
- [ ] Recommendation Engine
- [ ] AI Doubt Assistant
- [ ] Smart Revision Planner
- [ ] Analytics Dashboard

---

## 🤖 Version 4 — Machine Learning

Models planned:

- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest
- XGBoost
- LightGBM
- CatBoost

Applications:

- Performance Prediction
- Recommendation Engine
- Weak Topic Detection
- Productivity Analysis
- Learning Behaviour Analysis

---

## 🧠 Version 5 — Agentic AI

- Long-term Memory
- RAG
- Vector Database
- Autonomous AI Mentor
- Multi-Agent Learning Assistant
- Personalized AI Coach

---

# 🏗️ System Architecture

```text
                           User
                             │
                             ▼
                    React Frontend
                       (Future)
                             │
                        REST API
                             │
                             ▼
                   FastAPI Backend
                             │
        ┌────────────┬─────────────┬────────────┐
        ▼            ▼             ▼
    Authentication  Learning APIs   AI APIs
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

```text
User
 │
 ├── Subject
 │      │
 │      ├── Topic
 │      │      │
 │      │      ├── Task
 │      │      │      │
 │      │      │      └── Progress
 │      │      │
 │      │      └── AI Recommendation
 │      │
 │      └── Analytics
 │
 └── Learning Partner
```

---

# 📂 Project Structure

```text
LearnMate-AI/

├── backend/
│
│   ├── app/
│   │
│   ├── api/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── ml/
│   ├── utils/
│   └── main.py
│
├── frontend/
│
├── docs/
│
├── datasets/
│
├── notebooks/
│
└── README.md
```

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

---

## Frontend (Planned)

- React
- Tailwind CSS

---

## Artificial Intelligence

- OpenAI
- LangGraph
- RAG
- Vector Database

---

## Machine Learning

- Scikit-learn
- XGBoost
- LightGBM
- CatBoost
- Pandas
- NumPy

---

## Dev Tools

- Git
- GitHub
- Postman
- Swagger UI
- pgAdmin

---

# 🌐 Current API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome Endpoint |
| POST | `/subjects` | Create Subject |

> More APIs will be added as development progresses.

---

# 🚀 Getting Started

## Clone

```bash
git clone https://github.com/ADxSD-143/LearnMate-AI.git
```

---

## Navigate

```bash
cd LearnMate-AI/backend
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# 💡 Why This Project?

LearnMate AI is not just another CRUD project.

It is a long-term engineering project focused on building an intelligent learning ecosystem while documenting the complete journey of learning:

- Backend Engineering
- Software Architecture
- Databases
- Machine Learning
- Recommendation Systems
- Agentic AI

Every feature is implemented incrementally with the goal of evolving into a real-world AI product.

---

# 👨‍💻 Developer

**Aditya Narayan**

B.Tech Computer Science & Engineering

IIIT Bhubaneswar

---

# ⭐ Contributing

Contributions, suggestions, and feature ideas are always welcome.

Feel free to open an Issue or Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

## ⭐ If you like this project, consider giving it a star.

**Learn smarter. Learn consistently. Learn with AI. 🚀**

</div>
