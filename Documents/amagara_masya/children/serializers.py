from rest_framework import serializers
from .models import Photo, Child

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'status', 'created_at', 'updated_at']

class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Photo
        fields = ['id', 'child', 'photo', 'date', 'description', 'url']
        read_only_fields = ['date', 'uploaded_by']

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data) 