from django.urls import path, include


urlpatterns = [
   
    path('auth/', include('apps.cauth.urls')),
    path('languages/', include('apps.main.urls.language_urls')),
    path('projects/', include('apps.main.urls.project_urls')),
    path('question-group/', include('apps.main.urls.question_group_urls')),
    path('question/', include('apps.main.urls.question_urls')),
    path('chat/', include('apps.chat.urls')),
    path('order/', include('apps.order.urls')),
    path('click/', include('apps.clickuz.urls')),
      path('bot/', include('apps.bot.urls')),
    # path('main/', include('apps.main.urls')),
    
]
