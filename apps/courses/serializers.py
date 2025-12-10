from rest_framework import serializers
from .models import Course, Module, Lesson, Category, Review, UserLessonProgress
from apps.enrollments.models import Enrollment

# --- 1. Hỗ trợ Serializers (Category, Review) ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'icon_url']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Chỉ lấy tên user
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

# --- 2. Lesson Serializer (Cấp nhỏ nhất) ---

class LessonSerializer(serializers.ModelSerializer):
    # SerializerMethodField giúp ta tùy biến logic hiển thị dữ liệu
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'slug', 'lesson_type', 
            'duration', 'is_preview', 'video_source', 
            'video_url', 'order', 'is_completed'
        ]

    def get_is_completed(self, obj):
        """
        Kiểm tra xem User đang login đã học xong bài này chưa.
        Lấy user từ context request.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Lưu ý: Cách query này đơn giản nhưng có thể gây chậm nếu danh sách quá dài (N+1 query).
            # Ở phần Views, chúng ta sẽ tối ưu bằng prefetch_related sau.
            return UserLessonProgress.objects.filter(user=request.user, lesson=obj, is_completed=True).exists()
        return False
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Mặc định: Không cho xem link video
        allow_access = False

        if instance.is_preview:
             allow_access = True
        elif request and request.user.is_authenticated:
            # Lấy User từ request
            user = request.user
            
            # Logic tối ưu: Kiểm tra xem user có enrollment cho Course chứa lesson này không
            # Lưu ý: instance.module.course truy cập ngược lên cha
            # Để tránh query DB liên tục, nên cache enrollment vào request nếu có thể (Advanced)
            # Nhưng ở mức MVP, query này chấp nhận được.
            if Enrollment.objects.filter(user=user, course=instance.module.course).exists():
                allow_access = True
            
            # Nếu user là admin/staff -> Cho xem luôn
            if user.is_staff:
                allow_access = True

        if not allow_access:
            data.pop('video_url', None)
            data.pop('video_source', None)
            
        return data

# --- 3. Module Serializer (Chứa Lesson) ---

class ModuleSerializer(serializers.ModelSerializer):
    # Lồng Lesson vào trong Module
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons']

# --- 4. Course Serializers (Root) ---

# Dùng cho trang chủ, trang danh sách (Load nhanh)
class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = serializers.ReadOnlyField(source='instructor.username')
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'price', 'old_price', 
            'thumbnail', 'level', 'category', 'instructor',
            'status', 'total_lessons'
        ]
    
    def get_total_lessons(self, obj):
        # Đếm tổng số bài học qua các module
        return Lesson.objects.filter(module__course=obj).count()

# Dùng cho trang chi tiết & trang học (Load đầy đủ)
class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = serializers.ReadOnlyField(source='instructor.username')
    modules = ModuleSerializer(many=True, read_only=True) # Nested quan trọng nhất
    reviews = ReviewSerializer(many=True, read_only=True)
    
    # JSONField không cần khai báo đặc biệt, DRF tự hiểu
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'about',
            'what_will_learn', 'requirements', # JSON fields
            'price', 'old_price', 'thumbnail', 'trailer_url',
            'level', 'updated_at', 'category', 'instructor',
            'modules', 'reviews'
        ]