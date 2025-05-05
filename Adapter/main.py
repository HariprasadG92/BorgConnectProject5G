"""This is the main function."""
import argparse
import queue
import threading
import json
import time
import redis
from borgConnectNode import BorgConnectNode
from data_collector import DataCollector
from store_data import DataStorage


def run(instance_id):
    """Creating objects for all the functions."""
    data_queue = queue.Queue()
    node = BorgConnectNode()
    collector = DataCollector(node, data_queue)
    storage = DataStorage()
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def collector_thread():
        """Getting instance id and collecting data."""
        while True:
            settings = redis_client.get('dashboard_settings')
            if settings:
                settings = json.loads(settings)
                if settings.get('status') == 'running':
                    collector.collect(instance_id)
                else:
                    time.sleep(1)
            else:
                time.sleep(1)

    def storage_thread():
        """Collecting timestamp, values, instance_id."""
        while True:
            timestamp, values, inst_id = data_queue.get()
            storage.store(timestamp, values, inst_id)

    t1 = threading.Thread(target=collector_thread)
    t2 = threading.Thread(target=storage_thread, daemon=True)
    t1.start()
    t2.start()
    t1.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Data Adapter Simulation")
    parser.add_argument("--borg-connect-node", type=str, help="Instance ID")
    args = parser.parse_args()
    if args.borg_connect_node:
        run(args.borg_connect_node)
    else:
        print("Please provide instance ID using --borg-connect-node")
