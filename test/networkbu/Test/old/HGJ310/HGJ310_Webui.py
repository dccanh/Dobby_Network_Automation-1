import sys, os
sys.path.append('../')
import unittest
import configparser
import time
import datetime
import subprocess
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import HTMLTestRunner
import Helper.Helper_common
import re
import openpyxl
from pywinauto.application import Application
from winreg import *
from threading import Thread
import threading
import shutil
from seleniumwire import webdriver

config = configparser.ConfigParser()
config.read_file(open(r'../Config/ifconfig.txt'))
ipv4 = 'http://' + config.get('IFCONFIG', 'ipv4')
ipv6 = 'http://[' + config.get('IFCONFIG', 'ipv6') + ']'
ipv6_ping = config.get('IFCONFIG', 'ipv6')
ipv4_ping = config.get('IFCONFIG', 'ipv4')
ipv6_global = 'http://[' + config.get('IFCONFIG', 'ipv6_global') + ']'

user = config.get('USER_INFO', 'user')
pass_word = config.get('USER_INFO', 'pw')
rg_port = config.get('PORT', 'rg_port')
cm_port = config.get('PORT', 'cm_port')
com =rg_port
final_report = '../Report/final_report_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '-') + '.xlsx'
Helper.Helper_common.reset_report_result(final_report)


class PageLogin(unittest.TestCase):
    def setUp(self):
        # print("echo " + self._testMethodName)
        self.start_time = datetime.datetime.now()
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_LG_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(3)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 4. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('4. URL QS wrong: ' + driver.current_url)
        self.assertListEqual(list_steps_fail, [], '[UI_LG_01] Log in with IPv4 fail')

    def test_UI_LG_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv6)
        time.sleep(3)
        expected_quick_setup = ipv6 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 4. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Login Quick setup:  ' + driver.current_url)
            list_steps_fail.append('4. URL QS wrong: ' + driver.current_url)
        self.assertListEqual(list_steps_fail, [], '[UI_LG_02] Log in with link local IPv6 fail')

    def test_UI_LG_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv6_global)
        time.sleep(3)
        expected_quick_setup = ipv6_global + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 4. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('4. URL QS wrong: ' + driver.current_url)

        self.assertListEqual(list_steps_fail, [], '[UI_LG_03] Log in with global IPv6 fail')

    def test_UI_LG_05(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv4)
        api_login = Helper.Helper_common.api_login()
        session = api_login['system']['timer']['session']

        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup, '[UI_LG_05] URL page quick setup return wrong')
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Wait more than 10 minutes
        time.sleep(session * 60)
        Helper.Helper_common.login(driver, self, ipv4)
        # Click to 2.4 GHZ
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        self.assertEqual(driver.current_url, expected_quick_setup, '[UI_LG_05] URL page quick setup return wrong')
        time.sleep(3)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = "123456789"

        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(3)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        Helper.Helper_common.wait_time(self, driver)

        confirm_pw = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        time.sleep(3)
        actual_password = driver.find_element_by_css_selector('[id="2g-network-password"] strong').text
        self.assertEqual(actual_password, keys_send, '[UI_LG_05] Change password fail')

    def test_UI_LG_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.list_steps = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Step 1: Log in with correct user name and wrong password
        Helper.Helper_common.check_login(driver, self, ipv4)

        time.sleep(1)
        driver.find_element_by_id('login').send_keys(
            '''123! @ # ^ & * ( ) + _ - = { } [ ] | 456:789 . ? ` $ % \ ; '" < > , /''')
        driver.find_element_by_id('senha').send_keys(
            '''123! @ # ^ & * ( ) + _ - = { } [ ] | 456:789 . ? ` $ % \ ; '" < > , /''')
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(1)
        password_length = len(driver.find_element_by_id('senha').get_attribute('value'))
        username_length = len(driver.find_element_by_id('login').get_attribute('value'))
        user_text = driver.find_element_by_css_selector('[for=login]').text
        password_text = driver.find_element_by_css_selector('[for=senha]').text
        actual = [username_length, user_text, password_length, password_text]
        expected = [32, 'Login incorreto', 16, 'Senha incorreta']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append("\n[Pass] 2. Check values length and message of user and pw." )
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. Check values length and message of user and pw. \nExpected: %s. \nActual: %s." %(str(expected), str(actual)))
            list_steps_fail.append('[UI_LG_04] Verify Login with correct user name and wrong password fail. \nExpected: %s. \nActual: %s.' %(str(expected), str(actual)))
            pass

        self.assertEqual(list_steps_fail, [], list_steps_fail)

    def test_UI_LG_06(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        sample_input = '\; ls -l\;'
        for i in range(1, 6):
            Helper.Helper_common.test_login(driver, ipv4, user=sample_input, pass_word=sample_input)
            # Check red error
            error = driver.find_elements_by_css_selector('.f-wrap.error')
            try:
                self.assertNotEqual(len(error), 0)
                self.list_steps.append("\n[Pass] 2.1 Check Red text Error appear")
            except AssertionError:
                self.list_steps.append("\n[Fail] 2.1 Check Red text Error appear")
                list_steps_fail.append('\nCheck Red text Error appear but it were not appear')
                pass
            api_test_login = Helper.Helper_common.test_api_login(user=sample_input, pass_word=sample_input)
            actual = api_test_login['error']['code']
            expected = 422
            try:
                self.assertEqual(actual, expected)
                self.list_steps.append("\n[Pass] 2.1 Check Red text Error code")
            except AssertionError:
                self.list_steps.append("\n[Fail] 2.1 Check Red text Error code")
                list_steps_fail.append('\nCheck Red text Error code is %d but Actual is %d' %(expected, actual))
                pass
        # Fill correct info
        Helper.Helper_common.login(driver, self, ipv4)
        error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(len(error), 0)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error appear")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error appear")
            list_steps_fail.append('\nCheck Red text Error appear but it were not appear')
            pass
        api_test_login = Helper.Helper_common.test_api_login(user='humax', pass_word='humax')
        actual = api_test_login['error']['code']
        expected = 422
        try:
            self.assertEqual(actual, expected)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error code")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error code")
            list_steps_fail.append('\nCheck Red text Error code is %d but Actual is %d' %(expected, actual))
            pass
        # Wait 1 min with wrong info
        time.sleep(60)
        Helper.Helper_common.test_login(driver, ipv4, user=sample_input, pass_word=sample_input)
        # Check red error
        error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(len(error), 0)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error appear")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error appear")
            list_steps_fail.append('\nCheck Red text Error appear but it were not appear')
            pass
        api_test_login = Helper.Helper_common.test_api_login(user=sample_input, pass_word=sample_input)
        actual = api_test_login['error']['code']
        expected = 422
        try:
            self.assertEqual(actual, expected)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error code")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error code")
            list_steps_fail.append('\nCheck Red text Error code is %d but Actual is %d' % (expected, actual))
            pass
        # Wait 2 mins
        time.sleep(120)
        Helper.Helper_common.login(driver, self, ipv4)
        expected_url = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2.Login success: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.Login success ' + driver.current_url)
            list_steps_fail.append('2. URL QS wrong: ' + driver.current_url)
        self.assertListEqual(list_steps_fail, [], '[UI_LG_06] Assertion wrong')

    def test_UI_LG_07(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.list_steps = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        sample_input = '\; ls -l\;'
        for i in range(1, 6):
            Helper.Helper_common.test_login(driver, ipv6, user=sample_input, pass_word=sample_input)
            # Check red error
            error = driver.find_elements_by_css_selector('.f-wrap.error')
            try:
                self.assertNotEqual(len(error), 0)
                self.list_steps.append("\n[Pass] 2.1 Check Red text Error appear")
            except AssertionError:
                self.list_steps.append("\n[Fail] 2.1 Check Red text Error appear")
                list_steps_fail.append('\nCheck Red text Error appear but it were not appear')
                pass
            api_test_login = Helper.Helper_common.test_api_login(user=sample_input, pass_word=sample_input)
            actual = api_test_login['error']['code']
            expected = 422
            try:
                self.assertEqual(actual, expected)
                self.list_steps.append("\n[Pass] 2.1 Check Red text Error code")
            except AssertionError:
                self.list_steps.append("\n[Fail] 2.1 Check Red text Error code")
                list_steps_fail.append('\nCheck Red text Error code is %d but Actual is %d' % (expected, actual))
                pass
        # Fill correct info
        Helper.Helper_common.login(driver, self, ipv6)
        error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(len(error), 0)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error appear")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error appear")
            list_steps_fail.append('\nCheck Red text Error appear but it were not appear')
            pass
        api_test_login = Helper.Helper_common.test_api_login(user='humax', pass_word='humax')
        actual = api_test_login['error']['code']
        expected = 422
        try:
            self.assertEqual(actual, expected)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error code")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error code")
            list_steps_fail.append('\nCheck Red text Error code is %d but Actual is %d' % (expected, actual))
            pass
        # Wait 1 min with wrong info
        time.sleep(60)
        Helper.Helper_common.test_login(driver, ipv6, user=sample_input, pass_word=sample_input)
        # Check red error
        error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(len(error), 0)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error appear")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error appear")
            list_steps_fail.append('\nCheck Red text Error appear but it were not appear')
            pass
        api_test_login = Helper.Helper_common.test_api_login(user=sample_input, pass_word=sample_input)
        actual = api_test_login['error']['code']
        expected = 422
        try:
            self.assertEqual(actual, expected)
            self.list_steps.append("\n[Pass] 2.1 Check Red text Error code")
        except AssertionError:
            self.list_steps.append("\n[Fail] 2.1 Check Red text Error code")
            list_steps_fail.append('\nCheck Red text Error code is %d but Actual is %d' % (expected, actual))
            pass
        # Wait 2 mins
        time.sleep(120)
        Helper.Helper_common.login(driver, self, ipv6)
        expected_url = ipv6 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2.Login success: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.Login success ' + driver.current_url)
            list_steps_fail.append('2. URL QS wrong: Expected %s. Actual: %s' %(expected_url, driver.current_url))
        self.assertListEqual(list_steps_fail, [], '[UI_LG_06] Assertion wrong')

    def test_UI_LG_08(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        web_conponents = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'login.js',
                    'cmp_form.js',
                    'messagebox.js']
        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_conponents]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_conponents:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)

        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 2.2 Check API return wrong on Login page.')
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check API return wrong on Login page. \nActual: %s' %(str(value_wrong)))
            list_steps_fail.append('2.2 API return on Login page: \nActual: %s' %(str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_LG_08] Assertion wrong')


class PageQuickSetup(unittest.TestCase):
    def setUp(self):

        self.start_time = datetime.datetime.now()
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_QS_01(self):
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./factory.py /SERIAL ''' + com + ''' /BAUD 115200''')
        time.sleep(150)
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        time.sleep(5)
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 2.Login success: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.Login success ' + driver.current_url)
            list_steps_fail.append('2. URL QS wrong: ' + driver.current_url)
        expected_list_check_name = [True, True, True, True]
        time.sleep(2)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]')
        ActionChains(driver).move_to_element(name_2g).perform()
        time.sleep(5)
        name_2g = name_2g.text
        check_list_2g = [name_2g.startswith('NET_2G'), len(name_2g[6:]) == 6, name_2g.isupper(), ':' not in name_2g]
        try:
            self.assertListEqual(check_list_2g, expected_list_check_name)
            self.list_steps.append(
                '\n[Pass] 4.1 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.1 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon in name. \nActual: %s \nExpected'
                + str(check_list_2g))
            list_steps_fail.append(
                '4.1 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon not in name :'
                + str(check_list_2g))

        name_5g = driver.find_element_by_css_selector('[id="5g-network-name"]')
        ActionChains(driver).move_to_element(name_5g).perform()
        name_5g = name_5g.text
        check_list_5g = [name_5g.startswith('NET_5G'), len(name_5g[6:]) == 6, name_5g.isupper(), ':' not in name_5g]

        try:
            self.assertListEqual(check_list_5g, expected_list_check_name)
            self.list_steps.append(
                '\n[Pass] 4.2 Check condition: Start with NET_5G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.2 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
            list_steps_fail.append(
                '4.2. Check condition: Start with NET_2G, 6 characters at the end, is upper, colon not in name :'
                + str(check_list_2g))

        expected_list_check_pw = [True, True, True]
        pw_5g = driver.find_element_by_css_selector('[id="5g-network-password"]')
        ActionChains(driver).move_to_element(pw_5g).perform()
        pw_5g = pw_5g.text
        check_condition_5g = [len(pw_5g) == 8, pw_5g.isupper(), ':' not in pw_5g]
        try:
            self.assertListEqual(check_condition_5g, expected_list_check_pw)
            self.list_steps.append(
                '\n[Pass] 4.3 Check condition: 8 characters, is upper, colon  in PW :' + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.3 Check condition:8 characters, is upper, colon  in PW :' + str(check_list_2g))
            list_steps_fail.append(
                '4.3 Check condition: 8 characters, is upper, colon not in PW :' + str(check_list_2g))
            pass

        pw_2g = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(pw_2g).perform()
        pw_2g = pw_2g.text
        check_condition_2g = [len(pw_2g) == 8, pw_2g.isupper(), ':' not in pw_2g]
        try:
            self.assertListEqual(check_condition_2g, expected_list_check_pw)
            self.list_steps.append(
                '\n[Pass] 4.4. Check condition: 8 characters, is upper, colon  in PW :' + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.4 Check condition:8 characters, is upper, colon  in PW :' + str(check_list_2g))
            list_steps_fail.append(
                '4.4 Check condition: 8 characters, is upper, colon not in PW :' + str(check_list_2g))
            pass

        self.assertListEqual(list_steps_fail, [], '[UI_QS_01] Assertion Default wifi name and password fail')

    def test_UI_QS_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(5)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(5)
        expected_quick_setup = ipv4 + '/#page-quick-setup'

        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL Quick setup wrong: ' + driver.current_url)
        # Click to 2.4 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(3)
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        keys_name = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()

        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """12345678"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300, '[UI_QS_02] Pop-up change pw do not close. Time out 300s')
            self.list_steps.append('\n[Pass] Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail] Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append(' Watting time: ' + str(time_out) + ' > 300 s')

        time.sleep(5)
        confirm_name = driver.find_element_by_css_selector('[id="2g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="2g-network-name"] strong').text
        time.sleep(5)
        try:
            self.assertEqual(actual_name, keys_name[:31])
            self.list_steps.append('\n[Pass] 3. Display Name: ' + str(actual_name))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.Display Name: ' + str(actual_name))
            list_steps_fail.append('3. Name display wrong: Actual: ' + str(actual_name)
                                   + '. Expected: ' + str(keys_name[:31]))

        self.assertListEqual(list_steps_fail, [], '[UI_QS_02] Assertion 2.4 GHz wifi name with special characters fail')

    def test_UI_QS_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        # Click to 5 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="5-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(1)
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        keys_name = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()

        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """12345678"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass]. Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail]. Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append(' Watting time: ' + str(time_out) + ' > 300 s')
        time.sleep(5)
        confirm_name = driver.find_element_by_css_selector('[id="5g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="5g-network-name"] strong').text
        time.sleep(5)
        try:
            self.assertEqual(actual_name, keys_name[:31])
            self.list_steps.append('\n[Pass] 3. Display Name: ' + str(actual_name))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Display Name: ' + str(actual_name))
            list_steps_fail.append('3. Name display wrong: ' + str(actual_name)
                                   + '. Expected: ' + str(keys_name[:31]))
            pass

        self.assertListEqual(list_steps_fail, [], '[UI_QS_03] Assertion 5 GHz wifi name with special characters fail')

    def test_UI_QS_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(5)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(5)
        expected_quick_setup = ipv4 + '/#page-quick-setup'

        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Click to 2.4 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(3)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""

        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(3)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass]  Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail]  Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append(' Watting time: ' + str(time_out) + ' > 300 s')
        time.sleep(5)
        confirm_pw = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        time.sleep(3)
        actual_password = driver.find_element_by_css_selector('[id="2g-network-password"] strong').text
        if '\n' in actual_password:
            actual_password = actual_password.replace('\n', '')
        try:
            self.assertEqual(actual_password, keys_send[:63], '[UI_QS_04] Change password fail')
            self.list_steps.append('\n[Pass] 3. Display PW: ' + str(actual_password))
        except AssertionError:
            self.list_steps.append('\n[Fail]  3. Display PW: ' + str(actual_password))
            list_steps_fail.append('3. PW display wrong: ' + str(actual_password)
                                   + '. Expected: ' + keys_send[:63])

        self.assertListEqual(list_steps_fail, [],
                             '[UI_QS_04] Assertion 2.4 GHz wifi password with special characters fail')

    def test_UI_QS_05(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Click to 5 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="5-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(3)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(3)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass]  Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail]  Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append(' Watting time: ' + str(time_out) + ' > 300 s')

        confirm_pw = driver.find_element_by_css_selector('[id="5g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        time.sleep(5)
        actual_password = driver.find_element_by_css_selector('[id="5g-network-password"] strong').text
        if '\n' in actual_password:
            actual_password = actual_password.replace('\n', '')
        try:
            self.assertEqual(actual_password, keys_send[:63], '[UI_QS_05] Change PW fail with all spaces')
            self.list_steps.append('\n[Pass] 3. Display PW: ' + str(actual_password))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Display PW:  ' + str(actual_password))
            list_steps_fail.append('3. PW display wrong: ' + str(actual_password))

        self.assertListEqual(list_steps_fail, [],
                             '[UI_QS_05] Assertion 5 GHz wifi password with special characters fail')

    def test_UI_QS_06(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []

        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(5)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Click to 2.4 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(1)
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        # 65 spaces
        keys_name = """                                                                 """
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()

        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """                                                                 """
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass]  Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail] Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append('Watting time: ' + str(time_out) + ' > 300 s')

        confirm_name = driver.find_element_by_css_selector('[id="2g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="2g-network-name"] strong').text
        time.sleep(5)
        try:
            self.assertEqual(actual_name, keys_name[:31])
            self.list_steps.append('\n[Pass] 3.1 Display Name: ' + str(len(actual_name)))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Display Name: ' + str(actual_name))
            list_steps_fail.append('3.1 Name display wrong: Actual: ' + str(len(actual_name))
                                   + 'spaces. Expected: ' + str(len(keys_name[:31])))
            pass

        confirm_pw = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        time.sleep(3)
        actual_password = driver.find_element_by_css_selector('[id="2g-network-password"] strong').text
        if '\n' in actual_password:
            actual_password = actual_password.replace('\n', '')
        try:
            self.assertEqual(actual_password, keys_send[:63])
            self.list_steps.append('\n[Pass] 3.2 Display PW: ' + str(actual_password))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Display PW: ' + str(actual_password))
            list_steps_fail.append('3.2 PW display wrong: ' + str(actual_password))
            pass

        self.assertListEqual(list_steps_fail, [],
                             '[UI_QS_06] Assertion 2.4 GHz wifi name and password with all space characters fail')

    def test_UI_QS_07(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []

        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Click to 2.4 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="5-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(1)
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        keys_name = """                                                                 """
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()

        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """                                                                 """
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass]  Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail]  Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append(' Watting time: ' + str(time_out) + ' > 300 s')

        confirm_name = driver.find_element_by_css_selector('[id="5g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="5g-network-name"] strong').text
        time.sleep(3)
        try:
            self.assertEqual(actual_name, keys_name[:31])
            self.list_steps.append('\n[Pass] 3.1 Display Name: ' + str(actual_name))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Display Name: ' + str(actual_name))
            list_steps_fail.append('3.1 Name display wrong:  Actual: ' + str(len(actual_name))
                                   + 'spaces. Expected: ' + str(len(keys_name[:31])))
            pass

        confirm_pw = driver.find_element_by_css_selector('[id="5g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        time.sleep(5)
        actual_password = driver.find_element_by_css_selector('[id="5g-network-password"] strong').text
        if '\n' in actual_password:
            actual_password = actual_password.replace('\n', '')
        try:
            self.assertEqual(actual_password, keys_send[:63])
            self.list_steps.append('\n[Pass] 3.2 Display PW:' + str(actual_password))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Display PW: ' + str(actual_password))
            list_steps_fail.append('3.2 PW display wrong: ' + str(actual_password))
            pass

        self.assertListEqual(list_steps_fail, [],
                             '[UI_QS_07] Assertion 5 GHz wifi name and password with all space characters fail')

    def test_UI_QS_08(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        # hostname = socket.gethostname()
        # ipv4_addr = socket.gethostbyname(hostname)
        # starting_ipv4 = int(ipv4_addr.split('.')[-1])
        ipconfig_pc = str(subprocess.check_output('ipconfig', shell=True))

        starting_ipv4 = (re.findall("IPv4 Address. . . . . . . . . . . : 192.168.0.([0-9]*)", ipconfig_pc)[0])
        starting_local_addr_value = random.randint(int(starting_ipv4) + 1, 255)
        number_of_CPEs_value = 255 - starting_local_addr_value
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        driver.get(ipv4 + '/#page-network-dhcp')
        time.sleep(1)
        # Lease time
        lease_time = driver.find_element_by_css_selector('[name="rede-dhcp"] div:nth-child(5)')
        ActionChains(driver).move_to_element(lease_time).double_click().send_keys('5').perform()

        # Starting local address
        starting_local_address = driver.find_element_by_css_selector('[name="rede-dhcp"] .f-row:nth-child(3) input')
        ActionChains(driver).move_to_element(starting_local_address).double_click().send_keys(
            str(starting_local_addr_value)).perform()
        get_address = driver.find_element_by_css_selector(
            '[name="rede-dhcp"] .f-row:nth-child(3) .input-label-inline .span').text
        expected_ip_address = get_address + str(starting_local_addr_value)

        # Number of CPEs
        number_of_CPEs = driver.find_element_by_css_selector('[name="rede-dhcp"] .f-row:nth-child(4) input')
        ActionChains(driver).move_to_element(number_of_CPEs).double_click().send_keys(
            str(number_of_CPEs_value)).perform()

        driver.find_element_by_css_selector('.button').click()

        # Wating for more than 5 minutes
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass] Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail] Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append(' Watting time: ' + str(time_out) + ' > 300 s')
        time.sleep(300)
        driver.get(ipv4 + '/#page-login')
        time.sleep(1)
        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(3)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 5. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('5. URL QS wrong: ' + driver.current_url)

        table_list_devices = driver.find_element_by_css_selector('.table')
        ActionChains(driver).move_to_element(table_list_devices).perform()

        list_ip_addr = []
        ip_addr_elements = driver.find_elements_by_css_selector('.table tbody tr td:last-child')
        for ele in ip_addr_elements:
            list_ip_addr.append(ele.text)
        try:
            self.assertIn(expected_ip_address, list_ip_addr)
            self.list_steps.append('\n[Pass] 6. IP address of Test PC '
                                   + str(expected_ip_address) + ' not in: ' + str(list_ip_addr))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. IP address of Test PC'
                                   + str(expected_ip_address) + ' not in: ' + str(list_ip_addr))
            list_steps_fail.append('6. IP address of Test PC '
                                   + str(expected_ip_address) + ' not in: ' + str(list_ip_addr))

        self.assertListEqual(list_steps_fail, [],
                             '[UI_QS_08] Assertion Connected device list when change start IP fail')

    def test_UI_QS_09(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv4)
        driver.refresh()
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'quick_setup.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'srv_wifi.js',
                    'messagebox.js',
                    'cmp_headresult.js',
                    '270x600',
                    'wifi',
                    'devices?connected=true',
                    'menu_main.js',
                    'ssid',
                    'ssid',
                    'srv_network.js',
                    'wan']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Quick setup page.')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API return wrong on Quick setup page. \nActual: %s' % (str(value_wrong)))
            list_steps_fail.append('3. API return on Quick setup page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_LG_08] Assertion wrong')

    def test_UI_QS_10(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        # Click to 2 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(1)
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        keys_name = "NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()

        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_pw = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_pw).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_pw).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        time.sleep(3)
        confirm_name = driver.find_element_by_css_selector('[id="2g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="2g-network-name"] strong').text

        confirm_pw = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        actual_pw = driver.find_element_by_css_selector('[id="2g-network-password"] strong').text
        time.sleep(3)
        actual = [actual_name, actual_pw]
        expected = [keys_name[:31], keys_pw[:63]]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3. Change Wifi Name and Password 2G interface')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Change Wifi Name and Password 2G interface. \nExpected: %s \nActual: %s.' %(str(expected),str(actual_name)))
            list_steps_fail.append('3. Wifi Name and Password displayed wrong of 2G interface: \nExpected: %s \nActual: %s.' %(str(expected),str(actual_name)))
            pass

        self.assertListEqual(list_steps_fail, [], '[UI_QS_10] Assertion 2 GHz wifi name with special characters fail')

    def test_UI_QS_11(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        # Click to 5 GHZ
        time.sleep(3)
        click_type = driver.find_element_by_xpath('//label[@for="5-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(1)
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        keys_name = "NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()

        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_pw = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_pw).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_pw).perform()

        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        time.sleep(3)
        confirm_name = driver.find_element_by_css_selector('[id="5g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="5g-network-name"] strong').text

        confirm_pw = driver.find_element_by_css_selector('[id="5g-network-password"]')
        ActionChains(driver).move_to_element(confirm_pw).perform()
        actual_pw = driver.find_element_by_css_selector('[id="5g-network-password"] strong').text
        time.sleep(3)
        actual = [actual_name, actual_pw]
        expected = [keys_name[:31], keys_pw[:63]]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3. Change Wifi Name and Password 5G interface')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Change Wifi Name and Password 5G interface. \nExpected: %s \nActual: %s.' %(str(expected),str(actual_name)))
            list_steps_fail.append('3. Wifi Name and Password displayed wrong of 5G interface: \nExpected: %s \nActual: %s.' %(str(expected),str(actual_name)))
            pass

        self.assertListEqual(list_steps_fail, [], '[UI_QS_11] Assertion 5 GHz wifi name with special characters fail')


class PageStatusSoftware(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SS_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()

        Helper.Helper_common.check_login(driver, self, ipv4)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'

        try:
            self.assertEqual(driver.current_url, expected_quick_setup, '[UI_SS_01] URL page quick setup get wrong')
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        time.sleep(2)
        config_advance = driver.find_element_by_css_selector('a.next.config[href="#page-status-software"]')
        ActionChains(driver).move_to_element(config_advance).click().perform()
        expected_status_software = ipv4 + '/#page-status-software'

        try:
            self.assertEqual(driver.current_url, expected_status_software)
            self.list_steps.append('\n[Pass] 2. Page Status Software: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status Software: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Status Software wrong ' + driver.current_url)

        time.sleep(5)
        version_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(2) >li:nth-child(2)')
        ActionChains(driver).move_to_element(version_actual).perform()
        version_actual = version_actual.text.splitlines()[-1]

        json_api = Helper.Helper_common.api_gateway_about()
        version_expected = json_api['hardware']['version']

        try:
            self.assertEqual(version_actual, version_expected)
            self.list_steps.append('\n[Pass] 3. Get Version info: ' + str(version_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Get Version info: ' + str(version_actual))
            list_steps_fail.append('3. Version info wrong ' + str(version_actual))

        self.assertListEqual(list_steps_fail, [], '[UI_SS_01] Assertion H/W version status fail')

    def test_UI_SS_02(self):
        global value_expected_convert
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'

        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        config_advance = driver.find_element_by_css_selector('a.next.config[href="#page-status-software"]')
        ActionChains(driver).move_to_element(config_advance).click().perform()
        expected_status_software = ipv4 + '/#page-status-software'

        try:
            self.assertEqual(driver.current_url, expected_status_software)
            self.list_steps.append('\n[Pass] 2. Page Status software: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status software: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Status software wrong: ' + driver.current_url)

        time.sleep(3)
        value_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(2) >li:nth-child(5)')
        ActionChains(driver).move_to_element(value_actual).perform()
        value_actual = value_actual.text.splitlines()[-1]

        json_api = Helper.Helper_common.api_network_docsis()
        value_expected = json_api['docsisCert']
        if str(value_expected).lower() == 'true':
            value_expected_convert = 'Instalado'
        elif str(value_expected).lower() == 'false':
            value_expected_convert = 'Não instalado'
        try:
            self.assertEqual(value_actual, value_expected_convert)
            self.list_steps.append('\n[Pass] 3. Check CM certificate value: ' + str(value_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check CM certificate value: ' + str(value_actual))
            list_steps_fail.append('3. CM certificate value displayed wrong: ' + str(value_actual))

        self.assertListEqual(list_steps_fail, [], '[UI_SS_02] Asserttion CM certificate status fail')

    def test_UI_SS_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        config_advance = driver.find_element_by_css_selector('a.next.config[href="#page-status-software"]')
        ActionChains(driver).move_to_element(config_advance).click().perform()
        time.sleep(3)
        api_about_verify = Helper.Helper_common.api_gateway_about()
        expected_status_software = ipv4 + '/#page-status-software'
        api_docsis = Helper.Helper_common.api_network_docsis()
        api_about = Helper.Helper_common.api_gateway_about()
        try:
            self.assertEqual(driver.current_url, expected_status_software)
            self.list_steps.append('\n[Pass] 2. Page Status software: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status software: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Status software wrong: ' + driver.current_url)

        # Technology version
        technology_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(2) >li:nth-child(1)')
        ActionChains(driver).move_to_element(technology_actual).perform()
        technology_actual = technology_actual.text.splitlines()[-1]
        technology_expected = api_docsis['version']
        try:
            self.assertEqual(technology_actual, technology_expected)
            self.list_steps.append('\n[Pass] 3.1 Technology version' + str(technology_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Technology version' + str(technology_actual))
            list_steps_fail.append('3.1 Technology version displayed wrong ' + str(technology_actual))
            pass

        # Software version
        software_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(2) >li:nth-child(3)')
        ActionChains(driver).move_to_element(software_actual).perform()
        software_actual = software_actual.text.splitlines()[-1]
        software_expected = api_about['software']['version']

        try:
            self.assertEqual(software_actual, software_expected)
            self.list_steps.append('\n[Pass] 3.2 Software version' + str(software_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Software version' + str(software_actual))
            list_steps_fail.append('3.2 Software version display wrong' + str(software_actual))
            pass

        # MAC address of CM
        mac_addr_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(2) >li:nth-child(4)')
        ActionChains(driver).move_to_element(mac_addr_actual).perform()
        mac_addr_actual = mac_addr_actual.text.splitlines()[-1]
        mac_addr_expected = api_docsis['cm']['macAddress']
        try:
            self.assertEqual(mac_addr_actual, mac_addr_expected)
            self.list_steps.append('\n[Pass] 3.3  MAC Address of CM' + str(mac_addr_actual))
        except AssertionError:
            self.list_steps.append('\n[Pass] 3.3  MAC Address of CM' + str(mac_addr_actual))
            list_steps_fail.append('3.3  MAC Address of CM display wrong' + str(mac_addr_actual))
            pass

        # Access status
        access_status_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(4) >li:nth-child(2)')
        ActionChains(driver).move_to_element(access_status_actual).perform()
        access_status_actual = access_status_actual.text.splitlines()[-1]
        access_status_expected = api_docsis['networkAccess']
        if str(access_status_expected).lower() == 'true':
            access_status_expected_convert = 'Permitido'
        elif str(access_status_expected).lower() == 'false':
            access_status_expected_convert = 'Negado'
        try:
            self.assertEqual(access_status_actual, access_status_expected_convert)
            self.list_steps.append('\n[Pass] 3.4  Access status:' + str(access_status_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.4  Access status:' + str(access_status_actual))
            list_steps_fail.append('3.4  Access status display wrong' + str(access_status_actual))
            pass

        # System time
        time.sleep(3)
        system_time_actual = driver.find_element_by_css_selector('.box-content >.list:nth-child(4) >li:nth-child(1)')
        ActionChains(driver).move_to_element(system_time_actual).perform()
        system_time_actual = system_time_actual.text.splitlines()[-1]
        system_time_actual_check = \
            [int(i) for i in list(re.findall(r"([0-9]*) days ([0-9]*)h:([0-9]*)m:([0-9]*)s", system_time_actual)[0])]
        system_time_expected = api_about['operationTime']
        system_time_expected_check = \
            [int(i) for i in list(re.findall(r"([0-9]*) days ([0-9]*)h:([0-9]*)m:([0-9]*)s", system_time_expected)[0])]
        system_time_expected_before = api_about_verify['operationTime']
        system_time_expected_check_before = \
            [int(i) for i in
             list(re.findall(r"([0-9]*) days ([0-9]*)h:([0-9]*)m:([0-9]*)s", system_time_expected_before)[0])]
        if system_time_expected_check[3] <= 3 and system_time_expected_check_before[3] >= 3:
            system_time_expected_check[3] = system_time_expected_check[3] + 59

        try:
            self.assertAlmostEqual(system_time_actual_check[3], system_time_expected_check_before[3], delta=4)
            self.assertAlmostEqual(system_time_expected_check[3], system_time_actual_check[3], delta=4)
            self.list_steps.append('\n[Pass] 3.5  System time: ' + str(system_time_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.5  System time: ' + str(system_time_actual))
            list_steps_fail.append('3.5  System time display wrong: ' + str(system_time_actual))

        self.assertListEqual(list_steps_fail, [], '[UI_SS_03] Assertion Status information fail')

    def test_UI_SS_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status sortware
        config_advance = driver.find_element_by_css_selector('a.next.config[href="#page-status-software"]')
        ActionChains(driver).move_to_element(config_advance).click().perform()
        expected_status_software = ipv4 + '/#page-status-software'

        try:
            self.assertEqual(driver.current_url, expected_status_software)
            self.list_steps.append('\n[Pass] 2. Page Status software: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status software: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Status software wrong: ' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'software.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'about',
                    'docsis',
                    'menu_main.js',
                    'wan']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Status Software page.')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API return wrong on Status Software page. \nActual: %s' % (str(value_wrong)))
            list_steps_fail.append('3. API return on Status Software page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SS_04] Assertion wrong')


class PageStatusRFConnection(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SR_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        driver.get(ipv4 + '/#page-status-rf-connection')
        expected_url = ipv4 + '/#page-status-rf-connection'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Page Status RF Connection: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status RF Connection: ' + driver.current_url)
            list_steps_fail.append('2.  URL RF Connection display wrong' + driver.current_url)

        time.sleep(3)
        api_initial = Helper.Helper_common.api_network_docsis_initial_frequency()
        api_docsis = Helper.Helper_common.api_network_docsis()
        api_procedure = Helper.Helper_common.api_network_docsis_procedure()

        # Initial frequency
        initial_frequency_expected = api_initial['initialFrequency']

        initial_frequency_actual = driver.find_element_by_css_selector(
            '.box-content >.list:nth-child(2) >li:nth-child(1)')
        ActionChains(driver).move_to_element(initial_frequency_actual).perform()
        initial_frequency_actual = initial_frequency_actual.text.splitlines()[-1]
        try:
            self.assertEqual(initial_frequency_actual, str(initial_frequency_expected))
            self.list_steps.append('\n[Pass] 3.1 Initial frequency: ' + str(initial_frequency_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Initial frequency: ' + str(initial_frequency_actual))
            list_steps_fail.append('3.1 Initial frequency display wrong' + str(initial_frequency_actual))
            pass

        # Connectivity Status
        connect_state_expected = api_docsis['connectionState']
        if connect_state_expected == 10:
            connect_state_expected_convert = 'OK'
        else:
            connect_state_expected_convert = 'em progresso'
        connect_state_actual = driver.find_element_by_css_selector(
            '.box-content >.list:nth-child(2) >li:nth-child(2)')
        ActionChains(driver).move_to_element(connect_state_actual).perform()
        connect_state_actual = connect_state_actual.text.splitlines()[1]
        try:
            self.assertEqual(connect_state_actual, connect_state_expected_convert)
            self.list_steps.append('\n[Pass] 3.2 Connect Status: ' + str(connect_state_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Connect Status: ' + str(connect_state_actual))
            list_steps_fail.append('3.2 Connect Status display wrong' + str(connect_state_actual))
            pass

        # Initialization status
        initialization_status_expected = api_procedure['sequence']
        if initialization_status_expected == 1:
            initialization_status_expected_convert = 'OK'
        else:
            initialization_status_expected_convert = 'In Progress'
        initialization_status_actual = driver.find_element_by_css_selector(
            '.box-content >.list:nth-child(2) >li:nth-child(3)')
        ActionChains(driver).move_to_element(initialization_status_actual).perform()
        initialization_status_actual = initialization_status_actual.text.splitlines()[1]
        try:
            self.assertEqual(initialization_status_actual, initialization_status_expected_convert)
            self.list_steps.append('\n[Pass] 3.3 Initialization Status: ' + str(initialization_status_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.3 Initialization Status: ' + str(initialization_status_actual))
            list_steps_fail.append('3.3 Initialization Status display wrong' + str(initialization_status_actual))
        self.assertEqual(list_steps_fail, [], '[UI_SR_01] Assertion Startup procedure status fail')

    def test_UI_SR_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        driver.get(ipv4 + '/#page-status-rf-connection')
        expected_url = ipv4 + '/#page-status-rf-connection'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Page Status RF Connection: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status RF Connection: ' + driver.current_url)
            list_steps_fail.append('2.  URL RF Connection display wrong' + driver.current_url)

        api_channel = Helper.Helper_common.api_network_docsis_channel()
        num_of_downstream_expected = api_channel['numOfDownstream']
        for i in range(4):
            time.sleep(1)
            see_more = driver.find_element_by_css_selector('form[name="down-stream"] .f-row>button')
            ActionChains(driver).move_to_element(see_more).click().perform()
            time.sleep(1)

        num_of_downstream_actual = len(driver.find_elements_by_css_selector('form[name="down-stream"] li'))
        try:
            self.assertEqual(num_of_downstream_expected, num_of_downstream_actual)
            self.list_steps.append('\n[Pass] 3. Check Num of Downstream:' + str(num_of_downstream_expected))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check Num of Downstream:' + str(num_of_downstream_expected))
            list_steps_fail.append('3.  Num of Downstream display wrong' + str(num_of_downstream_expected))
        self.assertEqual(list_steps_fail, [], '[UI_SR_02] Assertion CM downstream channel status fail')

    def test_UI_SR_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        driver.get(ipv4 + '/#page-status-rf-connection')
        expected_url = ipv4 + '/#page-status-rf-connection'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Page Status RF Connection: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status RF Connection: ' + driver.current_url)
            list_steps_fail.append('2.  URL RF Connection display wrong' + driver.current_url)

        api_channel = Helper.Helper_common.api_network_docsis_channel()
        num_of_upstream_expected = api_channel['numOfUpstream']

        see_more = driver.find_element_by_css_selector('.up-str .f-row>button')
        ActionChains(driver).move_to_element(see_more).click().perform()
        time.sleep(2)
        num_of_upstream_actual = len(driver.find_elements_by_css_selector('form[name="up-stream"] li'))
        try:
            self.assertEqual(num_of_upstream_expected, num_of_upstream_actual)
            self.list_steps.append('\n[Pass] 3. Check Num of Upstream: ' + str(num_of_upstream_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check Num of Upstream: ' + str(num_of_upstream_actual))
            list_steps_fail.append('3.  Num of Upstream display wrong' + str(num_of_upstream_actual))

        self.assertEqual(list_steps_fail, [], '[UI_SR_03] Assertion CM upstream channel status fail')

    def test_UI_SR_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status RF Connection
        driver.get(ipv4 + '/#page-status-rf-connection')
        expected_url = ipv4 + '/#page-status-rf-connection'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Page Status RF Connection: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Status RF Connection: ' + driver.current_url)
            list_steps_fail.append('2.  URL RF Connection display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'rf_connection.js',
                    'srv_network.js',
                    'cmp_form.js',
                    'cmp_basic.js',
                    'docsis',
                    'procedure',
                    'channel',
                    'initialFrequency',
                    'about',
                    'menu_main.js']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Status RF Connection page.')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API return wrong on Status RF Connection page. \nActual: %s' % (str(value_wrong)))
            list_steps_fail.append('3. API return on Status RF Connection page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SR_04] Assertion wrong')


class PageStatusIPConnection(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SIC_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        driver.get(ipv4 + '/#page-status-ip-connection')
        expected_url = ipv4 + '/#page-status-ip-connection'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Status IP Connection: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Status IP Connection: ' + driver.current_url)
            list_steps_fail.append('2. URL Status IP Connection display wrong' + driver.current_url)

        api_wan = Helper.Helper_common.api_network_wan()['interfaces'][0]
        if api_wan['ipv6']['leaseTime'] == 0:
            api_wan['ipv6']['leaseTime'] = '--'
        ip_info_expected = [api_wan['ipv4']['address'],
                            api_wan['ipv6']['address'] + '/' + str(api_wan['ipv6']['prefixLength']),
                            str(api_wan['ipv6']['leaseTime']), api_wan['ipv6']['expireTime'],
                            api_wan['ipv4']['dnsServer1'], api_wan['ipv6']['dnsServer1'],
                            api_wan['macAddress']]

        time.sleep(3)
        rows = driver.find_elements_by_css_selector('.left li')
        time.sleep(3)
        ip_info_actual = []
        for i in range(1, len(rows) + 1):
            row = driver.find_element_by_css_selector('.left li:nth-child(' + str(i) + ')').text
            if '\n' not in row:
                row = ''
            else:
                row = row.splitlines()[1]
            ip_info_actual.append(row)

        try:
            self.assertListEqual(ip_info_expected, ip_info_actual)
            self.list_steps.append('\n[Pass] 3. Check List Status IP connection: ' + str(ip_info_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check List Status IP connection: ' + str(ip_info_actual))
            list_steps_fail.append('3. List Status IP connection display wrong' + str(ip_info_actual))

        self.assertEqual(list_steps_fail, [], '[UI_SIC_01] Assertion IP connection status fail')

    def test_UI_SIC_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver = self.driver
        driver.get(ipv4 + '/#page-status-ip-connection')
        expected_url = ipv4 + '/#page-status-ip-connection'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Status IP Connection: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Status IP Connection: ' + driver.current_url)
            list_steps_fail.append('2. URL Status IP Connection display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'ip_connection.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'wan',
                    'about',
                    'menu_main.js'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Status IP Connection page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Status IP Connection page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Status IP Connection page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SIC_02] Assertion wrong')


class PageStatusMTAStatus(unittest.TestCase):

    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SMS_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        driver.get(ipv4 + '/#page-status-mta-status')
        expected_url = ipv4 + '/#page-status-mta-status'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Status MTA Status: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Status MTA Status: ' + driver.current_url)
            list_steps_fail.append('2.URL page Status MTA Status display wrong' + driver.current_url)

        time.sleep(3)
        api_mta = Helper.Helper_common.api_mta_startup_procedure()
        status_expected = [api_mta['dhcp'], api_mta['security'],
                           api_mta['tftp'], api_mta['callServer'],
                           api_mta['registration']]
        status_expected_convert = [i.replace('\\', '') for i in status_expected]
        time.sleep(2)
        rows = len(driver.find_elements_by_css_selector('.list:nth-child(2) li'))
        status_actual = []
        for i in range(1, rows + 1):
            row = driver.find_element_by_css_selector('.list:nth-child(2) li:nth-child(' + str(i) + ')').text
            status_actual.append(row.split('Status: ')[-1])
            time.sleep(1)
        try:
            self.assertListEqual(status_expected_convert, status_actual)
            self.list_steps.append('\n[Pass] 3. Check List Initialization Procedure Status: ' + str(status_actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check List Initialization Procedure Status: ' + str(status_actual))
            list_steps_fail.append('3. List Initialization Procedure Status display wrong' + str(status_actual))

        self.assertEqual(list_steps_fail, [], '[UI_SMS_01] Assertion Initialization procedure status fail')

        # request_connect = subprocess.check_output('netsh wlan connect name=HVNWifi ssid=HVNWifi',
        #                                       shell=True)

    def test_UI_SMS_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        time.sleep(1)
        driver.get(ipv4 + '/#page-status-mta-status')
        expected_url = ipv4 + '/#page-status-mta-status'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Status MTA Status: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Status MTA Status: ' + driver.current_url)
            list_steps_fail.append('2.URL page Status MTA Status display wrong' + driver.current_url)

        time.sleep(2)
        line_status = driver.find_elements_by_css_selector('[name="status-conexao"] li')
        ActionChains(driver).move_to_element(line_status[-1]).perform()
        actual_result = []
        for i in range(1, len(line_status) + 1):
            line = driver.find_element_by_css_selector('[name="status-conexao"] li:nth-child(' + str(i) + ')').text
            list_value = []
            for j in line.splitlines():
                list_value.append(j.split(': ')[1])
            actual_result.append(list_value)

        # API
        api_lines = Helper.Helper_common.api_mta_line_status()
        expected_result = []
        for line in api_lines:
            if not line['active']:
                hookState = 'N/A'
            elif line['hookState']:
                hookState = 'No gancho'
            else:
                hookState = 'Fora do gancho'
            expected_result.append([str(line['lineno']), hookState, str(line['expireTime']), str(line['reRegTime'])])
        try:
            self.assertListEqual(actual_result, expected_result)
            self.list_steps.append('\n[Pass] 3. Check Values in Line status: ' + str(actual_result))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check Values in Line status: ' + str(actual_result))
            list_steps_fail.append('3. Values in Line status display wrong' + str(actual_result))

        self.assertListEqual(list_steps_fail, [], '[UI_SMS_02] Assertion Line status Fail')

    def test_UI_SMS_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver = self.driver
        driver.get(ipv4 + '/#page-status-mta-status')
        expected_url = ipv4 + '/#page-status-mta-status'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Status MTA Status: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Status MTA Status: ' + driver.current_url)
            list_steps_fail.append('2.URL page Status MTA Status display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'mta_status.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'line',
                    'procedure',
                    'about',
                    'menu_main.js',
                    'wan']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Status MTA Status page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Status MTA Status page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Status MTA Status page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SIC_02] Assertion wrong')


class PageNetworkBasicSettings(unittest.TestCase):
    def setUp(self):
        self.list_steps = []
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        self.driver.maximize_window()

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_NBS_01(self):
        list_steps_fail = []
        # Step1: Log in
        self.def_name = Helper.Helper_common.get_func_name()
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(2)

        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(expected_quick_setup, driver.current_url, "Login failed")
            self.list_steps.append('1. ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('1. ' + driver.current_url)

        # Step 2: Access the "page-network-basic-settings" page
        try:
            driver.get(ipv4 + '/#page-network-basic-settings')
            time.sleep(2)
            self.list_steps.append('2. ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('2. ' + driver.current_url)

        # Step 3: verify LAN information
        # get actual data
        time.sleep(3)
        list_lan_info = driver.find_elements_by_css_selector('.lan-info > li')
        ipv4_address = str(list_lan_info[0].text).split('\n')[-1].strip()
        ipv6_address = str(list_lan_info[1].text).split('\n')[-1].strip()
        ipv6_prefix = str(list_lan_info[2].text).split('\n')[-1].strip()
        mac_address = str(list_lan_info[3].text).split('\n')[-1].strip()
        actual = [ipv4_address,
                  ipv6_address,
                  ipv6_prefix,
                  mac_address]
        # call API to get expected data
        lan_info_expected = Helper.Helper_common.get_lan_info()
        ipv4_address_expected = lan_info_expected['ipv4']['ipAddress']
        ipv6_address_expected = lan_info_expected['ipv6']['ipAddress']
        ipv6_prefix_expected = lan_info_expected['ipv6']['prefix']
        mac_address_expected = lan_info_expected['macAddress']
        expected = [ipv4_address_expected,
                    ipv6_address_expected,
                    ipv6_prefix_expected,
                    mac_address_expected]
        # verify data

        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 2.2 Check API LAN Network Basic setting page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 2.2 Check API LAN Network Basic setting page. \nActual: %s. \nExpected: %s' %(str(actual), str(expected)))
            list_steps_fail.append('2.2 API LAN Network Basic setting page wrong: \nActual: %s. \nExpected: %s' %(str(actual), str(expected)))

        self.assertListEqual(list_steps_fail, [], '[UI_NBS_01] Assertion wrong')

    def test_UI_NBS_02(self):
        list_steps_fail = []
        # Step1: Log in
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(2)

        expected_quick_setup = ipv4 + '/#page-quick-setup'
        self.assertEqual(expected_quick_setup, driver.current_url, "Login failed")

        # Step 2: Access the "page-network-basic-settings" page
        driver.get(ipv4 + '/#page-network-basic-settings')
        time.sleep(5)


        # get actual data
        list_lan_info = driver.find_elements_by_css_selector('.wan-info > li')
        ipv4_address = str(list_lan_info[0].text).split('\n')[-1].strip()
        ipv6_address = str(list_lan_info[1].text).split('\n')[-1].strip()
        total_connection_time = str(list_lan_info[2].text).split('\n')[-1].strip()
        expiration_time = str(list_lan_info[3].text).split('\n')[-1].strip()
        IPv4_DNS_Server = str(list_lan_info[4].text).split('\n')[-1].strip()
        IPv6_DNS_Server = str(list_lan_info[5].text).split('\n')[-1].strip()
        mac_address = str(list_lan_info[6].text).split('\n')[-1].strip()
        actual = [ipv4_address,
                  ipv6_address,
                  total_connection_time,
                  expiration_time,
                  IPv4_DNS_Server,
                  IPv6_DNS_Server,
                  mac_address]

        # call API to get expected data
        wan_info_expected = Helper.Helper_common.get_wan_info()
        ipv4_address_expected = str(wan_info_expected['interfaces'][0]['ipv4']['address'])
        ipv6_address_expected = str(wan_info_expected['interfaces'][0]['ipv6']['address'])
        total_connection_time_expected = str(wan_info_expected['interfaces'][0]['ipv6']['leaseTime'])
        expiration_time_expected = str(wan_info_expected['interfaces'][0]['ipv6']['expireTime'])
        IPv4_DNS_Server_expected = str(wan_info_expected['interfaces'][0]['ipv4']['dnsServer1'])
        IPv6_DNS_Server_expected = str(wan_info_expected['interfaces'][0]['ipv6']['dnsServer1'])
        mac_address_expected = str(wan_info_expected['interfaces'][0]['macAddress'])
        expected = [ipv4_address_expected,
                    ipv6_address_expected,
                    total_connection_time_expected,
                    expiration_time_expected,
                    IPv4_DNS_Server_expected,
                    IPv6_DNS_Server_expected,
                    mac_address_expected]
        # verify data

        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 2.2 Check API WAN Network Basic setting page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 2.2 Check API WAN Network Basic setting page. \nActual: %s. \nExpected: %s' % (
                    str(actual), str(expected)))
            list_steps_fail.append(
                '2.2 API Network WAN Basic setting page wrong: \nActual: %s. \nExpected: %s' % (
                    str(actual), str(expected)))

        self.assertListEqual(list_steps_fail, [], '[UI_NBS_02] Assertion wrong')

    def test_UI_NBS_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-basic-settings')
        expected_url = ipv4 + '/#page-network-basic-settings'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network Basic Setting: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network Basic Setting: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network Basic Setting display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'mta_status.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'line',
                    'procedure',
                    'about',
                    'menu_main.js',
                    'wan']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Network Basic Setting page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Network Basic Setting page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Network Basic Setting page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_NBS_04] Assertion wrong')


class PageNetworkDHCP(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_ND_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        # DHCP url
        expected_dhcp_url = ipv4 + '/#page-network-dhcp'
        driver.get(expected_dhcp_url)
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_url)
            self.list_steps.append('\n[Pass] 2. Page Network DHCP available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page Network DHCP available: ' + driver.current_url)
            list_steps_fail.append('2. URL Network DHCP wrong: ' + driver.current_url)
        time.sleep(5)

        orange = '#ff9c00'
        sim_yes_no = driver.find_element_by_css_selector('[for=servidor-dhcp-sim]')
        color_check = sim_yes_no.value_of_css_property('background')
        color_check = Helper.Helper_common.convert_rbg_hex(color_check)
        if color_check == orange:
            actual_sim = True
            actual_nao = False
        else:
            actual_sim = False
            actual_nao = True

        if actual_sim:
            nao_btn = driver.find_element_by_css_selector('.inline div:last-child')
            nao_btn.click()
            btn_apply = driver.find_element_by_css_selector('.button')
            ActionChains(driver).move_to_element(btn_apply).click().perform()
            time.sleep(1)
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time_out = 0
            while len(pop_up_wait) == 1:
                pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
                time.sleep(1)
                time_out += 1
                if time_out == 300:
                    break
            try:
                self.assertLessEqual(time_out, 300)
                self.list_steps.append('Time out: ' + str(time_out) + ' < 300 s')
            except AssertionError:
                self.list_steps.append('Time out: ' + str(time_out) + ' > 300 s')
                list_steps_fail.append('Time out: ' + str(time_out) + ' > 300 s')
        # NAO
        api_lan = Helper.Helper_common.api_network_lan()
        expected_nao = api_lan['ipv4']['dhcp']['active']
        try:
            self.assertEqual(actual_nao, expected_nao)
            self.list_steps.append('\n[Pass] 4. NAO btn is selected' + str(expected_nao))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. NAO btn is selected:' + str(expected_nao))
            list_steps_fail.append('4. NAO btn is not selected' + str(expected_nao))

        # SIM
        sim_btn = driver.find_element_by_css_selector('.inline div:nth-child(2)')
        sim_btn.click()
        btn_apply = driver.find_element_by_css_selector('.button')
        ActionChains(driver).move_to_element(btn_apply).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        actual_sim = True
        api_lan = Helper.Helper_common.api_network_lan()
        expected_sim = api_lan['ipv4']['dhcp']['active']
        try:
            self.assertEqual(actual_sim, expected_sim)
            self.list_steps.append('\n[Pass] 6. SIM btn is selected:' + str(expected_sim))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. SIM btn is selected:' + str(expected_sim))
            list_steps_fail.append('6. SIM btn is not selected:' + str(expected_sim))

        # NAO
        nao_btn = driver.find_element_by_css_selector('.inline div:last-child')
        nao_btn.click()
        btn_apply = driver.find_element_by_css_selector('.button')
        ActionChains(driver).move_to_element(btn_apply).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        actual_nao = False
        api_lan = Helper.Helper_common.api_network_lan()
        expected_nao = api_lan['ipv4']['dhcp']['active']
        try:
            self.assertEqual(actual_nao, expected_nao)
            self.list_steps.append('\n[Pass] 8. NAO btn is selected' + str(expected_nao))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. NAO btn is selected:' + str(expected_nao))
            list_steps_fail.append('8. NAO btn is not selected' + str(expected_nao))

        self.assertEqual(list_steps_fail, [], '[UI_ND_01] Assertion Enable/Disable DHCP fail')

        # Restore default    
        sim_btn = driver.find_element_by_css_selector('.inline div:nth-child(2)')
        sim_btn.click()
        btn_apply = driver.find_element_by_css_selector('.button')
        ActionChains(driver).move_to_element(btn_apply).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break

    def test_UI_ND_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(4)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()

        expected_dhcp_url = ipv4 + '/#page-network-dhcp'
        driver.get(ipv4 + '/#page-network-dhcp')
        time.sleep(1)

        try:
            self.assertEqual(driver.current_url, expected_dhcp_url)
            self.list_steps.append('\n[Pass] 2. Page DHCP available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL DHCP wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL DHCP wrong: ' + driver.current_url)

        # Lease time
        lease_time = driver.find_element_by_css_selector('[name="rede-dhcp"] div:nth-child(5)')
        ActionChains(driver).move_to_element(lease_time).double_click().send_keys('5').perform()

        btn_apply = driver.find_element_by_css_selector('.button')
        btn_apply.click()

        # Wating for more than 5 minutes
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass] Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail] Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append('Watting time: ' + str(time_out) + ' > 300 s')

        # Connect PC to 2.4G Wifi
        request_connect = subprocess.check_output('netsh wlan connect name=' + name_2g + ' ssid=' + name_2g,
                                                  shell=True)
        connect_success_noti = 'Connection request was completed successfully.'
        try:
            self.assertIn(connect_success_noti, str(request_connect))
            self.list_steps.append('[Pass] 4. Connect to 2.4G wifi: ' + str(request_connect))
        except AssertionError:
            self.list_steps.append('[Fail] 4. Connect to 2.4G wifi: ' + str(request_connect))
            list_steps_fail.append('4. Connect to 2.4G wifi failure: ')
            pass
        time.sleep(10)

        # Ping to IPv4
        ping = subprocess.check_output('ping ' + ipv4_ping, shell=True)
        loss_value = int(str(ping).split('% loss')[0].split('(')[1])
        try:
            self.assertEqual(loss_value, 0)
            self.list_steps.append('\n[Pass] 5. Can not ping to ipv4 address:' + ipv4_ping
                                   + '.Loss: ' + str(loss_value) + '%')
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Can not ping to ipv4 address:' + ipv4_ping
                                   + '.Loss: ' + str(loss_value) + '%')
            list_steps_fail.append('5. Can not ping to ipv4 address:' + ipv4_ping
                                   + '.Loss: ' + str(loss_value) + '%')
            pass

        driver.get(ipv4 + '/#page-login')
        time.sleep(2)
        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(5)
        driver.get(ipv4 + '/#page-network-dhcp')
        time.sleep(10)
        # Lease time
        lease_time = driver.find_element_by_css_selector('[name="rede-dhcp"] div:nth-child(5)')
        ActionChains(driver).move_to_element(lease_time).double_click().send_keys('180').perform()
        time.sleep(5)
        btn_apply = driver.find_element_by_css_selector('.button')
        btn_apply.click()
        time.sleep(20)
        # Wating for more than 5 minutes
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass] Watting time: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail] Watting time: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append('Watting time: ' + str(time_out) + ' > 300 s')

        # Ping to IPv4 AGAIN
        ping = subprocess.check_output('ping ' + ipv4_ping, shell=True)
        loss_value = int(str(ping).split('% loss')[0].split('(')[1])
        try:
            self.assertEqual(loss_value, 0)
            self.list_steps.append('\n[Pass] 7. Can not ping to ipv4 address:' + ipv4_ping
                                   + '.Loss: ' + str(loss_value) + '%')
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Can not ping to ipv4 address:' + ipv4_ping
                                   + '.Loss: ' + str(loss_value) + '%')
            list_steps_fail.append('7. Can not ping to ipv4 address:' + ipv4_ping
                                   + '.Loss: ' + str(loss_value) + '%')
        self.assertListEqual(list_steps_fail, [],
                             '[UI_ND_02] Assertion Connected device list when change start IP fail')
        subprocess.check_output('netsh wlan disconnect', shell=True)

    def test_UI_ND_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1: ping to DUT
        ping_dut = str(subprocess.check_output('ping 192.168.0.1', shell=True))
        try:
            self.assertTrue('Lost = 0' in ping_dut)
            self.list_steps.append('\n[Pass] 1. Ping DUT success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Ping DUT fail')
            self.list_steps_fail.append('1. Ping DUT fail')
            pass

        # Step 2: get the IP address
        ipconfig_pc = str(subprocess.check_output('ipconfig', shell=True))

        current_ip_address_pc = re.findall("IPv4 Address. . . . . . . . . . . : 192.168.0.([0-9]*)", ipconfig_pc)[0]
        new_ip_address_pc = int(current_ip_address_pc) + 1

        self.list_steps.append('\n[Pass] 2. IP of PC: 192.168.0.' + str(current_ip_address_pc))

        Helper.Helper_common.login(driver, self, ipv4)
        driver.get(ipv4 + '#page-network-dhcp')
        time.sleep(2)
        # Step 3:
        driver.find_element_by_css_selector('#tempo-de-emprestimo').clear()
        driver.find_element_by_css_selector('#tempo-de-emprestimo').send_keys('5')

        # Step 4:
        driver.find_element_by_css_selector('#endereco-local-de-inicio').clear()
        driver.find_element_by_css_selector('#endereco-local-de-inicio').send_keys(new_ip_address_pc)

        # change number of CPU
        driver.find_element_by_css_selector('#numero-de-cpes').clear()
        driver.find_element_by_css_selector('#numero-de-cpes').send_keys('1')

        time.sleep(1)

        # click to Apply
        driver.find_element_by_css_selector('div.holder-icon').click()

        # Step 5: wait for 5 minutes
        time.sleep(60 * 2)

        # Step 6: Check the IP address
        ipconfig_pc = str(subprocess.check_output('ipconfig', shell=True))

        actual_new_ip_address_pc = re.findall("IPv4 Address. . . . . . . . . . . : 192.168.0.([0-9]*)", ipconfig_pc)[0]
        try:
            self.assertEqual(str(actual_new_ip_address_pc), str(new_ip_address_pc))
            self.list_steps.append('\n[Pass] 6. New IP of PC: 192.168.0.' + str(new_ip_address_pc))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 1. New IP of PC is not matching with the changes: 192.168.0.' + str(new_ip_address_pc))
            self.list_steps_fail.append('[UI_ND_03] 1. Test PC IP is not changed')
            pass

        # Step 7: ping the DUT again
        ping_dut = str(subprocess.check_output('ping 192.168.0.1', shell=True))
        try:
            self.assertTrue('Lost = 0' in ping_dut)
            self.list_steps.append('\n[Pass] 7. Ping DUT success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Ping DUT fail')
            self.list_steps_fail.append('[UI_ND_03] 7. Ping DUT fail')
            pass

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_ND_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1: connect test PC to DUT

        # Step 2: get DNS sever address
        ipconfig_pc = str(subprocess.check_output('ipconfig /all', shell=True))

        current_ip_address_pc = re.findall("IPv4 Address. . . . . . . . . . . : 192.168.0.([0-9]*)", ipconfig_pc)[0]
        new_ip_address_pc = int(current_ip_address_pc) + 1

        old_dns_server = re.findall("DNS Servers . . . . . . . . . . . : (192.168.0.[0-9]*)", ipconfig_pc)[0]

        self.list_steps.append('\n[Pass] 2. Get DNS server of PC success:' + str(old_dns_server))

        # Step 3: Login
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Login fail:' + driver.current_url)
            self.list_steps_fail.append('[UI_ND_04] 3. Login fail' + driver.current_url)

        # Step 4: redirect DHCP
        driver.get(ipv4 + '/#page-network-dhcp')
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-network-dhcp')
            self.list_steps.append('\n[Pass] 4. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. The page isn't available: " + driver.current_url)
            self.list_steps_fail.append("[UI_ND_04] 4. The page isn't available: " + driver.current_url)
            pass

        time.sleep(2)
        # Step 5:
        try:
            driver.find_element_by_css_selector('#tempo-de-emprestimo').clear()
            driver.find_element_by_css_selector('#tempo-de-emprestimo').send_keys('5')

            driver.find_element_by_css_selector('#numero-de-cpes').clear()
            driver.find_element_by_css_selector('#numero-de-cpes').send_keys('1')

            driver.find_element_by_css_selector('#endereco-local-de-inicio').clear()
            driver.find_element_by_css_selector('#endereco-local-de-inicio').send_keys(new_ip_address_pc)
            time.sleep(1)
            self.list_steps.append("\n[Pass] 5. Change the info successfully")
        except AssertionError:
            self.list_steps.append("\n[Fail] 5. Change the info failed")
            self.list_steps_fail.append("[UI_ND_04] 5. Change the info in DHCP failed")

        # click to Apply
        driver.find_element_by_css_selector('div.holder-icon').click()

        # wait for 2 minutes
        time.sleep(60 * 2)

        # Step 6: Check the DNS sever information
        ipconfig_pc = str(subprocess.check_output('ipconfig /all', shell=True))
        current_dns_server = re.findall("DNS Servers . . . . . . . . . . . : (192.168.0.[0-9]*)", ipconfig_pc)[0]
        try:
            self.assertEqual(old_dns_server, current_dns_server)
            self.list_steps.append('\n[Pass] 6. Value of new DNS server: ' + current_dns_server)
        except AssertionError:
            self.list_steps.append("\n[Fail] 6. Value of new DNS server: " + current_dns_server)
            self.list_steps_fail.append("[UI_ND_04] 6. Value of DNS server is not same as step 2")
            pass
        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_ND_05(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver

        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-dhcp')
        expected_url = ipv4 + '/#page-network-dhcp'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network DHCP: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network DHCP: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network DHCP display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'dhcp.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_ipinput.js',
                    'cmp_headresult.js',
                    'comparator.js',
                    'messagebox.js',
                    'lan',
                    'about',
                    'menu_main.js',
                    'wan']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Network DHCP page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Network DHCP page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Network DHCP page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_ND_05] Assertion wrong')

    def test_UI_ND_06(self):
        self.driver.quit()
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        # os.system('''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./factory.py /SERIAL '''
        #           + com + ''' /BAUD 115200''')
        # # Wait for factory
        # time.sleep(100)
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(2)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-dhcp')
        expected_url = ipv4 + '/#page-network-dhcp'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network DHCP: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network DHCP: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network DHCP display wrong' + driver.current_url)
        time.sleep(3)

        # Local Address
        local_addr = driver.find_elements_by_css_selector('.gatewayip div input')
        actual = []
        for val in local_addr:
            actual.append(val.get_attribute('value'))
        expected = ['192','168', '0', '1']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3.1 Check Value of Local Address.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3.1 Check Value of Local Address. \nActual: %s. \nExpected: %s' %(str(actual), str(expected)))
            list_steps_fail.append('3.1 Value of Local Address: \nActual: %s.  \nExpected: %s' %(str(actual), str(expected)))

        # Enable DHCP server (If SIM >>True), Starting local address, Number of CPE, Lease time
        dhcp = Helper.Helper_common.check_radio_tick(driver, '#servidor-dhcp-sim')
        starting_local_addr = driver.find_element_by_id('endereco-local-de-inicio').get_attribute('value')
        cpe = driver.find_element_by_id('numero-de-cpes').get_attribute('value')
        lease_time = driver.find_element_by_id('tempo-de-emprestimo').get_attribute('value')
        actual = [dhcp, starting_local_addr, cpe, lease_time]
        expected = ['true', '10', '245', '1440']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3.2 Check Value of Enable DHCP server (If SIM >>True), Starting local address, Number of CPE, Lease time.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3.2 Check Value of Enable DHCP server (If SIM >>True), Starting local address, Number of CPE, Lease time. \nActual: %s. \nExpected: %s' %(str(actual), str(expected)))
            list_steps_fail.append('3.2 Value of Enable DHCP server (If SIM >>True), Starting local address, Number of CPE, Lease time: \nActual: %s.  \nExpected: %s' %(str(actual), str(expected)))

        # Check response from API
        api_lan = Helper.Helper_common.call_get_api_genaeral('/api/v1/network/lan')
        expected = ['192.168.0.1', True, '192.168.0.10', '192.168.0.254', 86400]
        actual = [api_lan['ipv4']['ipAddress'],
                  api_lan['ipv4']['dhcp']['active'],
                  api_lan['ipv4']['dhcp']['startIP'],
                  api_lan['ipv4']['dhcp']['endIP'],
                  api_lan['ipv4']['dhcp']['leaseTime']]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3.3 Check Value of APi ipAddr, active, StartIp, EndIp, Lease time.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3.3 Check Value of APi ipAddr, active, StartIp, EndIp, Lease time. \nActual: %s. \nExpected: %s' %(str(actual), str(expected)))
            list_steps_fail.append('3.3 Value of APi ipAddr, active, StartIp, EndIp, Lease time: \nActual: %s.  \nExpected: %s' %(str(actual), str(expected)))

        self.assertListEqual(list_steps_fail, [], '[UI_ND_06] Assertion wrong')


class PageNetworkDHCPv6(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_NDv6_01(self):

        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []

        output = subprocess.check_output('ipconfig/all', shell=True)
        ipv6_local_link = \
            str(output).split('Ethernet adapter Ethernet:')[1].split('Default Gateway . . . . . . . . . : ')[1].split(
                '%')[0]
        ipv6_local_link_url = 'http://[' + ipv6_local_link + ']'

        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        driver.get(ipv6_local_link_url)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)

        expected_quick_setup = ipv6_local_link_url + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 3. Check Login success and redirect to Quick Setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check Login success and redirect to Quick Setup ' + driver.current_url)
            list_steps_fail.append('3. Check URL Page-quick-setup wrong: ' + driver.current_url)

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_01] Assertion Connect Web UI from IPv6 gateway fail')

    def test_UI_NDv6_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        # Restore default DHCPv66
        Helper.Helper_common.api_network_lan_restoreDefault()

        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv6)
        expected_quick_setup = ipv6 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login QS: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login QS: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_dhcp_v6 = ipv6 + '/#page-network-dhcp-v6'
        driver.get(expected_dhcp_v6)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_v6)
            self.list_steps.append('\n[Pass] 2. Check page Network DHCP v6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check page Network DHCP v6: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Network DHCP v6 wrong: ' + driver.current_url)

        time.sleep(2)
        # Uncheck ATIVAR
        driver.find_element_by_css_selector('.radio-check-label[for=ativar]').click()
        # Apply
        apply = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply).click().perform()
        time.sleep(2)

        # Reboot
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./reboot.py /SERIAL ''' + com + ''' /BAUD 115200''')
        time.sleep(5 * 60)

        Helper.Helper_common.login(driver, self, ipv6)
        expected_quick_setup = ipv6 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 5. Login QS after reboot: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Login QS after reboot: ' + driver.current_url)
            list_steps_fail.append('5. URL QS wrong after reboot: ' + driver.current_url)

        expected_dhcp_v6 = ipv6 + '/#page-network-dhcp-v6'
        driver.get(expected_dhcp_v6)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_v6)
            self.list_steps.append('\n[Pass] 6. Check page Network DHCP v6 after reboot: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check page Network DHCP v6 after reboot: ' + driver.current_url)
            list_steps_fail.append('6. URL Page Network DHCP v6 wrong after reboot: ' + driver.current_url)

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_03] Assertion Ping to gate way fail')

    def test_UI_NDv6_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        # Restore default DHCPv66
        Helper.Helper_common.api_network_lan_restoreDefault()
        # Ping to IPv6
        ping = subprocess.check_output('ping ' + ipv6_ping, shell=True)
        loss_value = int(str(ping).split('% loss')[0].split('(')[1])
        try:
            self.assertEqual(loss_value, 0)
            self.list_steps.append('\n[Pass] 1. Can not ping to ipv6 address:' + ipv6_ping
                                   + '.Loss: ' + str(loss_value) + '%')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Can not ping to ipv6 address:' + ipv6_ping
                                   + '.Loss: ' + str(loss_value) + '%')
            list_steps_fail.append('1. Can not ping to ipv6 address:' + ipv6_ping
                                   + '.Loss: ' + str(loss_value) + '%')

        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv6)
        expected_quick_setup = ipv6 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 2. URL QS wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL QS wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL QS wrong: ' + driver.current_url)

        expected_dhcp_v6 = ipv6 + '/#page-network-dhcp-v6'
        driver.get(expected_dhcp_v6)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_v6)
            self.list_steps.append('\n[Pass] 3. Check page Network DHCP v6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check page Network DHCP v6: ' + driver.current_url)
            list_steps_fail.append('3. URL Page Network DHCP v6 wrong: ' + driver.current_url)

        time.sleep(2)
        # Uncheck ATIVAR
        driver.find_element_by_css_selector('.radio-check-label[for=ativar]').click()
        # Apply
        apply = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply).click().perform()
        time.sleep(2)

        ping_again = subprocess.check_output('ping ' + ipv6_ping, shell=True)
        loss_value = int(str(ping_again).split('% loss')[0].split('(')[1])
        try:
            self.assertEqual(loss_value, 0)
            self.list_steps.append('\n[Pass] 5. Can not ping again to ipv6 address:' + ipv6_ping
                                   + '.Loss: ' + str(loss_value) + '%')
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Can not ping to ipv6 address:' + ipv6_ping
                                   + '.Loss: ' + str(loss_value) + '%')
            list_steps_fail.append('5. Can not ping again to ipv6 address:' + ipv6_ping
                                   + '.Loss: ' + str(loss_value) + '%')

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_03] Assertion Ping to gate way fail')

    def test_UI_NDv6_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        expected_dhcp_v6 = ipv4 + '/#page-network-dhcp-v6'
        driver.get(expected_dhcp_v6)
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_v6)
            self.list_steps.append('\n[Pass] 2. Check page Network DHCP v6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check page Network DHCP v6: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Network DHCP v6 wrong: ' + driver.current_url)

        # Call api_restore_default
        Helper.Helper_common.api_network_lan_restoreDefault()
        api_network_lan = Helper.Helper_common.api_network_lan()
        expected_default = api_network_lan['ipv6']

        restore = driver.find_elements_by_css_selector('.button.icon')
        ActionChains(driver).move_to_element(restore[1]).click().perform()
        time.sleep(3)

        api_network_lan = Helper.Helper_common.api_network_lan()
        actual_default = api_network_lan['ipv6']
        try:
            self.assertEqual(str(expected_default), str(actual_default))
            self.list_steps.append('\n[Pass] 4. Check Restore default: ' + str(actual_default))
        except AssertionError:
            self.list_steps.append('\n[Fail] 44. Check Restore default: ' + str(actual_default))
            list_steps_fail.append('4. Restore default is not same as API' + str(actual_default))

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_04] Assertion Restore DHCPv6 Default configurations fail')

    def test_UI_NDv6_05(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        Helper.Helper_common.api_network_lan_restoreDefault()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_dhcp_v6 = ipv4 + '/#page-network-dhcp-v6'
        driver.get(expected_dhcp_v6)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_v6)
            self.list_steps.append('\n[Pass] 2. Check page Network DHCP v6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check page Network DHCP v6: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Network DHCP v6 wrong: ' + driver.current_url)

        # If 3 checks box were check. Call API
        expected_rapid_commit_check = True
        api_network_lan = Helper.Helper_common.api_network_lan()
        actual_rapid_commit = api_network_lan['ipv6']['dhcpv6']['rapidCommit']
        try:
            self.assertEqual(expected_rapid_commit_check, actual_rapid_commit)
            self.list_steps.append('\n[Pass] 6. RapidCommit checked' + str(actual_rapid_commit))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. RapidCommit checked' + str(actual_rapid_commit))
            list_steps_fail.append('6. Actual RapidCommit wrong with checked RapidCommit API')
            pass
        time.sleep(2)
        # Check Ativar rapid commit
        uncheck_rapid = driver.find_element_by_css_selector('.radio-check[for=ativar-comprometimento-rapido]')
        ActionChains(driver).move_to_element(uncheck_rapid).click().perform()

        # Apply
        apply = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply).click().perform()
        time.sleep(1)
        # Check API again
        expected_rapid_commit_uncheck = False
        api_network_lan = Helper.Helper_common.api_network_lan()
        actual_rapid_commit = api_network_lan['ipv6']['dhcpv6']['rapidCommit']
        try:
            self.assertEqual(actual_rapid_commit, expected_rapid_commit_uncheck)
            self.list_steps.append('\n[Pass] 6. RapidCommit unchecked' + str(actual_rapid_commit))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. RapidCommit unchecked' + str(actual_rapid_commit))
            list_steps_fail.append('6. Actual RapidCommit wrong with unchecked RapidCommit API')
            pass

        # Ckeck DESATIVAR DHCPV6 STATELESS at default > Apply. > Call API
        expected_mode_check = 'stateful'
        api_network_lan = Helper.Helper_common.api_network_lan()
        actual_mode = api_network_lan['ipv6']['mode']
        try:
            self.assertEqual(actual_mode, expected_mode_check)
            self.list_steps.append('\n[Pass] 8. DHCPv6 StateLess checked' + str(actual_mode))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. DHCPv6 StateLess checked' + str(actual_mode))
            list_steps_fail.append('8. Actual DHCPv6 StateLess wrong with checked DHCPv6 StateLess API')
            pass

        # UnCkeck DESATIVAR DHCPV6 STATELESS at default > Apply. > Call API
        # Uncheck DESATIVAR DHCPV6 STATELESS
        uncheck_stateless = driver.find_element_by_css_selector('.radio-check[for=dhcpv6-stateless]')
        ActionChains(driver).move_to_element(uncheck_stateless).click().perform()
        # Apply
        apply = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply).click().perform()
        expected_mode_uncheck = 'stateless'
        api_network_lan = Helper.Helper_common.api_network_lan()
        actual_mode = api_network_lan['ipv6']['mode']
        try:
            self.assertEqual(actual_mode, expected_mode_uncheck)
            self.list_steps.append('\n[Pass] 8. DHCPv6 StateLess unchecked' + str(actual_mode))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. DHCPv6 StateLess unchecked' + str(actual_mode))
            list_steps_fail.append('8. Actual DHCPv6 StateLess wrong with unchecked DHCPv6 StateLess API')

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_05] Assertion State changes fail')

        restore = driver.find_elements_by_css_selector('.button.icon')
        ActionChains(driver).move_to_element(restore[1]).click().perform()
        time.sleep(3)

    def test_UI_NDv6_06(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        Helper.Helper_common.api_network_lan_restoreDefault()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_dhcp_v6 = ipv4 + '/#page-network-dhcp-v6'
        driver.get(expected_dhcp_v6)
        try:
            self.assertEqual(driver.current_url, expected_dhcp_v6)
            self.list_steps.append('\n[Pass] 2. Page DHCPv6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Page DHCPv6: ' + driver.current_url)
            list_steps_fail.append('2. Page DHCPv6: ' + driver.current_url)

        expected_dhcp = ipv4 + '/#page-network-dhcp'
        driver.get(expected_dhcp)
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, expected_dhcp)
            self.list_steps.append('\n[Pass] 4. Page DHCP: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Page DHCP: ' + driver.current_url)
            list_steps_fail.append('4. Page DHCP: ' + driver.current_url)
        time.sleep(1)
        # Starting local address
        starting_local_addr_value = 210
        starting_local_address = driver.find_element_by_css_selector('[name="rede-dhcp"] .f-row:nth-child(3) input')
        ActionChains(driver).move_to_element(starting_local_address).double_click().send_keys(
            str(starting_local_addr_value)).perform()

        # Number of CPEs
        number_of_CPEs_value = 9
        number_of_CPEs = driver.find_element_by_css_selector('[name="rede-dhcp"] .f-row:nth-child(4) input')
        ActionChains(driver).move_to_element(number_of_CPEs).double_click().send_keys(
            str(number_of_CPEs_value)).perform()

        # Lease time
        lease_time_value = 20
        lease_time = driver.find_element_by_css_selector('[name="rede-dhcp"] div:nth-child(5)')
        ActionChains(driver).move_to_element(lease_time).double_click().send_keys(str(lease_time_value)).perform()

        driver.find_element_by_css_selector('.button').click()

        # Wating for more than 5 minutes
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        time_out = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            time_out += 1
            if time_out == 300:
                break
        try:
            self.assertLessEqual(time_out, 300)
            self.list_steps.append('\n[Pass]. Time out: ' + str(time_out) + ' < 300 s')
        except AssertionError:
            self.list_steps.append('\n[Fail]. Time out: ' + str(time_out) + ' > 300 s')
            list_steps_fail.append('Time out: ' + str(time_out) + ' > 300 s')

        # Return DHCPv6
        driver.get(expected_dhcp_v6)
        time.sleep(3)
        api_lan = Helper.Helper_common.api_network_lan()
        actual_mode = api_lan['ipv6']['mode']
        # Ativar is checked at Default
        try:
            self.assertEqual(actual_mode, 'stateful')
            self.list_steps.append('\n[Pass] 7. Check Ativar mode' + actual_mode)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Check Ativar mode' + actual_mode)
            list_steps_fail.append('Check Ativar mode wrong' + actual_mode)

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_06] Assertion Changes from LAN/DHCP fail')

    def test_UI_NDv6_07(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        driver = self.driver

        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-dhcp-v6')
        expected_url = ipv4 + '/#page-network-dhcp-v6'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network DHCP V6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network DHCP V6: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network DHCP V6 display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'jquery.li18n.js',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'dhcp_v6.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'comparator.js',
                    'lan',
                    'about',
                    'menu_main.js',
                    'wan']

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Network DHCP V6 page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Network DHCP V6 page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Network DHCP V6 page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_NDv6_07] Assertion wrong')


class PageNetworkLanV6(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_NLv6_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup, '[UI_NLv6_01] URL page quick setup return wrong')
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_lan_v6 = ipv4 + '/#page-network-lan-v6'
        driver.get(expected_url_lan_v6)
        try:
            self.assertEqual(driver.current_url, expected_url_lan_v6)
            self.list_steps.append('\n[Pass] 2. URL network lan v6 wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network lan v6 wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network lan v6 wrong: ' + driver.current_url)

        api_lan_ipv6 = Helper.Helper_common.api_lan_ipv6()
        expected_lan_ipv6 = [api_lan_ipv6[0]['ipv6LinkLocalAddress'],
                             api_lan_ipv6[0]['macAddress'],
                             api_lan_ipv6[0]['ipv6Reachable']]
        lanipv6_ui = driver.find_element_by_css_selector('.box-content>.list>li').text
        actual_lan_ipv6 = []
        for i in lanipv6_ui.splitlines():
            actual_lan_ipv6.append(i.split(': ')[1])

        try:
            self.assertEqual(actual_lan_ipv6, expected_lan_ipv6)
            self.list_steps.append('\n[Pass] 3. IPv6 Locallink, MAC addr, IPv6 Reachable displayed fail '
                                   + str(actual_lan_ipv6))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. IPv6 Locallink, MAC addr, IPv6 Reachable displayed fail'
                                   + str(actual_lan_ipv6))
            list_steps_fail.append('3. IPv6 Locallink, MAC addr, IPv6 Reachable displayed fail' + str(actual_lan_ipv6))

    def test_UI_NLv6_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        driver = self.driver

        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-lan-v6')
        expected_url = ipv4 + '/#page-network-lan-v6'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network Lan V6: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network Lan V6: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network Lan V6 display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'jquery.li18n.js',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'lan_v6.js',
                    'cmp_basic.js',
                    'devices?interface=lan-2.4g-5g',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Network Lan V6 page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Network Lan V6 page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Network Lan V6 page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_NLv6_02] Assertion wrong')


class PageNetworkDNSv4(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_NDv4_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_lan_v6 = ipv4 + '/#page-network-dns-v4'
        driver.get(expected_url_lan_v6)
        time.sleep(5)
        try:
            self.assertEqual(driver.current_url, expected_url_lan_v6)
            self.list_steps.append('\n[Pass] 2. URL network dns v4 wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dns v4 wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dns v4 wrong: ' + driver.current_url)

        api_network_wan = Helper.Helper_common.api_network_wan()
        expected = [api_network_wan['interfaces'][0]['ipv4']['dnsServer1'],
                    (api_network_wan['interfaces'][0]['ipv4']['dnsServer2']).strip()]

        primary_value = driver.find_element_by_css_selector('#dns-primario').get_attribute('value')
        secondary_value = driver.find_element_by_css_selector('#dns-secundario').get_attribute('value')
        actual = [primary_value, secondary_value]

        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append('\n[Pass] 3. Check values of Primary and Secondary DNS displayed wrong ')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.  Check values of Primary and Secondary DNS displayed wrong')
            list_steps_fail.append('3.  Check values of Primary and Secondary DNS displayed wrong' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_NDv4_01] Assertion DNSv4 status fail')

    def test_UI_NDv4_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_lan_v6 = ipv4 + '/#page-network-dns-v4'
        driver.get(expected_url_lan_v6)
        try:
            self.assertEqual(driver.current_url, expected_url_lan_v6)
            self.list_steps.append('\n[Pass] 2. URL network dns v4 wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dns v4 wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dns v4 wrong: ' + driver.current_url)
        time.sleep(6)
        # If check_btn is True. It's mean uncheck
        check_btn = driver.find_element_by_css_selector('[id="dns-primario"]').get_attribute('disabled')
        if check_btn != 'true':
            driver.find_element_by_css_selector('.radio-check').click()

        api_network_wan_1 = Helper.Helper_common.api_network_wan()
        expected_network_wan_1 = api_network_wan_1['interfaces'][0]['ipv4']['dnsAuto']
        try:
            self.assertTrue(expected_network_wan_1)
            self.list_steps.append('\n [Pass] 4. Check values displayed when the UESD is unchecked.')
        except AssertionError:
            self.list_steps.append('\n [Fail] 4. Check values displayed when the UESD is unchecked.')
            list_steps_fail.append('\n 4. Check values displayed when the UESD is unchecked.')
            pass

        driver.find_element_by_css_selector('.radio-check').click()

        primary = driver.find_element_by_css_selector('[for="dns-primario"]')
        primary_key = '123.123.123.123'
        ActionChains(driver).move_to_element(primary).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(primary_key).perform()
        time.sleep(5)
        secondary = driver.find_element_by_css_selector('[for="dns-secundario"]')
        secondary_key = '123.123.123.123'
        ActionChains(driver).move_to_element(secondary).click().send_keys(secondary_key).perform()
        time.sleep(5)
        # Click Apply
        driver.find_element_by_css_selector('.button.icon').click()
        time.sleep(15)
        check_error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertEqual(0, len(check_error))
            self.list_steps.append('6. [Pass] Check input values')
        except AssertionError:
            self.list_steps.append('6. [Fail] Check input values')
            list_steps_fail.append('Check input values wrong')
            pass

        api_network_wan_2 = Helper.Helper_common.api_network_wan()
        expected_network_wan_2 = api_network_wan_2['interfaces'][0]['ipv4']['dnsAuto']
        try:
            self.assertEqual(expected_network_wan_2, False)
            self.list_steps.append('\n [Pass] 7. Check values displayed when the UESD is checked.')
        except AssertionError:
            self.list_steps.append('\n [Fail] 7. Check values displayed when the UESD is checked.')
            list_steps_fail.append('\n Check values displayed when the UESD is checked.')
            pass
        time.sleep(10)
        # Uncheck UESD again
        driver.find_element_by_css_selector('.radio-check').click()
        driver.find_element_by_css_selector('.button.icon').click()
        time.sleep(15)
        api_network_wan_3 = Helper.Helper_common.api_network_wan()
        expected_network_wan_3 = api_network_wan_3['interfaces'][0]['ipv4']['dnsAuto']
        try:
            self.assertEqual(expected_network_wan_3, True)
            self.list_steps.append('\n [Pass] 9. Check values displayed when the UESD is unchecked.')
        except AssertionError:
            self.list_steps.append('\n [Fail] 9. Check values displayed when the UESD is unchecked.')
            list_steps_fail.append('\n 9. Check values displayed when the UESD is unchecked.')

        self.assertListEqual(list_steps_fail, [], '[UI_NDv4_02] Assertion Auto DNS configuration fail')

    def test_UI_NDv4_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver

        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-dns-v4')
        expected_url = ipv4 + '/#page-network-dns-v4'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network DNS v4: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network DNS v4: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network DNS v4 display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'jquery.li18n.js',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'lan_v6.js',
                    'cmp_basic.js',
                    'devices?interface=lan-2.4g-5g',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Network DNS v4 page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Network DNS v4 page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Network DNS v4 page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_NDv4_03] Assertion wrong')


class PageNetworkWanConfiguration(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_NWC_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-network-wan-configuration'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL network dns v4 wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dns v4 wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dns v4 wrong: ' + driver.current_url)
        time.sleep(5)
        # Click OUEIA
        driver.find_element_by_css_selector('.radio-check[for="dynamic-mode"]').click()
        # Click Liberar lease de IP de wan
        driver.find_element_by_css_selector('[id=release]').click()
        time.sleep(3)
        api_wan = Helper.Helper_common.api_network_wan()
        actual_api = [api_wan['interfaces'][0]['ipv4']['address'],
                      api_wan['interfaces'][0]['ipv4']['subnet'],
                      api_wan['interfaces'][0]['ipv4']['gateway'],
                      api_wan['interfaces'][0]['ipv4']['dnsServer1'],
                      api_wan['interfaces'][0]['ipv4']['dnsServer2']]
        expected = {"address": "0.0.0.0",
                    "subnet": "0.0.0.0",
                    "gateway": "0.0.0.0",
                    "dnsServer1": "",
                    "dnsServer2": " "}
        try:
            self.assertListEqual(actual_api, list(expected.values()))
            self.list_steps.append('[Pass] 5. Check values return by API ofLIBERAR LEASE DE IP WAN ...')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check values return by API of LIBERAR LEASE DE IP WAN...')
            list_steps_fail.append('5. Check value return by API ofLIBERAR LEASE DE IP WAN... wrong')
            pass

        # Click RENOVAR LEASE DE IP DE WAN
        driver.find_element_by_css_selector('#renew').click()
        time.sleep(5)
        api_wan = Helper.Helper_common.api_network_wan()
        actual_api_2 = [api_wan['interfaces'][0]['ipv4']['address'],
                        api_wan['interfaces'][0]['ipv4']['subnet'],
                        api_wan['interfaces'][0]['ipv4']['gateway'],
                        api_wan['interfaces'][0]['ipv4']['dnsServer1'],
                        api_wan['interfaces'][0]['ipv4']['dnsServer2']]
        expected_2 = {"address": "0.0.0.0",
                      "subnet": "0.0.0.0",
                      "gateway": "0.0.0.0",
                      "dnsServer1": "",
                      "dnsServer2": " "}
        try:
            self.assertNotEqual(str(actual_api_2), str(list(expected_2.values())))
            self.list_steps.append('[Pass] 7. Check values return by API of RENOVAR LEASE DE IP DE WAN ...')
        except AssertionError:
            self.list_steps.append('[Fail] 7. Check values return by API of RENOVAR LEASE DE IP DE WAN...')
            list_steps_fail.append(
                '7. Check value return by API of RENOVAR LEASE DE IP DE WAN... shoud be different from step 5')

        self.assertListEqual(list_steps_fail, [], '[UI_NWC_01] Assertion Get WAN IP automatically fail')

    def test_UI_NWC_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-network-wan-configuration'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL network dns v4 wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dns v4 wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dns v4 wrong: ' + driver.current_url)
        time.sleep(5)
        # Click USAR
        driver.find_element_by_css_selector('.radio-check[for=static-mode]').click()
        # IP WAN
        wan_ip = driver.find_element_by_css_selector('#wan-ip')
        wan_ip_value = '10.0.0.102'
        ActionChains(driver).move_to_element(wan_ip).double_click().send_keys(wan_ip_value).perform()
        # WAN Subnet
        wan_subnet = driver.find_element_by_css_selector('#wan-subnet-mask')
        wan_subnet_value = '255.255.255.0'
        ActionChains(driver).move_to_element(wan_subnet).double_click().send_keys(wan_subnet_value).perform()
        # WAN gateway
        wan_gateway = driver.find_element_by_css_selector('#wan-gateway-ip')
        wan_gateway_value = '10.0.0.1'
        ActionChains(driver).move_to_element(wan_gateway).double_click().send_keys(wan_gateway_value).perform()
        # Primary DNS
        primary_dns = driver.find_element_by_css_selector('#dns-primary')
        primary_dns_value = '172.16.0.12'
        ActionChains(driver).move_to_element(primary_dns).double_click().send_keys(primary_dns_value).perform()
        # Secondary DNS
        secondary_dns = driver.find_element_by_css_selector('#dns-second')
        secondary_dns_value = '8.8.8.8'
        ActionChains(driver).move_to_element(secondary_dns).double_click().send_keys(secondary_dns_value).perform()
        expected = [wan_ip_value, wan_subnet_value, wan_gateway_value, primary_dns_value, secondary_dns_value]
        # Click Apply
        driver.find_element_by_css_selector('button[value="Aplicar ajustes"]').click()
        time.sleep(25)
        # Check API
        api_wan = Helper.Helper_common.api_network_wan()
        actual_api = [api_wan['interfaces'][0]['ipv4']['address'],
                      api_wan['interfaces'][0]['ipv4']['subnet'],
                      api_wan['interfaces'][0]['ipv4']['gateway'],
                      api_wan['interfaces'][0]['ipv4']['dnsServer1'],
                      api_wan['interfaces'][0]['ipv4']['dnsServer2']]

        try:
            self.assertListEqual(actual_api, expected)
            self.list_steps.append('[Pass] 5. Check values return by API of USAR O SEGUINTE...')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check values return by API of USAR O SEGUINTE...')
            list_steps_fail.append('5. Check value return by API of USAR O SEGUINTE... wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_NWC_02] Assertion Set WAN IP static fail')

    def test_UI_NWC_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver

        # Click status IP Connection
        driver.get(ipv4 + '/#page-network-wan-configuration')
        expected_url = ipv4 + '/#page-network-wan-configuration'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Network Wan Configuration: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Network Wan Configuration: ' + driver.current_url)
            list_steps_fail.append('2.URL page Network Wan Configuration display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'main.js',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'wan_configuration.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'comparator.js',
                    'lan',
                    'wan',
                    'about',
                    'menu_main.js'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Network Wan Configuration page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Network Wan Configuration page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Network Wan Configuration page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_NWC_03] Assertion wrong')


class PageAdvancedDMZHost(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_ADH_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advanced-dmz-host'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL network dmz host wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dmz host wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dmz host wrong: ' + driver.current_url)
        time.sleep(5)
        # Input gateway IP
        dmz_host = driver.find_element_by_css_selector('#dmz-ip-address')
        dmz_host_value = '192.168.0.1'
        ActionChains(driver).move_to_element(dmz_host).double_click().send_keys(dmz_host_value).perform()
        # Click Apply
        driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]').click()

        # Check error
        check_error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('4. [Pass] Check the red error cell')
        except AssertionError:
            self.list_steps.append('4. [Fail] Check the red error cell')
            list_steps_fail.append('4. Check the red error wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_ADH_01] Assertion Using gateway IP as DMZ fail')

    def test_UI_ADH_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advanced-dmz-host'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL network dmz host wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dmz host wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dmz host wrong: ' + driver.current_url)
        time.sleep(5)
        # Input gateway IP
        dmz_host = driver.find_element_by_css_selector('#dmz-ip-address')
        dmz_host_value = '192.168.0.' + str(random.randint(1, 255))
        ActionChains(driver).move_to_element(dmz_host).double_click().send_keys(dmz_host_value).perform()
        # Click Apply
        driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]').click()
        time.sleep(15)
        api_dmz = Helper.Helper_common.api_dmz()
        actual_api = [api_dmz['active'], api_dmz['destination']]
        expected = [True, dmz_host_value]
        try:
            self.assertListEqual(actual_api, expected)
            self.list_steps.append('4. [Pass] Check values return from API')
        except AssertionError:
            self.list_steps.append('4. [Fail] Check values return from API')
            list_steps_fail.append('4. Check values return from API wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_ADH_02] Assertion Setup a new DMZ fail')

    def test_UI_ADH_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advanced-dmz-host'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL network dmz host wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL network dmz host wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL network dmz host wrong: ' + driver.current_url)
        time.sleep(5)
        # Click Remover
        driver.find_element_by_css_selector('button[value=REMOVER]').click()
        time.sleep(5)

        api_dmz = Helper.Helper_common.api_dmz()
        actual_api = [api_dmz['active'], api_dmz['destination']]
        expected = [False, '192.168.0.0']
        try:
            self.assertListEqual(actual_api, expected)
            self.list_steps.append('4. [Pass] Check values of disable DMZ return from API')
        except AssertionError:
            self.list_steps.append('4. [Fail] Check values of disable DMZ return from API')
            list_steps_fail.append('4. Check values of disable DMZ return from API wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_ADH_03] Assertion Disable DMZ fail')

    def test_UI_ADH_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver.get(ipv4 + '/#page-advanced-dmz-host')
        expected_url = ipv4 + '/#page-advanced-dmz-host'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Advanced Dmz Host: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Advanced Dmz Host: ' + driver.current_url)
            list_steps_fail.append('2.URL page Advanced Dmz Host display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'util.js',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'dmz_host.js',
                    'srv_service.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'comparator.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'lan',
                    'dmz',
                    'about',
                    'menu_main.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Advanced Dmz Host page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Advanced Dmz Host page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Advanced Dmz Host page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_ADH_04] Assertion wrong')


class PageAdvancedDDNSService(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_AD_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advanced-ddns'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL DDNS wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL DDNS wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL DDNS wrong: ' + driver.current_url)
        time.sleep(5)
        # Click ADICIONAR to modify DDNS Setting
        driver.find_element_by_css_selector('[for=input-create]').click()

        # FIll information
        time.sleep(2)
        domain_name = driver.find_element_by_css_selector('#domain-name')
        domain_name_value = 'humaxvina.homedns.org'
        ActionChains(driver).move_to_element(domain_name).click().send_keys(domain_name_value).perform()

        time.sleep(2)
        user_name = driver.find_element_by_css_selector('#user-name')
        user_name_value = 'Humax2018'
        ActionChains(driver).move_to_element(user_name).click().send_keys(user_name_value).perform()

        time.sleep(2)
        password = driver.find_element_by_css_selector('#password')
        password_value = 'Hvn2018@!'
        ActionChains(driver).move_to_element(password).click().send_keys(password_value).perform()

        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_ddns = Helper.Helper_common.api_ddns()
        actual_api = [api_ddns['active'], api_ddns['configuration']['username'],
                      api_ddns['configuration']['password'], api_ddns['configuration']['hostname'],
                      api_ddns['configuration']['currentProvider']]
        expected = [True, user_name_value, password_value, domain_name_value, 0]

        try:
            self.assertListEqual(actual_api, expected)
            self.list_steps.append('5. [Pass] Check values return from API')
        except AssertionError:
            self.list_steps.append('5. [Fail] Check values return from API')
            list_steps_fail.append('5. Check values return from API wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_AD_01] Assertion Enable DDNS service fail')

    def test_UI_AD_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advanced-ddns'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL DDNS wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL DDNS wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL DDNS wrong: ' + driver.current_url)
        time.sleep(5)
        # Click Remover
        driver.find_element_by_css_selector('#remove').click()
        time.sleep(5)

        api_ddns = Helper.Helper_common.api_ddns()
        actual_api = [api_ddns['active'], api_ddns['configuration']['username'],
                      api_ddns['configuration']['password'], api_ddns['configuration']['hostname'],
                      api_ddns['configuration']['token'], api_ddns['configuration']['currentProvider']]
        expected = [False, '', '', '', '', 0]

        try:
            self.assertListEqual(actual_api, expected)
            self.list_steps.append('5. [Pass] Check values return from API')
        except AssertionError:
            self.list_steps.append('5. [Fail] Check values return from API')
            list_steps_fail.append('5. Check values return from API wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_AD_01] Assertion Enable DDNS service fail')

    def test_UI_AD_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-advanced-ddns')
        expected_url = ipv4 + '/#page-advanced-ddns'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Advanced DDNS: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Advanced DDNS: ' + driver.current_url)
            list_steps_fail.append('2.URL page Advanced DDNS display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'ddns.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'srv_service.js',
                    'comparator.js',
                    'messagebox.js',
                    'ddns',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Advanced DDNS page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Advanced DDNS page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Advanced DDNS page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_AD_03] Assertion wrong')


class PageAdvancedOptionAdvanced(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_AOD_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advaced-option-advanced'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL Option advanced wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL Option advanced wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL Option advanced wrong: ' + driver.current_url)
        time.sleep(5)

        # If BLOQUEIO WAN is disable -> Enable it
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#wanLock')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=wanLock]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption['wanBlocking'])
            self.list_steps.append('[Pass] 3. Check value when enable Wan Blocking')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check value when enable Wan Blocking')
            list_steps_fail.append('3. Check value when enable Wan Blocking wrong')
            pass
        # Disable BLOQUEIO WAN
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#wanLock')
        if wan_lock == 'true':
            driver.find_element_by_css_selector('.radio-check[for=wanLock]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption2 = Helper.Helper_common.api_networkOption()
        try:
            self.assertFalse(api_networkOption2['wanBlocking'])
            self.list_steps.append('[Pass] 4. Check value when disable Wan Blocking')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value when disable Wan Blocking')
            list_steps_fail.append('4. Check value when disable Wan Blocking wrong')
            pass

        # Enable BLOQUEIO WAN
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#wanLock')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=wanLock]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption3 = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption3['wanBlocking'])
            self.list_steps.append('[Pass] 5. Check value when enable Wan Blocking')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check value when enable Wan Blocking')
            list_steps_fail.append('5. Check value when enable Wan Blocking wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_01] Assertion Block WAN fail')

    def test_UI_AOD_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advaced-option-advanced'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL Option advanced wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL Option advanced wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL Option advanced wrong: ' + driver.current_url)
        time.sleep(5)

        # If Ipsec Pass Through is disable -> Enable it
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#ipsecPassThrough')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=ipsecPassThrough]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption['ipsecPassthrough'])
            self.list_steps.append('[Pass] 3. Check value when enable Ipsec Pass Through')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check value when enable Ipsec Pass Through')
            list_steps_fail.append('3. Check value when enable Ipsec Pass Through wrong')
            pass

        # Disable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#ipsecPassThrough')
        if wan_lock == 'true':
            driver.find_element_by_css_selector('.radio-check[for=ipsecPassThrough]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption2 = Helper.Helper_common.api_networkOption()
        try:
            self.assertFalse(api_networkOption2['ipsecPassthrough'])
            self.list_steps.append('[Pass] 4. Check value when disable Ipsec Pass Through')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value when disable Ipsec Pass Through')
            list_steps_fail.append('4. Check value when disable Ipsec Pass Through wrong')
            pass

        # Enable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#ipsecPassThrough')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=ipsecPassThrough]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption3 = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption3['ipsecPassthrough'])
            self.list_steps.append('[Pass] 5. Check value when enable Ipsec Pass Through')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check value when enable Ipsec Pass Through')
            list_steps_fail.append('5. Check value when enable Ipsec Pass Through wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_02] Assertion Ipsec Pass Through fail')

    def test_UI_AOD_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advaced-option-advanced'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL Option advanced wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL Option advanced wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL Option advanced wrong: ' + driver.current_url)
        time.sleep(5)

        # If PPTP PASS THROUGH is disable -> Enable it
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#pptpPassThrough')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=pptpPassThrough]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption['pptpPassthrough'])
            self.list_steps.append('[Pass] 3. Check value when enable PPTP Pass Through')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check value when enable PPTP Pass Through')
            list_steps_fail.append('3. Check value when enable PPTP Pass Through wrong')
            pass

        # Disable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#pptpPassThrough')
        if wan_lock == 'true':
            driver.find_element_by_css_selector('.radio-check[for=pptpPassThrough]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption2 = Helper.Helper_common.api_networkOption()
        try:
            self.assertFalse(api_networkOption2['pptpPassthrough'])
            self.list_steps.append('[Pass] 4. Check value when disable PPTP Pass Through')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value when disable PPTP Pass Through')
            list_steps_fail.append('4. Check value when disable PPTP Pass Through wrong')
            pass

        # Enable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#pptpPassThrough')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=pptpPassThrough]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption3 = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption3['pptpPassthrough'])
            self.list_steps.append('[Pass] 5. Check value when enable PPTP Pass Through')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check value when enable PPTP Pass Through')
            list_steps_fail.append('5. Check value when enable PPTP Pass Through wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_03] Assertion PPTP Pass Through fail')

    def test_UI_AOD_04(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advaced-option-advanced'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL Option advanced wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL Option advanced wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL Option advanced wrong: ' + driver.current_url)
        time.sleep(5)

        # If GERENCIAMENTO DA CONFIGURAÇÃO REMOTA is disable -> Enable it
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#remoteConfigManagement')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=remoteConfigManagement]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption['remoteAccess']['active'])
            self.list_steps.append('[Pass] 3. Check value when enable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check value when enable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA')
            list_steps_fail.append('3. Check value when enable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA wrong')
            pass

        # Disable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#remoteConfigManagement')
        if wan_lock == 'true':
            driver.find_element_by_css_selector('.radio-check[for=remoteConfigManagement]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption2 = Helper.Helper_common.api_networkOption()
        try:
            self.assertFalse(api_networkOption2['remoteAccess']['active'])
            self.list_steps.append('[Pass] 4. Check value when disable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value when disable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA')
            list_steps_fail.append('4. Check value when disable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA wrong')
            pass

        # Enable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#remoteConfigManagement')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=remoteConfigManagement]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption3 = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption3['remoteAccess']['active'])
            self.list_steps.append('[Pass] 5. Check value when enable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check value when enable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA')
            list_steps_fail.append('5. Check value when enable GERENCIAMENTO DA CONFIGURAÇÃO REMOTA wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_04] Assertion Remote Access fail')

    def test_UI_AOD_05(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advaced-option-advanced'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL Option advanced wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL Option advanced wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL Option advanced wrong: ' + driver.current_url)
        time.sleep(5)

        # If MULTICAST ATIVAR is disable -> Enable it
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#multicastActive')
        if wan_lock != 'true':
            multicast = driver.find_element_by_css_selector('.radio-check[for=multicastActive]')
            ActionChains(driver).move_to_element(multicast).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption['multicast'])
            self.list_steps.append('[Pass] 3. Check value when enable MULTICAST ATIVAR')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check value when enable MULTICAST ATIVAR')
            list_steps_fail.append('3. Check value when enable MULTICAST ATIVAR wrong')
            pass

        # Disable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#multicastActive')
        if wan_lock == 'true':
            driver.find_element_by_css_selector('.radio-check[for=multicastActive]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption2 = Helper.Helper_common.api_networkOption()
        try:
            self.assertFalse(api_networkOption2['multicast'])
            self.list_steps.append('[Pass] 4. Check value when disable MULTICAST ATIVAR')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value when disable MULTICAST ATIVAR')
            list_steps_fail.append('4. Check value when disable MULTICAST ATIVAR wrong')
            pass

        # Enable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#multicastActive')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=multicastActive]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_networkOption3 = Helper.Helper_common.api_networkOption()
        try:
            self.assertTrue(api_networkOption3['multicast'])
            self.list_steps.append('[Pass] 5. Check value when enable MULTICAST ATIVAR')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check value when enable MULTICAST ATIVAR')
            list_steps_fail.append('5. Check value when enable MULTICAST ATIVAR')

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_05] Assertion MULTICAST ATIVAR fail')

    def test_UI_AOD_06(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-advaced-option-advanced'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL Option advanced wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL Option advanced wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL Option advanced wrong: ' + driver.current_url)
        time.sleep(5)

        # If UPNP ATIVAR is disable -> Enable it
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#upnpActive')
        if wan_lock != 'true':
            multicast = driver.find_element_by_css_selector('.radio-check[for=upnpActive]')
            ActionChains(driver).move_to_element(multicast).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_upnp = Helper.Helper_common.api_upnp()
        try:
            self.assertTrue(api_upnp['active'])
            self.list_steps.append('[Pass] 3. Check value when enable UPNP ATIVAR')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check value when enable UPNP ATIVAR')
            list_steps_fail.append('3. Check value when enable UPNP ATIVAR wrong')
            pass

        # Disable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#upnpActive')
        if wan_lock == 'true':
            driver.find_element_by_css_selector('.radio-check[for=upnpActive]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_upnp2 = Helper.Helper_common.api_upnp()
        try:
            self.assertFalse(api_upnp2['active'])
            self.list_steps.append('[Pass] 4. Check value when disable UPNP ATIVAR')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value when disable UPNP ATIVAR')
            list_steps_fail.append('4. Check value when disable UPNP ATIVAR wrong')
            pass

        # Enable
        wan_lock = Helper.Helper_common.check_radio_tick(driver, '#upnpActive')
        if wan_lock != 'true':
            driver.find_element_by_css_selector('.radio-check[for=upnpActive]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        api_upnp3 = Helper.Helper_common.api_upnp()
        try:
            self.assertTrue(api_upnp3['active'])
            self.list_steps.append('[Pass] 5. Check value when enable UPNP ATIVAR')
        except AssertionError:
            self.list_steps.append('[Fail] 5. Check value when enable UPNP ATIVAR')
            list_steps_fail.append('5. Check value when enable UPNP ATIVAR')

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_06] Assertion UPNP ATIVAR fail')

    def test_UI_AOD_07(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-advaced-option-advanced')
        expected_url = ipv4 + '/#page-advaced-option-advanced'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Advanced Option Advanced: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Advanced Option Advanced: ' + driver.current_url)
            list_steps_fail.append('2.URL page Advanced Option Advanced display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'option_advanced.js',
                    'srv_service.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'comparator.js',
                    'messagebox.js',
                    'networkOption',
                    'upnp',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Advanced Option Advanced page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Advanced Option Advanced page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Advanced Option Advanced page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_AOD_07] Assertion wrong')


class PageSecurityFirewallBasic(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SFB_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose Desligado
        driver.find_element_by_css_selector('.combo-box[name=ipv4]').click()
        driver.find_element_by_css_selector('.combo-box[name=ipv4]>option:nth-child(1)').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        # Check API IPv4 Firewall
        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        try:
            self.assertFalse(api_firewall['ipv4']['active'])
            self.assertFalse(api_ipv4_firewall['active'])
            self.list_steps.append('[Pass] 4. Check value of API of IPv4 Firewall "Desligado" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value of API of IPv4 Firewall "Desligado" ')
            list_steps_fail.append('4. Check value of API of IPv4 Firewall "Desligado" ')

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_01] Assertion Disable IPv4 firewall protection fail')

    def test_UI_SFB_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose Baixo
        driver.find_element_by_css_selector('.combo-box[name=ipv4]').click()
        driver.find_element_by_css_selector('.combo-box[name=ipv4]>option:nth-child(2)').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        actual_firewall = [api_firewall['ipv4']['active'], api_firewall['ipv4']['level']]
        expected_firewall = [True, 'low']
        try:
            self.assertListEqual(actual_firewall, expected_firewall)
            self.list_steps.append('[Pass] 4.1 Check value of API of Firewall "Baixo" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.1 Check value of API of Firewall "Baixo" ')
            list_steps_fail.append('4.1 Check value of API of Firewall "Baixo" ')
            pass

        # Check API IPv4 Firewall
        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        actual_ipv4_firewall = [api_ipv4_firewall['active'], api_ipv4_firewall['level']]
        expected_ipv4_firewall = [True, 'low']
        try:
            self.assertListEqual(actual_ipv4_firewall, expected_ipv4_firewall)
            self.list_steps.append('[Pass] 4.2 Check value of API of IPv4 Firewall "Baixo" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.2 Check value of API of IPv4 Firewall "Baixo" ')
            list_steps_fail.append('4.2 Check value of API of IPv4 Firewall "Baixo" ')

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_02] Assertion IPv4 firewall protection with low level fail')

    def test_UI_SFB_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose Medium
        driver.find_element_by_css_selector('.combo-box[name=ipv4]').click()
        driver.find_element_by_css_selector('.combo-box[name=ipv4]>option:nth-child(3)').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        actual_firewall = [api_firewall['ipv4']['active'], api_firewall['ipv4']['level']]
        expected_firewall = [True, 'medium']
        try:
            self.assertListEqual(actual_firewall, expected_firewall)
            self.list_steps.append('[Pass] 4.1 Check value of API of Firewall "Medium" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.1 Check value of API of Firewall "Medium" ')
            list_steps_fail.append('4.1 Check value of API of Firewall "Medium" ')
            pass

        # Check API IPv4 Firewall
        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        actual_ipv4_firewall = [api_ipv4_firewall['active'], api_ipv4_firewall['level']]
        expected_ipv4_firewall = [True, 'medium']
        try:
            self.assertListEqual(actual_ipv4_firewall, expected_ipv4_firewall)
            self.list_steps.append('[Pass] 4.2 Check value of API of IPv4 Firewall "Medium" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.2 Check value of API of IPv4 Firewall "Medium" ')
            list_steps_fail.append('4.2 Check value of API of IPv4 Firewall "Medium" ')
            pass

        # Check response of Rules -> Medium is not None
        actual_rules = api_ipv4_firewall['rules']['medium']
        try:
            self.assertNotEqual(len(actual_rules), 0)
            self.list_steps.append('[Pass] 4.3 Check Rule of Meidum API of IPv4 Firewall "Medium" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.3 Check Rule of Meidum API of IPv4 Firewall "Medium" ')
            list_steps_fail.append('4.3 Check Rule of Meidum API of IPv4 Firewall "Medium" ')

        self.assertListEqual(list_steps_fail, [],
                             '[UI_SFB_03] Assertion IPv4 firewall protection with medium level fail')

    def test_UI_SFB_04(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose High
        driver.find_element_by_css_selector('.combo-box[name=ipv4]').click()
        driver.find_element_by_css_selector('.combo-box[name=ipv4]>option:nth-child(4)').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(15)
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        actual_firewall = [api_firewall['ipv4']['active'], api_firewall['ipv4']['level']]
        expected_firewall = [True, 'high']
        try:
            self.assertListEqual(actual_firewall, expected_firewall)
            self.list_steps.append('[Pass] 4.1 Check value of API of Firewall "High" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.1 Check value of API of Firewall "High" ')
            list_steps_fail.append('4.1 Check value of API of Firewall "High" ')
            pass

        # Check API IPv4 Firewall
        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        actual_ipv4_firewall = [api_ipv4_firewall['active'], api_ipv4_firewall['level']]
        expected_ipv4_firewall = [True, 'high']
        try:
            self.assertListEqual(actual_ipv4_firewall, expected_ipv4_firewall)
            self.list_steps.append('[Pass] 4.2 Check value of API of IPv4 Firewall "High" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.2 Check value of API of IPv4 Firewall "High" ')
            list_steps_fail.append('4.2 Check value of API of IPv4 Firewall "High" ')
            pass

        # Check response of Rules -> High is not None
        actual_rules = api_ipv4_firewall['rules']['high']
        try:
            self.assertNotEqual(len(actual_rules), 0)
            self.list_steps.append('[Pass] 4.3 Check Rule of High API of IPv4 Firewall "High" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.3 Check Rule of High API of IPv4 Firewall "High" ')
            list_steps_fail.append('4.3 Check Rule of High API of IPv4 Firewall "High" ')

        self.assertListEqual(list_steps_fail, [],
                             '[UI_SFB_04] Assertion IPv4 firewall protection with High level fail')

    def test_UI_SFB_05(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose Desligado
        driver.find_element_by_css_selector('.combo-box[name=ipv6]').click()
        driver.find_element_by_css_selector('.combo-box[name=ipv6]>option:nth-child(1)').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        try:
            self.assertFalse(api_firewall['ipv6']['active'])
            self.list_steps.append('[Pass] 4. Check value of API of IPv6 Firewall "Desligado" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value of API of IPv6 Firewall "Desligado" ')
            list_steps_fail.append('4. Check value of API of IPv6 Firewall "Desligado" ')

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_05] Assertion Disable IPv6 firewall protection fail')

    def test_UI_SFB_06(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose Ligado
        driver.find_element_by_css_selector('.combo-box[name=ipv6]').click()
        driver.find_element_by_css_selector('.combo-box[name=ipv6]>option:nth-child(2)').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        try:
            self.assertTrue(api_firewall['ipv6']['active'])
            self.list_steps.append('[Pass] 4. Check value of API of IPv6 Firewall "Ligado" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check value of API of IPv6 Firewall "Ligado" ')
            list_steps_fail.append('4. Check value of API of IPv6 Firewall "Ligado" ')

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_06] Assertion Enable IPv6 firewall protection fail')

    def test_UI_SFB_07(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose BLOQUEAR PACOTES IP FRAGMENTADOS (check if it is not checked)
        fragmented_tick = Helper.Helper_common.check_radio_tick(driver, '#fragmentedIp')
        if fragmented_tick != 'true':
            driver.find_element_by_css_selector('.radio-check[for =fragmentedIp]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)

        checked = Helper.Helper_common.check_radio_tick(driver, '#fragmentedIp')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check Fragmentation is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check Fragmentation is checked or not ')
            list_steps_fail.append('3. Check Fragmentation fail: ' + str(checked))
            pass
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        try:
            self.assertFalse(api_firewall['ipv4']['blocks']['fragmentedIpPackets'])
            self.list_steps.append('[Pass] 4.1 Check value of API of Firewall "fragmentedIpPackets" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.1 Check value of API of Firewall "fragmentedIpPackets" ')
            list_steps_fail.append('4.1 Check value of API of Firewall "fragmentedIpPackets": '
                                   + str(api_firewall['ipv4']['blocks']['fragmentedIpPackets']))
            pass

        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        try:
            self.assertFalse(api_ipv4_firewall['blocks']['fragmentedIpPackets'])
            self.list_steps.append('[Pass] 4.2 Check value of API of IPv4 Firewall "fragmentedIpPackets" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.2 Check value of API of IPv4 Firewall "fragmentedIpPackets" ')
            list_steps_fail.append('4.2 Check value of API of IPv4 Firewall "fragmentedIpPackets": '
                                   + str(api_ipv4_firewall['blocks']['fragmentedIpPackets']))

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_07] Assertion Enable block fragmented IP packages fail')

    def test_UI_SFB_08(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose DETECÇÃO DE VARREDURA DE PORTAS (check if it is not checked)
        port_scan_tick = Helper.Helper_common.check_radio_tick(driver, '#portScanDetect')
        if port_scan_tick != 'true':
            driver.find_element_by_css_selector('.radio-check[for =portScanDetect]').click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)

        checked = Helper.Helper_common.check_radio_tick(driver, '#portScanDetect')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check Detect Port Scan is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check Detect Port Scan is checked or not ')
            list_steps_fail.append('3. Check Detect Port Scan fail: ' + str(checked))
            pass
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        try:
            self.assertTrue(api_firewall['ipv4']['blocks']['portScanDetection'])
            self.list_steps.append('[Pass] 4.1 Check value of API of Firewall "portScanDetection" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.1 Check value of API of Firewall "portScanDetection" ')
            list_steps_fail.append('4.1 Check value of API of Firewall "portScanDetection": '
                                   + str(api_firewall['ipv4']['blocks']['portScanDetection']))
            pass

        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        try:
            self.assertTrue(api_ipv4_firewall['blocks']['portScanDetection'])
            self.list_steps.append('[Pass] 4.2 Check value of API of IPv4 Firewall "portScanDetection" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.2 Check value of API of IPv4 Firewall "portScanDetection" ')
            list_steps_fail.append('4.2 Check value of API of IPv4 Firewall "portScanDetection": '
                                   + str(api_ipv4_firewall['blocks']['portScanDetection']))

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_08] Assertion Enable port scan detection fail')

    def test_UI_SFB_09(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-basic'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Protection wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose DETECÇÃO DE IP FLOOD (check if it is not checked)
        flood_tick = Helper.Helper_common.check_radio_tick(driver, '#ipFlood')
        if flood_tick != 'true':
            flood_ele = driver.find_element_by_css_selector('.radio-check[for =ipFlood]')
            ActionChains(driver).move_to_element(flood_ele).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)

        checked = Helper.Helper_common.check_radio_tick(driver, '#ipFlood')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check IP flood detection is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check IP flood detection is checked or not ')
            list_steps_fail.append('3. Check IP flood detection fail: ' + str(checked))
            pass
        # Check API Firewall
        api_firewall = Helper.Helper_common.api_firewall()
        try:
            self.assertTrue(api_firewall['ipv4']['blocks']['ipFlood'])
            self.list_steps.append('[Pass] 4.1 Check value of API of Firewall "ipFlood" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.1 Check value of API of Firewall "ipFlood" ')
            list_steps_fail.append('4.1 Check value of API of Firewall "ipFlood": '
                                   + str(api_firewall['ipv4']['blocks']['ipFlood']))
            pass

        api_ipv4_firewall = Helper.Helper_common.api_ipv4_firewall()
        try:
            self.assertTrue(api_ipv4_firewall['blocks']['ipFlood'])
            self.list_steps.append('[Pass] 4.2 Check value of API of IPv4 Firewall "ipFlood" ')
        except AssertionError:
            self.list_steps.append('[Fail] 4.2 Check value of API of IPv4 Firewall "ipFlood" ')
            list_steps_fail.append('4.2 Check value of API of IPv4 Firewall "ipFlood": '
                                   + str(api_ipv4_firewall['blocks']['ipFlood']))

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_08] Assertion Enable IP flood detection fail')

    def test_UI_SFB_10(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-firewall-basic')
        expected_url = ipv4 + '/#page-security-firewall-basic'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security Firewall Basic: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security Firewall Basic: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security Firewall Basic display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'main.js',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'firewall_basic.js',
                    'cmp_basic.js',
                    'cmp_combobox.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'srv_security.js',
                    'messagebox.js',
                    'comparator.js',
                    'firewall',
                    'ipv4',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security Firewall Basic page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security Firewall Basic page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security Firewall Basic page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SFB_10] Assertion wrong')


class PageSecurityFirewallRemoteLog(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SFR_01(self):
        self.driver.quit()
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./factory.py /SERIAL ''' + com + ''' /BAUD 115200''')
        # Wait for Restore 120s
        time.sleep(180)
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Log in
        Helper.Helper_common.check_login(driver, self, ipv4)
        time.sleep(3)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()

        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        time.sleep(10)
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 2. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('2. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 3. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('3. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)
        # Check API Firewall Alert
        api_alert = Helper.Helper_common.api_firewall_alert()
        actual_alter_values = [api_alert['option']['permittedConnections'],
                               api_alert['option']['blockedConnections'],
                               api_alert['option']['knownInternetAttacks'],
                               api_alert['option']['productConfigurationEvent']]
        expected_alter_values = [False, False, False, False]
        # Check API Service Log
        api_log = Helper.Helper_common.api_service_log()
        actual_log_values = [api_log['active'], api_log['mode']]
        expected_log_values = [True, 'local']
        try:
            self.assertListEqual(actual_alter_values, expected_alter_values)
            self.list_steps.append('\n[Pass] 4.1 Check API firewall alter:' + str(actual_alter_values))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check API firewall alter:' + str(actual_alter_values))
            list_steps_fail.append('4.1 API firewall alert wrong: ' + str(actual_alter_values))
            pass

        try:
            self.assertListEqual(actual_log_values, expected_log_values)
            self.list_steps.append('\n[Pass] 4.2 Check API Serivice log:' + str(actual_log_values))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.2 Check API Serivice log:' + str(actual_log_values))
            list_steps_fail.append('4.2 API Service Log wrong: ' + str(actual_log_values))
        self.assertListEqual(list_steps_fail, [], '[UI_SFR_01] Assertion Default remote log settings fail')

    def test_UI_SFR_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)

        # Input server IP address in "Para servidor SysLog em" textbox and Apply setting
        para_service = driver.find_element_by_css_selector('#para-servidor')
        para_service_value = '192.168.0.102'
        ActionChains(driver).move_to_element(para_service).double_click().send_keys(para_service_value).perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        api_log = Helper.Helper_common.api_service_log()
        actual_values = [api_log['active'], api_log['mode'], api_log['remote']['address'], api_log['remote']['port']]
        expected_dict = {"active": True,
                         "mode": "remote",
                         "remote": {
                             "address": "192.168.0.102",
                             "port": 514
                         }
                         }
        expected_values = [expected_dict['active'],
                           expected_dict['mode'],
                           expected_dict['remote']['address'],
                           expected_dict['remote']['port']]

        try:
            self.assertEqual(actual_values, expected_values)
            self.list_steps.append('[Pass] 4. Check API of Service Log ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check API of Service Log ')
            list_steps_fail.append('4. Check API of Service Log fail: ' + str(actual_values))

        self.assertListEqual(list_steps_fail, [], '[UI_SFR_02] Assertion Enable Remote Log fail')

    def test_UI_SFR_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose CONEXÕES PERMITIDAS (check if it is not checked)
        tick = Helper.Helper_common.check_radio_tick(driver, '#permittedConnection')
        if tick != 'true':
            tick_ele = driver.find_element_by_css_selector('.radio-check[for=permittedConnection]')
            ActionChains(driver).move_to_element(tick_ele).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        # 3. The button works normally and apply setting successfully
        checked = Helper.Helper_common.check_radio_tick(driver, '#permittedConnection')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check Permitted connection is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check Permitted connection is checked or not ')
            list_steps_fail.append('3. Check Permitted connection fail: ' + str(checked))
            pass
        # 4. Check the result
        api_alert = Helper.Helper_common.api_firewall_alert()
        try:
            self.assertTrue(api_alert['option']['permittedConnections'])
            self.list_steps.append('[Pass] 4. Check Permitted connection API ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check Permitted connection API ')
            list_steps_fail.append('4. Check API Permitted connection fail: '
                                   + str(api_alert['option']['permittedConnections']))

        self.assertListEqual(list_steps_fail, [], '[UI_SFR_03] Assertion Remote log with permitted connections fail')

    def test_UI_SFR_04(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose CONEXÕES BLOQUEADAS (check if it is not checked)
        tick = Helper.Helper_common.check_radio_tick(driver, '#blockedConnection')
        if tick != 'true':
            tick_ele = driver.find_element_by_css_selector('.radio-check[for=blockedConnection]')
            ActionChains(driver).move_to_element(tick_ele).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        # 3. The button works normally and apply setting successfully
        checked = Helper.Helper_common.check_radio_tick(driver, '#blockedConnection')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check Blocked connection is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check Blocked connection is checked or not ')
            list_steps_fail.append('3. Check Blocked connection fail: ' + str(checked))
            pass
        # 4. Check the result
        api_alert = Helper.Helper_common.api_firewall_alert()
        try:
            self.assertTrue(api_alert['option']['blockedConnections'])
            self.list_steps.append('[Pass] 4. Check Permitted connection API ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check Blocked connection API ')
            list_steps_fail.append('4. Check API Blocked connection fail: '
                                   + str(api_alert['option']['blockedConnections']))

        self.assertListEqual(list_steps_fail, [], '[UI_SFR_04] Assertion Remote log with blocked connections fail')

    def test_UI_SFR_05(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose ATAQUES CONHECIDOS DA INTERNET (check if it is not checked)
        tick = Helper.Helper_common.check_radio_tick(driver, '#knownInternetAttack')
        if tick != 'true':
            tick_ele = driver.find_element_by_css_selector('.radio-check[for=knownInternetAttack]')
            ActionChains(driver).move_to_element(tick_ele).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        # 3. The button works normally and apply setting successfully
        checked = Helper.Helper_common.check_radio_tick(driver, '#knownInternetAttack')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check Known Internet Attacks is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check Known Internet Attacks is checked or not ')
            list_steps_fail.append('3. Check Known Internet Attacks fail: ' + str(checked))
            pass
        # 4. Check the result
        api_alert = Helper.Helper_common.api_firewall_alert()
        try:
            self.assertTrue(api_alert['option']['knownInternetAttacks'])
            self.list_steps.append('[Pass] 4. Check Known Internet Attacks API ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check Known Internet Attacks API ')
            list_steps_fail.append('4. Check API Known Internet Attacks fail: '
                                   + str(api_alert['option']['knownInternetAttacks']))

        self.assertListEqual(list_steps_fail, [], '[UI_SFR_05] Assertion Remote log with known internet attacks fail')

    def test_UI_SFR_06(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)

        # Choose EVENTOS DE CONFIGURAÇÃO DE PRODUTOS(check if it is not checked)
        tick = Helper.Helper_common.check_radio_tick(driver, '#productConfigEvent')
        if tick != 'true':
            tick_ele = driver.find_element_by_css_selector('.radio-check[for=productConfigEvent]')
            ActionChains(driver).move_to_element(tick_ele).click().perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        # 3. The button works normally and apply setting successfully
        checked = Helper.Helper_common.check_radio_tick(driver, '#productConfigEvent')
        try:
            self.assertEqual(checked, 'true')
            self.list_steps.append('[Pass] 3. Check Product Configuration Event is checked or not ')
        except AssertionError:
            self.list_steps.append('[Fail] 3. Check Product Configuration Event is checked or not ')
            list_steps_fail.append('3. Check Product Configuration Event fail: ' + str(checked))
            pass
        # 4. Check the result
        api_alert = Helper.Helper_common.api_firewall_alert()
        try:
            self.assertTrue(api_alert['option']['productConfigurationEvent'])
            self.list_steps.append('[Pass] 4. Check Product Configuration Event API ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check Product Configuration Event API ')
            list_steps_fail.append('4. Check API Product Configuration Event fail: '
                                   + str(api_alert['option']['productConfigurationEvent']))

        self.assertListEqual(list_steps_fail, [],
                             '[UI_SFR_06] Assertion Remote log with product configuration event fail')

    def test_UI_SFR_07(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-firewall-remote-log'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL IPv4 Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2. URL IPv4 Firewall Remote Log wrong: ' + driver.current_url)
        time.sleep(5)

        # 3. Remove the existed server IP address in "Para servidor SysLog em" textbox and Apply setting
        para_service = driver.find_element_by_css_selector('#para-servidor')
        ActionChains(driver).move_to_element(para_service).double_click().send_keys(Keys.DELETE).perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        api_log = Helper.Helper_common.api_service_log()
        actual_values = [api_log['active'], api_log['mode']]
        expected_values = [True, 'local']
        try:
            self.assertEqual(actual_values, expected_values)
            self.list_steps.append('[Pass] 4. Check API of Service Log ')
        except AssertionError:
            self.list_steps.append('[Fail] 4. Check API of Service Log ')
            list_steps_fail.append('4. Check API of Service Log fail: ' + str(actual_values))

        self.assertListEqual(list_steps_fail, [], '[UI_SFR_07] Assertion Disable remote log fail')

    def test_UI_SFR_08(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-firewall-remote-log')
        expected_url = ipv4 + '/#page-security-firewall-remote-log'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security Firewall Remote Log: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security Firewall Remote Log: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security Firewall Remote Log display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'util.js',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'firewall_remote_log.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'srv_service.js',
                    'messagebox.js',
                    'srv_security.js',
                    'srv_network.js',
                    'comparator.js',
                    'alert',
                    'log',
                    'lan',
                    'about',
                    'menu_main.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security Firewall Remote Log page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security Firewall Remote Log page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security Firewall Remote Log page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SFR_08] Assertion wrong')


class PageSecurityIPFiltering(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SIF_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-ip-filtering'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity IP Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity IP Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity IP Filtering wrong: ' + driver.current_url)

        # Delete all rules
        Helper.Helper_common.api_service_port_ip_delete_all()
        time.sleep(3)
        for times in range(0, 10):
            time.sleep(2)
            # Address
            address_ele = driver.find_elements_by_css_selector('.ipv4 >div')
            address_value = ('192.168.0.' + str(random.randint(1, 255)))
            list_address_value = address_value.split('.')
            for i in range(len(address_ele)):
                ActionChains(driver).move_to_element(address_ele[i]).click().send_keys(list_address_value[i]).perform()
            # Protocol
            driver.find_element_by_css_selector('.select-item').click()
            protocol = driver.find_element_by_css_selector(
                '.combo-box>option:nth-child(' + str(random.randint(1, 3)) + ')')
            time.sleep(1)
            protocol.click()
            # Click Apply
            apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            time.sleep(10)
            api_port = Helper.Helper_common.api_service_port_ip()
            actual = [api_port['rules'][times]['active'],
                      api_port['rules'][times]['ipAddress'],
                      api_port['rules'][times]['protocol']]
            protocol_value = protocol.get_attribute('value')
            expected = [True, address_value, protocol_value]
            try:
                self.assertListEqual(actual, expected)
                self.list_steps.append('[Pass] 4.' + str(times) + ' Check API of Port IP Filtering ')
            except AssertionError:
                self.list_steps.append('[Fail] 4.' + str(times) + ' Check API of Port IP Filtering ')
                list_steps_fail.append('4.' + str(times) + ' Check API of Port IP Filtering fail: ' + str(actual))
                pass
        # One more time
        # Address
        address_ele = driver.find_elements_by_css_selector('.ipv4 >div')
        address_value = '192.168.0.199'
        list_address_value = address_value.split('.')
        for i in range(len(address_ele)):
            ActionChains(driver).move_to_element(address_ele[i]).click().send_keys(
                list_address_value[i]).perform()
        # Protocol
        driver.find_element_by_css_selector('.select-item').click()
        protocol = driver.find_element_by_css_selector('.combo-box>option:nth-child(3)')
        protocol.click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        check_error = driver.find_elements_by_css_selector('.f-row.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('5. [Pass] Check input values')
        except AssertionError:
            self.list_steps.append('5. [Fail] Check input values')
            list_steps_fail.append('5. Check input values wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_SIF_01] Assertion Add new IP filter rules fail')

    def test_UI_SIF_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-ip-filtering'
        driver.get(expected_url_target)
        time.sleep(3)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity IP Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity IP Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity IP Filtering wrong: ' + driver.current_url)
        rules = driver.find_elements_by_css_selector('.radio-check')
        for rule in rules:
            time.sleep(1)
            ActionChains(driver).move_to_element(rule).click().perform()
            tick = Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler')
            try:
                self.assertEqual(tick, 'true')
                self.list_steps.append('[Pass] 3. Check radio box ticked: ' + tick)
            except AssertionError:
                self.list_steps.append('[Fail] 3. Check radio box ticked: ' + tick)
                list_steps_fail.append('3. Check radio box ticked: ' + tick)
                pass
        time.sleep(2)
        remover_btn = driver.find_element_by_css_selector('button#remover')
        ActionChains(driver).move_to_element(remover_btn).click().perform()
        time.sleep(5)
        api_port = Helper.Helper_common.api_service_port_ip()
        try:
            self.assertNotIn('rules', list(api_port.keys()))
            self.list_steps.append('\n[Pass] 4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))
            list_steps_fail.append('4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))

        self.assertListEqual(list_steps_fail, [], '[UI_SIF_02] Assertion Remove all existed IP filter rules fail')

    def test_UI_SIF_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-ip-filtering'
        driver.get(expected_url_target)
        time.sleep(3)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity IP Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity IP Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity IP Filtering wrong: ' + driver.current_url)

        # Address
        address_ele = driver.find_elements_by_css_selector('.ipv4 >div')
        address_value = '192.168.0.1'
        list_address_value = address_value.split('.')
        for i in range(len(address_ele)):
            ActionChains(driver).move_to_element(address_ele[i]).click().send_keys(
                list_address_value[i]).perform()
        # Protocol
        driver.find_element_by_css_selector('.select-item').click()
        protocol = driver.find_element_by_css_selector('.combo-box>option:nth-child(' + str(random.randint(1, 3)) + ')')
        time.sleep(1)
        protocol.click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        check_error = driver.find_elements_by_css_selector('.f-row.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('3. [Pass] Check red error of gatewayIP red error of gatewayIP')
        except AssertionError:
            self.list_steps.append('3. [Fail] Check red error of gatewayIP red error of gatewayIP')
            list_steps_fail.append('3. Check red error of gatewayIP red error of gatewayIP wrong')
        self.assertListEqual(list_steps_fail, [], '[UI_SIF_03] Assertion Add new IP filter rule with gateway IP fail')

    def test_UI_SIF_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-ip-filtering')
        expected_url = ipv4 + '/#page-security-ip-filtering'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security IP Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security IP Filtering: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security IP Filtering display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'util.js',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'ip_filtering.js',
                    'cmp_basic.js',
                    'cmp_ipinput.js',
                    'cmp_form.js',
                    'cmp_combobox.js',
                    'messagebox.js',
                    'srv_network.js',
                    'srv_service.js',
                    'cmp_headresult.js',
                    'lan',
                    'portIpFiltering',
                    'aboutc',
                    'menu_main.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security IP Filtering page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security IP Filtering page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security IP Filtering page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SIF_04] Assertion wrong')


class PageSecurityMACFiltering(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SMF_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-mac-filtering'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity MAC Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity MAC Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity MAC Filtering wrong: ' + driver.current_url)

        # Delete all rules
        Helper.Helper_common.api_service_macfiltering_delete_all()
        time.sleep(3)
        for times in range(1, 21):
            # Address
            mac_ele = driver.find_element_by_css_selector('#macInput')
            mac_value = '01:23:45:67:89:' + str("{:02d}".format(times))
            ActionChains(driver).move_to_element(mac_ele).click().send_keys(mac_value).perform()
            # Click Apply
            apply_btn = driver.find_element_by_css_selector('button[value="addMac"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            time.sleep(0.5)
            api_port = Helper.Helper_common.api_service_mac_filtering()
            actual = [api_port['rules'][times - 1]['active'],
                      api_port['rules'][times - 1]['macAddress']]

            expected = [True, mac_value]
            try:
                self.assertListEqual(actual, expected)
                self.list_steps.append('[Pass] 4.' + str(times) + ' Check API of MAC Filtering ')
            except AssertionError:
                self.list_steps.append('[Fail] 4.' + str(times) + ' Check API of MAC Filtering ')
                list_steps_fail.append('4.' + str(times) + ' Check API of MAC Filtering fail: ' + str(actual))
                pass
        # One more time
        mac_ele = driver.find_element_by_css_selector('#macInput')
        mac_value = '01:23:45:67:89:' + str("{:02d}".format(times))
        ActionChains(driver).move_to_element(mac_ele).click().send_keys(mac_value).perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="addMac"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(5)
        check_error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('5. [Pass] Check the red error')
        except AssertionError:
            self.list_steps.append('5. [Fail] Check the red error')
            list_steps_fail.append('5. The red error displayed wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_SMF_01] Assertion Add new MAC filter rules fail')

    def test_UI_SMF_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-mac-filtering'
        driver.get(expected_url_target)
        time.sleep(3)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity MAC Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity MAC Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity MAC Filtering wrong: ' + driver.current_url)
        rules = driver.find_elements_by_css_selector('.radio-check')
        for rule in rules:
            time.sleep(1)
            ActionChains(driver).move_to_element(rule).click().perform()
            tick = Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler')
            try:
                self.assertEqual(tick, 'true')
                self.list_steps.append('[Pass] 3. Check radio box ticked: ' + tick)
            except AssertionError:
                self.list_steps.append('[Fail] 3. Check radio box ticked: ' + tick)
                list_steps_fail.append('3. Check radio box ticked: ' + tick)
                pass
        time.sleep(2)
        remover_btn = driver.find_element_by_css_selector('button#remover')
        ActionChains(driver).move_to_element(remover_btn).click().perform()
        time.sleep(5)
        api_port = Helper.Helper_common.api_service_port_ip()
        try:
            self.assertNotIn('rules', list(api_port.keys()))
            self.list_steps.append('\n[Pass] 4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))
            list_steps_fail.append('4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))

        self.assertListEqual(list_steps_fail, [], '[UI_SMF_02] Assertion Remove all existed MAC filter rules fail')

    def test_UI_SMF_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-mac-filtering')
        expected_url = ipv4 + '/#page-security-mac-filtering'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security MAC Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security MAC Filtering: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security MAC Filtering display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'mac_filtering.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'messagebox.js',
                    'srv_service.js',
                    'cmp_headresult.js',
                    'macFiltering',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security MAC Filtering page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security MAC Filtering page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security MAC Filtering page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SMF_03] Assertion wrong')


class PageSecurityPortFiltering(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SPF_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-port-filtering'
        driver.get(expected_url_target)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity Port Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity Port Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity Port Filtering wrong: ' + driver.current_url)

        # Delete all rules
        Helper.Helper_common.api_service_portfiltering_delete_all()
        time.sleep(3)
        start_port_value = 1
        end_port_value = 2
        for times in range(1, 21):
            # Start Port
            start_port_ele = driver.find_element_by_css_selector('#start-port-number')
            start_port_value += 2
            ActionChains(driver).move_to_element(start_port_ele).click().send_keys(start_port_value).perform()

            # Final Port
            end_port_ele = driver.find_element_by_css_selector('#end-port-number')
            end_port_value += 2
            ActionChains(driver).move_to_element(end_port_ele).click().send_keys(end_port_value).perform()

            # Protocol
            driver.find_element_by_css_selector('.select-item').click()
            protocol = driver.find_element_by_css_selector(
                '.combo-box>option:nth-child(' + str(random.randint(1, 3)) + ')')
            protocol.click()

            # Click Apply
            apply_btn = driver.find_element_by_css_selector('button[value="addItem"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            time.sleep(1)
            api_port = Helper.Helper_common.api_service_port_filtering()
            actual = [api_port['rules'][times - 1]['active'],
                      api_port['rules'][times - 1]['startPort'],
                      api_port['rules'][times - 1]['endPort'],
                      api_port['rules'][times - 1]['protocol']]
            protocol_value = protocol.get_attribute('value')
            expected = [True, start_port_value, end_port_value, protocol_value]
            time.sleep(2)
            try:
                self.assertListEqual(actual, expected)
                self.list_steps.append('[Pass] 4.' + str(times) + ' Check API of Port Filtering ')
            except AssertionError:
                self.list_steps.append('[Fail] 4.' + str(times) + ' Check API of Port Filtering ')
                list_steps_fail.append('4.' + str(times) + ' Check API of Port Filtering fail: ' + str(actual))
                pass
        # One more time
        # Start Port
        start_port_ele = driver.find_element_by_css_selector('#start-port-number')
        start_port_value = 50
        ActionChains(driver).move_to_element(start_port_ele).click().send_keys(start_port_value).perform()
        # Final Port
        end_port_ele = driver.find_element_by_css_selector('#end-port-number')
        end_port_value = 51
        ActionChains(driver).move_to_element(end_port_ele).click().send_keys(end_port_value).perform()
        # Protocol
        driver.find_element_by_css_selector('.select-item').click()
        protocol = driver.find_element_by_css_selector('.combo-box>option:nth-child(3)')
        protocol.click()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="addItem"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        check_error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('5. [Pass] Check the red error')
        except AssertionError:
            self.list_steps.append('5. [Fail] Check the red error')
            list_steps_fail.append('5. The red error displayed wrong')

        self.assertListEqual(list_steps_fail, [], '[UI_SPF_01] Assertion Add new PORT filter rules fail')

    def test_UI_SPF_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        expected_url_target = ipv4 + '/#page-security-port-filtering'
        driver.get(expected_url_target)
        time.sleep(3)
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2. Check URL Sercurity Port Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check URL Sercurity Port Filtering: ' + driver.current_url)
            list_steps_fail.append('2. URL Sercurity Port Filtering wrong: ' + driver.current_url)
        rules = driver.find_elements_by_css_selector('.radio-check')
        for rule in rules:
            time.sleep(1)
            ActionChains(driver).move_to_element(rule).click().perform()
            tick = Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler')
            try:
                self.assertEqual(tick, 'true')
                self.list_steps.append('[Pass] 3. Check radio box ticked: ' + tick)
            except AssertionError:
                self.list_steps.append('[Fail] 3. Check radio box ticked: ' + tick)
                list_steps_fail.append('3. Check radio box ticked: ' + tick)
                pass
        time.sleep(2)
        remover_btn = driver.find_element_by_css_selector('button#remover')
        ActionChains(driver).move_to_element(remover_btn).click().perform()
        time.sleep(5)
        api_port = Helper.Helper_common.api_service_port_ip()
        try:
            self.assertNotIn('rules', list(api_port.keys()))
            self.list_steps.append('\n[Pass] 4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))
            list_steps_fail.append('4. Check "rules" key is not in api return: ' + str(list(api_port.keys())))

        self.assertListEqual(list_steps_fail, [], '[UI_SPF_02] Assertion Remove all existed Port filter rules fail')

    def test_UI_SPF_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-port-filtering')
        expected_url = ipv4 + '/#page-security-port-filtering'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security Port Filtering: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security Port Filtering: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security Port Filtering display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'port_filtering.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_combobox.js',
                    'messagebox.js',
                    'srv_service.js',
                    'cmp_headresult.js',
                    'portFiltering',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security Port Filtering page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security Port Filtering page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security Port Filtering page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SPF_03] Assertion wrong')


class PageAdvancedPortForwarding(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_APF_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-advanced-port-forwarding')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-advanced-port-forwarding')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # Step 3: Click "Criar" to add new setting
        try:
            driver.find_element_by_css_selector('.holder-icon .toggle').click()
            self.list_steps.append('\n[Pass] 3. Click the "Criar" successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. Can't Click the 'Criar'")
            self.list_steps_fail.append("2. Can't Click the 'Criar'")

        time.sleep(1)
        # Step 4:
        try:
            driver.find_element_by_class_name('radio-check').click()
            driver.find_element_by_id('service-select').click()
            driver.find_element_by_css_selector('#service-select > option:nth-of-type(2)').click()
            driver.find_element_by_css_selector('#ip-address').clear()
            driver.find_element_by_css_selector('#ip-address').send_keys('192.168.0.5')
            driver.find_element_by_id('apply').click()
            self.list_steps.append('\n[Pass] 4. Change the setting successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. Fail to change the setting")
            self.list_steps_fail.append("4. Fail to change the setting")
        time.sleep(2)

        # Step 5: Verify the information
        api_portForwarding = Helper.Helper_common.api_portForWarding()
        actual_portForwarding = driver.find_elements_by_css_selector('ul.list')
        try:
            for i in range(len(api_portForwarding['rules'])):
                actual_info = str(actual_portForwarding[i].text).split('\n')
                actual_name_service = actual_info[0].replace('Nome do Serviço:', '').strip()
                actual_ip = actual_info[1].replace('IP:', '').strip()
                actual_portExternal_start = actual_info[2].replace('Porta externa inicial:', '').strip()
                actual_portExternal_end = actual_info[3].replace('Porta externa final:', '').strip()
                actual_protocol = actual_info[4].replace('Protocolo:', '').strip()
                actual_portInternal_start = actual_info[5].replace('Porta inicial interna:', '').strip()
                actual_portInternal_end = actual_info[6].replace('Porta final interna: ', '').strip()

                self.assertEqual(actual_name_service, api_portForwarding['rules'][i]['serviceType'])
                self.assertEqual(actual_ip, api_portForwarding['rules'][i]['ipAddress'])
                self.assertEqual(actual_portExternal_start.strip(),
                                 str(api_portForwarding['rules'][i]['externalPort']['start']))
                self.assertEqual(actual_portExternal_end.strip(),
                                 str(api_portForwarding['rules'][i]['externalPort']['end']))
                self.assertEqual(actual_protocol.strip(), str(api_portForwarding['rules'][i]['protocol']).upper())
                self.assertEqual(actual_portInternal_start.strip(),
                                 str(api_portForwarding['rules'][i]['localPort']['start']))
                self.assertEqual(actual_portInternal_end.strip(),
                                 str(api_portForwarding['rules'][i]['localPort']['end']))
            self.list_steps.append('\n[Pass] 5. Value is same as response from API')
        except AssertionError:
            self.list_steps.append("\n[Fail] 5. Values displayed aren't same as response from API")
            self.list_steps_fail.append("5. Values displayed aren't same as response from API")

        # remove all config
        list_checkbox = driver.find_elements_by_class_name('radio-check')
        for i in list_checkbox:
            ActionChains(driver).move_to_element(i).click().perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element_by_id('remove')).click().perform()
        time.sleep(1)
        driver.find_element_by_id('ok').click()

    def test_UI_APF_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-advanced-port-forwarding')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-advanced-port-forwarding')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(3)
        # Step 3: Click "Criar" to add new setting
        try:
            driver.find_element_by_css_selector('.holder-icon .toggle').click()
            self.list_steps.append('\n[Pass] 3. Click the "Criar" successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. Can't Click the 'Criar'")
            self.list_steps_fail.append("2. Can't Click the 'Criar'")

        time.sleep(1)
        # Step 4
        try:
            driver.find_element_by_id('service-set').send_keys('abc')
            driver.find_element_by_css_selector('#ip-address').clear()
            driver.find_element_by_css_selector('#ip-address').send_keys('192.168.0.3')
            for i in range(12):
                driver.find_elements_by_css_selector('.input.ex-start')[i].send_keys(str(i + 1))
                driver.find_elements_by_css_selector('.input.ex-end')[i].send_keys(str(i + 1))
            driver.find_element_by_id('apply').click()
            self.list_steps.append('\n[Pass] 4. Change the setting successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. Fail to change the setting")
            self.list_steps_fail.append("4. Fail to change the setting")
        time.sleep(30)

        # Step 5
        driver.find_element_by_css_selector('.holder-icon .toggle').click()
        time.sleep(1)

        # Step 6
        driver.find_element_by_id('service-set').send_keys('abc')
        driver.find_element_by_css_selector('#ip-address').clear()
        driver.find_element_by_css_selector('#ip-address').send_keys('192.168.0.3')
        for i in range(12):
            driver.find_elements_by_css_selector('.input.ex-start')[i].send_keys(str(i + 13))
            driver.find_elements_by_css_selector('.input.ex-end')[i].send_keys(str(i + 13))
        driver.find_element_by_css_selector('#protocol0').send_keys('UDP')
        driver.find_element_by_id('apply').click()
        time.sleep(30)

        # Step 7
        driver.find_element_by_css_selector('.holder-icon .toggle').click()
        time.sleep(1)

        # Step 8
        driver.find_element_by_id('service-set').send_keys('abc')
        driver.find_element_by_css_selector('#ip-address').clear()
        driver.find_element_by_css_selector('#ip-address').send_keys('192.168.0.3')
        for i in range(8):
            driver.find_elements_by_css_selector('.input.ex-start')[i].send_keys(str(i + 25))
            driver.find_elements_by_css_selector('.input.ex-end')[i].send_keys(str(i + 25))
        driver.find_element_by_css_selector('#protocol0').send_keys('AMBOS')
        driver.find_element_by_id('apply').click()
        time.sleep(30)

        # Step 9:
        driver.find_element_by_css_selector('.holder-icon .toggle').click()
        time.sleep(1)

        # Step 10
        driver.find_element_by_id('service-set').send_keys('abc')
        driver.find_element_by_css_selector('#ip-address').clear()
        driver.find_element_by_css_selector('#ip-address').send_keys('192.168.0.3')
        driver.find_element_by_css_selector('.input.ex-start').send_keys('33')
        driver.find_element_by_css_selector('.input.ex-end').send_keys('33')
        driver.find_element_by_css_selector('#protocol0').send_keys(random.choice(['AMBOS', 'UDP', 'TCP']))
        driver.find_element_by_id('apply').click()

        border_color = driver.find_element_by_css_selector('.input.ex-start').value_of_css_property('border-color')
        self.assertEqual('rgb(182, 33, 33)', border_color)

        driver.refresh()
        time.sleep(30)
        # remove all config
        list_checkbox = driver.find_elements_by_class_name('radio-check')
        for i in list_checkbox:
            ActionChains(driver).move_to_element(i).click().perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element_by_id('remove')).click().perform()
        time.sleep(1)
        driver.find_element_by_id('ok').click()
        time.sleep(5)

    def test_UI_APF_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-advanced-port-forwarding')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-advanced-port-forwarding')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # Pre Step 3: Click "Criar" to add new setting

        driver.find_element_by_css_selector('.holder-icon .toggle').click()
        time.sleep(1)

        driver.find_element_by_class_name('radio-check').click()
        driver.find_element_by_id('service-select').click()
        driver.find_element_by_css_selector('#service-select > option:nth-of-type(2)').click()
        driver.find_element_by_css_selector('#ip-address').clear()
        driver.find_element_by_css_selector('#ip-address').send_keys('192.168.0.5')
        driver.find_element_by_id('apply').click()
        time.sleep(2)

        # Step 3:
        list_checkbox = driver.find_elements_by_class_name('radio-check')
        try:
            for i in list_checkbox:
                ActionChains(driver).move_to_element(i).click().perform()
            self.list_steps.append('\n[Pass] 3. The checkbox works normally')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. The checkbox works abnormally")
            self.list_steps_fail.append("3. The checkbox works abnormally")
        time.sleep(1)

        # Step 4:
        ActionChains(driver).move_to_element(driver.find_element_by_id('remove')).click().perform()
        time.sleep(1)
        try:
            driver.find_element_by_id('ok').click()
            self.list_steps.append('\n[Pass] 4. The pop-up is displayed')
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. The pop-up is not displayed")
            self.list_steps_fail.append("4. The pop-up is not displayed")
        time.sleep(2)

        # Step 5:
        list_config = len(driver.find_elements_by_css_selector('ul.list'))
        try:
            self.assertEqual(list_config, 0)
        except AssertionError:
            self.list_steps.append("\n[Fail] 5.List config isn't empty")
            self.list_steps_fail.append("5.List config isn't empty")

    def test_UI_APF_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-advanced-port-forwarding')
        expected_url = ipv4 + '/#page-advanced-port-forwarding'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Advanced Port Forwarding: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Advanced Port Forwarding: ' + driver.current_url)
            list_steps_fail.append('2.URL page Advanced Port Forwarding display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'util.js',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'port_forwarding.js',
                    'srv_service.js',
                    'srv_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'messagebox.js',
                    'listApps.json',
                    'portForwarding',
                    'about',
                    'menu_main.js',
                    'lan',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Advanced Port Forwarding page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Advanced Port Forwarding page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append('3. API return on Advanced Port Forwarding page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_APF_04] Assertion wrong')


class PageAdvancedPortTrigger(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_APT_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-advanced-port-trigger')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-advanced-port-trigger')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # Step 3: Click "Criar" to add new setting
        try:
            driver.find_element_by_css_selector('.holder-icon .toggle').click()
            self.list_steps.append('\n[Pass] 3. Click the "Criar" successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. Can't Click the 'Criar'")
            self.list_steps_fail.append("2. Can't Click the 'Criar'")

        time.sleep(1)
        # Step 4:
        try:
            driver.find_element_by_class_name('radio-check').click()
            driver.find_element_by_id('application-select').click()
            driver.find_element_by_css_selector('#application-select> option:nth-of-type(4)').click()
            time.sleep(1)
            driver.find_element_by_id('apply').click()
            self.list_steps.append('\n[Pass] 4. Change the setting successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. Fail to change the setting")
            self.list_steps_fail.append("4. Fail to change the setting")
        time.sleep(2)

        # Step 5: Verify the information
        api_portTriggering = Helper.Helper_common.api_portTriggering()
        actual_portTriggering = driver.find_elements_by_css_selector('ul.list')
        try:
            for i in range(len(api_portTriggering['rules'])):
                actual_info = str(actual_portTriggering[i].text).split('\n')
                actual_name_service = actual_info[0].replace('Nome da Aplicação:', '').strip()
                actual_triggered_port_start = actual_info[1].replace('Gatilho Porta Inicial:', '').strip()
                actual_triggered_port_end = actual_info[2].replace('Gatilo Porta Final:', '').strip()
                actual_triggered_protocol = actual_info[3].replace('Gatilho Protocolo:', '').strip()

                actual_forwarded_port_start = actual_info[4].replace('Alvo Porta Inicial:', '').strip()
                actual_forwarded_port_end = actual_info[5].replace('Alvo Porta Final:', '').strip()
                actual_forwarded_protocol = actual_info[6].replace('Gatilho Protocolo:', '').strip()

                self.assertEqual(actual_name_service, str(api_portTriggering['rules'][i]['description']))
                self.assertEqual(actual_triggered_port_start,
                                 str(api_portTriggering['rules'][i]['triggered']['startRange']))
                self.assertEqual(actual_triggered_port_end.strip(),
                                 str(api_portTriggering['rules'][i]['triggered']['endRange']))
                self.assertEqual(actual_triggered_protocol.strip(),
                                 str(api_portTriggering['rules'][i]['triggered']['protocol']).upper())
                self.assertEqual(actual_forwarded_port_start.strip(),
                                 str(api_portTriggering['rules'][i]['forwarded']['startRange']))
                self.assertEqual(actual_forwarded_port_end.strip(),
                                 str(api_portTriggering['rules'][i]['forwarded']['endRange']))
                self.assertEqual(actual_forwarded_protocol.strip(),
                                 str(api_portTriggering['rules'][i]['forwarded']['protocol']).upper())
            self.list_steps.append('\n[Pass] 5. Value is same as response from API')
        except AssertionError:
            self.list_steps.append("\n[Fail] 5. Values displayed aren't same as response from API")
            self.list_steps_fail.append("5. Values displayed aren't same as response from API")

        # remove all config
        list_checkbox = driver.find_elements_by_class_name('radio-check')
        for i in list_checkbox:
            ActionChains(driver).move_to_element(i).click().perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element_by_id('remove')).click().perform()
        time.sleep(1)
        driver.find_element_by_id('ok').click()

    def test_UI_APT_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-advanced-port-trigger')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-advanced-port-trigger')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # # Step 3: Click "Criar" to add new setting
        # try:
        #     driver.find_element_by_css_selector('.holder-icon .toggle').click()
        #     self.list_steps.append('\n[Pass] 3. Click the "Criar" successfully')
        # except AssertionError:
        #     self.list_steps.append("\n[Fail] 3. Can't Click the 'Criar'")
        #     self.list_steps_fail.append("2. Can't Click the 'Criar'")

        # time.sleep(1)
        # Step 4:
        try:
            # driver.find_element_by_class_name('radio-check').click()
            # driver.find_element_by_id('application-set').send_keys('abc')

            for i in range(8):
                driver.find_element_by_css_selector('.holder-icon .toggle').click()
                time.sleep(1)
                driver.find_element_by_id('application-set').send_keys('abc')
                time.sleep(1)
                for row in range(4):
                    if (i * 4 + row + 1) == 21:
                        continue
                    driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[0].send_keys(
                        str(i * 4 + row + 1))
                    driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[1].send_keys(
                        str(i * 4 + row + 1))
                    driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[2].send_keys(
                        str(i * 4 + row + 1))
                    driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[3].send_keys(
                        str(i * 4 + row + 1))
                driver.find_element_by_id('apply').click()
                pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
                while len(pop_up_wait) == 1:
                    pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
                    time.sleep(1)

            self.list_steps.append('\n[Pass] 4. Change the setting successfully')
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. Fail to change the setting")
            self.list_steps_fail.append("4. Fail to change the setting")
        time.sleep(2)

        # add value #33, #34
        driver.find_element_by_css_selector('.holder-icon .toggle').click()
        time.sleep(1)
        driver.find_element_by_id('application-set').send_keys('abc')
        time.sleep(1)
        for row in range(2):
            driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[0].send_keys(
                str(row + 33))
            driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[1].send_keys(
                str(row + 33))
            driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[2].send_keys(
                str(row + 33))
            driver.find_elements_by_xpath('//tr[' + str(row + 1) + ']//td//input')[3].send_keys(
                str(row + 33))
        driver.find_element_by_id('apply').click()

        border_color = driver.find_element_by_xpath('//tr[2]//td//input').value_of_css_property('border-color')
        self.assertEqual('rgb(182, 33, 33)', border_color)

        # remove all config
        list_checkbox = driver.find_elements_by_class_name('radio-check')
        for i in list_checkbox:
            ActionChains(driver).move_to_element(i).click().perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element_by_id('remove')).click().perform()
        time.sleep(3)
        driver.find_element_by_id('ok').click()
        list_config = len(driver.find_elements_by_css_selector('ul.list'))
        while list_config != 0:
            time.sleep(0.5)
            list_config = len(driver.find_elements_by_css_selector('ul.list'))

    def test_UI_APT_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-advanced-port-trigger')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-advanced-port-trigger')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # Pre Step 3: Click "Criar" to add new setting
        driver.find_element_by_css_selector('.holder-icon .toggle').click()
        time.sleep(1)
        driver.find_element_by_class_name('radio-check').click()
        driver.find_element_by_id('application-select').click()
        driver.find_element_by_css_selector('#application-select> option:nth-of-type(4)').click()
        time.sleep(1)
        driver.find_element_by_id('apply').click()

        time.sleep(2)

        # Step 3:
        list_checkbox = driver.find_elements_by_class_name('radio-check')
        try:
            for i in list_checkbox:
                ActionChains(driver).move_to_element(i).click().perform()
            self.list_steps.append('\n[Pass] 3. The checkbox works normally')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. The checkbox works abnormally")
            self.list_steps_fail.append("3. The checkbox works abnormally")
        time.sleep(1)

        # Step 4:
        ActionChains(driver).move_to_element(driver.find_element_by_id('remove')).click().perform()
        time.sleep(1)
        try:
            driver.find_element_by_id('ok').click()
            self.list_steps.append('\n[Pass] 4. The pop-up is displayed')
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. The pop-up is not displayed")
            self.list_steps_fail.append("4. The pop-up is not displayed")
        time.sleep(2)

        # Step 5:
        list_config = len(driver.find_elements_by_css_selector('ul.list'))
        try:
            self.assertEqual(list_config, 0)
        except AssertionError:
            self.list_steps.append("\n[Fail] 5.List config isn't empty")
            self.list_steps_fail.append("5.List config isn't empty")

    def test_UI_APT_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-advanced-port-trigger')
        expected_url = ipv4 + '/#page-advanced-port-trigger'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Advanced Port Trigger: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Advanced Port Trigger: ' + driver.current_url)
            list_steps_fail.append('2.URL page Advanced Port Trigger display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'port_trigger.js',
                    'srv_service.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'messagebox.js',
                    'cmp_headresult.js',
                    'portTriggering',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Advanced Port Trigger page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Advanced Port Trigger page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Advanced Port Trigger page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_APT_04] Assertion wrong')


class PageSecurityAccessByWifi(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SAB_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-security-access-bywifi')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-security-access-bywifi')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # Step 3: Click "LIGADO" to enable wifi
        try:
            driver.find_element_by_css_selector('.custom-radio[for="accessOn"]').click()
            driver.find_element_by_css_selector('.holder-icon').click()
            self.list_steps.append('\n[Pass] 3. The button work normally')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. Can't Click the 'LIGADO'")
            self.list_steps_fail.append("2. Can't Click the 'LIGADO'")

        time.sleep(1)

        # Step 4: Verify the information
        api_portTriggering = Helper.Helper_common.api_accessADM()
        try:
            self.assertEqual(api_portTriggering['accessADM'], True)
            self.list_steps.append('\n[Pass] 4. accessADM: ' + str(api_portTriggering['accessADM']))
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. accessADM: " + str(api_portTriggering['accessADM']))
            self.list_steps_fail.append('4. accessADM: ' + str(api_portTriggering['accessADM']))
        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_SAB_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-security-access-bywifi')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-security-access-bywifi')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(1)
        # Step 3: Click "DESLIGADO" to enable wifi
        try:
            driver.find_element_by_css_selector(".custom-radio[for='accessOff']").click()
            driver.find_element_by_css_selector('.holder-icon').click()
            self.list_steps.append('\n[Pass] 3. The button work normally')
        except AssertionError:
            self.list_steps.append("\n[Fail] 3. Can't Click the 'DESLIGADO'")
            self.list_steps_fail.append("2. Can't Click the 'DESLIGADO'")

        time.sleep(1)

        # Step 4: Verify the information
        api_portTriggering = Helper.Helper_common.api_accessADM()
        try:
            self.assertEqual(api_portTriggering['accessADM'], False)
            self.list_steps.append('\n[Pass] 4. accessADM: ' + str(api_portTriggering['accessADM']))
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. accessADM: " + str(api_portTriggering['accessADM']))
            self.list_steps_fail.append('4. accessADM: ' + str(api_portTriggering['accessADM']))
        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_SAB_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-access-bywifi')
        expected_url = ipv4 + '/#page-security-access-bywifi'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security Access By Wifi: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security Access By Wifi: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security Access By Wifi display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'util.js',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'access_bywifi.js',
                    'cmp_basic.js',
                    'cmp_headresult.js',
                    'cmp_form.js',
                    'messagebox.js',
                    'srv_service.js',
                    'comparator.js',
                    'accessADM',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security Access By Wifi page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security Access By Wifi page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security Access By Wifi page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SAB_03] Assertion wrong')


class PageSecurityParentalControl(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_SPC_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-security-parental-control')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-security-parental-control')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(5)
        # Step 3: Click "ADICIONAR FILTRO " and change the configuration
        try:
            driver.find_element_by_css_selector('#apply .holder-icon').click()
            time.sleep(2)
            driver.find_element_by_id('filter-name').send_keys('Rule #1')
            driver.find_element_by_id('mac-input').send_keys('11.12.13.14.15.16')
            if driver.find_element_by_id('active-whole-day').get_attribute('checked') == None:
                driver.find_element_by_css_selector('.radio-check[for="active-whole-day"]').click()
            driver.find_element_by_id('start-port').send_keys(random.randrange(1, 65635))
            start_port = int(driver.find_element_by_id('start-port').get_attribute('value'))
            driver.find_element_by_id('end-port').send_keys(random.randrange(start_port, 65635))
            driver.find_element_by_id('protocol').send_keys('AMBOS')
            driver.find_element_by_css_selector('.button.icon').click()

            self.list_steps.append('\n[Pass] 3. The button work normally')
        except AssertionError:
            self.list_steps.append(
                "\n[Fail] driver.find_element_by_css_selector('.filter').click()3. Can't Click the 'LIGADO'")
            self.list_steps_fail.append("2. Can't Click the 'LIGADO'")

        time.sleep(1)
        api_security_managedDevices = Helper.Helper_common.api_security_managedDevices()
        time.sleep(1)
        driver.find_element_by_css_selector('.filter').click()
        time.sleep(1)

        # Step 4: Verify the information
        try:
            expected_filter_name = api_security_managedDevices['devices'][0]['name']
            expected_mac_address = api_security_managedDevices['devices'][0]['macAddress']
            expected_keyword_url = api_security_managedDevices['devices'][0]['service']['keywordurl']
            expected_protocol = str(api_security_managedDevices['devices'][0]['service']['protocol']).upper()
            expected_start_port = api_security_managedDevices['devices'][0]['service']['startPort']
            expected_end_port = api_security_managedDevices['devices'][0]['service']['endPort']
            expected_days = len(api_security_managedDevices['devices'][0]['schedule']['day'])
            expected_start_time = api_security_managedDevices['devices'][0]['schedule']['time']['start']
            expected_end_time = api_security_managedDevices['devices'][0]['schedule']['time']['end']

            actual_filter_name = driver.find_element_by_css_selector('.parental .text').text
            actual_mac_address = driver.find_elements_by_css_selector('strong.radio-check-label')[0].text
            actual_keyword_url = driver.find_elements_by_css_selector('strong.radio-check-label')[1].text
            actual_protocol = driver.find_elements_by_css_selector('strong.radio-check-label')[2].text
            actual_start_port = driver.find_elements_by_css_selector('strong.radio-check-label')[3].text
            actual_end_port = driver.find_elements_by_css_selector('strong.radio-check-label')[4].text
            actual_days = len(driver.find_elements_by_css_selector('.day.checkbox'))
            actual_start_time = driver.find_elements_by_css_selector('strong.radio-check-label')[5].text
            actual_end_time = driver.find_elements_by_css_selector('strong.radio-check-label')[6].text

            self.assertEqual(expected_filter_name, actual_filter_name)
            self.assertEqual(expected_mac_address, actual_mac_address)
            self.assertEqual(expected_keyword_url, actual_keyword_url)
            self.assertEqual(expected_protocol, actual_protocol)
            self.assertEqual(str(expected_start_port), actual_start_port)
            self.assertEqual(str(expected_end_port), actual_end_port)
            self.assertEqual(expected_days, actual_days)
            self.assertEqual(str(expected_start_time), str(actual_start_time))
            self.assertEqual(str(expected_end_time), str(actual_end_time))

            self.list_steps.append("\n[Pass] 4. The info displayed same as API")
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. The info displayed different from API")
            self.list_steps_fail.append('4. The info displayed different from API')
            pass

        # remove filter
        driver.find_element_by_css_selector('.radio-check').click()
        driver.find_element_by_id('removeParental').click()
        time.sleep(2)
        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_SPC_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-security-parental-control')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-security-parental-control')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(5)
        # Step 3: Click "ADICIONAR FILTRO " and change the configuration
        try:
            driver.find_element_by_css_selector('#apply .holder-icon').click()
            time.sleep(2)
            driver.find_element_by_id('filter-name').send_keys('Rule #1')
            driver.find_element_by_id('mac-input').send_keys('11.12.13.14.15.16')
            if driver.find_element_by_id('active-whole-day').get_attribute('checked') == True:
                driver.find_element_by_css_selector('.radio-check[for="active-whole-day"]').click()
            # select time
            driver.find_element_by_css_selector('#hour').send_keys(random.randrange(0, 12))
            driver.find_element_by_css_selector('#minute').send_keys(random.randrange(00, 60))
            driver.find_elements_by_css_selector('#hour')[1].send_keys(random.randrange(0, 12))
            driver.find_elements_by_css_selector('#minute')[1].send_keys(random.randrange(00, 60))

            driver.find_element_by_id('keyword-url').send_keys('google.com')

            driver.find_element_by_id('start-port').send_keys(random.randrange(1, 65635))
            start_port = int(driver.find_element_by_id('start-port').get_attribute('value'))
            driver.find_element_by_id('end-port').send_keys(random.randrange(start_port, 65635))
            driver.find_element_by_id('protocol').send_keys('AMBOS')
            driver.find_element_by_css_selector('.button.icon').click()

            self.list_steps.append('\n[Pass] 3. The button work normally')
        except AssertionError:
            self.list_steps.append(
                "\n[Fail] driver.find_element_by_css_selector('.filter').click()3. Can't Click the 'LIGADO'")
            self.list_steps_fail.append("2. Can't Click the 'LIGADO'")

        time.sleep(1)
        api_security_managedDevices = Helper.Helper_common.api_security_managedDevices()
        time.sleep(1)
        driver.find_element_by_css_selector('.filter').click()
        time.sleep(1)

        # Step 4: Verify the information
        try:
            expected_filter_name = api_security_managedDevices['devices'][0]['name']
            expected_mac_address = api_security_managedDevices['devices'][0]['macAddress']
            expected_keyword_url = str(api_security_managedDevices['devices'][0]['service']['keywordurl']).upper()
            expected_protocol = str(api_security_managedDevices['devices'][0]['service']['protocol']).upper()
            expected_start_port = api_security_managedDevices['devices'][0]['service']['startPort']
            expected_end_port = api_security_managedDevices['devices'][0]['service']['endPort']
            expected_days = len(api_security_managedDevices['devices'][0]['schedule']['day'])
            expected_start_time = api_security_managedDevices['devices'][0]['schedule']['time']['start']
            expected_end_time = api_security_managedDevices['devices'][0]['schedule']['time']['end']

            actual_filter_name = driver.find_element_by_css_selector('.parental .text').text
            actual_mac_address = driver.find_elements_by_css_selector('strong.radio-check-label')[0].text
            actual_keyword_url = driver.find_elements_by_css_selector('strong.radio-check-label')[1].text
            actual_protocol = driver.find_elements_by_css_selector('strong.radio-check-label')[2].text
            actual_start_port = driver.find_elements_by_css_selector('strong.radio-check-label')[3].text
            actual_end_port = driver.find_elements_by_css_selector('strong.radio-check-label')[4].text
            actual_days = len(driver.find_elements_by_css_selector('.day.checkbox'))
            actual_start_time = driver.find_elements_by_css_selector('strong.radio-check-label')[5].text
            actual_end_time = driver.find_elements_by_css_selector('strong.radio-check-label')[6].text

            self.assertEqual(expected_filter_name, actual_filter_name)
            self.assertEqual(expected_mac_address, actual_mac_address)
            self.assertEqual(expected_keyword_url, actual_keyword_url)
            self.assertEqual(expected_protocol, actual_protocol)
            self.assertEqual(str(expected_start_port), actual_start_port)
            self.assertEqual(str(expected_end_port), actual_end_port)
            self.assertEqual(expected_days, actual_days)
            self.assertEqual(str(expected_start_time), str(actual_start_time))
            self.assertEqual(str(expected_end_time), str(actual_end_time))

            self.list_steps.append("\n[Pass] 4. The info displayed same as API")
        except AssertionError:
            self.list_steps.append("\n[Fail] 4. The info displayed different from API")
            self.list_steps_fail.append('4. The info displayed different from API')
            pass

        # remove filter
        driver.find_element_by_css_selector('.radio-check').click()
        driver.find_element_by_id('removeParental').click()
        time.sleep(2)
        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_SPC_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.get(ipv4 + '/#page-security-parental-control')
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-security-parental-control')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(5)
        # Step 3: Click "ADICIONAR FILTRO " and change the configuration
        try:
            driver.find_element_by_css_selector('#apply .holder-icon').click()
            time.sleep(2)
            driver.find_element_by_id('filter-name').send_keys('Rule #1')
            driver.find_element_by_id('mac-input').send_keys('11.12.13.14.15.16')
            if driver.find_element_by_id('active-whole-day').get_attribute('checked') == None:
                driver.find_element_by_css_selector('.radio-check[for="active-whole-day"]').click()
            driver.find_element_by_id('start-port').send_keys(random.randrange(1, 65635))
            start_port = int(driver.find_element_by_id('start-port').get_attribute('value'))
            driver.find_element_by_id('end-port').send_keys(random.randrange(start_port, 65635))
            driver.find_element_by_id('protocol').send_keys('AMBOS')
            driver.find_element_by_css_selector('.button.icon').click()

            self.list_steps.append('\n[Pass] 3. The button work normally')
        except AssertionError:
            self.list_steps.append(
                "\n[Fail] driver.find_element_by_css_selector('.filter').click()3. Can't Click the 'LIGADO'")
            self.list_steps_fail.append("2. Can't Click the 'LIGADO'")

        time.sleep(1)
        api_security_managedDevices = Helper.Helper_common.api_security_managedDevices()
        time.sleep(1)
        driver.find_element_by_css_selector('.filter').click()
        time.sleep(1)

        # Step 4: Verify the information
        try:
            expected_filter_name = api_security_managedDevices['devices'][0]['name']
            expected_mac_address = api_security_managedDevices['devices'][0]['macAddress']
            expected_keyword_url = api_security_managedDevices['devices'][0]['service']['keywordurl']
            expected_protocol = str(api_security_managedDevices['devices'][0]['service']['protocol']).upper()
            expected_start_port = api_security_managedDevices['devices'][0]['service']['startPort']
            expected_end_port = api_security_managedDevices['devices'][0]['service']['endPort']
            expected_days = len(api_security_managedDevices['devices'][0]['schedule']['day'])
            expected_start_time = api_security_managedDevices['devices'][0]['schedule']['time']['start']
            expected_end_time = api_security_managedDevices['devices'][0]['schedule']['time']['end']

            actual_filter_name = driver.find_element_by_css_selector('.parental .text').text
            actual_mac_address = driver.find_elements_by_css_selector('strong.radio-check-label')[0].text
            actual_keyword_url = driver.find_elements_by_css_selector('strong.radio-check-label')[1].text
            actual_protocol = driver.find_elements_by_css_selector('strong.radio-check-label')[2].text
            actual_start_port = driver.find_elements_by_css_selector('strong.radio-check-label')[3].text
            actual_end_port = driver.find_elements_by_css_selector('strong.radio-check-label')[4].text
            actual_days = len(driver.find_elements_by_css_selector('.day.checkbox'))
            actual_start_time = driver.find_elements_by_css_selector('strong.radio-check-label')[5].text
            actual_end_time = driver.find_elements_by_css_selector('strong.radio-check-label')[6].text

            self.assertEqual(expected_filter_name, actual_filter_name)
            self.assertEqual(expected_mac_address, actual_mac_address)
            self.assertEqual(expected_keyword_url, actual_keyword_url)
            self.assertEqual(expected_protocol, actual_protocol)
            self.assertEqual(str(expected_start_port), actual_start_port)
            self.assertEqual(str(expected_end_port), actual_end_port)
            self.assertEqual(expected_days, actual_days)
            self.assertEqual(str(expected_start_time), str(actual_start_time))
            self.assertEqual(str(expected_end_time), str(actual_end_time))

            self.list_steps.append("\n[Pass] 4.1. The info displayed same as API")
        except AssertionError:
            self.list_steps.append("\n[Fail] 4.1. The info displayed different from API")
            self.list_steps_fail.append('4.1. The info displayed different from API')
            pass

        # remove filter
        driver.find_element_by_css_selector('.radio-check').click()
        driver.find_element_by_id('removeParental').click()
        time.sleep(2)
        try:
            list_filter = len(driver.find_elements_by_css_selector('.parental .text'))
            self.assertEqual(list_filter, 0)
            self.list_steps.append("\n[Pass] 4.2. All existing filters are removed")
        except AssertionError:
            self.list_steps.append("\n[Fail] 4.2. All existing filters aren't removed")
            self.list_steps_fail.append("4.2. All existing filters aren't removed")
        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_SPC_05(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-security-parental-control')
        expected_url = ipv4 + '/#page-security-parental-control'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Security Parental Control: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Security Parental Control: ' + driver.current_url)
            list_steps_fail.append('2.URL page Security Parental Control display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'util.js',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'parental_control.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'srv_security.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'comparator.js',
                    'managedDevices',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Security Parental Control page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Security Parental Control page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Security Parental Control page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_SPC_05] Assertion wrong')


class PageWifiPrimaryNetwork(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_WPN_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(5)

        # Step 3: Click "Avitar' button
        if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                'checked') != 'true':
            driver.find_element_by_css_selector('.radio-check[for="active"]').click()

        # Step 4:
        # create a string contains 32 spaces
        special_chars = ''
        for i in range(32):
            special_chars = special_chars + ' '
        driver.find_element_by_id('network_name').clear()
        driver.find_element_by_id('network_name').send_keys(special_chars)
        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        expected_wifi_name = Helper.Helper_common.api_wifi_ssid_2G()['name']
        actual_wifi_name = driver.find_element_by_id('network_name').get_attribute('value')
        try:
            self.assertEqual(expected_wifi_name, actual_wifi_name)
            self.list_steps.append('\n[Pass] 4. Wifi 2G name displayed same as the API:' + actual_wifi_name)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Wifi 2G name displayed different from the API:' + actual_wifi_name)
            self.list_steps_fail.append("4. Wifi 2G name displayed different from the API:" + actual_wifi_name)
            pass

        # wifi 5G
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)

        # Step 5: Click "Avitar' button
        if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                'checked') != 'true':
            driver.find_element_by_css_selector('.radio-check[for="active"]').click()

        # Step 6:
        time.sleep(1)
        driver.find_element_by_id('network_name').clear()
        driver.find_element_by_id('network_name').send_keys(special_chars)
        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        expected_wifi5G_name = Helper.Helper_common.api_wifi_ssid_5G()['name']
        actual_wifi5G_name = driver.find_element_by_id('network_name').get_attribute('value')
        try:
            self.assertEqual(expected_wifi5G_name, actual_wifi5G_name)
            self.list_steps.append('\n[Pass] 6. Wifi 5G name displayed same as the API:' + actual_wifi_name)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Wifi 5G name displayed different from the API:' + actual_wifi_name)
            self.list_steps_fail.append("6. Wifi 5G name displayed different from the API:" + actual_wifi_name)
            pass

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(1)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available' + driver.current_url)
        except AssertionError:
            self.list_steps.append("\n[Fail] 2. The page isn't available:" + driver.current_url)
            self.list_steps_fail.append("2. The page isn't available:" + driver.current_url)

        time.sleep(5)

        # Step 3: Click "Avitar' button
        if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                'checked') != 'true':
            driver.find_element_by_css_selector('.radio-check[for="active"]').click()

        # Step 4:
        driver.find_element_by_id('close_network').send_keys('Ligado')
        driver.find_element_by_id('network_name').clear()
        driver.find_element_by_id('network_name').send_keys('abc')

        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        expected_closed_network = str(Helper.Helper_common.api_wifi_ssid_2G()['hiddenSSID']).lower()
        actual_close_network = driver.find_element_by_id('close_network').get_attribute('value')
        try:
            self.assertEqual(expected_closed_network, actual_close_network)
            self.list_steps.append(
                '\n[Pass] 4. Rede fechada information 2G displayed same as response from the API: ' + actual_close_network)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Rede fechada information 2G displayed different with response from the API: ' + actual_close_network)
            self.list_steps_fail.append(
                '4. Rede fechada information 2G displayed different with response from the API: ' + actual_close_network)
            pass

        # wifi 5G
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)

        # Step 5: Click "Avitar' button
        if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                'checked') != 'true':
            driver.find_element_by_css_selector('.radio-check[for="active"]').click()

        # Step 6:
        time.sleep(1)

        driver.find_element_by_id('close_network').send_keys('Ligado')
        driver.find_element_by_id('network_name').clear()
        driver.find_element_by_id('network_name').send_keys('abc')

        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        expected_closed_network = str(Helper.Helper_common.api_wifi_ssid_2G()['hiddenSSID']).lower()
        actual_close_network = driver.find_element_by_id('close_network').get_attribute('value')
        try:
            self.assertEqual(expected_closed_network, actual_close_network)
            self.list_steps.append(
                '\n[Pass] 6. Rede fechada information 5G displayed same as response from the API: ' + actual_close_network)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Rede fechada information 5G displayed different with response from the API: ' + actual_close_network)
            self.list_steps_fail.append(
                '4. Rede fechada information 5G displayed different with response from the API: ' + actual_close_network)
            pass

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2.1: Change setting on wifi radio
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rádio"]').click()
        time.sleep(3)

        # Set wirelessMode for 2G
        driver.find_element_by_id('wirelessMode').send_keys('Off')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        time.sleep(2)
        # Step 2.2: Set wirelessMode for 5G
        driver.find_element_by_css_selector('.custom-radio[for="radio5g"]').click()
        time.sleep(2)
        # Set wirelessMode for 2G
        driver.find_element_by_id('wirelessMode').send_keys('Off')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        # Step 3:
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(2)

        # 2G
        try:
            self.assertEqual('Nenhum\nERP', driver.find_element_by_id('mode_required').text)
            self.list_steps.append(
                '\n[Pass] 3.1. Wifi 2G Modo exigido info displayed correct: ' + driver.find_element_by_id(
                    'mode_required').text)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3.1. Wifi 2G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            self.list_steps_fail.append(
                '3.1. Wifi 2G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)

        # 5G
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        try:
            self.assertEqual('Nenhum', driver.find_element_by_id('mode_required').text)
            self.list_steps.append(
                '\n[Pass] 3.2. Wifi 5G Modo exigido info displayed correct: ' + driver.find_element_by_id(
                    'mode_required').text)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3.2. Wifi 5G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            self.list_steps_fail.append(
                '3.2. Wifi 5G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            pass

        # Step 4: Change setting on wifi radio
        driver.find_element_by_class_name('icon').click()
        time.sleep(1)
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rádio"]').click()
        time.sleep(1)

        # Step 4.1: Set wirelessMode for 2G to Auto
        driver.find_element_by_id('wirelessMode').send_keys('Auto')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break

        # Step 4.2: Set wirelessMode for 5G to Auto
        driver.find_element_by_css_selector('.custom-radio[for="radio5g"]').click()
        time.sleep(2)
        # Set wirelessMode for 2G
        driver.find_element_by_id('wirelessMode').send_keys('Auto')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()

        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        # Step 5:
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(1)

        # 2G
        try:
            self.assertEqual('Nenhum\nERP\nHT', driver.find_element_by_id('mode_required').text)
            self.list_steps.append(
                '\n[Pass] 5.1. Wifi 2G Modo exigido info displayed correct: ' + driver.find_element_by_id(
                    'mode_required').text)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.1. Wifi 2G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            self.list_steps_fail.append(
                '5.1. Wifi 2G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            pass

        # 5G
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        try:
            self.assertEqual('Nenhum\nHT\nVHT', driver.find_element_by_id('mode_required').text)
            self.list_steps.append(
                '\n[Pass] 5.2. Wifi 5G Modo exigido info displayed correct: ' + driver.find_element_by_id(
                    'mode_required').text)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.2. Wifi 5G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            self.list_steps_fail.append(
                '5.2. Wifi 5G Modo exigido info displayed incorrect: ' + driver.find_element_by_id(
                    'mode_required').text)
            pass

        # Step 6: Go to 2G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 6. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Can not check the Avitar checkbox')
            self.list_steps_fail.append('6. Can not check the Avitar checkbox')

        # Step 7:
        driver.find_element_by_id('mode_required').send_keys('ERP')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wireless_mode = Helper.Helper_common.api_wifi_radio_2G()['basic']['wirelessMode']
        try:
            self.assertEqual('802.11g+n', wireless_mode)
            self.list_steps.append('\n[Pass] 7. Value of wirelessMode is same as expectation: ' + wireless_mode)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Value of wirelessMode different with expectation: ' + wireless_mode)
            self.list_steps_fail.append('7. Value of wirelessMode different with expectation: ' + wireless_mode)

        # Step 8:
        driver.find_element_by_id('mode_required').send_keys('HT')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wireless_mode = Helper.Helper_common.api_wifi_radio_2G()['basic']['wirelessMode']
        try:
            self.assertEqual('802.11n', wireless_mode)
            self.list_steps.append('\n[Pass] 8. Value of wirelessMode is same as expectation: ' + wireless_mode)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Value of wirelessMode different with expectation: ' + wireless_mode)
            self.list_steps_fail.append('8. Value of wirelessMode different with expectation ' + wireless_mode)

        # Step 9: Go to 5G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 9. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 9. Can not check the Avitar checkbox')
            self.list_steps_fail.append('9. Can not check the Avitar checkbox')

        # Step 10:
        driver.find_element_by_id('mode_required').send_keys('ERP')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wireless_mode = Helper.Helper_common.api_wifi_radio_5G()['basic']['wirelessMode']
        try:
            self.assertEqual('802.11n+ac', wireless_mode)
            self.list_steps.append('\n[Pass] 10. Value of wirelessMode is same as expectation: ' + wireless_mode)
        except AssertionError:
            self.list_steps.append('\n[Fail] 10. Value of wirelessMode different with expectation: ' + wireless_mode)
            self.list_steps_fail.append('10. Value of wirelessMode different with expectation' + wireless_mode)

        # Step 11:
        driver.find_element_by_id('mode_required').send_keys('VHT')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wireless_mode = Helper.Helper_common.api_wifi_radio_5G()['basic']['wirelessMode']
        try:
            self.assertEqual('802.11ac', wireless_mode)
            self.list_steps.append('\n[Pass] 10. Value of wirelessMode is same as expectation: ' + wireless_mode)
        except AssertionError:
            self.list_steps.append('\n[Fail] 11. Value of wirelessMode different with expectation: ' + wireless_mode)
            self.list_steps_fail.append('11. Value of wirelessMode different with expectation:' + wireless_mode)

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2: Access the "page-wifi-primary-network" page
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. The page is not available: ' + driver.current_url)
            self.list_steps_fail.append('2. The page is not available: ' + driver.current_url)

        # Step 3: Go to 2G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 3. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Can not check the Avitar checkbox')
            self.list_steps_fail.append('3. Can not check the Avitar checkbox')

        # Step 4:  In "AP isolado" option, select "Ativado" and apply the setting
        driver.find_element_by_id('ap_isolate').send_keys('Ativado')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        expected_ap_isolate = str(Helper.Helper_common.api_wifi_ssid_2G()['APIsolate']).lower()
        actual_ap_isolate = driver.find_element_by_id('ap_isolate').get_attribute('value')
        try:
            self.assertEqual(expected_ap_isolate, actual_ap_isolate)
            self.list_steps.append('\n[Pass] 4. Value displayed is same as API response: ' + actual_ap_isolate)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Value displayed is not same as API response: ' + actual_ap_isolate)
            self.list_steps_fail.append('4. Value displayed is not same as API response: ' + actual_ap_isolate)

        # Step 5: Go to 5G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 5. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Can not check the Avitar checkbox')
            self.list_steps_fail.append('5. Can not check the Avitar checkbox')

        # Step 6:  In "AP isolado" option, select "Ativado" and apply the setting
        driver.find_element_by_id('ap_isolate').send_keys('Ativado')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        expected_ap_isolate = str(Helper.Helper_common.api_wifi_ssid_5G()['APIsolate']).lower()
        actual_ap_isolate = driver.find_element_by_id('ap_isolate').get_attribute('value')
        try:
            self.assertEqual(expected_ap_isolate, actual_ap_isolate)
            self.list_steps.append('\n[Pass] 4. Value displayed is same as API response: ' + actual_ap_isolate)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Value displayed is not same as API response: ' + actual_ap_isolate)
            self.list_steps_fail.append('4. Value displayed is not same as API response: ' + actual_ap_isolate)

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_07(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2: Access the "page-wifi-primary-network" page
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. The page is not available: ' + driver.current_url)
            self.list_steps_fail.append('2. The page is not available: ' + driver.current_url)

        # Step 3: Go to 2G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 3. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Can not check the Avitar checkbox')
            self.list_steps_fail.append('3. Can not check the Avitar checkbox')

        # Step 4: Click "HABILITAR" to enable WPS and apply setting
        driver.find_element_by_css_selector('.custom-radio[for="habilitar"]').click()
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wifi_wps = Helper.Helper_common.api_wifi_wps_2G()['active']

        try:
            self.assertTrue(wifi_wps)
            self.list_steps.append('\n[Pass] 4. Value displayed is same as API response: ' + str(wifi_wps))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Value displayed is not same as API response: ' + str(wifi_wps))
            self.list_steps_fail.append('4. Value displayed is not same as API response: ' + str(wifi_wps))

        # Step 5: Click "INCAPACITAR" to disable WPS and apply setting
        driver.find_element_by_css_selector('.custom-radio[for="incapacitar"]').click()
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wifi_wps = Helper.Helper_common.api_wifi_wps_2G()['active']

        try:
            self.assertFalse(wifi_wps)
            self.list_steps.append('\n[Pass] 5. Value displayed is same as API response: ' + str(wifi_wps))
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Value displayed is not same as API response: ' + str(wifi_wps))
            self.list_steps_fail.append('5. Value displayed is not same as API response: ' + str(wifi_wps))

        # Step 6: Go to 5G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 6. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Can not check the Avitar checkbox')
            self.list_steps_fail.append('6. Can not check the Avitar checkbox')

        # Step 7: Click "HABILITAR" to enable WPS and apply setting
        driver.find_element_by_css_selector('.custom-radio[for="habilitar"]').click()
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wifi_wps = Helper.Helper_common.api_wifi_wps_5G()['active']

        try:
            self.assertTrue(wifi_wps)
            self.list_steps.append('\n[Pass] 7. Value displayed is same as API response: ' + str(wifi_wps))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Value displayed is not same as API response: ' + str(wifi_wps))
            self.list_steps_fail.append('7. Value displayed is not same as API response: ' + str(wifi_wps))

        # Step 8: Click "INCAPACITAR" to disable WPS and apply setting
        driver.find_element_by_css_selector('.custom-radio[for="incapacitar"]').click()
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wifi_wps = Helper.Helper_common.api_wifi_wps_5G()['active']

        try:
            self.assertFalse(wifi_wps)
            self.list_steps.append('\n[Pass] 8. Value displayed is same as API response: ' + str(wifi_wps))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Value displayed is not same as API response: ' + str(wifi_wps))
            self.list_steps_fail.append('8. Value displayed is not same as API response: ' + str(wifi_wps))

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_08(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2: Access the "page-wifi-primary-network" page
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. The page is not available: ' + driver.current_url)
            self.list_steps_fail.append('2. The page is not available: ' + driver.current_url)

        # Step 3: Go to 2G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 3. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Can not check the Avitar checkbox')
            self.list_steps_fail.append('3. Can not check the Avitar checkbox')

        # Step 4: Click "HABILITAR" to enable WPS and apply setting
        driver.find_element_by_css_selector('.custom-radio[for="habilitar"]').click()
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wifi_wps = Helper.Helper_common.api_wifi_wps_2G()['active']

        try:
            self.assertTrue(wifi_wps)
            self.list_steps.append('\n[Pass] 4. Value displayed is same as API response: ' + str(wifi_wps))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Value displayed is not same as API response: ' + str(wifi_wps))
            self.list_steps_fail.append('4. Value displayed is not same as API response: ' + str(wifi_wps))

        # Step 5: Click "Gerar" to generate WPS PIN
        driver.find_element_by_xpath('//button[text()="Gerar"]').click()
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        expected_pin_info = Helper.Helper_common.api_wifi_wps_2G()['pin']
        actual_pin_info = driver.find_element_by_id('router_pin').get_attribute('value')

        try:
            self.assertEqual(actual_pin_info, expected_pin_info)
            self.list_steps.append('\n[Pass] 5. Pin value displayed is same as API response: ' + actual_pin_info)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Pin value displayed is not same as API response: ' + actual_pin_info)
            self.list_steps_fail.append('5. Pin value displayed is not same as API response: ' + actual_pin_info)

        # Step 6: Go to 5G page then Click "Avitar' button
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        try:
            if driver.find_element_by_css_selector('.radio-check-controler[value="Ativar"]').get_attribute(
                    'checked') != 'true':
                driver.find_element_by_css_selector('.radio-check[for="active"]').click()
            self.list_steps.append('\n[Pass] 6. The Avitar checkbox works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Can not check the Avitar checkbox')
            self.list_steps_fail.append('6. Can not check the Avitar checkbox')

        # Step 7: Click "HABILITAR" to enable WPS and apply setting
        driver.find_element_by_css_selector('.custom-radio[for="habilitar"]').click()
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)
        wifi_wps = Helper.Helper_common.api_wifi_wps_2G()['active']

        try:
            self.assertTrue(wifi_wps)
            self.list_steps.append('\n[Pass] 7. Value displayed is same as API response: ' + str(wifi_wps))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Value displayed is not same as API response: ' + str(wifi_wps))
            self.list_steps_fail.append('7. Value displayed is not same as API response: ' + str(wifi_wps))

        # Step 8: Click "Gerar" to generate WPS PIN
        driver.find_element_by_xpath('//button[text()="Gerar"]').click()
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        expected_pin_info = Helper.Helper_common.api_wifi_wps_2G()['pin']
        actual_pin_info = driver.find_element_by_id('router_pin').get_attribute('value')

        try:
            self.assertEqual(actual_pin_info, expected_pin_info)
            self.list_steps.append('\n[Pass] 8. Pin value displayed is same as API response: ' + actual_pin_info)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Pin value displayed is not same as API response: ' + actual_pin_info)
            self.list_steps_fail.append('8. Pin value displayed is not same as API response: ' + actual_pin_info)

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_05(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2: Access the "page-wifi-primary-network" page
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. The page is not available: ' + driver.current_url)
            self.list_steps_fail.append('2. The page is not available: ' + driver.current_url)

        # Step 3: Click "2.4 GHZ" to select 2.4 Ghz interface, in "Autenticação de rede" option, select "Nenhum" and apply the setting
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('NENHUM')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        security_type = Helper.Helper_common.api_wifi_ssid_2G()['security']['type']

        try:
            self.assertEqual('NONE', security_type)
            self.list_steps.append('\n[Pass] 3. Value displayed is same as API response: ' + security_type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Value displayed is not same as API response: ' + security_type)
            self.list_steps_fail.append('4. Value displayed is not same as API response: ' + security_type)
            pass

        # Step 4: Autenticação de rede" option, select "WPA-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(0.5)
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('2700')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_2G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['password']

        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , ''')

        try:
            self.assertEqual("WPA-PSK", type)
            self.list_steps.append('\n[Pass] 4.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('4.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("2700", str(groupKey))
            self.list_steps.append('\n[Pass] 4.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('4.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES/TKIP", encryption)
            self.list_steps.append('\n[Pass] 4.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('4.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 4.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('4.4. Pin value displayed is not same as API response: ' + password)
            pass

        # Step 5: Autenticação de rede" option, select "WPA2-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA2-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(1)
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('3600')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_2G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['password']
        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , ''')

        try:
            self.assertEqual("WPA2-PSK", type)
            self.list_steps.append('\n[Pass] 5.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('5.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("3600", str(groupKey))
            self.list_steps.append('\n[Pass] 5.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('5.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES", encryption)
            self.list_steps.append('\n[Pass] 5.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('5.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 5.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('5.4. Pin value displayed is not same as API response: ' + password)
            pass

        # Step 6: Autenticação de rede" option, select "WPA2/WPA-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA2/WPA-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(1)
        driver.find_element_by_css_selector('#encryption').send_keys('AES')
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('1800')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_2G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['password']
        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" <''')

        try:
            self.assertEqual("WPA2/WPA-PSK", type)
            self.list_steps.append('\n[Pass] 6.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('6.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("1800", str(groupKey))
            self.list_steps.append('\n[Pass] 6.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('6.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES", encryption)
            self.list_steps.append('\n[Pass] 6.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('6.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 6.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('6.4. Pin value displayed is not same as API response: ' + password)
            pass

        # Step 7: Autenticação de rede" option, select "WPA2/WPA-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA2/WPA-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(1)
        driver.find_element_by_css_selector('#encryption').send_keys('AES/TKIP')
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('2700')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_2G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_2G()['security']['personal']['password']
        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , ''')

        try:
            self.assertEqual("WPA2/WPA-PSK", type)
            self.list_steps.append('\n[Pass] 7.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('7.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("2700", str(groupKey))
            self.list_steps.append('\n[Pass] 7.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('7.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES/TKIP", encryption)
            self.list_steps.append('\n[Pass] 7.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('7.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 7.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('7.4. Pin value displayed is not same as API response: ' + password)
            pass

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_06(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2: Access the "page-wifi-primary-network" page
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Rede Principal"]').click()
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-primary-network')
            self.list_steps.append('\n[Pass] 2. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. The page is not available: ' + driver.current_url)
            self.list_steps_fail.append('2. The page is not available: ' + driver.current_url)

        # Step 3: Click "5 GHZ" to select 2.4 Ghz interface, in "Autenticação de rede" option, select "Nenhum" and apply the setting
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('NENHUM')
        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        security_type = Helper.Helper_common.api_wifi_ssid_5G()['security']['type']

        try:
            self.assertEqual('NONE', security_type)
            self.list_steps.append('\n[Pass] 3. Value displayed is same as API response: ' + security_type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Value displayed is not same as API response: ' + security_type)
            self.list_steps_fail.append('4. Value displayed is not same as API response: ' + security_type)
            pass

        # Step 4: Autenticação de rede" option, select "WPA-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(0.5)
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('2700')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_5G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['password']

        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" <''')

        try:
            self.assertEqual("WPA-PSK", type)
            self.list_steps.append('\n[Pass] 4.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('4.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("2700", str(groupKey))
            self.list_steps.append('\n[Pass] 4.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('4.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES/TKIP", encryption)
            self.list_steps.append('\n[Pass] 4.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('4.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 4.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('4.4. Pin value displayed is not same as API response: ' + password)
            pass

        # Step 5: Autenticação de rede" option, select "WPA2-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA2-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(1)
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('3600')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_5G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['password']
        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , ''')

        try:
            self.assertEqual("WPA2-PSK", type)
            self.list_steps.append('\n[Pass] 5.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('5.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("3600", str(groupKey))
            self.list_steps.append('\n[Pass] 5.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('5.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES", encryption)
            self.list_steps.append('\n[Pass] 5.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('5.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 5.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('5.4. Pin value displayed is not same as API response: ' + password)
            pass

        # Step 6: Autenticação de rede" option, select "WPA2/WPA-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA2/WPA-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(1)
        driver.find_element_by_css_selector('#encryption').send_keys('AES')
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('1800')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_5G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['password']
        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" <''')

        try:
            self.assertEqual("WPA2/WPA-PSK", type)
            self.list_steps.append('\n[Pass] 6.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('6.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("1800", str(groupKey))
            self.list_steps.append('\n[Pass] 6.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('6.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES", encryption)
            self.list_steps.append('\n[Pass] 6.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('6.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 6.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('6.4. Pin value displayed is not same as API response: ' + password)
            pass

        # Step 7: Autenticação de rede" option, select "WPA2/WPA-PSK"
        driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
        time.sleep(2)
        driver.find_element_by_id('security_type').send_keys('WPA2/WPA-PSK')
        if (driver.find_element_by_css_selector('.radio-check-controler#show_wpa').get_attribute('checked') != 'true'):
            driver.find_element_by_css_selector('.radio-check[for="show_wpa"]').click()
        time.sleep(1)
        driver.find_element_by_id('wpa_key').clear()
        driver.find_element_by_id('wpa_key').send_keys(
            '''@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /''')
        time.sleep(1)
        driver.find_element_by_css_selector('#encryption').send_keys('AES/TKIP')
        driver.find_element_by_id('group-key').clear()
        driver.find_element_by_id('group-key').send_keys('2700')

        # click Apply button
        driver.find_element_by_css_selector('.holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        type = Helper.Helper_common.api_wifi_ssid_5G()['security']['type']
        groupKey = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['groupKey']
        encryption = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['encryption']
        password = Helper.Helper_common.api_wifi_ssid_5G()['security']['personal']['password']
        expected_password = Helper.Helper_common.base64encode(
            '''HS:''' + user + ''':@ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , ''')

        try:
            self.assertEqual("WPA2/WPA-PSK", type)
            self.list_steps.append('\n[Pass] 7.1. Type value displayed is same as API response: ' + type)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.1. Type value displayed is not same as API response: ' + type)
            self.list_steps_fail.append('7.1. Type value displayed is not same as API response: ' + type)
            pass

        try:
            self.assertEqual("2700", str(groupKey))
            self.list_steps.append('\n[Pass] 7.2. groupKey value displayed is same as API response: ' + str(groupKey))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            self.list_steps_fail.append('7.2. groupKey value displayed is not same as API response: ' + str(groupKey))
            pass

        try:
            self.assertEqual("AES/TKIP", encryption)
            self.list_steps.append('\n[Pass] 7.3. Encryption value displayed is same as API response: ' + encryption)
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7.3. Encryption value displayed is not same as API response: ' + encryption)
            self.list_steps_fail.append('7.3. Encryption value displayed is not same as API response: ' + encryption)
            pass

        try:
            self.assertEqual(expected_password, password)
            self.list_steps.append('\n[Pass] 7.4. Password value displayed is same as API response: ' + password)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.4. Password value displayed is not same as API response: ' + password)
            self.list_steps_fail.append('7.4. Pin value displayed is not same as API response: ' + password)
            pass

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WPN_09(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-wifi-primary-network')
        expected_url = ipv4 + '/#page-wifi-primary-network'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Wifi Primary Network: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Wifi Primary Network: ' + driver.current_url)
            list_steps_fail.append('2.URL page Wifi Primary Network display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'main.js',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'primary_network.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'comparator.js',
                    'srv_wifi.js',
                    'wifi',
                    'wps?interfaceId=0',
                    'about',
                    'menu_main.js',
                    'ssid',
                    '0',
                    'radio',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Wifi Primary Network page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Wifi Primary Network page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Wifi Primary Network page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_WPN_09] Assertion wrong')


class PageWifiWdsConfiguration(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        # Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_WWC_01(self):
        self.def_name = Helper.Helper_common.get_func_name()
        self.list_steps_fail = []
        driver = self.driver

        # Step 1
        Helper.Helper_common.login(driver, self, ipv4)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-quick-setup')
            self.list_steps.append('\n[Pass] 1. Login success')
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login fail:' + driver.current_url)
            self.list_steps_fail.append('1. Login fail' + driver.current_url)

        # Step 2: Access the "page-wifi-wds-configuration" page
        time.sleep(2)
        driver.find_element_by_css_selector('.next.config').click()
        time.sleep(1)
        driver.find_element_by_class_name('icon').click()
        driver.find_element_by_css_selector('label[for="menu-wi-fi"]').click()
        driver.find_element_by_xpath('//a[text()="Configuração WDS"]').click()
        time.sleep(2)
        try:
            self.assertEqual(driver.current_url, ipv4 + '/#page-wifi-wds-configuration')
            self.list_steps.append('\n[Pass] 2. The page is available: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. The page is not available: ' + driver.current_url)
            self.list_steps_fail.append('2. The page is not available: ' + driver.current_url)

        # Step 3: Click "2.4 GHZ" to select 2.4 Ghz interface
        try:
            driver.find_element_by_css_selector('.custom-radio[for="2-4-ghz"]').click()
            time.sleep(2)
            self.list_steps.append('\n[Pass] 3. The button works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. The button does not works normally')
            self.list_steps_fail.append('3. The button does not works normally')

        # Step 4: Input these MAC addresses into "Conexões remotas" option:
        driver.find_element_by_css_selector('.combo-box#bridge').send_keys('Ativado')
        list_input_connection = driver.find_elements_by_css_selector('input.input')
        list_input_connection[0].clear()
        list_input_connection[0].send_keys('11:12:13:14:15:11')
        list_input_connection[1].clear()
        list_input_connection[1].send_keys('11:12:13:14:15:12')
        list_input_connection[2].clear()
        list_input_connection[2].send_keys('11:12:13:14:15:13')
        list_input_connection[3].clear()
        list_input_connection[3].send_keys('11:12:13:14:15:14')
        driver.find_element_by_css_selector('.button.icon[value="apply"] .holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        wifi_wds = Helper.Helper_common.api_wifi_wds_2G()
        time.sleep(1)

        try:
            self.assertTrue(wifi_wds['active'])
            self.list_steps.append(
                '\n[Pass] 4.1. Active value displayed is same as API response: ' + str(wifi_wds['active']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.1. Active value displayed is not same as API response: ' + str(wifi_wds['active']))
            self.list_steps_fail.append(
                '4.1. Active Value value displayed is not same as API response: ' + str(wifi_wds['active']))
            pass

        list_rules = Helper.Helper_common.api_wifi_wds_2G()['rules']

        for i in range(len(list_rules)):
            rule = list_rules[i]
            try:
                self.assertEqual(rule['mac'], '11:12:13:14:15:' + str(11 + i))
                self.list_steps.append(
                    '\n[Pass] 4.2. Rule value number ' + str(
                        rule['index']) + ' displayed is same as API response: ' + str(rule['mac']))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 4.2. Rule value number ' + str(
                        rule['index']) + ' displayed is not same as API response: ' + str(rule['mac']))
                self.list_steps_fail.append(
                    '4.2. Rule value number ' + str(
                        rule['index']) + ' displayed is not same as API response: ' + str(rule['mac']))
                pass
        # Step 5: Click "2.4 GHZ" to select 5 Ghz interface
        try:
            driver.find_element_by_css_selector('.custom-radio[for="5-ghz"]').click()
            time.sleep(2)
            self.list_steps.append('\n[Pass] 5. The button works normally')
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. The button does not works normally')
            self.list_steps_fail.append('5. The button does not works normally')

        # Step 6: Input these MAC addresses into "Conexões remotas" option:
        driver.find_element_by_css_selector('.combo-box#bridge').send_keys('Ativado')
        list_input_connection = driver.find_elements_by_css_selector('input.input')
        list_input_connection[0].clear()
        list_input_connection[0].send_keys('11:12:13:14:15:15')
        list_input_connection[1].clear()
        list_input_connection[1].send_keys('11:12:13:14:15:16')
        list_input_connection[2].clear()
        list_input_connection[2].send_keys('11:12:13:14:15:17')
        list_input_connection[3].clear()
        list_input_connection[3].send_keys('11:12:13:14:15:18')
        driver.find_element_by_css_selector('.button.icon[value="apply"] .holder-icon').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
        timeout = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgInnerWrap')
            time.sleep(1)
            if timeout == 60 * 10:
                break
        time.sleep(2)

        wifi_wds = Helper.Helper_common.api_wifi_wds_5G()
        time.sleep(1)

        try:
            self.assertTrue(wifi_wds['active'])
            self.list_steps.append(
                '\n[Pass] 6.1. Active value displayed is same as API response: ' + str(wifi_wds['active']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.1. Active value displayed is not same as API response: ' + str(wifi_wds['active']))
            self.list_steps_fail.append(
                '6.1. Active Value value displayed is not same as API response: ' + str(wifi_wds['active']))
            pass

        list_rules = Helper.Helper_common.api_wifi_wds_5G()['rules']

        for i in range(len(list_rules)):
            rule = list_rules[i]
            try:
                self.assertEqual(rule['mac'], '11:12:13:14:15:' + str(15 + i))
                self.list_steps.append(
                    '\n[Pass] 6.2. Rule value number ' + str(
                        rule['index']) + ' displayed is same as API response: ' + str(rule['mac']))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 6.2. Rule value number ' + str(
                        rule['index']) + ' displayed is not same as API response: ' + str(rule['mac']))
                self.list_steps_fail.append(
                    '6.2. Rule value number ' + str(
                        rule['index']) + ' displayed is not same as API response: ' + str(rule['mac']))
                pass

        self.assertEqual(self.list_steps_fail, [], self.list_steps_fail)

    def test_UI_WWC_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-wifi-wds-configuration')
        expected_url = ipv4 + '/#page-wifi-wds-configuration'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Wifi WDS Configuration: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Wifi WDS Configuration: ' + driver.current_url)
            list_steps_fail.append('2.URL page Wifi Primary Wifi WDS Configuration' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'define.js',
                    'util.js',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'wds_configuration.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_combobox.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'srv_wifi.js',
                    'wifi',
                    'about',
                    'menu_main.js',
                    'wds',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Wifi WDS Configuration page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Wifi WDS Configuration page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Wifi WDS Configuration page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_WWC_03] Assertion wrong')


class PageWifiRadio(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_WR_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
            pass
        time.sleep(1)
        # Click Restore
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, '[UI_WR_01] Pop-up change PW was timeout > 5 minutes')

        # Check API
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 4.1 Check API value active return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check API value active return: ' + str(actual))
            list_steps_fail.append('4.1 API value return wrong.')
            pass

        # Check display on WebUI
        ativar_tick_2g = Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler')
        # Pais
        country = driver.find_element_by_css_selector('#country')
        country = country.get_attribute('value')
        # Output Power
        output_power = driver.find_element_by_css_selector('#outputPower')
        output_power = output_power.get_attribute('value')
        # Wireless Mode
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        wireless_mode = wireless_mode.get_attribute('value')
        # Band With
        band_with_2g = driver.find_element_by_css_selector('#bandwidth')
        band_with_2g = band_with_2g.get_attribute('value')
        # SIDEband
        sideband = driver.find_element_by_css_selector('#sideband')
        sideband = sideband.get_attribute('value')
        # Chanel
        chanel = driver.find_element_by_css_selector('#channel')
        chanel = chanel.get_attribute('value')
        # Beamforming
        beamforming = driver.find_element_by_css_selector('#beamforming')
        beamforming = beamforming.get_attribute('value')

        # Click to 5G
        driver.find_element_by_css_selector('[for=radio5g]').click()
        ativar_tick_5g = Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler')
        # Band With
        band_with_5g = driver.find_element_by_css_selector('#bandwidth')
        band_with_5g = band_with_5g.get_attribute('value')
        list_actual_value = [ativar_tick_2g, country, output_power,
                             wireless_mode, band_with_2g, chanel,
                             beamforming, ativar_tick_5g, band_with_5g]
        try:
            self.assertEqual(ativar_tick_2g, 'true')
            self.assertEqual(country, 'MEXICO')
            self.assertEqual(output_power, 'high')
            self.assertEqual(wireless_mode, 'auto')
            self.assertEqual(band_with_2g, '40MHz')
            self.assertEqual(chanel, 'auto')
            self.assertEqual(beamforming, 'false')
            self.assertEqual(ativar_tick_5g, 'true')
            self.assertEqual(band_with_5g, '80MHz')
            self.list_steps.append('\n[Pass] 4.2 Check WebUI displayed:' + str(list_actual_value))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.2 Check WebUI displayed: ' + str(list_actual_value))
            list_steps_fail.append('4.2 WebUI displayed wrong: ' + str(list_actual_value))

        self.assertListEqual(list_steps_fail, [], '[UI_WR_01] Assertion Restore the wireless defaults fail')

    def test_UI_WR_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(1)
        # Click to 2.4g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') == 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 3. Check API uncheck Ativar return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API uncheck Ativar return: ' + str(actual))
            list_steps_fail.append('3. URL Page Wifi Radio wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_02] Assertion Disable 2.4 GHz interface fail')

    def test_UI_WR_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(1)
        # Click to 2.4g
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') == 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 3. Check API uncheck Ativar return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API uncheck Ativar return: ' + str(actual))
            list_steps_fail.append('3. URL Page Wifi Radio wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_03] Assertion Disable 5 GHz interface fail')

    def test_UI_WR_04(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(1)
        # Click to 2.4g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Output Power
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(2)
        # Click Medium
        driver.find_element_by_css_selector('#outputPower option:nth-child(2)').click()
        time.sleep(1)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 4. Check Output Power is Medium: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check Output Power is Medium: ' + actual)
            list_steps_fail.append('4.Medium Output Power is wrong: ' + actual)
            pass

        # Output Power
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(1)
        # Click Alto
        driver.find_element_by_css_selector('#outputPower option:nth-child(1)').click()
        time.sleep(2)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 5. Check Output Power is Alto: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check Output Power is Alto: ' + actual)
            list_steps_fail.append('5. Alto Output Power is wrong: ' + actual)
            pass

        # Output Power
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(2)
        # Click Baixo
        driver.find_element_by_css_selector('#outputPower option:nth-child(3)').click()
        time.sleep(1)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 6. Check Output Power is Baixo: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check Output Power is Baixo: ' + actual)
            list_steps_fail.append('6. Baixo Output Power is wrong: ' + actual)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_04] Assertion 2.4GHZ output power settings fail')

    def test_UI_WR_05(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 5g
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Output Power
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(2)
        # Click Medium
        driver.find_element_by_css_selector('#outputPower option:nth-child(2)').click()
        time.sleep(1)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 4. Check Output Power is Medium: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check Output Power is Medium: ' + actual)
            list_steps_fail.append('4. Medium Output Power is wrong: ' + actual)
            pass

        # Output Power
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(1)
        # Click Alto
        driver.find_element_by_css_selector('#outputPower option:nth-child(1)').click()
        time.sleep(2)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 5. Check Output Power is Alto: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check Output Power is Alto: ' + actual)
            list_steps_fail.append('5. Alto Output Power is wrong: ' + actual)
            pass

        # Output Power
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(2)
        # Click Baixo
        driver.find_element_by_css_selector('#outputPower option:nth-child(3)').click()
        time.sleep(1)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 6. Check Output Power is Baixo: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check Output Power is Baixo: ' + actual)
            list_steps_fail.append('6. Baixo Output Power is wrong: ' + actual)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_05] Assertion 5GHZ output power settings fail')

    def test_UI_WR_06(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 2g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # wireless Mode
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        # Bandwidth
        bandwidth = driver.find_elements_by_css_selector('#bandwidth option')
        actual_bandwidth = []
        for i in bandwidth:
            actual_bandwidth.append(i.get_attribute('value'))

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.1 Check Wireless Mode is OFF: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check Wireless Mode is OFF: ' + actual_wireless)
            list_steps_fail.append('4.1 OFF Wireless Mode is wrong: ' + actual_wireless)
            pass

        try:
            self.assertListEqual(actual_bandwidth, ['20'])
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
        except AssertionError:
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('4.2 BandWidth is wrong: ' + str(actual_bandwidth))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # wireless Mode
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        # Bandwidth
        bandwidth = driver.find_elements_by_css_selector('#bandwidth option')
        actual_bandwidth = []
        for i in bandwidth:
            actual_bandwidth.append(i.get_attribute('value'))

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
            list_steps_fail.append('5.1 AUTO Wireless Mode is wrong: ' + actual_wireless)
            pass
        expected_bandwidth = ['20', '40']
        try:
            self.assertListEqual(actual_bandwidth, expected_bandwidth)
            self.list_steps.append(
                '\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
        except AssertionError:
            self.list_steps.append(
                '\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('5.2 BandWidth is wrong: ' + str(actual_bandwidth))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.assertListEqual(list_steps_fail, [], '[UI_WR_06] Assertion 2.4GHZ 802.11.n mode settings fail')

    def test_UI_WR_07(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 5g
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)

        # wireless Mode
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        # Bandwidth
        bandwidth = driver.find_elements_by_css_selector('#bandwidth option')
        actual_bandwidth = []
        for i in bandwidth:
            actual_bandwidth.append(i.get_attribute('value'))

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.assertListEqual(actual_bandwidth, ['20'])
            self.list_steps.append('\n[Pass] 4.1 Check Wireless Mode is OFF: ' + actual_wireless)
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check Wireless Mode is OFF: ' + actual_wireless)
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('4. OFF Wireless Mode is wrong: ' + actual_wireless)
            list_steps_fail.append('4. BandWidth is wrong: ' + str(actual_bandwidth))
            pass

        # wireless Mode
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        # Bandwidth
        bandwidth = driver.find_elements_by_css_selector('#bandwidth option')
        actual_bandwidth = []
        for i in bandwidth:
            actual_bandwidth.append(i.get_attribute('value'))

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
            list_steps_fail.append('5.1 AUTO Wireless Mode is wrong: ' + actual_wireless)
            pass
        expected_bandwidth = ['20', '40', '80']
        try:
            self.assertListEqual(actual_bandwidth, expected_bandwidth)
            self.list_steps.append(
                '\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
        except AssertionError:
            self.list_steps.append(
                '\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('5.2 BandWidth is wrong: ' + str(actual_bandwidth))

        self.assertListEqual(list_steps_fail, [], '[UI_WR_07] Assertion 5GHZ 802.11.n mode settings fail')

    def test_UI_WR_08(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 2g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Wireless = Auto; BandWidth = 20; SideBand = Disable
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'
        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="20"]').click()
        time.sleep(1)

        # Verify sideband is diable
        side_band = driver.find_element_by_css_selector('#sideband').get_attribute('disabled')
        try:
            self.assertEqual(side_band, 'true')
            self.list_steps.append('\n[Pass] 4.1 Check Largura de Banda is disable: ' + side_band)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
            pass
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        expected_band_width = '20'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_band_width, actual_band_width)
            self.list_steps.append('\n[Pass] 4.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('4.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11b+g+n but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Wireless = Auto; BandWidth = 40; SideBand = Alto
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 5.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('5.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.3 Check Wireless Mode is 802.11b+g+n but wrong: ' + actual_wireless)
            pass

        try:
            self.assertEqual('upper', actual_sideband)
            self.list_steps.append('\n[Pass] 5.4 Check Side Band: ' + actual_sideband)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.4 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('5.4 Check Side band is upper but wrong: ' + actual_sideband)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Wireless = Auto; BandWidth = 40; SideBand = Baixo
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="lower"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 6.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('6.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.3 Check Wireless Mode is 802.11b+g+n but wrong: ' + actual_wireless)
            pass

        try:
            self.assertEqual('lower', actual_sideband)
            self.list_steps.append('\n[Pass] 6.4 Check Side Band: ' + actual_sideband)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.4 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('6.4 Check Side band is lower but wrong: ' + actual_sideband)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_08] Assertion 2.4GHZ Bandwidth settings fail')

    def test_UI_WR_09(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 5g
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Wireless = Auto; BandWidth = 20; SideBand = Disable
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="20"]').click()
        time.sleep(1)

        # Verify sideband is diable
        side_band = driver.find_element_by_css_selector('#sideband').get_attribute('disabled')
        try:
            self.assertEqual(side_band, 'true')
            self.list_steps.append('\n[Pass] 4.1 Check Largura de Banda is disable: ' + side_band)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
            pass
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        expected_band_width = '20'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_band_width, actual_band_width)
            self.list_steps.append('\n[Pass] 4.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('4.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Wireless = Auto; BandWidth = 80; SideBand = Disable
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="80"]').click()
        time.sleep(1)

        # Verify sideband is diable
        side_band = driver.find_element_by_css_selector('#sideband').get_attribute('disabled')
        try:
            self.assertEqual(side_band, 'true')
            self.list_steps.append('\n[Pass] 5.1 Check Largura de Banda is disable: ' + side_band)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('5.1  Check Largura de Banda is disable wrong: ' + side_band)
            pass
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        expected_band_width = '80'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_band_width, actual_band_width)
            self.list_steps.append('\n[Pass] 5.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('5.2 Check BandWidth set is 80 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.3 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Wireless = Auto; BandWidth = 40; SideBand = Alto
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 6.1 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.1 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('6.1 Check BandWidth set is 40 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.2 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)
            pass

        try:
            self.assertEqual('upper', actual_sideband)
            self.list_steps.append('\n[Pass] 6.3 Check Side Band: ' + actual_sideband)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.3 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('6.3 Check Side band is upper but wrong: ' + actual_sideband)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Wireless = Auto; BandWidth = 40; SideBand = Baixo
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="lower"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 7.1 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.1 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('7.1 Check BandWidth set is 20 but wrong: ' + actual_band_width)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 7.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('7.2 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)
            pass

        try:
            self.assertEqual('lower', actual_sideband)
            self.list_steps.append('\n[Pass] 7.3 Check Side Band: ' + actual_sideband)
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.3 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('7.3 Check Side band is lower but wrong: ' + actual_sideband)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_09] Assertion 5GHZ Bandwidth settings fail')

    def test_UI_WR_10(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 2g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4 Wireless = Off; Chanel = Auto
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'
        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="auto"]').click()
        time.sleep(1)

        # Verify Banda lateral para canal de controle is disable
        side_band = driver.find_element_by_css_selector('#sideband').get_attribute('disabled')
        try:
            self.assertEqual(side_band, 'true')
            self.list_steps.append('\n[Pass] 4.1 Check Largura de Banda is disable: ' + side_band)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
            pass
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = 'auto'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 4.2 Check Channel Set: ' + actual_channel)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.2 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('4.2 Check Channel Set is Auto but wrong: ' + actual_channel)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11b+g but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5 Wireless = Off; Canal = 1
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'
        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="1"]').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '1'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 5.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('5.1 Check Channel Set is 1 but wrong: ' + actual_channel)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.2 Check Wireless Mode is 802.11b+g but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 6 Wireless = Off; Canal = 13
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'
        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="13"]').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '13'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 6.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('6.1 Check Channel Set is 13 but wrong: ' + actual_channel)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.2 Check Wireless Mode is 802.11b+g but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 7 Wireless = Auto; BandWidth = 40; SideBand = Baixo, Channel = 1
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="lower"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="1"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '1']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append('\n[Pass] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 8 Wireless = Auto; BandWidth = 40; SideBand = Baixo; Channel = 9
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="lower"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="9"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '9']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 9 Wireless = Auto; BandWidth = 40; SideBand = Alto; Channel = 5
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="5"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '5']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 10 Wireless = Auto; BandWidth = 40; SideBand = Alto; Channel = 13
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11b+g'
        else:
            expected_wireless = '802.11b+g+n'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="13"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '13']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass

        self.assertListEqual(list_steps_fail, [], '[UI_WR_10] Assertion 2.4GHZ Channel Control settings fail')

    def test_UI_WR_11(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 5g
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4 Wireless = Off; Chanel = Auto
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="auto"]').click()
        time.sleep(1)

        # Verify Banda lateral para canal de controle is disable
        side_band = driver.find_element_by_css_selector('#sideband').get_attribute('disabled')
        try:
            self.assertEqual(side_band, 'true')
            self.list_steps.append('\n[Pass] 4.1 Check Largura de Banda is disable: ' + side_band)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
            pass
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = 'auto'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 4.2 Check Channel Set: ' + actual_channel)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.2 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('4.2 Check Channel Set is Auto but wrong: ' + actual_channel)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11a but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5 Wireless = Off; Canal = 36
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="36"]').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '36'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 5.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('5.1 Check Channel Set is 36 but wrong: ' + actual_channel)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.2 Check Wireless Mode is 802.11a but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 6 Wireless = Off; Canal = 165
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)
        # Click Off
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(2)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'
        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="165"]').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '165'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 6.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('6.1 Check Channel Set is 165 but wrong: ' + actual_channel)
            pass

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.2 Check Wireless Mode is 802.11a but wrong: ' + actual_wireless)
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 7 Wireless = Auto; BandWidth = 40; SideBand = Baixo, Channel = 36
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="lower"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="36"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '36']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append('\n[Pass] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 8 Wireless = Auto; BandWidth = 40; SideBand = Baixo; Channel = 157
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="lower"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="157"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '157']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 9 Wireless = Auto; BandWidth = 40; SideBand = Alto; Channel = 40
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="40"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '40']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 10 Wireless = Auto; BandWidth = 40; SideBand = Alto; Channel = 161
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="40"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="161"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '161']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 11 Wireless = Auto; BandWidth = 80; SideBand = Alto; Channel = 36
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="80"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="36"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '80', 'upper', '36']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 11. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 11. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('11. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 12 Wireless = Auto; BandWidth = 80; SideBand = Alto; Channel = 161
        wireless_mode = driver.find_element_by_css_selector('#wirelessMode')
        ActionChains(driver).move_to_element(wireless_mode).click().perform()
        time.sleep(2)

        # Click Auto
        driver.find_element_by_css_selector('#wirelessMode option:nth-child(1)').click()
        time.sleep(1)
        expected_wireless = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        if expected_wireless == 'off':
            expected_wireless = '802.11a'
        else:
            expected_wireless = '802.11a+n+ac'

        # Click to Bandwidth
        band_width = driver.find_element_by_css_selector('#bandwidth')
        ActionChains(driver).move_to_element(band_width).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#bandwidth option[value="80"]').click()
        time.sleep(1)

        # Side band
        side_band = driver.find_element_by_css_selector('#sideband')
        ActionChains(driver).move_to_element(side_band).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#sideband option[value="upper"]').click()
        time.sleep(1)

        # Click to Canal de controle
        channel = driver.find_element_by_css_selector('#channel')
        ActionChains(driver).move_to_element(channel).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#channel option[value="161"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '80', 'upper', '161']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 12. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 12. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('12. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            pass

        self.assertListEqual(list_steps_fail, [], '[UI_WR_11] Assertion 5GHZ Channel Control settings fail')

    def test_UI_WR_12(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 2g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4 Beamforming = Disable
        beamforming = driver.find_element_by_css_selector('#beamforming')
        ActionChains(driver).move_to_element(beamforming).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#beamforming option[value="true"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertTrue(actual)
            self.list_steps.append(
                '\n[Pass] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
            list_steps_fail.append('4. Check Value of Beamforming is Enable is true wrong: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5 Beamforming = Disable
        beamforming = driver.find_element_by_css_selector('#beamforming')
        ActionChains(driver).move_to_element(beamforming).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#beamforming option[value="false"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
            list_steps_fail.append('5. Check Value of Beamforming is Disable is false wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_12] Assertion 2.4GHZ Beamforming settings fail')

    def test_UI_WR_13(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 5g
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # Check Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler') != 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4 Beamforming = Disable
        beamforming = driver.find_element_by_css_selector('#beamforming')
        ActionChains(driver).move_to_element(beamforming).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#beamforming option[value="true"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertTrue(actual)
            self.list_steps.append(
                '\n[Pass] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
            list_steps_fail.append('4. Check Value of Beamforming is Enable is true wrong: ' + str(actual))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5 Beamforming = Disable
        beamforming = driver.find_element_by_css_selector('#beamforming')
        ActionChains(driver).move_to_element(beamforming).click().perform()
        time.sleep(2)
        driver.find_element_by_css_selector('#beamforming option[value="false"]').click()
        time.sleep(1)

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
            list_steps_fail.append('5. Check Value of Beamforming is Disable is false wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_13] Assertion 5GHZ Beamforming settings fail')

    def test_UI_WR_14(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 2g
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Click Varredura de pontos de acesso Wifi
        scan_btn = driver.find_element_by_css_selector('button[value="Varredura de pontos de acesso Wi-Fi"]')
        ActionChains(driver).move_to_element(scan_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        time.sleep(1)
        driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        driver.find_element_by_css_selector('button[value=refresh]').click()
        time.sleep(2)
        api_wifi_scan_result = Helper.Helper_common.api_wifi_scanResult(0)
        list_wifi = driver.find_elements_by_css_selector('ul.list >li')

        expected = []
        actual = []
        for ele in api_wifi_scan_result:
            expected.append([ele['ssid'], ele['security'], ele['mode'], ele['phyMode'],
                             ele['rssi'], ele['channel'], ele['bandwidth'], ele['macAddress']])

        for ele in list_wifi:
            block = []
            for front in ele.text.splitlines():
                block.append(front.split(': ')[1])
            actual.append(block)
        try:
            self.assertEqual(len(expected), len(actual))
            self.list_steps.append('\n[Pass] 4.1 Check quantity of result: ' + str(len(actual)))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check quantity of result: ' + str(len(actual)))
            list_steps_fail.append('\n4.1 Check quantity of result wrong: \nActual: ' + str(len(actual))
                                   + '\nExpected: ' + str(len(expected)))
            pass

        for i in range(len(actual)):
            for j in range(len(expected)):
                if actual[i][0] == expected[j][0]:
                    try:
                        self.assertListEqual(expected[j], actual[i])
                        self.list_steps.append(
                            '\n[Pass] 4.' + str(i) + ' Check Wifi list information: ' + str(actual[i]))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 4.' + str(i) + ' Check Wifi list information: ' + str(actual[i]))
                        list_steps_fail.append('\n4. Check Wifi info of ' + actual[i][0] + ' wrong: \nActual: '
                                               + str(actual[i]) + '\nExpected: ' + str(expected[j]))
                        pass
                    break
                else:
                    continue

        self.assertListEqual(list_steps_fail, [], '[UI_WR_14] Assertion Wi-Fi Access point scanning fail')

    def test_UI_WR_15(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver.get(ipv4 + '/#page-wifi-radio')
        expected_url = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2.URL page Wifi Radio display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'radio.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'comparator.js',
                    'srv_wifi.js',
                    'wifi',
                    'about',
                    'menu_main.js',
                    'radio',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Wifi Radio page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Wifi Radio page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Wifi Radio page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_WR_15] Assertion wrong')
 

class PageWifiConnectedEquip(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_WCE_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-connected-equip"]').click()
        expected_url_target = ipv4 + '/#page-wifi-connected-equip'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 2g
        driver.find_element_by_css_selector('[for="2g"]').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Modo restrito por MAC -> Desacticado
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission >option[value=disabled]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(7)
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(0)
        try:
            self.assertFalse(api_wifi_access_control['active'])
            self.list_steps.append(
                '\n[Pass] 4. Check API when choose Desaticado: ' + str(api_wifi_access_control['active']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Check API when choose Desaticado: ' + str(api_wifi_access_control['active']))
            self.list_steps.append(
                '\n4. Check API when choose Desaticado wrong ' + str(api_wifi_access_control['active']))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Modo restrito por MAC -> Negar
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission >option[value=deny]').click()
        time.sleep(1)

        for i in range(1, 21):
            mac_value = '11:12:13:14:15:' + str("{:02d}".format(i))
            # MAC input
            mac_input = driver.find_element_by_css_selector('#mac-input')
            ActionChains(driver).move_to_element(mac_input).click().send_keys(mac_value).perform()
            # Click Apply
            apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            time.sleep(10)
            count_time = 0
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            while len(pop_up_wait) == 1:
                pop_up_wait = driver.find_elements_by_css_selector('.msgText')
                time.sleep(1)
                count_time += 1
                if count_time >= 300:
                    break
            self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
            api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(0)
            actual = [api_wifi_access_control['active'], api_wifi_access_control['rules'][i - 1]['macAddress']]
            expected = [True, mac_value]
            try:
                self.assertListEqual(actual, expected)
                self.list_steps.append(
                    '\n[Pass] 5.' + str(i) + ' Check API Active, macAddress return: ' + str(actual))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 5.' + str(i) + ' Check API Active, macAddress return: ' + str(actual))
                self.list_steps.append(
                    '\n5.' + str(i) + ' Check API Active, macAddress return wrong: ' + str(actual))
                pass
        mac_value = '11:12:13:14:15:21'
        # MAC input
        mac_input = driver.find_element_by_css_selector('#mac-input')
        ActionChains(driver).move_to_element(mac_input).click().send_keys(mac_value).perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        # Check error
        check_error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('6. [Pass] Check the red error cell')
        except AssertionError:
            self.list_steps.append('6. [Fail] Check the red error cell')
            list_steps_fail.append('6. Check the red error wrong')
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Modo restrito por MAC -> Permitir
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission >option[value=allow]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(0)
        try:
            self.assertTrue(api_wifi_access_control['allow'])
            self.list_steps.append(
                '\n[Pass] 7. Check API when choose Permitir: ' + str(api_wifi_access_control['allow']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check API when choose Permitir: ' + str(api_wifi_access_control['allow']))
            self.list_steps.append(
                '\n7. Check API when choose Permitir wrong: ' + str(api_wifi_access_control['allow']))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Filtro de MAC baseado Probe Response -> Ativado
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select/option[@value="true"]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(0)
        try:
            self.assertTrue(api_wifi_access_control['probeResponse'])
            self.list_steps.append(
                '\n[Pass] 8. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
            self.list_steps.append(
                '\n8. Check API when choose Ativado wrong: ' + str(api_wifi_access_control['probeResponse']))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Filtro de MAC baseado Probe Response -> Desativado
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select/option[@value="false"]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(0)
        try:
            self.assertFalse(api_wifi_access_control['probeResponse'])
            self.list_steps.append(
                '\n[Pass] 9. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
            self.list_steps.append(
                '\n9. Check API when choose Ativado wrong: ' + str(api_wifi_access_control['probeResponse']))

        self.assertListEqual(list_steps_fail, [], '[UI_WCE_01] Assertion 2.4GHz connected equipments fail')

    def test_UI_WCE_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-connected-equip"]').click()
        expected_url_target = ipv4 + '/#page-wifi-connected-equip'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(2)
        # Click to 5g
        driver.find_element_by_css_selector('[for="5g"]').click()
        time.sleep(1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Modo restrito por MAC -> Desacticado
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission >option[value=disabled]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(7)
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(1)
        try:
            self.assertFalse(api_wifi_access_control['active'])
            self.list_steps.append(
                '\n[Pass] 4. Check API when choose Desaticado: ' + str(api_wifi_access_control['active']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Check API when choose Desaticado: ' + str(api_wifi_access_control['active']))
            self.list_steps.append(
                '\n4. Check API when choose Desaticado wrong ' + str(api_wifi_access_control['active']))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Modo restrito por MAC -> Negar
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission >option[value=deny]').click()
        time.sleep(1)

        for i in range(1, 21):
            mac_value = '11:12:13:14:15:' + str("{:02d}".format(i))
            # MAC input
            mac_input = driver.find_element_by_css_selector('#mac-input')
            ActionChains(driver).move_to_element(mac_input).click().send_keys(mac_value).perform()
            # Click Apply
            apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            time.sleep(10)
            count_time = 0
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            while len(pop_up_wait) == 1:
                pop_up_wait = driver.find_elements_by_css_selector('.msgText')
                time.sleep(1)
                count_time += 1
                if count_time >= 300:
                    break
            self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
            api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(1)
            actual = [api_wifi_access_control['active'], api_wifi_access_control['rules'][i - 1]['macAddress']]
            print(i)
            expected = [True, mac_value]
            try:
                self.assertListEqual(actual, expected)
                self.list_steps.append(
                    '\n[Pass] 5.' + str(i) + ' Check API Active, macAddress return: ' + str(actual))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 5.' + str(i) + ' Check API Active, macAddress return: ' + str(actual))
                self.list_steps.append(
                    '\n5.' + str(i) + ' Check API Active, macAddress return wrong: ' + str(actual))
                pass
        mac_value = '11:12:13:14:15:21'
        # MAC input
        mac_input = driver.find_element_by_css_selector('#mac-input')
        ActionChains(driver).move_to_element(mac_input).click().send_keys(mac_value).perform()
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        # Check error
        check_error = driver.find_elements_by_css_selector('.f-wrap.error')
        try:
            self.assertNotEqual(0, len(check_error))
            self.list_steps.append('6. [Pass] Check the red error cell')
        except AssertionError:
            self.list_steps.append('6. [Fail] Check the red error cell')
            list_steps_fail.append('6. Check the red error wrong')
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Modo restrito por MAC -> Permitir
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission >option[value=allow]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(1)
        try:
            self.assertTrue(api_wifi_access_control['allow'])
            self.list_steps.append(
                '\n[Pass] 7. Check API when choose Permitir: ' + str(api_wifi_access_control['allow']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check API when choose Permitir: ' + str(api_wifi_access_control['allow']))
            self.list_steps.append(
                '\n7. Check API when choose Permitir wrong: ' + str(api_wifi_access_control['allow']))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Filtro de MAC baseado Probe Response -> Ativado
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select/option[@value="true"]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(1)
        try:
            self.assertTrue(api_wifi_access_control['probeResponse'])
            self.list_steps.append(
                '\n[Pass] 8. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
            self.list_steps.append(
                '\n8. Check API when choose Ativado wrong: ' + str(api_wifi_access_control['probeResponse']))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click Filtro de MAC baseado Probe Response -> Desativado
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select/option[@value="false"]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(1)
        try:
            self.assertFalse(api_wifi_access_control['probeResponse'])
            self.list_steps.append(
                '\n[Pass] 9. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check API when choose Ativado: ' + str(api_wifi_access_control['probeResponse']))
            self.list_steps.append(
                '\n9. Check API when choose Ativado wrong: ' + str(api_wifi_access_control['probeResponse']))

        self.assertListEqual(list_steps_fail, [], '[UI_WCE_02] Assertion 5GHz connected equipments fail')

    def test_UI_WCE_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-connected-equip"]').click()
        expected_url_target = ipv4 + '/#page-wifi-connected-equip'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Wifi Radio wrong: ' + driver.current_url)
        time.sleep(4)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click to 2g
        driver.find_element_by_css_selector('[for="2g"]').click()
        time.sleep(1)
        remove_tick = driver.find_elements_by_css_selector('.radio-check')
        for i in remove_tick:
            ActionChains(driver).move_to_element(i).click().perform()
            time.sleep(0.1)
        # Click remove
        remove_btn = driver.find_element_by_css_selector('#remove-mac')
        ActionChains(driver).move_to_element(remove_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(0)
        actual = api_wifi_access_control['rules']
        try:
            self.assertEqual(len(actual), 0)
            self.list_steps.append(
                '\n[Pass] 5. Check Number of rules when Remover list Mac Address: ' + str(len(actual)))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Number of rules when Remover list Mac Address: ' + str(len(actual)))
            self.list_steps.append(
                '\n5. Check Number of rules when Remover list Mac Address wrong: ' + str(len(actual)))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Click to 5g
        time.sleep(2)
        driver.find_element_by_css_selector('[for="5g"]').click()
        time.sleep(1)
        remove_tick = driver.find_elements_by_css_selector('.radio-check')
        for i in remove_tick:
            ActionChains(driver).move_to_element(i).click().perform()
            time.sleep(0.1)
        # Click remove
        remove_btn = driver.find_element_by_css_selector('#remove-mac')
        ActionChains(driver).move_to_element(remove_btn).click().perform()
        count_time = 0
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        api_wifi_access_control = Helper.Helper_common.api_wifi_accessControl(1)
        actual = api_wifi_access_control['rules']
        try:
            self.assertEqual(len(actual), 0)
            self.list_steps.append(
                '\n[Pass] 8. Check Number of rules when Remover list Mac Address: ' + str(len(actual)))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check Number of rules when Remover list Mac Address: ' + str(len(actual)))
            self.list_steps.append(
                '\n8. Check Number of rules when Remover list Mac Address wrong: ' + str(len(actual)))
        self.assertListEqual(list_steps_fail, [], '[UI_WCE_03] Assertion Remove connected equipments fail')

    def test_UI_WCE_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver.get(ipv4 + '/#page-wifi-connected-equip')
        expected_url = ipv4 + '/#page-wifi-connected-equip'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Wifi Connected Equip: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Wifi Connected Equip: ' + driver.current_url)
            list_steps_fail.append('2.URL page Wifi Connected Equip display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'util.js',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'main.js',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'connected_equip.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_combobox.js',
                    'cmp_fieldinput.js',
                    'cmp_headresult.js',
                    'messagebox.js',
                    'srv_wifi.js',
                    'comparator.js',
                    'wifi',
                    'about',
                    'menu_main.js',
                    'ssid',
                    'devices?connected=true&interface=2.4g',
                    'accessControl',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Wifi Connected Equip page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Wifi Connected Equip page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Wifi Connected Equip page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_WCE_04] Assertion wrong')


class PageAdminRouterPassword(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_ARP_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click Senha roteador
        driver.find_element_by_css_selector('a[href="#page-admin-router-password"]').click()
        expected_url_target = ipv4 + '/#page-admin-router-password'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Admin Router Password: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Admin Router Password: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Admin Router Password wrong: ' + driver.current_url)
        time.sleep(2)

        # Click to Senha atual da ID de ...
        old_pw = driver.find_element_by_css_selector('#senha-atual')
        ActionChains(driver).move_to_element(old_pw).click().send_keys(pass_word).perform()
        # New password
        new_pw_value = "A-Z,a-z,0-9,-_(){}[]|/?,.~`!@$%^*;"
        new_pw = driver.find_element_by_css_selector('#nova-senha')
        ActionChains(driver).move_to_element(new_pw).click().send_keys(new_pw_value).perform()
        new_pw_verify = driver.find_element_by_css_selector('#nova-senha').get_attribute('value')
        try:
            self.assertEqual(len(new_pw_verify), 16)
            self.list_steps.append('\n[Pass] 3.1 Check New Password 16 characters: ' + str(len(new_pw_verify)))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Check New Password 16 characters: ' + str(len(new_pw_verify)))
            list_steps_fail.append('3.1 New Password is not contain 16 characters when input more than 16 characters: '
                                   + str(len(new_pw_verify)))
            pass
        # Repeat New password
        new_pw = driver.find_element_by_css_selector('#repetir-nova-senha')
        ActionChains(driver).move_to_element(new_pw).click().send_keys(new_pw_value).perform()

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        #
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./get_info.py /SERIAL ''' + com + ''' /BAUD 115200''')
        time.sleep(7)
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/ifconfig.txt'))
        pass_word_verify = config.get('USER_INFO', 'pw')

        # Login
        Helper.Helper_common.check_login(driver, self, ipv4)

        driver.find_element_by_id('login').send_keys(user)
        driver.find_element_by_id('senha').send_keys(pass_word_verify)
        driver.find_element_by_xpath('//button[@value="Entrar"]').click()
        time.sleep(2)
        expected_quick_setup = ipv4 + '/#page-quick-setup'

        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 4. Login to Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Login to Quick setup: ' + driver.current_url)
            list_steps_fail.append('4. Login to Quick Setup Fail: ' + driver.current_url)

        self.assertListEqual(list_steps_fail, [],
                             '[UI_ARP_01] Assertion Change admin router password with special characters fail')

    def test_UI_ARP_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver.get(ipv4 + '/#page-admin-router-password')
        expected_url = ipv4 + '/#page-admin-router-password'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Admin Router Password: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Admin Router Password: ' + driver.current_url)
            list_steps_fail.append('2.URL page Admin Router Password display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'futubd.woff',
                    'main.js',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'router_password.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'cmp_headresult.js',
                    'comparator.js',
                    'messagebox.js',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Admin Router Password page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Admin Router Password page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Admin Router Password page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_ARP_02] Assertion wrong')


class PageAdminDiagnostics(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_ADI_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click Diagnostics
        driver.find_element_by_css_selector('a[href="#page-admin-diagnostics"]').click()
        expected_url_target = ipv4 + '/#page-admin-diagnostics'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Admin Diagnostics: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Admin Diagnostics: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Admin Diagnostics wrong: ' + driver.current_url)
        time.sleep(2)

        # Utilitário > Ping
        driver.find_element_by_css_selector('#combo-1').click()
        ping = driver.find_element_by_css_selector('#combo-1 [value=Ping]').click()
        # Endereço IP / Domínio:
        ip = 'google.com'
        domain = driver.find_element_by_css_selector('#alvo')
        ActionChains(driver).move_to_element(domain).click().send_keys(ip).perform()
        size = driver.find_element_by_css_selector('#tamanho-do-ping').get_attribute('value')
        count = driver.find_element_by_css_selector('#n-de-pings').get_attribute('value')
        interval = driver.find_element_by_css_selector('#intervalo-do-ping').get_attribute('value')
        # Start test
        start_test = driver.find_element_by_css_selector('button[value="Começar teste"]')
        ActionChains(driver).move_to_element(start_test).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')

        result_actual = driver.find_element_by_css_selector('#result').get_attribute('value')
        api_diagnostics_ping = Helper.Helper_common.api_diagnostics_ping(ip, int(size), int(count), int(interval))
        if not len(api_diagnostics_ping['msg']):
            result_expected = ''
        else:
            result_expected = ''
            for i in api_diagnostics_ping['msg']:
                result_expected += i

        try:
            self.assertEqual(result_actual, result_expected)
            self.list_steps.append('\n[Pass] 4. Check API return from Return box: ' + result_actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API return from Return box: ' + result_actual)
            list_steps_fail.append('4. API return from Return box wrong: ' + result_actual)

        self.assertListEqual(list_steps_fail, [], '[UI_AD_01] Assertion Ping diagnostic fail')

    def test_UI_ADI_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click Diagnostics
        driver.find_element_by_css_selector('a[href="#page-admin-diagnostics"]').click()
        expected_url_target = ipv4 + '/#page-admin-diagnostics'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Admin Admin Diagnostics: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Admin Diagnostics: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Admin Diagnostics wrong: ' + driver.current_url)
        time.sleep(2)

        # Utilitário > Traceroute
        driver.find_element_by_css_selector('#combo-1').click()
        ping = driver.find_element_by_css_selector('#combo-1 [value=Traceroute]').click()
        # Endereço IP / Domínio:
        ip = 'google.com'
        domain = driver.find_element_by_css_selector('#alvo')
        ActionChains(driver).move_to_element(domain).click().send_keys(ip).perform()

        # Start test
        start_test = driver.find_element_by_css_selector('button[value="Começar teste"]')
        ActionChains(driver).move_to_element(start_test).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')

        result_actual = driver.find_element_by_css_selector('#result').get_attribute('value')
        api_diagnostics_routehops = Helper.Helper_common.api_diagnostics_routehops()
        if not len(api_diagnostics_routehops['msg']):
            result_expected = ''
        else:
            result_expected = ''
            for i in api_diagnostics_routehops['msg']:
                result_expected += i

        try:
            self.assertEqual(result_actual, result_expected)
            self.list_steps.append('\n[Pass] 4. Check API return from Return box: ' + result_actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API return from Return box: ' + result_actual)
            list_steps_fail.append('4. API return from Return box wrong: ' + result_actual)

        self.assertListEqual(list_steps_fail, [], '[UI_AD_02] Assertion Traceroute diagnostic fail')

    def test_UI_ADI_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click Diagnostics
        driver.find_element_by_css_selector('a[href="#page-admin-diagnostics"]').click()
        expected_url_target = ipv4 + '/#page-admin-diagnostics'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Admin Admin Diagnostics: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Admin Diagnostics: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Admin Diagnostics wrong: ' + driver.current_url)
        time.sleep(2)

        clear_test_result = driver.find_element_by_css_selector('button[value="Limpar resultados"]')
        ActionChains(driver).move_to_element(clear_test_result).click().perform()
        result_actual = driver.find_element_by_css_selector('#result').get_attribute('value')
        try:
            self.assertEqual(result_actual, '')
            self.list_steps.append('\n[Pass] 3. Check API return from Return box: ' + result_actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API return from Return box: ' + result_actual)
            list_steps_fail.append('3. API return from Return box wrong: ' + result_actual)
        self.assertListEqual(list_steps_fail, [], '[UI_AD_03] Assertion Clear test results fail')

    def test_UI_ADI_04(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver.get(ipv4 + '/#page-admin-diagnostics')
        expected_url = ipv4 + '/#page-admin-diagnostics'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Admin Diagnostics: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Admin Diagnostics: ' + driver.current_url)
            list_steps_fail.append('2.URL page Admin Diagnostics display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'diagnostics.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'srv_service.js',
                    'messagebox.js',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Admin Diagnostics page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Admin Diagnostics page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Admin Diagnostics page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_ADI_04] Assertion wrong')


class PageAdminBackup(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_AB_01(self):
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click Diagnostics
        driver.find_element_by_css_selector('a[href="#page-admin-backup"]').click()
        expected_url_target = ipv4 + '/#page-admin-backup'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Admin Backup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Admin Backup: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Admin Backup wrong: ' + driver.current_url)
        time.sleep(2)
        driver.find_element_by_css_selector('button[value=Backup]').click()

        with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
           Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
        exists = os.path.isfile(os.path.join(Downloads, 'backupsettings.conf'))
        try:
            self.assertTrue(exists)
            self.list_steps.append('\n[Pass] 3. Check File backupsettings.conf in Download folder ')
        except FileNotFoundError:
            self.list_steps.append('\n[Pass] 3. Check File backupsettings.conf in Download folder ' )
            list_steps_fail.append('3. File backupsettings.conf is not in Download folder ')

        self.assertListEqual(list_steps_fail, [], '[UI_AB_01] Assertion Backup Configuration fail')

    def test_UI_AB_02(self):
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./restore_default.py /SERIAL '''
            + com + ''' /BAUD 115200''')
        time.sleep(120)
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        time.sleep(2)

        # Click to 2.4 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(3)
        # Name
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        expected_2g_name = name.get_attribute('value')
        keys_name = '1234567890123'
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()
        # Password
        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """12345678"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()
        # Click Submit
        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        # Confirm name of 2.4 G changed
        time.sleep(5)
        confirm_name = driver.find_element_by_css_selector('[id="2g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="2g-network-name"] strong').text
        time.sleep(5)
        try:
            self.assertEqual(actual_name, keys_name[:31])
            self.list_steps.append('\n[Pass] 3. Display Name: ' + str(actual_name))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.Display Name: ' + str(actual_name))
            list_steps_fail.append('3. Name display wrong: ' + str(actual_name))

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click backup
        driver.find_element_by_css_selector('a[href="#page-admin-backup"]').click()
        expected_url_target = ipv4 + '/#page-admin-backup'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 4. Check URL of Page Admin Backup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check URL of Page Admin Backup: ' + driver.current_url)
            list_steps_fail.append('4. URL Page Admin Backup wrong: ' + driver.current_url)
        time.sleep(2)
        # Click Escolher arquivo
        driver.find_element_by_css_selector('[for=arquivo]').click()
        time.sleep(1)
        # Uplaod path of backupsettings.conf
        with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
           Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
        file_path = os.path.join(Downloads, 'backupsettings.conf')
        app = Application().connect(title_re="Open")
        app.Open.Edit.type_keys(file_path)
        time.sleep(2)
        app.Open.Open.click()
        time.sleep(2)
        # Click Restaurar
        driver.find_element_by_css_selector('button[value="Restaurar"]').click()
        time.sleep(1)
        # Click OK
        driver.find_element_by_css_selector('.msgBtn#ok').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        # Login again
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(5)
        actual_2g_name = driver.find_element_by_css_selector('[id="wifi-net-name"]').get_attribute('value')
        try:
            self.assertEqual(expected_2g_name, actual_2g_name)
            self.list_steps.append('\n[Pass] 8. Check 2G name is same as previous name: ' + actual_2g_name)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Check 2G name is same as previous name: ' + actual_2g_name)
            list_steps_fail.append('8. 2G name is not same as previous name: ' + actual_2g_name)

        self.assertListEqual(list_steps_fail, [], '[UI_AB_02] Assertion Restore Configuration fail')

    def test_UI_AB_03(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        Helper.Helper_common.login(driver, self, ipv4)
        # Click status IP Connection
        driver.get(ipv4 + '/#page-admin-backup')
        expected_url = ipv4 + '/#page-admin-backup'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Admin Backup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Admin Backup: ' + driver.current_url)
            list_steps_fail.append('2.URL page Admin Backup display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'util.js',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'backup.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'messagebox.js',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Admin Backup page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Admin Backup page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Admin Backup page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_AB_03] Assertion wrong')


class PageAdminFactoryDefault(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')
        driver = self.driver
        driver.maximize_window()
        Helper.Helper_common.login(driver, self, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration, final_report)
        self.driver.quit()

    def test_UI_AFD_01(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)

        # Click to 2.4 GHZ
        time.sleep(5)
        click_type = driver.find_element_by_xpath('//label[@for="2-4-ghz"]')
        ActionChains(driver).move_to_element(click_type).click().perform()
        time.sleep(3)
        # Name
        name = driver.find_element_by_css_selector('[id="wifi-net-name"]')
        # expected_2g_name = name.get_attribute('value')
        keys_name = '000000_______1234567890123'
        ActionChains(driver).move_to_element(name).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(keys_name).perform()
        # Password
        time.sleep(1)
        new_pw = driver.find_element_by_css_selector('#wifi-net-password.input')
        keys_send = """12345678"""
        ActionChains(driver).move_to_element(new_pw).click().send_keys(keys_send).perform()
        time.sleep(1)
        re_new_pw = driver.find_element_by_css_selector('#re-wifi-net-password.input')
        ActionChains(driver).move_to_element(re_new_pw).click().send_keys(keys_send).perform()
        # Click Submit
        submit = driver.find_element_by_css_selector('.holder-icon')
        ActionChains(driver).move_to_element(submit).click().perform()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        # Confirm name of 2.4 G changed
        time.sleep(5)
        confirm_name = driver.find_element_by_css_selector('[id="2g-network-name"]')
        ActionChains(driver).move_to_element(confirm_name).perform()
        actual_name = driver.find_element_by_css_selector('[id="2g-network-name"] strong').text
        time.sleep(5)
        try:
            self.assertEqual(actual_name, keys_name[:31])
            self.list_steps.append('\n[Pass] 3. Display Name: ' + str(actual_name))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.Display Name: ' + str(actual_name))
            list_steps_fail.append('3. Name display wrong: ' + str(actual_name))
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 4.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('4. URL Configuration Advance wrong: ' + driver.current_url)
        time.sleep(1)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Admin
        driver.find_element_by_css_selector('[for=menu-administracao]').click()
        time.sleep(1)
        # Click Configuration default
        driver.find_element_by_css_selector('a[href="#page-admin-factory-defaults"]').click()
        expected_url_target = ipv4 + '/#page-admin-factory-defaults'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 4. Check URL of Page Admin Factory Default: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check URL of Page Admin Factory Default: ' + driver.current_url)
            list_steps_fail.append('4. URL Page Admin Factory Default wrong: ' + driver.current_url)
        time.sleep(2)
        # Click SIM
        driver.find_element_by_css_selector('[for="restaurar-de-fabrica-sim"]').click()
        time.sleep(1)
        # Click Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('.msgBtn#ok').click()
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        count_time = 0
        while len(pop_up_wait) == 1:
            pop_up_wait = driver.find_elements_by_css_selector('.msgText')
            time.sleep(1)
            count_time += 1
            if count_time >= 300:
                break
        self.assertLessEqual(count_time, 300, 'Pop-up change PW was timeout > 5 minutes')
        # Wait for reboot router
        time.sleep(60)
        Helper.Helper_common.login(driver, self, ipv4)
        time.sleep(5)

        # Name
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]')
        name_2g = name_2g.text
        check_list_2g = [name_2g.startswith('NET_2G'), len(name_2g[6:]) == 6, name_2g.isupper(), ':' not in name_2g]
        expected_list_check_name = [True, True, True, True]
        try:
            self.assertListEqual(check_list_2g, expected_list_check_name)
            self.list_steps.append(
                '\n[Pass] 6.1 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.1 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
            list_steps_fail.append(
                '6.1 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon not in name :'
                + str(check_list_2g))

        name_5g = driver.find_element_by_css_selector('[id="5g-network-name"]')
        name_5g = name_5g.text
        check_list_5g = [name_5g.startswith('NET_5G'), len(name_5g[6:]) == 6, name_5g.isupper(), ':' not in name_5g]

        try:
            self.assertListEqual(check_list_5g, expected_list_check_name)
            self.list_steps.append(
                '\n[Pass] 6.2 Check condition: Start with NET_5G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.2 Check condition: Start with NET_2G, 6 characters at the end, is upper, colon in name :'
                + str(check_list_2g))
            list_steps_fail.append(
                '6.2. Check condition: Start with NET_2G, 6 characters at the end, is upper, colon not in name :'
                + str(check_list_2g))

        expected_list_check_pw = [True, True, True]
        pw_5g = driver.find_element_by_css_selector('[id="5g-network-password"]')
        ActionChains(driver).move_to_element(pw_5g).perform()
        pw_5g = pw_5g.text
        check_condition_5g = [len(pw_5g) == 8, pw_5g.isupper(), ':' not in pw_5g]
        try:
            self.assertListEqual(check_condition_5g, expected_list_check_pw)
            self.list_steps.append(
                '\n[Pass] 6.3 Check condition: 8 characters, is upper, colon  in PW :' + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.3 Check condition:8 characters, is upper, colon  in PW :' + str(check_list_2g))
            list_steps_fail.append(
                '6.3 Check condition: 8 characters, is upper, colon not in PW :' + str(check_list_2g))
            pass

        pw_2g = driver.find_element_by_css_selector('[id="2g-network-password"]')
        ActionChains(driver).move_to_element(pw_2g).perform()
        pw_2g = pw_2g.text
        check_condition_2g = [len(pw_2g) == 8, pw_2g.isupper(), ':' not in pw_2g]
        try:
            self.assertListEqual(check_condition_2g, expected_list_check_pw)
            self.list_steps.append(
                '\n[Pass] 6.4. Check condition: 8 characters, is upper, colon  in PW :' + str(check_list_2g))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6.4 Check condition:8 characters, is upper, colon  in PW :' + str(check_list_2g))
            list_steps_fail.append(
                '6.4 Check condition: 8 characters, is upper, colon not in PW :' + str(check_list_2g))

        self.assertListEqual(list_steps_fail, [], '[UI_AD_01] Assertion Ping diagnostic fail')

    def test_UI_AFD_02(self):
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        driver = self.driver
        # Click status IP Connection
        driver.get(ipv4 + '/#page-admin-factory-defaults')
        expected_url = ipv4 + '/#page-admin-factory-defaults'
        try:
            self.assertEqual(driver.current_url, expected_url)
            self.list_steps.append('\n[Pass] 2. Check Page Admin Factory Default: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2. Check Page Admin Factory Default: ' + driver.current_url)
            list_steps_fail.append('2.URL page Admin Factory Default display wrong' + driver.current_url)
        time.sleep(3)
        web_components = Helper.Helper_common.get_wenui_components(driver)
        expected = ['192.168.0.1',
                    'login.css',
                    'structure.css',
                    'logo-net.png',
                    'require.js',
                    'jquery.js',
                    'jquery.base64.js',
                    'jquery.li18n.js',
                    'define.js',
                    'util.js',
                    'main.js',
                    'futubd.woff',
                    'futuram.woff',
                    'futult.woff',
                    'roboto-regular.woff',
                    'roboto-medium.woff',
                    'icons-net.ttf',
                    'config.json',
                    'page_manager.js',
                    'srv_gateway.js',
                    'factory_defaults.js',
                    'cmp_basic.js',
                    'cmp_form.js',
                    'messagebox.js',
                    'about',
                    'menu_main.js',
                    'srv_network.js',
                    'wan'
                    ]

        value_wrong = []
        for e in expected:
            if e not in [i[0] for i in web_components]:
                value_wrong.append(str(e) + 'not found')
            else:
                for w in web_components:
                    if w[0] == e:
                        if w[1] != 'OK':
                            value_wrong.append(w)
        try:
            self.assertListEqual(value_wrong, [])
            self.list_steps.append('\n[Pass] 3. Check API return wrong on Admin Factory Default page.')
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 3. Check API return wrong on Admin Factory Default page. \nActual: %s' % (
                    str(value_wrong)))
            list_steps_fail.append(
                '3. API return on Admin Factory Default page: \nActual: %s' % (str(value_wrong)))

        self.assertListEqual(list_steps_fail, [], '[UI_AFD_02] Assertion wrong')


if __name__ == '__main__':
    unittest.main()