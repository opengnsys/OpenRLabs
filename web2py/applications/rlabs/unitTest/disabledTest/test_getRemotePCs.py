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

class TestGetRemotePCs(BaseTest):
    
    def testGetRemotePCs(self):
        
        ou_id = '2' #eupt
        lab_id = '6' #informatica1
                    
        login_info = opengnsys.doLogin()
        opengnsys.setApiKey(login_info['apikey'])        
        
        remotePCs = opengnsys.getRemotePCs(ou_id, lab_id)
        
        pci115 = None
        for pc in remotePCs:        
            if pc['pc']['id'] == 36:
                pci115 = pc            
                
        self.assertIsNotNone(pci115['status'])

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGetRemotePCs))
unittest.TextTestRunner(verbosity=2).run(suite)
