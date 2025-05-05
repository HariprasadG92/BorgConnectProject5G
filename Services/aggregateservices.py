"""Sampler module for aggregating and storing data using Redis and RabbitMQ."""

import json
import time
import pika
import redis
from threading import Thread
from collections import defaultdict

# Redis client
REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0)


class Sampler:
    """Handles data aggregation and storage."""

    def __init__(self):
        self.data = defaultdict(list)
        self.running = False
        self.sampling_type = 'avg'
        self.sampling_freq = 5

    def update_settings(self):
        """Fetches and updates sampler settings from Redis."""
        settings = REDIS_CLIENT.get('dashboard_settings')
        if settings:
            settings = json.loads(settings)
            self.sampling_type = settings.get('sampling_type', 'avg')
            self.sampling_freq = settings.get('sampling_freq', 5)
            self.running = settings.get('status', 'stopped') == 'running'

    def process(self, instance_id, value):
        """Appends value to instance data if sampling is running."""
        if self.running:
            self.data[instance_id].append(value)

    def sample_and_store(self):
        """Performs sampling and stores the result in Redis and RabbitMQ."""
        while True:
            self.update_settings()

            if self.running and self.data:
                time.sleep(self.sampling_freq)
                timestamp_now = int(time.time())

                for instance_id, values in self.data.items():
                    if not values:
                        continue

                    flat = [val for sublist in values for val in sublist]

                    if self.sampling_type == 'sum':
                        result = sum(flat)
                    elif self.sampling_type == 'avg':
                        result = sum(flat) / len(flat)
                    elif self.sampling_type == 'min':
                        result = min(flat)
                    elif self.sampling_type == 'max':
                        result = max(flat)
                    elif self.sampling_type == 'latest':
                        result = flat[-1]
                    else:
                        result = None

                    redis_key = f'aggregated_{instance_id}_{timestamp_now}'
                    redis_data = {
                        "sampling_type": self.sampling_type,
                        "sampling_frequency": self.sampling_freq,
                        "value": result,
                        "timestamp": timestamp_now,
                        "instance_id": instance_id
                    }

                    REDIS_CLIENT.setex(redis_key, 3600, json.dumps(redis_data))

                    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                    channel = connection.channel()
                    channel.queue_declare(queue='aggregated_queue')
                    channel.basic_publish(
                        exchange='',
                        routing_key='aggregated_queue',
                        body=json.dumps(redis_data)
                    )
                    connection.close()

                    print(f"[REDIS] Stored aggregated data: {redis_data}")

                self.data.clear()
            else:
                time.sleep(1)


def callback(ch, method, properties, body):
    """Callback for consuming messages from RabbitMQ."""
    message = json.loads(body)
    instance_id = message["instance_id"]
    values = message["values"]
    SAMPLER.process(instance_id, values)


def consume_from_rabbit():
    """Consumes raw data from RabbitMQ and processes it."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='rawqueue')
    channel.basic_consume(queue='rawqueue', on_message_callback=callback, auto_ack=True)
    print("[RabbitMQ] Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    SAMPLER = Sampler()
    Thread(target=SAMPLER.sample_and_store, daemon=True).start()
    consume_from_rabbit()
