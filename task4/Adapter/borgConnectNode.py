'''This the the Borg Connect Node data simulator'''
import random
import time
class BorgConnectNode:
    '''Node Class''' 
    def __init__(self):
        '''Constructor'''
        self.running = True
    def get_data(self):
        '''Function to pump the data'''
        while self.running:
            yield[random.randint(0, 100) for _ in range(6)]
            time.sleep(1)
    def stop(self):
        '''function stop node'''
        self.running=False
