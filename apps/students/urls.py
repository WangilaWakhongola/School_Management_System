from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListCreateView.as_view(), name='student-list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('classes/', views.ClassListCreateView.as_view(), name='class-list'),
    path('classes/<int:pk>/', views.ClassDetailView.as_view(), name='class-detail'),
]
