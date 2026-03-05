from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeacherListCreateView.as_view(), name='teacher-list'),
    path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('subjects/', views.SubjectListCreateView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
]
