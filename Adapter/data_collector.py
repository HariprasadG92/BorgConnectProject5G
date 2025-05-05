"""Data collector for Borg Connect Node."""

import json
import time
import pika
import redis


class DataCollector:
    """Collects data from a node and sends it to RabbitMQ."""

    def __init__(self, node, data_queue):
        """Initialize the data collector."""
        self.node = node
        self.data_queue = data_queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rawqueue')
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def collect(self, instance_id):
        """Collect and publish data until status is not 'running'."""
        for values in self.node.get_data():
            settings = self.redis_client.get('dashboard_settings')
            if settings:
                settings = json.loads(settings)
                if settings.get('status') != 'running':
                    break

            timestamp = int(time.time())
            data = {
                "timestamp": timestamp,
                "values": values,
                "instance_id": instance_id
            }
            self.channel.basic_publish(
                exchange='',
                routing_key='rawqueue',
                body=json.dumps(data)
            )
            self.data_queue.put((timestamp, values, instance_id))
            print(f"[{timestamp}] Sent to RabbitMQ: {data}")
