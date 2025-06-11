from rest_framework import viewsets
from apps.main.models import QuestionGroup
from apps.main.paginator import StandardResultsSetPagination
from apps.main.serializers import QuestionGroupSerializer
from apps.cauth.permissions import AdminPermission
from rest_framework.permissions import IsAuthenticated
from apps.main.models.question import Question
from apps.main.serializers.question_serializer import QuestionSerializer
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class QuestionPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'question_page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return {
            'questions': data,
            'pagination': {
                'total': self.page.paginator.count,
                'per_page': self.page.paginator.per_page,
                'current_page': self.page.number,
                'last_page': self.page.paginator.num_pages,
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link(),
            }
        }
    

@extend_schema(
    summary="Questions",
    description="Kategoriyalar ro'yxati",
   
)
@extend_schema_view(
    list=extend_schema(
        summary="Kategoriyalar ro'yxati",
        description="Barcha mavjud Kategoriyalarni paginatsiya bilan qaytaradi",    
    ),
    create=extend_schema(
        summary="Kategoriya qo'shish (Admin)",
        description="Faqat adminlar yangi Kategoriya qo'shishi mumkin"
    ),
    retrieve=extend_schema(
        summary="Kategoriyani ko'rish",
        description="Kategoriya ID si orqali bitta Kategoriyani ko'rish"
    ),
    update=extend_schema(
        summary="Kategoriyani to'liq yangilash (Admin)",
        description="Faqat adminlar Kategoriya ma'lumotlarini to'liq yangilashi mumkin"
    ),
    partial_update=extend_schema(
        summary="Kategoriyani qisman yangilash (Admin)",
        description="Faqat adminlar Kategoriya ma'lumotlarini qisman yangilashi mumkin"
    ),
    destroy=extend_schema(
        summary="Kategoriyani o'chirish (Admin)",
        description="Faqat adminlar Kategoriyani o'chirishi mumkin"
    ),
)    
class QuestionGroupViewSet(viewsets.ModelViewSet):
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerializer
    pagination_class = StandardResultsSetPagination

  
    def get_permissions(self):
        # Faqat create, update, partial_update, destroy uchun AdminPermission kerak
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [AdminPermission]
        else:
            # list va retrieve uchun oddiy IsAuthenticated yetarli
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        questions = Question.objects.filter(group=obj)
        
        # Paginator yaratish
        paginator = QuestionPagination()
        page = paginator.paginate_queryset(questions, request)
        
        # Asosiy javob
        res = super().retrieve(request, *args, **kwargs)
        
        if page is not None:
            # Agar pagination qo'llanilsa
            serializer = QuestionSerializer(page, many=True)
            paginated_data = paginator.get_paginated_response(serializer.data)
            res.data.update(paginated_data)
        else:
            # Pagination qo'llanilmasa
            res.data['questions'] = QuestionSerializer(questions, many=True).data
            
        return res