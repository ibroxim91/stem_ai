FROM python:3.11-slim

# Ishchi katalogni o'rnatish
WORKDIR /app

# Fayllarni nusxalash
COPY . /app/

# Kutubxonalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Migrations, collectstatic va serverni ishga tushirish uchun bash script ishlatamiz
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && uvicorn config.asgi:application --host 0.0.0.0 --port 8000"]
