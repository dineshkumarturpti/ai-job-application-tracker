from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models.application import Application
from ..models.user import User
from ..schemas.application import ApplicationCreate, ApplicationOut, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=List[ApplicationOut])
def list_applications(
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Application).filter(Application.owner_id == current_user.id)
    if status_filter:
        query = query.filter(Application.status == status_filter)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Application.company.ilike(like)) | (Application.role.ilike(like))
        )
    return query.order_by(Application.created_at.desc()).all()


@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = Application(owner_id=current_user.id, **payload.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def _get_owned_application(app_id: str, db: Session, current_user: User) -> Application:
    application = (
        db.query(Application)
        .filter(Application.id == app_id, Application.owner_id == current_user.id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("/{app_id}", response_model=ApplicationOut)
def get_application(
    app_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_owned_application(app_id, db, current_user)


@router.put("/{app_id}", response_model=ApplicationOut)
def update_application(
    app_id: str,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = _get_owned_application(app_id, db, current_user)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    app_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = _get_owned_application(app_id, db, current_user)
    db.delete(application)
    db.commit()
    return None
