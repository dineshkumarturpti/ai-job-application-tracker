# AI Job Application Tracker — Backend

FastAPI backend for the tracker: JWT authentication, PostgreSQL-backed job
application records, and a server-side endpoint that calls OpenAI to compare
a resume against a job description.

Currently implemented: authentication, application CRUD, and the AI resume
analyzer, all covered by tests. Redis caching, Docker, and deployment are
still in progress — see the roadmap in the top-level README.

## Project layout

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router wiring
│   ├── config.py            # Settings, read from .env
│   ├── database.py          # SQLAlchemy engine/session
│   ├── deps.py               # get_current_user auth dependency
│   ├── models/                # SQLAlchemy ORM models (User, Application)
│   ├── schemas/               # Pydantic request/response shapes
│   ├── services/
│   │   ├── security.py        # password hashing + JWT
│   │   └── ai_service.py      # the actual OpenAI call
│   └── routes/
│       ├── auth.py             # POST /auth/register, /auth/login
│       ├── applications.py    # CRUD for job applications
│       └── ai.py                # POST /ai/analyze
├── tests/                    # pytest suite (uses SQLite, no Postgres needed)
├── requirements.txt
└── .env.example
```

## Setup

1. **Install PostgreSQL** if you haven't already, and create a database:
   ```bash
   createdb job_tracker
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up your environment file:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env`:
   - `DATABASE_URL` — point it at your local Postgres instance
   - `SECRET_KEY` — generate one: `python3 -c "import secrets; print(secrets.token_hex(32))"`
   - `OPENAI_API_KEY` — your key from https://platform.openai.com/api-keys

4. **Run it:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Tables are created automatically on first run. Visit
   `http://localhost:8000/docs` for interactive API docs (Swagger UI).

5. **Run the tests** (no Postgres or API key needed — they use SQLite and
   mock the OpenAI call):
   ```bash
   pytest -v
   ```

## API overview

| Method | Path                | Auth required | Purpose |
|--------|----------------------|----------------|---------|
| POST   | `/auth/register`     | No             | Create an account |
| POST   | `/auth/login`        | No             | Get a JWT (form fields: `username`=email, `password`) |
| GET    | `/applications`      | Yes            | List your applications (`?status=applied&search=acme`) |
| POST   | `/applications`      | Yes            | Create an application |
| GET    | `/applications/{id}` | Yes            | Get one application |
| PUT    | `/applications/{id}` | Yes            | Update an application |
| DELETE | `/applications/{id}` | Yes            | Delete an application |
| POST   | `/ai/analyze`        | Yes            | Compare a resume against a job description |

Every `/applications` and `/ai` route expects `Authorization: Bearer <token>`,
where the token comes from `/auth/login`.

### Example: register → login → create an application

```bash
curl -X POST localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"a-real-password"}'

curl -X POST localhost:8000/auth/login \
  -d "username=you@example.com&password=a-real-password"
# -> { "access_token": "...", "token_type": "bearer" }

curl -X POST localhost:8000/applications \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"company":"Aquatic Capital","role":"Quant Researcher","status":"saved"}'
```

### The AI endpoint

```bash
curl -X POST localhost:8000/ai/analyze \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"...","job_description":"...","application_id":"optional-uuid"}'
```

Returns:
```json
{
  "verdict": "Partial Match",
  "summary": "...",
  "missingSkills": ["..."],
  "suggestedKeywords": ["..."],
  "interviewTopics": ["..."]
}
```

The OpenAI API key lives only in `.env` on the server — it's never sent to
or visible from the browser. If you pass `application_id`, the report is
saved onto that application's record (`last_analysis` field) automatically.

The default model is set via `OPENAI_MODEL` in `.env`, so it can be swapped
for a cheaper or more capable one without touching code.

## Known limitations

- Schema is created via `Base.metadata.create_all()`, which is fine for a
  single-developer project but doesn't handle schema changes over time.
  Alembic migrations are the natural next step before this touches a real
  production database.
- No role-based access control yet — a logged-in user can only see and edit
  their own applications, but there's no admin/staff tier.
- Redis caching for repeated AI analyses, Docker packaging, and a deployed
  instance are planned next (tracked in the top-level README's roadmap).
