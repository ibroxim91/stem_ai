# bot/webhook.py
import os
from aiogram import types
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from aiogram import Bot
from apps.bot.telegram.dispatcher import setup_dispatcher
from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from aiogram import types

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") 
bot = Bot(token=TOKEN)


# @extend_schema( tags=["Bot Webhook"])
# @extend_schema_view(
#     post=extend_schema(
#         summary="Telegram bot webhook",
#         description="Botni webhook qilib ishga tushirish uchun endpoint",    
#     )
# )
@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookAsyncView(View):
    async def post(self, request, *args, **kwargs):
        # try:
        dp = await setup_dispatcher()
        body_unicode = request.body.decode('utf-8')
        import json
        data = json.loads(body_unicode)
        telegram_update = types.Update(**data)
        await dp.feed_update(bot=bot, update=telegram_update)
        # except Exception as e:
        #     return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"status": "ok"})
