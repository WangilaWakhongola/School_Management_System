from django.db import models
from apps.students.models import Class
from apps.teachers.models import Teacher, Subject


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_number = models.IntegerField()

    class Meta:
        db_table = 'time_slots'
        ordering = ['slot_number']

    def __str__(self):
        return f"Slot {self.slot_number}: {self.start_time} - {self.end_time}"


class Timetable(models.Model):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    DAY_CHOICES = [
        (MONDAY, 'Monday'), (TUESDAY, 'Tuesday'), (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'), (FRIDAY, 'Friday'), (SATURDAY, 'Saturday'),
    ]

    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetable_entries')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    room = models.CharField(max_length=50, blank=True)
    academic_year = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'timetable'
        unique_together = ['class_ref', 'time_slot', 'day_of_week', 'academic_year']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.time_slot} - {self.subject.name}"
