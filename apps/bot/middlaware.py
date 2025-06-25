# your_project/middleware/disable_silk_for_webhook.py
from django.utils.deprecation import MiddlewareMixin

class DisableSilkForTelegramWebhookMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/api/v1/bot/webhook/"):
            request._dont_profile = True
