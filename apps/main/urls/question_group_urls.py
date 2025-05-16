from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.views.language_view import LanguageViewSet
from apps.main.views.question_group_view import QuestionGroupViewSet


router = DefaultRouter()

router.register(r'', QuestionGroupViewSet, basename='question-group')


urlpatterns = [
    path('', include(router.urls)),

]
