from rest_framework import serializers
from .models import FeeStructure, FeePayment


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'


class FeePaymentSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    student_name = serializers.SerializerMethodField()
    fee_name = serializers.SerializerMethodField()

    class Meta:
        model = FeePayment
        fields = '__all__'
        read_only_fields = ['collected_by', 'payment_date']

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def get_fee_name(self, obj):
        return obj.fee_structure.name

    def create(self, validated_data):
        validated_data['collected_by'] = self.context['request'].user
        fee = validated_data['fee_structure']
        amount_paid = validated_data['amount_paid']
        if amount_paid >= fee.amount:
            validated_data['status'] = 'paid'
        elif amount_paid > 0:
            validated_data['status'] = 'partial'
        return super().create(validated_data)
