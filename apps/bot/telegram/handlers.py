from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from apps.bot.utils.create_user import create_user_object
from apps.bot.utils.check_user import check_user, check_user_phone
from apps.bot.utils.get_usr import get_user_object
from apps.bot.utils.translations import get_translated_buttons, get_user_language, tr
from apps.bot.utils.validators import validate_age, validate_fullname,  validate_surname
from .keyboards import generate_login_button, get_language_keyboard, language_selection_keyboard, phone_request_keyboard, start_keyboard, start_keyboard_register
from apps.cauth.models import User
from asgiref.sync import sync_to_async
from aiogram.filters.state import StateFilter
router = Router()

__all__ = ["router"]

@router.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_exists = await check_user(telegram_id=user_id)

    if not user_exists:
        await create_user_object(user_id)
        text = "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please select your language"
        await message.answer(text, reply_markup=await language_selection_keyboard())
    else:
        phone_check = await check_user_phone(user_id)
        print()
        print("31 phone_check ", phone_check)
        print()
        if not phone_check:
            register_text = await tr(telegram_id=message.from_user.id, key="start.register_text")
            await message.answer(register_text, reply_markup=await start_keyboard(register=True, telegram_id=user_id))
        else:
            lang = await get_user_language(user_id)
            text = await tr(telegram_id=user_id, key="start.login_text")
            await message.answer(text, reply_markup=await start_keyboard(lang=lang, telegram_id=user_id))


# Routerni tashqi faylda ishlatish uchun eksport qilamiz


class RegisterState(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    language = State()


register_texts =  get_translated_buttons("keyboard.register")
login_texts =  get_translated_buttons("keyboard.login")

register_texts.append("📝 Register")

print()
print("register_texts ", register_texts)
print("login_texts ", login_texts)
print()

# REGISTER
@router.message(F.text.in_(register_texts))
async def register_start(message: Message, state: FSMContext):
    print()
    print("message.text Register", message.text)
    print()
    text = await tr(telegram_id=message.from_user.id, key="register.request_name")
    await message.answer(text)
    await state.set_state(RegisterState.name)


# LOgin
@router.message(F.text.in_(login_texts))
async def register_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_exists = await check_user(telegram_id=user_id)
    register_text = await tr(telegram_id=message.from_user.id, key="start.register_text")
    if not user_exists:
        await message.answer(register_text, reply_markup=start_keyboard(register=True, telegram_id=user_id))
    else:
        phone_check = await check_user_phone(user_id)
        if not phone_check:
            await message.answer(register_text, reply_markup=start_keyboard(register=True, telegram_id=user_id))
        keyboard = await generate_login_button(user_id)
        text = await tr(telegram_id=user_id, key="auth.login_text")
        await message.answer(
           text,
            reply_markup=keyboard
        )    
       
   

@router.message(RegisterState.name)
async def register_fullname(message: Message, state: FSMContext):
    if not validate_fullname(message.text):
        text = await tr(telegram_id=message.from_user.id, key="register.invalid_name")
        await message.answer(text)
        return
    await state.update_data(name=message.text.strip())
    text = await tr(telegram_id=message.from_user.id, key="register.request_surname")
    await message.answer(text)
    await state.set_state(RegisterState.surname)

@router.message(RegisterState.surname)
async def register_fullname(message: Message, state: FSMContext):
    if not validate_surname(message.text):
        text = await tr(telegram_id=message.from_user.id, key="register.invalid_surname")
        await message.answer(text)
        return
    await state.update_data(surname=message.text.strip())
    text = await tr(telegram_id=message.from_user.id, key="register.request_phone")
    button_text = await tr(telegram_id=message.from_user.id, key="keyboard.send_phone")
    await message.answer(
       text,
        reply_markup=phone_request_keyboard(button_text)
    )
    await state.set_state(RegisterState.phone)


@router.message(RegisterState.phone, F.contact)
async def handle_phone_contact(message: Message, state: FSMContext):
    contact = message.contact
    if not contact or not contact.phone_number:
        text = await tr(telegram_id=message.from_user.id, key="register.phone_error")
        await message.answer(text)
        return
    await state.update_data(phone=contact.phone_number)
    data = await state.get_data()
    data["telegram_id"] = message.from_user.id
    data["username"] = message.from_user.username if message.from_user.username else f"AAbb{message.from_user.id}"
    user = await get_user_object(data["telegram_id"]) 
    user.first_name = data["name"]
    user.last_name = data["surname"]
    user.phone = data["phone"]
    user.username = data["username"]
    user.set_unusable_password()
    user = await sync_to_async(user.save)()
    # ✅ Token yaratish
    keyboard = await generate_login_button(data["telegram_id"])

    text = await tr(telegram_id=message.from_user.id, key="register.success")
    await message.answer(
       text,
        reply_markup=keyboard
    )
    await state.clear()


from aiogram import types, F

@router.callback_query(F.data.startswith("lang_"))
async def language_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    selected_lang = callback.data.split("_")[1]  # uz, ru, en

    # Update user's language
    await sync_to_async(User.objects.filter(telegram_id=user_id).update)(language=selected_lang)

    # Javob qaytarish
    lang_selected_text = await tr(telegram_id=user_id, key="language.selected")
    await callback.message.edit_text(lang_selected_text)

    # Keyingi bosqich (masalan: menu ko'rsatish)
    text = await tr(telegram_id=user_id, key="start.register_text")
    await callback.message.answer(text, reply_markup=await start_keyboard(register=True, lang=selected_lang, telegram_id=user_id))


@router.message(StateFilter(None))  # Faqat FSM holati yo‘q bo‘lsa ishlaydi
async def handle_free_text(message: Message, state: FSMContext):
    current_state = await state.get_state()
    user_id = message.from_user.id
    user_exists = await check_user(telegram_id=user_id)
    print()
    print()
    print("message text ", message.text)
    print("user_exists ", user_exists)
    print()
    print()
    if  user_exists == False:
        await message.answer("Please register now!", reply_markup=await start_keyboard_register())
    else:
        text = await tr(telegram_id=message.from_user.id, key="fallback.text")
        lang = await get_user_language(telegram_id=user_id)
        print()
        print()
        print("user ", lang)
        print()
        print()
        if not lang:
            text = "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please select your language"
            await message.answer(text, reply_markup = await language_selection_keyboard())
        else:
            await message.answer(text, reply_markup = await start_keyboard(telegram_id=user_id))
