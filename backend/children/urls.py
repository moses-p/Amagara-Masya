from django.urls import path
from .views import child_risk_score, simulate_location_update, dashboard_child_locations, wearable_location_update, list_wearable_devices, create_wearable_device, set_wearable_device_active, delete_wearable_device

urlpatterns = []
urlpatterns += [
    path('child/<int:child_id>/risk-score/', child_risk_score, name='child-risk-score'),
    path('child/<int:child_id>/simulate-location/', simulate_location_update, name='simulate-location-update'),
    path('dashboard/child-locations/', dashboard_child_locations, name='dashboard-child-locations'),
    path('wearable/location-update/', wearable_location_update, name='wearable-location-update'),
    path('wearable/devices/', list_wearable_devices, name='list-wearable-devices'),
    path('wearable/devices/create/', create_wearable_device, name='create-wearable-device'),
    path('wearable/devices/<int:device_id>/set-active/', set_wearable_device_active, name='set-wearable-device-active'),
    path('wearable/devices/<int:device_id>/delete/', delete_wearable_device, name='delete-wearable-device'),
] 