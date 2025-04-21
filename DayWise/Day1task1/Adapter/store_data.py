'''This module is to store the data'''
import sqlite3
import json
class DataStorage:
    '''Class Created to data storage'''
    def __init__(self, db_name="database.db"):
        '''Constructor creating the db model'''
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
    def create_table(self):
        '''Function to create table'''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data(
            timestamp INTEGERS,
            data_values  TEXT,
            instance_id TEXT
            )''')
        self.conn.commit()
    def store(self ,timestamp,values, instance_id):
        '''Funciton to store the data timestamp, values, instance_id'''
        self.cursor.execute(
            'INSERT INTO data(timestamp, data_values, instance_id) VALUES (?, ?, ?)',
            (timestamp, json.dumps(values), instance_id)
            )
        self.conn.commit()
