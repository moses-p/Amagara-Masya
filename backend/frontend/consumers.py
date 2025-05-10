import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AnomalyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("anomalies", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("anomalies", self.channel_name)

    async def anomaly_alert(self, event):
        await self.send(text_data=json.dumps(event["anomaly"])) 