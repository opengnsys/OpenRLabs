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

import concurrent.futures
import threading
from dummy import DummySingleton, Dummy
import dummy_module

class TestThreading(BaseTest):
    
        
        
    def do_singleton(self, var):
        print(threading.current_thread())
        ds = DummySingleton()
        ds.set_var(var)
        d = Dummy()
        d.set_var(var)
        dummy_module.set_var(var)
        
    def new_threads(self, var):
        print(threading.current_thread())
        if var == 1:
            vars = [3,4]
        else:
            vars = [5,6]
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            PCs_with_status =  list(executor.map(self.do_singleton, vars))

    
    def test_threads(self):
        vars = [1,2]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            PCs_with_status =  list(executor.map(self.new_threads, vars))
            
    def d_do_new_threads(self):
        print(threading.current_thread())
        threads = []
        for i in range(2,4):
            t = threading.Thread(target=self.do_singleton, args=(i,))
            threads.append(t)
            t.start()  
        
    def d_test_threads(self):
        threads = []
        for i in range(2):
            t = threading.Thread(target=self.do_new_threads)
            threads.append(t)
            t.start()  
        t.join()

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestThreading))
unittest.TextTestRunner(verbosity=2).run(suite)
