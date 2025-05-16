from django.urls import path
from apps.main.views.question_view import (
    QuestionListCreateView, QuestionRetrieveUpdateDestroyView,
    QuestionOptionListCreateView, QuestionOptionRetrieveUpdateDestroyView
)


urlpatterns = [
    path('', QuestionListCreateView.as_view(), name='question-list-create'),
    path('<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-detail'),
    
    path('options/', QuestionOptionListCreateView.as_view(), name='question-option-list-create'),
    path('question-options/<int:pk>/', QuestionOptionRetrieveUpdateDestroyView.as_view(), name='question-option-detail'),
]
