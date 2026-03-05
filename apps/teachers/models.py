from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile',
                                limit_choices_to={'role': 'teacher'})
    employee_id = models.CharField(max_length=20, unique=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
