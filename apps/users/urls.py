# apps/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserProfileView

urlpatterns = [
    # Auth endpoints
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='auth_login'), # Trả về access & refresh token
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'), # Lấy access token mới
    
    # Profile endpoint
    path('me/', UserProfileView.as_view(), name='auth_profile'),
]