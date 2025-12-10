from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Module, UserLessonProgress
from apps.enrollments.models import Enrollment
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet xử lý hiển thị khóa học.
    - ReadOnlyModelViewSet: Mặc định chỉ cung cấp API đọc (GET).
    - Để tạo/sửa/xóa khóa học, ta sẽ dùng Django Admin cho an toàn.
    """
    lookup_field = 'slug' # URL sẽ là /api/courses/hoc-python/ thay vì ID
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Tối ưu hóa Query (Chống N+1 Query):
        Sử dụng prefetch_related để lấy luôn dữ liệu Module và Lesson trong 1 lần gọi DB.
        """
        queryset = Course.objects.select_related('category', 'instructor') \
                                 .prefetch_related('modules__lessons')

        # Nếu là Admin (Superuser) -> Thấy hết (kể cả bản nháp)
        if self.request.user.is_staff:
            return queryset
        
        # Nếu là User thường -> Chỉ thấy khóa học đã Public
        return queryset.filter(status='published')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    def get_serializer_context(self):
        """
        Truyền thêm thông tin vào Serializer để xử lý logic ẩn/hiện video URL.
        """
        context = super().get_serializer_context()
        # Logic check xem user đã mua khóa học này chưa được đặt trong Serializer
        # nhưng chúng ta cần đảm bảo request user được truyền vào.
        return context

    # --- ACTION 1: Đăng ký khóa học (Mua) ---
    # URL: POST /api/courses/{slug}/enroll/
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, slug=None):
        course = self.get_object()
        user = request.user

        # 1. Kiểm tra đã mua chưa
        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response(
                {"message": "Bạn đã đăng ký khóa học này rồi!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Xử lý thanh toán (Giả lập cho MVP)
        # Trong thực tế: Bạn sẽ check Webhook từ Stripe/Momo ở đây. 
        # Nếu khóa học FREE -> Cho qua luôn.
        if course.price > 0:
            # TODO: Integrate Payment Gateway logic here
            # return Response({"message": "Vui lòng thanh toán..."}, status=PAYMENT_REQUIRED)
            pass

        # 3. Tạo Enrollment
        Enrollment.objects.create(user=user, course=course)
        
        return Response(
            {"message": "Đăng ký thành công! Chúc bạn học tốt."}, 
            status=status.HTTP_201_CREATED
        )


class LessonViewSet(viewsets.GenericViewSet):
    """
    ViewSet xử lý riêng cho Bài học (VD: Đánh dấu hoàn thành).
    Chúng ta không cần list/retrieve ở đây vì đã gộp vào CourseDetail rồi.
    """
    queryset = Lesson.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    # --- ACTION 2: Đánh dấu hoàn thành bài học ---
    # URL: POST /api/lessons/{id}/complete/
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        
        # Cập nhật hoặc tạo mới tiến độ
        progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        
        if not progress.is_completed:
            progress.is_completed = True
            progress.save()
            return Response({"status": "Marked as completed"}, status=status.HTTP_200_OK)
        
        return Response({"status": "Already completed"}, status=status.HTTP_200_OK)

    # --- ACTION 3: Cập nhật thời gian xem (Resume) ---
    # URL: POST /api/lessons/{id}/update-progress/
    # Body: { "seconds": 120 }
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        lesson = get_object_or_404(Lesson, pk=pk)
        seconds = request.data.get('seconds', 0)
        
        progress, created = UserLessonProgress.objects.get_or_create(
            user=request.user, 
            lesson=lesson
        )
        
        progress.last_watched_position = int(seconds)
        progress.save()
        
        return Response({"status": "Progress updated"}, status=status.HTTP_200_OK)