# utils/translations.py
from apps.bot.models.bot_translation_model import BotTranslation
from asgiref.sync import sync_to_async

from apps.cauth.models.user import User
from apps.main.models.languages import Language


async def tr(telegram_id: int, key: str) -> str:
    lang =  await get_user_language(telegram_id)
    try:
        t = await sync_to_async(BotTranslation.objects.get)(language=lang)  
        return t.translations.get(key )
    except BotTranslation.DoesNotExist:
        return key


# @sync_to_async
def get_button_names(lang: Language, key: str) -> str:
    try:
        t = BotTranslation.objects.get(language=lang)
        return t.translations.get(key )
    except BotTranslation.DoesNotExist:
        return ""


# async def get_user_language(telegram_id: int) -> str:
#     print()
#     print("telegram_id ", telegram_id)
#     print()
#     # try:
#     user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
#     print()
#     print("user ", user)
#     print("user.language ", user.language)
#     print()
#     return user.language 
# # except:
#     #     raise Exception("User does not exist")

from asgiref.sync import sync_to_async

@sync_to_async
def get_user_language(telegram_id: int) -> str:
    print()
    print("telegram_id ", telegram_id)
    print(User.objects.filter(telegram_id=telegram_id))
    print()
    user = User.objects.get(telegram_id=telegram_id)
    return user.language


def get_translated_buttons(key: str) -> list[str]:
    langs = Language.objects.all()
    return [ get_button_names(lang, key) for lang in langs]
