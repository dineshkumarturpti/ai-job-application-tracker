# 🗂️ AI Job Application Tracker

> A full-stack AI-powered job application tracker — track every application, analyze your resume against any job description, and get back a verdict with missing skills, suggested keywords, and interview prep topics.
> **Status:** Auth, application CRUD, and the AI resume analyzer are built, tested, and wired end-to-end between the frontend and the FastAPI backend. Redis caching, Docker packaging, and a deployed instance are next — see Roadmap below.

[![Backend CI](https://github.com/dineshkumarturpti/ai-job-application-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/dineshkumarturpti/ai-job-application-tracker/actions)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- 🔐 User registration & login with **JWT authentication**
- 📋 Create, edit, delete job applications
- 🎯 Track status: **Saved → Applied → Interview → Offer / Rejected**
- 🗃️ Store job description, resume version, notes, deadline, and job link
- 📊 **Kanban board** with drag-and-drop between stages
- 🔍 Table view with search and status filters
- 🤖 **AI Resume Analyzer** — paste your resume + job description and get:
  - ✅ Match verdict (Strong Match / Partial Match / Needs Work)
  - 📌 Missing skills
  - 🔑 Suggested keywords to add to your resume
  - 🎤 Likely interview topics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Vanilla JS (ES6+), CSS3 |
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Auth | JWT (PyJWT + bcrypt) |
| AI | OpenAI API via a server-side call (model configurable via `.env`) |
| Caching | Redis *(planned)* |
| Containers | Docker + Docker Compose *(planned)* |
| CI/CD | GitHub Actions |
| Deployment | *(planned)* |

---

## 📁 Project structure

```
ai-job-application-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app, CORS, router wiring
│   │   ├── config.py          # Settings, read from .env
│   │   ├── database.py        # SQLAlchemy engine/session
│   │   ├── deps.py             # get_current_user auth dependency
│   │   ├── models/              # SQLAlchemy ORM models (User, Application)
│   │   ├── schemas/             # Pydantic request/response shapes
│   │   ├── services/            # password hashing + JWT, the OpenAI call
│   │   └── routes/              # /auth, /applications, /ai
│   ├── tests/                 # pytest suite (SQLite, no Postgres needed)
│   ├── requirements.txt
│   └── README.md              # backend-specific setup and API reference
├── frontend/
│   └── index.html             # single-file UI (Kanban board, table view, AI panel)
├── .github/workflows/ci.yml   # pytest on every push
└── README.md                  # you are here
```

## 🚀 Quickstart

**1. Start the backend** (see `backend/README.md` for full details):

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL, SECRET_KEY, OPENAI_API_KEY
uvicorn app.main:app --reload
```

The API is now live at `http://localhost:8000` (interactive docs at `/docs`).

**2. Serve the frontend** from the repo root, on a port the backend's CORS
config already allows:

```bash
cd frontend
python3 -m http.server 5173
```

Open `http://localhost:5173`, create an account, and you're in. The
frontend talks to the backend at `http://localhost:8000` by default — set
`window.API_BASE` before the page's script runs if you're pointing it
somewhere else.

**3. Run the tests:**

```bash
cd backend
pytest -v
```

## 🗺️ Roadmap

- [x] JWT auth, application CRUD, AI resume analyzer
- [x] Frontend wired to the live backend (Kanban board, table view, AI panel)
- [x] Test suite + CI on every push
- [ ] Redis caching for repeated AI analyses
- [ ] Docker + Docker Compose for one-command local setup
- [ ] Alembic migrations instead of `create_all()`
- [ ] Deployed instance with a live demo link

## License

MIT — see [LICENSE](LICENSE).
