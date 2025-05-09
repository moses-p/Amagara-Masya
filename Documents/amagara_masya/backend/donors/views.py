from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Donor, Donation, DonationType, DonationCampaign, DonorCommunication
from .serializers import (
    DonorSerializer, DonationSerializer, DonationTypeSerializer,
    DonationCampaignSerializer, DonorCommunicationSerializer
)

class DonationTypeViewSet(viewsets.ModelViewSet):
    queryset = DonationType.objects.all()
    serializer_class = DonationTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['donor_type', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'organization_name']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['donor', 'donation_type', 'status', 'is_active']
    search_fields = ['donor__user__first_name', 'donor__user__last_name', 'donor__organization_name']
    ordering_fields = ['donation_date', 'amount', 'created_at']

class DonationCampaignViewSet(viewsets.ModelViewSet):
    queryset = DonationCampaign.objects.all()
    serializer_class = DonationCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['status', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']

class DonorCommunicationViewSet(viewsets.ModelViewSet):
    queryset = DonorCommunication.objects.all()
    serializer_class = DonorCommunicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['donor', 'communication_type', 'is_active']
    search_fields = ['donor__user__first_name', 'donor__user__last_name', 'subject']
    ordering_fields = ['communication_date', 'created_at'] 