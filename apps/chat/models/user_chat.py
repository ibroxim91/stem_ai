from django.db import models
from apps.main.models.base import TimeStampedModel, UserStampedModel
from apps.main.models import ProjectCategory


class UserChat(TimeStampedModel, UserStampedModel):
    user = models.ForeignKey('cauth.User', on_delete=models.CASCADE, related_name="projects")
    project = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name="chats")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    message_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
