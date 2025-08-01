"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import  SpectacularRedocView, SpectacularSwaggerView
from .swagger_settings import CustomSpectacularAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('config.urls')),
    
]


urlpatterns += [
    path("schema/", CustomSpectacularAPIView.as_view(urlconf=urlpatterns),name="schema",),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"),name="swagger",),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)