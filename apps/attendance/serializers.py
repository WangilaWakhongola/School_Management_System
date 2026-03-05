from rest_framework import serializers
from .models import Attendance, AttendanceSummary


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    marked_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['marked_by']

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def get_marked_by_name(self, obj):
        return obj.marked_by.get_full_name() if obj.marked_by else None

    def create(self, validated_data):
        validated_data['marked_by'] = self.context['request'].user
        return super().create(validated_data)


class BulkAttendanceSerializer(serializers.Serializer):
    class_ref = serializers.IntegerField()
    date = serializers.DateField()
    subject = serializers.IntegerField(required=False)
    records = serializers.ListField(child=serializers.DictField())


class AttendanceSummarySerializer(serializers.ModelSerializer):
    attendance_percentage = serializers.ReadOnlyField()
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSummary
        fields = '__all__'

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
