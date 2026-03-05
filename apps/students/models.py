from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g. "Form 1", "Grade 5"
    grade_level = models.IntegerField()
    section = models.CharField(max_length=10, blank=True)  # e.g. "A", "B"
    academic_year = models.CharField(max_length=20)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'role': 'teacher'}, related_name='class_teacher')
    capacity = models.IntegerField(default=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'classes'
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        unique_together = ['name', 'section', 'academic_year']

    def __str__(self):
        return f"{self.name} {self.section} ({self.academic_year})"

    @property
    def student_count(self):
        return self.students.count()


class Student(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female'), (OTHER, 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile',
                                limit_choices_to={'role': 'student'})
    admission_number = models.CharField(max_length=20, unique=True)
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True,
                                      related_name='students')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    admission_date = models.DateField(auto_now_add=True)
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    # Parent/Guardian
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', limit_choices_to={'role': 'parent'})

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.admission_number} - {self.user.get_full_name()}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
