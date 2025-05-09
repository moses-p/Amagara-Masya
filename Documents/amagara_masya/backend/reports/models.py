from django.db import models
from django.conf import settings
from core.models import BaseModel

class Report(BaseModel):
    REPORT_TYPES = (
        ('location', 'Location Report'),
        ('financial', 'Financial Report'),
        ('academic', 'Academic Report'),
        ('custom', 'Custom Report'),
    )

    REPORT_STATUS = (
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    documents = models.ManyToManyField('core.Document', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.report_type}"

class ReportAccess(BaseModel):
    ACCESS_TYPES = (
        ('view', 'View'),
        ('edit', 'Edit'),
        ('admin', 'Admin'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPES)

    def __str__(self):
        return f"{self.user} - {self.report} - {self.access_type}"

class LocationReport(BaseModel):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    findings = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Location Report - {self.location_name}"

class FinancialReport(BaseModel):
    REPORT_TYPES = (
        ('income', 'Income Report'),
        ('expense', 'Expense Report'),
        ('budget', 'Budget Report'),
        ('donation', 'Donation Report'),
    )

    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    analysis = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Financial Report - {self.report_type}"

class CustomReport(BaseModel):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    template = models.TextField()
    data = models.JSONField()
    analysis = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Custom Report - {self.report.title}"

class AcademicReport(BaseModel):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    term = models.CharField(max_length=20)
    performance_summary = models.TextField()
    challenges = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Academic Report - {self.academic_year} - {self.term}" 