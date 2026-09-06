from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.technical import TechnicalIndicators
from app.schemas.technical import TechnicalOut

router = APIRouter(prefix="/technical", tags=["technical"])


@router.get("/current", response_model=TechnicalOut)
def get_current_technical(
    symbol: str = Query("gold_18k"),
    db: Session = Depends(get_db),
):
    return (
        db.query(TechnicalIndicators)
        .filter(TechnicalIndicators.symbol == symbol)
        .order_by(desc(TechnicalIndicators.computed_at))
        .first()
    )


@router.get("/history", response_model=list[TechnicalOut])
def get_technical_history(
    symbol: str = Query("gold_18k"),
    limit: int = Query(200, le=2000),
    db: Session = Depends(get_db),
):
    return (
        db.query(TechnicalIndicators)
        .filter(TechnicalIndicators.symbol == symbol)
        .order_by(desc(TechnicalIndicators.computed_at))
        .limit(limit)
        .all()
    )
