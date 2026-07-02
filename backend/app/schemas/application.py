from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict

StatusType = Literal["saved", "applied", "interview", "offer", "rejected"]


class ApplicationBase(BaseModel):
    company: str
    role: str
    status: StatusType = "saved"
    link: Optional[str] = None
    deadline: Optional[str] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    job_description: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[StatusType] = None
    link: Optional[str] = None
    deadline: Optional[str] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    job_description: Optional[str] = None


class ApplicationOut(ApplicationBase):
    id: str
    last_analysis: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
