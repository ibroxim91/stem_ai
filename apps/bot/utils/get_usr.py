from asgiref.sync import sync_to_async
from apps.cauth.models import User

@sync_to_async
def get_user_object(telegram_id):
    return User.objects.get(telegram_id=telegram_id)
