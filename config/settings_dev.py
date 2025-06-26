import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stem_ai_2',
        'USER': os.environ.get('DB_USER', 'user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '12345'),
        'HOST': 'localhost',# os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

FRONT_URL = "https://sinaps-ai-client.vercel.app"
FRONT_TELEGRAM_AUTH_URL = "/auth/telegram/token"
