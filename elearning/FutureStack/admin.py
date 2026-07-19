from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor_name', 'payable_amount', 'duration')
    search_fields = ('title', 'instructor_name')
    list_filter = ('category', 'level')
