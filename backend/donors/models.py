from django.db import models
from django.conf import settings
from core.models import BaseModel
from children.models import Child

class Donor(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    donation_history = models.TextField(blank=True, null=True)
    total_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    verification_documents = models.FileField(upload_to='donor_documents/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Donor"
        verbose_name_plural = "Donors"

class Donation(BaseModel):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=50, choices=[
        ('monetary', 'Monetary'),
        ('in_kind', 'In-Kind'),
        ('sponsorship', 'Child Sponsorship')
    ])
    description = models.TextField(blank=True, null=True)
    donation_date = models.DateField()
    is_anonymous = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')

    def __str__(self):
        return f"Donation from {self.donor} - {self.amount}"

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ['-donation_date']

class Sponsorship(BaseModel):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='sponsorships')
    child = models.ForeignKey('children.Child', on_delete=models.CASCADE, related_name='sponsorships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='active')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.donor} sponsors {self.child}"

    class Meta:
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorships"
        ordering = ['-start_date'] 