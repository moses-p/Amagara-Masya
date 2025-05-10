from staff.models import Staff, StaffAssignment
from donors.models import Donor, Sponsorship, Donation
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from ai.models import Anomaly
from django.utils import timezone

@login_required
def staff_dashboard(request):
    staff = Staff.objects.get(user=request.user)
    assignments = StaffAssignment.objects.filter(staff=staff, is_active=True)
    return render(request, 'frontend/staff_dashboard.html', {'assignments': assignments})

@login_required
def donor_dashboard(request):
    donor = Donor.objects.get(user=request.user)
    sponsored_children = Sponsorship.objects.filter(donor=donor, status='active')
    donation_history = Donation.objects.filter(donor=donor)
    return render(request, 'frontend/donor_dashboard.html', {
        'sponsored_children': sponsored_children,
        'donation_history': donation_history,
    })

@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'frontend/notifications.html', {'notifications': notes})

@login_required
def device_management(request):
    devices = UserDevice.objects.filter(user=request.user)
    return render(request, 'frontend/device_management.html', {'devices': devices})

@login_required
def audit_log(request):
    logs = AuditLog.objects.all().order_by('-timestamp')[:100]
    return render(request, 'frontend/audit_log.html', {'logs': logs})

@login_required
def settings_view(request):
    # Add logic to update notification preferences if POST
    return render(request, 'frontend/settings.html')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def anomaly_dashboard(request):
    anomalies = Anomaly.objects.all().order_by('-timestamp')
    severity = request.GET.get('severity')
    anomaly_type = request.GET.get('type')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')

    if severity:
        anomalies = anomalies.filter(severity=severity)
    if anomaly_type:
        anomalies = anomalies.filter(anomaly_type=anomaly_type)
    if date_from:
        anomalies = anomalies.filter(timestamp__gte=date_from)
    if date_to:
        anomalies = anomalies.filter(timestamp__lte=date_to)

    context = {
        'anomalies': anomalies[:100],
        'severity': severity,
        'anomaly_type': anomaly_type,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'frontend/anomaly_dashboard.html', context) 