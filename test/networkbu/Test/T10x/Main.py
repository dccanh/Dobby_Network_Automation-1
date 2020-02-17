#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
# from Helper.t10x.config.captcha import *
from Helper.t10x.config.data_expected import *
from Helper.t10x.config.elements import *
# from Helper.t10x.config.read_config import *
from Helper.t10x.secure_crt.common import *
from Helper.t10x.common import *
from selenium import webdriver
from selenium.webdriver.support.select import Select


class MAIN(unittest.TestCase):
    def setUp(self):
        try:
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            if '_Firefox' in self._testMethodName:
                self.driver = webdriver.Firefox(executable_path=driver_firefox_path)
            elif '_Edge' in self._testMethodName:
                self.driver = webdriver.Edge()
            elif '_Safari' in self._testMethodName:
                self.driver = webdriver.Safari(driver_safari_path)
            else:
                self.driver = webdriver.Chrome(driver_path)
            self.driver.maximize_window()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        try:
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        except:
            # Connect by wifi if internet is down to handle exception for PPPoE
            os.system('netsh wlan connect ssid=HVNWifi name=HVNWifi')
            time.sleep(1)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
            time.sleep(5)
            # Connect by LAN again
            os.system('netsh wlan disconnect')
            time.sleep(1)
        self.driver.quit()

    def test_04_Verify_the_Web_UI_connection_through_Gateway_IP(self):
        self.key = 'MAIN_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ~~~~~~~~~~~~~~~~~~~~~~ Get info URL, ACCOUNT ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Get and write URL
            get_url_ipconfig(ipconfig_field='Default Gateway')

            url_config = get_config('URL', 'url')
            time.sleep(1)
            check_url = True if url_config is not '' else False
            # Check url, account info is not None
            list_actual1 = [check_url]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Get result by command success\n')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Get result by command success. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: Actual not None')
            list_step_fail.append('1, 2. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_config)
            check_lg_page_displayed = len(driver.find_elements_by_css_selector(lg_page)) != 0
            check_lg_id_field = len(driver.find_elements_by_css_selector(lg_user)) != 0
            check_lg_password_field = len(driver.find_elements_by_css_selector(lg_password)) != 0
            check_lg_captcha_img = len(driver.find_elements_by_css_selector(lg_captcha_src)) != 0
            check_lg_captcha_field = len(driver.find_elements_by_css_selector(lg_captcha_box)) != 0

            list_actual2 = [check_lg_page_displayed,
                           check_lg_id_field,
                           check_lg_password_field,
                           check_lg_captcha_img,
                           check_lg_captcha_field]
            list_expected2 = [return_true]*5
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check login Page displayed, id, password, captcha img, captcha input field\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check login Page displayed, id, password, captcha img, captcha input field. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Connect Wifi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            wifi_name = get_config('GENERAL', 'wifi_ssid_2g')
            command = 'netsh wlan connect ssid="' + wifi_name + '" name="' + wifi_name+'" interface=Wi-Fi'
            check_connect_wifi = subprocess.check_output(command)
            check_connect_wifi = check_connect_wifi.decode('ascii').strip()
            list_actual3 = [check_connect_wifi]
            list_expected3 = [connect_wifi_msg]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check Msg connect wifi successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Msg connect wifi successfully. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check login again ~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_config)
            check_lg_page_displayed = len(driver.find_elements_by_css_selector(lg_page)) != 0
            check_lg_id_field = len(driver.find_elements_by_css_selector(lg_user)) != 0
            check_lg_password_field = len(driver.find_elements_by_css_selector(lg_password)) != 0
            check_lg_captcha_img = len(driver.find_elements_by_css_selector(lg_captcha_src)) != 0
            check_lg_captcha_field = len(driver.find_elements_by_css_selector(lg_captcha_box)) != 0

            list_actual4 = [check_lg_page_displayed,
                           check_lg_id_field,
                           check_lg_password_field,
                           check_lg_captcha_img,
                           check_lg_captcha_field]
            list_expected4 = [return_true]*5
            check = assert_list(list_actual4, list_expected4)
            os.system('netsh wlan disconnect')
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5 Check login Page displayed, id, password, captcha img, captcha input field\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check login Page displayed, id, password, captcha img, captcha input field. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_05_Verify_the_Default_setting_of_Language(self):
        self.key = 'MAIN_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url = get_config('URL', 'url')
        set_language_1 = 'English'
        set_language_2 = 'Tiếng Việt'

        filename_ = 'account.txt'
        command_ = 'capitest get Device.Users.User.2. leaf'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)

            # System > Restart / Factory > Factory Reset > OK
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_reset).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_pop_factory_reset).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(btn_ok).click()
            # Wait until dialog loading disappear
            time.sleep(1)

            check_time_out = wait_popup_disappear(driver, dialog_loading)

            run_cmd(command_, filename_)
            time.sleep(3)
            # Get account information from web server and write to config.txt
            url_login = get_config('URL', 'url')
            get_result_command_from_server(url_ip=url_login, filename=filename_)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            list_actual1 = [check_time_out]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Login and Restore successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Login and Restore fail. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~ Change Language
        try:
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            driver.get(url + homepage)
            time.sleep(1)

            # System > Language
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_language).click()

            language_selected = driver.find_element_by_css_selector(language_selected_text)
            if language_selected.text != set_language_1:
                language_selected.click()
                language_options = driver.find_elements_by_css_selector(list_language_option)
                for o in language_options:
                    if o.text == set_language_1:
                        o.click()

                time.sleep(1)
                # Apply
                driver.find_element_by_css_selector(pop_up_btn_apply).click()
                time.sleep(3)
                # Confirm
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(2)
            # Goto Login page
            driver.get(url)
            time.sleep(3)

            welcome_text = driver.find_element_by_css_selector(lg_welcome_text).text

            list_actual2 = [welcome_text]
            list_expected2 = [expected_welcome_text_en]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3,4. Change language and check in login\n')
        except:
            self.list_steps.append(
                f'[Fail] 3,4. Change language and check in login. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append(
                '3,4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Again
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            driver.get(url + homepage)
            time.sleep(1)

            # System > Restart / Factory > Factory Reset > OK
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_reset).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_pop_factory_reset).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(btn_ok).click()
            # Wait until dialog loading disappear
            time.sleep(1)

            check_time_out = wait_popup_disappear(driver, dialog_loading)

            run_cmd(command_, filename_)
            time.sleep(3)
            # Get account information from web server and write to config.txt
            url_login = get_config('URL', 'url')
            get_result_command_from_server(url_ip=url_login, filename=filename_)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            list_actual3 = [check_time_out]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Login and Restore successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Login and Restore fail. Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~ Change Language and verify
        try:
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            driver.get(url + homepage)
            time.sleep(1)

            # System > Language
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_language).click()

            language_selected = driver.find_element_by_css_selector(language_selected_text)
            if language_selected.text != set_language_2:
                language_selected.click()
                language_options = driver.find_elements_by_css_selector(list_language_option)
                for o in language_options:
                    if o.text == set_language_2:
                        o.click()

                time.sleep(1)
                # Apply
                driver.find_element_by_css_selector(pop_up_btn_apply).click()
                time.sleep(3)
                # Confirm
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(2)
            # Goto Login page
            driver.get(url)
            time.sleep(3)

            welcome_text = driver.find_element_by_css_selector(lg_welcome_text).text

            list_actual4 = [welcome_text]
            list_expected4= [expected_welcome_text_vi]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6,7. Change language and check in login\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6,7. Change language and check in login. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '6,7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_06_Verify_the_Web_UI_connection_through_domain_address(self):
        global list_actual, list_expected, password_config, url_config, user_config
        self.key = 'MAIN_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        sub_url = get_config('URL', 'sub_url')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Get and write URL
            os.system('netsh wlan disconnect')
            driver.get(sub_url)
            time.sleep(1)
            check_lg_page_displayed = len(driver.find_elements_by_css_selector(lg_page)) != 0
            check_lg_id_field = len(driver.find_elements_by_css_selector(lg_user)) != 0
            check_lg_password_field = len(driver.find_elements_by_css_selector(lg_password)) != 0
            check_lg_captcha_img = len(driver.find_elements_by_css_selector(lg_captcha_src)) != 0
            check_lg_captcha_field = len(driver.find_elements_by_css_selector(lg_captcha_box)) != 0

            list_actual = [check_lg_page_displayed,
                           check_lg_id_field,
                           check_lg_password_field,
                           check_lg_captcha_img,
                           check_lg_captcha_field]
            list_expected = [return_true] * 5
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check login Page displayed, id, password, captcha img, captcha input field in LAN\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Get result by command success. Actual: {str(list_actual)}. Expected: Actual not None')
            list_step_fail.append('1, 2. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Connect Wifi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            wifi_name = get_config('GENERAL', 'wifi_ssid')
            command = 'netsh wlan connect ssid="' + wifi_name + '" name="' + wifi_name+'" interface=Wi-Fi'
            check_connect_wifi = subprocess.check_output(command)
            check_connect_wifi = check_connect_wifi.decode('ascii').strip()
            list_actual = [check_connect_wifi]
            list_expected = [connect_wifi_msg]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Msg connect wifi successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Msg connect wifi successfully. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check login again ~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(sub_url)
            wait_popup_disappear(driver, dialog_loading)
            check_lg_page_displayed = len(driver.find_elements_by_css_selector(lg_page)) != 0
            check_lg_id_field = len(driver.find_elements_by_css_selector(lg_user)) != 0
            check_lg_password_field = len(driver.find_elements_by_css_selector(lg_password)) != 0
            check_lg_captcha_img = len(driver.find_elements_by_css_selector(lg_captcha_src)) != 0
            check_lg_captcha_field = len(driver.find_elements_by_css_selector(lg_captcha_box)) != 0

            list_actual = [check_lg_page_displayed,
                           check_lg_id_field,
                           check_lg_password_field,
                           check_lg_captcha_img,
                           check_lg_captcha_field]
            list_expected = [return_true]*5
            check = assert_list(list_actual, list_expected)
            os.system('netsh wlan disconnect')
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check login Page displayed, id, password, captcha img, captcha input field\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check login Page displayed, id, password, captcha img, captcha input field. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_07_Verify_the_Login_page(self):
        self.key = 'MAIN_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        LANGUAGE = "English"
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Get and write URL
            driver.get(url_login)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            act = ActionChains(driver)
            act.send_keys(user_request)
            act.send_keys(Keys.TAB)
            act.send_keys(pass_word)
            act.send_keys(Keys.TAB)
            act.send_keys(captcha_text)
            act.perform()

            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(3)
            # Check Privacy Policy
            policy_popup = driver.find_elements_by_css_selector(lg_privacy_policy_pop)
            if len(policy_popup):
                ActionChains(driver).move_to_element(policy_popup[0]).click().send_keys(Keys.ARROW_DOWN).perform()
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(3)

            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_login]
            list_expected1 = [return_true]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check function TAB key in login')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check function TAB key in login. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2,3. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Change Language
        try:
            # Goto Homepage
            driver.get(url_login + homepage)
            time.sleep(1)

            # System > Language
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_language).click()

            language_selected = driver.find_element_by_css_selector(language_selected_text)
            if language_selected.text != LANGUAGE:
                language_selected.click()
                language_options = driver.find_elements_by_css_selector(list_language_option)
                for o in language_options:
                    if o.text == LANGUAGE:
                        o.click()
                        break

                time.sleep(1)
                # Apply
                driver.find_element_by_css_selector(pop_up_btn_apply).click()
                time.sleep(3)
                # Confirm
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(2)
            # Goto Login page
            driver.get(url_login)
            time.sleep(3)

            welcome_text = driver.find_element_by_css_selector(lg_welcome_text).text
            id_holder = driver.find_element_by_css_selector(lg_user).get_attribute('placeholder')
            password_holder = driver.find_element_by_css_selector(lg_password).get_attribute('placeholder')
            captcha_holder = driver.find_element_by_css_selector(lg_captcha_box).get_attribute('placeholder')
            extra_lg_info = driver.find_element_by_css_selector(lg_extra_info).text

            list_actual2 = [welcome_text,
                           id_holder,
                           password_holder,
                           captcha_holder,
                           extra_lg_info]
            list_expected2 = [expected_welcome_text_en,
                             exp_lg_id_holder,
                             exp_lg_password_holder,
                             exp_lg_captcha_holder,
                             exp_lg_extra_info]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Change language and check in login\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change language and check in login. Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_08_Verify_the_Humax_Retail_CPE_Site_operation(self):
        global list_actual, list_expected
        self.key = 'MAIN_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Get and write URL
            driver.get(url_login)
            time.sleep(1)
            tooltip_img = driver.find_element_by_css_selector(lg_company_img).get_attribute('title')
            list_actual = [tooltip_img]
            list_expected = [exp_tooltip_img]

            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check tooltip in Company Img')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check tooltip in Company Img. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Click to image
        try:
            driver.find_element_by_css_selector(lg_company_img).click()
            time.sleep(3)
            driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(1)
            check_current_url = exp_quantum_url in driver.current_url
            list_actual = [check_current_url]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Check current URL\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check current URL. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_09_Verify_the_Login_operation(self):
        self.key = 'MAIN_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        NEW_PASSWORD = 'Dinhcongcanh1'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt

        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)

        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check pop-up welcome appear')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check pop-up welcome appear. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2,3. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Click to image
        try:
            # Click to Language
            driver.find_element_by_css_selector(welcome_language).click()
            time.sleep(0.2)

            # Choose Language
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_language)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_language:
                    t.click()
                    break

            # Click to time zone
            driver.find_element_by_css_selector(welcome_time_zone).click()
            time.sleep(0.2)

            # Choose time zone in drop down: Vn zone GMT +7
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_time_zone)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_time_zone:
                    t.click()
                    break
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            # Next Change pw
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Operation Mode
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Internet Setup 1
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Internet setup 2
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Wireless Setup
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Humax Wifi App
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            check_dialog_disappear = wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)
            check_home_displayed = driver.find_element_by_css_selector(home_view_wrap).is_displayed()
            list_actual2 = [check_dialog_disappear, check_home_displayed]
            list_expected2 = [return_true, return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check Welcome dialog disappear, Home page display\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4.Check Welcome dialog disappear, Home page display. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_10_Verify_the_operation_at_Login(self):
        self.key = 'MAIN_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 3 mins for factory
        # time.sleep(250)
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt

        get_result_command_from_server(url_ip=url_login, filename=filename_2)

        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(7)

            # Check Privacy Policy
            check_policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) != 0

            list_actual1 = [check_policy_popup]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check pop-up Privacy is displayed')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check pop-up Privacy is displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Check Privacy
        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)
            # Check Privacy Policy disappear
            check_policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) != 0
            # Check Login page appear
            check_lg_page = driver.find_element_by_css_selector(lg_page).is_displayed()
            list_actual2 = [check_policy_popup, check_lg_page]
            list_expected2 = [return_false, return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Send: ESC. Check Privacy disappear, Home page displayed\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Send: ESC. Check Privacy disappear, Home page displayed. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login again ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(5)

            # Check Privacy Policy
            check_policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) != 0
            check_btn_agree = driver.find_element_by_css_selector(btn_ok).get_property('disabled')

            list_actual3 = [check_policy_popup, check_btn_agree]
            list_expected3 = [return_true, return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check pop-up Privacy is displayed, Agree disabled')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check pop-up Privacy is displayed, Agree disabled. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~ Check Check scroll ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            check_policy_popup = driver.find_element_by_css_selector(lg_privacy_policy_pop)
            act = ActionChains(driver)
            act.move_to_element(check_policy_popup)
            act.click()
            act.send_keys(Keys.ARROW_DOWN)
            act.send_keys(Keys.PAGE_DOWN)
            act.send_keys(Keys.PAGE_UP)
            act.perform()
            time.sleep(1)
            # Check btn Agree enabled
            check_btn_agree = driver.find_element_by_css_selector(btn_ok).get_property('disabled')

            list_actual4 = [check_btn_agree]
            list_expected4 = [return_false]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Send key: PAGE_UP, DOWN. Check Agree enabled')
        except:
            self.list_steps.append(
                f'[Fail] 5. Send key: PAGE_UP, DOWN. Check Agree enabled. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('5. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~ Check Welcome ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Click Agree
            driver.find_element_by_css_selector(btn_ok).click()
            # Check Welcome Dialog appear
            time.sleep(3)
            check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            list_actual5 = [check_welcome]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Click Agree. Check Welcome dialog displayed')
        except:
            self.list_steps.append(
                f'[Fail] 6. Click Agree. Check Welcome dialog displayed. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('6. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~ Logout and Login Again ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Logout
            driver.get(url_login)
            check_lg_page = len(driver.find_elements_by_css_selector(lg_page) ) != 0
            # Input values
            time.sleep(3)
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(5)

            # Check Welcome dialog
            check_welcome = driver.find_element_by_css_selector(lg_welcome_header).is_displayed()
            list_actual6 = [check_lg_page, check_welcome]
            list_expected6 = [return_true, return_true]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Login again. Check Welcome dialog displayed')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Login again. Check Welcome dialog displayed. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_11_Verify_the_operation_at_Login_page_with_incorrect_id_pw(self):
        self.key = 'MAIN_11'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        WRONG_CAPTCHA = 'ciel'
        WRONG_USER = 'ciel'
        WRONG_PW = 'ciel'
        # Get account information from web server and write to config.txt
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # ~~~~~~~~~~~~~~~~~ Correct ID/PW; InCorrect Captcha
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)
            # Correct ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Incorrect Captcha
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(WRONG_CAPTCHA)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(5)

            # Check Msg Error
            msg_error = driver.find_element_by_css_selector(lg_msg_error).text
            # Check Login page displayed
            check_lg_page = driver.find_element_by_css_selector(lg_page).is_displayed()

            list_actual1 = [msg_error, check_lg_page]
            list_expected1 = [exp_wrong_captcha, return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Error Wrong Captcha, Page login displayed.')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Error Wrong Captcha Page login displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2. Assertion wong')
        # ~~~~~~~~~~~~~~~~~ Incorrect ID/PW; Correct Captcha
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)
            # InCorrect ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(WRONG_USER)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(WRONG_PW)
            time.sleep(1)
            # Correct Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(5)

            # Check MSG Error
            msg_error = driver.find_element_by_css_selector(lg_msg_error).text
            # Check Login page displayed
            check_lg_page = driver.find_element_by_css_selector(lg_page).is_displayed()
            list_actual2 = [msg_error, check_lg_page]
            list_expected2 = [exp_wrong_id_pw, return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Error wrong ID& PW.')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Error wrong ID& PW. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong')

        # ~~~~~~~~~~~~~~~~~ Incorrect ID/PW; Correct Captcha Login 10 times
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)
            # InCorrect ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(WRONG_USER)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(WRONG_PW)
            time.sleep(1)
            # Correct Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            list_error_msg = []
            # Login 10 times
            for i in range(1, 11):
                driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
                time.sleep(2)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                list_error_msg.append(msg_error)
            # 9 errors
            check_error_msg = True
            for e in list_error_msg[:9]:
                if e != exp_wrong_id_pw:
                    check_error_msg = False

            # Set up minute<=0, second
            min = [i for i in range(0, 2)]
            sec = [i for i in range(1, 61)]
            check_error_msg_time = False
            for i in min:
                for j in sec:
                    error_format = 'Too many failed login attempts. Try again in {min} minute(s) {sec} seconds.'.format(min=str(i), sec=str(j))
                    if error_format == list_error_msg[9]:
                        check_error_msg_time = True

            check_lg_btn = driver.find_element_by_css_selector(lg_btn_login).is_enabled()

            list_actual3 = [check_error_msg, check_error_msg_time, check_lg_btn]
            list_expected3 = [return_true, check_error_msg_time, return_false]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check Error wrong ID& PW: 9 msg warning, 1 msg count time, lgin btn enabled after count.')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Error wrong ID& PW: 9 msg warning, 1 msg count time, lgin btn enabled after count. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong')

        # ~~~~~~~~~~~~~~~~~ Incorrect ID/PW; Correct Captcha Login 2 times more
        try:
            while True:
                time.sleep(0.5)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                if msg_error == '':
                    break

            time.sleep(5)
            driver.get(url_login)
            time.sleep(2)
            # InCorrect ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(WRONG_USER)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(WRONG_PW)
            time.sleep(1)
            # Correct Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            list_error_msg = []
            # Login 2 times
            for i in range(1, 3):
                driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
                time.sleep(2)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                list_error_msg.append(msg_error)
            # 2 errors
            check_error_msg = True
            for e in list_error_msg[:1]:
                if e != exp_wrong_id_pw:
                    check_error_msg = False

            # Set up minute<=2, second
            min = [i for i in range(0, 3)]
            sec = [i for i in range(1, 61)]
            check_error_msg_time = False
            for i in min:
                for j in sec:
                    error_format = 'Too many failed login attempts. Try again in {min} minute(s) {sec} seconds.'.format(min=str(i), sec=str(j))
                    if error_format == list_error_msg[1]:
                        check_error_msg_time = True

            check_lg_btn = driver.find_element_by_css_selector(lg_btn_login).is_enabled()

            list_actual4 = [check_error_msg, check_error_msg_time, check_lg_btn]
            list_expected4 = [return_true, check_error_msg_time, return_false]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Error wrong ID& PW: 1 msg warning, 1 msg count time, lgin btn enabled after count.')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Error wrong ID& PW: 1 msg warning, 1 msg count time, lgin btn enabled after count. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('5. Assertion wong')

        # ~~~~~~~~~~~~~~~~~ Incorrect ID/PW; Correct Captcha Login 2 times more
        try:

            while True:
                time.sleep(0.5)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                if msg_error == '':
                    break

            time.sleep(5)
            driver.get(url_login)
            time.sleep(2)
            # InCorrect ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(WRONG_USER)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(WRONG_PW)
            time.sleep(1)
            # Correct Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            list_error_msg = []
            # Login 2 times
            for i in range(1, 3):
                driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
                time.sleep(2)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                list_error_msg.append(msg_error)
            # 2 errors
            check_error_msg = True
            for e in list_error_msg[:1]:
                if e != exp_wrong_id_pw:
                    check_error_msg = False

            # Set up minute<=2, second
            min = [i for i in range(0, 5)]
            sec = [i for i in range(1, 61)]
            check_error_msg_time = False
            for i in min:
                for j in sec:
                    error_format = 'Too many failed login attempts. Try again in {min} minute(s) {sec} seconds.'.format(
                        min=str(i), sec=str(j))
                    if error_format == list_error_msg[1]:
                        check_error_msg_time = True

            check_lg_btn = driver.find_element_by_css_selector(lg_btn_login).is_enabled()

            list_actual5 = [check_error_msg, check_error_msg_time, check_lg_btn]
            list_expected5 = [return_true, check_error_msg_time, return_false]
            check = assert_list(list_actual5, list_expected5)
            # Wait until Done
            while True:
                time.sleep(0.5)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                if msg_error == '':
                    break
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check Error wrong ID& PW: 1 msg warning, 1 msg count time, lgin btn enabled after count.')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Error wrong ID& PW: 1 msg warning, 1 msg count time, lgin btn enabled after count. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_13_Verify_the_Log_out_operation(self):
        self.key = 'MAIN_13'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        login(driver)
        wait_popup_disappear(driver, dialog_loading)
        if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
            handle_winzard_welcome(driver)
            wait_popup_disappear(driver, dialog_loading)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            tooltip = driver.find_element_by_css_selector(logout_btn).get_attribute('title')
            driver.find_element_by_css_selector(logout_btn).click()

            dialog_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            btn_ok_display = driver.find_element_by_css_selector(btn_ok).is_displayed()
            check_btn_cancel = driver.find_element_by_css_selector(btn_cancel)
            btn_cancel_display = check_btn_cancel.is_displayed()
            # Click cancel
            time.sleep(0.2)
            check_btn_cancel.click()
            check_home_page = driver.find_element_by_css_selector(home_view_wrap).is_displayed()
            list_actual1 = [tooltip, dialog_msg, btn_ok_display, btn_cancel_display, check_home_page]
            list_expected1 = [exp_tooltip_logout, exp_logout_msg, return_true, return_true, return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check logout: Check tooltip, dialog msg, btn ok, cancel and home page is displayed')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check logout: Check tooltip, dialog msg, btn ok, cancel and home page is displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.find_element_by_css_selector(logout_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(btn_ok).click()

            # Click cancel
            check_login_page = driver.find_element_by_css_selector(lg_page).is_displayed()
            list_actual2 = [check_login_page]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Click Logout >Ok: Check login page is displayed')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Click Logout >Ok: Check login page is displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_14_Verify_the_time_out_operation(self):
        self.key = 'MAIN_14'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        login(driver)
        wait_popup_disappear(driver, dialog_loading)
        if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
            handle_winzard_welcome(driver)
            wait_popup_disappear(driver, dialog_loading)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Wait 20 mins
            sleep_time = 20*60
            time.sleep(sleep_time)
            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)

            msg_time_out = driver.find_element_by_css_selector(content).text

            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()

            # Home is display
            check_home = driver.find_element_by_css_selector(home_view_wrap).is_displayed()
            list_actual1 = [msg_time_out, check_home]
            list_expected1 = [exp_time_out_msg, return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Time out: Check msg time out, home page is displayed')
        except:
            self.list_steps.append(
                f'[Fail] 1. Time out: Check msg time out, home page is displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            sleep_time = 20 * 60
            # Click cancel
            check_login_page = driver.find_element_by_css_selector(lg_page).is_displayed()
            list_actual2 = [check_login_page]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Click Logout >Ok: Check login page is displayed')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Click Logout >Ok: Check login page is displayed. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_16_Check_Chrome_Browser_behavior(self):
        self.key = 'MAIN_16'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'sub_url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)

            list_actual1 = [url_login+'/']
            list_expected1 = [driver.current_url]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check URL Login Page in Chrome')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check URL Login Page in Chrome. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)

            user_value = driver.find_element_by_css_selector(lg_user).get_attribute('value')
            captcha_value = driver.find_element_by_css_selector(lg_captcha_box).get_attribute('value')
            # Click Login
            driver.find_element_by_css_selector(lg_btn_login).click()

            list_actual2 = [user_value, captcha_value]
            list_expected2 = [user_request, captcha_text]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2,3. Check input correct username and captcha')
        except:
            self.list_steps.append(
                f'[Fail] 2,3. Check input correct username and captcha. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2,3. Assertion wong')

        try:
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(url_login + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)

            list_tab_text = driver.find_elements_by_css_selector(ls_tab)
            list_tab_text = [i.text for i in list_tab_text]

            list_actual3 = [list_tab_text]
            list_expected3 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check Menu tree in Home page via domain address')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Menu tree in Home page via domain address. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong')

        try:
            url_login = get_config('URL', 'url')
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(url_login + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)

            list_tab_text = driver.find_elements_by_css_selector(ls_tab)
            list_tab_text = [i.text for i in list_tab_text]

            list_actual4 = [list_tab_text]
            list_expected4 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check Menu tree in Home page via IP address')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Menu tree in Home page via IP address. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_17_Check_Firefox_Browser_behavior(self):
        self.key = 'MAIN_17'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'sub_url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)

            list_actual1 = [url_login + '/']
            list_expected1 = [driver.current_url]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check URL Login Page in Chrome')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check URL Login Page in Chrome. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)

            user_value = driver.find_element_by_css_selector(lg_user).get_attribute('value')
            captcha_value = driver.find_element_by_css_selector(lg_captcha_box).get_attribute('value')
            # Click Login
            driver.find_element_by_css_selector(lg_btn_login).click()

            list_actual2 = [user_value, captcha_value]
            list_expected2 = [user_request, captcha_text]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2,3. Check input correct username and captcha')
        except:
            self.list_steps.append(
                f'[Fail] 2,3. Check input correct username and captcha. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2,3. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(url_login + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)

            list_tab_text = driver.find_elements_by_css_selector(ls_tab)
            list_tab_text = [i.text for i in list_tab_text]

            list_actual3 = [list_tab_text]
            list_expected3 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check Menu tree in Home page via domain address')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Menu tree in Home page via domain address. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong')

        try:
            url_login = get_config('URL', 'url')
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(url_login + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)

            list_tab_text = driver.find_elements_by_css_selector(ls_tab)
            list_tab_text = [i.text for i in list_tab_text]

            list_actual4 = [list_tab_text]
            list_expected4 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check Menu tree in Home page via IP address')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Menu tree in Home page via IP address. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # NOT GOOD
    def test_18_Check_Edge_Browser_behavior(self):
        self.key = 'MAIN_18'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            driver.get(url_login)
            time.sleep(1)

            list_actual1 = [url_login]
            list_expected1 = [driver.current_url]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check URL Login Page in Edge')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check URL Login Page in Edge. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)

            user_value = driver.find_element_by_css_selector(lg_user).get_attribute('value')
            captcha_value = driver.find_element_by_css_selector(lg_captcha_box).get_attribute('value')

            list_actual2 = [user_value, captcha_value]
            list_expected2 = [user_request, captcha_text]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check input correct username and captcha')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check input correct username and captcha. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_20_Verify_the_Winzard_Main_page(self):
        self.key = 'MAIN_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt

        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            url_login = get_config('URL', 'url')
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')
            driver.get(url_login)
            time.sleep(2)
            driver.find_element_by_css_selector(lg_user).send_keys(user_request)
            time.sleep(1)
            driver.find_element_by_css_selector(lg_password).send_keys(pass_word)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_element_by_css_selector(lg_btn_login).click()

            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Check Privacy Policy
            time.sleep(2)
            policy_popup = driver.find_elements_by_css_selector(lg_privacy_policy_pop)
            if len(policy_popup):
                ActionChains(driver).move_to_element(policy_popup[0]).click().send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(1)
                check_agree_enable = driver.find_element_by_css_selector(btn_ok).is_enabled()
                time.sleep(3)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_agree_enable, check_welcome]
            list_expected1 = [return_true]*2
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check Agree button is enable, Click Agree, Welcome page display')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Agree button is enable, Click Agree, Welcome page display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            text_welcome_title = driver.find_element_by_css_selector(lg_welcome_header).text
            text_welcome_msg_up = driver.find_element_by_css_selector(welcome_msg_up).text
            text_welcome_pic_first = driver.find_element_by_css_selector(welcome_first_pic).text
            text_welcome_pic_second = driver.find_element_by_css_selector(welcome_second_pic).text
            text_welcome_pic_third = driver.find_element_by_css_selector(welcome_third_pic).text
            text_welcome_msg_down = driver.find_element_by_css_selector(welcome_msg_down).text
            language_box = len(driver.find_elements_by_css_selector(welcome_language_wz)) != 0
            timezone_box = len(driver.find_elements_by_css_selector(welcome_timezone_wz)) != 0
            text_welcome_btn_start = driver.find_element_by_css_selector(welcome_start_btn).text
            list_actual2 = [text_welcome_title, text_welcome_msg_up, text_welcome_pic_first,
                            text_welcome_pic_second, text_welcome_pic_third, text_welcome_msg_down,
                            language_box, timezone_box, text_welcome_btn_start]
            list_expected2 = [header_login_text, exp_welcome_msg_up, exp_internet,
                              exp_wireless, exp_changepw, exp_welcome_msg_down,
                              return_true, return_true, 'Start']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check title, message up, icon Internet, Wireless, Change PW,'
                                   'message down, language box, timezone box, Start text')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check title, message up, icon Internet, Wireless, Change PW, '
                f'message down, language box, timezone box, Start text'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # def test_21_Verify_the_Language_operation_on_Winzard_page(self):
    #     self.key = 'MAIN_20'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     url_login = get_config('URL', 'url')
    #     user_request = get_config('ACCOUNT', 'user')
    #     pass_word = get_config('ACCOUNT', 'password')
    #     filename = '1'
    #     commmand = 'factorycfg.sh -a'
    #     run_cmd(commmand, filename=filename)
    #     # Wait 5 mins for factory
    #     time.sleep(100)
    #     wait_DUT_activated(url_login)
    #     wait_ping('192.168.1.1')
    #
    #     filename_2 = 'account.txt'
    #     commmand_2 = 'capitest get Device.Users.User.2. leaf'
    #     run_cmd(commmand_2, filename_2)
    #     time.sleep(3)
    #     # Get account information from web server and write to config.txt
    #
    #     user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         url_login = get_config('URL', 'url')
    #         user_request = get_config('ACCOUNT', 'user')
    #         pass_word = get_config('ACCOUNT', 'password')
    #         driver.get(url_login)
    #         time.sleep(2)
    #         driver.find_element_by_css_selector(lg_user).send_keys(user_request)
    #         time.sleep(1)
    #         driver.find_element_by_css_selector(lg_password).send_keys(pass_word)
    #         time.sleep(1)
    #         # Captcha
    #         captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
    #         captcha_text = get_captcha_string(captcha_src)
    #         driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
    #         time.sleep(1)
    #         driver.find_element_by_css_selector(lg_btn_login).click()
    #
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #         # Check Privacy Policy
    #         time.sleep(2)
    #         policy_popup = driver.find_elements_by_css_selector(lg_privacy_policy_pop)
    #         if len(policy_popup):
    #             ActionChains(driver).move_to_element(policy_popup[0]).click().send_keys(Keys.ARROW_DOWN).perform()
    #             time.sleep(1)
    #             check_agree_enable = driver.find_element_by_css_selector(btn_ok).is_enabled()
    #             time.sleep(3)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(2)
    #         check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
    #
    #         list_actual1 = [check_agree_enable, check_welcome]
    #         list_expected1 = [return_true]*2
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 1. Check Agree button is enable, Click Agree, Welcome page display')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1. Check Agree button is enable, Click Agree, Welcome page display. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         list_step_fail.append('1. Assertion wong')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         text_welcome_title = driver.find_element_by_css_selector(lg_welcome_header).text
    #         text_welcome_msg_up = driver.find_element_by_css_selector(welcome_msg_up).text
    #         text_welcome_pic_first = driver.find_element_by_css_selector(welcome_first_pic).text
    #         text_welcome_pic_second = driver.find_element_by_css_selector(welcome_second_pic).text
    #         text_welcome_pic_third = driver.find_element_by_css_selector(welcome_third_pic).text
    #         text_welcome_msg_down = driver.find_element_by_css_selector(welcome_msg_down).text
    #         language_box = len(driver.find_elements_by_css_selector(welcome_language_wz)) != 0
    #         timezone_box = len(driver.find_elements_by_css_selector(welcome_timezone_wz)) != 0
    #         text_welcome_btn_start = driver.find_element_by_css_selector(welcome_start_btn).text
    #         list_actual2 = [text_welcome_title, text_welcome_msg_up, text_welcome_pic_first,
    #                         text_welcome_pic_second, text_welcome_pic_third, text_welcome_msg_down,
    #                         language_box, timezone_box, text_welcome_btn_start]
    #         list_expected2 = [header_login_text, exp_welcome_msg_up, exp_internet,
    #                           exp_wireless, exp_changepw, exp_welcome_msg_down,
    #                           return_true, return_true, 'Start']
    #         check = assert_list(list_actual2, list_expected2)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 2. Check title, message up, icon Internet, Wireless, Change PW,'
    #                                'message down, language box, timezone box, Start text')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2. Check title, message up, icon Internet, Wireless, Change PW, '
    #             f'message down, language box, timezone box, Start text'
    #             f'Actual: {str(list_actual2)}. '
    #             f'Expected: {str(list_expected2)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('2. Assertion wong')
    #
    #     self.assertListEqual(list_step_fail, [])

    def test_22_Change_Password_Page_Confirmation(self):
        self.key = 'MAIN_22'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_welcome]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check Welcome page display')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Welcome page display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            text_welcome_btn_start = driver.find_element_by_css_selector(welcome_start_btn)
            text_welcome_btn_start.click()
            time.sleep(4)
            #
            text_change_pw_page_title = driver.find_element_by_css_selector(lg_welcome_header).text
            text_change_pw_msg = driver.find_element_by_css_selector(change_pw_msg).text
            text_change_pw_label = driver.find_elements_by_css_selector(welcome_change_pw_label)
            text_change_pw_label = [i.text for i in text_change_pw_label]

            text_change_pw_placeholder = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            text_change_pw_placeholder = [i.get_attribute('placeholder') for i in text_change_pw_placeholder]

            text_default_login_id = driver.find_element_by_css_selector(change_pw_default_login_id).text

            list_actual2 = [text_change_pw_page_title, text_change_pw_msg, text_default_login_id,
                            text_change_pw_label, text_change_pw_placeholder]
            list_expected2 = [exp_change_pw_title, exp_change_pw_msg, 'admin',
                              ['Login ID', 'Current Password', 'New Password', ' Retype New Password'],
                              ['Enter the current password', 'Enter the new password', 'Retype the new password.']]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Check title Change PW, message, Default Login ID, list Label, list placeholder')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check title Change PW, message , Default Login ID, list Label, list placeholder'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_23_Check_Correct_Password_operation(self):
        self.key = 'MAIN_23'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        NEW_PASSWORD = '!@#^&*()_+-={}|[]:.?'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt

        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if not check_login:
                driver.get(url_login+'/welcome')

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check pop-up welcome appear')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check pop-up welcome appear. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2,3. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            # Click to Language
            driver.find_element_by_css_selector(welcome_language).click()
            time.sleep(0.2)

            # Choose Language
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_language)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_language:
                    t.click()
                    break

            # Click to time zone
            driver.find_element_by_css_selector(welcome_time_zone).click()
            time.sleep(0.2)

            # Choose time zone in drop down: Vn zone GMT +7
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_time_zone)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_time_zone:
                    t.click()
                    break
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            # Next Change pw
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Operation Mode
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Internet Setup 1
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Internet setup 2
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Wireless Setup
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Humax Wifi App
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            check_dialog_disappear = wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)
            # check_home_displayed = driver.find_element_by_css_selector(home_view_wrap).is_displayed()

            login(driver)
            time.sleep(3)
            check_login = len(driver.find_elements_by_css_selector(home_view_wrap)) != 0
            list_actual2 = [check_login]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check title Change PW, message , Default Login ID, list Label, list placeholder')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check title Change PW, message , Default Login ID, list Label, list placeholder'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_24_Check_InCorrect_Password_operation(self):
        self.key = 'MAIN_24'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')

        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt

        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)
        WRONG_PW = 'acb000'
        NEW_PASSWORD = 'acb123'
        RETYPE_NEW_PASSWORD = 'acb321'
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if not check_login:
                driver.get(url_login+'/welcome')

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check pop-up welcome appear')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check pop-up welcome appear. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2,3. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            # Click to Language
            driver.find_element_by_css_selector(welcome_language).click()
            time.sleep(0.2)

            # Choose Language
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_language)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_language:
                    t.click()
                    break

            # Click to time zone
            driver.find_element_by_css_selector(welcome_time_zone).click()
            time.sleep(0.2)

            # Choose time zone in drop down: Vn zone GMT +7
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_time_zone)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_time_zone:
                    t.click()
                    break
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [WRONG_PW, NEW_PASSWORD, RETYPE_NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            current_pw_error_msg = driver.find_element_by_css_selector(welcome_current_pw_error_msg).text
            retype_new_pw_pw_error_msg = driver.find_elements_by_css_selector(error_message)[2].text

            list_actual2 = [current_pw_error_msg, retype_new_pw_pw_error_msg]
            list_expected2 = [exp_current_pw_error_msg, exp_retype_new_pw_error_msg]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3, 5. Check Current pw error msg and Retype new pw error message')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3, 5. Check Current pw error msg and Retype new pw error message'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3, 5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_28_Verification_of_Manual_Setup_Dynamic_IP(self):
        self.key = 'MAIN_28'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'

        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)

        GOOGLE_URL = 'http://google.com'
        YOUTUBE_URL = 'http://youtube.com'
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if not check_login:
                driver.get(url_login+'/welcome')

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check pop-up welcome appear')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check pop-up welcome appear. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2,3. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            time.sleep(3)
            # Click to Language
            driver.find_element_by_css_selector(welcome_language).click()
            time.sleep(3)

            # Choose Language
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_language)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_language:
                    t.click()
                    break
            time.sleep(3)
            # Click to time zone
            driver.find_element_by_css_selector(welcome_time_zone).click()
            time.sleep(3)

            # Choose time zone in drop down: Vn zone GMT +7
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_time_zone)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_time_zone:
                    t.click()
                    break
            time.sleep(3)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            # Next Change pw
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(5)

            check_operation_mode = driver.find_element_by_css_selector(lg_welcome_header).text
            list_actual2 = [check_operation_mode]
            list_expected2 = ['Operation Mode']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check operation mode title')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check operation mode title. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            # Next Operation Mode
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(0.5)
            time.sleep(3)
            # Check Internet setup page displayed
            check_internet_setup_title = driver.find_element_by_css_selector(lg_welcome_header).text
            check_internet_setup_guide = '\n'.join([i.text for i in driver.find_elements_by_css_selector(welcome_internet_setup1_guide)])
            # Click arrow down
            time.sleep(3)
            driver.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            ls_connection_type = driver.find_elements_by_css_selector(welcome_internet_setup1_ls_option_connection_type)
            ls_connection_type_text = [i.text for i in ls_connection_type]
            # Click Dynamic IP
            for i in ls_connection_type:
                if i.text == 'Dynamic IP':
                    i.click()
            time.sleep(1)

            list_actual3 = [check_internet_setup_title, check_internet_setup_guide, ls_connection_type_text]
            list_expected3 = ['Internet Setup', exp_internet_setup_guide, ['Dynamic IP', 'Static IP', 'PPPoE']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check internet setup title, Guidle text, list option connection type')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check internet setup title, Guidle text, list option connection type. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong')

        try:
            # Next Internet Setup 1
            time.sleep(2)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Get internet setup values
            ls_label = driver.find_elements_by_css_selector(label_name_in_2g)
            ls_label_text = [i.text for i in ls_label]
            check_manual_dns_displayed = 'Manual DNS' in driver.page_source

            # Next Internet setup 2
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Wireless Setup
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Humax Wifi App
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(3)

            list_actual4 = [ls_label_text, check_manual_dns_displayed]
            list_expected4 = [['Connection Type', 'IP Address', 'Subnet Mask', 'Getway', 'DNS Server 1', 'DNS Server 2'],
                              return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check label and Manual DNS button displayed')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check label and Manual DNS button displayed. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong')

        try:
            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)

            driver.get(YOUTUBE_URL)
            time.sleep(5)
            check_youtube = len(driver.find_elements_by_css_selector('#logo-icon-container')) != 0

            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_google = len(driver.find_elements_by_css_selector('[alt="Google"]')) != 0
            list_actual5 = [check_youtube, check_google]
            list_expected5 = [return_true]*2
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check verify Access Youtube and Google')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check verify Access Youtube and Google'
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_29_Verification_of_Manual_Setup_Static_IP(self):
        self.key = 'MAIN_29'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'

        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)

        GOOGLE_URL = 'http://google.com'
        YOUTUBE_URL = 'http://youtube.com'
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if not check_login:
                driver.get(url_login+'/welcome')

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check pop-up welcome appear')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check pop-up welcome appear. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            time.sleep(3)
            # Click to Language
            driver.find_element_by_css_selector(welcome_language).click()
            time.sleep(3)

            # Choose Language
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_language)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_language:
                    t.click()
                    break
            time.sleep(3)
            # Click to time zone
            driver.find_element_by_css_selector(welcome_time_zone).click()
            time.sleep(3)

            # Choose time zone in drop down: Vn zone GMT +7
            ls_time_zone = driver.find_elements_by_css_selector(welcome_list_time_zone)
            for t in ls_time_zone:
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_time_zone:
                    t.click()
                    break
            time.sleep(3)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            # Next Change pw
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(5)

            check_operation_mode = driver.find_element_by_css_selector(lg_welcome_header).text
            list_actual2 = [check_operation_mode]
            list_expected2 = ['Operation Mode']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check operation mode title')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check operation mode title. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            # Next Operation Mode
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(0.5)
            time.sleep(3)
            # Check Internet setup page displayed
            check_internet_setup_title = driver.find_element_by_css_selector(lg_welcome_header).text
            check_internet_setup_guide = '\n'.join([i.text for i in driver.find_elements_by_css_selector(welcome_internet_setup1_guide)])
            # Click arrow down
            time.sleep(3)
            driver.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            ls_connection_type = driver.find_elements_by_css_selector(welcome_internet_setup1_ls_option_connection_type)
            ls_connection_type_text = [i.text for i in ls_connection_type]
            # Click Static IP
            for i in ls_connection_type:
                if i.text == 'Static IP':
                    i.click()
            time.sleep(1)

            dns_2_input = driver.find_elements_by_css_selector('.wrap-form:last-child .wrap-input input')
            for i in dns_2_input:
                ActionChains(driver).move_to_element(i).click().send_keys('0').perform()
                time.sleep(0.5)


            list_actual3 = [check_internet_setup_title, check_internet_setup_guide, ls_connection_type_text]
            list_expected3 = ['Internet Setup', exp_internet_setup_guide, ['Dynamic IP', 'Static IP', 'PPPoE']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Set to Static IP; Check internet setup title, Guidle text, list option connection type')
        except:
            self.list_steps.append(
                f'[Fail] 3. Set to Static IP; Check internet setup title, Guidle text, list option connection type. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong')

        try:
            # Next Internet Setup 1
            time.sleep(2)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Wireless Setup
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()

            # Next Humax Wifi App
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(3)

            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)

            driver.get(YOUTUBE_URL)
            time.sleep(5)
            check_youtube = len(driver.find_elements_by_css_selector('#logo-icon-container')) != 0

            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_google = len(driver.find_elements_by_css_selector('[role="search"]')) != 0
            list_actual5 = [check_youtube, check_google]
            list_expected5 = [return_true]*2
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check verify Access Youtube and Google')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check verify Access Youtube and Google'
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_44_Help_Guide_Check_Help_Icon_action(self):
        self.key = 'MAIN_44'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            help_guide = driver.find_element_by_css_selector(ele_humax_help_guide)
            help_guide_tooltip = help_guide.get_attribute('title')
            # CLick
            help_guide.click()
            time.sleep(2)
            # Switch new tab
            driver.switch_to.window(self.driver.window_handles[-1])
            help_guide_link = driver.current_url

            list_actual3 = [help_guide_tooltip, help_guide_link]
            list_expected3 = ['Go to Support page', 'https://quantum.humaxdigital.com/support/']
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Check Help Guide tooltip and support URL')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check Help Guide tooltip and support URL. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_73_Verification_the_Footer_hyperlink_menu_operation(self):
        self.key = 'MAIN_73'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        # Login and CHeck About HUMAX Wifi
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            humax_about = driver.find_element_by_css_selector(ele_humax_about)
            ActionChains(driver).move_to_element(humax_about).perform()
            time.sleep(1)
            humax_about_title = humax_about.get_attribute('title')
            # Click HUmax about
            humax_about.click()
            time.sleep(2)
            # Switch new tab
            driver.switch_to.window(self.driver.window_handles[-1])
            humax_about_link = driver.current_url

            list_actual1 = [humax_about_title, humax_about_link]
            list_expected1 = ['Link to About HUMAX Wi-Fi', 'https://quantum.humaxdigital.com/']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Check Humax about tooltip; Click to this; Check current URL')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Check Humax about tooltip; Click to this; Check current URL. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~ Support
        try:
            time.sleep(3)
            driver.switch_to.window(self.driver.window_handles[0])

            humax_support = driver.find_element_by_css_selector(ele_humax_support)
            ActionChains(driver).move_to_element(humax_support).perform()
            time.sleep(1)
            humax_support_title = humax_support.get_attribute('title')
            # Click HUmax about
            humax_support.click()
            time.sleep(2)
            # Switch new tab
            driver.switch_to.window(self.driver.window_handles[-1])
            humax_support_link = driver.current_url

            list_actual2 = [humax_support_title, humax_support_link]
            list_expected2 = ['Go to Support page', 'https://quantum.humaxdigital.com/support/']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Humax Support tooltip, Check current URL')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Humax Support tooltip, Check current URL. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong')

        # Contact Us
        try:
            time.sleep(3)
            driver.switch_to.window(self.driver.window_handles[0])

            humax_contact_us = driver.find_element_by_css_selector(ele_humax_contact_us)
            ActionChains(driver).move_to_element(humax_contact_us).perform()
            time.sleep(1)
            humax_contact_us_title = humax_contact_us.get_attribute('title')
            # Click HUmax about
            humax_contact_us.click()
            time.sleep(2)
            # Switch new tab
            driver.switch_to.window(self.driver.window_handles[-1])
            humax_contact_us_link = driver.current_url

            list_actual3 = [humax_contact_us_title, humax_contact_us_link]
            list_expected3 = ['Go to Contact Us page', 'https://quantum.humaxdigital.com/contact-us/']
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check Humax Contact US tooltip, Check current URL')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Humax Contact US tooltip, Check current URL. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_74_Check_Keyword_Search_Function(self):
        self.key = 'MAIN_74'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        SEARCH_KEY = 'DHCP'

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Search key: DHCP
            search_area = driver.find_element_by_css_selector(ele_humax_search_box)
            ActionChains(driver).move_to_element(search_area).click().send_keys(SEARCH_KEY).perform()
            time.sleep(2)

            list_search_value_menu_2 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_2)
            check_search_result = [True if SEARCH_KEY in i.text else False for i in list_search_value_menu_2]

            list_actual1 = check_search_result
            list_expected1 = [return_true]*2
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Check Search key in Search result')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Check Search key in Search result. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            list_search_value_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)

            check_ = list()
            for i in list_search_value_menu_1:
                time.sleep(1)
                ActionChains(driver).move_to_element(i).click().perform()
                time.sleep(1)
                current_url = driver.current_url
                time.sleep(1)
                if i.text.lower().split()[0] in current_url:
                    check_.append(True)
                else:
                    check_.append(False)

            list_actual2 = [all(check_)]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check link search menu 1')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check link search menu 1. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_75_Verify_Hyperlink_Capabilities(self):
        self.key = 'MAIN_75'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        #
        try:
            # Click to first Menu item. Verify redirect page
            list_search_value_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            time.sleep(1)
            ActionChains(driver).move_to_element(list_search_value_menu_1[0]).click().perform()
            time.sleep(1)
            current_url = driver.current_url
            time.sleep(1)
            if list_search_value_menu_1[0].text.lower().split()[0] in current_url:
                check_ = True
            else:
                check_ = False

            list_actual2 = [check_]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click to first Menu item. Verify redirect page: {list_search_value_menu_1[0].text}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click to first Menu item. Verify redirect page: {list_search_value_menu_1[0].text}. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_76_Verify_the_Network_hyperlink(self):
        self.key = 'MAIN_76'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]


            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        #
        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'Dual WAN':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_dual_wan = detect_current_menu(driver)

            time.sleep(2)
            for i in list_items_menu_1:
                if i.text == 'Internet Setting':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_internet_setting = detect_current_menu(driver)

            list_actual2 = [detect_dual_wan, detect_internet_setting]
            list_expected2 = [('NETWORK', 'Internet')]*2
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click Dual WAN and Internet setting; Check target page')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click Dual WAN and Internet setting; Check target page. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong')

        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'LAN Setting':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_lan_setting = detect_current_menu(driver)

            time.sleep(2)
            for i in list_items_menu_1:
                if i.text == 'Reserved IP Address':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_reserved_ip_address = detect_current_menu(driver)

            list_actual3 = [detect_lan_setting, detect_reserved_ip_address]
            list_expected3 = [('NETWORK', 'LAN')]*2
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click LAN setting and Reserved IP address; Check target page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click LAN setting and Reserved IP address; Check target page '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_77_Verify_the_Security_hyperlink(self):
        self.key = 'MAIN_77'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        #
        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'Firewall':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_firewall = detect_current_menu(driver)

            list_actual2 = [detect_firewall]
            list_expected2 = [('SECURITY', 'Firewall')]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click Firewall; Check target page')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click Firewall; Check target page. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong')

        try:
            for i in list_items_menu_1:
                if i.text == 'IP/Port Filtering':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_port_filtering = detect_current_menu(driver)

            time.sleep(2)
            for i in list_items_menu_1:
                if i.text == 'MAC Filtering':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_mac_filtering = detect_current_menu(driver)

            list_actual3 = [detect_port_filtering, detect_mac_filtering]
            list_expected3 = [('SECURITY', 'Filtering')]*2
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click IP/Port Filtering and MAC Filtering; Check target page')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click IP/Port Filtering and MAC Filtering; Check target page '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong')

        #
        try:
            for i in list_items_menu_1:
                if i.text == 'Parental Control':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_parental_control = detect_current_menu(driver)

            time.sleep(2)
            for i in list_items_menu_1:
                if i.text == 'Security Check':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_security_check = detect_current_menu(driver)

            time.sleep(2)
            for i in list_items_menu_1:
                if i.text == 'VPN Server/Client':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_vpn_server = detect_current_menu(driver)

            list_actual4 = [detect_parental_control, detect_security_check, detect_vpn_server]
            list_expected4 = [('SECURITY', 'Parental Control'),
                              ('SECURITY', 'Security Self-Check'),
                              ('SECURITY', 'VPN')]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5, 6, 7. Click Parental Control, Security Check and VPN server; Check target page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5, 6, 7. Click Parental Control, Security Check and VPN server; Check target page '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5, 6, 7. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_78_Verify_the_Wireless_hyperlink(self):
        self.key = 'MAIN_78'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'Guest Network':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_guest_nw = detect_current_menu(driver)

            list_actual2 = [detect_guest_nw]
            list_expected2 = [('WIRELESS', 'Guest Network')]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click Guest Network; Check target page')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click Dual WAN and Internet setting; Check target page. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong')

        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'Primary Wireless':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_primary_wireless = detect_current_menu(driver)

            list_actual3 = [detect_primary_wireless]
            list_expected3 = [('WIRELESS', 'Primary Network')]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click Primary wireless; Check target page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click Primary wireless; Check target page '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_79_Verify_the_Home_hyperlink(self):
        self.key = 'MAIN_79'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'Home':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_primary_wireless = detect_current_menu(driver)

            list_actual3 = [detect_primary_wireless]
            list_expected3 = [('HOME', 0)]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click Home; Check target page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click Home; Check target page '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_80_Verify_the_Media_Share_hyperlink(self):
        self.key = 'MAIN_80'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text.startswith('Media Share'):
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_media_share = detect_current_menu(driver)

            list_actual3 = [detect_media_share]
            list_expected3 = [('MEDIA SHARE', 'Server Settings')]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click Media Share; Check target page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click Media Share; Check target page '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_81_Verify_the_QoS_hyperlink(self):
        self.key = 'MAIN_81'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            check_login = driver.find_elements_by_css_selector(lg_welcome_header) != 0
            if check_login:
                handle_winzard_welcome(driver)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ls_menu_text
            list_expected1 = list_menu_text_order
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            # Click to first Menu item. Verify redirect page
            list_items_menu_1 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            for i in list_items_menu_1:
                if i.text == 'QoS':
                    ActionChains(driver).move_to_element(i).click().perform()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    break
            detect_qos = detect_current_menu(driver)

            list_actual3 = [detect_qos]
            list_expected3 = [('QOS', 0)]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Click QoS; Check target page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click QoS; Check target page '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
