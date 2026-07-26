# NeuralDesk

> A multi-tenant AI chatbot platform built with **FastAPI**, **React**, **PostgreSQL**, and pluggable **LLM providers** (OpenAI, Groq, and OpenRouter). Designed with clean architecture, JWT authentication, streaming responses, and modular backend services.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![License](https://img.shields.io/badge/License-MIT-success)

---

## Live Demo

**Frontend**

https://neuraldesk-puce.vercel.app

**Backend API**

https://YOUR-RAILWAY-URL.up.railway.app/docs

**Architecture Document**

See [ARCHITECTURE.md](./ARCHITECTURE.md)

---

# Screenshots

> *(Replace these with your own screenshots.)*

## Login

![Login](./screenshots/login.png)

## Dashboard

![Dashboard](./screenshots/dashboard.png)

## Chat

![Chat](./screenshots/chat.png)

---

# Overview

NeuralDesk is a multi-tenant chatbot platform where every user can create multiple AI agents ("Projects"), each with its own:

- System Prompt
- LLM Provider
- AI Model
- Temperature
- Prompt Library
- Conversation History

The platform supports configurable providers through a provider abstraction layer, allowing projects to seamlessly switch between OpenAI, Groq, and OpenRouter without changing business logic.

---

# Features

- JWT Authentication
- User Registration & Login
- Secure Password Hashing (bcrypt)
- AI Project Management (CRUD)
- Prompt Library per Project
- Multiple Conversation Threads
- Streaming Chat Responses (SSE)
- OpenAI / Groq / OpenRouter Support
- File Upload Support
- Protected Backend APIs
- PostgreSQL Persistence

---

# Tech Stack

| Layer | Technology |
|---------|------------|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS |
| State Management | Zustand |
| Backend | FastAPI |
| ORM | SQLAlchemy Async |
| Database | PostgreSQL (Neon) |
| Authentication | JWT + bcrypt |
| AI Providers | OpenAI, Groq, OpenRouter |
| Deployment | Vercel + Railway |

---

# LLM Provider Abstraction

The platform uses an abstraction layer that separates business logic from AI providers.

Every provider implements the same interface:

```python
LLMProvider
    ├── OpenAI
    ├── Groq
    └── OpenRouter
```

This makes switching providers a configuration change instead of an application rewrite.

During development, OpenAI's free-tier quota was exhausted, so the project was switched to Groq without requiring changes to the service layer.

---

# High-Level Architecture

```
                React + Vite
                      │
                Axios API Calls
                      │
──────────────────────▼──────────────────────
                FastAPI Backend
                      │
        ┌─────────────┼─────────────┐
        │             │             │
      Routes      Services      Repositories
        │             │             │
        └─────────────▼─────────────┘
                PostgreSQL (Neon)

                      │

          LLM Provider Factory

        OpenAI • Groq • OpenRouter
```

For a detailed explanation of the architecture, design decisions, database schema, scalability, and security, see:

**ARCHITECTURE.md**

---

# Repository Layout

```
neuraldesk/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── llm/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── schemas/
│   │
│   ├── requirements.txt
│   └── create_tables.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── store/
│   │   └── hooks/
│
├── ARCHITECTURE.md
├── README.md
└── LICENSE
```

---

# Running Locally

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

---

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Configure your environment variables:

```env
DATABASE_URL=

SECRET_KEY=

OPENAI_API_KEY=

GROQ_API_KEY=

OPENROUTER_API_KEY=
```

Create the database:

```bash
python create_tables.py
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register |
| POST | `/auth/login` | Login |
| GET | `/auth/me` | Current User |
| POST | `/projects` | Create Project |
| GET | `/projects` | List Projects |
| PUT | `/projects/{id}` | Update Project |
| DELETE | `/projects/{id}` | Delete Project |
| POST | `/chat` | Stream AI Response |
| POST | `/prompts` | Create Prompt |
| POST | `/files` | Upload File |

---

# Deployment

## Frontend

**Platform:** Vercel

```
Build Command:
npm run build

Output Directory:
dist
```

---

## Backend

**Platform:** Railway

Environment variables are configured through Railway's dashboard.

The FastAPI application is served using:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

# Future Improvements

- Redis caching
- Vector database integration (RAG)
- Anthropic & Gemini support
- Team workspaces
- Role-based permissions
- Rate limiting
- Analytics dashboard
- Observability & tracing

---

# License

This project is licensed under the MIT License.

---

## Author

**Kshitisha Negi**

GitHub:
https://github.com/kshitisha

LinkedIn:
https://linkedin.com/in/YOUR-LINKEDIN

Portfolio:
https://YOUR-PORTFOLIO
