from time import sleep

from baseTest import  BaseTest, URL_ROOT
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



class TestDoReserveConnectUnreserve (BaseTest):
    
    
    def __select_lab(self):
        self.get_ou().click()
        self.get_lab().click()
        sleep(2)                

    def test_do_reserve_connect_unreserve(self):
        self.doLogin()
        
        self.__select_lab()
        self.get_button_reserve().click()
        self.get_button_select_broser().click()
        sleep(5)
        self.assertIn("Equipo concedido", self.get_console_log().get_attribute("value"))

        WebDriverWait(self.browser, 100).until(ec.invisibility_of_element_located((By.ID, 'text_consolelog')))

        sleep(1)        
        self.get_button_connect().click()
        sleep(4)
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.assertIsNotNone(self.get_canvas())

        sleep(2)
        self.browser.switch_to.window(self.browser.window_handles[0])
        button_used = self.get_button_cancel()
        button_used.click()
        sleep(2)
        try:
            button_used.click()
            not_found = False
        except:
            not_found = True            
        self.assertTrue(not_found)        



    






