from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.views.project_categories_view import ProjectCategoryDetailView
from apps.main.views.project_view import ProjectCategoryViewSet
from apps.main.views.project_questions_group import QuestionGroupsByCategoryView


router = DefaultRouter()


router.register(r'', ProjectCategoryViewSet, basename='project-category')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/question-groups/', QuestionGroupsByCategoryView.as_view() ,name="project-question-groups" )
]
