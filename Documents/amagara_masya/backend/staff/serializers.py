from rest_framework import serializers
from .models import Staff, StaffRole, StaffSchedule, StaffAttendance, StaffLeave, StaffTraining, StaffPerformance
from core.serializers import UserSerializer, DocumentSerializer

class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = StaffRoleSerializer(read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class StaffScheduleSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    
    class Meta:
        model = StaffSchedule
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class StaffAttendanceSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    
    class Meta:
        model = StaffAttendance
        fields = '__all__'
        read_only_fields = ['created_at']

class StaffLeaveSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    
    class Meta:
        model = StaffLeave
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class StaffTrainingSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = StaffTraining
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class StaffPerformanceSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    evaluated_by = StaffSerializer(read_only=True)
    
    class Meta:
        model = StaffPerformance
        fields = '__all__'
        read_only_fields = ['created_at'] 