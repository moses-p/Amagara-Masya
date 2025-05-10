from django.db import models
from django.conf import settings
from core.models import BaseModel
from children.models import Child

class Staff(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

class StaffAssignment(BaseModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    child = models.ForeignKey('children.Child', on_delete=models.CASCADE, related_name='assignments')
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.staff} assigned to {self.child}"

    class Meta:
        verbose_name = "Staff Assignment"
        verbose_name_plural = "Staff Assignments" 