from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorViewSet, DonationViewSet, DonationTypeViewSet,
    DonationCampaignViewSet, DonorCommunicationViewSet
)

router = DefaultRouter()
router.register(r'donors', DonorViewSet, basename='donor')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'donation-types', DonationTypeViewSet, basename='donation-type')
router.register(r'campaigns', DonationCampaignViewSet, basename='donation-campaign')
router.register(r'communications', DonorCommunicationViewSet, basename='donor-communication')

urlpatterns = [
    path('', include(router.urls)),
] 