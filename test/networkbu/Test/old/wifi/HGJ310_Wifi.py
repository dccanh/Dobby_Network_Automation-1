#$language = "python"
#$interface = "1.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
from pywinauto.application import Application
import glob
import HTMLTestRunner
import Helper.Helper_common
import re
from winreg import *
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class WF_2G_WR(unittest.TestCase):
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
        Helper.Helper_common.write_actual_excel(self.list_steps, self.def_name, duration)
        self.driver.quit()

    def test_WF_2G_WR_01(self):
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
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong. Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass

        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface, uncheck "ATIVAR" box and apply the setting
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # UnCheck Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
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
            self.list_steps.append('\n[Pass] 4. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API radio value return: ' + str(actual))
            list_steps_fail.append('4. API radio value return wrong. Actual: ' + str(actual) + ' Expected: ' + 'False')
            pass

        # 5. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 bss', 'wl1 radio', 'nvram get wl1_radio', 'uci show wireless.wl1.disabled']
        expected_uncheck = ['down', '0x0001', '0', "wireless.wl1.disabled='1'"]
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        path_cmd_value = '../Config/cmd_value.txt'
        actual_uncheck = []
        count = 0
        while 1:
            os.system('''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
                + rg_port + ''' /BAUD 115200''')
            config = configparser.ConfigParser()
            config.read_file(open(path_cmd_value, 'r'))
            try:
                for i in range(len(list_cmd)):
                    actual_uncheck.append(config.get('COMMAND', options[i]))
                break
            except KeyError and configparser.NoOptionError:
                a = open(path_cmd_value, 'w')
                a.write('')
                a.close()
                count += 1
                if count == 5:
                    break
        try:
            self.assertListEqual(actual_uncheck, expected_uncheck)
            self.list_steps.append(
                '\n[Pass] 5. Check Value return RG console when Uncheck ativar' + str(actual_uncheck))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Value return RG console when Uncheck ativar' + str(actual_uncheck))
            list_steps_fail.append('5. Value return RG console when Uncheck ativar return wrong: Actual: ' + str(actual_uncheck) + ' Expected: ' + str(expected_uncheck))
            pass
        time.sleep(20)
        # 6. From test PC, check SSID of 2.4 Ghz interface whether is in available wifi list or not

        check_ssid = Helper.Helper_common.show_network(name_2g)
        try:
            self.assertFalse(check_ssid)
            self.list_steps.append('\n[Pass] 6. Check 2G SSID is not in wifi list ')
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check 2G SSID is not in wifi list ')
            list_steps_fail.append('6. 2G SSID is in wifi list: Actual: ' + str(check_ssid) + ' Expected: ' + 'False')
            pass

        # 7. Check "ATIVAR" box and apply the setting
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 7. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Check API radio value return: ' + str(actual))
            list_steps_fail.append('7. API radio value return wrong. Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass

        # 8. Using the RG console to check the current configuration in wl driver by below commands:
        expected_check = ['up', '0x0000', '1', "wireless.wl1.disabled='0'"]
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        path_cmd_value = '../Config/cmd_value.txt'
        actual_check = []
        count = 0
        while 1:
            os.system('''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
                      + rg_port + ''' /BAUD 115200''')
            config = configparser.ConfigParser()
            config.read_file(open(path_cmd_value, 'r'))
            try:
                for i in range(len(list_cmd)):
                    actual_check.append(config.get('COMMAND', options[i]))
                break
            except KeyError and configparser.NoOptionError:
                a = open(path_cmd_value, 'w')
                a.write('')
                a.close()
                count += 1
                if count == 5:
                    break

        try:
            self.assertListEqual(actual_check, expected_check)
            self.list_steps.append(
                '\n[Pass] 8. Check Value return RG console when check ativar' + str(actual_check))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check Value return RG console when check ativar' + str(actual_check))
            list_steps_fail.append('8. Value return RG console when check ativar return wrong: Actual: ' + str(actual_check) + ' Expected: ' + str(expected_check))
            pass

        # 9. From test PC, check SSID of 2.4 Ghz interface whether is in available wifi list or not
        check_ssid = Helper.Helper_common.show_network(name_2g)
        try:
            self.assertTrue(check_ssid)
            self.list_steps.append('\n[Pass] 9. Check 2G SSID in wifi list ')
        except AssertionError:
            self.list_steps.append('\n[Fail] 9. Check 2G SSID in wifi list ')
            list_steps_fail.append('9. 2G SSID is not in wifi list: Actual: ' + str(check_ssid) + ' Expected: ' + 'True')
            pass

        # 10. Click "5 GHZ" to select 5 Ghz interface, uncheck "ATIVAR" box and apply the setting
        driver.find_element_by_css_selector('[for=radio5g]').click()
        time.sleep(1)
        # UnCheck Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = api_wifi_radio['active']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 10. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 10. Check API radio value return: ' + str(actual))
            list_steps_fail.append('10. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'False')

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_01] Assertion 2.4GHz wifi radio fail')

    def test_WF_2G_WR_02(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)

        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass

        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface and check the selected value of "Potência de saída" option on Web UI
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(1)
        # Click Alto
        driver.find_element_by_css_selector('#outputPower option[value=high]').click()
        time.sleep(2)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 4. Check Output Power is Alto: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check Output Power is Alto: ' + actual)
            list_steps_fail.append('4. Alto Output Power is wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 5. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 pwr_percent', 'nvram get wl1_txpwr_percent']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open('../Config/cmd_value.txt', 'r'))
        actual_uncheck = []
        for i in range(len(list_cmd)):
            actual_uncheck.append(config.get('COMMAND', options[i]))
        expected_uncheck = ['100', '100']

        try:
            self.assertListEqual(actual_uncheck, expected_uncheck)
            self.list_steps.append(
                '\n[Pass] 5. Check Value return RG console ' + str(actual_uncheck))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Value return RG console ' + str(actual_uncheck))
            list_steps_fail.append('5. Value return RG console wrong: Actual: ' + str(actual_uncheck) + ' Expected: ' + str(expected_uncheck))
        time.sleep(7)

        # 6. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(1)
        # Click Alto
        driver.find_element_by_css_selector('#outputPower option[value=medium]').click()
        time.sleep(2)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 6. Check Output Power is Medium: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check Output Power is Medium: ' + actual)
            list_steps_fail.append('6. Alto Output Power is wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 7. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 pwr_percent', 'nvram get wl1_txpwr_percent']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open('../Config/cmd_value.txt', 'r'))
        actual_uncheck = []
        for i in range(len(list_cmd)):
            actual_uncheck.append(config.get('COMMAND', options[i]))
        expected_uncheck = ['60', '60']
        try:
            self.assertListEqual(actual_uncheck, expected_uncheck)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual_uncheck))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual_uncheck))
            list_steps_fail.append('7. Value return RG console wrong: Actual: ' + str(actual_uncheck) + ' Expected: ' + str(expected_uncheck))
            pass
        time.sleep(7)

        # 8. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(1)
        # Click Alto
        driver.find_element_by_css_selector('#outputPower option[value=low]').click()
        time.sleep(2)
        expected = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        time.sleep(1)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 8. Check Output Power is Baixo: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Check Output Power is Baixo: ' + actual)
            list_steps_fail.append('8. Alto Output Power is wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 9. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 pwr_percent', 'nvram get wl1_txpwr_percent']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open('../Config/cmd_value.txt', 'r'))
        actual_uncheck = []
        for i in range(len(list_cmd)):
            actual_uncheck.append(config.get('COMMAND', options[i]))
        expected_uncheck = ['40', '40']

        try:
            self.assertListEqual(actual_uncheck, expected_uncheck)
            self.list_steps.append(
                '\n[Pass] 9. Check Value return RG console ' + str(actual_uncheck))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check Value return RG console ' + str(actual_uncheck))
            list_steps_fail.append('9. Value return RG console wrong: Actual: ' + str(actual_uncheck) + ' Expected: ' + str(expected_uncheck))
            pass
        time.sleep(7)

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_02] Assertion 2.4GHz output power fail')

    def test_WF_2G_WR_03(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong:Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass

        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Check Ativar
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'], api_wifi_radio['basic']['wirelessMode']]
        expected = [True, '802.11b+g+n']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface and change the "Modo 802.11.n" option to "Off" and apply setting
        # Click Modo 802.11n >off
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=off]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode']]
        expected = ['802.11b+g']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 4. Check API Wireless mode off: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API Wireless mode off: ' + str(actual))
            list_steps_fail.append('4. API Wireless mode off wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        #5. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['nvram get wl1_nmode', 'uci get wireless.@wifi-device[1].standard']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['0', 'b,g']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 5. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Value return RG console ' + str(actual))
            list_steps_fail.append('5. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Using the below command from Windows command prompt to get and check wifi network information
        scan_wf = Helper.Helper_common.scan_wifi(name_2g)
        actual_radio = scan_wf[0]
        expected_radio = '802.11g'
        if scan_wf != False:
            try:
                self.assertEqual(actual_radio, expected_radio)
                self.list_steps.append(
                    '\n[Pass] 6. Check Value of Radio type: ' + str(actual_radio))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 6. Check Value of Radio type: ' + str(actual_radio))
                list_steps_fail.append('6. Value of Radio type wrong: Actual: ' + str(actual_radio) + ' Expected: ' + str(expected_radio))
        else:
            try:
                self.assertTrue(scan_wf)
                self.list_steps.append(
                    '\n[Pass] 6. Check 2G SSID is exist in list Wifi: ' + str(actual_radio))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 6. Check 2G SSID is exist in list Wifi: ' + str(actual_radio))
                list_steps_fail.append('6. Check 2G SSID is exist wrong in list Wifi: Actual: ' + str(actual_radio) + ' Expected: ' + 'True')

        # 7. Click the "Modo 802.11.n" to change to "Auto" and apply setting
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=auto]').click()

        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode']]
        expected = ['802.11b+g+n']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 7. Check API Wireless mode auto: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Check API Wireless mode auto: ' + str(actual))
            list_steps_fail.append('7. API Wireless mode auto wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass


        # 8. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['nvram get wl1_nmode', 'uci get wireless.@wifi-device[1].standard']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['-1', 'b,g,n']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 8. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check Value return RG console ' + str(actual))
            list_steps_fail.append('8. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 9. Using the below command from Windows command prompt to get and check wifi network information
        scan_wf = Helper.Helper_common.scan_wifi(name_2g)
        actual_radio = scan_wf[0]
        expected_radio = '802.11n'
        if not scan_wf:
            try:
                self.assertEqual(actual_radio, expected_radio)
                self.list_steps.append(
                    '\n[Pass] 9. Check Value of Radio type: ' + str(actual_radio))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 9. Check Value of Radio type: ' + str(actual_radio))
                list_steps_fail.append('9. Value of Radio type wrong: Actual: ' + str(actual_radio) + ' Expected: ' + str(expected_radio))
        else:
            try:
                self.assertTrue(scan_wf)
                self.list_steps.append(
                    '\n[Pass] 9. Check 2G SSID is exist in list Wifi: ' + str(actual_radio))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 9. Check 2G SSID is exist in list Wifi: ' + str(actual_radio))
                list_steps_fail.append('9. Check 2G SSID is exist wrong in list Wifi: Actual: ' + str(actual_radio) + ' Expected: ' + 'True')

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_03] Assertion 2.4 GHz 802.11n mode fail')

    def test_WF_2G_WR_04(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
            list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # Check Ativar
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [True, '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface and change below options:
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Change Modo802.11n >auto
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=auto]').click()
        time.sleep(1)
        # Change Largura de banda > 20MHz
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="20"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [True, '20', '20']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 4. Check API Largura de banda = 20: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API Largura de banda = 20: ' + str(actual))
            list_steps_fail.append('4. API Largura de banda = 20 wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 5. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['wl -i wl1 bw_cap 2g', 'nvram get wl1_bw_cap',
                    'uci get wireless.wl1.htmode', 'latticecli -n "get WiFi.Radio.2.ConfiguredChannelBandwidth"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['0x1', '1', 'HT20', 'Success to get value from WiFi.Radio.2.ConfiguredChannelBandwidth: 1']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 5. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Value return RG console ' + str(actual))
            list_steps_fail.append('5. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Change "Largura de banda" option to "40MHz" and apply setting
        # Change Largura de banda > 20MHz
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="40"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [True, '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 6. Check API Largura de banda = 40: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check API Largura de banda = 40: ' + str(actual))
            list_steps_fail.append('6. API Largura de banda = 40 wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 7. Using the RG console to check the current configuration in wl driver by below commands
        time.sleep(1)
        list_cmd = ['wl -i wl1 bw_cap 2g', 'nvram get wl1_bw_cap',
                    'uci get wireless.wl1.htmode', 'latticecli -n "get WiFi.Radio.2.ConfiguredChannelBandwidth"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['0x3', '3', 'HT40+', 'Success to get value from WiFi.Radio.2.ConfiguredChannelBandwidth: 2']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual))
            list_steps_fail.append('7. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 8. Change "Modo 802.11.n" option to "Off " and apply setting
        # Change Modo802.11n >off
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=off]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)

        # Get list options of Largura de banda
        options = driver.find_elements_by_css_selector('#bandwidth > option')
        actual = []
        for i in options:
            actual.append(i.get_attribute('text'))
        expected = ['20MHz']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 8. Check List value of Largura de banda ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 8. Check List value of Largura de banda ' + str(actual))
            list_steps_fail.append('8. List value of Largura de banda wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_04] Assertion 2.4 GHz Bandwidth fail')

    def test_WF_2G_WR_05(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # Check Ativar
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler'):
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband']]
        expected = [True, '40', '40', 'lower']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface and change below options:
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Change Modo802.11n >auto
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=auto]').click()
        time.sleep(1)
        # Change Largura de banda > 40MHz
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="40"]').click()
        # Change Banda lateral para canal de controle > Alto
        driver.find_element_by_css_selector('#sideband').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#sideband > option[value="upper"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband']]
        expected = [True, '40', '40', 'upper']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 4.1 Check API Largura de banda = 20: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check API Largura de banda = 20: ' + str(actual))
            list_steps_fail.append('4.1 API Largura de banda = 20 wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # In the "Canal de controle" option, the available channel list should include channels: Auto; 5 -> 13
        channels = driver.find_elements_by_css_selector('#channel > option')
        actual = []
        for i in channels:
            actual.append(i.get_attribute('text'))

        expected = []
        [expected.append(str(i)) for i in range(5, 14)]
        expected.insert(0, 'Auto')
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 4.2 Check List value of Largura de banda ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4.2 Check List value of Largura de banda ' + str(actual))
            list_steps_fail.append('4.2 List value of Largura de banda wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 5. Change "Canal de controle" option to "6" and apply setting
        driver.find_element_by_css_selector('#channel > option[value="6"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['channel']['used'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband']]
        expected = ['6', '6', '40', '40', 'upper']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 5. Check API value: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check API value: ' + str(actual))
            list_steps_fail.append('5. API value wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['nvram get wl1_nctrlsb',
                    'wl -i wl1 chanspec',
                    'nvram get wl1_chanspec',
                    'latticecli -n "get WiFi.Radio.2.ExtensionChannel"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['AboveControlChannel',
                    '6u (0x1904)',
                    '6u',
                    'Success to get value from WiFi.Radio.2.ExtensionChannel: 1']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 6. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6. Check Value return RG console ' + str(actual))
            list_steps_fail.append('6. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 7. Change "Banda lateral para canal de controle" option to "Baixo" and apply setting
        driver.find_element_by_css_selector('#sideband').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#sideband > option[value="lower"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['sideband']]
        expected = ['lower']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 7.1 Check API: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7.1 Check API: ' + str(actual))
            list_steps_fail.append('7.1 API return wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # In the "Canal de controle" option, the available channel list should include channels: Auto; 1 -> 9
        channels = driver.find_elements_by_css_selector('#channel > option')
        actual = []
        for i in channels:
            actual.append(i.get_attribute('text'))

        expected = []
        [expected.append(str(i)) for i in range(1, 10)]
        expected.insert(0, 'Auto')
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7.2 Check Channel list ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7.2 Check Channel list ' + str(actual))
            list_steps_fail.append('7.2 Channel list wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 8. Change "Canal de controle" option to "5" and apply setting
        driver.find_element_by_css_selector('#channel > option[value="5"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['channel']['used'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband']]
        expected = ['6', '6', '40', '40', 'lower']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 8. Check API value: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Check API value: ' + str(actual))
            list_steps_fail.append('8. API value wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['nvram get wl1_nctrlsb',
                    'wl -i wl1 chanspec',
                    'nvram get wl1_chanspec',
                    'latticecli -n "get WiFi.Radio.2.ExtensionChannel"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['BelowControlChannel',
                    '66l (0x1808)',
                    '6l',
                    'Success to get value from WiFi.Radio.2.ExtensionChannel: 2']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 9. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check Value return RG console ' + str(actual))
            list_steps_fail.append('9. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 10. Change "Largura de banda" option to "20MHz" and apply setting
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="20"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        side_band = driver.find_element_by_css_selector('#sideband').get_property('disabled')
        try:
            self.assertTrue(side_band)
            self.list_steps.append(
                '\n[Pass] 10. Check Banda lateral True is disabled: ' + str(side_band))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 10. Check Banda lateral True is disabled: ' + str(side_band))
            list_steps_fail.append('10. Banda lateral True is disabled: Actual: ' + str(side_band) + ' Expected: ' + 'True')
            pass

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_05] Assertion 2.4 GHz side band control channel fail')

    def test_WF_2G_WR_06(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # Check default value of Ativar
        ativar_check = driver.find_element_by_class_name('radio-check-controler').get_property('checked')
        try:
            self.assertTrue(ativar_check)
            self.list_steps.append('\n[Pass] 3.1 Check Ativar box is checked by default: ' + str(ativar_check))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Check Ativar box is checked by default: ' + str(ativar_check))
            list_steps_fail.append('3.1 Ativar box is not checked by default: Actual: ' + str(ativar_check) + ' Expected: ' + 'True')
            pass
        # Check default value of Modo 802.11.n
        modo_value = driver.find_element_by_id('wirelessMode').get_attribute('value')
        expected_modo = 'auto'
        try:
            self.assertEqual(modo_value, expected_modo)
            self.list_steps.append('\n[Pass] 3.2 Check value of Modo box by default: ' + str(modo_value))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Check value of Modo box by default: ' + str(modo_value))
            list_steps_fail.append('3.2 Value of Modo box by default wrong: Actual: ' + str(modo_value) + ' Expected: ' + str(expected_modo))
            pass
        # Check default value of Cannal de controle
        channel_value = driver.find_element_by_id('channel').get_attribute('value')
        expected_channel = 'auto'
        try:
            self.assertEqual(channel_value, expected_channel)
            self.list_steps.append('\n[Pass] 3.3 Check value of Cannal de controle box by default: ' + str(channel_value))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.3 Check value of Cannal de controle box by default: ' + str(channel_value))
            list_steps_fail.append('3.3 Value of Cannal de controle box by default wrong: Actual: ' + str(channel_value) + ' Expected: ' + str(expected_channel))
            pass
        # Check API in default
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['active'],
                  api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['wirelessMode']]
        expected = [True, 'auto', '802.11b+g+n']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3.4 Check API radio value by default: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.4 Check API radio value by default: ' + str(actual))
            list_steps_fail.append('3.4 API radio value by default wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 4. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['uci get wireless.wl1.channel',
                    'nvram get wl1_channel']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['auto', '0']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 4. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Check Value return RG console ' + str(actual))
            list_steps_fail.append('4. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 5. Click "2.4 GHZ" to select 2.4 Ghz interface and change "Largura de banda" option to "20MHz" and apply
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        # Change Largura de banda > 20MHz
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="20"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = ['20', '20']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 5.1 Check API if Largura de banda changed: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 5.1 Check API if Largura de banda changed: ' + str(actual))
            list_steps_fail.append('5.1 API if Largura de banda changed wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # In the "Canal de controle" option, the available channel list should include channels: Auto; 1 -> 13
        channels = driver.find_elements_by_css_selector('#channel > option')
        actual = []
        for i in channels:
            actual.append(i.get_attribute('text'))
        # Create a list contain element from 1 to 13
        expected = []
        for i in range(1, 14):
            expected.append(str(i))
        # Insert channel Auto in first index
        expected.insert(0, 'Auto')
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 5.2 Check List value of Largura de banda: ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5.2 Check List value of Largura de banda: ' + str(actual))
            list_steps_fail.append('5.2 List value of Largura de banda wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Change "Canal de controle" option to "6" and apply setting
        driver.find_element_by_css_selector('#channel > option[value="6"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['channel']['used'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = ['6', 6, '20', '20']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 6. Check API value if Canal = 6: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check API value if Canal = 6: ' + str(actual))
            list_steps_fail.append('6. API value if Canal = 6 wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 7. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['wl -i wl1 channel',
                    'wl -i wl1 chanspec',
                    'nvram get wl1_channel',
                    'nvram get wl1_chanspec',
                    'uci get wireless.wl1.channel',
                    'latticecli -n "get WiFi.Radio.2.AutoChannelEnable"',
                    'latticecli -n "get WiFi.Radio.2.channel"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['current mac channel 6 target channel 6',
                    '6 (0x1006)',
                    '6',
                    '6',
                    '6',
                    'Success to get value from WiFi.Radio.2.AutoChannelEnable: 0',
                    'Success to get value from WiFi.Radio.2.channel: 6']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual))
            list_steps_fail.append('7. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 8. Using the below command from Windows command prompt to get and check wifi network information
        scan_wf = Helper.Helper_common.scan_wifi(name_2g)
        if not scan_wf:
            actual_channel = scan_wf[1]
            expected_channel = '6'
            try:
                self.assertEqual(actual_channel, expected_channel)
                self.list_steps.append(
                    '\n[Pass] 8. Check Value of channel: ' + str(actual_channel))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 8. Check Value of channel: ' + str(actual_channel))
                list_steps_fail.append('8. Value of channel wrong: Actual: ' + str(actual_channel) + ' Expected: ' + str(expected_channel))
        else:
            try:
                self.assertTrue(scan_wf)
                self.list_steps.append(
                    '\n[Pass] 8. Check 2G SSID is exist in list Wifi: ' + str(scan_wf))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 8. Check 2G SSID is exist in list Wifi: ' + str(scan_wf))
                list_steps_fail.append('8. Check 2G SSID is exist wrong in list Wifi: Actual: ' + str(scan_wf) + ' Expected: ' + 'True')

        # 9. Change below options:
        # Change Largura de banda > 40MHz
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="40"]').click()
        # Change Banda lateral para canal de controle > Alto
        driver.find_element_by_css_selector('#sideband').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#sideband > option[value="upper"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband']]
        expected = ['40', '40', 'upper']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 9.1 Check API if Sideband and Bandwidth changed: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 9.1 Check API if Sideband and Bandwidth changed: ' + str(actual))
            list_steps_fail.append('9.1 API if Sideband and Bandwidth changed wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # In the "Canal de controle" option, the available channel list should include channels: Auto; 1 -> 13
        channels = driver.find_elements_by_css_selector('#channel > option')
        actual = []
        for i in channels:
            actual.append(i.get_attribute('text'))

        expected = []
        for i in range(5, 14):
            expected.append(str(i))
        expected.insert(0, 'Auto')
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 9.2 Check Channel list ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9.2 Check Channel list ' + str(actual))
            list_steps_fail.append('9.2 Channel list wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 10. Change "Canal de controle" option to "6" and apply setting
        driver.find_element_by_css_selector('#channel > option[value="6"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['channel']['used'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = ['6', 6, '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 10. Check API value if Canal = 6: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 10. Check API value if Canal = 6: ' + str(actual))
            list_steps_fail.append('10. API value if Canal = 6 wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 11. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['wl -i wl1 channel',
                    'wl -i wl1 chanspec',
                    'nvram get wl1_channel',
                    'nvram get wl1_chanspec',
                    'uci get wireless.wl1.channel',
                    'latticecli -n "get WiFi.Radio.2.AutoChannelEnable"',
                    'latticecli -n "get WiFi.Radio.2.channel"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['current mac channel 6 target channel 6',
                    '6u (0x1904)',
                    '6',
                    '6',
                    '6',
                    'Success to get value from WiFi.Radio.2.AutoChannelEnable: 0',
                    'Success to get value from WiFi.Radio.2.channel: 6']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 11. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 11. Check Value return RG console ' + str(actual))
            list_steps_fail.append('11. Value return RG console wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 12. Using the below command from Windows command prompt to get and check wifi network information
        scan_wf = Helper.Helper_common.scan_wifi(name_2g)
        if not scan_wf:
            actual_channel = scan_wf[1]
            expected_channel = '6'
            try:
                self.assertEqual(actual_channel, expected_channel)
                self.list_steps.append(
                    '\n[Pass] 12. Check Value of channel: ' + str(actual_channel))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 12. Check Value of channel: ' + str(actual_channel))
                list_steps_fail.append('12. Value of channel wrong: Actual: ' + str(actual_channel) + ' Expected: ' + str(expected_channel))
        else:
            try:
                self.assertTrue(scan_wf)
                self.list_steps.append(
                    '\n[Pass] 12. Check 2G SSID is exist in list Wifi: ' + str(scan_wf))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 12. Check 2G SSID is exist in list Wifi: ' + str(scan_wf))
                list_steps_fail.append('12. Check 2G SSID is exist wrong in list Wifi: Actual: ' + str(scan_wf) + ' Expected: ' + 'True')

        # 13. Change below options:
        # Change Largura de banda > 40MHz
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#bandwidth > option[value="40"]').click()
        # Change Banda lateral para canal de controle > Baixo
        driver.find_element_by_css_selector('#sideband').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#sideband > option[value="lower"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband']]
        expected = ['40', '40', 'lower']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 13.1 Check API if Sideband and Bandwidth changed: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 13.1 Check API if Sideband and Bandwidth changed: ' + str(actual))
            list_steps_fail.append('13.1 API if Sideband and Bandwidth changed wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # In the "Canal de controle" option, the available channel list should include channels: Auto; 1 -> 9
        channels = driver.find_elements_by_css_selector('#channel > option')
        actual = []
        for i in channels:
            actual.append(i.get_attribute('text'))

        expected = []
        for i in range(1, 10):
            expected.append(str(i))
        expected.insert(0, 'Auto')
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 13.2 Check Channel list ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 13.2 Check Channel list ' + str(actual))
            list_steps_fail.append('13.2 Channel list wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 14. Change "Canal de controle" option to "6" and apply setting
        driver.find_element_by_css_selector('#channel > option[value="6"]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['channel']['used'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = ['6', 6, '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 14. Check API value if Canal = 6: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 14. Check API value if Canal = 6: ' + str(actual))
            list_steps_fail.append('14. API value if Canal = 6 wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 15. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['wl -i wl1 channel',
                    'wl -i wl1 chanspec',
                    'nvram get wl1_channel',
                    'nvram get wl1_chanspec',
                    'uci get wireless.wl1.channel',
                    'latticecli -n "get WiFi.Radio.2.AutoChannelEnable"',
                    'latticecli -n "get WiFi.Radio.2.channel"']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        actual[0] = ' '.join(actual[0].split('.')[1].split())
        expected = ['current mac channel 6 target channel 6',
                    '6l (0x1808)',
                    '6',
                    '6',
                    '6',
                    'Success to get value from WiFi.Radio.2.AutoChannelEnable: 0',
                    'Success to get value from WiFi.Radio.2.channel: 6']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 15. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 15. Check Value return RG console ' + str(actual))
            list_steps_fail.append('15. Value return RG console wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 16. Using the below command from Windows command prompt to get and check wifi network information
        scan_wf = Helper.Helper_common.scan_wifi(name_2g)
        if not scan_wf:
            actual_channel = scan_wf[1].strip()
            expected_channel = '6'
            try:
                self.assertEqual(actual_channel, expected_channel)
                self.list_steps.append(
                    '\n[Pass] 12. Check Value of channel: ' + str(actual_channel))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 12. Check Value of channel: ' + str(actual_channel))
                list_steps_fail.append('12. Value of channel wrong: Actual: ' + str(actual_channel) + ' Expected: ' + str(expected_channel))
        else:
            try:
                self.assertTrue(scan_wf)
                self.list_steps.append(
                    '\n[Pass] 16. Check 2G SSID is exist in list Wifi: ' + str(scan_wf))
            except AssertionError:
                self.list_steps.append(
                    '\n[Fail] 16. Check 2G SSID is exist in list Wifi: ' + str(scan_wf))
                list_steps_fail.append('16. Check 2G SSID is exist wrong in list Wifi: Actual: ' + str(scan_wf) + ' Expected: ' + 'True')

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_06] Assertion 2.4 GHz control channel fail')

    def test_WF_2G_WR_07(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong. Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # Check default value of Ativar
        ativar_check = driver.find_element_by_class_name('radio-check-controler').get_property('checked')
        try:
            self.assertTrue(ativar_check)
            self.list_steps.append('\n[Pass] 3.1 Check Ativar box is checked by default: ' + str(ativar_check))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Check Ativar box is checked by default: ' + str(ativar_check))
            list_steps_fail.append('3.1 Ativar box is not checked by default: Actual: ' + str(ativar_check) + ' Expected: ' + 'True')
            pass
        # Check default value of Modo 802.11.n
        modo_value = driver.find_element_by_id('wirelessMode').get_attribute('value')
        expected_modo = 'auto'
        try:
            self.assertEqual(modo_value, expected_modo)
            self.list_steps.append('\n[Pass] 3.2 Check value of Modo box by default: ' + str(modo_value))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Check value of Modo box by default: ' + str(modo_value))
            list_steps_fail.append('3.2 Value of Modo box by default wrong: Actual: ' + str(modo_value) + ' Expected: ' + str(expected_modo))
            pass
        # The default "Beamforming" value of 2.4 GHz wifi is "Disabled"
        beamforming_value = driver.find_element_by_id('beamforming').get_attribute('value')
        if beamforming_value == 'false':
            beamforming_value_transfer = 'Disabled'
        else:
            beamforming_value_transfer = 'Enabled'
        expected_beamforming = 'Disabled'
        try:
            self.assertEqual(beamforming_value_transfer, expected_beamforming)
            self.list_steps.append('\n[Pass] 3.3 Check value of Beamforming box by default: ' + str(beamforming_value_transfer))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.3 Check value of Beamforming box by default: ' + str(beamforming_value_transfer))
            list_steps_fail.append('3.3 Value of Beamforming box by default wrong: Actual: ' + str(beamforming_value_transfer) + ' Expected: ' + str(expected_beamforming))
            pass
        # Check API in default
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['advanced']['beamforming'],
                  api_wifi_radio['active'],
                  api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [False, True, 'auto', '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3.4 Check API radio value by default: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.4 Check API radio value by default: ' + str(actual))
            list_steps_fail.append('3.4 API radio value by default wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface, change "Modo 802.11.n" option to "Auto" and apply setting
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=auto]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        beamforming_value = driver.find_element_by_id('beamforming').get_attribute('value')
        if beamforming_value == 'false':
            beamforming_value_transfer = 'Disabled'
        else:
            beamforming_value_transfer = 'Enabled'

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [beamforming_value_transfer,
                  api_wifi_radio['basic']['wirelessMode'],
                  api_wifi_radio['advanced']['beamforming']]
        expected = ['Disabled', '802.11b+g+n', False]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 4. Check API radio value by changed Modo 802.11n: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API radio value by changed Modo 802.11n: ' + str(actual))
            list_steps_fail.append('4. API radio value by changed Modo 802.11n wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 5. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['wl -i wl1 txbf_bfr_cap',
                    'wl -i wl1 txbf_ht_enable',
                    'nvram get wl1_txbf_bfr_cap',
                    'uci get wireless.wl1.beamforming']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['0', '0', '0', '0']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 5. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Value return RG console ' + str(actual))
            list_steps_fail.append('5. Value return RG console wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Change "Beamforming" option to "Enabled" and apply setting
        driver.find_element_by_css_selector('#beamforming').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#beamforming > option[value=true]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['advanced']['beamforming'],
                  api_wifi_radio['active'],
                  api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [True, True, 'auto', '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 6. Check API radio value by default: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check API radio value by default: ' + str(actual))
            list_steps_fail.append('6. API radio value by default wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 7. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['1', '1', '1', '1']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual))
            list_steps_fail.append('7. Value return RG console wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_07] Assertion BFR transmission by beamforming fail')

    def test_WF_2G_WR_08(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
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
            list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
        # from the "page-wifi-radio" page
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 3. Check API radio value return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API radio value return: ' + str(actual))
            list_steps_fail.append('3. API radio value return wrong. Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # Check default value of Ativar
        ativar_check = driver.find_element_by_class_name('radio-check-controler').get_property('checked')
        try:
            self.assertTrue(ativar_check)
            self.list_steps.append('\n[Pass] 3.1 Check Ativar box is checked by default: ' + str(ativar_check))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.1 Check Ativar box is checked by default: ' + str(ativar_check))
            list_steps_fail.append('3.1 Ativar box is not checked by default: Actual: ' + str(actual) + ' Expected: ' + 'True')
            pass
        # Check default value of Modo 802.11.n
        modo_value = driver.find_element_by_id('wirelessMode').get_attribute('value')
        expected_modo = 'auto'
        try:
            self.assertEqual(modo_value, expected_modo)
            self.list_steps.append('\n[Pass] 3.2 Check value of Modo box by default: ' + str(modo_value))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.2 Check value of Modo box by default: ' + str(modo_value))
            list_steps_fail.append('3.2 Value of Modo box by default wrong: Actual: ' + str(modo_value) + ' Expected: ' + str(expected_modo))
            pass
        # The default "Beamforming" value of 2.4 GHz wifi is "Disabled"
        beamforming_value = driver.find_element_by_id('beamforming').get_attribute('value')
        if beamforming_value == 'false':
            beamforming_value_transfer = 'Disabled'
        else:
            beamforming_value_transfer = 'Enabled'
        expected_beamforming = 'Disabled'
        try:
            self.assertEqual(beamforming_value_transfer, expected_beamforming)
            self.list_steps.append('\n[Pass] 3.3 Check value of Beamforming box by default: ' + str(beamforming_value_transfer))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.3 Check value of Beamforming box by default: ' + str(beamforming_value_transfer))
            list_steps_fail.append('3.3 Value of Beamforming box by default wrong. Actual: ' + str(beamforming_value_transfer) + ' Expected: ' + str(expected_beamforming))
            pass
        # Check API in default
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['advanced']['beamforming'],
                  api_wifi_radio['active'],
                  api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [False, True, 'auto', '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3.4 Check API radio value by default: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3.4 Check API radio value by default: ' + str(actual))
            list_steps_fail.append('3.4 API radio value by default wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 4. Click "2.4 GHZ" to select 2.4 Ghz interface, change "Modo 802.11.n" option to "Auto" and apply setting
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#wirelessMode > option[value=auto]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        beamforming_value = driver.find_element_by_id('beamforming').get_attribute('value')
        if beamforming_value == 'false':
            beamforming_value_transfer = 'Disabled'
        else:
            beamforming_value_transfer = 'Enabled'

        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [beamforming_value_transfer,
                  api_wifi_radio['basic']['wirelessMode'],
                  api_wifi_radio['advanced']['beamforming']]
        expected = ['Disabled', '802.11b+g+n', False]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 4. Check API radio value by changed Modo 802.11n: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check API radio value by changed Modo 802.11n: ' + str(actual))
            list_steps_fail.append('4. API radio value by changed Modo 802.11n wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 5. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        list_cmd = ['wl -i wl1 txbf_bfe_cap',
                    'nvram get wl1_txbf_bfe_cap',
                    'uci get wireless.wl1.beamforming']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['0', '0', '0']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual))
            list_steps_fail.append('7. Value return RG console wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 6. Change "Beamforming" option to "Enabled" and apply setting
        driver.find_element_by_css_selector('#beamforming').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#beamforming > option[value=true]').click()
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_wifi_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_wifi_radio['advanced']['beamforming'],
                  api_wifi_radio['active'],
                  api_wifi_radio['basic']['channel']['set'],
                  api_wifi_radio['basic']['bandwidth']['used'],
                  api_wifi_radio['basic']['bandwidth']['set']]
        expected = [True, True, 'auto', '40', '40']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 6. Check API radio value by default: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check API radio value by default: ' + str(actual))
            list_steps_fail.append('6. API radio value by default wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # 7. Using the RG console to check the current configuration in wl driver by below commands:
        time.sleep(1)
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        expected = ['1', '1', '1']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual))
            list_steps_fail.append('7. Value return RG console wrong. Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_07] Assertion BFR reception by beamforming fail')

    def test_WF_2G_WR_09(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append('1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-primary-network"]').click()
        expected_url_target = ipv4 + '/#page-wifi-primary-network'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Rede Principal : ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Rede Principal: ' + driver.current_url)
            list_steps_fail.append('2. URL Page Rede Principal wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 3. Click "2.4 GHZ" to select 2.4 Ghz interface and change below options:
        driver.find_element_by_css_selector('[for="2-4-ghz"]').click()

        # UnCheck Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler[id=active]'):
            driver.find_element_by_css_selector('.radio-check[for=active]').click()
        time.sleep(0.5)
        # - Change "Nome da rede" option to "NET_2G_TEST"
        network_name_value = 'NET_2G_TEST'
        network_name = driver.find_element_by_id('network_name')
        ActionChains(driver).move_to_element(network_name).double_click().send_keys(network_name_value).perform()

        # - Change "Rede fechada" option to "Ligado"
        driver.find_element_by_css_selector('#close_network').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#close_network option[value=true]').click()

        # - Change "Modo exigido" option to "ERP"
        driver.find_element_by_css_selector('#mode_required').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#mode_required option[value=ERP]').click()

        # - Change "AP isolado" option to "Ativado"
        driver.find_element_by_css_selector('#ap_isolate').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#ap_isolate option[value=true]').click()

        # - Change "Autenticação de rede" option to "WPA2-PSK"
        driver.find_element_by_css_selector('#security_type').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#security_type option[value=WPA2-PSK]').click()

        # - Check the "MOSTRAR CHAVE" box
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler[id=show_wpa]'):
            driver.find_element_by_css_selector('.radio-check[for=show_wpa]').click()

        # - Change "WPA Chave pré-compartilhada" option to "00000000"
        wpa_key_value = '00000000'
        wpa_key = driver.find_element_by_id('wpa_key')
        ActionChains(driver).move_to_element(wpa_key).double_click().send_keys(wpa_key_value).perform()

        # - Change "Rotação da chave do grupo" option to "3000"
        group_key_value = '3000'
        group_key = driver.find_element_by_id('group-key')
        ActionChains(driver).move_to_element(group_key).double_click().send_keys(group_key_value).perform()

        # - Select the "INCAPACITAR"
        if not Helper.Helper_common.check_radio_tick(driver, '.custom-radio-controler[id=incapacitar]'):
            driver.find_element_by_css_selector('.custom-radio[for=incapacitar]').click()


        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)

        api_interface = Helper.Helper_common.api_wifi_wps_2G()
        api_ssid = Helper.Helper_common.api_wifi_ssid_2G()
        actual = [api_interface['active'],
                  api_ssid['active'],
                  api_ssid['name'],
                  api_ssid['security']['type'],
                  api_ssid['security']['personal']['encryption'],
                  api_ssid['security']['personal']['password'],
                  api_ssid['security']['personal']['groupKey'],
                  api_ssid['hiddenSSID'],
                  api_ssid['APIsolate']]
        expected = [False, False, network_name_value, 'WPA2-PSK', 'AES',
                    Helper.Helper_common.base64encode(pass_word), group_key_value, True, True]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 3 Check values of APIs: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3 Check values of APIs: ' + str(actual))
            list_steps_fail.append('3 Values of APIs wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4. Access the "page-wifi-radio" page
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 4. Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('4. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5. Click "2.4 GHZ" to select 2.4 Ghz interface and change below options:
        driver.find_element_by_css_selector('[for="radio2g"]').click()
        time.sleep(1)
        # UnCheck Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler[id=active]'):
            driver.find_element_by_css_selector('.radio-check[for=active]').click()
        time.sleep(0.5)
        # - Change "Potência de saída" option to "Médio"
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(0.5)
        # Click medium
        driver.find_element_by_css_selector('#outputPower option[value=medium]').click()

        # - Change "Modo 802.11.n" option to "Off"
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#wirelessMode > option[value=off]').click()

        # - Change "Largura de banda" option to "20MHZ"
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#bandwidth > option[value="20"]').click()

        # - Change "Canal de controle" option to "11"
        driver.find_element_by_css_selector('#channel').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#channel > option[value="11"]').click()

        # - Change "Beamforming" option to "Enabled"
        driver.find_element_by_css_selector('#beamforming').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#beamforming > option[value="true"]').click()

        # and apply settings
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)

        api_radio = Helper.Helper_common.api_wifi_radio(0)
        actual = [api_radio['advanced']['beamforming'],
                  api_radio['active'],
                  api_radio['basic']['channel']['set'],
                  api_radio['basic']['channel']['used'],
                  api_radio['basic']['bandwidth']['used'],
                  api_radio['basic']['bandwidth']['set'],
                  api_radio['basic']['wirelessMode'],
                  api_radio['basic']['outputPower']]
        expected = [True, False, '11', 11, '20', '20', '802.11g', 'medium']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 5. Check values of API: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check values of API: ' + str(actual))
            list_steps_fail.append('5. values of API wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
        time.sleep(0.5)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 6. Access the "page-wifi-connected-equip" page
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-connected-equip"]').click()
        expected_url_target = ipv4 + '/#page-wifi-connected-equip'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 6. Check URL of Page Wifi Connected Equip: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check URL of Page Wifi Connected Equip: ' + driver.current_url)
            list_steps_fail.append('6. URL Page Wifi Connected Equip wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 7. Click "2.4 GHZ" to select 2.4 Ghz interface and change below options
        driver.find_element_by_css_selector('[for="2g"]').click()
        time.sleep(1)
        # - Change "Modo restrito por MAC" box to "Permitir"
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#mac-permission > option[value="allow"]').click()

        # - Change "Filtro de MAC baseado Probe Response" option to "Ativado"
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select/option[@value="true"]').click()

        # - Sequentially add below MAC addresses to "Endereço MAC" option:
        mac_addr_list = ['40:3D:EC:97:0B:0D', '40:3D:EC:97:0B:2D', '40:3D:EC:97:0B:0C']
        for i in mac_addr_list:
            mac_input = driver.find_element_by_id('mac-input')
            ActionChains(driver).move_to_element(mac_input).click().send_keys(i).perform()
            # and apply settings
            apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            Helper.Helper_common.wait_time(self, driver)
            time.sleep(1)
        api_access_control = Helper.Helper_common.api_wifi_accessControl(0)
        actual = [api_access_control['active'],
                  api_access_control['allow'],
                  api_access_control['probeResponse'],
                  api_access_control['maxRules']]
        for i in range(len(api_access_control['rules'])):
            actual.append([api_access_control['rules'][i]['id'], api_access_control['rules'][i]['macAddress']])

        expected = [True, True, True, 20]
        for i in range(len(mac_addr_list)):
            expected.append([i, mac_addr_list[i]])

        try:
            self.assertEqual(actual, expected)
            self.list_steps.append('\n[Pass] 7. Check values of API Access Control: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 7. Check values of API Access Control: ' + str(actual))
            list_steps_fail.append('7. values of API Access Control wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
        time.sleep(0.5)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 8. Repeat from step 2 to step 7 with the 5 GHz interface
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-primary-network"]').click()
        expected_url_target = ipv4 + '/#page-wifi-primary-network'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 8.1 Check URL of Page Rede Principal : ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8.1 Check URL of Page Rede Principal: ' + driver.current_url)
            list_steps_fail.append('8.1. URL Page Rede Principal wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)

        # 3. Click "5GHZ" to select 5 Ghz interface and change below options:
        driver.find_element_by_css_selector('[for="5-ghz"]').click()
        time.sleep(1)
        # UnCheck Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler[id=active]'):
            driver.find_element_by_css_selector('.radio-check[for=active]').click()
        time.sleep(0.5)
        # - Change "Nome da rede" option to "NET_2G_TEST"
        network_name_value = 'NET_2G_TEST'
        network_name = driver.find_element_by_id('network_name')
        ActionChains(driver).move_to_element(network_name).double_click().send_keys(network_name_value).perform()
        time.sleep(0.5)
        # - Change "Rede fechada" option to "Ligado"
        driver.find_element_by_css_selector('#close_network').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#close_network option[value=true]').click()

        # - Change "Modo exigido" option to "HT"
        driver.find_element_by_css_selector('#mode_required').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#mode_required option[value=Nenhum]').click()

        # - Change "AP isolado" option to "Ativado"
        driver.find_element_by_css_selector('#ap_isolate').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#ap_isolate option[value=true]').click()

        # - Change "Autenticação de rede" option to "WPA2-PSK"
        driver.find_element_by_css_selector('#security_type').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#security_type option[value=WPA2-PSK]').click()

        # - Check the "MOSTRAR CHAVE" box
        if not Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler[id=show_wpa]'):
            driver.find_element_by_css_selector('.radio-check[for=show_wpa]').click()

        # - Change "WPA Chave pré-compartilhada" option to "00000000"
        wpa_key_value = '00000000'
        wpa_key = driver.find_element_by_id('wpa_key')
        ActionChains(driver).move_to_element(wpa_key).double_click().send_keys(wpa_key_value).perform()

        # - Change "Rotação da chave do grupo" option to "3000"
        group_key_value = '3000'
        group_key = driver.find_element_by_id('group-key')
        ActionChains(driver).move_to_element(group_key).double_click().send_keys(group_key_value).perform()

        # - Select the "INCAPACITAR"
        if not Helper.Helper_common.check_radio_tick(driver, '.custom-radio-controler[id=incapacitar]'):
            driver.find_element_by_css_selector('.custom-radio[for=incapacitar]').click()


        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)
        api_interface = Helper.Helper_common.api_wifi_wps_5G()
        api_ssid = Helper.Helper_common.api_wifi_ssid_5G()

        actual = [api_interface['active'],
                  api_ssid['active'],
                  api_ssid['name'],
                  api_ssid['security']['type'],
                  api_ssid['security']['personal']['encryption'],
                  api_ssid['security']['personal']['password'],
                  api_ssid['security']['personal']['groupKey'],
                  api_ssid['hiddenSSID'],
                  api_ssid['APIsolate']]
        expected = [False, False, network_name_value, 'WPA2-PSK', 'AES',
                    Helper.Helper_common.base64encode(pass_word), group_key_value, True, True]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 8.2 Check values of APIs: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8.2 Check values of APIs: ' + str(actual))
            list_steps_fail.append('8.2 Values of APIs wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))

        # 4. Access the "page-wifi-radio" page
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
            self.list_steps.append('\n[Pass] 8.3. Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8.3. Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('8.3. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)

        # 5. Click "5 GHZ" to select 5 Ghz interface and change below options:
        driver.find_element_by_css_selector('[for="radio5g"]').click()

        # UnCheck Ativar
        if Helper.Helper_common.check_radio_tick(driver, '.radio-check-controler[id=active]'):
            driver.find_element_by_css_selector('.radio-check[for=active]').click()

        # - Change "Potência de saída" option to "Médio"
        driver.find_element_by_css_selector('#outputPower').click()
        time.sleep(0.5)
        # Click medium
        driver.find_element_by_css_selector('#outputPower option[value=medium]').click()

        # - Change "Modo 802.11.n" option to "Off"
        driver.find_element_by_css_selector('#wirelessMode').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#wirelessMode > option[value=off]').click()

        # - Change "Largura de banda" option to "20MHZ"
        driver.find_element_by_css_selector('#bandwidth').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#bandwidth > option[value="20"]').click()

        # - Change "Canal de controle" option to "36"
        driver.find_element_by_css_selector('#channel').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#channel > option[value="36"]').click()

        # - Change "Beamforming" option to "Enabled"
        driver.find_element_by_css_selector('#beamforming').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#beamforming > option[value="true"]').click()

        # and apply settings
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        Helper.Helper_common.wait_time(self, driver)

        api_radio = Helper.Helper_common.api_wifi_radio(1)
        actual = [api_radio['advanced']['beamforming'],
                  api_radio['active'],
                  api_radio['basic']['channel']['set'],
                  api_radio['basic']['channel']['used'],
                  api_radio['basic']['bandwidth']['used'],
                  api_radio['basic']['bandwidth']['set'],
                  api_radio['basic']['wirelessMode'],
                  api_radio['basic']['outputPower']]
        expected = [True, False, '36', 36, '20', '20', '802.11a', 'medium']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 8.4. Check values of API: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8.4. Check values of API: ' + str(actual))
            list_steps_fail.append('8.4. values of API wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
        time.sleep(0.5)

        # 6. Access the "page-wifi-connected-equip" page
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-connected-equip"]').click()
        expected_url_target = ipv4 + '/#page-wifi-connected-equip'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 8.5. Check URL of Page Wifi Connected Equip: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8.5. Check URL of Page Wifi Connected Equip: ' + driver.current_url)
            list_steps_fail.append('8.5. URL Page Wifi Connected Equip wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # 7. Click "5 GHZ" to select 5 Ghz interface and change below options
        driver.find_element_by_css_selector('[for="5g"]').click()
        time.sleep(1)
        # - Change "Modo restrito por MAC" box to "Permitir"
        driver.find_element_by_css_selector('#mac-permission').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#mac-permission > option[value="allow"]').click()
        time.sleep(1)
        # - Change "Filtro de MAC baseado Probe Response" option to "Ativado"
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="f-row"][2]//select/option[@value="true"]').click()
        time.sleep(1)
        # - Sequentially add below MAC addresses to "Endereço MAC" option:
        mac_addr_list = ['40:3D:EC:97:0B:0D', '40:3D:EC:97:0B:2D', '40:3D:EC:97:0B:0C']
        for i in mac_addr_list:
            mac_input = driver.find_element_by_id('mac-input')
            ActionChains(driver).move_to_element(mac_input).click().send_keys(i).perform()
            # and apply settings
            apply_btn = driver.find_element_by_css_selector('button[value="apply"]')
            ActionChains(driver).move_to_element(apply_btn).click().perform()
            Helper.Helper_common.wait_time(self, driver)
            time.sleep(1)
        api_access_control = Helper.Helper_common.api_wifi_accessControl(1)
        actual = [api_access_control['active'],
                  api_access_control['allow'],
                  api_access_control['probeResponse'],
                  api_access_control['maxRules']]
        for i in range(len(api_access_control['rules'])):
            actual.append([api_access_control['rules'][i]['id'], api_access_control['rules'][i]['macAddress']])

        expected = [True, True, True, 20]
        for i in range(len(mac_addr_list)):
            expected.append([i, mac_addr_list[i]])

        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append('\n[Pass] 8.6. Check values of API Access Control: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 8.6. Check values of API Access Control: ' + str(actual))
            list_steps_fail.append('8.6. values of API Access Control wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
        time.sleep(1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 9. Access the "page-wifi-radio" page
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
            self.list_steps.append('\n[Pass] 4. Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append('4. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 10. Click "2.4 GHZ" to select 2.4 Ghz interface and restore the default wireless configurations by clicking
        # the "Restaurar padrões sem fio" button from the "page-wifi-radio" page
        time.sleep(1)
        driver.find_element_by_css_selector('[for=radio2g]').click()
        time.sleep(1)
        restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
        ActionChains(driver).move_to_element(restore_btn).click().perform()
        # Click OK
        driver.find_element_by_css_selector('#ok').click()
        Helper.Helper_common.wait_time(self, driver)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 11. Access the "page-wifi-primary-network" page and click "2.4 GHZ" to select 2.4 Ghz interface and
        # check the default values of 2.4 Ghz, current values of 5 GHz
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(1)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(1)
        # Click Rede Principal
        driver.find_element_by_css_selector('a[href="#page-wifi-primary-network"]').click()
        expected_url_target = ipv4 + '/#page-wifi-primary-network'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 11. Check URL of Page Wifi Primary Network: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 11. Check URL of Page Wifi Primary Network: ' + driver.current_url)
            list_steps_fail.append('11. URL Page Wifi Primary Network wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(1)
        driver.find_element_by_css_selector('[for="2-4-ghz"]').click()
        time.sleep(1)
        # Verify 2.4G in default
        ativar = driver.find_element_by_css_selector('.radio-check-controler[id=active]').get_property('checked')
        actual_nw_name = driver.find_element_by_css_selector('#network_name').get_attribute('value')
        close_nw = driver.find_element_by_css_selector('#close_network').get_attribute('value')
        mode_require = driver.find_element_by_css_selector('#mode_required').get_attribute('value')
        ap_isolate = driver.find_element_by_css_selector('#ap_isolate').get_attribute('value')
        security_type = driver.find_element_by_css_selector('#security_type').get_attribute('value')
        encryption = driver.find_element_by_css_selector('#encryption').get_attribute('value')
        show_wpa = driver.find_element_by_css_selector('.radio-check-controler[id=show_wpa]').get_property('checked')
        if not show_wpa:
            driver.find_element_by_css_selector('.radio-check[for=show_wpa]').click()
        actual_wpa_key = driver.find_element_by_css_selector('#wpa_key').get_attribute('value')
        group_key = driver.find_element_by_css_selector('#group-key').get_attribute('value')
        habilitar = driver.find_element_by_css_selector('#habilitar').get_property('checked')

        actual = [ativar, actual_nw_name, close_nw, mode_require, ap_isolate,
                  security_type, encryption, show_wpa, actual_wpa_key, group_key, habilitar]
        list_cmd = ['/Con/show ip']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + cm_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        more_info = []
        for i in range(len(list_cmd)):
            more_info.append(config.get('COMMAND', options[i]))
        more_info_convert = more_info[0].split('CM')[1].split('not configured')[0].strip().replace(':','').upper()
        network_name = 'NET_2G' + more_info_convert[-6:]
        wpa_key = more_info_convert[-8:]

        expected = [True, network_name, 'false', 'Nenhum', 'false',
                    'WPA2/WPA-PSK', 'AES/TKIP', False, wpa_key, '3600', True]
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append('\n[Pass] 11.1 Check value default of 2.4 G: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 11.1 Check value default of 2.4 G: ' + str(actual))
            list_steps_fail.append('11.1 Value default of 2.4 G wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))

        # Check 5G interface
        driver.find_element_by_css_selector('[for="5-ghz"]').click()
        actual_ativar = driver.find_element_by_css_selector('.radio-check-controler[id=active]').get_property('checked')
        actual_nw_name = driver.find_element_by_css_selector('#network_name').get_attribute('value')
        actual_close_nw = driver.find_element_by_css_selector('#close_network').get_attribute('value')
        actual_mode_require = driver.find_element_by_css_selector('#mode_required').get_attribute('value')
        actual_ap_isolate = driver.find_element_by_css_selector('#ap_isolate').get_attribute('value')
        actual_security_type = driver.find_element_by_css_selector('#security_type').get_attribute('value')

        actual_show_wpa = driver.find_element_by_css_selector('.radio-check-controler[id=show_wpa]').get_property('checked')
        if not show_wpa:
            driver.find_element_by_css_selector('.radio-check[for=show_wpa]').click()
        actual_wpa_key = driver.find_element_by_css_selector('#wpa_key').get_attribute('value')
        actual_group_key = driver.find_element_by_css_selector('#group-key').get_attribute('value')
        actual_inhabilitar = driver.find_element_by_css_selector('#incapacitar').get_property('checked')

        actual_5g = [actual_ativar, actual_nw_name, actual_close_nw, actual_mode_require,
                     actual_ap_isolate, actual_security_type, actual_show_wpa,
                     actual_wpa_key, actual_group_key, actual_inhabilitar]
        expected_5g = [False, network_name_value, 'true', 'Nenhum', 'true',
                       'WPA2-PSK', True, wpa_key_value, group_key_value, True]
        try:
            self.assertListEqual(expected_5g, actual_5g)
            self.list_steps.append('\n[Pass] 11.2 Check value default of 5 G: ' + str(actual_5g))
        except AssertionError:
            self.list_steps.append('\n[Fail] 11.2 Check value default of 5 G: ' + str(actual_5g))
            list_steps_fail.append('11.2 Value default of 5 G wrong: Actual: ' + str(actual_5g) + ' Expected: ' + str(expected_5g))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 12. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 bss',
                    'wl1 ssid',
                    'wl1 closed',
                    'wl1 mode_reqd',
                    'dhd -i wl1 ap_isolate',
                    'wl -i wl1 wpa_auth',
                    'wl -i wl1 wsec',
                    'nvram get wl1_wps_mode',
                    'nvram get wl1_wpa_psk']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))
        new_network_name = 'Current SSID: "'+network_name+'"'
        expected = ['up', new_network_name, '0', '0', '0', '0x84 WPA-PSK WPA2-PSK', '70', 'enabled', wpa_key]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 12. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 12. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '12. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 13. Access the "page-wifi-radio" page and click "2.4 GHZ" to select 2.4 Ghz interface and check the default values of 2.4 Ghz, current values of 5 GHz
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
            self.list_steps.append('\n[Pass] 13. Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 13. Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append(
                '13. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # Click 2.4G interface
        driver.find_element_by_css_selector('[for=radio2g]').click()
        actual_ativar = driver.find_element_by_css_selector('.radio-check-controler[id=active]').get_property('checked')
        actual_outputPower = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        actual_wirelessMode = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        actual_bandwidth = driver.find_element_by_css_selector('#bandwidth').get_attribute('value')
        actual_sideband = driver.find_element_by_css_selector('#sideband').get_attribute('value')
        actual_channel = driver.find_element_by_css_selector('#channel').get_attribute('value')
        actual_beamforming = driver.find_element_by_css_selector('#beamforming').get_attribute('value')

        actual = [actual_ativar, actual_outputPower, actual_wirelessMode, actual_bandwidth, actual_sideband,
                  actual_channel, actual_beamforming]
        expected = [True, 'high', 'auto', '40', 'lower', 'auto', 'false']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 13.1 Check Default Value 2G interface ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 13.1 Check Default Value 2G interface ' + str(actual))
            list_steps_fail.append(
                '13.1 Default Value 2G interface wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # Click 5G interface
        driver.find_element_by_css_selector('[for=radio5g]').click()
        actual_ativar = driver.find_element_by_css_selector('.radio-check-controler[id=active]').get_property('checked')
        actual_outputPower = driver.find_element_by_css_selector('#outputPower').get_attribute('value')
        actual_wirelessMode = driver.find_element_by_css_selector('#wirelessMode').get_attribute('value')
        actual_bandwidth = driver.find_element_by_css_selector('#bandwidth').get_attribute('value')

        actual_channel = driver.find_element_by_css_selector('#channel').get_attribute('value')
        actual_beamforming = driver.find_element_by_css_selector('#beamforming').get_attribute('value')
        actual = [actual_ativar, actual_outputPower, actual_wirelessMode, actual_bandwidth,
                  actual_channel, actual_beamforming]
        expected = [False, 'medium', 'off', '20', '36', 'true']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 13.2 Check Value 5G interface ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 13.2 Check Value 5G interface ' + str(actual))
            list_steps_fail.append(
                '13.2 Value 5G interface wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 14. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 radio',
                    'wl1 country',
                    'wl1 pwr_percent',
                    'nvram get wl1_nmode',
                    'wl1 bw_cap 2g',
                    'nvram get wl1_channel',
                    'wl1 txbf_bfr_cap']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['0x0000', 'BR (BR/24) BRAZIL', '100', '-1', '0x3', '0', '0']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 14. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 14. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '14. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 15. Access the "page-wifi-connected-equip" page and click "2.4 GHZ" to select 2.4 Ghz interface and check the default values of 2.4 Ghz, current values of 5 GHz
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
            self.list_steps.append('\n[Pass] 15. Check URL of Page Wifi Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 15. Check URL of Page Wifi Radio: ' + driver.current_url)
            list_steps_fail.append(
                '15. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # Click 2.4G interface
        driver.find_element_by_css_selector('[for="2g"]').click()
        mac_permission = driver.find_element_by_id('mac-permission').get_attribute('value')

        actual = [mac_permission]
        expected = ['disabled']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 15.1 Check Default Value 2G interface ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 15.1 Check Default Value 2G interface ' + str(actual))
            list_steps_fail.append(
                '15.1 Default Value 2G interface wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass
        # Click 5G interface
        driver.find_element_by_css_selector('[for="5g"]').click()
        mac_permission = driver.find_element_by_id('mac-permission').get_attribute('value')
        mac_filter =  driver.find_element_by_xpath('//div[@class="f-row"][2]//select').get_attribute('value')
        total_result = driver.find_elements_by_xpath('//table[@class="table-fil"]/tbody/tr')
        mac_addr = []
        for i in range(1, len(total_result)+1):
            mac_addr.append(driver.find_element_by_xpath('//table[@class="table-fil"]/tbody/tr['+str(i)+']/td[1]').text)

        actual = [mac_permission, mac_filter, mac_addr]
        expected = ['allow', 'true', mac_addr_list]
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 15.2 Check Value 5G interface ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 15.2 Check Value 5G interface ' + str(actual))
            list_steps_fail.append(
                '15.2 Value 5G interface wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 16. Using the RG console to check the current configuration in wl driver by below commands:
        list_cmd = ['wl1 mac']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 16. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 16. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '16. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 17. From test PC, check SSID of 2.4 Ghz interface whether is in available wifi list or not
        check_ssid = Helper.Helper_common.show_network(name_2g)
        try:
            self.assertTrue(check_ssid)
            self.list_steps.append('\n[Pass] 17. Check 2G SSID is not in wifi list ')
        except AssertionError:
            self.list_steps.append('\n[Fail] 17. Check 2G SSID is not in wifi list ')
            list_steps_fail.append('17. 2G SSID is in wifi list: Actual: ' + str(check_ssid) + ' Expected: ' + 'True')
            pass

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_09] Assertion 2.4 GHz Restore wireless default fail')

    def test_WF_2G_WR_10(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append(
                '1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append(
                '2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Radio: ' + driver.current_url)
            list_steps_fail.append(
                '2. URL Page Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 3. Click "2.4 GHZ" to select 2.4 Ghz interface and click the "Varredura de pontos de acesso Wi-Fi" button
        driver.find_element_by_css_selector('[for=radio2g]').click()
        driver.find_element_by_css_selector('button[value="Varredura de pontos de acesso Wi-Fi"]').click()
        Helper.Helper_common.wait_time(self, driver)
        window_scan_ap_result = self.driver.window_handles[1]
        driver.switch_to.window(window_scan_ap_result)
        time.sleep(5)

        dict_key_translate = {
            'ssid': 'Nome da rede',
            'security': 'Modo de segurança',
            'mode': 'Modo',
            'phyMode': 'Modo PHY',
            'rssi': 'RSSI',
            'channel': 'Canal',
            'bandwidth': 'Largura de banda',
            'macAddress': 'BSSID'
        }
        block_lists = driver.find_elements_by_css_selector('.list li')
        count_existed = 0
        for i in range(1, len(block_lists)+1):
            web_text = driver.find_element_by_css_selector('.list li:nth-child('+str(i)+')').text
            f = open('../Config/01.txt', 'w')
            f.write('[DATA]\n')
            f.write(web_text)
            f.close()
            conf = configparser.ConfigParser()
            conf.read_file(open('../Config/01.txt'))
            actual = [conf.get('DATA', dict_key_translate['macAddress']),
                      conf.get('DATA', dict_key_translate['ssid']),
                      conf.get('DATA', dict_key_translate['phyMode']),
                      conf.get('DATA', dict_key_translate['security'])]
            api_scanResult = Helper.Helper_common.api_wifi_scanResult(0)

            for result in api_scanResult:
                if conf.get('DATA', dict_key_translate['macAddress']) == result['macAddress']:
                    expected = [result['macAddress'], result['ssid'], result['phyMode'], result['security']]
                    try:
                        self.assertListEqual(actual, expected)
                        self.list_steps.append(
                            '\n[Pass] 3. Check Values between API and WebUI' + str(actual))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 3. Checks Value between API and WebUI' + str(actual))
                        list_steps_fail.append(
                            '3. Values between API and WebUI wrong: Actual: ' + str((actual))
                            + ' Expected: ' + str(expected))
                        pass

                    count_existed += 1
                    break
                else:
                    continue
        # Not match = Total (len(block_lists))   -  Match case    <   20% Total
        try:
            self.assertLessEqual(len(block_lists) - count_existed, len(block_lists)*0.2)
            self.list_steps.append(
                '\n[Pass] 3+. Check number of not match wifi > = 20% of Total:' + str(len(block_lists) - count_existed))
        except AssertionError:
            self.list_steps.append(
                '\n[Pass] 3+. Check number of not match wifi > = 20% of Total:' + str(len(block_lists) - count_existed))
            list_steps_fail.append(
                '3+. Number of not match wifi < = 20% of Total: Actual: ' + str((len(block_lists) - count_existed))
                + ' Expected: ' + str(len(block_lists)*0.2))


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ['iwinfo wl1 scan > /tmp/web_ui/out/www/01.txt',
                    'wl -i wl1 escanresults > /tmp/web_ui/out/www/02.txt']
        Helper.Helper_common.write_command(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')

        driver2 = webdriver.Chrome('../Driver/chromedriver.exe')
        driver2.get('http://192.168.0.1/01.txt')
        a = driver2.find_element_by_css_selector('body>pre').text + '\n\n'
        cell_blocks = re.findall(r"(?s)Address: .*?\n\n", a)
        count_existed = 0
        for cell in cell_blocks:
            b = ''
            for j in cell.splitlines():
                b += j.strip() + '\n'

            f = open('../Config/01.txt', 'w')
            f.write('[DATA]\n')
            f.write(b)
            f.close()
            conf = configparser.ConfigParser()
            conf.read_file(open('../Config/01.txt'))
            actual_crt = [conf.get('DATA', 'Address'),
                          conf.get('DATA', 'ESSID'),
                          conf.get('DATA', 'HWMode'),
                          conf.get('DATA', 'Encryption')]
            api_scanResult = Helper.Helper_common.api_wifi_scanResult(0)

            for result in api_scanResult:
                if conf.get('DATA', 'Address') == result['macAddress']:
                    expected_crt = [result['macAddress'],
                                    result['ssid'],
                                    result['phyMode'].replace('+', ''),
                                    result['security']]
                    try:
                        self.assertListEqual(actual_crt, expected_crt)
                        self.list_steps.append(
                            '\n[Pass] 4.1 Check Values between API and CRT' + str(actual_crt))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 4.1 Checks Value between API and CRT' + str(actual_crt))
                        list_steps_fail.append(
                            '4.1 Values between API and CRT wrong: Actual: ' + str((actual_crt))
                            + ' Expected: ' + str(expected_crt))
                        pass
                    count_existed += 1
                    break
                else:
                    continue

        # Second command check
        driver2.get('http://192.168.0.1/02.txt')
        a = driver2.find_element_by_css_selector('body>pre').text + '\n\n'
        cell_blocks = re.findall(r"(?s)Address: .*?\n\n", a)
        for cell in cell_blocks:
            f = open('../Config/02.txt', 'w')
            f.write('[DATA]\n')
            f.write(cell)
            f.close()
            conf = configparser.ConfigParser()
            conf.read_file(open('../Config/02.txt'))
            actual_crt = [conf.get('DATA', 'BSSID').split('Capability')[0].strip(),
                          conf.get('DATA', 'SSID')]
            api_scanResult = Helper.Helper_common.api_wifi_scanResult(0)

            for result in api_scanResult:
                if actual_crt[0] == result['macAddress']:
                    expected_crt = [result['macAddress'],
                                    result['ssid']]
                    try:
                        self.assertListEqual(actual_crt, expected_crt)
                        self.list_steps.append(
                            '\n[Pass] 4.2 Check Values between API and CRT' + str(actual_crt))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 4.2 Checks Value between API and CRT' + str(actual_crt))
                        list_steps_fail.append(
                            '4.2 Values between API and CRT wrong: Actual: ' + str((actual_crt))
                            + ' Expected: ' + str(expected_crt))
                        pass
                    count_existed += 1
                    break
                else:
                    continue

        # Not match = Total (len(block_lists))   -  Match case    <   20% Total
        try:
            self.assertLessEqual(len(cell_blocks) - count_existed, len(cell_blocks) * 0.2)
            self.list_steps.append(
                '\n[Pass] 4.3 Check number of not match wifi > = 20% of Total:' + str(
                    len(cell_blocks) - count_existed))
        except AssertionError:
            self.list_steps.append(
                '\n[Pass] 4.3 Check number of not match wifi > = 20% of Total:' + str(
                    len(cell_blocks) - count_existed))
            list_steps_fail.append(
                '4.3 Number of not match wifi < = 20% of Total: Actual: ' + str(
                    (len(cell_blocks) - count_existed))
                + ' Expected: ' + str(len(cell_blocks) * 0.2))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5. Click the "Atualizar" button to re-scan
        driver.switch_to.window(window_scan_ap_result)
        driver.find_element_by_css_selector('button[value=refresh]').click()
        time.sleep(7)
        block_lists = driver.find_elements_by_css_selector('.list li')
        count_existed = 0
        for i in range(1, len(block_lists) + 1):
            web_text = driver.find_element_by_css_selector('.list li:nth-child(' + str(i) + ')').text
            f = open('../Config/01.txt', 'w')
            f.write('[DATA]\n')
            f.write(web_text)
            f.close()
            conf = configparser.ConfigParser()
            conf.read_file(open('../Config/01.txt'))
            actual = [conf.get('DATA', dict_key_translate['macAddress']),
                      conf.get('DATA', dict_key_translate['ssid']),
                      conf.get('DATA', dict_key_translate['phyMode']),
                      conf.get('DATA', dict_key_translate['security'])]
            api_scanResult = Helper.Helper_common.api_wifi_scanResult(0)

            for result in api_scanResult:
                if conf.get('DATA', dict_key_translate['macAddress']) == result['macAddress']:
                    expected = [result['macAddress'], result['ssid'], result['phyMode'], result['security']]
                    try:
                        self.assertListEqual(actual, expected)
                        self.list_steps.append(
                            '\n[Pass] 5.1 Check Values between API and WebUI' + str(actual))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 5.1 Checks Value between API and WebUI' + str(actual))
                        list_steps_fail.append(
                            '5.1 Values between API and WebUI wrong: Actual: ' + str((actual))
                            + ' Expected: ' + str(expected))
                        pass

                    count_existed += 1
                    break
                else:
                    continue

        # Not match = Total (len(block_lists))   -  Match case    <   20% Total
        try:
            self.assertLessEqual(len(block_lists) - count_existed, len(block_lists) * 0.2)
            self.list_steps.append(
                '\n[Pass] 5.2 Check number of not match wifi > = 20% of Total:' + str(len(block_lists) - count_existed))
        except AssertionError:
            self.list_steps.append(
                '\n[Pass] 5.2 Check number of not match wifi > = 20% of Total:' + str(len(block_lists) - count_existed))
            list_steps_fail.append(
                '5.2 Number of not match wifi < = 20% of Total: Actual: ' + str((len(block_lists) - count_existed))
                + ' Expected: ' + str(len(block_lists) * 0.2))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 6. Using the RG console to check the current configuration in wl driver by one of below commands:
        Helper.Helper_common.write_command(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        driver2.get('http://192.168.0.1/01.txt')
        a = driver2.find_element_by_css_selector('body>pre').text + '\n\n'
        cell_blocks = re.findall(r"(?s)Address: .*?\n\n", a)
        count_existed = 0
        for cell in cell_blocks:
            b = ''
            for j in cell.splitlines():
                b += j.strip() + '\n'

            f = open('../Config/01.txt', 'w')
            f.write('[DATA]\n')
            f.write(b)
            f.close()
            conf = configparser.ConfigParser()
            conf.read_file(open('../Config/01.txt'))
            actual_crt = [conf.get('DATA', 'Address'),
                          conf.get('DATA', 'ESSID'),
                          conf.get('DATA', 'HWMode'),
                          conf.get('DATA', 'Encryption')]
            api_scanResult = Helper.Helper_common.api_wifi_scanResult(0)

            for result in api_scanResult:
                if conf.get('DATA', 'Address') == result['macAddress']:
                    expected_crt = [result['macAddress'],
                                    result['ssid'],
                                    result['phyMode'].replace('+', ''),
                                    result['security']]
                    try:
                        self.assertListEqual(actual_crt, expected_crt)
                        self.list_steps.append(
                            '\n[Pass] 6.1 Check Values between API and CRT' + str(actual_crt))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 6.1 Checks Value between API and CRT' + str(actual_crt))
                        list_steps_fail.append(
                            '6.1 Values between API and CRT wrong: Actual: ' + str((actual_crt))
                            + ' Expected: ' + str(expected_crt))
                        pass
                    count_existed += 1
                    break
                else:
                    continue

        # Second command check
        driver2.get('http://192.168.0.1/02.txt')
        a = driver2.find_element_by_css_selector('body>pre').text + '\n\n'
        cell_blocks = re.findall(r"(?s)Address: .*?\n\n", a)
        for cell in cell_blocks:
            f = open('../Config/02.txt', 'w')
            f.write('[DATA]\n')
            f.write(cell)
            f.close()
            conf = configparser.ConfigParser()
            conf.read_file(open('../Config/02.txt'))
            actual_crt = [conf.get('DATA', 'BSSID').split('Capability')[0].strip(),
                          conf.get('DATA', 'SSID')]
            api_scanResult = Helper.Helper_common.api_wifi_scanResult(0)

            for result in api_scanResult:
                if actual_crt[0] == result['macAddress']:
                    expected_crt = [result['macAddress'],
                                    result['ssid']]
                    try:
                        self.assertListEqual(actual_crt, expected_crt)
                        self.list_steps.append(
                            '\n[Pass] 6.2 Check Values between API and CRT' + str(actual_crt))
                    except AssertionError:
                        self.list_steps.append(
                            '\n[Fail] 6.2 Checks Value between API and CRT' + str(actual_crt))
                        list_steps_fail.append(
                            '6.2 Values between API and CRT wrong: Actual: ' + str((actual_crt))
                            + ' Expected: ' + str(expected_crt))
                        pass
                    count_existed += 1
                    break
                else:
                    continue
        # Not match = Total (len(block_lists))   -  Match case    <   20% Total
        try:
            self.assertLessEqual(len(cell_blocks) - count_existed, len(cell_blocks) * 0.2)
            self.list_steps.append(
                '\n[Pass] 6.3 Check number of not match wifi > = 20% of Total:' + str(
                    len(cell_blocks) - count_existed))
        except AssertionError:
            self.list_steps.append(
                '\n[Pass] 6.3 Check number of not match wifi > = 20% of Total:' + str(
                    len(cell_blocks) - count_existed))
            list_steps_fail.append(
                '6.3 Number of not match wifi < = 20% of Total: Actual: ' + str(
                    (len(cell_blocks) - count_existed))
                + ' Expected: ' + str(len(cell_blocks) * 0.2))
        driver2.quit()

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_10] Assertion 2.4 GHz Site Survey fail')

    def test_WF_2G_WR_11(self):
        driver = self.driver
        self.def_name = Helper.Helper_common.get_func_name()
        list_steps_fail = []
        expected_quick_setup = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected_quick_setup)
            self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 1. Login Quick setup: ' + driver.current_url)
            list_steps_fail.append(
                '1. URL QS wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
        name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
        # Configuration Advance
        driver.find_element_by_css_selector('.next.config').click()
        expected_url_target = ipv4 + '/#page-status-software'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
            list_steps_fail.append(
                '2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)
        # Click Menu
        driver.find_element_by_css_selector('span.icon').click()
        time.sleep(0.5)
        # Click Wifi
        driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
        time.sleep(0.5)
        # Click Radio
        driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
        expected_url_target = ipv4 + '/#page-wifi-radio'
        try:
            self.assertEqual(driver.current_url, expected_url_target)
            self.list_steps.append('\n[Pass] 2.2 Check URL of Page Radio: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 2.2 Check URL of Page Radio: ' + driver.current_url)
            list_steps_fail.append(
                '2. URL Page Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
        time.sleep(0.5)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 3. Click "2.4 GHZ" to select 2.4 Ghz interface and check the country code displayed in "País"section
        driver.find_element_by_css_selector('[for=radio2g]').click()
        country_style = driver.find_element_by_id('country').get_attribute('readonly')
        country_code = driver.find_element_by_id('country').get_attribute('value')
        actual = [country_style, country_code]
        api_radio = Helper.Helper_common.api_wifi_radio(0)
        expected = ['true', api_radio['advanced']['countryCode']]
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 3. Check values between webUI and API: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check values between webUI and API: ' + str(actual))
            list_steps_fail.append(
                '3. Values between webUI and API wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 4. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ['grep -i -e "ccode" -e "regrev" /data/provisioned_wifi_wl1_vars.txt',
                    'wl1 country']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_mul_line.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['ccode=BR regrev=24', 'BR (BR/24) BRAZIL']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 4. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 4. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '4. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 5. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ['wl1 country US/0']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 5. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 5. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '5. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 6. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ['wl1 country']
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['US (US/0) UNITED STATES']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 6. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 6. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '6. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 7. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ["sed -i '/ccode=/c\ccode=US/0' /data/provisioned_wifi_wl1_vars.txt",
                    "sed -i '/regrev=/c\\regrev=US/0' /data/provisioned_wifi_wl1_vars.txt"]
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['', '']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 7. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 7. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '7. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 8. Using the RG console to check the current configuration in wl driver by one of below commands:

        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./reboot.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        time.sleep(120)
        Helper.Helper_common.login(driver, self, ipv4)
        expected = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected)
            self.list_steps.append('\n[Pass] 8. Check reboot successfully: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 8. Check reboot successfully: ' + driver.current_url)
            list_steps_fail.append(
                '8. Reboot successfully: Actual: ' + driver.current_url + ' Expected: ' + expected)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 9. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ["wl1 country",
                    "rm -rf /data/provisioned_wifi_wl1_vars.txt"]
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['US (US/0) UNITED STATES',
                    'The "provisioned_wifi_wl1_vars.txt" file was deleted from the "/data" directory (ls: /data/provisioned_wifi_wl1_vars.txt: No such file or directory)']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 9. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 9. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '9. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 10. Using the RG console to check the current configuration in wl driver by one of below commands:
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./reboot.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        time.sleep(120)
        Helper.Helper_common.login(driver, self, ipv4)
        expected = ipv4 + '/#page-quick-setup'
        try:
            self.assertEqual(driver.current_url, expected)
            self.list_steps.append('\n[Pass] 10. Check reboot successfully: ' + driver.current_url)
        except AssertionError:
            self.list_steps.append('\n[Fail] 10. Check reboot successfully: ' + driver.current_url)
            list_steps_fail.append(
                '10. Reboot successfully: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 11. Using the RG console to check the current configuration in wl driver by one of below commands:
        list_cmd = ["wl1 country"]
        Helper.Helper_common.write_command(list_cmd)
        options = Helper.Helper_common.option_key(list_cmd)
        os.system(
            '''"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./wl_test.py /SERIAL '''
            + rg_port + ''' /BAUD 115200''')
        config = configparser.ConfigParser()
        config.read_file(open(r'../Config/cmd_value.txt'))
        actual = []
        for i in range(len(list_cmd)):
            actual.append(config.get('COMMAND', options[i]))

        expected = ['BR (BR/24) BRAZIL']
        try:
            self.assertListEqual(actual, expected)
            self.list_steps.append(
                '\n[Pass] 11. Check Value return RG console ' + str(actual))
        except AssertionError:
            self.list_steps.append(
                '\n[Fail] 11. Check Value return RG console ' + str(actual))
            list_steps_fail.append(
                '11. Value return RG console wrong: Actual: ' + str(actual) + ' Expected: ' + str(expected))
            pass

        self.assertListEqual(list_steps_fail, [], '[WF_2G_WR_11] Assertion 2.4 GHz Country code fail')

    # def test_WF_2G_WPN_01(self):
    #     driver = self.driver
    #     self.def_name = Helper.Helper_common.get_func_name()
    #     list_steps_fail = []
    #     expected_quick_setup = ipv4 + '/#page-quick-setup'
    #     try:
    #         self.assertEqual(driver.current_url, expected_quick_setup)
    #         self.list_steps.append('\n[Pass] 1. Login Quick setup: ' + driver.current_url)
    #     except AssertionError:
    #         self.list_steps.append('\n[Fail] 1. Login Quick setup: Actual: ' + driver.current_url + ' Expected: ' + expected_quick_setup)
    #         list_steps_fail.append('1. URL QS wrong: ' + driver.current_url)
    #     name_2g = driver.find_element_by_css_selector('[id="2g-network-name"]').text.strip()
    #     # Configuration Advance
    #     driver.find_element_by_css_selector('.next.config').click()
    #     expected_url_target = ipv4 + '/#page-status-software'
    #     try:
    #         self.assertEqual(driver.current_url, expected_url_target)
    #         self.list_steps.append('\n[Pass] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
    #     except AssertionError:
    #         self.list_steps.append('\n[Fail] 2.1 Check URL of Configuration Advance: ' + driver.current_url)
    #         list_steps_fail.append('2. URL Configuration Advance wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
    #     time.sleep(1)
    #     # Click Menu
    #     driver.find_element_by_css_selector('span.icon').click()
    #     time.sleep(1)
    #     # Click Wifi
    #     driver.find_element_by_css_selector('[for=menu-wi-fi]').click()
    #     time.sleep(1)
    #     # Click Radio
    #     driver.find_element_by_css_selector('a[href="#page-wifi-radio"]').click()
    #     expected_url_target = ipv4 + '/#page-wifi-radio'
    #     try:
    #         self.assertEqual(driver.current_url, expected_url_target)
    #         self.list_steps.append('\n[Pass] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
    #     except AssertionError:
    #         self.list_steps.append('\n[Fail] 2.2 Check URL of Page Wifi Radio: ' + driver.current_url)
    #         list_steps_fail.append('2. URL Page Wifi Radio wrong: Actual: ' + driver.current_url + ' Expected: ' + expected_url_target)
    #     time.sleep(1)
    #
    #     # 3. Restore the default wireless configurations by clicking the "Restaurar padrões sem fio" button
    #     # from the "page-wifi-radio" page
    #     restore_btn = driver.find_element_by_css_selector('button[value="Restaurar padrões sem fio"]')
    #     ActionChains(driver).move_to_element(restore_btn).click().perform()
    #     # Click OK
    #     driver.find_element_by_css_selector('#ok').click()
    #     Helper.Helper_common.wait_time(self, driver)

if __name__ == '__main__':
    HTMLTestRunner.main()
