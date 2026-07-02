from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models.application import Application
from ..models.user import User
from ..schemas.ai import AnalyzeReport, AnalyzeRequest
from ..services.ai_service import analyze_resume

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze", response_model=AnalyzeReport)
def analyze(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not payload.resume_text.strip() or not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Both resume_text and job_description are required")

    try:
        report = analyze_resume(payload.resume_text, payload.job_description)
    except RuntimeError as exc:
        # OPENAI_API_KEY missing -- a server misconfiguration, not the caller's fault.
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not complete the analysis: {exc}")

    if payload.application_id:
        application = (
            db.query(Application)
            .filter(Application.id == payload.application_id, Application.owner_id == current_user.id)
            .first()
        )
        if application:
            application.last_analysis = {**report, "ranAt": datetime.now(timezone.utc).isoformat()}
            db.commit()

    return report
