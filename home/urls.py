
from django.contrib import admin
from django.urls import path
from home import settings
from django.conf.urls.static import static
from maydon.views import *
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("api.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
