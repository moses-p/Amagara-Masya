from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User, Document, BaseModel
from children.models import Child
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class DonationType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Donor(BaseModel):
    DONOR_TYPES = (
        ('individual', 'Individual'),
        ('organization', 'Organization'),
        ('corporate', 'Corporate'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    donor_type = models.CharField(max_length=20, choices=DONOR_TYPES)
    organization_name = models.CharField(max_length=200, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    documents = models.ManyToManyField(Document, blank=True)
    
    def __str__(self):
        if self.donor_type == 'individual':
            return f"{self.user.first_name} {self.user.last_name}"
        return self.organization_name

class Sponsorship(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='sponsorships')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='sponsorships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_frequency = models.CharField(max_length=20, default='monthly')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor} sponsors {self.child}"

class Donation(BaseModel):
    DONATION_STATUS = (
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    )

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donation_type = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    donation_date = models.DateField()
    status = models.CharField(max_length=20, choices=DONATION_STATUS, default='pending')
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.donor} - {self.donation_type} - {self.donation_date}"

class DonorReport(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=200)
    content = models.TextField()
    period_start = models.DateField()
    period_end = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    documents = models.ManyToManyField(Document, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.donor}"

class DonationCampaign(BaseModel):
    CAMPAIGN_STATUS = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    documents = models.ManyToManyField('core.Document', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

class DonorCommunication(BaseModel):
    COMMUNICATION_TYPES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('meeting', 'Meeting'),
        ('letter', 'Letter'),
        ('other', 'Other'),
    )
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPES)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    communication_date = models.DateTimeField()
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.donor} - {self.subject} - {self.communication_date}" 