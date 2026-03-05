from django.db import models
from apps.students.models import Student, Class
from apps.teachers.models import Subject
from django.contrib.auth import get_user_model

User = get_user_model()


class Attendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    LATE = 'late'
    EXCUSED = 'excused'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
        (EXCUSED, 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRESENT)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  related_name='marked_attendance')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance'
        unique_together = ['student', 'date', 'subject']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class AttendanceSummary(models.Model):
    """Monthly summary for reporting."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    late_days = models.IntegerField(default=0)

    class Meta:
        db_table = 'attendance_summary'
        unique_together = ['student', 'month', 'year']

    @property
    def attendance_percentage(self):
        if self.total_days == 0:
            return 0
        return round((self.present_days / self.total_days) * 100, 2)
