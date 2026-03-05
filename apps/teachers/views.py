from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Teacher, Subject
from .serializers import TeacherSerializer, TeacherCreateSerializer, SubjectSerializer
from apps.accounts.permissions import IsAdmin, IsAdminOrTeacher


class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrTeacher]
    search_fields = ['name', 'code']


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdmin]


class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.select_related('user').prefetch_related('subjects').all()
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeacherCreateSerializer
        return TeacherSerializer


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.select_related('user').prefetch_related('subjects').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]
