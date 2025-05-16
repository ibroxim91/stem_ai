from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.views.language_view import LanguageViewSet


router = DefaultRouter()

router.register(r'', LanguageViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
