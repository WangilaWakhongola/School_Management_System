from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Attendance, AttendanceSummary
from .serializers import AttendanceSerializer, BulkAttendanceSerializer, AttendanceSummarySerializer
from apps.accounts.permissions import IsAdminOrTeacher
from apps.students.models import Student, Class
from apps.teachers.models import Subject


class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.select_related('student__user', 'class_ref', 'subject', 'marked_by').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'class_ref', 'date', 'status', 'subject']
    ordering = ['-date']


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacher]


class BulkAttendanceView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def post(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        class_ref = Class.objects.get(id=data['class_ref'])
        subject = Subject.objects.get(id=data['subject']) if data.get('subject') else None
        created, updated = 0, 0

        for record in data['records']:
            student = Student.objects.get(id=record['student_id'])
            obj, is_created = Attendance.objects.update_or_create(
                student=student, date=data['date'], subject=subject,
                defaults={
                    'class_ref': class_ref,
                    'status': record.get('status', 'present'),
                    'remarks': record.get('remarks', ''),
                    'marked_by': request.user,
                }
            )
            if is_created:
                created += 1
            else:
                updated += 1

        return Response({
            'message': f'Attendance recorded. Created: {created}, Updated: {updated}'
        }, status=status.HTTP_200_OK)


class AttendanceSummaryView(generics.ListAPIView):
    queryset = AttendanceSummary.objects.select_related('student__user', 'class_ref').all()
    serializer_class = AttendanceSummarySerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'class_ref', 'month', 'year']


class StudentAttendanceView(APIView):
    def get(self, request, student_id):
        attendance = Attendance.objects.filter(student_id=student_id).order_by('-date')
        total = attendance.count()
        present = attendance.filter(status='present').count()
        percentage = round((present / total) * 100, 2) if total > 0 else 0

        serializer = AttendanceSerializer(attendance[:30], many=True)
        return Response({
            'total_days': total,
            'present_days': present,
            'attendance_percentage': percentage,
            'recent_records': serializer.data,
        })
