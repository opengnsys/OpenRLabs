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
filename = "applications/" + APP + "/controllers/default.py"

exec(compile(open(filename, "rb").read(), filename, 'exec'), globals())

from gluon.storage import Storage

import ognsys
from lab import Lab
from client_lab import Client
import ou

class OgActions(BaseTest):
    
    def d_test_diskcfg(self):
        opengnsys.init(db, "4")
        lab = Lab("4" , "17")
        response = lab.getDiskConfigClient(194)
        
        self.assertIsNot(len(response), 0)
    
    def d_test_get_status_cient(self):
        opengnsys.init(db, "4")
        lab = Lab("4" , "17")
        response = lab.getStatusClient({ 'ip' : '10.7.1.96'})
        
        self.assertIsNot(len(response), 0)
        
    def test_get_credentials(self):
        opengnsys = ognsys.Ognsys(db)
        r = opengnsys.set_apikey(4)

        self.assertIsNot(r, False)

    def test_get_labs(self):
        opengnsys = ognsys.Ognsys(db)
        opengnsys.set_apikey(4)        
        labs = ou.get_labs_on(4)
        
        self.assertIsNot(len(labs), 0)

    def test_get_clients(self):
        opengnsys = ognsys.Ognsys(db)
        opengnsys.set_apikey(4)
        lab = Lab("4" , "17")
        clients = lab.get_remote_clients()
        print(clients)
        self.assertIsNot(len(clients), 0)
        
    def test_reserve_client(self):
        opengnsys = ognsys.Ognsys(db)
        opengnsys.set_apikey(4)
        
        my_context = Storage({"ou_id" : 4, "lab_id" : 17, "image_id": 16, "maxtime" : 2})
  
        client = Client(my_context)
        equipo_reservado = client.reserve_remote_pc()
        print(equipo_reservado)
        
        r = client.redirect_events()
        print(r)
        t = client.register_session_timeout()
        print(t)
        
        self.assertIsNot(equipo_reservado, "")
        
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(OgActions))
unittest.TextTestRunner(verbosity=2).run(suite)
