# Gold Intelligence Platform — Phase 0/1

این نسخه فقط **Data Ingestion + Raw Storage + API پایه** رو پیاده‌سازی می‌کنه
(طبق فازبندی سند پروژه). هنوز Signal Engine، News، Premium و بقیه نیست —
اول باید مطمئن بشیم این پایه محکمه.

## پیش‌نیاز
- Docker + Docker Compose
- (اختیاری برای اجرای مستقیم بدون Docker) Python 3.11+

## راه‌اندازی سریع

```bash
cp .env.example .env
# GOLDAPI_KEY رو با کلید رایگانت از goldapi.io پر کن

docker compose up -d db      # فقط دیتابیس رو بالا بیار
docker compose up backend    # API روی http://localhost:8000
```

مستندات API خودکار: http://localhost:8000/docs

## اجرای ingestion (fetcher ها)

فعلاً جدا از backend service اجرا می‌شه (در فازهای بعد به Celery/Kafka منتقل می‌شه):

```bash
cd ingestion
pip install -r ../backend/requirements.txt
export DATABASE_URL=postgresql+psycopg2://gold_user:gold_pass@localhost:5432/gold_intelligence
export GOLDAPI_KEY=your_key
python -m ingestion.scheduler
```

این هر ۱۰ دقیقه (قابل تنظیم با `FETCH_INTERVAL_MINUTES`) دو منبع رو fetch می‌کنه:
- **tgju** (ایران): طلای ۱۸، سکه امامی، نیم/ربع سکه، نرخ دلار
- **goldapi** (جهانی): XAU/USD

## چک کردن نتیجه

```bash
curl http://localhost:8000/prices/live
curl "http://localhost:8000/prices/history?symbol=gold_18k&limit=50"
```

## نکات مهم قبل از استفاده‌ی واقعی

1. **selectors سایت tgju رو verify کن** — ساختار HTML سایت‌های ایرانی مدام
   تغییر می‌کنه؛ `ingestion/sources/tgju_source.py` رو با inspect کردن صفحه‌ی
   واقعی به‌روزرسانی کن.
2. کلید GoldAPI رایگان محدودیت درخواست داره — برای تست کافیه، برای production
   باید پلن مناسب بگیری یا منبع جایگزین (metals-api.com) اضافه کنی.
3. این فاز **بدون Data Quality Layer** هست — یعنی اگه یه منبع قیمت غلط بده،
   فعلاً فیلتر نمی‌شه. این در فاز ۶ اضافه می‌شه (طبق سند پروژه).

## قدم بعدی
طبق نقشه‌ی راه: Phase 2 (Premium Engine) و Phase 3 (Technical Engine).
