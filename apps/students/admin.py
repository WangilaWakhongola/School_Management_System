from django.contrib import admin
from .models import Student, Class


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'grade_level', 'academic_year', 'class_teacher', 'student_count']
    list_filter = ['academic_year', 'grade_level']
    search_fields = ['name', 'section']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'get_name', 'current_class', 'gender', 'is_active']
    list_filter = ['current_class', 'gender', 'is_active']
    search_fields = ['admission_number', 'user__first_name', 'user__last_name']

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Full Name'
