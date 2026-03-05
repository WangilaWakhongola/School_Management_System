from django.urls import path
from . import views

urlpatterns = [
    path('', views.AttendanceListCreateView.as_view(), name='attendance-list'),
    path('<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    path('bulk/', views.BulkAttendanceView.as_view(), name='attendance-bulk'),
    path('summary/', views.AttendanceSummaryView.as_view(), name='attendance-summary'),
    path('student/<int:student_id>/', views.StudentAttendanceView.as_view(), name='student-attendance'),
]
