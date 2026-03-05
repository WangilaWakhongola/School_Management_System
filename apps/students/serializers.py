from rest_framework import serializers
from .models import Student, Class
from apps.accounts.serializers import UserSerializer


class ClassSerializer(serializers.ModelSerializer):
    student_count = serializers.ReadOnlyField()
    class_teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = '__all__'

    def get_class_teacher_name(self, obj):
        if obj.class_teacher:
            return obj.class_teacher.get_full_name()
        return None


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_class_name = serializers.SerializerMethodField()
    age = serializers.ReadOnlyField()
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_current_class_name(self, obj):
        return str(obj.current_class) if obj.current_class else None

    def get_parent_name(self, obj):
        return obj.parent.get_full_name() if obj.parent else None


class StudentCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, default='School@123')

    class Meta:
        model = Student
        fields = ['email', 'first_name', 'last_name', 'password', 'admission_number',
                  'current_class', 'date_of_birth', 'gender', 'address',
                  'blood_group', 'emergency_contact', 'parent']

    def create(self, validated_data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_data = {
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
            'role': 'student',
        }
        user = User.objects.create_user(**user_data)
        return Student.objects.create(user=user, **validated_data)
