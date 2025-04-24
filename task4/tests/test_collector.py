'''Data Collector Module'''
import unittest
import queue
import threading
from Adapter import BorgConnectNode, DataCollector
class TestDataCollector(unittest.TestCase):
    '''Class for data collector'''
    def test_collects_data(self):
        '''function collects data'''
        data_q = queue.Queue()
        node = BorgConnectNode()
        collector = DataCollector(node, data_q)
        def run_collector():
            '''funtion to run the collector module'''
            for _ in range(1):
                collector.collect("123456")
        thread = threading.Thread(target=run_collector, daemon=True)
        thread.start()
        collected = data_q.get(timeout=3)
        self.assertEqual(len(collected[1]), 6)
        self.assertEqual(collected[2], "123456")
        node.stop()
    if __name__ == '__main__':
        unittest.main()
