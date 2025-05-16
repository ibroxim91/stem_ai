from drf_spectacular.settings import spectacular_settings
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)



class CustomSpectacularAPIView(SpectacularAPIView):
    def get(self, request, *args, **kwargs):
        spectacular_settings.TITLE = "Stem AI api V1"
        spectacular_settings.VERSION = "1.0"
        return super().get(request, *args, **kwargs)





