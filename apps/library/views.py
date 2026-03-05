from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, BookIssue
from .serializers import BookSerializer, BookIssueSerializer
from apps.accounts.permissions import IsAdmin, IsAdminOrTeacher


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'publication_year']
    search_fields = ['title', 'author', 'isbn']


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrTeacher]


class BookIssueListCreateView(generics.ListCreateAPIView):
    queryset = BookIssue.objects.select_related('book', 'borrower', 'issued_by').all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'borrower', 'book']


class BookIssueDetailView(generics.RetrieveUpdateAPIView):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAdminOrTeacher]
