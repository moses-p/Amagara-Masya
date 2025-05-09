from django.db import models
from django.conf import settings
from core.models import BaseModel, Group, Location

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
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='current_children')
    last_known_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='last_known_children')
    notes = models.TextField(blank=True)

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

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
    documents = models.ManyToManyField('core.Document', blank=True)
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
    documents = models.ManyToManyField('core.Document', blank=True)
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
    documents = models.ManyToManyField('core.Document', blank=True)
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
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.child} - {self.location}"

class Tracking(BaseModel):
    STATUS_CHOICES = (
        ('missing', 'Missing'),
        ('found', 'Found'),
        ('under_investigation', 'Under Investigation'),
    )
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='tracking_records')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='missing')
    last_seen = models.DateTimeField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.child} - {self.status} - {self.last_seen}" 