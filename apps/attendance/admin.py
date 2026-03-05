from django.contrib import admin
from .models import Attendance, AttendanceSummary


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_ref', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date', 'class_ref']
    search_fields = ['student__user__first_name', 'student__admission_number']
    date_hierarchy = 'date'


@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ['student', 'month', 'year', 'total_days', 'present_days', 'attendance_percentage']
