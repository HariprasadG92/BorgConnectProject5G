"""This module collects the data or is known as the data collector."""

import time

class DataCollector:
    """Class for data collection from a node into a queue."""

    def __init__(self, node, data_queue):
        """Initialize the DataCollector with a node and a queue."""
        self.node = node
        self.data_queue = data_queue

    def collect(self, instance_id):
        """Collect data from the node and add it to the queue."""
        for values in self.node.get_data():
            timestamp = int(time.time())
            self.data_queue.put((timestamp, values, instance_id))
            print(f"[{timestamp}] Instance{instance_id}->{values}")
