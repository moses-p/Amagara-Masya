from django.db import models
from children.models import Tracking
from core.models import Notification, User, AuditLog
from django.core.mail import send_mail
import os
try:
    from pyfcm import FCMNotification
except ImportError:
    FCMNotification = None

FCM_API_KEY = os.environ.get('FCM_API_KEY')

def log_audit_action(user, action, model_name, details=None, request=None):
    """
    Log an audit action performed by a user.
    
    :param user: The user performing the action.
    :param action: The action being performed.
    :param model_name: The name of the model being acted upon.
    :param details: Additional details about the action.
    """
    ip = request.META.get('REMOTE_ADDR') if request else None
    user_agent = request.META.get('HTTP_USER_AGENT') if request else None
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        details=str(details) if details else None,
        ip_address=ip,
        user_agent=user_agent
    )
    print(f"Audit: User {user} performed {action} on {model_name} with details: {details}")

def send_push_notification(user, message, subject=None):
    # Integrate with FCM if available
    if FCM_API_KEY and FCMNotification:
        push_service = FCMNotification(api_key=FCM_API_KEY)
        tokens = [device.device_token for device in user.devices.all()]
        if tokens:
            push_service.notify_multiple_devices(
                registration_ids=tokens,
                message_title=subject or 'Notification',
                message_body=message
            )
    else:
        for device in user.devices.all():
            print(f"Push to {device.device_token}: {subject or ''} {message}")
    # Implement actual push logic here

def send_notification(user, message, subject=None, push=False):
    # In-app notification
    Notification.objects.create(user=user, message=message)
    # Email notification
    if user.email:
        send_mail(
            subject=subject or 'Notification',
            message=message,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True
        )
    # Push notification
    if push:
        send_push_notification(user, message, subject)
    # Placeholder for SMS/push integration
    # e.g., send_sms(user.phone_number, message)
    # e.g., send_push(user, message)

def check_for_escaped_children(safe_zone=None):
    # Placeholder: safe_zone can be a geofence or coordinates
    for tracking in Tracking.objects.filter(status='in_center'):
        if tracking.is_outside_safe_zone(safe_zone):
            tracking.status = 'escaped'
            tracking.save()
            admins = User.objects.filter(user_type='admin')
            for admin in admins:
                send_notification(
                    user=admin,
                    message=f"Child {tracking.child} has left the center! Please take immediate action.",
                    subject='URGENT: Child Escaped from Center',
                    push=True
                ) 