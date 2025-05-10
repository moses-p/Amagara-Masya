from django.db import models
from django.conf import settings
from core.models import BaseModel, CenterConfig
from math import radians, cos, sin, asin, sqrt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

class Child(BaseModel):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('transferred', 'Transferred'),
        ('inactive', 'Inactive'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    unique_identifier = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Enrollment(BaseModel):
    ENROLLMENT_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    ENROLLMENT_TYPES = (
        ('new', 'New Enrollment'),
        ('transfer', 'Transfer'),
        ('re_enrollment', 'Re-enrollment'),
    )
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20, unique=True)
    enrollment_date = models.DateField()
    enrollment_type = models.CharField(max_length=20, choices=ENROLLMENT_TYPES)
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS, default='pending')
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.child} - {self.enrollment_number}"

class ParentGuardian(BaseModel):
    RELATIONSHIP_TYPES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.relationship_type}"

class AcademicRecord(BaseModel):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    academic_level = models.CharField(max_length=50)
    school_name = models.CharField(max_length=200)
    performance = models.TextField()
    attendance = models.TextField()
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.child} - {self.academic_year}"

class MedicalRecord(BaseModel):
    RECORD_TYPES = (
        ('general', 'General Checkup'),
        ('vaccination', 'Vaccination'),
        ('treatment', 'Treatment'),
        ('emergency', 'Emergency'),
    )
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    record_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.child} - {self.record_type} - {self.record_date}"

class BudgetRecord(BaseModel):
    RECORD_TYPES = (
        ('education', 'Education'),
        ('medical', 'Medical'),
        ('clothing', 'Clothing'),
        ('food', 'Food'),
        ('other', 'Other'),
    )
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    record_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.child} - {self.record_type} - {self.record_date}"

class LocationHistory(BaseModel):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.child} - Location History"

class Tracking(BaseModel):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='tracking_records')
    last_seen = models.DateTimeField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    last_known_location = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('in_center', 'In Center'),
        ('off_premises', 'Off Premises'),
        ('escaped', 'Escaped'),
        ('unknown', 'Unknown')
    ], default='in_center')

    def is_outside_safe_zone(self, safe_zone=None):
        # Use CenterConfig for geofence
        try:
            center = safe_zone or CenterConfig.objects.first()
            if not center or not self.last_known_location:
                return False
            lat1, lon1 = map(float, self.last_known_location.split(','))
            lat2, lon2 = center.latitude, center.longitude
            # Haversine formula
            R = 6371000  # Earth radius in meters
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            distance = R * c
            return distance > center.safe_radius_m
        except Exception:
            return False

    def __str__(self):
        return f"{self.child} - {self.status} - {self.last_seen}"

class ChildAIProfile(models.Model):
    child = models.OneToOneField(Child, on_delete=models.CASCADE, related_name='ai_profile')
    escape_risk_score = models.FloatField(default=0.0)
    last_evaluated = models.DateTimeField(auto_now=True)

    def update_risk_score(self):
        # Placeholder: implement AI logic here
        # For now, assign a random risk score
        import random
        self.escape_risk_score = random.uniform(0, 1)
        self.save()

    def __str__(self):
        return f"AI Profile for {self.child} (Risk: {self.escape_risk_score:.2f})"

class WearableDevice(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='wearable_devices')
    device_id = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_id} for {self.child}"

def broadcast_dashboard_update():
    from .models import Child, Tracking, ChildAIProfile
    children = Child.objects.all()
    data = []
    for child in children:
        tracking = child.tracking_records.last() if hasattr(child, 'tracking_records') else None
        ai_profile = getattr(child, 'ai_profile', None)
        data.append({
            'id': child.id,
            'name': f"{child.first_name} {child.last_name}",
            'status': tracking.status if tracking else None,
            'last_known_location': tracking.last_known_location if tracking else None,
            'last_update': tracking.last_update if tracking else None,
            'risk_score': ai_profile.escape_risk_score if ai_profile else None,
        })
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard',
        {'type': 'dashboard_update', 'data': {'children': data}}
    )

@receiver(post_save, sender=Tracking)
def tracking_post_save(sender, instance, **kwargs):
    broadcast_dashboard_update()

@receiver(post_save, sender=ChildAIProfile)
def ai_profile_post_save(sender, instance, **kwargs):
    broadcast_dashboard_update() 