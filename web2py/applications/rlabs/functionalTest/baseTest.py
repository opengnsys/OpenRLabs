#!/usr/bin/python
try: 
    import unittest2 as unittest #for Python <= 2.6
except:
    import unittest
    
import urllib2
import subprocess
import os.path
import os

from selenium import webdriver

URL_ROOT = 'http://127.0.0.1:8000'
#URL_APP = os.path.basename(os.getcwd())
#URL_ROOT = 'https://tkdgescamp.com'
URL_APP = 'alfambra2018'


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #self.web2py = start_web2py_server()
        self.browser = webdriver.Firefox()

    def setUp(self):
        # User enter email and passwd            
        self.doLogin()
        
    @classmethod    
    def tearDownClass(self):
        self.browser.close()
        #self.web2py.kill()
        os.system('pkill geckodriver') 
        

    def get_response_code(self, url):
        """Returns the response code of the given url

        url     the url to check for 
        return  the response code of the given url
        """
        handler = urllib2.urlopen(url)
        return handler.getcode()
    
    def doLogin(self):

        ## go to login web page
        self.browser.get(URL_ROOT + '/' + URL_APP + '/user/login')               
        
        #User is invited to enter  mail
        inputboxMail = self.browser.find_element_by_name('email')
        
        #User is invited to enter  passwdl        
        inputboxPasswd = self.browser.find_element_by_name('password')
                    
        #User write mail and passwd and pulse Enter on login buttom
        inputboxMail.send_keys('ramon@teruel.es')
        inputboxPasswd.send_keys('ramonB')
                
        ##WebDriverWait(self.browser, 20).until(expected_conditions.element_to_be_clickable((By.XPATH,  "//input[@type='submit']")));        
        self.browser.find_element_by_xpath("//input[@type='submit']").click()
        
def start_web2py_server():
    #noreload ensures single process
    
    print(os.path.curdir)
    
    return subprocess.Popen([
            'python', '../../web2py.py', 'runserver', '-a "passwd"', '-p 8001'
            
    ])
