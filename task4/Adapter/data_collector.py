import pika
import json
import time

class DataCollector:
    def __init__(self, node, data_queue):
        self.node = node
        self.data_queue = data_queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rawqueue')

    def collect(self, instance_id):
        for values in self.node.get_data():
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
            print(f"[{timestamp}] Sent to RabbitMQ: {data}")
