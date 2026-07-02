from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routes import ai, applications, auth

# Creates tables if they don't exist yet. Fine for an early-stage project --
# swap in Alembic migrations once the schema needs to evolve safely in production.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Job Application Tracker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(ai.router)


@app.get("/health")
def health():
    return {"status": "ok"}
