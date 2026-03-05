from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from .models import FeeStructure, FeePayment
from .serializers import FeeStructureSerializer, FeePaymentSerializer
from apps.accounts.permissions import IsAdmin, IsAdminOrTeacher


class FeeStructureListCreateView(generics.ListCreateAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fee_type', 'term', 'academic_year', 'grade_level']


class FeeStructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAdmin]


class FeePaymentListCreateView(generics.ListCreateAPIView):
    queryset = FeePayment.objects.select_related('student__user', 'fee_structure').all()
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'status', 'payment_method', 'fee_structure']


class FeePaymentDetailView(generics.RetrieveUpdateAPIView):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAdmin]


class StudentFeeView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request, student_id):
        payments = FeePayment.objects.filter(student_id=student_id).select_related('fee_structure')
        total_paid = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
        serializer = FeePaymentSerializer(payments, many=True)
        return Response({
            'payments': serializer.data,
            'total_paid': total_paid,
            'total_records': payments.count(),
        })


class FeeReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_collected = FeePayment.objects.filter(status='paid').aggregate(
            total=Sum('amount_paid'))['total'] or 0
        pending = FeePayment.objects.filter(status__in=['pending', 'partial']).aggregate(
            total=Sum('amount_paid'))['total'] or 0
        return Response({
            'total_collected': total_collected,
            'total_pending': pending,
            'paid_count': FeePayment.objects.filter(status='paid').count(),
            'pending_count': FeePayment.objects.filter(status__in=['pending', 'partial']).count(),
        })
