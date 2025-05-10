from django.urls import path
from . import views

urlpatterns = [
    path('assigned-children/', views.assigned_children, name='assigned_children'),
    path('printable-assigned-children-report/', views.printable_assigned_children_report, name='printable_assigned_children_report'),
    path('printable-assigned-children-report-csv/', views.printable_assigned_children_report_csv, name='printable_assigned_children_report_csv'),
] 