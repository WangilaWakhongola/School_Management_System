from django.urls import path
from . import views

urlpatterns = [
    path('structures/', views.FeeStructureListCreateView.as_view(), name='fee-structure-list'),
    path('structures/<int:pk>/', views.FeeStructureDetailView.as_view(), name='fee-structure-detail'),
    path('payments/', views.FeePaymentListCreateView.as_view(), name='fee-payment-list'),
    path('payments/<int:pk>/', views.FeePaymentDetailView.as_view(), name='fee-payment-detail'),
    path('student/<int:student_id>/', views.StudentFeeView.as_view(), name='student-fees'),
    path('report/', views.FeeReportView.as_view(), name='fee-report'),
]
