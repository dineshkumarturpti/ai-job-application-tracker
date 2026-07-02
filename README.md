# AI Job Application Tracker

A full-stack AI-powered job application tracker built with **React (HTML/JS), FastAPI, PostgreSQL, OpenAI, Docker, and GitHub Actions CI/CD**.

Track every job application through a visual Kanban board, analyze your resume against any job description using AI, and get back a verdict, missing skills, suggested keywords, and interview prep topics — all stored securely per user.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Vanilla JS (ES6+), CSS3 |
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Auth | JWT (PyJWT + bcrypt) |
| AI | OpenAI API (`gpt-5.4-mini`) via server-side call |
| Caching | Redis *(Phase 3 — coming soon)* |
| Containers | Docker + Docker Compose *(Phase 4 — coming soon)* |
| CI/CD | GitHub Actions *(Phase 5 — coming soon)* |
| Deployment | AWS EC2 *(Phase 6 — coming soon)* |

---

## Features

- ✅ User registration & login with JWT-based authentication
- ✅ Create, edit, delete job applications
- ✅ Track status: **Saved → Applied → Interview → Offer / Rejected**
- ✅ Store job description, resume version, notes, deadline, and job link per application
- ✅ Kanban board with drag-and-drop
- ✅ Table view with search and filters
- ✅ Dashboard showing total applications, interviews, offers, and rejections
- ✅ **AI resume analyzer** — paste your resume and the job description; the backend calls OpenAI and returns:
  - Match verdict (Strong / Partial / Needs Work)
  - Missing skills
  - Suggested keywords to add to your resume
  - Likely interview topics
- ✅ Analysis results saved to the linked application record

---

## Project Structure

```
ai-job-application-tracker/
│
├── frontend/
│   └── index.html              # Full tracker UI (Kanban, table, AI case file)
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py             # App entry point, CORS, router wiring
│   │   ├── config.py           # Settings from .env
│   │   ├── database.py         # SQLAlchemy engine + session
│   │   ├── deps.py             # Auth dependency (get_current_user)
│   │   ├── models/             # ORM models: User, Application
│   │   ├── schemas/            # Pydantic request/response shapes
│   │   ├── services/
│   │   │   ├── security.py     # Password hashing + JWT helpers
│   │   │   └── ai_service.py   # OpenAI Structured Output call
│   │   └── routes/
│   │       ├── auth.py         # POST /auth/register, /auth/login
│   │       ├── applications.py # Full CRUD for applications
│   │       └── ai.py           # POST /ai/analyze
│   ├── tests/                  # pytest suite (7 tests, SQLite, no real API key needed)
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md               # Backend-specific setup guide
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions: test on every push + PR
│
├── .gitignore
└── README.md                   # ← you are here
```

---

## Quick Start

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set DATABASE_URL, SECRET_KEY, and OPENAI_API_KEY

uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs
```

### 2. Frontend

Open `frontend/index.html` in your browser. Point the `API_BASE` constant at
the backend URL (default `http://localhost:8000`).

> The frontend currently uses Claude.ai's artifact storage when opened inside
> Claude.ai. To use it as a standalone file connected to this backend, update
> `API_BASE` and replace the storage calls with `fetch` calls to the API.

### 3. Tests (no Postgres or OpenAI key needed)

```bash
cd backend
pytest -v
```

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Get JWT token |
| GET | `/applications` | Yes | List applications (`?status=&search=`) |
| POST | `/applications` | Yes | Create application |
| GET | `/applications/{id}` | Yes | Get one application |
| PUT | `/applications/{id}` | Yes | Update application |
| DELETE | `/applications/{id}` | Yes | Delete application |
| POST | `/ai/analyze` | Yes | AI resume vs job description analysis |
| GET | `/health` | No | Health check |

---

## Roadmap

- [ ] Phase 3: Redis caching for AI results (skip redundant API calls)
- [ ] Phase 4: Docker + Docker Compose (containerise all services)
- [ ] Phase 5: GitHub Actions full CI/CD pipeline
- [ ] Phase 6: Deploy backend to AWS EC2, frontend to Vercel or S3

---

## License

MIT
