from .models import Child, ChildAIProfile, Tracking, WearableDevice
from .serializers import ChildAIProfileSerializer, WearableDeviceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from core.utils import check_for_escaped_children
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def child_risk_score(request, child_id):
    try:
        profile = ChildAIProfile.objects.get(child_id=child_id)
    except ChildAIProfile.DoesNotExist:
        return Response({'detail': 'AI profile not found.'}, status=404)
    serializer = ChildAIProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def simulate_location_update(request, child_id):
    """Simulate a location update for a child and trigger escape detection."""
    lat = request.data.get('lat')
    lon = request.data.get('lon')
    if not lat or not lon:
        return Response({'detail': 'lat and lon required.'}, status=400)
    try:
        tracking = Tracking.objects.get(child_id=child_id)
    except Tracking.DoesNotExist:
        return Response({'detail': 'Tracking record not found.'}, status=404)
    tracking.last_known_location = f"{lat},{lon}"
    tracking.save()
    # Run escape detection for this child
    check_for_escaped_children()
    return Response({'detail': 'Location updated and escape detection triggered.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def dashboard_child_locations(request):
    from .models import Child, Tracking, ChildAIProfile
    children = Child.objects.all()
    data = []
    for child in children:
        tracking = getattr(child, 'tracking_records', None)
        tracking = tracking.last() if hasattr(tracking, 'last') else None
        ai_profile = getattr(child, 'ai_profile', None)
        data.append({
            'id': child.id,
            'name': f"{child.first_name} {child.last_name}",
            'status': tracking.status if tracking else None,
            'last_known_location': tracking.last_known_location if tracking else None,
            'last_update': tracking.last_update if tracking else None,
            'risk_score': ai_profile.escape_risk_score if ai_profile else None,
        })
    return Response(data)

@api_view(['POST'])
def wearable_location_update(request):
    """Endpoint for wearable devices to update child location. Auth via device_id."""
    device_id = request.data.get('device_id')
    lat = request.data.get('lat')
    lon = request.data.get('lon')
    if not device_id or not lat or not lon:
        return Response({'detail': 'device_id, lat, and lon required.'}, status=400)
    try:
        device = WearableDevice.objects.get(device_id=device_id, is_active=True)
        tracking = device.child.tracking_records.last()
        if not tracking:
            return Response({'detail': 'Tracking record not found for child.'}, status=404)
        tracking.last_known_location = f"{lat},{lon}"
        tracking.save()
        device.last_seen = timezone.now()
        device.save()
        check_for_escaped_children()
        return Response({'detail': 'Location updated and escape detection triggered.'})
    except WearableDevice.DoesNotExist:
        return Response({'detail': 'Device not found or inactive.'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_wearable_devices(request):
    devices = WearableDevice.objects.all()
    serializer = WearableDeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_wearable_device(request):
    serializer = WearableDeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def set_wearable_device_active(request, device_id):
    try:
        device = WearableDevice.objects.get(id=device_id)
    except WearableDevice.DoesNotExist:
        return Response({'detail': 'Device not found.'}, status=404)
    is_active = request.data.get('is_active')
    if is_active is not None:
        device.is_active = bool(is_active)
        device.save()
        return Response({'detail': 'Device status updated.'})
    return Response({'detail': 'is_active required.'}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_wearable_device(request, device_id):
    try:
        device = WearableDevice.objects.get(id=device_id)
        device.delete()
        return Response({'detail': 'Device deleted.'})
    except WearableDevice.DoesNotExist:
        return Response({'detail': 'Device not found.'}, status=404) 