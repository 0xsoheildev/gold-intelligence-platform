from fastapi import FastAPI

from app.api import news, premium, prices, quality, signals, technical

app = FastAPI(
    title="Gold Intelligence Platform",
    description="API قیمت طلا، تاریخچه، و (به‌زودی) سیگنال هوشمند خرید/فروش",
    version="0.1.0",
)

app.include_router(prices.router)
app.include_router(premium.router)
app.include_router(technical.router)
app.include_router(signals.router)
app.include_router(news.router)
app.include_router(quality.router)


@app.get("/health")
def health():
    return {"status": "ok"}
