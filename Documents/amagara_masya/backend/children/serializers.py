from rest_framework import serializers
from .models import Enrollment, Child, ParentGuardian, AcademicRecord, MedicalRecord, BudgetRecord, LocationHistory, Tracking
from core.serializers import UserSerializer, LocationSerializer, DocumentSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')

class EnrollmentDocumentSerializer(serializers.Serializer):
    document = serializers.FileField()
    document_type = serializers.CharField(max_length=20)
    description = serializers.CharField(required=False)

class EnrollmentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Enrollment.ENROLLMENT_STATUS)
    notes = serializers.CharField(required=False)

class ChildSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSerializer(read_only=True)
    group = serializers.StringRelatedField()
    current_location = LocationSerializer(read_only=True)
    last_known_location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Child
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ParentGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentGuardian
        fields = '__all__'

class AcademicRecordSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = AcademicRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class MedicalRecordSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class BudgetRecordSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = BudgetRecord
        fields = '__all__'
        read_only_fields = ['created_at']

class LocationHistorySerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    recorded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = LocationHistory
        fields = '__all__'
        read_only_fields = ['created_at']

class TrackingSerializer(serializers.ModelSerializer):
    child = ChildSerializer(read_only=True)
    reported_by = UserSerializer(read_only=True)

    class Meta:
        model = Tracking
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at'] 