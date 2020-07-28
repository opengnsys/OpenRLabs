#!/usr/bin/python3
try: 
    import unittest2 as unittest #for Python <= 2.6
except:
    import unittest

import sys

def run_tests(dir):
    print('running tests')
    tests = unittest.defaultTestLoader.discover(dir)

    runner = unittest.TextTestRunner()
    runner.run(tests)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(" Directory test is needed, Run:")        
        print("  python runFunctionalTest.py FUNCTIONAL_TEST_DIRECTORY")
        exit()
    else:
        run_tests(sys.argv[1])
