from django.contrib import admin
from django.urls import path, include  # Import include to include app URLs
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pathoapp.urls')),  # Include the URLs from pathoapp
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
