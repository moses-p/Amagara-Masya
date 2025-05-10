from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.permissions import IsDonor
from .models import Donor, Sponsorship, Donation
from children.serializers import ChildSerializer, BudgetRecordSerializer
from children.models import Child, BudgetRecord
from django.db import models
import csv
from django.http import HttpResponse
from core.utils import log_audit_action
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django.db.models import Sum
from django.utils import timezone
from .serializers import DonorSerializer, DonationSerializer, SponsorshipSerializer
from core.models import Notification, User

@api_view(['GET'])
@permission_classes([IsDonor])
def sponsored_children(request):
    donor = Donor.objects.get(user=request.user)
    sponsorships = Sponsorship.objects.filter(donor=donor, status='active')
    children = [s.child for s in sponsorships]
    data = ChildSerializer(children, many=True, context={'request': request}).data
    return Response({'sponsored_children': data})

@api_view(['GET'])
@permission_classes([IsDonor])
def donation_history(request):
    donor = Donor.objects.get(user=request.user)
    donations = Donation.objects.filter(donor=donor).values('amount', 'donation_date', 'status')
    return Response({'donation_history': list(donations)})

@api_view(['GET'])
@permission_classes([IsDonor])
def impact_report(request):
    donor = Donor.objects.get(user=request.user)
    sponsorships = Sponsorship.objects.filter(donor=donor, status='active')
    children_ids = [s.child.id for s in sponsorships]
    budgets = BudgetRecord.objects.filter(child_id__in=children_ids)
    data = BudgetRecordSerializer(budgets, many=True, context={'request': request}).data
    return Response({'impact_report': data})

@api_view(['GET'])
@permission_classes([IsDonor])
def printable_impact_report(request):
    donor = Donor.objects.get(user=request.user)
    sponsorships = Sponsorship.objects.filter(donor=donor, status='active')
    children = [s.child for s in sponsorships]
    children_data = ChildSerializer(children, many=True, context={'request': request}).data
    donations = Donation.objects.filter(donor=donor, status='received')
    total_donated = donations.aggregate(total=models.Sum('amount'))['total'] or 0
    impact_data = {
        'sponsored_children': children_data,
        'total_donated': total_donated,
        'donation_history': list(donations.values('amount', 'donation_date', 'status')),
    }
    log_audit_action(request.user, 'generate_report', 'Donor', details={'type': 'printable_impact_report'})
    return Response({'printable_impact_report': impact_data})

@api_view(['GET'])
@permission_classes([IsDonor])
def printable_impact_report_csv(request):
    donor = Donor.objects.get(user=request.user)
    sponsorships = Sponsorship.objects.filter(donor=donor, status='active')
    children = [s.child for s in sponsorships]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donor_impact_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Child ID', 'First Name', 'Last Name', 'Gender', 'Status', 'Unique ID'])
    for child in children:
        writer.writerow([child.id, child.first_name, child.last_name, child.gender, child.status, child.unique_identifier])
    donations = Donation.objects.filter(donor=donor, status='received')
    writer.writerow([])
    writer.writerow(['Donation History'])
    writer.writerow(['Amount', 'Date', 'Status'])
    for d in donations:
        writer.writerow([d.amount, d.donation_date, d.status])
    log_audit_action(request.user, 'export_csv', 'Donor', details={'type': 'printable_impact_report_csv'})
    return response

@api_view(['GET'])
@permission_classes([IsDonor])
def export_csv(request):
    # Placeholder for CSV export logic
    return Response({"message": "CSV export functionality will be implemented here."})

@api_view(['GET'])
@permission_classes([IsDonor])
def printable_report(request):
    # Placeholder for printable report logic
    return Response({"message": "Printable report functionality will be implemented here."})

class IsDonorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'admin':
            return True
        return obj.user == request.user

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDonorOrAdmin]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return Donor.objects.all()
        return Donor.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def donations(self, request, pk=None):
        donor = self.get_object()
        donations = donor.donations.all()
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def donation_summary(self, request, pk=None):
        donor = self.get_object()
        summary = {
            'total_donated': donor.total_donated,
            'donation_count': donor.donations.count(),
            'last_donation': donor.donations.order_by('-donation_date').first(),
            'donation_by_type': donor.donations.values('donation_type').annotate(
                total=Sum('amount')
            )
        }
        return Response(summary)

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Donation.objects.all()
        elif user.user_type == 'donor':
            return Donation.objects.filter(donor__user=user)
        return Donation.objects.none()

    def perform_create(self, serializer):
        donation = serializer.save()
        # Create notification for admin
        Notification.objects.create(
            user=User.objects.filter(user_type='admin').first(),
            message=f"New donation received from {donation.donor.user.username} for {donation.amount}"
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response(
                {"detail": "Only admins can approve donations"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        donation = self.get_object()
        donation.status = 'approved'
        donation.save()
        
        # Update donor's total_donated
        donor = donation.donor
        donor.total_donated = donor.donations.filter(status='approved').aggregate(
            total=Sum('amount')
        )['total'] or 0
        donor.save()
        
        # Create notification for donor
        Notification.objects.create(
            user=donation.donor.user,
            message=f"Your donation of {donation.amount} has been approved"
        )
        
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response(
                {"detail": "Only admins can reject donations"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        donation = self.get_object()
        donation.status = 'rejected'
        donation.save()
        
        # Create notification for donor
        Notification.objects.create(
            user=donation.donor.user,
            message=f"Your donation of {donation.amount} has been rejected"
        )
        
        return Response({"status": "rejected"})

class SponsorshipViewSet(viewsets.ModelViewSet):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Sponsorship.objects.all()
        elif user.user_type == 'donor':
            return Sponsorship.objects.filter(donor__user=user)
        return Sponsorship.objects.none()

    def perform_create(self, serializer):
        sponsorship = serializer.save()
        # Create notification for admin
        Notification.objects.create(
            user=User.objects.filter(user_type='admin').first(),
            message=f"New sponsorship request from {sponsorship.donor.user.username} for {sponsorship.child}"
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response(
                {"detail": "Only admins can approve sponsorships"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        sponsorship = self.get_object()
        sponsorship.status = 'active'
        sponsorship.save()
        
        # Create notification for donor
        Notification.objects.create(
            user=sponsorship.donor.user,
            message=f"Your sponsorship request for {sponsorship.child} has been approved"
        )
        
        return Response({"status": "active"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response(
                {"detail": "Only admins can reject sponsorships"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        sponsorship = self.get_object()
        sponsorship.status = 'cancelled'
        sponsorship.save()
        
        # Create notification for donor
        Notification.objects.create(
            user=sponsorship.donor.user,
            message=f"Your sponsorship request for {sponsorship.child} has been rejected"
        )
        
        return Response({"status": "cancelled"})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        if request.user.user_type != 'admin':
            return Response(
                {"detail": "Only admins can complete sponsorships"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        sponsorship = self.get_object()
        sponsorship.status = 'completed'
        sponsorship.end_date = timezone.now().date()
        sponsorship.save()
        
        # Create notification for donor
        Notification.objects.create(
            user=sponsorship.donor.user,
            message=f"Your sponsorship for {sponsorship.child} has been completed"
        )
        
        return Response({"status": "completed"}) 