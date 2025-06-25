from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot.utils.generate_auth_token import generate_token
from asgiref.sync import sync_to_async
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.conf import settings

from apps.bot.utils.translations import tr
from apps.main.models.languages import Language


async def start_keyboard(register: bool = False, lang="uz", telegram_id=None)  -> ReplyKeyboardMarkup:
    btn_text =  await tr( telegram_id=telegram_id, key="keyboard.register") if register else await  tr(telegram_id=telegram_id, key= "keyboard.login")
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn_text)]],
        resize_keyboard=True
    )


async def start_keyboard_register()  -> ReplyKeyboardMarkup:
    btn_text =  "📝 Register"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn_text)]],
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


async def generate_login_button(telegram_id):
    token = generate_token(telegram_id)

    # ✅ Frontend URL — real frontend adresingiz bo'lishi kerak
    login_url = f"{settings.FRONT_URL}{settings.FRONT_TELEGRAM_AUTH_URL}?token={token}"

    # ✅ Inline tugma
    text = await tr(telegram_id=telegram_id, key="keyboard.login_button")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=login_url)]
        ]
    )
    return keyboard



def phone_request_keyboard(button_text):
    keyboard = [
        [KeyboardButton(text=button_text, request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)




async def language_selection_keyboard():
    langs = await sync_to_async(list)(Language.objects.values("id", "name"))
    print()
    print("langs ", langs)
    print()
    keys = []
    for lang in langs:
        keys.append( InlineKeyboardButton(text=lang["name"], callback_data=f"lang_{lang['id']}"))

    return InlineKeyboardMarkup(inline_keyboard=[keys])
