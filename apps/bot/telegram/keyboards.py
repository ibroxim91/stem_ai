from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot.utils.generate_auth_token import generate_token
from asgiref.sync import sync_to_async
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings

from apps.main.models.languages import Language


def start_keyboard(register: bool = False) -> ReplyKeyboardMarkup:

    keyboard=[]
    register_btn = [KeyboardButton(text="📝 Ro'yxatdan o'tish")]
    login_btn = [KeyboardButton(text="✅Tizimga kirish")]
    if register:
        keyboard.append(register_btn)
    else:
        keyboard.append(login_btn)    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )





async def get_language_keyboard():
    regions = await sync_to_async(list)(Language.objects.values("id", "name"))
    builder = InlineKeyboardBuilder()

    if not regions:
        builder.add(
            InlineKeyboardButton(text="❌ Tillar yuklanmadi", callback_data="region_error")
        )
    else:
        for region in regions:
            builder.add(
                InlineKeyboardButton(text=region["name"], callback_data=f"language_{region['id']}")
            )

    builder.adjust(2)  # 2 ta tugma bir qatorga
    return builder.as_markup()


def generate_login_button(telegram_id):
    token = generate_token(telegram_id)

    # ✅ Frontend URL — real frontend adresingiz bo'lishi kerak
    login_url = f"{settings.FRONT_URL}{settings.FRONT_TELEGRAM_AUTH_URL}?token={token}"

    # ✅ Inline tugma
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔓 Kirish", url=login_url)]
        ]
    )
    return keyboard



def phone_request_keyboard():
    keyboard = [
        [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
