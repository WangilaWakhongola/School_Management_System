from django.db import models
from apps.students.models import Student, Class
from apps.teachers.models import Subject
from django.contrib.auth import get_user_model

User = get_user_model()


class Exam(models.Model):
    MIDTERM = 'midterm'
    FINAL = 'final'
    CAT = 'cat'
    ASSIGNMENT = 'assignment'

    EXAM_TYPE_CHOICES = [
        (MIDTERM, 'Midterm'),
        (FINAL, 'Final'),
        (CAT, 'Continuous Assessment Test'),
        (ASSIGNMENT, 'Assignment'),
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    passing_marks = models.DecimalField(max_digits=5, decimal_places=2)
    exam_date = models.DateField()
    academic_year = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exams'

    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.class_ref})"


class Grade(models.Model):
    A_PLUS = 'A+'
    A = 'A'
    B_PLUS = 'B+'
    B = 'B'
    C_PLUS = 'C+'
    C = 'C'
    D = 'D'
    F = 'F'

    GRADE_CHOICES = [
        (A_PLUS, 'A+'), (A, 'A'), (B_PLUS, 'B+'), (B, 'B'),
        (C_PLUS, 'C+'), (C, 'C'), (D, 'D'), (F, 'F'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    remarks = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grades'
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.marks_obtained}"

    def save(self, *args, **kwargs):
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
        if percentage >= 90:
            self.grade = 'A+'
        elif percentage >= 80:
            self.grade = 'A'
        elif percentage >= 75:
            self.grade = 'B+'
        elif percentage >= 70:
            self.grade = 'B'
        elif percentage >= 65:
            self.grade = 'C+'
        elif percentage >= 60:
            self.grade = 'C'
        elif percentage >= 50:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)

    @property
    def percentage(self):
        return round((self.marks_obtained / self.exam.total_marks) * 100, 2)

    @property
    def passed(self):
        return self.marks_obtained >= self.exam.passing_marks
