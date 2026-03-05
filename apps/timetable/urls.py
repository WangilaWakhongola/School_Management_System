from django.urls import path
from . import views

urlpatterns = [
    path('', views.TimetableListCreateView.as_view(), name='timetable-list'),
    path('<int:pk>/', views.TimetableDetailView.as_view(), name='timetable-detail'),
    path('slots/', views.TimeSlotListCreateView.as_view(), name='timeslot-list'),
]
