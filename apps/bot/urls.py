from django.urls import path
from apps.bot.views.webhook_view import TelegramWebhookAsyncView



urlpatterns = [
    path("webhook/", TelegramWebhookAsyncView.as_view()),
]
