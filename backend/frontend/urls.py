from .views import (
    login_view, logout_view, admin_dashboard, staff_dashboard, donor_dashboard,
    notifications, device_management, audit_log, settings_view
)
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),
    path('donor-dashboard/', donor_dashboard, name='donor_dashboard'),
    path('notifications/', notifications, name='notifications'),
    path('device-management/', device_management, name='device_management'),
    path('audit-log/', audit_log, name='audit_log'),
    path('settings/', settings_view, name='settings'),
    path('anomalies/', views.anomaly_dashboard, name='anomaly_dashboard'),
] 