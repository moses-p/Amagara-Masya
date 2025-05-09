from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StaffViewSet, StaffRoleViewSet, StaffScheduleViewSet,
    StaffAttendanceViewSet, StaffLeaveViewSet, StaffTrainingViewSet,
    StaffPerformanceViewSet
)

router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'roles', StaffRoleViewSet, basename='staff-role')
router.register(r'schedules', StaffScheduleViewSet, basename='staff-schedule')
router.register(r'attendance', StaffAttendanceViewSet, basename='staff-attendance')
router.register(r'leaves', StaffLeaveViewSet, basename='staff-leave')
router.register(r'trainings', StaffTrainingViewSet, basename='staff-training')
router.register(r'performance', StaffPerformanceViewSet, basename='staff-performance')

urlpatterns = [
    path('', include(router.urls)),
] 