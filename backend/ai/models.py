from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Anomaly)
def broadcast_high_severity_anomaly(sender, instance, created, **kwargs):
    if created and instance.severity == 'high':
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "anomalies",
            {
                "type": "anomaly.alert",
                "anomaly": {
                    "id": instance.id,
                    "child": str(instance.child) if instance.child else None,
                    "type": instance.anomaly_type,
                    "description": instance.description,
                    "severity": instance.severity,
                    "timestamp": instance.timestamp.isoformat(),
                }
            }
        ) 