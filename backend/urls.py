from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/', include('apps.courses.urls')),
    path('api/auth/', include('apps.users.urls')),
]

# Serve media files locally in development (if not using Cloudinary)
if settings.DEBUG and not settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)