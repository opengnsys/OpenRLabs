#!/usr/bin/python3

import subprocess
import os
import sys
import glob

APP = os.path.basename(os.getcwd())

def start_unittests(dir):        
    TEST_DIR = dir
    err = ''
    
    testFileList = glob.glob(os.getcwd() + '/' + TEST_DIR + '/test*.py')
    # Execute all test in directory
    for testFile in testFileList:
        # Framework web2py launch test script. It sets up the operating environment,
        # brings in our database and gives us all of the variables that are normally passed into the controller.
        command_str = os.getcwd().split('applications')[0] + 'web2py.py' + ' -S ' + APP + ' -M -R '+ os.getcwd() + \
                                                '/' + TEST_DIR + '/' + os.path.basename(testFile) + \
                                                ' -A ' + APP
                                                                
        subprocess.run('python3 ' + command_str, shell=True)
            
        
        
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(" Directory test is needed, Run:")        
        print("  python runUnitTest.py UNITTEST_DIRECTORY")
        exit()
    else:
        start_unittests(sys.argv[1])
