from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Enrollment, Child, ParentGuardian, AcademicRecord, MedicalRecord, BudgetRecord, LocationHistory, Tracking
from .serializers import (
    EnrollmentSerializer,
    EnrollmentDocumentSerializer,
    EnrollmentStatusUpdateSerializer,
    ChildSerializer,
    ParentGuardianSerializer,
    AcademicRecordSerializer,
    MedicalRecordSerializer,
    BudgetRecordSerializer,
    LocationHistorySerializer,
    TrackingSerializer
)
from core.models import User
from core.permissions import IsAdmin, IsAdminOrStaff, IsDonor, IsAdminOrStaffOrDonor
from django_filters import rest_framework as filters

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['status', 'enrollment_type', 'is_active']
    search_fields = ['child__first_name', 'child__last_name', 'enrollment_number']
    ordering_fields = ['enrollment_date', 'created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrStaff]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        enrollment = self.get_object()
        serializer = EnrollmentDocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            document = Document.objects.create(
                title=f"{enrollment.first_name} {enrollment.last_name} - {serializer.validated_data['document_type']}",
                document_type=serializer.validated_data['document_type'],
                file=serializer.validated_data['document'],
                description=serializer.validated_data.get('description', '')
            )
            enrollment.documents.add(document)
            return Response({'status': 'document uploaded'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        enrollment = self.get_object()
        serializer = EnrollmentStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            enrollment.status = serializer.validated_data['status']
            if serializer.validated_data.get('notes'):
                enrollment.notes = serializer.validated_data['notes']
            enrollment.save()
            
            # If approved, create a new Child record
            if enrollment.status == 'approved':
                child = Child.objects.create(
                    enrollment=enrollment,
                    first_name=enrollment.first_name,
                    last_name=enrollment.last_name,
                    date_of_birth=enrollment.date_of_birth,
                    gender=enrollment.gender,
                    photo=enrollment.photo,
                    date_joined=enrollment.created_at.date()
                )
                
                # Create parent/guardian record
                ParentGuardian.objects.create(
                    child=child,
                    first_name=enrollment.parent_guardian_name.split()[0],
                    last_name=' '.join(enrollment.parent_guardian_name.split()[1:]),
                    relationship=enrollment.parent_guardian_relationship,
                    phone_number=enrollment.parent_guardian_phone,
                    address=enrollment.parent_guardian_address
                )
                
                # Transfer documents
                for doc in enrollment.documents.all():
                    child.documents.add(doc)
            
            return Response({'status': 'status updated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        enrollment = self.get_object()
        return Response({
            'status': enrollment.status,
            'notes': enrollment.notes
        })

class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [IsAdminOrStaffOrDonor]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['status', 'gender', 'age', 'group', 'current_location', 'is_active']
    search_fields = ['first_name', 'last_name', 'nickname', 'unique_identifier']
    ordering_fields = ['first_name', 'last_name', 'age', 'created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'donor':
            # Donors can only see children they sponsor
            return Child.objects.filter(sponsorships__donor__user=user)
        elif user.user_type == 'staff':
            # Staff can see children they are assigned to
            return Child.objects.filter(staff_assignments__staff__user=user)
        return super().get_queryset()

    @action(detail=False, methods=['get'], url_path='report', permission_classes=[IsAdminOrStaffOrDonor])
    def report(self, request):
        user = request.user
        if user.user_type == 'admin':
            children = Child.objects.all()
        elif user.user_type == 'donor':
            children = Child.objects.filter(sponsorships__donor__user=user)
        else:
            children = Child.objects.none()
        data = ChildSerializer(children, many=True).data
        # You can add more aggregation or formatting here for printable/exportable reports
        return Response({'children': data})

class ParentGuardianViewSet(viewsets.ModelViewSet):
    queryset = ParentGuardian.objects.all()
    serializer_class = ParentGuardianSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['relationship_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'phone_number', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_at']

class AcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = AcademicRecord.objects.all()
    serializer_class = AcademicRecordSerializer
    permission_classes = [IsAdminOrStaffOrDonor]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['academic_level', 'is_active']
    search_fields = ['child__first_name', 'child__last_name', 'school_name']
    ordering_fields = ['academic_year', 'created_at']

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAdminOrStaff]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['record_type', 'is_active']
    search_fields = ['child__first_name', 'child__last_name', 'diagnosis']
    ordering_fields = ['record_date', 'created_at']

class BudgetRecordViewSet(viewsets.ModelViewSet):
    queryset = BudgetRecord.objects.all()
    serializer_class = BudgetRecordSerializer
    permission_classes = [IsAdminOrStaff]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['record_type', 'is_active']
    search_fields = ['child__first_name', 'child__last_name', 'description']
    ordering_fields = ['record_date', 'created_at']

class LocationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LocationHistory.objects.all()
    serializer_class = LocationHistorySerializer
    permission_classes = [IsAdminOrStaff]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['location', 'recorded_by']
    ordering_fields = ['created_at']

class TrackingViewSet(viewsets.ModelViewSet):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    permission_classes = [IsAdminOrStaff]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['status', 'child', 'reported_by', 'is_active']
    search_fields = ['child__first_name', 'child__last_name', 'notes']
    ordering_fields = ['last_seen', 'created_at']

    def get_permissions(self):
        user = self.request.user
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if user.user_type == 'admin':
                return [IsAdmin()]
            return [permissions.IsAdminUser()]
        return [IsAdminOrStaff()] 