from rest_framework import generics, permissions, viewsets
from apps.main.models import Question, QuestionOption
from apps.main.paginator import StandardResultsSetPagination
from  apps.main.serializers.question_serializer import QuestionSerializer, QuestionOptionSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


@extend_schema_view(
    list=extend_schema(
        request=QuestionSerializer,
        summary="Questionlar ro'yxati",
        description="Barcha mavjud Questionlarni paginatsiya bilan qaytaradi",    
    ),
    create=extend_schema(
        summary="Questionlar qo'shish (Admin)",
        description="Faqat adminlar yangi Questionlar qo'shishi mumkin"
    ),
    retrieve=extend_schema(
        summary="Questionni ko'rish",
        description="Question ID si orqali bitta Questionlarni ko'rish"
    ),
    update=extend_schema(
        summary="Questionni to'liq yangilash (Admin)",
        description="Faqat adminlar Question ma'lumotlarini to'liq yangilashi mumkin"
    ),
    partial_update=extend_schema(
        summary="Question qisman yangilash (Admin)",
        description="Faqat adminlar Question ma'lumotlarini qisman yangilashi mumkin"
    ),
    destroy=extend_schema(
        summary="Questionni o'chirish (Admin)",
        description="Faqat adminlar Questionlarni o'chirishi mumkin"
    ),
) 
class QuestionView(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Question.objects.all().prefetch_related('translations', 'options__translations')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
  
  

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
