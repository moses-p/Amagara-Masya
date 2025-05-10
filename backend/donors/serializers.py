from rest_framework import serializers
from .models import Donor, Donation, Sponsorship
from core.models import User
from children.serializers import ChildSerializer

class DonorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type='donor'))
    total_donated = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = Donor
        fields = ['id', 'user', 'organization_name', 'address', 'donation_history', 
                 'total_donated', 'is_verified', 'verification_documents']
        read_only_fields = ['total_donated', 'is_verified']

    def validate_user(self, value):
        if value.user_type != 'donor':
            raise serializers.ValidationError("User must be of type 'donor'")
        return value

class DonationSerializer(serializers.ModelSerializer):
    donor = serializers.PrimaryKeyRelatedField(queryset=Donor.objects.all())
    receipt_number = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donor', 'amount', 'donation_type', 'description', 
                 'donation_date', 'is_anonymous', 'receipt_number', 'status']
        read_only_fields = ['receipt_number', 'status']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

    def create(self, validated_data):
        # Generate receipt number
        import uuid
        validated_data['receipt_number'] = f"RCP-{uuid.uuid4().hex[:8].upper()}"
        return super().create(validated_data)

class SponsorshipSerializer(serializers.ModelSerializer):
    donor = serializers.PrimaryKeyRelatedField(queryset=Donor.objects.all())
    child_details = ChildSerializer(source='child', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Sponsorship
        fields = ['id', 'donor', 'child', 'child_details', 'start_date', 'end_date',
                 'monthly_amount', 'status', 'notes']
        read_only_fields = ['status']

    def get_fields(self):
        fields = super().get_fields()
        from children.models import Child
        fields['child'] = serializers.PrimaryKeyRelatedField(queryset=Child.objects.all())
        return fields

    def validate(self, data):
        if data.get('end_date') and data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

    def validate_monthly_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Monthly amount must be greater than zero")
        return value 