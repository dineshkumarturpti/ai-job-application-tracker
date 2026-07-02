import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON

from ..database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False, default="saved")  # saved|applied|interview|offer|rejected

    link = Column(String, nullable=True)
    deadline = Column(String, nullable=True)  # ISO date string (YYYY-MM-DD)
    resume_version = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    job_description = Column(Text, nullable=True)

    last_analysis = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
