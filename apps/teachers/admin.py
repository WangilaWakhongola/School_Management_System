from django.contrib import admin
from .models import Teacher, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['name', 'code']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_name', 'specialization', 'joining_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name']
    filter_horizontal = ['subjects']

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Full Name'
