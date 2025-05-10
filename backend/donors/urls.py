from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'donors', views.DonorViewSet)
router.register(r'donations', views.DonationViewSet)
router.register(r'sponsorships', views.SponsorshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('export-csv/', views.export_csv, name='export-csv'),
    path('printable-report/', views.printable_report, name='printable-report'),
] 