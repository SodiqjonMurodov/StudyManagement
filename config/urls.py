from config import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('management.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
