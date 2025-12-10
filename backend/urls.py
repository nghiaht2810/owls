# backend/urls.py
# ... (giữ nguyên các import cũ)
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Courses (Core)
    path('api/', include('apps.courses.urls')),
    
    # API Auth (Mới thêm) -> Sẽ tạo ra các link: /api/auth/login/, /api/auth/register/
    path('api/auth/', include('apps.users.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)