from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Enrollment(models.Model):
	"""Simple Enrollment model linking a user to a course.

	Uses a string reference to the Course model to avoid circular imports.
	"""
	user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
	course = models.ForeignKey('courses.Course', related_name='enrollments', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'course')

	def __str__(self):
		return f"{self.user} -> {self.course}"
