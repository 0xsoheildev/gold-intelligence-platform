from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.quality import ConsensusPrice, SourceReliability
from app.schemas.quality import ConsensusPriceOut, SourceReliabilityOut

router = APIRouter(prefix="/quality", tags=["quality"])


@router.get("/consensus/current", response_model=ConsensusPriceOut)
def get_current_consensus(
    symbol: str = Query("gold_18k"),
    db: Session = Depends(get_db),
):
    return (
        db.query(ConsensusPrice)
        .filter(ConsensusPrice.symbol == symbol)
        .order_by(desc(ConsensusPrice.computed_at))
        .first()
    )


@router.get("/consensus/history", response_model=list[ConsensusPriceOut])
def get_consensus_history(
    symbol: str = Query("gold_18k"),
    limit: int = Query(200, le=2000),
    db: Session = Depends(get_db),
):
    return (
        db.query(ConsensusPrice)
        .filter(ConsensusPrice.symbol == symbol)
        .order_by(desc(ConsensusPrice.computed_at))
        .limit(limit)
        .all()
    )


@router.get("/reliability", response_model=list[SourceReliabilityOut])
def get_source_reliability(db: Session = Depends(get_db)):
    return db.query(SourceReliability).order_by(desc(SourceReliability.reliability)).all()
