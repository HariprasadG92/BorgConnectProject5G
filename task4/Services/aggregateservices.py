import pika
import json
import redis
import time
from threading import Thread
from collections import defaultdict
import argparse

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class Sampler:
    def __init__(self, sampling_type, sampling_freq):
        self.sampling_type = sampling_type
        self.sampling_freq = sampling_freq
        self.data = defaultdict(list)

    def process(self, instance_id, value):
        self.data[instance_id].append(value)

    def sample_and_store(self):
        while True:
            time.sleep(self.sampling_freq)
            timestamp_now = int(time.time())

            for instance_id, values in self.data.items():
                if not values:
                    continue

                flat = [val for sublist in values for val in sublist]  # flatten

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

                # Store in Redis (value expires after 5 seconds)
                redis_data = {
                    "sampling_type": self.sampling_type,
                    "sampling_frequency": self.sampling_freq,
                    "value": result,
                    "timestamp": timestamp_now
                }
                redis_client.setex(instance_id, 5, json.dumps(redis_data))
                print(f"[REDIS] Stored for {instance_id}: {redis_data}")

            self.data.clear()


def callback(ch, method, properties, body):
    message = json.loads(body)
    instance_id = message["instance_id"]
    values = message["values"]
    sampler.process(instance_id, values)


def consume_from_rabbit():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='rawqueue')
    channel.basic_consume(queue='rawqueue', on_message_callback=callback, auto_ack=True)
    print("[RabbitMQ] Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate Sampling Service")
    parser.add_argument("--samplingtype", type=str, default="avg")
    parser.add_argument("--samplingfreq", type=int, default=5)
    args = parser.parse_args()

    sampler = Sampler(args.samplingtype, args.samplingfreq)

    Thread(target=sampler.sample_and_store, daemon=True).start()
    consume_from_rabbit()
