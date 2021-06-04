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

import requests
requests.packages.urllib3.disable_warnings()
import json

class Request(BaseTest):
    
    def test_request(self):
        recurso = "https://10.7.1.109:8000/opengnsys/status"
        __APIKEY__ = "82261ccd9c46192ce7883f6e79d52493"
        timeout = 0.05
        allow_redirects = False

        r = requests.get(recurso,headers={'Accept': 'application/json',
                                         'Authorization': __APIKEY__}, verify=False,
                            timeout=timeout, 
                            allow_redirects=allow_redirects)
                  
        print(r.text)
        self.assertIsNot(len(r.json()), 0)

           

    
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(Request))
unittest.TextTestRunner(verbosity=2).run(suite)
