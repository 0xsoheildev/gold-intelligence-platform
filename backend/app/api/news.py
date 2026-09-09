from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.news import NewsItem
from app.schemas.news import NewsItemOut

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/recent", response_model=list[NewsItemOut])
def get_recent_news(
    classified_only: bool = Query(True),
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(NewsItem)
    if classified_only:
        q = q.filter(NewsItem.classified_at.isnot(None))
    return q.order_by(desc(NewsItem.fetched_at)).limit(limit).all()
