"""This module is to store the data."""

import sqlite3
import json


class DataStorage:
    """Class created for data storage."""

    def __init__(self, db_name="database.db"):
        """Constructor creating the DB model."""
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Function to create table."""
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS data(
                timestamp INTEGER,
                data_values TEXT,
                instance_id TEXT
            )'''
        )
        self.conn.commit()

    def store(self, timestamp, values, instance_id):
        """Function to store the data timestamp, values, instance_id."""
        self.cursor.execute(
            'INSERT INTO data(timestamp, data_values, instance_id) VALUES (?, ?, ?)',
            (timestamp, json.dumps(values), instance_id)
        )
        self.conn.commit()
