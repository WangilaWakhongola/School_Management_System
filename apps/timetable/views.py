from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import TimeSlot, Timetable
from .serializers import TimeSlotSerializer, TimetableSerializer
from apps.accounts.permissions import IsAdmin, IsAdminOrTeacher


class TimeSlotListCreateView(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAdmin]


class TimetableListCreateView(generics.ListCreateAPIView):
    queryset = Timetable.objects.select_related('class_ref', 'subject', 'teacher__user', 'time_slot').all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_ref', 'teacher', 'day_of_week', 'academic_year', 'is_active']


class TimetableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdmin]
