from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Staff, StaffRole, StaffSchedule, StaffAttendance, StaffLeave, StaffTraining, StaffPerformance
from .serializers import (
    StaffSerializer, StaffRoleSerializer, StaffScheduleSerializer,
    StaffAttendanceSerializer, StaffLeaveSerializer, StaffTrainingSerializer,
    StaffPerformanceSerializer
)

class StaffRoleViewSet(viewsets.ModelViewSet):
    queryset = StaffRole.objects.all()
    serializer_class = StaffRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['role', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'staff_id']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']

class StaffScheduleViewSet(viewsets.ModelViewSet):
    queryset = StaffSchedule.objects.all()
    serializer_class = StaffScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['staff', 'day_of_week', 'is_active']
    search_fields = ['staff__user__first_name', 'staff__user__last_name']
    ordering_fields = ['day_of_week', 'start_time', 'created_at']

class StaffAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StaffAttendance.objects.all()
    serializer_class = StaffAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['staff', 'status', 'is_active']
    search_fields = ['staff__user__first_name', 'staff__user__last_name']
    ordering_fields = ['date', 'check_in_time', 'created_at']

class StaffLeaveViewSet(viewsets.ModelViewSet):
    queryset = StaffLeave.objects.all()
    serializer_class = StaffLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['staff', 'leave_type', 'status', 'is_active']
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'reason']
    ordering_fields = ['start_date', 'end_date', 'created_at']

class StaffTrainingViewSet(viewsets.ModelViewSet):
    queryset = StaffTraining.objects.all()
    serializer_class = StaffTrainingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['staff', 'training_type', 'is_active']
    search_fields = ['staff__user__first_name', 'staff__user__last_name', 'title']
    ordering_fields = ['start_date', 'end_date', 'created_at']

class StaffPerformanceViewSet(viewsets.ModelViewSet):
    queryset = StaffPerformance.objects.all()
    serializer_class = StaffPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['staff', 'evaluated_by', 'is_active']
    search_fields = ['staff__user__first_name', 'staff__user__last_name']
    ordering_fields = ['evaluation_date', 'created_at'] 