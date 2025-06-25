from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from apps.bot.utils.check_user import check_user
from apps.bot.utils.validators import validate_age, validate_fullname,  validate_surname
from .keyboards import generate_login_button, get_language_keyboard, phone_request_keyboard, start_keyboard
from apps.cauth.models import User
from asgiref.sync import sync_to_async
from aiogram.filters.state import StateFilter
router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message): 
    user_id = message.from_user.id
    user_exists = await check_user(telegram_id=user_id)
    print("user exists:", user_exists, "\n")
    if not user_exists:
        text = "Assalomu alaykum!\nRo'yxatdan o'tish  uchun quyidagi  tugmani bosing"
        await message.answer(text, reply_markup=start_keyboard(register=True))
    else:    
        text = "Assalomu alaykum!\nTizimga kirish uchun quyidagi  tugmani bosing"
        await message.answer(text, reply_markup=start_keyboard())


# Routerni tashqi faylda ishlatish uchun eksport qilamiz
__all__ = ["router"]


class RegisterState(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    language = State()



@router.message(F.text == "📝 Ro'yxatdan o'tish")
async def register_start(message: Message, state: FSMContext):
    await message.answer("Iltimos, to'liq ismingizni kiriting:")
    await state.set_state(RegisterState.name)


@router.message(F.text ==  "✅Tizimga kirish")
async def register_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_exists = await check_user(telegram_id=user_id)
    if not user_exists:
        text = "Assalomu alaykum!\nRo'yxatdan o'tish  uchun quyidagi  tugmani bosing"
        await message.answer(text, reply_markup=start_keyboard(register=True))
    else:
        keyboard = generate_login_button(user_id)

        await message.answer(
            "✅  Kirish uchun tugmani bosing:",
            reply_markup=keyboard
        )    
       
   

@router.message(RegisterState.name)
async def register_fullname(message: Message, state: FSMContext):
    if not validate_fullname(message.text):
        await message.answer("❌ Ism kamida 3 ta belgidan iborat bo‘lishi kerak. Qayta urinib ko‘ring:")
        return
    await state.update_data(name=message.text.strip())
    await message.answer("Familyangizni kiriting:")
    await state.set_state(RegisterState.surname)

@router.message(RegisterState.surname)
async def register_fullname(message: Message, state: FSMContext):
    if not validate_surname(message.text):
        await message.answer("❌ Familyan kamida 5 ta belgidan iborat bo‘lishi kerak. Qayta urinib ko‘ring:")
        return
    await state.update_data(surname=message.text.strip())
    await message.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=phone_request_keyboard()
    )
    await state.set_state(RegisterState.phone)


@router.message(RegisterState.phone, F.contact)
async def handle_phone_contact(message: Message, state: FSMContext):
    contact = message.contact
    if not contact or not contact.phone_number:
        await message.answer("❌ Telefon raqamini olishda xatolik. Qayta urinib ko‘ring.")
        return
    await state.update_data(phone=contact.phone_number)
    region_keyboard = await get_language_keyboard()
    await message.answer("Tilni  tanlang:", reply_markup=region_keyboard)
    await state.set_state(RegisterState.language)

@router.callback_query(RegisterState.language)
async def register_region(callback: CallbackQuery, state: FSMContext):
    if not callback.data.startswith("language_"):
        await callback.answer("❌ Til tanlanmadi!", show_alert=True)
        return

    region_id = int(callback.data.split("_")[1])
    data = await state.get_data()
    data["region_id"] = region_id
    data["telegram_id"] = callback.from_user.id
    data["username"] = callback.from_user.username if callback.from_user.username else f"AAbb{callback.from_user.id}"
    user = User(
        first_name=data["name"],
        last_name=data["surname"],
        phone=data["phone"],
        age=data["age"],
        region_id=data["region_id"],
        telegram_id=data["telegram_id"],
        username=data["username"],
    )
    user.set_unusable_password()
    user = await sync_to_async(user.save)()
    # ✅ Token yaratish
    keyboard = generate_login_button(data["telegram_id"])

    await callback.message.edit_text(
        "✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!\n\n👇 Kirish uchun tugmani bosing:",
        reply_markup=keyboard
    )
    await state.clear()


@router.message(StateFilter(None))  # Faqat FSM holati yo‘q bo‘lsa ishlaydi
async def handle_free_text(message: Message, state: FSMContext):
    current_state = await state.get_state()
    text = "👇 Quyidagi tugmalardan birini tanlang"
    user_id = message.from_user.id
    user_exists = await check_user(telegram_id=user_id)
    if not user_exists:
        await message.answer(text, reply_markup=start_keyboard(register=True))
    else:
        await message.answer(text, reply_markup=start_keyboard())
