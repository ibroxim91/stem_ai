FROM python:3.11-slim

# Ishchi katalogni o'rnatish
WORKDIR /app

# Fayllarni nusxalash
COPY . /app/

# Get fonts
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    && rm -rf /var/lib/apt/lists/*
# Kutubxonalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Migrations, collectstatic va serverni ishga tushirish uchun bash script ishlatamiz
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
