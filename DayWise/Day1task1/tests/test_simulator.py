'''Test Unit - Simulator'''
import unittest
from Adapter import BorgConnectNode
class TestBorgConnect(unittest.TestCase):
    '''UnitTest class for borg connect module'''
    def test_get_data(self):
        '''function to pump data'''
        node = BorgConnectNode()
        generator =node.get_data()
        data = next(generator)
        self.assertEqual(len(data), 6)
        self.assertTrue(all(isinstance(x, int) for x in data))
        node.stop()
    if __name__ == '__main__':
        unittest.main()
