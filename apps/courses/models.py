from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# 1. Abstract Base Class: Giúp tái sử dụng fields created_at/updated_at
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# 2. Category: Phân loại khóa học (VD: Lập trình Web, Design, Marketing)
class Category(TimeStampedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon_url = models.URLField(blank=True, null=True) # Icon hiển thị menu

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

# 3. Course: Đối tượng chính
class Course(TimeStampedModel):
    # Các trạng thái của khóa học
    STATUS_CHOICES = (
        ('draft', 'Nháp'),
        ('published', 'Đang bán'),
        ('archived', 'Lưu trữ'),
    )
    
    LEVEL_CHOICES = (
        ('beginner', 'Cơ bản'),
        ('intermediate', 'Trung cấp'),
        ('advanced', 'Nâng cao'),
    )

    instructor = models.ForeignKey(User, related_name='courses_taught', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(help_text="Mô tả ngắn hiển thị ở card")
    about = models.TextField(help_text="Nội dung chi tiết (HTML/Markdown)")
    
    # Mở rộng tương lai: Lưu danh sách gạch đầu dòng dưới dạng JSON thay vì text
    # VD: ["Biết code React", "Hiểu về Hook", ...]
    what_will_learn = models.JSONField(default=list, blank=True) 
    requirements = models.JSONField(default=list, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Để hiện giảm giá
    
    thumbnail = models.ImageField(upload_to='courses/thumbnails/')
    trailer_url = models.URLField(blank=True, null=True) # Video giới thiệu
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    is_featured = models.BooleanField(default=False) # Khóa học nổi bật lên trang chủ

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# 4. Module: Chương học (Gom nhóm bài học)
class Module(TimeStampedModel):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0) # Sắp xếp thứ tự chương

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# 5. Lesson: Bài học (Core content)
class Lesson(TimeStampedModel):
    TYPE_CHOICES = (
        ('video', 'Video'),
        ('article', 'Bài viết'),
        ('quiz', 'Trắc nghiệm'), # Mở rộng tương lai
    )
    
    VIDEO_SOURCE_CHOICES = (
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('cloudflare', 'Cloudflare Stream'),
        ('upload', 'Self Hosted'),
    )

    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    
    lesson_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='video')
    
    # Nội dung bài học
    content = models.TextField(blank=True, help_text="Nội dung bài viết hoặc ghi chú video")
    
    # Cấu hình Video (Mở rộng để hỗ trợ nhiều nguồn)
    video_source = models.CharField(max_length=20, choices=VIDEO_SOURCE_CHOICES, default='youtube')
    video_url = models.CharField(max_length=500, blank=True, null=True) # ID video hoặc URL đầy đủ
    duration = models.DurationField(null=True, blank=True) # Thời lượng bài học (VD: 00:15:30)

    is_preview = models.BooleanField(default=False) # Cho phép xem thử không cần mua
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'slug'] # Slug chỉ cần duy nhất trong 1 module (hoặc course)

    def __str__(self):
        return self.title

# 6. UserProgress: Theo dõi tiến độ học tập (Gamification sau này)
class UserLessonProgress(TimeStampedModel):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_watched_position = models.PositiveIntegerField(default=0) # Lưu giây thứ mấy user đang xem dở

    class Meta:
        unique_together = ('user', 'lesson')

# 7. Review: Đánh giá khóa học
class Review(TimeStampedModel):
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    class Meta:
        unique_together = ('user', 'course') # Mỗi người chỉ review 1 lần/khóa