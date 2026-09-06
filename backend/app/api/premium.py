from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.premium import GoldPremium
from app.schemas.premium import PremiumOut

router = APIRouter(prefix="/premium", tags=["premium"])


@router.get("/current", response_model=PremiumOut)
def get_current_premium(
    symbol: str = Query("gold_18k"),
    db: Session = Depends(get_db),
):
    return (
        db.query(GoldPremium)
        .filter(GoldPremium.symbol == symbol)
        .order_by(desc(GoldPremium.computed_at))
        .first()
    )


@router.get("/history", response_model=list[PremiumOut])
def get_premium_history(
    symbol: str = Query("gold_18k"),
    limit: int = Query(200, le=2000),
    db: Session = Depends(get_db),
):
    return (
        db.query(GoldPremium)
        .filter(GoldPremium.symbol == symbol)
        .order_by(desc(GoldPremium.computed_at))
        .limit(limit)
        .all()
    )
