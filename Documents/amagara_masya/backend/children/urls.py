from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChildViewSet, EnrollmentViewSet, ParentGuardianViewSet,
    AcademicRecordViewSet, MedicalRecordViewSet, BudgetRecordViewSet,
    LocationHistoryViewSet, TrackingViewSet
)

router = DefaultRouter()
router.register(r'children', ChildViewSet, basename='child')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'parent-guardians', ParentGuardianViewSet, basename='parent-guardian')
router.register(r'academic-records', AcademicRecordViewSet, basename='academic-record')
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')
router.register(r'budget-records', BudgetRecordViewSet, basename='budget-record')
router.register(r'location-history', LocationHistoryViewSet, basename='location-history')
router.register(r'tracking', TrackingViewSet, basename='tracking')

urlpatterns = [
    path('', include(router.urls)),
] 