from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.ExamListCreateView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam-detail'),
    path('', views.GradeListCreateView.as_view(), name='grade-list'),
    path('<int:pk>/', views.GradeDetailView.as_view(), name='grade-detail'),
    path('bulk/', views.BulkGradeView.as_view(), name='grade-bulk'),
    path('report/<int:student_id>/', views.StudentReportView.as_view(), name='student-report'),
]
