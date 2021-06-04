from time import sleep

from baseTest import  BaseTest, URL_ROOT
from selenium.common.exceptions import NoSuchElementException

class TestReserveWorkFlow (BaseTest):

    def test_do_sucessfully_login(self):
        self.doLogin()     
        ## Double check
        # User is redirect to index page
        self.assertEqual(self.browser.current_url,  URL_ROOT + '/rlabs/show/ous')             
        
        # Index page don't containt link to login page
        try:
            hrefLogin = self.browser.find_element_by_xpath("//a[@href='/user/login']")
        except NoSuchElementException:
            hrefLogin = None
            
        self.assertEqual(hrefLogin,  None,  "Exits link element to Login page, Ergo login process don't work :-(")


    def test_show_ou(self):                
        self.assertIsNotNone(self.get_ou())

    
    def test_warning_ou_setup(self):        
        self.get_ou_not_setup().click()        
        alert = self.browser.switch_to.alert
        text_error = alert.text
        alert.accept()
        self.assertIn("Error de acceso", text_error)
    
    def test_show_labs(self):        
        self.get_ou().click()
        self.assertIsNotNone(self.get_lab())
        
    
    def __select_lab(self):
        self.get_ou().click()
        self.get_lab().click()
        sleep(2)
    
    def test_show_clients_and_button_reserve(self):
        self.__select_lab()
        self.assertIsNotNone(self.get_some_client())
        self.assertIsNotNone(self.get_button_reserve())        
    

