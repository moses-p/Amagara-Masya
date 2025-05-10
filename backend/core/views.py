from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAdmin, IsDonor, IsStaff
from children.models import Child, Enrollment, AcademicRecord
from donors.models import Donor, Sponsorship, Donation
from staff.models import Staff, StaffAssignment
from django.contrib.auth import get_user_model
from django.db import models
from children.serializers import ChildSerializer, ParentGuardianSerializer, AcademicRecordSerializer, BudgetRecordSerializer
import csv
from django.http import HttpResponse
from core.utils import log_audit_action
from .models import UserDevice
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard(request):
    children_count = Child.objects.count()
    staff_count = Staff.objects.count()
    donor_count = Donor.objects.count()
    active_children = Child.objects.filter(status='active').count()
    graduated_children = Child.objects.filter(status='graduated').count()
    total_donations = Donation.objects.filter(status='received').aggregate(total=models.Sum('amount'))['total'] or 0
    return Response({
        'children_count': children_count,
        'staff_count': staff_count,
        'donor_count': donor_count,
        'active_children': active_children,
        'graduated_children': graduated_children,
        'total_donations': total_donations,
    })

@api_view(['GET'])
@permission_classes([IsDonor])
def donor_dashboard(request):
    donor = Donor.objects.get(user=request.user)
    sponsored_children = [s.child.first_name + ' ' + s.child.last_name for s in Sponsorship.objects.filter(donor=donor, status='active')]
    donation_history = list(Donation.objects.filter(donor=donor).values('amount', 'donation_date', 'status'))
    impact_reports = []  # Placeholder for future donor reports
    return Response({
        'sponsored_children': sponsored_children,
        'donation_history': donation_history,
        'impact_reports': impact_reports,
    })

@api_view(['GET'])
@permission_classes([IsStaff])
def staff_dashboard(request):
    staff = Staff.objects.get(user=request.user)
    assignments = list(StaffAssignment.objects.filter(staff=staff, is_active=True).values('child__first_name', 'child__last_name', 'role'))
    return Response({
        'assignments': assignments,
    })

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_printable_children_report(request):
    children = Child.objects.all()
    children_data = ChildSerializer(children, many=True, context={'request': request}).data
    # Optionally include related data
    for child in children_data:
        child_id = child['id']
        child['parents'] = ParentGuardianSerializer(ParentGuardian.objects.filter(child_id=child_id), many=True, context={'request': request}).data
        child['academic_records'] = AcademicRecordSerializer(AcademicRecord.objects.filter(child_id=child_id), many=True, context={'request': request}).data
        child['budget_records'] = BudgetRecordSerializer(BudgetRecord.objects.filter(child_id=child_id), many=True, context={'request': request}).data
    log_audit_action(request.user, 'generate_report', 'Child', details={'type': 'admin_printable_children_report'})
    return Response({'children_report': children_data})

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_printable_children_report_csv(request):
    from children.models import Child
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="children_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Gender', 'Status', 'Unique ID'])
    for child in Child.objects.all():
        writer.writerow([child.id, child.first_name, child.last_name, child.gender, child.status, child.unique_identifier])
    log_audit_action(request.user, 'export_csv', 'Child', details={'type': 'admin_printable_children_report_csv'})
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device_token(request):
    token = request.data.get('device_token')
    device_type = request.data.get('device_type', '')
    if not token:
        return Response({'detail': 'device_token required.'}, status=400)
    device, created = UserDevice.objects.get_or_create(user=request.user, device_token=token)
    device.device_type = device_type
    device.save()
    return Response({'detail': 'Device registered.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deregister_device_token(request):
    token = request.data.get('device_token')
    if not token:
        return Response({'detail': 'device_token required.'}, status=400)
    UserDevice.objects.filter(user=request.user, device_token=token).delete()
    return Response({'detail': 'Device deregistered.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_notification_preferences(request):
    # Example: {"email": true, "push": true}
    email = request.data.get('email')
    push = request.data.get('push')
    user = request.user
    if email is not None:
        user.profile_notify_email = bool(email)
    if push is not None:
        user.profile_notify_push = bool(push)
    user.save()
    return Response({'detail': 'Notification preferences updated.'}) 