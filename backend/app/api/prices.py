from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.price import RawPrice
from app.schemas.price import PriceOut

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/live", response_model=list[PriceOut])
def get_live_prices(db: Session = Depends(get_db)):
    """
    آخرین قیمت ثبت‌شده برای هر (source, symbol).
    فاز ۱: ساده و مستقیم؛ فاز ۶ این‌جا consensus_prices جایگزین میشه.
    """
    subquery = (
        db.query(
            RawPrice.source,
            RawPrice.symbol,
            RawPrice.price,
            RawPrice.currency,
            RawPrice.fetched_at,
        )
        .order_by(RawPrice.source, RawPrice.symbol, desc(RawPrice.fetched_at))
        .distinct(RawPrice.source, RawPrice.symbol)
    )
    return subquery.all()


@router.get("/history", response_model=list[PriceOut])
def get_price_history(
    symbol: str = Query(..., description="مثلا gold_18k یا xau_usd"),
    source: str | None = Query(None),
    limit: int = Query(200, le=2000),
    db: Session = Depends(get_db),
):
    q = db.query(RawPrice).filter(RawPrice.symbol == symbol)
    if source:
        q = q.filter(RawPrice.source == source)
    return q.order_by(desc(RawPrice.fetched_at)).limit(limit).all()
