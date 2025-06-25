from apps.cauth.models import User
from asgiref.sync import sync_to_async


async def check_user(telegram_id):
    user_exists = await sync_to_async(User.objects.filter(telegram_id=telegram_id).exists)()
    return user_exists

@sync_to_async
def check_user_phone(telegram_id):
    user_exists = User.objects.filter(telegram_id=telegram_id).first()
    if user_exists:
        return  True if user_exists.phone else False
    return None