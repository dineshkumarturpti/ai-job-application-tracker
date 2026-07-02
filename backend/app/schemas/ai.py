from typing import List, Literal, Optional

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
    application_id: Optional[str] = None


class AnalyzeReport(BaseModel):
    verdict: Literal["Strong Match", "Partial Match", "Needs Work"]
    summary: str
    missingSkills: List[str]
    suggestedKeywords: List[str]
    interviewTopics: List[str]
