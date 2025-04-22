'''unit test storage module'''
import unittest
import os
import sqlite3
import json
import time
from Adapter import DataStorage
class TestDataStorage(unittest.TestCase):
    '''Class test data storage'''
    def setUp(self):
        '''setting up the database'''
        self.db_name = "test_db.sqlite"
        self.storage = DataStorage(db_name=self.db_name)
    def tearDown(self):
        '''Closing the connection in data storage is exists'''
        if hasattr(self.storage, 'conn') and self.storage.conn:
            self.storage.conn.close()
        if os.path.exists(self.db_name):
            try:
                os.remove(self.db_name)
            except PermissionError:
                print(f"Could not delete {self.db_name} - still in use.")
    def test_store_and_retrieve(self):
        '''Function to tests storing data and retrieve data'''
        ts = int(time.time())
        values = [10, 20, 30, 40, 50, 60]
        iid = "654321"
        self.storage.store(ts, values, iid)
        cursor = self.storage.conn.cursor()
        cursor.execute('''SELECT timestamp, data_values, instance_id
                       FROM data ORDER BY rowid DESC LIMIT 1''')
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No row was returned from the database.")
        self.assertEqual(row[0], ts)
        self.assertEqual(json.loads(row[1]), values)
        self.assertEqual(row[2], iid)
if __name__ == '__main__':
    unittest.main()
