from django.contrib import admin
from .models import FeeStructure, FeePayment


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'fee_type', 'amount', 'term', 'academic_year', 'due_date']
    list_filter = ['fee_type', 'term', 'academic_year']
    search_fields = ['name']


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'amount_paid', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_method']
    search_fields = ['student__user__first_name', 'transaction_id']
    date_hierarchy = 'payment_date'
