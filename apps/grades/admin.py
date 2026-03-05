from django.contrib import admin
from .models import Exam, Grade


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'class_ref', 'subject', 'exam_date', 'total_marks']
    list_filter = ['exam_type', 'academic_year', 'class_ref']
    search_fields = ['name', 'subject__name']
    date_hierarchy = 'exam_date'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'grade', 'percentage', 'passed']
    list_filter = ['grade', 'exam__class_ref']
    search_fields = ['student__user__first_name', 'student__admission_number']
