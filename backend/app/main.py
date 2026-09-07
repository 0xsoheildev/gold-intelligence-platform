from fastapi import FastAPI

from app.api import premium, prices, signals, technical

app = FastAPI(
    title="Gold Intelligence Platform",
    description="API قیمت طلا، تاریخچه، و (به‌زودی) سیگنال هوشمند خرید/فروش",
    version="0.1.0",
)

app.include_router(prices.router)
app.include_router(premium.router)
app.include_router(technical.router)
app.include_router(signals.router)


@app.get("/health")
def health():
    return {"status": "ok"}
