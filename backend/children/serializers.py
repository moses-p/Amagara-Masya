from rest_framework import serializers
from .models import Child, ParentGuardian, AcademicRecord, BudgetRecord, ChildAIProfile, WearableDevice

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name', 'nickname', 'date_of_birth', 'gender', 'unique_identifier', 'status', 'notes']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        # Hide notes for donors
        if hasattr(user, 'user_type') and user.user_type == 'donor':
            data.pop('notes', None)
        return data

class ParentGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentGuardian
        fields = ['id', 'first_name', 'last_name', 'relationship_type', 'phone_number', 'email', 'address', 'occupation', 'notes']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        # Only admins and staff can see contact info
        if not (hasattr(user, 'user_type') and user.user_type in ['admin', 'staff']):
            data.pop('phone_number', None)
            data.pop('email', None)
            data.pop('address', None)
        return data

class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['id', 'child', 'academic_year', 'academic_level', 'school_name', 'performance', 'attendance', 'notes']

class BudgetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetRecord
        fields = ['id', 'child', 'record_type', 'record_date', 'amount', 'description', 'created_by', 'notes']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        # Donors can only see amount, record_type, and record_date
        if hasattr(user, 'user_type') and user.user_type == 'donor':
            allowed = {'id', 'child', 'record_type', 'record_date', 'amount'}
            data = {k: v for k, v in data.items() if k in allowed}
        return data

class ChildAIProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildAIProfile
        fields = ['escape_risk_score', 'last_evaluated']

class WearableDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WearableDevice
        fields = ['id', 'child', 'device_id', 'description', 'is_active', 'last_seen'] 