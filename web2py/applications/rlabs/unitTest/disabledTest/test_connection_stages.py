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




class ConnectionStageTest(BaseTest):
    
    def testGetStatus(self):                     
        opengnsys.setServers(db)
        opengnsys.setApiKey(opengnsys.doLogin(db, '2')['apikey'])
                        
        status = clients.check_pc_status('2', '2', '6', numRetries = 6)
        
        print(status)                        
        
        #self.assertRegex(message['output'], "Sending")
        self.assertIsNotNone(status)        
        
    def testRedirectEvents(self):
        opengnsys.setServers(db)
        opengnsys.setApiKey(opengnsys.doLogin(db, '2')['apikey'])

        redirect = clients.redirect_events('2', '2', '6', '2')
        print(redirect)
        self.assertIsNotNone(redirect)

            
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(ConnectionStageTest))
unittest.TextTestRunner(verbosity=2).run(suite)
