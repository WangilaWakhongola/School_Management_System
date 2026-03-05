from django.db import models
from apps.students.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()


class FeeStructure(models.Model):
    TUITION = 'tuition'
    TRANSPORT = 'transport'
    LIBRARY = 'library'
    SPORTS = 'sports'
    EXAM = 'exam'
    OTHER = 'other'

    FEE_TYPE_CHOICES = [
        (TUITION, 'Tuition Fee'),
        (TRANSPORT, 'Transport Fee'),
        (LIBRARY, 'Library Fee'),
        (SPORTS, 'Sports Fee'),
        (EXAM, 'Exam Fee'),
        (OTHER, 'Other'),
    ]

    TERM1 = 'term1'
    TERM2 = 'term2'
    TERM3 = 'term3'
    ANNUAL = 'annual'

    TERM_CHOICES = [
        (TERM1, 'Term 1'), (TERM2, 'Term 2'), (TERM3, 'Term 3'), (ANNUAL, 'Annual'),
    ]

    name = models.CharField(max_length=100)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    academic_year = models.CharField(max_length=20)
    grade_level = models.IntegerField(null=True, blank=True)
    due_date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'fee_structures'

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.term})"


class FeePayment(models.Model):
    PAID = 'paid'
    PENDING = 'pending'
    PARTIAL = 'partial'
    OVERDUE = 'overdue'

    STATUS_CHOICES = [
        (PAID, 'Paid'), (PENDING, 'Pending'),
        (PARTIAL, 'Partial'), (OVERDUE, 'Overdue'),
    ]

    CASH = 'cash'
    MPESA = 'mpesa'
    BANK = 'bank_transfer'
    CHEQUE = 'cheque'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Cash'), (MPESA, 'M-Pesa'),
        (BANK, 'Bank Transfer'), (CHEQUE, 'Cheque'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fee_payments'

    def __str__(self):
        return f"{self.student} - {self.fee_structure.name} - {self.amount_paid}"

    @property
    def balance(self):
        return self.fee_structure.amount - self.amount_paid
