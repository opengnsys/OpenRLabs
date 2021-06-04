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

class TestRegisterSessionParams(BaseTest):
    
    def testRegisterSessionParams(self):
        
        ou_id = '2' #eupt
        lab_id = '6' #informatica1
        image_id = '14' #Windows 10
        pc_id = '36' # eupti115
        maxtime = "1"
                    
        login_info = opengnsys.doLogin()
        opengnsys.setApiKey(login_info['apikey'])      
        
        resultado = opengnsys.register_session_parameters(ou_id, lab_id, pc_id, maxtime)
        print(resultado)
        
        self.assertIsNotNone(resultado)
        


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestRegisterSessionParams))
unittest.TextTestRunner(verbosity=2).run(suite)
