#!/usr/bin/python3
import ports_manager

from fileinput import filename



try: 
    import unittest2 as unittest #for Python <= 2.6
except:
    import unittest    

import os
import sys
sys.path.append(os.path.dirname(sys.argv[0]) + '/') #Path to my unitTest directory
from gluon import *

from baseTest import BaseTest

APP =sys.argv[1]



#This line executes your controller file, bringing all of the function declarations into the local namespace.
#execfile("applications/" + APP + "/controllers/default.py", globals())
filename = "applications/" + APP + "/controllers/connectPC.py"

exec(compile(open(filename, "rb").read(), filename, 'exec'), globals())




class PortManagerTest(BaseTest):
    
    def testGetPort(self):       
        port = None              
        port = ports_manager.get_origin_port('155.210.68.44', '10.7.1.112', '8080', '2')
        print(port)
        self.assertIsNotNone(port)
        

            
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(PortManagerTest))
unittest.TextTestRunner(verbosity=2).run(suite)
