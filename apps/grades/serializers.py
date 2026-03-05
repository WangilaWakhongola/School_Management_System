from rest_framework import serializers
from .models import Exam, Grade


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class GradeSerializer(serializers.ModelSerializer):
    percentage = serializers.ReadOnlyField()
    passed = serializers.ReadOnlyField()
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['grade', 'graded_by']

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def create(self, validated_data):
        validated_data['graded_by'] = self.context['request'].user
        return super().create(validated_data)


class BulkGradeSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    grades = serializers.ListField(child=serializers.DictField())
