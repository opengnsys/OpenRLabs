#!/usr/bin/python3
try: 
    import unittest2 as unittest #for Python <= 2.6
except:
    import unittest
    
import urllib3
import subprocess
import os.path
import os

from selenium import webdriver

URL_ROOT = 'http://127.0.0.1:8000'
#URL_APP = os.path.basename(os.getcwd())
#URL_ROOT = 'https://tkdgescamp.com'
URL_APP = 'rlabs'


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #self.web2py = start_web2py_server()
        print("set driver")
        self.browser = webdriver.Firefox()
        print('setting driver ok')        
        self.ou_not_setup = "2"
        self.ou = "4"
        self.lab = "19"
        self.time_to_wait = 100
        


    


    def setUp(self):
        # User enter email and passwd                    
        pass        
        
    @classmethod    
    def tearDownClass(self):
        self.browser.quit()
        #self.web2py.kill()
        os.system('pkill geckodriver') 
        

    def get_response_code(self, url):
        """Returns the response code of the given url

        url     the url to check for 
        return  the response code of the given url
        """
        handler = urllib3.urlopen(url)
        return handler.getcode()
    
    def doLogin(self):
        print(URL_ROOT + '/' + URL_APP)
        ## go to login web page
        self.browser.get(URL_ROOT + '/' + URL_APP)
        
        #User is invited to enter  mail
        inputboxMail = self.browser.find_element_by_name('username')
        
        #User is invited to enter  passwdl        
        inputboxPasswd = self.browser.find_element_by_name('password')
                    
        #User write mail and passwd and pulse Enter on login buttom
        inputboxMail.send_keys('admin')
        inputboxPasswd.send_keys('admin')
                        
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

    def get_ou(self):
        return self.browser.find_element_by_xpath("//span[@data-ou='" + self.ou + "']")

    def get_ou_not_setup(self):
        return self.browser.find_element_by_xpath("//span[@data-ou='" + self.ou_not_setup + "']")
    
    def get_lab(self):
        return self.browser.find_element_by_xpath("//span[@data-lab_id='" + self.lab + "']")

    def get_some_client(self):
        return self.browser.find_element_by_xpath("//tr[@class='pc']")

    def get_button_reserve(self):
        return self.browser.find_element_by_xpath("//button[@data-ou_id='" + self.ou + "' and @data-lab_id='" + self.lab + "']")

    def get_button_select_broser(self):
        return self.browser.find_element_by_xpath("//button[@data-client='browser']")

    def get_console_log(self):
        return self.browser.find_element_by_xpath("//textarea[@id='text_consolelog']")
    
    def get_button_connect(self):
        return self.browser.find_element_by_xpath("//button[contains(text(),'Conectar')]")

    def get_img_status_ready(self):
        try:
            return self.browser.find_element_by_xpath("//img[@data-status!='busy']")
        except:
            return None
    
    def get_canvas(self):
        return self.browser.find_element_by_xpath("//canvas")

def start_web2py_server():
    #noreload ensures single process
    
    print(os.path.curdir)
    
    return subprocess.Popen([
            'python', '../../web2py.py', 'runserver', '-a "passwd"', '-p 8001'
            
    ])
