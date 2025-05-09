from rest_framework import serializers
from .models import Report, ReportAccess, LocationReport, FinancialReport, CustomReport, AcademicReport
from core.serializers import UserSerializer, DocumentSerializer

class ReportSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ReportAccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    report = ReportSerializer(read_only=True)
    
    class Meta:
        model = ReportAccess
        fields = '__all__'
        read_only_fields = ['created_at']

class LocationReportSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    
    class Meta:
        model = LocationReport
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class FinancialReportSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    
    class Meta:
        model = FinancialReport
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CustomReportSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    
    class Meta:
        model = CustomReport
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class AcademicReportSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    
    class Meta:
        model = AcademicReport
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at'] 