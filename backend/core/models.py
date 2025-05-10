from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('donor', 'Donor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='staff')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_notify_email = models.BooleanField(default=True)
    profile_notify_push = models.BooleanField(default=True)

    def __str__(self):
        return self.username 

class Notification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.user}: {self.message[:50]}" 

class CenterConfig(models.Model):
    name = models.CharField(max_length=100, default='Main Center')
    latitude = models.FloatField()
    longitude = models.FloatField()
    safe_radius_m = models.FloatField(default=100.0)  # meters

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})" 

class UserDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    device_token = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=50, blank=True)  # e.g., 'android', 'ios', 'web'
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.device_type} - {self.device_token[:10]}..." 

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action} on {self.model_name}" 