from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.signal import Signal
from app.schemas.signal import SignalOut

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("/current", response_model=SignalOut)
def get_current_signal(
    symbol: str = Query("gold_18k"),
    horizon: str = Query("7D"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Signal)
        .filter(Signal.symbol == symbol, Signal.horizon == horizon)
        .order_by(desc(Signal.generated_at))
        .first()
    )


@router.get("/history", response_model=list[SignalOut])
def get_signal_history(
    symbol: str = Query("gold_18k"),
    horizon: str = Query("7D"),
    limit: int = Query(200, le=2000),
    db: Session = Depends(get_db),
):
    return (
        db.query(Signal)
        .filter(Signal.symbol == symbol, Signal.horizon == horizon)
        .order_by(desc(Signal.generated_at))
        .limit(limit)
        .all()
    )
