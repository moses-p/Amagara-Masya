from django.urls import path
from . import views
from .views import register_device_token, deregister_device_token, set_notification_preferences

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('admin-printable-children-report/', views.admin_printable_children_report, name='admin_printable_children_report'),
    path('admin-printable-children-report-csv/', views.admin_printable_children_report_csv, name='admin_printable_children_report_csv'),
    path('register-device-token/', register_device_token, name='register-device-token'),
    path('deregister-device-token/', deregister_device_token, name='deregister-device-token'),
    path('set-notification-preferences/', set_notification_preferences, name='set-notification-preferences'),
] 