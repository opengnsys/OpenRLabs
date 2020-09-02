#!/usr/bin/python3
import opengnsys
import labs
import clients


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




class ShowClientsTest(BaseTest):
    
        
        
    def testSetServers(self):
        
        opengnsys.setServers(db)
        
        print(opengnsys.__OPENGNSYS_SERVER__)
        print(opengnsys.__RLABS_SERVER__)
        
        self.assertIsNot(opengnsys.__OPENGNSYS_SERVER__, '')
        self.assertIsNot(opengnsys.__RLABS_SERVER__, '')
        
        
    def testDoLogin(self):
        
        opengnsys.setServers(db)

        respuesta = opengnsys.doLogin(db, '2')
        print(respuesta)
        
        self.assertIsNot(respuesta, '')
        
    def testGetLabs(self):
        
        opengnsys.setServers(db)        
        opengnsys.setApiKey(opengnsys.doLogin(db, '2')['apikey'])
                
        laboratorios = labs.getLABS('2')
        
        
        labsON =  labs.getLabsOn(laboratorios)
        
        print(labsON)                   
        
        
        self.assertIsNot(laboratorios, '')
            
                
    def testGetReomtePCs(self):
        opengnsys.setServers(db)        
        opengnsys.setApiKey(opengnsys.doLogin(db, '2')['apikey'])
                        
        remoteClients = clients.getRemoteClients('2', '2')        
        
    
        self.assertIsNot(remoteClients, '')
    
        
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(ShowClientsTest))
unittest.TextTestRunner(verbosity=2).run(suite)
