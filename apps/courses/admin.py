from django.contrib import admin
from .models import Category, Course, Module, Lesson, Review, UserLessonProgress

# Dùng StackedInline để hiện Bài học ngay trong trang sửa Module
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

# Dùng StackedInline để hiện Module ngay trong trang sửa Khóa học
class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'price', 'status', 'created_at']
    list_filter = ['status', 'category', 'level']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline] # Cho phép thêm Module ngay trong Course

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    inlines = [LessonInline] # Cho phép thêm Lesson ngay trong Module

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'lesson_type', 'is_preview', 'order']
    list_filter = ['module__course', 'lesson_type']
    search_fields = ['title']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']

@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'last_watched_position', 'updated_at']
    list_filter = ['is_completed', 'lesson__module__course']
    search_fields = ['user__username', 'lesson__title']
    readonly_fields = ['created_at', 'updated_at']
