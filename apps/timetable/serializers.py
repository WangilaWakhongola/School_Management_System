from rest_framework import serializers
from .models import TimeSlot, Timetable


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    time_slot_info = TimeSlotSerializer(source='time_slot', read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'

    def get_day_name(self, obj):
        return obj.get_day_of_week_display()

    def get_subject_name(self, obj):
        return obj.subject.name

    def get_teacher_name(self, obj):
        return obj.teacher.user.get_full_name()

    def get_class_name(self, obj):
        return str(obj.class_ref)
