import sys, os

sys.path.append('../')
import unittest
import configparser
import time
import datetime
import socket
import subprocess
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import helper.runner
import helper.common
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
config_file = str(os.path.join(script_dir, "..", "..", "config", "config.ini"))
if not os.path.exists(config_file):
    print("The config_file: " + config_file + "not exist. Exit!!!")
    sys.exit()

config = configparser.RawConfigParser()
config.read(config_file)

ipv4 = 'http://' + config.get('IP', 'ipv4')
ipv6 = 'http://[' + config.get('IP', 'ipv6') + ']'
ipv6_ping = config.get('IP', 'ipv6')
ipv4_ping = config.get('IP', 'ipv4')
ipv6_global = 'http://[' + config.get('IP', 'ipv6_global') + ']'
user = config.get('AUTHENTICATION', 'gw_user')
pass_word = config.get('AUTHENTICATION', 'gw_pw')
url = config.get('COMMON', 'url')
rg_port = config.get('SERIAL', 'rg_port')

class WifiRadio(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime.datetime.now()
        self.driver = webdriver.Chrome(str(os.path.join(script_dir, "..", "helper", "driver", "chromedriver.exe")))
        driver = self.driver
        driver.maximize_window()
        helper.common.login(driver, ipv4)
        self.list_steps = []

    def tearDown(self):
        end_time = datetime.datetime.now()
        duration = str((end_time - self.start_time))
        helper.common.write_actual_excel(self.list_steps, self.def_name, duration)
        self.driver.quit()

    # Fail Country, bandside
    def UI_WR_01(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = api_wifi_radio['active']
        try:
            self.assertTrue(actual)
            self.list_steps.append('\n[Pass] 4.1 Check API value active return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 4.1 Check API value active return: ' + str(actual))
            list_steps_fail.append('4.1 API value return wrong.')

        # Check display on WebUI
        ativar_tick_2g = helper.common.check_radio_tick(driver, '.radio-check-controler')
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
        ativar_tick_5g = helper.common.check_radio_tick(driver, '.radio-check-controler')
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

    def UI_WR_02(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') == 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 3. Check API uncheck Ativar return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API uncheck Ativar return: ' + str(actual))
            list_steps_fail.append('3. URL Page Wifi Radio wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_02] Assertion Disable 2.4 GHz interface fail')

    def UI_WR_03(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') == 'true':
            driver.find_element_by_css_selector('.radio-check').click()
        time.sleep(1)
        # Apply
        apply_btn = driver.find_element_by_css_selector('button[value="Aplicar Ajustes"]')
        ActionChains(driver).move_to_element(apply_btn).click().perform()
        time.sleep(10)
        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['active']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 3. Check API uncheck Ativar return: ' + str(actual))
        except AssertionError:
            self.list_steps.append('\n[Fail] 3. Check API uncheck Ativar return: ' + str(actual))
            list_steps_fail.append('3. URL Page Wifi Radio wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_03] Assertion Disable 5 GHz interface fail')

    def UI_WR_04(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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
        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 4. Check Output Power is Medium: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check Output Power is Medium: ' + actual)
            list_steps_fail.append('4.Medium Output Power is wrong: ' + actual)

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
        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 5. Check Output Power is Alto: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check Output Power is Alto: ' + actual)
            list_steps_fail.append('5. Alto Output Power is wrong: ' + actual)

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
        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 6. Check Output Power is Baixo: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check Output Power is Baixo: ' + actual)
            list_steps_fail.append('6. Baixo Output Power is wrong: ' + actual)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_04] Assertion 2.4GHZ output power settings fail')

    def UI_WR_05(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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
        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 4. Check Output Power is Medium: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 4. Check Output Power is Medium: ' + actual)
            list_steps_fail.append('4. Medium Output Power is wrong: ' + actual)

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
        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 5. Check Output Power is Alto: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 5. Check Output Power is Alto: ' + actual)
            list_steps_fail.append('5. Alto Output Power is wrong: ' + actual)

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
        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = api_wifi_radio['basic']['outputPower']
        try:
            self.assertEqual(expected, actual)
            self.list_steps.append('\n[Pass] 6. Check Output Power is Baixo: ' + actual)
        except AssertionError:
            self.list_steps.append('\n[Fail] 6. Check Output Power is Baixo: ' + actual)
            list_steps_fail.append('6. Baixo Output Power is wrong: ' + actual)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_05] Assertion 5GHZ output power settings fail')

    def UI_WR_06(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.1 Check Wireless Mode is OFF: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.1 Check Wireless Mode is OFF: ' + actual_wireless)
            list_steps_fail.append('4.1 OFF Wireless Mode is wrong: ' + actual_wireless)

        try:
            self.assertListEqual(actual_bandwidth, ['20'])
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
        except AssertionError:
            pass
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('4.2 BandWidth is wrong: ' + str(actual_bandwidth))
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
            list_steps_fail.append('5.1 AUTO Wireless Mode is wrong: ' + actual_wireless)
        expected_bandwidth = ['20', '40']
        try:
            self.assertListEqual(actual_bandwidth, expected_bandwidth)
            self.list_steps.append('\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
        except AssertionError:
            pass
            self.list_steps.append('\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('5.2 BandWidth is wrong: ' + str(actual_bandwidth))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.assertListEqual(list_steps_fail, [], '[UI_WR_06] Assertion 2.4GHZ 802.11.n mode settings fail')

    def UI_WR_07(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.assertListEqual(actual_bandwidth, ['20'])
            self.list_steps.append('\n[Pass] 4.1 Check Wireless Mode is OFF: ' + actual_wireless)
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4. Check Wireless Mode is OFF: ' + actual_wireless)
            self.list_steps.append('\n[Pass] 4.2 Check Option of Bandwidth is 20MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('4. OFF Wireless Mode is wrong: ' + actual_wireless)
            list_steps_fail.append('4. BandWidth is wrong: ' + str(actual_bandwidth))

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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.1 Check Wireless Mode is AUTO: ' + actual_wireless)
            list_steps_fail.append('5.1 AUTO Wireless Mode is wrong: ' + actual_wireless)
        expected_bandwidth = ['20', '40', '80']
        try:
            self.assertListEqual(actual_bandwidth, expected_bandwidth)
            self.list_steps.append('\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
        except AssertionError:
            pass
            self.list_steps.append('\n[Pass] 5.2 Check Option of Bandwidth is 20MHz and 40MHz: ' + str(actual_bandwidth))
            list_steps_fail.append('5.2 BandWidth is wrong: ' + str(actual_bandwidth))

        self.assertListEqual(list_steps_fail, [], '[UI_WR_07] Assertion 5GHZ 802.11.n mode settings fail')

    def UI_WR_08(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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
            pass
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        expected_band_width = '20'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_band_width, actual_band_width)
            self.list_steps.append('\n[Pass] 4.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('4.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11b+g+n but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 5.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('5.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.3 Check Wireless Mode is 802.11b+g+n but wrong: ' + actual_wireless)

        try:
            self.assertEqual('upper', actual_sideband)
            self.list_steps.append('\n[Pass] 5.4 Check Side Band: ' + actual_sideband)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.4 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('5.4 Check Side band is upper but wrong: ' + actual_sideband)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 6.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('6.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.3 Check Wireless Mode is 802.11b+g+n but wrong: ' + actual_wireless)

        try:
            self.assertEqual('lower', actual_sideband)
            self.list_steps.append('\n[Pass] 6.4 Check Side Band: ' + actual_sideband)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.4 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('6.4 Check Side band is lower but wrong: ' + actual_sideband)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_08] Assertion 2.4GHZ Bandwidth settings fail')

    def UI_WR_09(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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
            pass
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        expected_band_width = '20'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_band_width, actual_band_width)
            self.list_steps.append('\n[Pass] 4.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('4.2 Check BandWidth set is 20 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)
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
            pass
            self.list_steps.append('\n[Fail] 5.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('5.1  Check Largura de Banda is disable wrong: ' + side_band)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        expected_band_width = '80'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_band_width, actual_band_width)
            self.list_steps.append('\n[Pass] 5.2 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.2 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('5.2 Check BandWidth set is 80 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.3 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 6.1 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.1 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('6.1 Check BandWidth set is 40 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.2 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)

        try:
            self.assertEqual('upper', actual_sideband)
            self.list_steps.append('\n[Pass] 6.3 Check Side Band: ' + actual_sideband)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.3 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('6.3 Check Side band is upper but wrong: ' + actual_sideband)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_band_width = api_wifi_radio['basic']['bandwidth']['set']
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        actual_sideband = api_wifi_radio['basic']['sideband']
        try:
            self.assertEqual('40', actual_band_width)
            self.list_steps.append('\n[Pass] 7.1 Check BandWidth Set: ' + actual_band_width)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 7.1 Check BandWidth Set: ' + actual_band_width)
            list_steps_fail.append('7.1 Check BandWidth set is 20 but wrong: ' + actual_band_width)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 7.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 7.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('7.2 Check Wireless Mode is 802.11a+n+ac but wrong: ' + actual_wireless)

        try:
            self.assertEqual('lower', actual_sideband)
            self.list_steps.append('\n[Pass] 7.3 Check Side Band: ' + actual_sideband)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 7.3 Check Side Band: ' + actual_sideband)
            list_steps_fail.append('7.3 Check Side band is lower but wrong: ' + actual_sideband)

        self.assertListEqual(list_steps_fail, [], '[UI_WR_09] Assertion 5GHZ Bandwidth settings fail')

    def UI_WR_10(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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
            pass
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = 'auto'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 4.2 Check Channel Set: ' + actual_channel)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.2 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('4.2 Check Channel Set is Auto but wrong: ' + actual_channel)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11b+g but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '1'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 5.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('5.1 Check Channel Set is 1 but wrong: ' + actual_channel)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.2 Check Wireless Mode is 802.11b+g but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '13'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 6.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('6.1 Check Channel Set is 13 but wrong: ' + actual_channel)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.2 Check Wireless Mode is 802.11b+g but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '1']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append('\n[Pass] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '9']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '5']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '13']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))

        self.assertListEqual(list_steps_fail, [], '[UI_WR_10] Assertion 2.4GHZ Channel Control settings fail')

    def UI_WR_11(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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
            pass
            self.list_steps.append('\n[Fail] 4.1 Check Largura de Banda is disable: ' + side_band)
            list_steps_fail.append('4.1  Check Largura de Banda is disable wrong: ' + side_band)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = 'auto'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 4.2 Check Channel Set: ' + actual_channel)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.2 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('4.2 Check Channel Set is Auto but wrong: ' + actual_channel)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 4.3 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 4.3 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('4.3 Check Wireless Mode is 802.11a but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '36'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 5.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('5.1 Check Channel Set is 36 but wrong: ' + actual_channel)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 5.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('5.2 Check Wireless Mode is 802.11a but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual_channel = api_wifi_radio['basic']['channel']['set']
        expected_channel = '165'
        actual_wireless = api_wifi_radio['basic']['wirelessMode']
        try:
            self.assertEqual(expected_channel, actual_channel)
            self.list_steps.append('\n[Pass] 6.1 Check Channel Set: ' + actual_channel)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.1 Check Channel Set: ' + actual_channel)
            list_steps_fail.append('6.1 Check Channel Set is 165 but wrong: ' + actual_channel)

        try:
            self.assertEqual(expected_wireless, actual_wireless)
            self.list_steps.append('\n[Pass] 6.2 Check Wireless Mode: ' + actual_wireless)
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 6.2 Check Wireless Mode: ' + actual_wireless)
            list_steps_fail.append('6.2 Check Wireless Mode is 802.11a but wrong: ' + actual_wireless)
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '36']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append('\n[Pass] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('7. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'lower', '157']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('8. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '40']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('9. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '40', 'upper', '161']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('10. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '80', 'upper', '36']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 11. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 11. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('11. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = [api_wifi_radio['basic']['wirelessMode'], api_wifi_radio['basic']['bandwidth']['set'],
                  api_wifi_radio['basic']['sideband'], api_wifi_radio['basic']['channel']['set']]
        expected = [expected_wireless, '80', 'upper', '161']
        try:
            self.assertListEqual(expected, actual)
            self.list_steps.append(
                '\n[Pass] 12. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 12. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))
            list_steps_fail.append('12. Check Value of WireMode, BandWidth, SideBand, Channel: ' + str(actual))

        self.assertListEqual(list_steps_fail, [], '[UI_WR_11] Assertion 5GHZ Channel Control settings fail')

    def UI_WR_12(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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

        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertTrue(actual)
            self.list_steps.append(
                '\n[Pass] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
            list_steps_fail.append('4. Check Value of Beamforming is Enable is true wrong: ' + str(actual))
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
        api_wifi_radio = helper.common.api_wifi_radio(0)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
            list_steps_fail.append('5. Check Value of Beamforming is Disable is false wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_12] Assertion 2.4GHZ Beamforming settings fail')

    def UI_WR_13(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        if helper.common.check_radio_tick(driver, '.radio-check-controler') != 'true':
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

        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertTrue(actual)
            self.list_steps.append(
                '\n[Pass] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append(
                '\n[Fail] 4. Check Value of Beamforming is Enable is true: ' + str(actual))
            list_steps_fail.append('4. Check Value of Beamforming is Enable is true wrong: ' + str(actual))
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
        api_wifi_radio = helper.common.api_wifi_radio(1)
        actual = api_wifi_radio['advanced']['beamforming']
        try:
            self.assertFalse(actual)
            self.list_steps.append('\n[Pass] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
        except AssertionError:
            pass
            self.list_steps.append('\n[Fail] 5. Check Value of Beamforming is Disable is false: ' + str(actual))
            list_steps_fail.append('5. Check Value of Beamforming is Disable is false wrong: ' + str(actual))
        self.assertListEqual(list_steps_fail, [], '[UI_WR_13] Assertion 5GHZ Beamforming settings fail')

    def UI_WR_14(self):
        driver = self.driver
        self.def_name = helper.common.get_func_name()
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
        driver.find_element_by_css_selector('button[value=refresh]'). click()
        time.sleep(2)
        api_wifi_scan_result = helper.common.api_wifi_scanResult(0)
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
            pass
            self.list_steps.append('\n[Fail] 4.1 Check quantity of result: ' + str(len(actual)))
            list_steps_fail.append('\n4.1 Check quantity of result wrong: \nActual: ' + str(len(actual))
                                   + '\nExpected: ' + str(len(expected)))

        for i in range(len(actual)):
            for j in range(len(expected)):
                if actual[i][0] == expected[j][0]:
                    try:
                        self.assertListEqual(expected[j], actual[i])
                        self.list_steps.append('\n[Pass] 4.'+str(i)+' Check Wifi list information: ' + str(actual[i]))
                    except AssertionError:
                        pass
                        self.list_steps.append('\n[Fail] 4.'+str(i)+' Check Wifi list information: ' + str(actual[i]))
                        list_steps_fail.append('\n4. Check Wifi info of '+actual[i][0]+' wrong: \nActual: '
                                               + str(actual[i]) +'\nExpected: '+ str(expected[j]))
                    break
                else:
                    continue

        self.assertListEqual(list_steps_fail, [], '[UI_WR_14] Assertion Wi-Fi Access point scanning fail')

if __name__ == '__main__':
    helper.runner.main()
