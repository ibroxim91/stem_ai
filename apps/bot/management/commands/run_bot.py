import asyncio
import logging

from django.core.management.base import BaseCommand
from aiogram import Bot
from apps.bot.telegram.dispatcher import setup_dispatcher
from apps.bot.telegram.handlers import router as main_router
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
TOKEN = os.getenv("BOT_TOKEN") 

# class Command(BaseCommand):
#     help = "Telegram botni ishga tushiradi"

#     def handle(self, *args, **options):
#         asyncio.run(self.run_bot())

#     async def run_bot(self):
#         logging.basicConfig(level=logging.INFO)
#         bot = Bot(token=TOKEN)
#         dp = await setup_dispatcher()
#         # dp.include_router(main_router)
#         await dp.start_polling(bot)
