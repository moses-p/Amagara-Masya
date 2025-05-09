from django.db import models
from django.conf import settings
from core.models import BaseModel, User, Document
from children.models import Child
from phonenumber_field.modelfields import PhoneNumberField

RATING_CHOICES = (
    (1, 'Poor'),
    (2, 'Below Average'),
    (3, 'Average'),
    (4, 'Above Average'),
    (5, 'Excellent')
)

NOTE_TYPES = (
    ('general', 'General Note'),
    ('performance', 'Performance Note'),
    ('disciplinary', 'Disciplinary Note'),
    ('achievement', 'Achievement Note'),
    ('training', 'Training Note')
)

class StaffRole(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Staff(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    role = models.ForeignKey(StaffRole, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField()
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"

class StaffSchedule(BaseModel):
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.staff} - {self.day_of_week}"

class StaffAttendance(BaseModel):
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
    )

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.staff} - {self.date} - {self.status}"

class StaffLeave(BaseModel):
    LEAVE_TYPES = (
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('other', 'Other'),
    )

    LEAVE_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.staff} - {self.leave_type} - {self.start_date}"

class StaffTraining(BaseModel):
    TRAINING_TYPES = (
        ('onboarding', 'Onboarding'),
        ('professional', 'Professional Development'),
        ('safety', 'Safety Training'),
        ('other', 'Other'),
    )

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPES)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    documents = models.ManyToManyField('core.Document', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.staff} - {self.title}"

class StaffPerformance(BaseModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='performance_records')
    evaluated_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='performance_evaluations_given')
    evaluation_date = models.DateField()
    performance_rating = models.IntegerField(choices=RATING_CHOICES)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals = models.TextField()
    
    def __str__(self):
        return f"Performance record for {self.staff} on {self.evaluation_date}"

class StaffAssignment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='staff_assignments')
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.staff} assigned to {self.child} as {self.role}"

class StaffNote(BaseModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_notes')
    note_type = models.CharField(max_length=50, choices=NOTE_TYPES)
    note_date = models.DateField()
    content = models.TextField()
    created_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='staff_notes_created'
    )
    
    def __str__(self):
        return f"Note for {self.staff} on {self.note_date}"

class StaffEvaluation(BaseModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='evaluations_received')
    evaluator = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='evaluations_performed')
    evaluation_date = models.DateField()
    performance_rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    next_evaluation_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Evaluation of {self.staff} by {self.evaluator} on {self.evaluation_date}" 