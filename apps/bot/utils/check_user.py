from apps.cauth.models import User
from asgiref.sync import sync_to_async


async def check_user(telegram_id):
    user_exists = await sync_to_async(User.objects.filter(telegram_id=telegram_id).exists)()
    return user_exists