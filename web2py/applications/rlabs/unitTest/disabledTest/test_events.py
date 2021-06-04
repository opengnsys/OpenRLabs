#!/usr/bin/python3
import clients
import opengnsys

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




class EventsTest(BaseTest):
    
    def testLoginEvent(self):                     
        opengnsys.setServers(db)
        opengnsys.setApiKey(opengnsys.doLogin(db, '2')['apikey'])

        parametros_sesion_registrados = clients.register_session_parameters('2', '2', '6', '2')
        
        print(parametros_sesion_registrados)                        
        
        #self.assertRegex(message['output'], "Sending")
        self.assertIsNotNone(parametros_sesion_registrados)
        
    def testLogoutEvent(self):                     
        opengnsys.setServers(db)
        opengnsys.setApiKey(opengnsys.doLogin(db, '2')['apikey'])

        resultad0 = clients.unreserveRemotePC('2', '2', '6')
        
        print(resultad0)                        
        
        #self.assertRegex(message['output'], "Sending")
        self.assertIsNotNone(resultad0)
        

            
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(EventsTest))
unittest.TextTestRunner(verbosity=2).run(suite)
