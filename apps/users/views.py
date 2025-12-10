# apps/users/views.py
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer

# 1. API Đăng ký
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # Ai cũng có thể đăng ký
    serializer_class = RegisterSerializer

# 2. API Lấy thông tin bản thân (Me)
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,) # Phải đăng nhập mới xem được
    serializer_class = UserSerializer

    def get_object(self):
        # Trả về user đang thực hiện request
        return self.request.user