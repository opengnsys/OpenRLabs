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

#import global_context
#import adoDB_active_reserves
from gluon.storage import Storage

class GlobalContext(BaseTest):
    
    def test_context(self):
        my_context = Storage({'a' :1, 'b' : 2})
        
        my_dict = {'c' :3, 'd' : 4}
        for k,v in my_dict.items():
            my_context[k] = v

        my_dict = {'e' :5, 'f' : 6}
        for k,v in my_dict.items():
            my_context[k] = v
            
        print(my_context)
        print(my_context['b'])
        print(my_context['d'])
        print(my_context['f'])
        self.assertIsNot(len(my_context), 0)

           
    '''    
    def test_context(self):
        
        global_context.add_context(db = db, user_id = "pepe")

        context = global_context.get_context() 
        print('context')
        print(context)        

        if 'user_id' in context:
            user_id = context['user_id']
        else: 
            user_id = ''
             
  
        
        global_context.add_context(new_context = "new context")
        
        context = global_context.get_context() 
        print('new context')
        print(context)

        kk = {}
        kk['kk'] =  'kk' 
        kk['kk2'] = 'kk2'
        print(kk)      
        global_context.add_context(**kk)

        print(global_context.get_context() )
        global_context.add_context(new_context = "new context_repeated")
        
        context = global_context.get_context() 
        print('new context')
        print(context)

        objs = global_context.get_context('user_id', 'new_context') 
        print('objects')
        print(objs)
        
        print(global_context.get_context() )
        
        if 'new_context' in context:
            new_context = context['new_context']
        else: 
            new_context = ''
             
        self.assertIsNot(new_context, '')
        self.assertIsNot(user_id, '')
        
    def test_insert_reserve(self):
        global_context.add_context(port = '3389',
                                   lab_id = '17',
                                   image_id = '16', 
                                   ou_id = '4', 
                                   protocol = 'rdp',
                                   user_id = 11,
                                   id = 210, 
                                   name = 'eupti117',
                                   ip = '10.7.1.112',
                                   expiration_time = '08/04/2020 13:20:26')
                                   
        global_context.add_context(db = db)
        adoDB_active_reserves.insert(global_context)
    '''
    
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(GlobalContext))
unittest.TextTestRunner(verbosity=2).run(suite)
