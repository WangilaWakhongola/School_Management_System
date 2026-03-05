from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('issues/', views.BookIssueListCreateView.as_view(), name='book-issue-list'),
    path('issues/<int:pk>/', views.BookIssueDetailView.as_view(), name='book-issue-detail'),
]
