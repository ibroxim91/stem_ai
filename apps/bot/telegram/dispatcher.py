from aiogram import Dispatcher
from apps.bot.telegram.handlers import router as main_router

dp: Dispatcher  = None  # Optional global

async def setup_dispatcher() -> Dispatcher:
    global dp
    if dp is None:
        dp = Dispatcher()
        dp.include_router(main_router)
    return dp


def setup_dispatcher_sync() -> Dispatcher:
    global dp
    if dp is None:
        dp = Dispatcher()
        dp.include_router(main_router)
    return dp
