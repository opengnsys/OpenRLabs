#!/usr/bin/python3

# BaseTest  containt all commons tasks and variables 
try: 
    import unittest2 as unittest #for Python <= 2.6
except:
    import unittest
'''
from gluon.globals import Request
from gluon.globals import Storage
'''

class BaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        pass

        
    def setUp(self):                
        pass
        #self.request = Request(Storage())  # Use a clean Request object
