from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.views.question_view import (
    QuestionView, QuestionRetrieveUpdateDestroyView,
    QuestionOptionListCreateView, QuestionOptionRetrieveUpdateDestroyView
)

router = DefaultRouter()

router.register(r'', QuestionView, basename='question-group')


urlpatterns = [
    path('', include(router.urls)),

]
