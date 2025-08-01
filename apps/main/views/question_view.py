from rest_framework import generics, permissions
from apps.main.models import Question, QuestionOption
from  apps.main.serializers.question_serializer import QuestionSerializer, QuestionOptionSerializer

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all().prefetch_related('translations', 'options__translations')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all().prefetch_related('translations', 'options__translations')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionOptionListCreateView(generics.ListCreateAPIView):
    queryset = QuestionOption.objects.all().prefetch_related('translations')
    serializer_class = QuestionOptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionOptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionOption.objects.all().prefetch_related('translations')
    serializer_class = QuestionOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
