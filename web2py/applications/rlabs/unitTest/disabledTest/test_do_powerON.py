#!/usr/bin/python3
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

import opengnsys

class TestDoPowerON(BaseTest):
    
    def testDoPowerON(self):
        
        mac = 'a0481c91296c'     
                
        message = opengnsys.do_poweron(mac)
        
        self.assertRegex(message['output'], "Sending")
        


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDoPowerON))
unittest.TextTestRunner(verbosity=2).run(suite)
