from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.analytics_repository import (
    AnalyticsRepository,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)


@router.get("")
def get_analytics(
    db: Session = Depends(get_db),
):
    repository = AnalyticsRepository(db)
    service = AnalyticsService(repository)

    return service.get_analytics()