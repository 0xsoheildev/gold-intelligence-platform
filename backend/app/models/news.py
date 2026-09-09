from sqlalchemy import Column, BigInteger, String, Text, Numeric, TIMESTAMP, JSON

from app.core.db import Base


class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(BigInteger, primary_key=True)
    source = Column(String, nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False, unique=True)
    summary = Column(Text, nullable=True)
    published_at = Column(TIMESTAMP(timezone=True), nullable=True)
    fetched_at = Column(TIMESTAMP(timezone=True), nullable=False)
    event = Column(String, nullable=True)
    assets = Column(JSON, nullable=True)
    direction = Column(String, nullable=True)
    importance = Column(Numeric, nullable=True)
    classified_at = Column(TIMESTAMP(timezone=True), nullable=True)
