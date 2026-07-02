# AI Job Application Tracker — Backend

FastAPI backend for the tracker: JWT authentication, PostgreSQL-backed job
application records, and a server-side endpoint that calls OpenAI to compare
a resume against a job description. This is Phase 1 + Phase 2 of the original
build plan (core tracker + AI features). Redis caching, Docker, CI, and AWS
deployment are the next phases once this is working for you locally.

## What's actually been verified

This isn't just generated and handed to you — before delivery:
- `pip install -r requirements.txt` was run clean
- The full test suite (7 tests covering auth, CRUD, ownership isolation, and
  the AI endpoint) was run and passes
- The app was booted end-to-end and every route was confirmed registered

The one thing **not** verified here is a live PostgreSQL connection (this
environment couldn't install Postgres), so double-check that step on your
machine. Everything else — the actual logic — has been exercised.

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

The model used is `gpt-5.4-mini` by default (set via `OPENAI_MODEL` in
`.env`) — fast and inexpensive, which is the right tradeoff for this kind of
text-comparison task. Swap in `gpt-5.5` if you want deeper reasoning at
higher cost.

## Connecting this to a frontend

This backend is framework-agnostic on the frontend side — point any client
at it with `fetch`/`axios`, storing the JWT (e.g. in memory or a cookie) and
sending it as `Authorization: Bearer <token>` on every `/applications` and
`/ai` request.

If you want, I can wire this directly into the HTML tracker we already
built — swapping its `window.storage` calls and direct Claude call for real
`fetch` calls to this API — just ask.

## Honest notes for your resume

- Don't claim a specific cache-hit percentage (e.g. "75% reduction in API
  calls") unless you've actually added Redis caching and measured it —
  that's Phase 3, not built yet.
- `Base.metadata.create_all()` is used for schema setup, which is fine for a
  personal project but not how you'd manage schema changes in a real
  production app — mention Alembic migrations as a "next step" if asked
  about it in an interview, rather than pretending it's already there.
