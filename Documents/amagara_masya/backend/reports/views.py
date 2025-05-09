from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Report, ReportAccess, LocationReport, FinancialReport, CustomReport, AcademicReport
from .serializers import (
    ReportSerializer, ReportAccessSerializer, LocationReportSerializer,
    FinancialReportSerializer, CustomReportSerializer, AcademicReportSerializer
)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['report_type', 'status', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

class ReportAccessViewSet(viewsets.ModelViewSet):
    queryset = ReportAccess.objects.all()
    serializer_class = ReportAccessSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['user', 'report', 'access_type', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'report__title']
    ordering_fields = ['created_at']

class LocationReportViewSet(viewsets.ModelViewSet):
    queryset = LocationReport.objects.all()
    serializer_class = LocationReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['report', 'is_active']
    search_fields = ['report__title', 'location_name']
    ordering_fields = ['created_at', 'updated_at']

class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['report', 'report_type', 'is_active']
    search_fields = ['report__title', 'description']
    ordering_fields = ['created_at', 'updated_at']

class CustomReportViewSet(viewsets.ModelViewSet):
    queryset = CustomReport.objects.all()
    serializer_class = CustomReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['report', 'is_active']
    search_fields = ['report__title', 'description']
    ordering_fields = ['created_at', 'updated_at']

class AcademicReportViewSet(viewsets.ModelViewSet):
    queryset = AcademicReport.objects.all()
    serializer_class = AcademicReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['report', 'is_active']
    search_fields = ['report__title', 'description']
    ordering_fields = ['created_at', 'updated_at'] 