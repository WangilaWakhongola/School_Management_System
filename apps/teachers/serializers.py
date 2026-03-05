from rest_framework import serializers
from .models import Teacher, Subject
from apps.accounts.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Subject.objects.all(), write_only=True, source='subjects', required=False
    )

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, default='Teacher@123')
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Subject.objects.all(), write_only=True, source='subjects', required=False
    )

    class Meta:
        model = Teacher
        fields = ['email', 'first_name', 'last_name', 'password', 'employee_id',
                  'qualification', 'specialization', 'joining_date', 'salary', 'subject_ids']

    def create(self, validated_data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        subjects = validated_data.pop('subjects', [])
        user_data = {
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
            'role': 'teacher',
        }
        user = User.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.subjects.set(subjects)
        return teacher
