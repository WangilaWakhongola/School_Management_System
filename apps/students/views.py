from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student, Class
from .serializers import StudentSerializer, StudentCreateSerializer, ClassSerializer
from apps.accounts.permissions import IsAdmin, IsAdminOrTeacher


class ClassListCreateView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['academic_year', 'grade_level']
    search_fields = ['name', 'section']


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdmin]


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.select_related('user', 'current_class', 'parent').all()
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['current_class', 'gender', 'is_active']
    search_fields = ['admission_number', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['admission_number', 'user__first_name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentCreateSerializer
        return StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.select_related('user', 'current_class', 'parent').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrTeacher]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return super().get_permissions()
