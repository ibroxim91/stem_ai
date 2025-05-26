from django.contrib import admin
from apps.chat.models.chat_history import UserOpenAIChatHistory
from apps.chat.models.user_chat import UserChat

admin.site.register(UserChat)
admin.site.register(UserOpenAIChatHistory)
# Register your models here.
