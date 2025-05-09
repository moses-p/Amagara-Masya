from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Group, Location, Document, AuditLog

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 
                 'phone_number', 'profile_picture', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'year_formed', 'description', 'is_active']
        read_only_fields = ['id']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'is_active']
        read_only_fields = ['id']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'document_type', 'file', 'upload_date', 'description']
        read_only_fields = ['id', 'upload_date']

class AuditLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'model', 'object_id', 'timestamp', 'details']
        read_only_fields = ['id', 'timestamp'] 