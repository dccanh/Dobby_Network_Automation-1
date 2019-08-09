import sys
sys.path.append('../')
import unittest
import configparser
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import HTMLTestRunner
import Helper.Helper_common


config = configparser.ConfigParser()
config.read_file(open(r'../Config/ifconfig.txt'))
ipv4 = 'http://' + config.get('IFCONFIG', 'ipv4')
ipv6 = 'http://[' + config.get('IFCONFIG', 'ipv6') + ']'
user = config.get('USER_INFO', 'user')
pass_word = config.get('USER_INFO', 'pw')

config.read_file(open(r'../Config/config.txt'))
url = config.get('URL', 'url')


class UI_LG_01(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()

    def test_login_ipv4(self):
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        driver.get(ipv4)
        time.sleep(3)
        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(3)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        self.assertEqual(driver.current_url, expected_quick_setup, '[UI_LG_01] URL page quick setup return wrong')

    def tearDown(self):
        end_time = datetime.datetime.now()
        print('Duration: ' + str((end_time - self.start_time)))
        self.driver.quit()


class UI_LG_02(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()

    def test_login_ipv6(self):
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        driver.get(ipv6)
        time.sleep(3)
        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(3)
        expected_quick_setup = ipv6 + '/#page-quick-setup'
        self.assertEqual(driver.current_url, expected_quick_setup, '[UI_LG_02] URL page quick setup return wrong')

    def tearDown(self):
        end_time = datetime.datetime.now()
        print('Duration: ' + str((end_time - self.start_time)))
        self.driver.quit()


class UI_QS_01(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()

    def test_change_2g_pw(self):
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        driver.get(ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        self.assertEqual(driver.current_url, expected_quick_setup, '[UI_QS_01] URL page quick setup return wrong')

        # Click to 2.4 GHZ
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(3)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = "Chrome123!@#^&*()"

        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(3)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
        confirm_pw = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        time.sleep(3)
        actual_password = driver.find_element_by_css_selector('[id="2g-network-password"] strong').text
        self.assertEqual(actual_password, keys_send, '[UI_QS_01] Change password fail')

    def tearDown(self):
        end_time = datetime.datetime.now()
        print('Duration: ' + str((end_time - self.start_time)))
        self.driver.quit()


class UI_SS_01(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()

    def test_status_sortware_version(self):
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        driver.get(ipv4 + '/#page-login')
        time.sleep(5)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        self.assertEqual(driver.current_url, expected_quick_setup, '[UI_SS_01] URL page quick setup get wrong')

        config_advance = driver.find_element_by_css_selector('a.next.config[href="#page-status-software"]')
        ActionChains(driver).move_to_element(config_advance).click().perform()
        expected_status_software = ipv4 + '/#page-status-software'
        self.assertEqual(driver.current_url, expected_status_software, '[UI_SS_01] URL page Status software get wrong')
        time.sleep(3)
        version_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(2) >li:nth-child(2)')
        ActionChains(driver).move_to_element(version_actual).perform()
        version_actual = version_actual.text.splitlines()[-1]

        json_api = Helper.Helper_common.gateway_about()
        version_expected = json_api['hardware']['version']
        self.assertEqual(version_actual, version_expected,
                         '[UI_SS_01] Hardware version did not display match between WebUI and API')

    def tearDown(self):
        end_time = datetime.datetime.now()
        print('Duration: ' + str((end_time - self.start_time)))
        self.driver.quit()


if __name__ == '__main__':
    HTMLTestRunner.main()