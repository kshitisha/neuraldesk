# NeuralDesk — Production-Grade Chatbot Platform

> A multi-tenant AI chatbot platform built as a hiring assessment for a Senior AI Engineer role. Designed with production software practices: clean architecture, LLM provider abstraction, streaming responses, and JWT authentication.

**Live Demo:** https://neuraldesk-puce.vercel.app/login  
**Backend API Docs:** https://your-railway-url.up.railway.app/docs  
**GitHub:** https://github.com/kshitisha/neuraldesk

---

## What It Does

NeuralDesk lets users create AI "projects" — each project is a configurable AI agent with its own system prompt, model, temperature, and prompt library. Users can have multiple projects, each with multiple conversation threads, and chat with agents in real-time via streaming responses.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.11), async |
| Database | PostgreSQL (Neon serverless) |
| ORM | SQLAlchemy 2.0 async |
| Auth | JWT (HS256), bcrypt password hashing |
| LLM Providers | OpenAI, Groq, OpenRouter (swappable via factory pattern) |
| Frontend | React + TypeScript + Vite |
| State Management | Zustand |
| Styling | Tailwind CSS v4 |
| Deployment | Railway (backend) + Vercel (frontend) |

---

## A Note on LLM Provider

The assignment specifies the OpenAI Responses API. During development, the OpenAI free-tier quota was exhausted. Rather than block progress, I made use of the LLM abstraction layer built into the architecture to swap in **Groq** — a free-tier LLM provider with an OpenAI-compatible API that offers extremely fast inference via their LPU hardware.

This swap required **zero changes to business logic** — only the provider name in the project config changes. This is exactly why the abstraction layer was designed this way: the system supports OpenAI, Groq, and OpenRouter interchangeably. To switch back to OpenAI, set `provider: "openai"` when creating a project and supply a valid key.

---

## Features

- User registration and login with JWT authentication
- Create, edit, and delete AI projects (agents)
- Per-project configuration: system prompt, model, temperature, provider
- Prompt library per project — reusable prompts injectable into chat
- Multiple conversation threads per project
- Real-time streaming chat via Server-Sent Events (SSE)
- File upload to OpenAI Files API (stored with project metadata)
- Full CRUD on projects and prompts
- Protected routes on both frontend and backend

---

## Running Locally

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your DATABASE_URL, SECRET_KEY, and API keys

# Create database tables
python create_tables.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Environment Variables

Create `backend/.env` with the following:

```env
APP_ENV=development
APP_NAME=NeuralDesk
DEBUG=true

DATABASE_URL=postgresql+asyncpg://user:password@host:5432/neuraldesk

SECRET_KEY=your-secret-key-minimum-32-characters

OPENAI_API_KEY=sk-your-openai-key
GROQ_API_KEY=your-groq-api-key
OPENROUTER_API_KEY=your-openrouter-key
DEFAULT_PROVIDER=groq

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | ❌ | Register new user |
| POST | `/api/v1/auth/login` | ❌ | Login, get tokens |
| POST | `/api/v1/auth/refresh` | ❌ | Refresh access token |
| GET | `/api/v1/auth/me` | ✅ | Get current user |
| GET | `/api/v1/projects` | ✅ | List user's projects |
| POST | `/api/v1/projects` | ✅ | Create project |
| GET | `/api/v1/projects/{id}` | ✅ | Get project |
| PUT | `/api/v1/projects/{id}` | ✅ | Update project |
| DELETE | `/api/v1/projects/{id}` | ✅ | Delete project |
| GET | `/api/v1/projects/{id}/prompts` | ✅ | List prompt library |
| POST | `/api/v1/projects/{id}/prompts` | ✅ | Add prompt |
| DELETE | `/api/v1/projects/{id}/prompts/{pid}` | ✅ | Delete prompt |
| POST | `/api/v1/projects/{id}/conversations` | ✅ | Start conversation |
| GET | `/api/v1/projects/{id}/conversations` | ✅ | List conversations |
| GET | `/api/v1/projects/{id}/conversations/{cid}/messages` | ✅ | Load messages |
| POST | `/api/v1/projects/{id}/conversations/{cid}/chat` | ✅ | Chat (SSE stream) |
| POST | `/api/v1/projects/{id}/files` | ✅ | Upload file |
| GET | `/api/v1/projects/{id}/files` | ✅ | List files |
| DELETE | `/api/v1/projects/{id}/files/{fid}` | ✅ | Delete file |

---

## Deployment

### Backend — Railway

1. Connect GitHub repo to Railway
2. Set root directory to `backend/`
3. Add all environment variables in the Variables tab
4. Railway auto-detects Python and runs `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend — Vercel

1. Connect GitHub repo to Vercel
2. Set root directory to `frontend/`
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VITE_API_URL=https://your-railway-url.up.railway.app`

---

## Project Structure

```
neuraldesk/
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/     # Auth, projects, chat, files
│   │   ├── core/              # Config, security, exceptions
│   │   ├── db/models/         # SQLAlchemy models
│   │   ├── repositories/      # Data access layer
│   │   ├── services/          # Business logic
│   │   ├── llm/               # LLM abstraction layer
│   │   └── schemas/           # Pydantic request/response schemas
│   ├── requirements.txt
│   └── create_tables.py
└── frontend/
    └── src/
        ├── api/               # Typed API client
        ├── pages/             # Login, Register, Dashboard, Chat
        ├── store/             # Zustand state
        └── hooks/             # useChat, useAuth
```
