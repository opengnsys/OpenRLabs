from time import sleep

from baseTest import  BaseTest, URL_ROOT
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec


class TestDoUnReserve (BaseTest):
        
    def test_do_unreserve(self):
        self.doLogin()
        self.get_button_cancel().click()
        #sleep(2)
        #self.assertIsNone(self.get_button_cancel())


    






