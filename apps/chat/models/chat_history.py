from django.db import models
# from apps.chat.models.user_chat import UserChat
# from apps.main.models.base import TimeStampedModel, UserStampedModel
from apps.main.models.question import Question, QuestionOption
from apps.main.models.question_group import QuestionGroup


class UserOpenAIChatHistory(models.Model):
    chat = models.ForeignKey('chat.UserChat', on_delete=models.CASCADE, related_name="chats")
    model_name = models.CharField(max_length=50, default="gpt-4o")
    response_text = models.TextField()
    prompt_tokens = models.IntegerField()
    completion_tokens = models.IntegerField()
    total_tokens = models.IntegerField(blank=True, null=True)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6)
    prompt_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.chat.title} | {self.model_name} | {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class UserOpenAIChatHistoryQuestion( models.Model):
    chat_history = models.ForeignKey(UserOpenAIChatHistory, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_options = models.ManyToManyField(QuestionOption)
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, blank=True, null=True)
    boolean = models.BooleanField(null=True, blank=True)


