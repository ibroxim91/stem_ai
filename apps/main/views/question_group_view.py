from rest_framework import viewsets
from apps.main.models import QuestionGroup
from apps.main.serializers import QuestionGroupSerializer
from apps.cauth.permissions import AdminPermission
from rest_framework.permissions import IsAuthenticated
from apps.main.models.question import Question
from apps.main.serializers.question_serializer import QuestionSerializer


class QuestionGroupViewSet(viewsets.ModelViewSet):
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerializer

  
    def get_permissions(self):
        # Faqat create, update, partial_update, destroy uchun AdminPermission kerak
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [AdminPermission]
        else:
            # list va retrieve uchun oddiy IsAuthenticated yetarli
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = self.get_object()
        questions = Question.objects.filter(group=obj)
        res = super().retrieve(request, *args, **kwargs)
        res.data['questions'] = QuestionSerializer(questions, many=True).data
        return res