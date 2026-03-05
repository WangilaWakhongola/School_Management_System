from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .models import Exam, Grade
from .serializers import ExamSerializer, GradeSerializer, BulkGradeSerializer
from apps.accounts.permissions import IsAdminOrTeacher
from apps.students.models import Student


class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.select_related('class_ref', 'subject', 'created_by').all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_ref', 'subject', 'exam_type', 'academic_year']


class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrTeacher]


class GradeListCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.select_related('student__user', 'exam').all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'exam', 'grade']


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrTeacher]


class BulkGradeView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def post(self, request):
        serializer = BulkGradeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        created, updated = 0, 0

        for record in data['grades']:
            student = Student.objects.get(id=record['student_id'])
            obj, is_created = Grade.objects.update_or_create(
                student=student, exam_id=data['exam_id'],
                defaults={
                    'marks_obtained': record['marks_obtained'],
                    'remarks': record.get('remarks', ''),
                    'graded_by': request.user,
                }
            )
            if is_created:
                created += 1
            else:
                updated += 1

        return Response({'message': f'Grades saved. Created: {created}, Updated: {updated}'})


class StudentReportView(APIView):
    def get(self, request, student_id):
        grades = Grade.objects.filter(student_id=student_id).select_related('exam__subject')
        avg = grades.aggregate(avg=Avg('marks_obtained'))['avg']
        serializer = GradeSerializer(grades, many=True)
        return Response({
            'grades': serializer.data,
            'average_marks': round(avg, 2) if avg else 0,
            'total_exams': grades.count(),
        })
