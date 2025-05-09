from rest_framework import serializers
from .models import Donor, Donation, DonationType, DonationCampaign, DonorCommunication
from core.serializers import UserSerializer, DocumentSerializer

class DonationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationType
        fields = '__all__'

class DonorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class DonationSerializer(serializers.ModelSerializer):
    donor = DonorSerializer(read_only=True)
    donation_type = DonationTypeSerializer(read_only=True)
    processed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class DonationCampaignSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = DonationCampaign
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class DonorCommunicationSerializer(serializers.ModelSerializer):
    donor = DonorSerializer(read_only=True)
    initiated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = DonorCommunication
        fields = '__all__'
        read_only_fields = ['created_at'] 