from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReportViewSet, ReportAccessViewSet, LocationReportViewSet,
    FinancialReportViewSet, CustomReportViewSet, AcademicReportViewSet
)

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'report-access', ReportAccessViewSet, basename='report-access')
router.register(r'location-reports', LocationReportViewSet, basename='location-report')
router.register(r'financial-reports', FinancialReportViewSet, basename='financial-report')
router.register(r'custom-reports', CustomReportViewSet, basename='custom-report')
router.register(r'academic-reports', AcademicReportViewSet, basename='academic-report')

urlpatterns = [
    path('', include(router.urls)),
] 