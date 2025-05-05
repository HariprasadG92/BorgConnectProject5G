import json
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis
import time

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'dashboard_updates'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
        # Send initial data if available
        self.send_initial_data()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_initial_data(self):
        # Get last 10 aggregated values from Redis
        aggregated_data = []
        for key in redis_client.keys('aggregated_*'):
            data = json.loads(redis_client.get(key))
            aggregated_data.append(data)
        
        # Sort by timestamp and get last 10
        aggregated_data.sort(key=lambda x: x['timestamp'])
        last_10 = aggregated_data[-10:]
        
        self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': last_10
        }))

    def dashboard_update(self, event):
        self.send(text_data=json.dumps(event['data']))