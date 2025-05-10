from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.permissions import IsStaff
from .models import Staff, StaffAssignment
from children.serializers import ChildSerializer, AcademicRecordSerializer, BudgetRecordSerializer
from children.models import Child, AcademicRecord, BudgetRecord
import csv
from django.http import HttpResponse
from core.utils import log_audit_action

@api_view(['GET'])
@permission_classes([IsStaff])
def assigned_children(request):
    staff = Staff.objects.get(user=request.user)
    assignments = StaffAssignment.objects.filter(staff=staff, is_active=True)
    children = [a.child for a in assignments]
    data = ChildSerializer(children, many=True, context={'request': request}).data
    return Response({'assigned_children': data})

@api_view(['GET'])
@permission_classes([IsStaff])
def printable_assigned_children_report(request):
    staff = Staff.objects.get(user=request.user)
    assignments = StaffAssignment.objects.filter(staff=staff, is_active=True)
    children = [a.child for a in assignments]
    children_data = ChildSerializer(children, many=True, context={'request': request}).data
    for child in children_data:
        child_id = child['id']
        child['academic_records'] = AcademicRecordSerializer(AcademicRecord.objects.filter(child_id=child_id), many=True, context={'request': request}).data
        child['budget_records'] = BudgetRecordSerializer(BudgetRecord.objects.filter(child_id=child_id), many=True, context={'request': request}).data
    log_audit_action(request.user, 'generate_report', 'Staff', details={'type': 'printable_assigned_children_report'})
    return Response({'assigned_children_report': children_data})

@api_view(['GET'])
@permission_classes([IsStaff])
def printable_assigned_children_report_csv(request):
    staff = Staff.objects.get(user=request.user)
    assignments = StaffAssignment.objects.filter(staff=staff, is_active=True)
    children = [a.child for a in assignments]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="staff_assigned_children_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Child ID', 'First Name', 'Last Name', 'Gender', 'Status', 'Unique ID'])
    for child in children:
        writer.writerow([child.id, child.first_name, child.last_name, child.gender, child.status, child.unique_identifier])
    log_audit_action(request.user, 'export_csv', 'Staff', details={'type': 'printable_assigned_children_report_csv'})
    return response 