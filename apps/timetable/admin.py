from django.contrib import admin
from .models import TimeSlot, Timetable


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['slot_number', 'start_time', 'end_time']


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['class_ref', 'subject', 'teacher', 'day_of_week', 'time_slot', 'room', 'is_active']
    list_filter = ['day_of_week', 'class_ref', 'is_active', 'academic_year']
