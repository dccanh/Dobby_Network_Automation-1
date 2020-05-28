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

os.chdir(test_t10x_path)
class MAIN(unittest.TestCase):

    def setUp(self):
        try:
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            check_enable_ethernet()
            if '_Firefox' in self._testMethodName:
                self.driver = webdriver.Firefox(executable_path=driver_firefox_path)
            elif 'Explorer' in self._testMethodName:
                self.driver = webdriver.Ie(explorer_driver_path)
            elif '_Edge' in self._testMethodName:
                self.driver = webdriver.Edge(executable_path=driver_edge_path)
            elif '_Safari' in self._testMethodName:
                self.driver = webdriver.Safari(driver_safari_path)
            else:
                self.driver = webdriver.Chrome(driver_path)
            self.driver.maximize_window()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        check_enable_ethernet()
        try:
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        except:
            # Connect by wifi if internet is down to handle exception for PPPoE
            connect_wifi_by_command('HVNWifi', 'Wifihvn12@!')
            time.sleep(1)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
            time.sleep(5)
            # Connect by LAN again
            os.system('netsh wlan disconnect')
            time.sleep(1)
        write_to_excel(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        # write_to_excel_tmp(self.key, self.list_steps, self.def_name)
        save_duration_time(test_case_key=type(self).__name__,
                           test_case_name=self.def_name,
                           test_case_steps=self.list_steps,
                           start_time=self.start_time)
        self.driver.quit()
    # OK
    def test_04_MAIN_Verify_the_Web_UI_connection_through_Gateway_IP(self):
        self.key = 'MAIN_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        detect_firmware_version(driver)
        # ~~~~~~~~~~~~~~~~~~~~~~ Get info URL, ACCOUNT ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            step_1_2_name = "1, 2. Get result by command success."
            list_check_in_step = ["Get result by command success"]

            # Get and write URL
            url_ = get_value_from_ipconfig('Ethernet adapter Ethernet', 'Default Gateway')
            save_config(config_path, 'URL', 'url', 'http://'+url_)
            url_config = get_config('URL', 'url')
            time.sleep(1)
            check_url = checkIPAddress(url_)
            # Check url, account info is not None
            list_actual1 = [check_url]
            list_expected1 = [return_true]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            list_check_in_step = [
                "Login page is appear",
                "User field is appear",
                "Password field is appear",
                "Captcha image is appear",
                "Captcha field is appear"
            ]
            step_3_name = "1,2. Check login Page displayed, id, password, captcha img, captcha input field."

            time.sleep(1)
            driver.get(url_config)
            time.sleep(3)
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
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~ Connect Wifi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            step_4_name = "4. Check Msg connect wifi successfully."
            list_check_in_step = ["Msg is connected wifi"]

            URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            time.sleep(10)
            os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            command = f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"'

            check_connect_wifi = subprocess.check_output(command)
            check_connect_wifi = check_connect_wifi.decode('ascii').strip()

            # os.system(f'python {nw_interface_path} -i Ethernet -a disable')

            list_actual3 = [check_connect_wifi]
            list_expected3 = [connect_wifi_msg]

            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check login again ~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            step_5_name = "5. Check login Page displayed, id, password, captcha img, captcha input field."
            list_check_in_step = [
                "Login page is appear",
                "User field is appear",
                "Password field is appear",
                "Captcha image is appear",
                "Captcha field is appear"
            ]

            time.sleep(1)
            driver.get(url_config)
            time.sleep(2)
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
            time.sleep(2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_05_MAIN_Verify_the_Default_setting_of_Language(self):
        self.key = 'MAIN_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url = get_config('URL', 'url')
        # ======================================================
        set_language_1 = get_config('MAIN', 'main5_set_language_1', input_data_path)
        set_language_2 = get_config('MAIN', 'main5_set_language_2', input_data_path)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:


            grand_login(driver)
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
            wait_popup_disappear(driver, icon_loading)
            check_time_out = wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            list_actual1 = [check_time_out]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            step_1_2_name = "1,2. Check Login and Restore successfully."
            list_check_in_step = [
                "Check Login and Restore success"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~ Change Language
        try:


            wait_ethernet_available()

            filename_2 = 'account2.txt'
            command_2 = 'capitest get Device.Users.User.2. leaf'
            run_cmd(command_2, filename_2)
            time.sleep(10)
            url_login = get_config('URL', 'url')
            get_result_command_from_server_api(url_login, filename_2)
            # Goto Homepage
            grand_login(driver)
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
            step_3_4_name = "3,4. Change language and check in login. "
            list_check_in_step = [
                f"Welcome message is {expected_welcome_text_en}."
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append(
                '3,4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Again
        try:


            wait_ethernet_available()
            grand_login(driver)
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
            wait_popup_disappear(driver, dialog_loading)

            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(3)
            wait_ethernet_available()
            wait_popup_disappear(driver, dialog_loading)
            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual3 = [check_login_page]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            step_5_name = "5. Check Login and Restore successfully"
            list_check_in_step = [
                "Login and Restore success"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~ Change Language and verify
        try:


            filename_2 = 'account2.txt'
            command_2 = 'capitest get Device.Users.User.2. leaf'
            run_cmd(command_2, filename_2)
            time.sleep(10)
            url_login = get_config('URL', 'url')
            # url = url_login + '/' + filename_2
            # _res = requests.get(url)
            # Get account information from web server and write to config.txt
            get_result_command_from_server_api(url_login, filename_2)
            # Goto Homepage
            time.sleep(5)
            grand_login(driver)
            time.sleep(5)

            # System > Language
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_language).click()
            time.sleep(1)
            language_selected = driver.find_element_by_css_selector(language_selected_text)
            if language_selected.text != 'Tiếng Việt':
                language_selected.click()
                language_options = driver.find_elements_by_css_selector(list_language_option)
                for o in language_options:
                    if o.text == 'Tiếng Việt':
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
            time.sleep(10)
            wait_popup_disappear(driver, dialog_loading)
            driver.get(url)
            time.sleep(3)

            welcome_text = driver.find_element_by_css_selector(lg_welcome_text).text

            list_actual6 = [welcome_text]
            list_expected6 = ['CHÀO MỪNG!']

            check = assert_list(list_actual6, list_expected6)
            step_6_7_name = "6,7. Change language and check in login."
            list_check_in_step = [
                "Login page displayed with text: CHÀO MỪNG!"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_7_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_7_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '6,7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_06_MAIN_Verify_the_Web_UI_connection_through_domain_address(self):
        self.key = 'MAIN_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        sub_url = get_config('URL', 'sub_url')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            list_check_in_step = [
                "Login page is appear",
                "User field is appear",
                "Password field is appear",
                "Captcha image is appear",
                "Captcha field is appear",
            ]
            step_1_2_name = "1,2. Check login Page displayed, id, password, captcha img, captcha input field."

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
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )

        # ~~~~~~~~~~~~~~~~~~~~~~~ Connect Wifi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            step_3_name = "3. Check Msg connect wifi successfully."
            list_check_in_step = [
                "Msg is connected wifi."
            ]

            URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wifi_default_file_path}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            command = f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"'
            check_connect_wifi = subprocess.check_output(command)
            check_connect_wifi = check_connect_wifi.decode('ascii').strip()

            list_actual3 = [check_connect_wifi]
            list_expected3 = [connect_wifi_msg]

            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Unknown error.')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check login again ~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            step_4_name = "4. Check login Page displayed again, id, password, captcha img, captcha input field"
            list_check_in_step = [
                "Login page is appear",
                "User field is appear",
                "Password field is appear",
                "Captcha image is appear",
                "Captcha field is appear",
            ]

            time.sleep(1)
            driver.get(sub_url)
            wait_popup_disappear(driver, dialog_loading)
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
            step_4_name = "4. Check login Page displayed again, id, password, captcha img, captcha input field"
            check = assert_list(list_actual4, list_expected4)
            os.system('netsh wlan disconnect')
            self.assertTrue(check["result"])

            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
    # OK
    def test_07_MAIN_Verify_the_Login_page(self):
        self.key = 'MAIN_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
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
            wait_popup_disappear(driver, dialog_loading)
            # Check Privacy Policy
            policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) > 0
            welcome_popup = len(driver.find_elements_by_css_selector(lg_welcome_header)) > 0
            home_view = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            check_tab_true = False
            if any([policy_popup, welcome_popup, home_view]):
                check_tab_true = True

            list_actual1 = [check_tab_true]
            list_expected1 = [return_true]
            list_check_in_step_1_2_3 = [
                "Login page is appear"
            ]
            step_1_2_3_name = "1,2,3. Check function TAB key in login: TAB step by step, Click login check. "
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1,2,3. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~ Change Language
        try:
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
            list_check_in_step_4 = [
                f"Wellcome message is {expected_welcome_text_en}",
                f"Placeholder of ID input box is {exp_lg_id_holder}",
                f"Placeholder of Password input box is {exp_lg_password_holder}",
                f"Placeholder of Security code is {exp_lg_captcha_holder}",
                f"Guide message is {exp_lg_extra_info}"
            ]
            step_4_name = "4. Check Login page component: Welcome, user holder, pw holder, captcha holer, extra info. . "
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_08_MAIN_Verify_the_Humax_Retail_CPE_Site_operation(self):
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
            list_check_in_step_1 = [
                "Check tooltip company image"
            ]
            step_1_name = "1. Check tooltip in Company Img. "
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            list_step_fail.append('1. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Click to image
        try:
            driver.find_element_by_css_selector(lg_company_img).click()
            time.sleep(3)
            driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(1)
            check_current_url = exp_quantum_url in driver.current_url

            list_actual2 = [check_current_url]
            list_expected2 = [return_true]
            step_2_name = "2. Check current URL."
            list_check_in_step_2 = [
             f"Current URL contain: {exp_quantum_url}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_09_MAIN_Verify_the_Login_operation(self):
        self.key = 'MAIN_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        wait_ethernet_available()
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            step_1_2_3_name = "1,2,3. Check pop-up welcome appear"
            list_check_in_step_1_2_3 = [
             f"Pop-up welcome appear"
            ]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1,2,3. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Click to image
        try:
            handle_winzard_welcome(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            check_ota_auto_update(driver)

            # wait_visible(driver, home_view_wrap)
            time.sleep(5)
            check_home_displayed = driver.find_element_by_css_selector(home_view_wrap).is_displayed()

            list_actual2 = [check_home_displayed]
            list_expected2 = [return_true]
            step_4_name = "4. Check Welcome dialog disappear, Home page display. "
            list_check_in_step_4 = [
                "Home page is appear"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_10_MAIN_Verify_the_operation_at_Login(self):
        self.key = 'MAIN_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ============================================
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
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)

            # Check Privacy Policy
            check_policy_popup_ = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) > 0

            list_actual1 = [check_policy_popup_]
            list_expected1 = [return_true]
            step_1_2_name = "1,2. Check pop-up Privacy is displayed."
            list_check_in_step_1_2 = [
                "Pop-up Privacy is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1,2. Assertion wong')

        # # ~~~~~~~~~~~~~~~~~~ Check Privacy
        # try:
        #     ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        #     time.sleep(2)
        #     # Check Privacy Policy disappear
        #     check_policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) != 0
        #     # Check Login page appear
        #     check_lg_page = driver.find_element_by_css_selector(lg_page).is_displayed()
        #
        #     list_actual2 = [check_policy_popup, check_lg_page]
        #     list_expected2 = [return_false, return_true]
        #     check = assert_list(list_actual2, list_expected2)
        #     self.assertTrue(check["result"])
        #     self.list_steps.append(
        #         '[Pass] 3. Send: ESC. Check Privacy disappear, Home page displayed. '
        #         f'Actual: {str(list_actual2)}. '
        #         f'Expected: {str(list_expected2)}')
        # except:
        #     self.list_steps.append(
        #         f'[Fail] 3. Send: ESC. Check Privacy disappear, Home page displayed. '
        #         f'Actual: {str(list_actual2)}. '
        #         f'Expected: {str(list_expected2)}')
        #     list_step_fail.append('3. Assertion wong.')

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
            step_4_name = "4. Check pop-up Privacy is displayed, Agree disabled. "
            list_check_in_step_4 = [
                "Pop-up Privacy is appear",
                "Agree button is disabled"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_5_name = "5. Send key: PAGE_UP, DOWN. Check Agree enabled. "
            list_check_in_step_5 = [
                "Agree button is enabled"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
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
            step_6_name = "6. Click Agree. Check Welcome dialog displayed. "
            list_check_in_step_6 = [
                "Welcome dialog is appear"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
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
            step_7_name = "7. Login again. Check Welcome dialog displayed. "
            list_check_in_step_7 = [
                "Login page is appear",
                "Welcome dialog is appear"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_11_MAIN_Verify_the_operation_at_Login_page_with_incorrect_id_pw(self):
        self.key = 'MAIN_11'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # Get account information from web server and write to config.txt
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # =======================================================
        WRONG_CAPTCHA = get_config('MAIN', 'main11_wrong_captcha', input_data_path)
        WRONG_USER = get_config('MAIN', 'main11_wrong_user', input_data_path)
        WRONG_PW = get_config('MAIN', 'main11_wrong_pw', input_data_path)
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
            step_1_2_name = "1,2. Check Error Wrong Captcha, Page login displayed. "
            list_check_in_step_1_2 = [
                f"Error message is displayed: {exp_wrong_captcha}",
                f"Login page is kept"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check Error wrong ID& PW."
            list_check_in_step_3 = [
                f"Error message is displayed: {exp_wrong_id_pw}",
                f"Login page is kept"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Check Error wrong ID& PW: 9 msg warning, 1 msg count time, login btn enabled after count. "
            list_check_in_step_4 = [
                f"Error message is displayed: {exp_wrong_id_pw} for 9 times: is displayed",
                "Error message for count time is appear",
                "Login page is enabled"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('4. Assertion wong')

        # ~~~~~~~~~~~~~~~~~ Incorrect ID/PW; Correct Captcha Login 2 times more
        try:
            while True:
                time.sleep(0.5)
                # Check MSG Error
                msg_error = driver.find_element_by_css_selector(lg_msg_error).text
                if msg_error == '':
                    break

            driver.get(url_login)
            time.sleep(1)
            # InCorrect ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(WRONG_USER)
            time.sleep(0.5)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(WRONG_PW)
            time.sleep(0.5)
            # Correct Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            # ==========================================
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(2)
            # Check MSG Error
            msg_error = driver.find_element_by_css_selector(lg_msg_error).text
            # ==========================================

            min = [i for i in range(0, 3)]
            sec = [i for i in range(1, 61)]
            check_error_msg_time = False
            for i in min:
                for j in sec:
                    error_format = 'Too many failed login attempts. Try again in {min} minute(s) {sec} seconds.'.format(min=str(i), sec=str(j))
                    if error_format == msg_error:
                        check_error_msg_time = True

            check_lg_btn = driver.find_element_by_css_selector(lg_btn_login).is_enabled()

            list_actual4 = [check_error_msg_time, check_lg_btn]
            list_expected4 = [check_error_msg_time, return_false]
            step_5_name = "5. Check Error wrong ID& PW: 1 msg count time, lgin btn enabled after count. "
            list_check_in_step_5 = [
                "Error message for count time is appear",
                "Login button is disabled"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('5. Assertion wong')

        # ~~~~~~~~~~~~~~~~~ Incorrect ID/PW; Correct Captcha Login 2 times more
        try:
            # Wait for 3 mins
            time.sleep(180)
            # while True:
            #     time.sleep(0.5)
            #     # Check MSG Error
            #     msg_error = driver.find_element_by_css_selector(lg_msg_error).text
            #     if msg_error == '':
            #         break

            driver.get(url_login)
            time.sleep(1)
            # InCorrect ID/PW
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(WRONG_USER)
            time.sleep(0.5)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(WRONG_PW)
            time.sleep(0.5)
            # Correct Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            # =====================================
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(2)
            # Check MSG Error
            msg_error_2 = driver.find_element_by_css_selector(lg_msg_error).text
            # Set up minute<=2, second
            min = [i for i in range(0, 5)]
            sec = [i for i in range(1, 61)]
            check_error_msg_time = False
            for i in min:
                for j in sec:
                    error_format = 'Too many failed login attempts. Try again in {min} minute(s) {sec} seconds.'.format(
                        min=str(i), sec=str(j))
                    if error_format == msg_error_2:
                        check_error_msg_time = True

            check_lg_btn = driver.find_element_by_css_selector(lg_btn_login).is_enabled()

            list_actual5 = [check_error_msg_time, check_lg_btn]
            list_expected5 = [check_error_msg_time, return_false]
            step_6_name = "6. Check Error wrong ID& PW: 1 msg count time, lgin btn enabled after count. "
            list_check_in_step_6 = [
                "Error message for count time is appear",
                "Login button is enabled"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')
        # Wait for 5 mins
        time.sleep(300)
        self.assertListEqual(list_step_fail, [])
    # OK
    def test_13_MAIN_Verify_the_Log_out_operation(self):
        self.key = 'MAIN_13'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
            time.sleep(2)

            tooltip = driver.find_element_by_css_selector(logout_btn).get_attribute('title')
            driver.find_element_by_css_selector(logout_btn).click()

            dialog_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            btn_ok_display = len(driver.find_elements_by_css_selector(btn_ok)) > 0
            check_btn_cancel = driver.find_elements_by_css_selector(btn_cancel)
            btn_cancel_display = len(check_btn_cancel) > 0
            # Click cancel
            time.sleep(0.2)
            check_btn_cancel[0].click()
            check_home_page = driver.find_element_by_css_selector(home_view_wrap).is_displayed()
            list_actual1 = [tooltip, dialog_msg, btn_ok_display, btn_cancel_display, check_home_page]
            list_expected1 = [exp_tooltip_logout, exp_logout_msg, return_true, return_true, return_true]
            check = assert_list(list_actual1, list_expected1)
            step_1_name = "1. Check logout: Check tooltip, dialog msg, btn ok, cancel and home page is displayed. "
            list_check_in_step_1 = [
                f"Logout tooltip is: {exp_tooltip_logout}",
                "Dialog msg is appear",
                "Button OK is appear",
                "Button Cancel is appear",
                "Home page is appear"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.find_element_by_css_selector(logout_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            # Click cancel
            check_login_page = driver.find_element_by_css_selector(lg_page).is_displayed()
            list_actual2 = [check_login_page]
            list_expected2 = [return_true]
            step_2_name = "2. Click Logout >Ok: Check login page is displayed."
            list_check_in_step_2 = [
                "Login page is appear"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # def test_14_MAIN_Verify_the_time_out_operation(self):
    #     self.key = 'MAIN_14'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     try:
    #         grand_login(driver)
    #         self.list_steps.append('[Pass] Login successfully')
    #     except:
    #         self.list_steps.append('[Fail] Login fail')
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         goto_menu(driver, network_tab, network_internet_tab)
    #         # Wait 20 mins
    #         sleep_time = 20 * 60
    #         time.sleep(sleep_time)
    #         time.sleep(1)
    #         goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #         msg_time_out = driver.find_elements_by_css_selector(content)
    #         if len(msg_time_out) > 0:
    #             msg_time_out_text = msg_time_out[0].text
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             time.sleep(3)
    #         else:
    #             msg_time_out_text = 'No popup appear'
    #         # Click ok
    #         # Lg is display
    #         check_lg_page = len(driver.find_elements_by_css_selector(lg_page)) > 0
    #         list_actual1 = [msg_time_out_text, check_lg_page]
    #         list_expected1 = [exp_time_out_msg, return_true]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 1. Time out: Check msg time out, Login page is displayed'
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1. Time out: Check msg time out, Login page is displayed. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         list_step_fail.append('1. Assertion wong')
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         grand_login(driver)
    #         sleep_time = 20 * 60
    #         time.sleep(sleep_time)
    #         goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
    #         # Click cancel
    #         time.sleep(2)
    #         msg_time_out_pop = len(driver.find_elements_by_css_selector(content)) == 0
    #         list_actual2 = [msg_time_out_pop]
    #         list_expected2 = [return_true]
    #         check = assert_list(list_actual2, list_expected2)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 2. Wait in Home page: After 20 mins. Check popup time out do not appear. '
    #             f'Actual: {str(list_actual2)}. '
    #             f'Expected: {str(list_expected2)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2. Wait in Home page: After 20 mins. Check popup time out do not appear.'
    #             f'Actual: {str(list_actual2)}. '
    #             f'Expected: {str(list_expected2)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('2. Assertion wong')
    #     self.assertListEqual(list_step_fail, [])

    def test_15_MAIN_Check_Explorer_Browser_behavior(self):
        self.key = 'MAIN_15'
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
            step_1_name = "1. Check URL Login Page in Internet Explorer. "
            list_check_in_step_1 = [
                "URL login page is correct"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_3_name = "2,3. Check input correct username and captcha. "
            list_check_in_step_2_3 = [
                "Input correct user",
                "Input correct captcha"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2,3. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Check Privacy Policy
            time.sleep(2)
            policy_popup = driver.find_elements_by_css_selector(lg_privacy_policy_pop)
            if len(policy_popup):
                wait_popup_disappear(driver, icon_loading)
                wait_popup_disappear(driver, icon_loading)
                time.sleep(3)
                ActionChains(driver).move_to_element(policy_popup[0]).click().send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(3)

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
            step_4_name = "4. Check Menu tree in Home page via domain address. "
            list_check_in_step_4 = [
                "There is no problem with menu"
            ]
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_5_name = "5. Check Menu tree in Home page via IP address. "
            list_check_in_step_5 = [
                "There is no problem with menu"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # OK
    def test_16_MAIN_Check_Chrome_Browser_behavior(self):
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
            step_1_name = "1. Check URL Login Page in Chrome. "
            list_check_in_step_1 = [
                "Login page URL is correct"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_3_name = "2,3. Check input correct username and captcha. "
            list_check_in_step_2_3 = [
                "Input user correct",
                "Input captcha correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Check Menu tree in Home page via domain address. "
            list_check_in_step_4 = [
                "There is no problem with menu"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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

            step_5_name = "5. Check Menu tree in Home page via IP address. "
            list_check_in_step_5 = [
                "There is no problem with menu"
            ]
            list_actual4 = [list_tab_text]
            list_expected4 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_17_MAIN_Check_Firefox_Browser_behavior(self):
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
            step_1_name = "1. Check URL Login Page in Chrome. "
            list_check_in_step_1 = [
                "Login page URL is correct"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_3_name = "2,3. Check input correct username and captcha. "
            list_check_in_step_2_3 = [
                "Input user correct",
                "Input captcha correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Check Menu tree in Home page via domain address. "
            list_check_in_step_4 = [
                "There is no problem with menu"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_5_name = "5. Check Menu tree in Home page via IP address. "
            list_check_in_step_5 = [
                "There is no problem with menu"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_18_MAIN_Check_Edge_Browser_behavior(self):
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
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)

            list_actual1 = [url_login + '/']
            list_expected1 = [driver.current_url]
            step_1_name = "1. Check URL Login Page in Chrome. "
            list_check_in_step_1 = [
                "Login page URL is correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_3_name = "2,3. Check input correct username and captcha. "
            list_check_in_step_2_3 = [
                "Input user correct",
                "Input captcha correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Check Menu tree in Home page via domain address. "
            list_check_in_step_4 = [
                "There is no problem with menu"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_5_name = "5. Check Menu tree in Home page via IP address. "
            list_check_in_step_5 = [
                "There is no problem with menu"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # def test_19_MAIN_Check_Safari_Browser_behavior(self):
    #     self.key = 'MAIN_19'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     url_login = get_config('URL', 'url')
    #     user_request = get_config('ACCOUNT', 'user')
    #     pass_word = get_config('ACCOUNT', 'password')
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         time.sleep(1)
    #         driver.get(url_login)
    #         time.sleep(2)
    #
    #         list_actual1 = [url_login + '/']
    #         list_expected1 = [driver.current_url]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 1. Check URL Login Page in Chrome. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1. Check URL Login Page in Chrome. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         list_step_fail.append('1. Assertion wong')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
    #         time.sleep(1)
    #         driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
    #         time.sleep(1)
    #         # Captcha
    #         captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
    #         captcha_text = get_captcha_string(captcha_src)
    #         driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
    #         time.sleep(1)
    #
    #         user_value = driver.find_element_by_css_selector(lg_user).get_attribute('value')
    #         captcha_value = driver.find_element_by_css_selector(lg_captcha_box).get_attribute('value')
    #         # Click Login
    #         driver.find_element_by_css_selector(lg_btn_login).click()
    #
    #         list_actual2 = [user_value, captcha_value]
    #         list_expected2 = [user_request, captcha_text]
    #         check = assert_list(list_actual2, list_expected2)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 2,3. Check input correct username and captcha. '
    #                                f'Actual: {str(list_actual2)}. '
    #                                f'Expected: {str(list_expected2)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2,3. Check input correct username and captcha. '
    #             f'Actual: {str(list_actual2)}. '
    #             f'Expected: {str(list_expected2)}')
    #         list_step_fail.append('2,3. Assertion wong')
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #         # Goto Homepage
    #         if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
    #             driver.get(url_login + homepage)
    #             time.sleep(2)
    #             wait_popup_disappear(driver, dialog_loading)
    #
    #         list_tab_text = driver.find_elements_by_css_selector(ls_tab)
    #         list_tab_text = [i.text for i in list_tab_text]
    #
    #         list_actual3 = [list_tab_text]
    #         list_expected3 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
    #         check = assert_list(list_actual3, list_expected3)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 4. Check Menu tree in Home page via domain address. '
    #                                f'Actual: {str(list_actual3)}. '
    #                                f'Expected: {str(list_expected3)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 4. Check Menu tree in Home page via domain address. '
    #             f'Actual: {str(list_actual3)}. '
    #             f'Expected: {str(list_expected3)}')
    #         list_step_fail.append('4. Assertion wong')
    #
    #     try:
    #         url_login = get_config('URL', 'url')
    #         login(driver)
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #         # Goto Homepage
    #         if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
    #             driver.get(url_login + homepage)
    #             time.sleep(2)
    #             wait_popup_disappear(driver, dialog_loading)
    #
    #         list_tab_text = driver.find_elements_by_css_selector(ls_tab)
    #         list_tab_text = [i.text for i in list_tab_text]
    #
    #         list_actual4 = [list_tab_text]
    #         list_expected4 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'QOS', 'SECURITY', 'ADVANCED']]
    #         check = assert_list(list_actual4, list_expected4)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 5. Check Menu tree in Home page via IP address. '
    #                                f'Actual: {str(list_actual4)}. '
    #                                f'Expected: {str(list_expected4)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 5. Check Menu tree in Home page via IP address. '
    #             f'Actual: {str(list_actual4)}. '
    #             f'Expected: {str(list_expected4)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('5. Assertion wong')
    #
    #     self.assertListEqual(list_step_fail, [])
    # OK
    def test_20_MAIN_Verify_the_Wizard_Main_page(self):
        self.key = 'MAIN_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================

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
            time.sleep(5)
            check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_agree_enable, check_welcome]
            list_expected1 = [return_true]*2
            step_1_name = "1. Check Agree button is enable, Click Agree, Welcome page display. "
            list_check_in_step_1 = [
                "Button agress is enabled",
                "Wellcome page is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            list_expected2 = [header_login_text, exp_welcome_msg_up,
                              exp_changepw, exp_internet, exp_wireless,
                              exp_welcome_msg_down, return_true, return_true, 'Start']
            step_2_name = "2. Check title, message up, icon Internet, Wireless, Change PW, " \
                          "message down, language box, timezone box, Start text"
            list_check_in_step_2 = [
                f"Title is: {header_login_text}",
                f"Message up is: {exp_welcome_msg_up}",
                f"Change password label is: {exp_changepw}",
                f"Internet Setup label is: {exp_internet}",
                f"Wireless Setup label is: {exp_wireless}",
                f"Message down is: {exp_welcome_msg_down}",
                "Language box is appear",
                "Timezone box is appear",
                "Text button start is: Start"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_21_MAIN_Verify_the_Language_operation_on_Wizard_page(self):
        self.key = 'MAIN_21'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if check_login:
                wait_visible(driver, welcome_language)
                time.sleep(2)

            # Get default language
            default_language_box = driver.find_element_by_css_selector(' '.join([welcome_language_wz, input]))
            default_language_text = default_language_box.get_attribute('value')
            # Click to box
            default_language_box.click()
            time.sleep(1)

            # Get list Language
            ls_text_welcome = list()
            ls_language = driver.find_elements_by_css_selector(active_drop_down_values)

            for i in ls_language:
                ActionChains(driver).move_to_element(i).click().perform()

                welcome_text = driver.find_element_by_css_selector(lg_welcome_header).text
                ls_text_welcome.append(welcome_text)
                time.sleep(0.5)
                default_language_box.click()
                time.sleep(1)
            expected_ls_welcome_language = ['Welcome to HUMAX T10X',
                                            'Willkommen bei HUMAX T10X',
                                            'ยินดีต้อนรับสู่ HUMAX T10X',
                                            'Chào mừng bạn đến với HUMAX T10X',
                                            'Bem-vindo ao HUMAX T10X',
                                            'HUMAX T10Xへようこそ',
                                            'HUMAX T10X에 오신 것을 환영합니다.',
                                            'مرحبًا بكم في HUMAX T10X',
                                            'به HUMAX T10X خوش آمدید']
            list_actual1 = [default_language_text, len(ls_language), ls_text_welcome]
            list_expected1 = ['English', 9, expected_ls_welcome_language]
            step_1_name = "1. Check Default Language, Number of Language supported, List Welcome Language. "
            list_check_in_step_1 = [
                "Default Language is: English",
                "Number of Language supported is: 9",
                f"List text wellcome is: {expected_ls_welcome_language}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_22_MAIN_Change_Password_Page_Confirmation(self):
        self.key = 'MAIN_22'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if not check_welcome:
                driver.get(URL_LOGIN + '/welcome')
                time.sleep(1)
                check_welcome = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual1 = [check_welcome]
            list_expected1 = [return_true]
            step_1_name = "1. Check Welcome page display. "
            list_check_in_step_1 = [
                "Welcome page is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_name = "2. Check title Change PW, message, Default Login ID, list Label, list placeholder. "
            list_check_in_step_2 = [
                f"Title change password page is: {text_change_pw_page_title}",
                f"Change password message is: {exp_change_pw_msg}",
                "Default login id is: admin",
                "List label is correct",
                "List placeholder is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_23_MAIN_Check_Correct_Password_operation(self):
        self.key = 'MAIN_23'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # =====================================
        NEW_PASSWORD = get_config('MAIN', 'main23_new_pw', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) > 0

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            step_1_2_3_name = "1,2,3. Check pop-up welcome appear. "
            list_check_in_step_1_2_3 = [
                "Pop-up welcome is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)
                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            check_dialog_disappear = wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            check_ota_auto_update(driver)

            login(driver)
            time.sleep(3)
            check_ota_auto_update(driver)
            time.sleep(1)
            check_login = len(driver.find_elements_by_css_selector(home_view_wrap)) != 0

            list_actual2 = [check_login]
            list_expected2 = [return_true]
            step_2_name = "2. Check title Change PW, message , Default Login ID, list Label, list placeholder. "
            list_check_in_step_2 = [
                "After change password, re-login success"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_24_MAIN_Check_InCorrect_Password_operation(self):
        self.key = 'MAIN_24'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        WRONG_PW = get_config('MAIN', 'main24_wrong_pw', input_data_path)
        NEW_PASSWORD = get_config('MAIN', 'main24_new_pw', input_data_path)
        RETYPE_NEW_PASSWORD = get_config('MAIN', 'main24_retype_new_pw', input_data_path)
        # ================================================================================

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_winzard).click()
            time.sleep(2)

            check_wizard = len(driver.find_elements_by_css_selector(ele_winzard_step_id)) > 0

            list_actual1 = [check_wizard]
            list_expected1 = [return_true]
            step_1_name = "1. Check pop-up welcome appear. "
            list_check_in_step_1 = [
                "Pop-up welcome is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            title_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual2 = [title_page]
            list_expected2 = ['Change Login Password']
            step_2_name = "2. Click Start button. Check title page displayed. "
            list_check_in_step_2 = [
                "Title page is: Change Login Password"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [WRONG_PW, NEW_PASSWORD, RETYPE_NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            retype_new_pw_pw_error_msg = driver.find_elements_by_css_selector(error_message)[2].text

            list_actual3 = [retype_new_pw_pw_error_msg]
            list_expected3 = ['Password does not match.']
            step_3_4_5_name = "3, 4, 5. Enter incorrect Current PW, valid New Password, differrent Retype New PW. "
            list_check_in_step_3_4_5 = [
                "Error message is: Password does not match."
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4, 5. Assertion wong')

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [WRONG_PW, RETYPE_NEW_PASSWORD, RETYPE_NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                p.clear()
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            current_pw_error_msg = driver.find_elements_by_css_selector(error_message)[1].text

            list_actual6 = [current_pw_error_msg]
            list_expected6 = ['Password is not correct.']
            step_6_name = "6. Enter incorrect Current PW, valid New Password, valid Retype New PW. "
            list_check_in_step_6 = [
                "Error message is: Password is not correct."
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_25_MAIN_Verify_of_Dynamic_IP_auto_detection(self):
        self.key = 'MAIN_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # =============================================
        NEW_PASSWORD = get_config('MAIN', 'main25_new_pw', input_data_path)

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            title_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [title_page]
            list_expected1 = ['Change Login Password']
            step_1_name = "1. Login. Click Start button. Check title page displayed. "
            list_check_in_step_1 = [
                "Title page is: Change Login Password"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')


        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            title_next_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual2 = [title_next_page]
            list_expected2 = ['Operation Mode']
            step_2_name = "2. Check title Operation Mode. "
            list_check_in_step_2 = [
                "Title page is: Operation Mode"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            ls_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
            for o in ls_options:
                if o.text == 'Router Mode':
                    o.click()
                    time.sleep(1)
                    break
            time.sleep(1)
            # Click next
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            title_next_page_ = driver.find_element_by_css_selector(lg_welcome_header).text

            check_internet_setup_guide = '\n'.join(
                [i.text for i in driver.find_elements_by_css_selector(welcome_internet_setup1_guide)])
            time.sleep(1)
            default_connection_type = driver.find_element_by_css_selector(ele_welcome_connection_box).text

            list_labels = ['IP Address', 'Subnet Mask', 'Gateway', 'Manual DNS', 'DNS Server 1', 'DNS Server 2']
            check_ = True
            for i in list_labels:
                if i not in driver.page_source:
                    check_ = False
                    break

            list_actual3 = [title_next_page_,check_internet_setup_guide, default_connection_type, check_]
            list_expected3 = ['Internet Setup', exp_internet_setup_guide, 'Dynamic IP', return_true]
            step_3_name = "3. Click next to Internet Setup. "
            list_check_in_step_3 = [
                "Title page is: Internet Setup",
                "Label internet setup guild is correct",
                "Default conection type is correct",
                "List label is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')
        self.assertListEqual(list_step_fail, [])
    # OK
    def test_28_MAIN_Verification_of_Manual_Setup_Dynamic_IP(self):
        self.key = 'MAIN_28'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        NEW_PASSWORD = 'abc123'

        # ===========================================================
        factory_dut()
        # ================================================================
        GOOGLE_URL = get_config('COMMON', 'google_url', input_data_path)
        YOUTUBE_URL = get_config('COMMON', 'youtube_url', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) > 0

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            step_1_name = "1. Check pop-up welcome appear. "
            list_check_in_step_1 = [
                "Pop-up welcome is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_name = "2. Check operation mode title "
            list_check_in_step_2 = [
                "Title mode is: Operation Mode"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_3_name = "3. Check internet setup title, Guidle text, list option connection type. "
            list_check_in_step_3 = [
                "Interet setup title is: Internet Setup",
                "Label internet setup guild is correct",
                "List connection title is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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

            while True:
                time.sleep(2)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)
                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            list_actual4 = [ls_label_text, check_manual_dns_displayed]
            list_expected4 = [['Connection Type', 'IP Address', 'Subnet Mask', 'Gateway', 'DNS Server 1', 'DNS Server 2'],
                              return_true]
            step_4_name = "4. Check label and Manual DNS button displayed. "
            list_check_in_step_4 = [
                "List label text is correct",
                "Manual DNS is displayed"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4. Assertion wong')

        try:
            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            wait_popup_disappear(driver, dialog_loading)
            wait_visible(driver, home_view_wrap)
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            time.sleep(5)

            driver.get(YOUTUBE_URL)
            time.sleep(5)
            check_youtube = len(driver.find_elements_by_css_selector('#logo-icon-container')) > 0

            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_google = len(driver.find_elements_by_css_selector(google_img)) > 0

            list_actual5 = [check_youtube, check_google]
            list_expected5 = [return_true]*2
            step_5_name = "5. Check verify Access Youtube and Google. "
            list_check_in_step_5 = [
                "Access youtube success",
                "Access google success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_29_MAIN_Verification_of_Manual_Setup_Static_IP(self):
        self.key = 'MAIN_29'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'

        # ===========================================================
        factory_dut()
        # ======================================================
        GOOGLE_URL = get_config('COMMON', 'google_url', input_data_path)
        YOUTUBE_URL = get_config('COMMON', 'youtube_url', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if not check_login:
                driver.get(url_login+'/welcome')

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            step_1_name = "1. Check pop-up welcome appear. "
            list_check_in_step_1 = [
                "Pop-up welcome appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_name = "2. Check operation mode title. "
            list_check_in_step_2 = [
                "Title of operation mode is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_3_name = "3. Set to Static IP; Check internet setup title, Guidle text, list option connection type."
            list_check_in_step_3 = [
                "Internet setup title is correct",
                "Guide text is correct ",
                "List connection type options is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            # Check OTA
            check_ota_auto_update(driver)

            driver.get(YOUTUBE_URL)
            time.sleep(5)
            check_youtube = len(driver.find_elements_by_css_selector('#logo-icon-container')) != 0

            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_google = len(driver.find_elements_by_css_selector('[role="search"]')) != 0
            list_actual5 = [check_youtube, check_google]
            list_expected5 = [return_true]*2
            step_4_name = "4. Check verify Access Youtube and Google. "
            list_check_in_step_4 = [
                "Access Youtube success",
                "Access Google success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_31_MAIN_Verification_of_operation_after_selecting_operation_mode(self):
        self.key = 'MAIN_31'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ====================================================
        factory_dut()
        # ======================================================
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        REPEATER_THIRD_NAME = get_config('REPEATER', 'third_party_name', input_data_path)
        REPEATER_THIRD_PW = get_config('REPEATER', 'third_party_pw', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            time.sleep(1)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            title_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [title_page]
            list_expected1 = ['Change Login Password']
            step_1_name = "1. Login. Click Start button. Check title page displayed. "
            list_check_in_step_1 = [
                "Title page is correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            title_next_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual2 = [title_next_page]
            list_expected2 = ['Operation Mode']
            step_2_name = "2. Check title Operation Mode. "
            list_check_in_step_2 = [
                "Title Operation Mode is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            list_operation_mode_text = [i.text for i in list_options]

            list_actual3 = [sorted(list_operation_mode_text)]
            list_expected3 = [sorted(['Router Mode', 'Repeater Mode', 'Access Point Mode', 'Bridge Mode'])]
            step_3_name = "3. Get list 4 operation mode supported."
            list_check_in_step_3 = [
                "List supported operation mode is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            # Choose repeater
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            # Get title
            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            # wait_popup_disappear(driver, icon_loading)
            # Chosse Third Party
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_THIRD_NAME:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_THIRD_PW).perform()
            time.sleep(1)
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            # Title
            title_wireless_setup_2 = driver.find_element_by_css_selector(lg_welcome_header).text

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_humax_wifi_app_3 = driver.find_element_by_css_selector(lg_welcome_header).text
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_summary_4 = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual4 = [[title_repeater_setting_1, title_wireless_setup_2, title_humax_wifi_app_3, title_summary_4]]
            list_expected4 = [['Repeater Setting', 'Wireless Setup', 'HUMAX Wi-Fi App', 'Summary']]
            step_4_name = "4.1 Check order of page wizard with Repeater mode Third party. "
            list_check_in_step_4 = [
                "Order of page wizard with Repeater mode Third party is correct"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4.1 Assertion wong')

        try:
            # Refresh
            driver.refresh()
            time.sleep(3)
            # Click Start
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            # Change PW
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Choose repeater
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            # Get title
            time.sleep(10)
            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            # wait_popup_disappear(driver, icon_loading)
            # Chosse Third Party
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
                    r.click()
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_MESH_PW).perform()
            time.sleep(1)
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_humax_wifi_app_2 = driver.find_element_by_css_selector(lg_welcome_header).text
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_summary_3 = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual5 = [[title_repeater_setting_1, title_humax_wifi_app_2, title_summary_3]]
            list_expected5 = [['Repeater Setting', 'HUMAX Wi-Fi App', 'Summary']]
            step_4_2_name = "4.2 Check order of page wizard with Repeater mode with Mesh mode. "
            list_check_in_step_4_2 = [
                "Order of page wizard with Repeater mode with Mesh mode is correct"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_2_name,
                    list_check_in_step=list_check_in_step_4_2,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_2_name,
                    list_check_in_step=list_check_in_step_4_2,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('4.2 Assertion wong')

        try:
            # Refresh
            driver.refresh()
            time.sleep(3)
            # Click Start
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            # Change PW
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Choose AP Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            for o in list_options:
                if o.text == 'Access Point Mode':
                    o.click()
                    break
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            # Get title
            title_wireless_setup_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_humax_wifi_app_2 = driver.find_element_by_css_selector(lg_welcome_header).text
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_summary_3 = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual6 = [[title_wireless_setup_1, title_humax_wifi_app_2, title_summary_3]]
            list_expected6 = [['Wireless Setup', 'HUMAX Wi-Fi App', 'Summary']]
            step_5_name = "5. Check order of page wizard with Access Point mode. "
            list_check_in_step_5 = [
                "Order of page wizard with Access Point mode is correct"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            # Refresh
            driver.refresh()
            time.sleep(3)
            # Click Start
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            # Change PW
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Choose AP Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            for o in list_options:
                if o.text == 'Bridge Mode':
                    o.click()
                    break
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            # Get title
            title_wireless_setup_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_humax_wifi_app_2 = driver.find_element_by_css_selector(lg_welcome_header).text
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_summary_3 = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual7 = [[title_wireless_setup_1, title_humax_wifi_app_2, title_summary_3]]
            list_expected7 = [['Wireless Setup', 'HUMAX Wi-Fi App', 'Summary']]
            step_6_name = "6.  Check order of page wizard with Bridge mode."
            list_check_in_step_6 = [
                "Order of page wizard with Bridge mode is correct"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_32_MAIN_Verification_of_setting_Repeater_Mode_via_Wizard(self):
        self.key = 'MAIN_32'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ====================================================
        # disconnect_or_connect_wan(disconnected=True)
        factory_dut()
        # ======================================================
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        REPEATER_THIRD_NAME = get_config('REPEATER', 'third_party_name', input_data_path)
        REPEATER_THIRD_PW = get_config('REPEATER', 'third_party_pw', input_data_path)
        NEW_PASSWORD_1 = get_config('MAIN', 'main_31_new_pw_1', input_data_path)
        NEW_PASSWORD_2 = get_config('MAIN', 'main_31_new_pw_2', input_data_path)
        try:
            os.system(f'netsh wlan delete profile name=*')
            time.sleep(1)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            title_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [title_page]
            list_expected1 = ['Change Login Password']
            step_1_name = "1. Login. Click Start button. Check title page displayed"
            list_check_in_step_1 = [
                "Title page is correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_1, NEW_PASSWORD_1]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            # Choose
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break

            check_router_again = driver.find_element_by_css_selector(ele_welcome_router_box)
            check_router_again_text = check_router_again.find_element_by_css_selector(input).get_attribute('value')
            list_actual2 = [check_router_again_text]
            list_expected2 = ['Repeater Mode']
            step_2_name = "2. Select Repeater mode. Check Repeater mode is selected."
            list_check_in_step_2 = [
                "Selected mode is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)

            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_MESH_PW).perform()
            time.sleep(1)

            list_actual3 = [title_repeater_setting_1]
            list_expected3 = ['Repeater Setting']
            step_3_name = "3. Check title of Repeater Settings. Choose Mesh network. Input password normally."
            list_check_in_step_3 = [
                "Repeater Setting screen is shown"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            time.sleep(1)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(3)
            title_humax_wifi_app_2 = driver.find_element_by_css_selector(lg_welcome_header).text

            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_summary_3 = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual4 = [[title_humax_wifi_app_2, title_summary_3]]
            list_expected4 = [['HUMAX Wi-Fi App', 'Summary']]
            step_4_1_name = "4.1 Check order of page wizard with Repeater mode Mesh mode. "
            list_check_in_step_4_1 = [
                "Order of page wizard with Repeater mode Mesh mode is correct"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_1_name,
                    list_check_in_step=list_check_in_step_4_1,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_1_name,
                    list_check_in_step=list_check_in_step_4_1,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4.1 Assertion wong')

        try:
            # Click Let go
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            time.sleep(150)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, lg_page)
            time.sleep(5)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_1)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(5)

            wait_ethernet_available()
            time.sleep(10)
            wait_ethernet_available()
            time.sleep(5)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            check_wan_mode = driver.find_element_by_css_selector(home_connection_description).text
            check_google = check_connect_to_google()

            list_actual5 = [check_wan_mode, check_google]
            list_expected5 = ['Repeater Mode', return_true]
            step_5_name = "5. Click Let go. Login again. Check WAN mode description. Check connect google. "
            list_check_in_step_5 = [
                "WAN mode description is correct",
                "Access to google success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            goto_system(driver, ele_sys_winzard)
            time.sleep(2)
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)
            # ===================================================
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_2, NEW_PASSWORD_2]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)
            # ===================================================
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            # Choose
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break
            # Apply
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)
            # ======================================================
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_THIRD_NAME:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_THIRD_PW).perform()
            time.sleep(1)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(3)

            # Check SSID tag
            network_name = driver.find_elements_by_css_selector('.input-wrap input[name="input-field"]')
            check_network_name_2g = network_name[0].get_attribute('value').endswith('_Ext2G')
            check_network_name_5g = network_name[1].get_attribute('value').endswith('_Ext5G')
            # =============================================================

            list_actual6 = [check_network_name_2g, check_network_name_5g]
            list_expected6 = [return_true] * 2
            step_6_name = "6. Run wizard again. Select Repeater -3 Party mode."
            list_check_in_step_6 = [
                "Network for 2g is existed",
                "Network for 5g is existed"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('6. Assertion wong')

        try:
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            time.sleep(150)
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            wait_visible(driver, lg_page)
            time.sleep(10)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(3)
            wait_ethernet_available()
            time.sleep(3)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(3)
            wait_popup_disappear(driver, dialog_loading)

            check_wan_mode_2 = driver.find_element_by_css_selector(home_connection_description).text

            time.sleep(2)
            check_google_2 = check_connect_to_google()

            list_actual7 = [check_wan_mode_2, check_google_2]
            list_expected7 = ['Repeater Mode', return_true]
            step_7_name = "7. Click Let go. Check Wan mode is Repeater Mode. Check connect to Google. "
            list_check_in_step_7 = [
                "Wan mode is correct",
                "Access to google success"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('7. Assertion wong')
        # disconnect_or_connect_wan(disconnected=False)
        self.assertListEqual(list_step_fail, [])

    # OK F
    def test_34_MAIN_Verification_of_setting_Bridge_Mode_via_Wizard(self):
        self.key = 'MAIN_34'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ====================================================
        factory_dut()
        # ======================================================
        GOOGLE_URL = get_config('COMMON', 'google_url', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            title_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [title_page]
            list_expected1 = ['Change Login Password']
            step_1_name = "1. Login. Click Start button. Check title page displayed. "
            list_check_in_step_1 = [
                "Title page is Change Login Password"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            title_next_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual2 = [title_next_page]
            list_expected2 = ['Operation Mode']
            step_2_name = "2. Check title Operation Mode."
            list_check_in_step_2 = [
                "Title Operation Mode is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            list_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
            for o in list_options:
                if o.text == 'Bridge Mode':
                    o.click()
                    break

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_next_page_2 = driver.find_element_by_css_selector(lg_welcome_header).text

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_next_page_3 = driver.find_element_by_css_selector(lg_welcome_header).text

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)

            title_next_page_4 = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual3 = [title_next_page_2, title_next_page_3, title_next_page_4]
            list_expected3 = ['Wireless Setup', 'HUMAX Wi-Fi App', 'Summary']
            step_3_4_name = "3, 4. Change Operation Mode to Bridge Mode. Check title is Wireless Mode. "
            list_check_in_step_3_4 = [
                f"Title next page times 2 is: {list_expected3[0]}",
                f"Title next page times 3 is: {list_expected3[1]}",
                f"Title next page times 4 is: {list_expected3[2]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            time.sleep(200)
            wait_visible(driver, lg_page)
            time.sleep(1)
            wait_visible(driver, lg_page)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            time.sleep(2)
            driver.get('http://dearmyextender.net')
            time.sleep(3)
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')
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
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            check_bridge_mode = driver.find_element_by_css_selector(home_connection_mode).text
            check_ip_assigned = driver.find_element_by_css_selector(home_conection_img_wan_ip).text != '0.0.0.0'

            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_google = len(driver.find_elements_by_css_selector(google_img)) > 0

            list_actual5 = [check_bridge_mode, check_ip_assigned, check_google]
            list_expected5 = ['Bridge Mode', return_true, return_true]
            step_5_6_name = "5, 6. Click Let Go. Login again. Check DUT in Bridge Mode and IP assigned (diff 0.0.0.0). "
            list_check_in_step_5_6 = [
                "Connection mode is: Bridge Mode",
                "Condition 'Assigned IP diff 0.0.0.0' is correct",
                "Access to google success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5, 6. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_35_MAIN_Wizard_Verification_of_Wireless_Setting_Page(self):
        self.key = 'MAIN_35'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===================================================================
        factory_dut()
        # ===================================================================
        NEW_PASSWORD = get_config('MAIN', 'main35_new_pw', input_data_path)

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            # System
            goto_system(driver, ele_sys_winzard)

            # Welcome pop up displayed
            wait_visible(driver, welcome_start_btn)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)

            check_change_pw_display = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [check_change_pw_display]
            list_expected1 = ['Change Login Password']
            step_1_name = "1. Check Password Setup page is displayed. "
            list_check_in_step_1 = [
                "Title page is: Password Setup"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]

            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)
                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break

            popup = driver.find_element_by_css_selector(ele_winzard_step_id)
            pop = popup.find_element_by_css_selector(ele_wizard_template)

            popup_title = pop.find_element_by_css_selector(lg_welcome_header).text
            # Check step
            check_step = "4/5" in pop.text

            #
            labels = pop.find_elements_by_css_selector(label_name_in_2g)
            values = pop.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == "Country":
                    check_country_name = v.text
                    break

            # Wireless setting
            wl_block = pop.find_elements_by_css_selector(ele_wizard_wl_block)
            # 2.4 G
            labels_24g = wl_block[0].find_elements_by_css_selector(label_name_in_2g)
            values_24g = wl_block[0].find_elements_by_css_selector(input)
            for l, v in zip(labels_24g, values_24g):
                if l.text == "Network Name(SSID)":
                    check_2g_ssid = v.get_attribute('value')
                    continue
                if l.text == "Password":
                    pw_eye_2g = wl_block[0].find_element_by_css_selector(password_eye)
                    act = ActionChains(driver)
                    act.click_and_hold(pw_eye_2g)
                    check_pw_2g_value = wl_block[0].find_element_by_css_selector(
                        input_pw).get_attribute('value')
                    act.release(pw_eye_2g)
                    act.perform()
                    break

            # 2.4 G
            labels_5g = wl_block[1].find_elements_by_css_selector(label_name_in_2g)
            values_5g = wl_block[1].find_elements_by_css_selector(input)
            for l, v in zip(labels_5g, values_5g):
                if l.text == "Network Name(SSID)":
                    check_5g_ssid = v.get_attribute('value')
                    continue
                if l.text == "Password":
                    pw_eye_5g = wl_block[1].find_element_by_css_selector(password_eye)
                    act = ActionChains(driver)
                    act.click_and_hold(pw_eye_5g)
                    check_pw_5g_value = wl_block[1].find_element_by_css_selector(
                        input_pw).get_attribute('value')
                    act.release(pw_eye_5g)
                    act.perform()
                    break
            check_box_text = wl_block[1].find_element_by_css_selector(ele_wizard_check_same_pw).text
            check_box_status = wl_block[1].find_element_by_css_selector(ele_wizard_checkbox_status).is_selected()


            wl_desc = pop.find_element_by_css_selector(ele_wireless_description).text

            check_btn_skip = driver.find_element_by_css_selector(ele_skip_btn).is_displayed()
            check_btn_back = driver.find_element_by_css_selector(ele_back_btn).is_displayed()
            check_btn_next = driver.find_element_by_css_selector(welcome_next_btn).is_displayed()

            exp_default_pw = 'humax_' + get_config('GENERAL', 'serial_number')
            exp_same_2g_pw_text = 'Same as 2.4GHz password'
            list_actual2 = [popup_title, check_step, check_2g_ssid, check_pw_2g_value,
                            check_5g_ssid, check_pw_5g_value, check_box_text, check_box_status,
                            wl_desc, check_btn_skip, check_btn_back, check_btn_next]
            list_expected2 = ['Wireless Setup', return_true, exp_ssid_2g_default_val, exp_default_pw,
                              exp_ssid_5g_default_val, exp_default_pw, exp_same_2g_pw_text, return_true,
                              exp_wizard_wl_desc, return_true, return_true, return_true]
            step_2_3_name = " 2, 3. Check Wireless Setup popup component"
            list_check_in_step_2_3 = [
                f"Popup title is: {list_expected2[0]}",
                f"Step index page 4/5 is correct",
                f"Default ssid 2g is: {list_expected2[2]}",
                f"Default password ssid 2g is: {list_expected2[3]}",
                f"Default ssid 5g is: {list_expected2[4]}",
                f"Default password ssid 5g is: {list_expected2[5]}",
                f"Label for check box 'Same as 2.4GHz password' is correct",
                "Default value check box 'Same as 2.4GHz password' is check",
                "Wizard description is correct",
                "Button skip is appear",
                "Button back is appear",
                "Button next is appear"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2, 3. Assertion wong')

        try:
            # Click Back
            driver.find_element_by_css_selector(ele_back_btn).click()
            time.sleep(1)

            title_back = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual3 = [title_back]
            list_expected3 = ['Internet Setup']
            step_4_name = "4. Click Back. Check title of Previous step."
            list_check_in_step_4 = [
                f"Title of previous step is: {list_expected3[0]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('4. Assertion wong')

        try:
            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(2)
                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break
            # Click Next
            driver.find_element_by_css_selector(welcome_next_btn).click()
            time.sleep(3)
            title_next = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual5 = [title_next]
            list_expected5 = ['HUMAX Wi-Fi App']
            step_5_name = "5. Click next. Check title of Next step. "
            list_check_in_step_5 = [
                "Title of step is correct"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            # Click Back
            driver.find_element_by_css_selector(ele_back_btn).click()
            time.sleep(1)

            # Click Skip
            driver.find_element_by_css_selector(ele_skip_btn).click()
            time.sleep(1)

            skip_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text

            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.2)
            title_skip = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual6 = [skip_confirm_msg, title_skip]
            list_expected6 = [exp_wizard_skip_confirm, 'Wireless Setup']
            step_6_name = "6. Click Skip. Check confirm message. Click Cancel. Check previous popup. "
            list_check_in_step_6 = [
                f"Skip confirm message is: {exp_wizard_skip_confirm}",
                "Title of page is correct"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('6. Assertion wong')

        try:
            # Click Skip
            driver.find_element_by_css_selector(ele_skip_btn).click()
            time.sleep(1)
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            check_login_page_display = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual7 = [check_login_page_display]
            list_expected7 = [return_true]
            step_6_2_name = "6.2 Click Skip. Click OK. Check Home Page display. "
            list_check_in_step_6_2 = [
                "Home Page is appear"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_2_name,
                    list_check_in_step=list_check_in_step_6_2,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_2_name,
                    list_check_in_step=list_check_in_step_6_2,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6.2 Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_36_MAIN_Wizard_Verify_the_default_SSID_and_check_the_wireless_operation(self):
        self.key = 'MAIN_36'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===================================================================
        NEW_PASSWORD_4 = get_config('MAIN', 'main36_password_4', input_data_path)
        NEW_PASSWORD_5_1 = get_config('MAIN', 'main36_password_5_1', input_data_path)
        NEW_PASSWORD_5_2 = get_config('MAIN', 'main36_password_5_2', input_data_path)
        NEW_PASSWORD_5_3 = get_config('MAIN', 'main36_password_5_3', input_data_path)

        WL_SSID_4 = get_config('MAIN', 'main36_ssid_wifi_4', input_data_path)
        WL_SSID_5_1 = get_config('MAIN', 'main36_ssid_wifi_5_1', input_data_path)
        if WL_SSID_5_1 != '    123   ':
            WL_SSID_5_1 = '    123   '
        WL_SSID_5_2 = 'Tiếng 한국'
        WL_SSID_5_3 = get_config('MAIN', 'main36_ssid_wifi_5_3', input_data_path)

        # Login , Goto Wizard
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            # System
            goto_system(driver, ele_sys_winzard)

            # Welcome pop up displayed
            wait_visible(driver, welcome_start_btn)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)

            check_change_pw_display = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [check_change_pw_display]
            list_expected1 = ['Change Password']
            step_1_name = "1. Check Password Setup page is displayed."
            list_check_in_step_1 = [
                f"Title of page is: {list_expected1[0]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        # Change Password
        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_4, NEW_PASSWORD_4]

            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(2)
                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break

            popup = driver.find_element_by_css_selector(ele_winzard_step_id)
            pop = popup.find_element_by_css_selector(ele_wizard_template)

            popup_title = pop.find_element_by_css_selector(lg_welcome_header).text

            list_actual2 = [popup_title]
            list_expected2 = ['Wireless Setup']
            step_2_name = "2. Goto Wireless Setup page. Check Page title. "
            list_check_in_step_2 = [
                f"Page title is: {list_expected2[0]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        # Verify Wireless Name SSID and Error message
        try:
            wl_block = pop.find_elements_by_css_selector(ele_wizard_wl_block)
            # 2.4 G
            labels_24g = wl_block[0].find_elements_by_css_selector(label_name_in_2g)
            values_24g = wl_block[0].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_24g, values_24g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        ssid_2g_holder = v.get_attribute('placeholder')
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break
            msg_error_2g = wl_block[0].find_element_by_css_selector(error_message).text

            # ===========================================================================
            labels_5g = wl_block[1].find_elements_by_css_selector(label_name_in_2g)
            values_5g = wl_block[1].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_5g, values_5g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        ssid_5g_holder = v.get_attribute('placeholder')
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break
            msg_error_5g = wl_block[1].find_element_by_css_selector(error_message).text
            # ===========================================================================

            list_actual3 = [ssid_2g_holder, ssid_5g_holder, msg_error_2g, msg_error_5g]
            list_expected3 = [exp_wizard_enter_ssid] * 2 + [exp_account_null_id] * 2
            step_3_name = "3. Check 2G and 5G place holder and error message field required. "
            list_check_in_step_3 = [
                f"SSID 2g holder is:{exp_wizard_enter_ssid}",
                f"SSID 5g holder is:{exp_wizard_enter_ssid}",
                f"Error message account field required for ssid 2g is:{exp_account_null_id}",
                f"Error message account field required for ssid 5g is:{exp_account_null_id}",
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong')

        # Change Wireless name and Let go. Check display
        try:
            nw_name = driver.find_elements_by_css_selector(ele_wl_ssid_value_field)
            nw_name[0].send_keys(WL_SSID_4)
            time.sleep(0.5)
            nw_name[1].send_keys(WL_SSID_4)
            time.sleep(0.5)
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_4)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(3)

            # Home page
            wireless_card = driver.find_element_by_css_selector(wireless_block)
            # Click 2GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[0].click()
            time.sleep(1)

            labels_2g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_2g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2g, values_2g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_2g = v.text
                    break
            # Click 5GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[1].click()
            time.sleep(1)

            labels_5g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_5g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_5g, values_5g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_5g = v.text
                    break

            # Goto Wireless > Primary
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            primary_2g = driver.find_element_by_css_selector(left)
            wl_labels_2g = primary_2g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_2g = primary_2g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_2g, wl_values_2g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_2g = v.get_attribute('value')
                    break

            primary_5g = driver.find_element_by_css_selector(right)
            wl_labels_5g = primary_5g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_5g = primary_5g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_5g, wl_values_5g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_5g = v.get_attribute('value')
                    break

            list_actual4 = [home_nw_name_2g, home_nw_name_5g, wireless_nw_name_2g, wireless_nw_name_5g]
            list_expected4 = [WL_SSID_4[:32]] * 4
            step_4_name = "4. Change Wizard SSID of 2G and 5G. Check SSID 2G and 5G in HOME and WIRELESS.. "
            list_check_in_step_4 = [
                "Home new name 2g is correct",
                "Home new name 5g is correct",
                "Wireless new name 2g is correct",
                "Wireless new name 5g is correct"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4. Assertion wong')

        try:
            goto_system(driver, ele_sys_winzard)
            # Welcome pop up displayed
            wait_visible(driver, welcome_start_btn)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_5_1, NEW_PASSWORD_5_1]

            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)
                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break

            popup = driver.find_element_by_css_selector(ele_winzard_step_id)
            pop = popup.find_element_by_css_selector(ele_wizard_template)

            wl_block = pop.find_elements_by_css_selector(ele_wizard_wl_block)
            # 2.4 G
            labels_24g = wl_block[0].find_elements_by_css_selector(label_name_in_2g)
            values_24g = wl_block[0].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_24g, values_24g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break

            # ===========================================================================
            labels_5g = wl_block[1].find_elements_by_css_selector(label_name_in_2g)
            values_5g = wl_block[1].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_5g, values_5g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break

            nw_name = driver.find_elements_by_css_selector(ele_wl_ssid_value_field)
            nw_name[0].send_keys(WL_SSID_5_1)
            time.sleep(0.5)
            nw_name[1].send_keys(WL_SSID_5_1)
            time.sleep(0.5)
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_5_1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(3)

            # Home page
            wireless_card = driver.find_element_by_css_selector(wireless_block)
            # Click 2GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[0].click()
            time.sleep(1)

            labels_2g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_2g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2g, values_2g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_2g_5_1 = v.text
                    break
            # Click 5GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[1].click()
            time.sleep(1)

            labels_5g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_5g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_5g, values_5g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_5g_5_1 = v.text
                    break

            # Goto Wireless > Primary
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            primary_2g = driver.find_element_by_css_selector(left)
            wl_labels_2g = primary_2g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_2g = primary_2g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_2g, wl_values_2g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_2g_5_1 = v.get_attribute('value')
                    break

            primary_5g = driver.find_element_by_css_selector(right)
            wl_labels_5g = primary_5g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_5g = primary_5g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_5g, wl_values_5g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_5g_5_1 = v.get_attribute('value')
                    break

            list_actual6 = [home_nw_name_2g_5_1, home_nw_name_5g_5_1, wireless_nw_name_2g_5_1, wireless_nw_name_5g_5_1]
            list_expected6 = [WL_SSID_5_1] * 4
            step_5_0_name = "5.0. Check NW ssid at HOME and WIRELESS. SSID with space at end and begin. "
            list_check_in_step_5_0 = [
                "Home new name 2g is correct",
                "Home new name 5g is correct",
                "Wireless new name 2g is correct",
                "Wireless new name 5g is correct"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_0_name,
                    list_check_in_step=list_check_in_step_5_0,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_0_name,
                    list_check_in_step=list_check_in_step_5_0,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('5.0. Assertion wong')

        # ====================================================================
        try:
            goto_system(driver, ele_sys_winzard)
            # Welcome pop up displayed
            wait_visible(driver, welcome_start_btn)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_5_2, NEW_PASSWORD_5_2]

            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)
                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break

            popup = driver.find_element_by_css_selector(ele_winzard_step_id)
            pop = popup.find_element_by_css_selector(ele_wizard_template)

            wl_block = pop.find_elements_by_css_selector(ele_wizard_wl_block)
            # 2.4 G
            labels_24g = wl_block[0].find_elements_by_css_selector(label_name_in_2g)
            values_24g = wl_block[0].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_24g, values_24g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break

            # ===========================================================================
            labels_5g = wl_block[1].find_elements_by_css_selector(label_name_in_2g)
            values_5g = wl_block[1].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_5g, values_5g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break

            nw_name = driver.find_elements_by_css_selector(ele_wl_ssid_value_field)
            nw_name[0].send_keys(WL_SSID_5_2)
            time.sleep(0.5)
            nw_name[1].send_keys(WL_SSID_5_2)
            time.sleep(0.5)
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_5_2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(3)

            # Home page
            wireless_card = driver.find_element_by_css_selector(wireless_block)
            # Click 2GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[0].click()
            time.sleep(1)

            labels_2g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_2g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2g, values_2g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_2g_5_2 = v.text
                    break
            # Click 5GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[1].click()
            time.sleep(1)

            labels_5g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_5g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_5g, values_5g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_5g_5_2 = v.text
                    break

            # Goto Wireless > Primary
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            primary_2g = driver.find_element_by_css_selector(left)
            wl_labels_2g = primary_2g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_2g = primary_2g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_2g, wl_values_2g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_2g_5_2 = v.get_attribute('value')
                    break

            primary_5g = driver.find_element_by_css_selector(right)
            wl_labels_5g = primary_5g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_5g = primary_5g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_5g, wl_values_5g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_5g_5_2 = v.get_attribute('value')
                    break

            list_actual7 = [home_nw_name_2g_5_2, home_nw_name_5g_5_2, wireless_nw_name_2g_5_2, wireless_nw_name_5g_5_2]
            list_expected7 = [WL_SSID_5_2] * 4
            step_5_2_name = "5.2. Check NW ssid at HOME and WIRELESS. SSID contain Korean and Vietnamese. "
            list_check_in_step_5_2 = [
                "Home new name 2g is correct",
                "Home new name 5g is correct",
                "Wireless new name 2g is correct",
                "Wireless new name 5g is correct"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_2_name,
                    list_check_in_step=list_check_in_step_5_2,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_2_name,
                    list_check_in_step=list_check_in_step_5_2,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('5.2. Assertion wong')

        # ====================================================================
        try:
            goto_system(driver, ele_sys_winzard)
            # Welcome pop up displayed
            wait_visible(driver, welcome_start_btn)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            time.sleep(3)
            wait_visible(driver, welcome_change_pw_fields)
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_5_3, NEW_PASSWORD_5_3]

            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)
                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break

            popup = driver.find_element_by_css_selector(ele_winzard_step_id)
            pop = popup.find_element_by_css_selector(ele_wizard_template)

            wl_block = pop.find_elements_by_css_selector(ele_wizard_wl_block)
            # 2.4 G
            labels_24g = wl_block[0].find_elements_by_css_selector(label_name_in_2g)
            values_24g = wl_block[0].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_24g, values_24g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break

            # ===========================================================================
            labels_5g = wl_block[1].find_elements_by_css_selector(label_name_in_2g)
            values_5g = wl_block[1].find_elements_by_css_selector(input)
            for i in range(2):
                for l, v in zip(labels_5g, values_5g):
                    if l.text == "Network Name(SSID)":
                        ActionChains(driver).click(v).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
                        time.sleep(1)
                        pop.find_element_by_css_selector(lg_welcome_header).click()
                        break

            nw_name = driver.find_elements_by_css_selector(ele_wl_ssid_value_field)
            nw_name[0].send_keys(WL_SSID_5_3)
            time.sleep(0.5)
            nw_name[1].send_keys(WL_SSID_5_3)
            time.sleep(0.5)
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_5_3)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(3)

            # Home page
            wireless_card = driver.find_element_by_css_selector(wireless_block)
            # Click 2GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[0].click()
            time.sleep(1)

            labels_2g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_2g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2g, values_2g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_2g_5_3 = v.text
                    break
            # Click 5GHz
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[1].click()
            time.sleep(1)

            labels_5g = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values_5g = wireless_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_5g, values_5g):
                if l.text == "Network Name(SSID)":
                    home_nw_name_5g_5_3 = v.text
                    break

            # Goto Wireless > Primary
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            primary_2g = driver.find_element_by_css_selector(left)
            wl_labels_2g = primary_2g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_2g = primary_2g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_2g, wl_values_2g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_2g_5_3 = v.get_attribute('value')
                    break

            primary_5g = driver.find_element_by_css_selector(right)
            wl_labels_5g = primary_5g.find_elements_by_css_selector(label_name_in_2g)
            wl_values_5g = primary_5g.find_elements_by_css_selector(input)
            for l, v in zip(wl_labels_5g, wl_values_5g):
                if l.text == "Network Name(SSID)":
                    wireless_nw_name_5g_5_3 = v.get_attribute('value')
                    break

            list_actual8 = [home_nw_name_2g_5_3, home_nw_name_5g_5_3, wireless_nw_name_2g_5_3,
                            wireless_nw_name_5g_5_3]
            list_expected8 = [WL_SSID_5_3[:32]] * 4
            step_5_3_name = "5.3. Check NW ssid at HOME and WIRELESS. SSID up to 32 characters. "
            list_check_in_step_5_3 = [
                "Home new name 2g is up to 32 characters",
                "Home new name 5g is up to 32 characters",
                "Wireless new name 2g is up to 32 characters",
                "Wireless new name 5g is up to 32 characters"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_3_name,
                    list_check_in_step=list_check_in_step_5_3,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_3_name,
                    list_check_in_step=list_check_in_step_5_3,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5.3. Assertion wong')

        self.assertListEqual(list_step_fail, [])


    def test_37_MAIN_Wizard_Verify_the_default_password_and_check_the_wireless_operation(self):
        self.key = 'MAIN_37'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===================================================================
        factory_dut()
        # ===================================================================
        NEW_PASSWORD = 'abc321'
        GOOGLE_URL = get_config('COMMON', 'google_url', input_data_path)
        WL_2G_PW = get_config('MAIN', 'main37_1', input_data_path)
        grand_login(driver)
        try:
            # Run wizard
            goto_system(driver, ele_sys_winzard)
            # Click Start
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            title_page = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual1 = [title_page]
            list_expected1 = ['Change Password']
            step_1_name = "1. Check Change Password page is displayed. "
            list_check_in_step_1 = [
                "Change Password page is appear with correct title"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]

            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)

            while True:
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if driver.find_element_by_css_selector(lg_welcome_header).text == 'Wireless Setup':
                    break



            block_2g = driver.find_element_by_css_selector('.card-wizard:not(.right)')
            pw_2g_value = wireless_check_pw_eye(driver, block_2g, change_pw=False)

            block_5g = driver.find_element_by_css_selector('.card-wizard.right')
            pw_5g_value = wireless_check_pw_eye(driver, block_5g, change_pw=False)

            expected_default_pw = 'humax_' + get_config('GENERAL', 'serial_number')

            list_actual2 = [pw_2g_value, pw_5g_value]
            list_expected2 = [expected_default_pw]*2
            step_2_3_name = "2->3. Goto Wireless popup. Check default password of 2G and 5G. "
            list_check_in_step_2_3 = [
                "Default password of 2G is correct",
                "Default password of 5G is correct",
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2->3. Assertion wong')

        try:
            for i in range(2):
                pw_2g_place = driver.find_element_by_css_selector(ele_wizard_wl_2g_pw)
                ActionChains(driver).move_to_element(pw_2g_place).click().send_keys(
                    Keys.CONTROL + 'A').perform()
                ActionChains(driver).move_to_element(pw_2g_place).click().send_keys(
                    Keys.DELETE).perform()
            time.sleep(2)
            pw_2g_holder = driver.find_element_by_css_selector(ele_wizard_wl_2g_pw).get_attribute('placeholder')
            msg_error_2g = block_2g.find_element_by_css_selector(' '.join([password_input_cls, error_message])).text
            # ===========================================================================
            for i in range(2):
                pw_5g_place = driver.find_element_by_css_selector(ele_wizard_wl_5g_pw)
                ActionChains(driver).move_to_element(pw_5g_place).click().send_keys(
                    Keys.CONTROL + 'A').perform()
                ActionChains(driver).move_to_element(pw_5g_place).click().send_keys(
                    Keys.DELETE).perform()
            time.sleep(2)
            pw_5g_holder = driver.find_element_by_css_selector(ele_wizard_wl_5g_pw).get_attribute('placeholder')
            msg_error_5g = block_5g.find_element_by_css_selector(' '.join([password_input_cls, error_message])).text
            # ===========================================================================

            list_actual3 = [pw_2g_holder, pw_5g_holder, msg_error_2g, msg_error_5g]
            list_expected3 = [exp_lg_password_holder] * 2 + [exp_account_null_id] * 2
            step_4_name = "4. Check 2G and 5G place holder and error message. "
            list_check_in_step_4 = [
                "Password 2g holder is correct",
                "Password 5g holder is correct",
                "Error message require password 2g is show correct",
                "Error message require password 5g is show correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('4. Assertion wong')

        try:
            driver.find_element_by_css_selector(ele_wizard_wl_2g_pw).send_keys(WL_2G_PW)
            time.sleep(1)
            copy_pw = driver.find_element_by_css_selector('[name="square-check-box-template"]').is_selected()

            list_actual5 = [copy_pw]
            list_expected5 = [return_false]
            step_5_name = "5. Input Password 2G. Check Box Same as 2.4GHz password is cleared. "
            list_check_in_step_5 = [
                "Check Box Same as 2.4GHz password is uncheck"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            # Check Same as 2.4GHz password
            driver.find_element_by_css_selector('.checkbox-sprite').click()
            time.sleep(1)
            block_5g = driver.find_element_by_css_selector('.card-wizard.right')
            pw_wireless_5g = wireless_check_pw_eye(driver, block_5g, change_pw=False)
            # Finish
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            wait_visible(driver, home_view_wrap)

            list_actual6 = [pw_wireless_5g]
            list_expected6 = [WL_2G_PW]
            step_6_name = "6. Click Same as 2.4GHz. Check current password of Wireless 5GHz. "
            list_check_in_step_6 = [
                "Current password of Wireless 5GHz is correct"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('6. Assertion wong')

        try:
            write_data_to_xml(wifi_default_file_path, new_name=exp_ssid_2g_default_val, new_pw=WL_2G_PW)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            time.sleep(2)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)
            current_wifi_2g = current_connected_wifi()
            driver.get(GOOGLE_URL)
            time.sleep(2)
            check_google_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            list_actual7 = [current_wifi_2g, check_google_2g]
            list_expected7 = [exp_ssid_2g_default_val, return_true]
            step_7_1_name = "7.1 Connect Wifi 2G. Check Access Google successfully. "
            list_check_in_step_7_1 = [
                "Connected to wifi 2G",
                "Access google success"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_1_name,
                    list_check_in_step=list_check_in_step_7_1,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_1_name,
                    list_check_in_step=list_check_in_step_7_1,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('7.1 Assertion wong')

        try:
            os.system('netsh wlan disconnect')
            time.sleep(2)
            write_data_to_xml(wifi_default_file_path, new_name=exp_ssid_5g_default_val, new_pw=WL_2G_PW)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            time.sleep(2)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)
            current_wifi_5g = current_connected_wifi()
            driver.get(GOOGLE_URL)
            time.sleep(2)
            check_google_5g = len(driver.find_elements_by_css_selector(google_img)) > 0

            list_actual8 = [current_wifi_5g, check_google_5g]
            list_expected8 = [exp_ssid_5g_default_val, return_true]
            step_7_2_name = "7.2 Connect Wifi 5G. Check Access Google successfully. "
            list_check_in_step_7_2 = [
                "Connected to wifi 5G",
                "Access google success"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_2_name,
                    list_check_in_step=list_check_in_step_7_2,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_2_name,
                    list_check_in_step=list_check_in_step_7_2,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('7.2 Assertion wong')
        self.assertListEqual(list_step_fail, [])

    # OK
    def test_39_MAIN_Wizard_Summary(self):
        self.key = 'MAIN_39'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ============================================================
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            time.sleep(3)
            list_actual1 = [check_login]
            list_expected1 = [return_true]
            step_1_name = "1. Check pop-up welcome appear. "
            list_check_in_step_1 = [
                "Pop-up welcome is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')
            # ~~~~~~~~~~~~~~~~~~ Click to image

        try:
            wait_visible(driver, welcome_start_btn)
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

            # Click Next
            detect_text = 'Internet is successfully connected as below'
            btn_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))
            while btn_let_go == 0:
                time.sleep(1)
                is_page = driver.find_elements_by_css_selector('.align-text')
                if len(is_page) > 0:
                    if is_page[0].text == detect_text:
                        ip_addr = driver.find_element_by_css_selector('.wrap-form:nth-child(2) .text-box').text
                        subnet = driver.find_element_by_css_selector('.wrap-form:nth-child(3) .text-box').text

                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)
                btn_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))

            check_summary_title = driver.find_element_by_css_selector(lg_welcome_header).text

            # ~~~~~ Internet
            internet_row = driver.find_element_by_css_selector(internet_cls)
            internet_row_title = internet_row.find_element_by_css_selector(title_cls).text

            internet_dict = {'title': internet_row_title}
            internet_table_row = internet_row.find_elements_by_css_selector(table_row)
            for r in internet_table_row:
                label = r.find_element_by_css_selector(left).text.strip()
                value = r.find_element_by_css_selector(right).text
                internet_dict.update({label: value})

            wireless_row = driver.find_elements_by_css_selector(wireless_cls)
            # ~~~~~ WL 24G
            wireless_2g_row_title = wireless_row[0].find_element_by_css_selector(title_cls).text
            wl_2g_dict = {'title': wireless_2g_row_title}
            wl_2g_table_row = wireless_row[0].find_elements_by_css_selector(table_row)
            for r in wl_2g_table_row:
                label = r.find_element_by_css_selector(left).text
                value = r.find_element_by_css_selector(right).text
                wl_2g_dict.update({label: value})

            # ~~~~~ WL 25G
            wireless_5g_row_title =  wireless_row[1].find_element_by_css_selector(title_cls).text
            wl_5g_dict = {'title': wireless_5g_row_title}
            wl_5g_table_row = wireless_row[1].find_elements_by_css_selector(table_row)
            for r in wl_5g_table_row:
                label = r.find_element_by_css_selector(left).text
                value = r.find_element_by_css_selector(right).text
                wl_5g_dict.update({label: value})

            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)

            check_home_displayed = driver.find_element_by_css_selector(home_view_wrap).is_displayed()
            #
            expected_internet_dict = {'title': 'Internet',
                                      'Operation Mode': 'Router Mode',
                                      'Connection Type': 'Dynamic IP',
                                      'IP Address': ip_addr,
                                      'Subnet Mask'.strip(): subnet}

            expected_wireless_2g = {'title': 'Wireless\n2.4GHz',
                                    'Network Name (SSID)': exp_ssid_2g_default_val,
                                    'Password': 'humax_'+get_config('GENERAL', 'serial_number')}

            expected_wireless_5g = {'title': 'Wireless\n5GHz',
                                    'Network Name (SSID)': exp_ssid_5g_default_val,
                                    'Password': 'humax_' + get_config('GENERAL', 'serial_number')}

            list_actual2 = [check_summary_title,
                            internet_dict,
                            wl_2g_dict,
                            wl_5g_dict,
                            check_home_displayed]
            list_expected2 = ['Summary',
                              expected_internet_dict,
                              expected_wireless_2g,
                              expected_wireless_5g,
                              return_true]
            step_2_name = "2. Check Summary title, block internet, 2g, 5g, Home wrap display. "
            list_check_in_step_2 = [
                f"Title page is: {list_expected2[0]}",
                "Block internet is correct",
                "Block 2g is correct",
                "Block 5g is correct",
                "Home wrap is appear"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_41_MAIN_Check_Connection_icon(self):
        self.key = 'MAIN_41'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)

            icon_connected_stt = driver.find_elements_by_css_selector(ele_system_connected_status)
            check_icon_exist = len(icon_connected_stt) > 0
            check_icon_tooltip = icon_connected_stt[0].get_attribute('title')

            list_actual2 = [check_icon_exist, check_icon_tooltip]
            list_expected2 = [return_true, 'Internet Connected']
            step_2_name = "2. Check Internet connected icon and tooltip"
            list_check_in_step_2 = [
                "WAN connection icon is appear",
                "Wan connection icon tooltip is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_42_MAIN_Wireless_24GHz_Signal_Strength_Icon_Check(self):
        self.key = 'MAIN_42'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================
        wait_ethernet_available()
        try:
            grand_login(driver)
            time.sleep(1)

            # Actions Click 2.4G
            system_2g_button = driver.find_element_by_css_selector(ele_system_2g)
            ActionChains(driver).move_to_element(system_2g_button).perform()
            time.sleep(0.2)
            system_2g_tooltip = system_2g_button.get_attribute('title')
            time.sleep(0.2)
            get_signal_power = system_2g_button.get_attribute('name').split()[-1].capitalize()

            # Click to 2.4G
            system_2g_button.click()
            time.sleep(0.5)
            dialog_exist = len(driver.find_elements_by_css_selector(dialog_content)) != 0
            dialog_title = driver.find_element_by_css_selector(ele_check_for_update_title).text

            expected_tooltip_2g = f'Wireless 2.4GHz Strength - {get_signal_power}'

            # Exit popup
            driver.find_element_by_css_selector(ele_close_button).click()
            time.sleep(2)

            list_actual2 = [system_2g_tooltip, dialog_exist, dialog_title]
            list_expected2 = [expected_tooltip_2g, return_true, 'Wireless Signal Strength']
            step_2_name = "2. Check tooltip 2.4G, Dialog signal, Dialog signal title. "
            list_check_in_step_2 = [
                "Tooltip for wireless 2.4G is correct",
                "'Wireless Signal Strength' popup is appear",
                "'Wireless Signal Strength' popup title is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            goto_menu(driver, advanced_tab, advanced_wireless_tab)
            time.sleep(2)

            # Left is 2.4 GHz
            block_2g = driver.find_element_by_css_selector(left)
            radio_row = block_2g.find_element_by_css_selector(adv_wl_radio_row)
            status_of_radio = radio_row.find_element_by_css_selector('input').get_property('checked')
            if status_of_radio:
                radio_row.find_element_by_css_selector(select).click()
                time.sleep(1)
                block_2g.find_element_by_css_selector(apply).click()
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            status_after_radio = radio_row.find_element_by_css_selector('input').get_property('checked')

            # Get current tooltip 2.4GHz
            system_2g_button = driver.find_element_by_css_selector(ele_system_2g)
            ActionChains(driver).move_to_element(system_2g_button).perform()
            time.sleep(0.2)
            current_system_2g_tooltip = system_2g_button.get_attribute('title')

            expected_tooltip_2g_off = f'Wireless 2.4GHz - Off'

            list_actual3 = [status_after_radio, current_system_2g_tooltip]
            list_expected3 = [return_false, expected_tooltip_2g_off]
            step_3_4_name = "3,4. OFF Radio of Wireless 2.4G, check tooltip is off. "
            list_check_in_step_3_4 = [
                "Wireless 2.4G is turned off",
                "Tooltip for Wireless 2.4G is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3,4. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_43_MAIN_Wireless_5GHz_Signal_Strength_Icon_Check(self):
        self.key = 'MAIN_43'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()

        try:
            grand_login(driver)
            time.sleep(1)

            # Actions Click 2.4G
            system_5g_button = driver.find_element_by_css_selector(ele_system_5g)
            ActionChains(driver).move_to_element(system_5g_button).perform()
            time.sleep(0.2)
            system_5g_tooltip = system_5g_button.get_attribute('title')
            time.sleep(0.2)
            get_signal_power = system_5g_button.get_attribute('name').split()[-1].capitalize()

            # Click to 5G
            system_5g_button.click()
            time.sleep(0.5)
            dialog_exist = len(driver.find_elements_by_css_selector(dialog_content)) != 0
            dialog_title = driver.find_element_by_css_selector(ele_check_for_update_title).text

            expected_tooltip_5g = f'Wireless 5GHz Strength - {get_signal_power}'

            # Exit popup
            driver.find_element_by_css_selector(ele_close_button).click()
            time.sleep(2)

            list_actual2 = [system_5g_tooltip, dialog_exist, dialog_title]
            list_expected2 = [expected_tooltip_5g, return_true, 'Wireless Signal Strength']
            step_2_name = "2. Check tooltip 5G, Dialog signal, Dialog signal title. "
            list_check_in_step_2 = [
                "Tooltip for wireless 5G is correct",
                "'Wireless Signal Strength' popup is appear",
                "'Wireless Signal Strength' popup title is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            goto_menu(driver, advanced_tab, advanced_wireless_tab)
            time.sleep(2)

            # Right is 5GHz
            block_5g = driver.find_element_by_css_selector(right)
            radio_row = block_5g.find_element_by_css_selector(adv_wl_radio_row)
            status_of_radio = radio_row.find_element_by_css_selector('input').get_property('checked')
            if status_of_radio:
                radio_row.find_element_by_css_selector(select).click()
                time.sleep(1)
                block_5g.find_element_by_css_selector(apply).click()
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            status_after_radio = radio_row.find_element_by_css_selector('input').get_property('checked')

            # Get current tooltip 5GHz
            system_5g_button = driver.find_element_by_css_selector(ele_system_5g)
            ActionChains(driver).move_to_element(system_5g_button).perform()
            time.sleep(0.2)
            current_system_5g_tooltip = system_5g_button.get_attribute('title')

            expected_tooltip_5g_off = f'Wireless 5GHz - Off'

            list_actual3 = [status_after_radio, current_system_5g_tooltip]
            list_expected3 = [return_false, expected_tooltip_5g_off]
            step_3_4_name = "3,4. OFF Radio of Wireless 5G, check tooltip is off. "
            list_check_in_step_3_4 = [
                "Wireless 5G is turned off",
                "Tooltip for Wireless 5G is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3,4. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_44_MAIN_Help_Guide_Check_Help_Icon_action(self):
        self.key = 'MAIN_44'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            grand_login(driver)
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
            step_2_name = "2. Check Help Guide tooltip and support URL. "
            list_check_in_step_2 = [
                "Help guide tooltip is displayed correct",
                "New browser window is open with correct URL"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_45_MAIN_System_Language_operation_check(self):
        self.key = 'MAIN_45'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        # factory_dut()

        try:
            grand_login(driver)
            time.sleep(1)

            icon_system = driver.find_element_by_css_selector(system_btn)
            check_icon_tooltip = icon_system.get_attribute('title')

            # Click
            icon_system.click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(sys_language).click()
            time.sleep(0.2)

            popup = driver.find_element_by_css_selector(ele_popup_language)
            # Verify
            popup_title = driver.find_element_by_css_selector(ele_check_for_update_title).text

            # Click Down arrow
            popup.find_element_by_css_selector(arrow_down_cls).click()
            time.sleep(0.5)
            ls_option = popup.find_elements_by_css_selector(secure_value_in_drop_down)
            num_of_language = len(ls_option)

            # Random
            # random_option = random.choice(ls_option)
            # random_option_text = random_option.text
            # random_option.click()




            mapping_language = [
                ['English', 'WELCOME!'],
                ['Deutsch', 'WILLKOMMEN!'],
                ['ไทย', 'ยินดีต้อนรับ!'],
                ['Tiếng Việt', 'CHÀO MỪNG!'],
                ['Portuguese', 'BEM-VINDA!'],
                ['日本語', 'ようこそ!'],
                ['한국어', '환영합니다!'],
                ['العربية', 'أهلاً بك!'],
                ['فارسی', 'خوش آمدید!']
            ]
            ls_value = list()
            for i in range(len(ls_option)):
                language_text = ls_option[i].text
                ls_option[i].click()
                time.sleep(1)

                actual_option_selected = driver.find_element_by_css_selector(ele_time_content).text
                ls_value.append([language_text, actual_option_selected])
                popup.find_element_by_css_selector(arrow_down_cls).click()
                time.sleep(0.5)

            # expected_language = mapping_language[random_option_text]
            # actual_option_selected = driver.find_element_by_css_selector(ele_time_content).text

            list_actual3 = [check_icon_tooltip, popup_title, num_of_language, ls_value]
            list_expected3 = ['System', 'Language', 18, mapping_language]
            step_1_2_3_name = "1, 2, 3. Check System tooltip, Popup Language title, number of options language, check output"
            list_check_in_step_1_2_3 = [
                "System tooltip is displayed correct",
                "Dropdown list show the popup of Language",
                "Total supported languages is 18",
                "Mapping language is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2, 3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # Case 48, 49, 51 chay sau cung

    def test_60_MAIN_System_Change_password(self):
        self.key = 'MAIN_60'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        NEW_PASSWORD_1 = get_config('MAIN', 'main60_1', input_data_path)
        NEW_PASSWORD_2 = get_config('MAIN', 'main60_2', input_data_path)
        try:
            grand_login(driver)
            time.sleep(1)

            # Actions Systems > Change PW
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_change_pw).click()
            time.sleep(0.2)

            # Check Change password Popup
            title_popup = driver.find_element_by_css_selector(ele_check_for_update_title).text
            sub_title_popup = driver.find_element_by_css_selector(sub_title_popup_cls).text

            ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
            # Current pw
            get_current_pw_holder = ls_pw_box[0].find_element_by_css_selector(input).get_attribute('placeholder')
            get_new_pw_holder = ls_pw_box[1].find_element_by_css_selector(input).get_attribute('placeholder')
            get_retype_new_pw_holder = ls_pw_box[2].find_element_by_css_selector(input).get_attribute('placeholder')

            get_button_text = driver.find_element_by_css_selector(apply).text

            list_actual2 = [title_popup,
                            sub_title_popup,
                            get_current_pw_holder,
                            get_new_pw_holder,
                            get_retype_new_pw_holder,
                            get_button_text]
            list_expected2 = ['Change Password',
                              'You can change the login password.',
                              'Enter the current password',
                              'Enter the new password',
                              'Retype the new password.',
                              'Apply']
            step_2_name = "2. Check Popup Change password component. "
            list_check_in_step_2 = [
                f"Title popup is: {list_expected2[0]}",
                f"Sub Title popup is: {list_expected2[1]}",
                f"Current password holder is: {list_expected2[2]}",
                f"New password holder is: {list_expected2[3]}",
                f"Retype password holder is: {list_expected2[4]}",
                f"Text in button next is: {list_expected2[5]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            def change_pw(pw):
                current_pw = get_config('ACCOUNT', 'password')
                ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
                # Current pw
                ActionChains(driver).move_to_element(ls_pw_box[0]).click().send_keys(current_pw).perform()
                time.sleep(0.2)
                # New pw
                ActionChains(driver).move_to_element(ls_pw_box[1]).click().send_keys(pw).perform()
                time.sleep(0.2)
                # Retype new pw
                ActionChains(driver).move_to_element(ls_pw_box[2]).click().send_keys(pw).perform()
                time.sleep(0.2)
                # CLick to other place
                driver.find_element_by_css_selector(apply).click()
                time.sleep(0.2)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
            change_pw(NEW_PASSWORD_1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Check popup messages
            confirm_msg_pw = driver.find_element_by_css_selector(confirm_dialog_msg).text
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_1)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            check_in_main_page = len(driver.find_elements_by_css_selector(menu_main_cls)) != 0

            list_actual3 = [confirm_msg_pw, check_in_main_page]
            list_expected3 = ['The password has been changed. Do you want to log in again?', True]
            step_3_4_5_6_name = "3->6. Input valid information, Check Confirm message, Check not logout after click Cancel."
            list_check_in_step_3_4_5_6 = [
                "Confirm message is correct",
                "After click Cancel, home page is appear"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_6_name,
                    list_check_in_step=list_check_in_step_3_4_5_6,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_6_name,
                    list_check_in_step=list_check_in_step_3_4_5_6,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3->6. Assertion wong')

        try:
            # Actions Systems > Change PW
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_change_pw).click()
            time.sleep(0.2)

            change_pw(NEW_PASSWORD_2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_2)
            # Popup confirm display
            check_popup_confirm = len(driver.find_elements_by_css_selector(confirm_dialog_cls)) != 0
            step_7_name = "7. Re-do step 2-5 Check popup confirm displayed. "
            if check_popup_confirm:
                time.sleep(0.2)
                # Click ok
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
                check_in_login_page = len(driver.find_elements_by_css_selector(lg_page)) != 0

                list_actual4 = [check_popup_confirm, check_in_login_page]
                list_expected4 = [return_true]*2
                list_check_in_step_7 = [
                    "Popup confirm is appear",
                    "Login page is appear"
                ]
            else:
                list_check_in_step_7 = [
                    "Popup confirm is appear",
                ]
                list_actual4 =[check_popup_confirm]
                list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])

            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('7. Assertion wong')

        try:
            time.sleep(2)
            # Logout
            lg_out = driver.find_elements_by_css_selector(logout_btn)
            if len(lg_out) > 0:
                time.sleep(2)
                lg_out[0].click()
                time.sleep(2)

                btn_confirm_pop = driver.find_elements_by_css_selector(btn_ok)
                if len(btn_confirm_pop) > 0:
                    btn_confirm_pop[0].click()
                time.sleep(1)

            current_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual5 = [len(btn_confirm_pop) > 0, current_page]
            list_expected5 = [return_true] * 2
            step_7_2_name = "7.2 Click Log out, check popup confirm, Check page login display. "
            list_check_in_step_7_2 = [
                "After click log out, popup confirm is appear",
                "Login page is appear"
            ]

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_2_name,
                    list_check_in_step=list_check_in_step_7_2,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_2_name,
                    list_check_in_step=list_check_in_step_7_2,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('7.2 Assertion wong')

        try:
            # Check Login with old PW
            user_request = get_config('ACCOUNT', 'user')

            driver.find_element_by_css_selector(lg_user).send_keys(user_request)
            time.sleep(1)
            driver.find_element_by_css_selector(lg_password).send_keys(NEW_PASSWORD_1)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_element_by_css_selector(lg_btn_login).click()

            check_wrongPw_error = driver.find_element_by_css_selector(lg_msg_error).text != ''

            # Check Login with new PW
            user_check = driver.find_element_by_css_selector(lg_user)
            user_check.clear()
            user_check.send_keys(user_request)

            time.sleep(1)
            pw_check = driver.find_element_by_css_selector(lg_password)
            pw_check.clear()
            pw_check.send_keys(NEW_PASSWORD_2)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            captcha_check = driver.find_element_by_css_selector(lg_captcha_box)
            captcha_check.clear()
            captcha_check.send_keys(captcha_text)
            time.sleep(1)
            driver.find_element_by_css_selector(lg_btn_login).click()

            check_truePw_error = driver.find_elements_by_css_selector(lg_msg_error)
            check_login_no_error = False
            if len(check_truePw_error) > 0:
                if check_truePw_error[0].text == '':
                    check_login_no_error = True
            else:
                check_login_no_error = True

            list_actual5 = [check_wrongPw_error, check_login_no_error]
            list_expected5 = [return_true]*2
            step_8_9_name = "8-9. Login with old PW; Login with current pw. "
            list_check_in_step_8_9 = [
                "Login with old password unsuccess",
                "Login with current password success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_9_name,
                    list_check_in_step=list_check_in_step_8_9,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_9_name,
                    list_check_in_step=list_check_in_step_8_9,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('8-9. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_61_MAIN_Check_InValid_Password_operation(self):
        self.key = 'MAIN_61'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # =======================================================
        NEW_PASSWORD = get_config('MAIN', 'main61_new_pw', input_data_path)
        NEW_PASSWORD_RETYPE = get_config('MAIN', 'main61_retype_new_pw', input_data_path)
        WRONG_PASSWORD = get_config('MAIN', 'main61_wrong_pw', input_data_path)

        try:
            grand_login(driver)
            time.sleep(1)

            # Actions Systems > Change PW
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_change_pw).click()
            time.sleep(0.2)

            ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
            # Current pw
            ActionChains(driver).move_to_element(ls_pw_box[0]).click().perform()
            time.sleep(0.2)
            # New pw
            ActionChains(driver).move_to_element(ls_pw_box[1]).click().perform()
            time.sleep(0.2)
            # CLick to other place
            driver.find_element_by_css_selector(ele_check_for_update_title).click()
            time.sleep(1)
            # Check error messages
            ls_error_msg_current_pw = ls_pw_box[0].find_element_by_css_selector(error_message).text
            ls_error_msg_new_pw = ls_pw_box[1].find_element_by_css_selector(error_message).text

            list_actual2 = [ls_error_msg_current_pw, ls_error_msg_new_pw]
            list_expected2 = [exp_account_null_id]*2
            step_1_2_name = "1, 2. Login. Let empty Current password and new password, Check Warning Message. "
            list_check_in_step_1_2 = [
                f"Error message for current password is {exp_account_null_id}",
                f"Error message for new password is {exp_account_null_id}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(1)
            ls_pw_box_2 = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))

            time.sleep(1)
            # Current pw
            ActionChains(driver).move_to_element(ls_pw_box_2[0].find_element_by_css_selector(input)).click().send_keys(WRONG_PASSWORD).perform()
            time.sleep(1)
            # New pw
            ActionChains(driver).move_to_element(ls_pw_box_2[1].find_element_by_css_selector(input)).click().send_keys(NEW_PASSWORD).perform()
            time.sleep(1)
            # Retype new pw
            ActionChains(driver).move_to_element(ls_pw_box_2[2].find_element_by_css_selector(input)).click().send_keys(NEW_PASSWORD).perform()
            time.sleep(0.2)
            # CLick to other place
            driver.find_element_by_css_selector(apply).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Check error messages
            ls_error_msg_current_pw_ = ls_pw_box_2[0].find_elements_by_css_selector(error_message)[1].text

            list_actual3 = [ls_error_msg_current_pw_]
            list_expected3 = ['Password is not correct.']
            step_3_name = "3. Let wrong Current password, Check Warning Message. "
            list_check_in_step_3 = [
                f"Error message for current password is: {list_expected3[0]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            time.sleep(2)
            ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
            # New pw
            ls_pw_box[1].find_element_by_css_selector(input).clear()
            time.sleep(0.2)
            ActionChains(driver).move_to_element(ls_pw_box[1].find_element_by_css_selector(input)).click().send_keys(NEW_PASSWORD).perform()
            time.sleep(1)
            # Retype new pw
            ls_pw_box[2].find_element_by_css_selector(input).clear()
            time.sleep(0.2)
            ActionChains(driver).move_to_element(ls_pw_box[2].find_element_by_css_selector(input)).click().send_keys(NEW_PASSWORD_RETYPE).perform()
            time.sleep(0.2)
            # CLick to other place
            driver.find_element_by_css_selector(ele_check_for_update_title).click()
            time.sleep(1)
            # Check error messages
            ls_error_msg_new_pw_retype_ = ls_pw_box[2].find_element_by_css_selector(error_message).text

            list_actual4 = [ls_error_msg_new_pw_retype_]
            list_expected4 = ['Password does not match.']
            step_4_name = "4. Let New password and retype new password different, Check Warning Message. "
            list_check_in_step_4 = [
                f"Error message for new password retype is: {ls_error_msg_new_pw_retype_}"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_62_MAIN_System_Password_Minimum_and_maximum_number_of_input(self):
        self.key = 'MAIN_62'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===================================
        NEW_PASSWORD_OVER = get_config('MAIN', 'main62_new_pw_over', input_data_path)
        NEW_PASSWORD_SHORT = get_config('MAIN', 'main62_new_pw_short', input_data_path)

        try:
            grand_login(driver)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            # Actions Systems > Change PW
            # system_button = driver.find_element_by_css_selector(system_btn)
            # ActionChains(driver).move_to_element(system_button).click().perform()
            # time.sleep(0.2)
            # driver.find_element_by_css_selector(ele_sys_change_pw).click()
            goto_system(driver, ele_sys_change_pw)
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)
            ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
            new_pw_box = ls_pw_box[1].find_element_by_css_selector(input)
            new_pw_box.clear()
            # New pw
            ActionChains(driver).move_to_element(new_pw_box).click().send_keys(NEW_PASSWORD_SHORT).perform()
            time.sleep(0.2)

            error_msg_new_pw_short = ls_pw_box[1].find_element_by_css_selector(error_message).text

            list_actual2 = [error_msg_new_pw_short]
            list_expected2 = ["That's too short."]
            step_2_name = "2. Let less than 2 letter in New password, Check Warning Message. "
            list_check_in_step_2 = [
                f"Error message for new password is: {list_expected2[0]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
            new_pw_box = ls_pw_box[1].find_element_by_css_selector(input)
            new_pw_box.clear()
            # New pw
            ActionChains(driver).move_to_element(new_pw_box).click().send_keys(NEW_PASSWORD_OVER).perform()
            time.sleep(0.2)
            new_pw_eye = ls_pw_box[1].find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(new_pw_eye)
            new_pw_value = ls_pw_box[1].find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(new_pw_eye)
            act.perform()

            list_actual3 = [new_pw_value]
            list_expected3 = [NEW_PASSWORD_OVER[:32]]
            step_3_name = "3. Let more than 2 letter in New password, Check number of letter accepted. "
            list_check_in_step_3 = [
                "Number of letter accepted is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_63_MAIN_Check_Backup_Operation(self):
        self.key = 'MAIN_63'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        url_login = get_config('URL', 'url')
        # ===========================================================
        factory_dut()

        try:
            grand_login(driver)
            time.sleep(1)

            # Actions Systems > Change PW
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_backup_restore).click()
            time.sleep(0.2)

            popup = driver.find_element_by_css_selector(dialog_content)
            # Click button Backup
            btn_active = popup.find_elements_by_css_selector(apply)

            for i in btn_active:
                if i.text == 'Back up':
                    i.click()
                    break
            time.sleep(2)
            check_popup_confirm = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()

            time.sleep(1)
            check_popup_backup = len(driver.find_elements_by_css_selector(popup_header_cls)) != 0

            list_actual2 = [check_popup_confirm, check_popup_backup]
            list_expected2 = [exp_backup_confirm_msg, return_true]
            step_2_name = "2. Goto Backup/Restore. Click Backup, Check message, click Cancel, back to previous steps. "
            list_check_in_step_2 = [
                f"Confirm message when backup is: {exp_backup_confirm_msg}",
                f"After click cancel, previous steps is appear"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            download_path = download_destination_path()
            # Remove if file exist
            backup_path = os.path.join(download_path, exp_backup_file_name)
            if os.path.exists(backup_path):
                os.remove(backup_path)
            # Click button Backup
            time.sleep(2)
            popup = driver.find_element_by_css_selector(dialog_content)
            btn_active = popup.find_elements_by_css_selector(btn_active_not_disabled)

            for i in btn_active:
                if i.text == 'Back up':
                    i.click()
                    break
            time.sleep(2)
            check_popup_confirm2 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            # Click Cancel
            driver.find_element_by_css_selector(btn_ok).click()

            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)

            check_exist_backup_file = os.path.exists(backup_path)

            list_actual3 = [check_popup_confirm2, check_exist_backup_file]
            list_expected3 = [exp_backup_confirm_msg, return_true]
            step_3_name = "3. Click Backup; Check Message confirm and download successfully. "
            list_check_in_step_3 = [
                f"Confirm message is: {exp_backup_confirm_msg}",
                "Download backup file success"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_64_MAIN_Check_Restore_Operation(self):
        self.key = 'MAIN_64'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================
        NEW_PASSWORD_2 = get_config('MAIN', 'main64_new_pw_2', input_data_path)
        SSID_2G_NEW = get_config('MAIN', 'main64_ssid_2g_new', input_data_path)
        WL_PW_2G = get_config('MAIN', 'main64_wl_pw_2g', input_data_path)
        try:
            grand_login(driver)

            # Change Settings
            # Change login password
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_change_pw).click()
            time.sleep(0.2)

            change_pw(driver, NEW_PASSWORD_2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_2)
            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(3)

            grand_login(driver)

            #  Change wireless SSID and PW of 2.4GHz
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            left_2g = driver.find_element_by_css_selector(left)
            ssid_2g = left_2g.find_element_by_css_selector('input[placeholder="Enter the network name (SSID)"]')
            ActionChains(driver).click(ssid_2g).key_down(Keys.CONTROL).send_keys('a') \
                .send_keys(Keys.DELETE).key_up(Keys.CONTROL).send_keys(SSID_2G_NEW).perform()

            pw_2g = left_2g.find_element_by_css_selector('input[placeholder="Enter the Password"]')
            ActionChains(driver).click(pw_2g).key_down(Keys.CONTROL).send_keys('a') \
                .send_keys(Keys.DELETE).key_up(Keys.CONTROL).send_keys(WL_PW_2G).perform()

            left_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            # Enable QOS
            goto_menu(driver, qos_tab, 0)
            time.sleep(1)
            select_btn = driver.find_element_by_css_selector(select)
            if not select_btn.find_element_by_css_selector(input).is_selected():
                select_btn.click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Change Firewall to Medium
            goto_menu(driver, security_tab, security_firewall_tab)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_firewall_medium).click()
            time.sleep(1)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            self.list_steps.append('[Pass] Precondition Pass')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
            list_step_fail.append('Assertion wong')

        try:
            # Actions Systems > Backup
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(ele_sys_backup_restore).click()
            time.sleep(0.5)

            download_path = download_destination_path()
            # Remove if file exist
            backup_path = os.path.join(download_path, exp_backup_file_name)
            if os.path.exists(backup_path):
                os.remove(backup_path)
            # Click button Backup
            time.sleep(2)

            popup = driver.find_element_by_css_selector(dialog_content)
            btn_active = popup.find_elements_by_css_selector(btn_active_not_disabled)

            for i in btn_active:
                if i.text == 'Back up':
                    i.click()
                    break
            time.sleep(2)
            check_popup_confirm2 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()

            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            driver.find_element_by_css_selector(btn_ok).click()

            check_exist_backup_file = os.path.exists(backup_path)

            list_actual3 = [check_popup_confirm2, check_exist_backup_file]
            list_expected3 = [exp_backup_confirm_msg, return_true]
            step_3_name = "3. Click Backup; Check Message confirm and download successfully."
            list_check_in_step_3 = [
                f"Confirm message when back up is: {exp_backup_confirm_msg}",
                "Download backup file success"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            # ===========================================================
            factory_dut()
            # ===========================================================
            time.sleep(3)
            self.list_steps.append(f'[Pass] 4. Factory DUT Successfully.')
        except:
            self.list_steps.append(f'[Fail] 4. Factory DUT Fail.')
            list_step_fail.append('4. Assertion wong')

        try:
            grand_login(driver)

            # Actions Systems > Change PW
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_backup_restore).click()
            time.sleep(0.2)

            popup = driver.find_element_by_css_selector(dialog_content)

            os.chdir(download_path)
            backup_path = os.path.join(os.getcwd(), exp_backup_file_name)
            popup.find_element_by_css_selector(ele_choose_firmware_file).send_keys(backup_path)
            time.sleep(1)

            popup = driver.find_element_by_css_selector(dialog_content)
            # Click button Restore
            btn_active = popup.find_elements_by_css_selector(apply)

            for i in btn_active:
                if i.text == 'Restore':
                    i.click()
                    break
            time.sleep(2)
            check_popup_confirm_restore1 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()

            time.sleep(1)
            check_popup_backup = len(driver.find_elements_by_css_selector(popup_header_cls)) != 0

            list_actual5 = [check_popup_confirm_restore1, check_popup_backup]
            list_expected5 = [exp_restore_confirm_msg, return_true]
            step_5_name = "5. Goto Backup/Restore, Choose file, Check message, click Cancel, back to previous steps."
            list_check_in_step_5 = [
                f"Restore confirm message is: {exp_restore_confirm_msg}",
                "After click cancel restore, previous step is appear"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            popup = driver.find_element_by_css_selector(dialog_content)
            #
            os.chdir(download_path)
            backup_path = os.path.join(os.getcwd(), exp_backup_file_name)
            popup.find_element_by_css_selector(ele_choose_firmware_file).send_keys(backup_path)
            time.sleep(1)
            os.chdir(test_t10x_path)
            popup = driver.find_element_by_css_selector(dialog_content)
            # Click button Restore
            btn_active = popup.find_elements_by_css_selector(btn_active_not_disabled)

            for i in btn_active:
                if i.text == 'Restore':
                    i.click()
                    break
            time.sleep(2)
            check_popup_confirm_restore2 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, dialog_loading)

            list_actual7 = [check_popup_confirm_restore2]
            list_expected7 = [exp_restore_confirm_msg]
            step_7_name = "7. Goto Backup/Restore, Choose file, Check message, click OK."
            list_check_in_step_7 = [
                f"Restore confirm message is: {exp_restore_confirm_msg}"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('7. Assertion wong')

        try:
            # time.sleep(120)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_2)

            # Verify
            grand_login(driver)

            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            left_2g = driver.find_element_by_css_selector(left)
            ssid_2g = left_2g.find_element_by_css_selector('input[placeholder="Enter the network name (SSID)"]')
            ssid_2g_value = ssid_2g.get_attribute('value')

            pw_eye_2g = left_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            new_pw_2g = left_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_2g)
            act.perform()
            time.sleep(1)

            goto_menu(driver, qos_tab, 0)
            time.sleep(1)
            select_btn = driver.find_element_by_css_selector(select)
            verify_qos_selected = select_btn.find_element_by_css_selector(input).is_selected()
            time.sleep(1)

            # Check Firewall to Medium
            goto_menu(driver, security_tab, security_firewall_tab)
            time.sleep(1)
            check_firewall = len(driver.find_elements_by_css_selector(ele_firewall_lv_medium)) > 0
            time.sleep(1)

            list_actual8 = [ssid_2g_value, new_pw_2g, verify_qos_selected, check_firewall]
            list_expected8 = [SSID_2G_NEW, WL_PW_2G, return_true, return_true]
            step_8_name = "8. Verify restore: New wireless 2g ssid, new pw, qos is checked, firewall level is medium. "
            list_check_in_step_8 = [
                f"New wireless 2g ssid is: {SSID_2G_NEW}",
                f"New 2G password is: {WL_PW_2G}",
                "qos is check",
                "Condition 'firewall level is medium' is correct"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('8. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_72_MAIN_System_Verify_Wizard_popup(self):
        self.key = 'MAIN_72'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =================================================
        factory_dut()
        # Login and CHeck About HUMAX Wifi
        try:
            grand_login(driver)
            time.sleep(1)
            # Actions Systems > Wizard
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_winzard).click()
            time.sleep(0.2)
            check_wizard = len(driver.find_elements_by_css_selector(ele_winzard_step_id)) != 0

            list_actual3 = [check_wizard]
            list_expected3 = [return_true]
            step_3_name = "2. Check Welcome popup display."
            list_check_in_step_3 = [
                "Welcome popup appear"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_73_MAIN_Verification_the_Footer_hyperlink_menu_operation(self):
        self.key = 'MAIN_73'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # Login and CHeck About HUMAX Wifi
        try:
            grand_login(driver)
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
            step_1_2_name = "1, 2. Login; Check Humax about tooltip; Click to this; Check current URL. "
            list_check_in_step_1_2 = [
                f"Tooltip about humax is: {list_expected1[0]}",
                f"After click about humax, new browser is open to: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check Humax Support tooltip, Check current URL. "
            list_check_in_step_3 = [
                f"Humax support page title is: {list_expected1[0]}",
                f"After click humax suport, new browser is open to: {list_expected1[1]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Check Humax Contact US tooltip, Check current URL. "
            list_check_in_step_4 = [
                f"Contact Us page title is: {list_expected1[0]}",
                f"After click Contact Us, new browser is open to: {list_expected1[1]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_74_MAIN_Check_Keyword_Search_Function(self):
        self.key = 'MAIN_74'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        SEARCH_KEY = get_config('MAIN', 'main74_search_key', input_data_path)

        try:
            grand_login(driver)
            time.sleep(1)

            # Search key: DHCP
            search_area = driver.find_element_by_css_selector(ele_humax_search_box)
            ActionChains(driver).move_to_element(search_area).click().send_keys(SEARCH_KEY).perform()
            time.sleep(2)

            list_search_value_menu_2 = driver.find_elements_by_css_selector(ele_humax_search_value_menu_2)
            check_search_result = [True if SEARCH_KEY in i.text else False for i in list_search_value_menu_2]

            list_actual1 = check_search_result
            list_expected1 = [return_true]*2
            step_1_2_name = "1, 2. Login; Check Search key in Search result. "
            list_check_in_step_1_2 = [
                "At 1st menu, Search key is appear",
                "At 2nd menu, Search key is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check link search menu 1. "
            list_check_in_step_3 = [
                f"Page redirect after click links search is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_75_MAIN_Verify_Hyperlink_Capabilities(self):
        self.key = 'MAIN_75'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = ['ADVANCED WIRELESS', 'DDNS', 'DMZ', 'DUAL WAN', 'FIREWALL', 'GUEST NETWORK',
                                    'HOME', 'INTERNET SETTING', 'IP/PORT FILTERING', 'IPTV', 'IPV6', 'LAN SETTING',
                                    'MAC FILTERING', 'MEDIA SHARE (DLNA, FTP, SAMBA)', 'NAT ALG SETTING',
                                    'OPERATION MODE', 'PARENTAL CONTROL', 'PING TEST', 'PORT FORWARDING/DMZ',
                                    'PORT TRIGGERING', 'PRIMARY WIRELESS', 'PRINTER SERVER', 'QOS',
                                    'RESERVED IP ADDRESS', 'ROUTING', 'SECURITY CHECK', 'TIME MACHINE', 'TORRENT',
                                    'UPNP', 'USB SETTINGS', 'VPN SERVER/CLIENT', 'WEBDAV', 'WOL', 'WPS']

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. "
            list_check_in_step_1_2 = [
                f"List Menu ordered A-Z is: {list_expected1[0]} "
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2. Assertion wong')

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
            step_3_name = f"3. Click to first Menu item. Verify redirect page: {list_search_value_menu_1[0].text}. "
            list_check_in_step_3 = [
                f"Condition 'redirect page: {list_search_value_menu_1[0].text}' is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_76_MAIN_Verify_the_Network_hyperlink(self):
        self.key = 'MAIN_76'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]


            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. "
            list_check_in_step_1_2 = [
                f"List Menu ordered A-Z is: {list_expected1[0]} "
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click Dual WAN and Internet setting; Check target page. "
            list_check_in_step_3 = [
                "After click Dual WAN, Target page is correct",
                "After click Internet setting, Target page is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Click LAN setting and Reserved IP address; Check target page. "
            list_check_in_step_4 = [
                "After click LAN setting, Target page is correct",
                "After click Reserved IP address, Target page is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_77_MAIN_Verify_the_Security_hyperlink(self):
        self.key = 'MAIN_77'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. "
            list_check_in_step_1_2 = [
                f"List Menu ordered A-Z is: {list_expected1[0]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click Firewall; Check target page. "
            list_check_in_step_3 = [
                f"After click firewall, Target page is correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Click IP/Port Filtering and MAC Filtering; Check target page. "
            list_check_in_step_4 = [
                "After click IP/Port Filtering, Target page is correct",
                "After click MAC Filtering, Target page is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
                              ('SECURITY', 'Security check'),
                              ('SECURITY', 'VPN')]
            step_5_6_7_name = "5, 6, 7. Click Parental Control, Security Check and VPN server; Check target page. "
            list_check_in_step_5_6_7 = [
                "After click Parental Control, Target page is correct",
                "After click Security Check, Target page is correct",
                "After click VPN server, Target page is correct"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_7_name,
                    list_check_in_step=list_check_in_step_5_6_7,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_7_name,
                    list_check_in_step=list_check_in_step_5_6_7,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5, 6, 7. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_78_MAIN_Verify_the_Wireless_hyperlink(self):
        self.key = 'MAIN_78'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)
            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()
            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. "
            list_check_in_step_1_2 = [
                f"List Menu ordered A-Z is: {list_menu_text_order}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click Guest Network; Check target page. "
            list_check_in_step_3 = [
                "Target page is: WIRELESS/Guest Network"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Click Primary wireless; Check target page. "
            list_check_in_step_4 = [
                "Taget page is: WIRELESS/Primary Network"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_79_MAIN_Verify_the_Home_hyperlink(self):
        self.key = 'MAIN_79'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. "
            list_check_in_step_1_2 = [
                f"list Menu ordered A-Z is: {list_expected1[0]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click Home; Check target page. "
            list_check_in_step_3 = [
                "Taget page is: HOME"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_80_MAIN_Verify_the_Media_Share_hyperlink(self):
        self.key = 'MAIN_80'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            grand_login(driver)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z."
            list_check_in_step_1_2 = [
                f"list Menu ordered A-Z is: {list_expected1[0]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click Media Share; Check target page."
            list_check_in_step_3 = [
                "Target page is: MEDIA SHARE/Server Settings"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_81_MAIN_Verify_the_QoS_hyperlink(self):
        self.key = 'MAIN_81'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            grand_login(driver)
            time.sleep(1)

            # Click Show
            driver.find_element_by_css_selector(ele_humax_show).click()

            # List in menu
            ls_menu = driver.find_elements_by_css_selector(ele_humax_search_value_menu_1)
            ls_menu_text = [i.text.upper() for i in ls_menu]

            list_menu_text_order = sorted(ls_menu_text)

            list_actual1 = ["/".join(ls_menu_text)]
            list_expected1 = ["/".join(list_menu_text_order)]
            step_1_2_name = "1, 2. Login; Click Show at Footer; Check list Menu ordered A-Z. "
            list_check_in_step_1_2 = [
                f"List Menu ordered A-Z is: {list_expected1[0]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click QoS; Check target page"
            list_check_in_step_3 = [
                "Target page is: QOS"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # Casse 84, 85-2 Chay sau cung

    # OK
    def test_52_MAIN_Router_mode_Check_firmware_upgrade_when_disconnected_internet(self):
        self.key = 'MAIN_52'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')

        try:
            # Call API disconnect WAN
            URL_DISCONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/disconnect'
            _METHOD = 'POST'
            _TOKEN = get_token(_USER, _PW)
            _BODY = ''
            call_api(URL_DISCONNECT_WAN, _METHOD, _BODY, _TOKEN)
            time.sleep(10)

            self.list_steps.append(
                f'[Pass] API Disconnect WAN Success. Check Status code. ')
        except:
            self.list_steps.append(
                f'[Fail] Disconnect WAN Fail. Check Status code. ')
            list_step_fail.append('0. Assertion wong')

        try:
            grand_login(driver)
            time.sleep(1)

            # System > Firmware
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)

            # Check pop up firmware update display
            check_pop_firmware_display = driver.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual1 = [check_pop_firmware_display]
            list_expected1 = ['Firmware Update']
            step_1_name = "1. Login > System > Firmware. Check name of popup displayed."
            list_check_in_step_1 = [
                f"Name of popup is: {list_expected1[0]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            message = driver.find_element_by_css_selector(ele_firm_update_msg).text

            list_actual2 = [message]
            list_expected2 = ['Internet disconnected']
            step_2_name = "2. Check Message shown in pop up firmware update. "
            list_check_in_step_2 = [
                f"Message '{list_expected2[0]}' is shown"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')

        try:
            # Call API disconnect WAN
            URL_CONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/connect'
            _METHOD = 'POST'
            _TOKEN = get_token(_USER, _PW)
            _BODY = ''
            call_api(URL_CONNECT_WAN, _METHOD, _BODY, _TOKEN)
            time.sleep(10)

            self.list_steps.append(
                f'[Pass] API Connect WAN Success After test. Check Status code. ')
        except:
            self.list_steps.append(
                f'[Fail] Connect WAN Fail After test. Check Status code. ')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_27_MAIN_Verification_of_Internet_Setup_page(self):
        self.key = 'MAIN_27'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        URL_CONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/connect'
        _METHOD = 'POST'
        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')
        _TOKEN = get_token(_USER, _PW)
        _BODY = ''
        call_api(URL_CONNECT_WAN, _METHOD, _BODY, _TOKEN)
        # ===========================================================
        factory_dut()
        # ===========================================================

        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)

        try:
            time.sleep(1)
            login(driver)
            time.sleep(1)

            URL_DISCONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/disconnect'
            _METHOD = 'POST'
            _TOKEN = get_token(_USER, _PW)
            _BODY = ''
            call_api(URL_DISCONNECT_WAN, _METHOD, _BODY, _TOKEN)
            time.sleep(10)

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

            # Mode
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(5)
            internet_setup_title = driver.find_element_by_css_selector(ele_internet_setup_title).text
            internet_setup_error = driver.find_element_by_css_selector(ele_internet_setup_error_msg).text
            default_connection_type = driver.find_element_by_css_selector(ele_welcome_connection_box).text
            # check_btn_skip = driver.find_element_by_css_selector(ele_skip_btn).is_displayed()
            check_btn_back = driver.find_element_by_css_selector(ele_back_btn).is_displayed()
            check_btn_next = driver.find_element_by_css_selector(welcome_next_btn).is_displayed()

            list_actual1 = [internet_setup_title,
                            internet_setup_error,
                            default_connection_type,
                            check_btn_back,
                            check_btn_next]
            list_expected1 = ['Internet Setup',
                              exp_internet_setup_error_msg,
                              'Dynamic IP'] + [return_true]*2
            step_1_2_3_4_name = "1 -> 4. Wizard > Internet setting: Check title, error message, Default connect type, btn Skip, Back, Next displayed."
            list_check_in_step_1_2_3_4 = [
                f"Title page is: {list_expected1[0]}",
                f"Internet setup error message is: {list_expected1[1]}",
                f"Default connect type is: {list_expected1[3]}",
                "Button back is appear",
                "Button next is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_4_name,
                    list_check_in_step=list_check_in_step_1_2_3_4,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_4_name,
                    list_check_in_step=list_check_in_step_1_2_3_4,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            time.sleep(3)
            driver.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            ls_connection_type = driver.find_elements_by_css_selector(welcome_internet_setup1_ls_option_connection_type)

            # Click Static IP
            for i in ls_connection_type:
                if i.text == 'Static IP':
                    i.click()
                    break
            time.sleep(1)

            ls_label_static_ip = [i.text for i in driver.find_elements_by_css_selector(label_name_in_2g)]

            list_actual2 = ["/".join(ls_label_static_ip)]
            list_expected2 = ["/".join(['Connection Type',
                              'WAN IP Address',
                              'Subnet Mask',
                              'Gateway',
                              'DNS Server 1',
                              'DNS Server 2'])]
            step_5_name = "5. Check Internet Setup Label of Static IP"
            list_check_in_step_5 = [
                "The sub-items are output corresponding the connection type"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            time.sleep(3)
            driver.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            ls_connection_type = driver.find_elements_by_css_selector(welcome_internet_setup1_ls_option_connection_type)

            # Click PPPoE
            for i in ls_connection_type:
                if i.text == 'PPPoE':
                    i.click()
                    break
            time.sleep(1)

            ls_label_pppoe = [i.text for i in driver.find_elements_by_css_selector(label_name_in_2g)]

            list_actual3 = ["/".join(ls_label_pppoe)]
            list_expected3 = ["/".join(['Connection Type',
                              'User Name',
                              'Password',
                              'Dynamic IP'])]
            step_6_name = "6. Check Internet Setup Label of PPPoE. "
            list_check_in_step_6 = [
                "The sub-items are output corresponding the connection type"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('6. Assertion wong')

        try:
            driver.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            ls_connection_type = driver.find_elements_by_css_selector(welcome_internet_setup1_ls_option_connection_type)

            # Click PPPoE
            for i in ls_connection_type:
                if i.text == 'Dynamic IP':
                    i.click()
                    break
            time.sleep(1)
            while True:
                time.sleep(2)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)

            # Call API disconnect WAN
            URL_CONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/connect'
            _METHOD = 'POST'
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            _BODY = ''
            call_api(URL_CONNECT_WAN, _METHOD, _BODY, _TOKEN)
            time.sleep(10)

            self.list_steps.append(
                f'[Pass] API Connect WAN Success After test. Check Status code. ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] Connect WAN Fail After test. Check Status code. ')
            self.list_steps.append('[END TC]')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_69_MAIN_System_Verify_the_Date_Time_operation(self):
        self.key = 'MAIN_69'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        exp_time_zone = get_config('MAIN', 'main69_exp_time_zone', input_data_path)
        try:
            grand_login(driver)
            time.sleep(1)

            # Actions Systems > Change PW
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(ele_sys_date_time).click()
            time.sleep(1)

            check_popup_title = driver.find_element_by_css_selector(ele_check_for_update_title).text
            check_popup_sub_title = driver.find_element_by_css_selector(sub_title_popup_cls).text

            time_large = driver.find_element_by_css_selector(ele_time_content).text
            try:
                datetime.strptime(time_large, '%Y.%m.%d %H:%M:%S')
                check_format_time = True
            except ValueError:
                check_format_time = False

            date_time = driver.find_element_by_css_selector(ele_timezone_cls)
            check_date_time_label = date_time.find_element_by_css_selector(label_name_in_2g).text

            daylight_st = driver.find_element_by_css_selector(ele_dst_cls)
            check_daylight_st_label = daylight_st.find_element_by_css_selector(label_name_in_2g).text

            ntp = driver.find_element_by_css_selector(ele_ntp_cls)
            check_ntp_label = ntp.find_element_by_css_selector(label_name_in_2g).text
            time.sleep(3)
            ntp_server = driver.find_element_by_css_selector(ele_npt_server_cls)
            check_ntp_server_label = [i.text for i in ntp_server.find_elements_by_css_selector(ele_index_cls)]
            check_ntp_server_desc = [i.text for i in ntp_server.find_elements_by_css_selector(description)]

            check_ntp_server_edit = len(ntp_server.find_elements_by_css_selector(edit_cls))
            check_ntp_server_delete = len(ntp_server.find_elements_by_css_selector(delete_cls))

            btn_add_text = ntp_server.find_element_by_css_selector(add_class).text
            check_add_button = '+ ADD' in btn_add_text

            list_actual2 = [check_popup_title, check_popup_sub_title, check_format_time,
                            check_date_time_label, check_daylight_st_label, check_ntp_label,
                            check_ntp_server_label, check_ntp_server_desc,
                            check_ntp_server_edit, check_ntp_server_delete, check_add_button]
            list_expected2 = ['Date/Time', 'You can set the date and time.', return_true,
                              'Time Zone', 'Daylight Saving Time', 'NTP (Network Time Protocol)',
                              ['NTP Server 1', 'NTP Server 2', 'NTP Server 3'],
                              ['0.pool.ntp.org', '1.pool.ntp.org', '2.pool.ntp.org'],
                              3, 3, return_true]
            step_3_name = "3. Check info popup: Title, Sub title, Format time, label timezone, dst, " \
                          "ntp, 3 servers, 3 desc, 3 icon edit, 3 icon delete, icon +ADD displayed. "
            list_check_in_step_3 = [
                f"Popup Title is: {list_expected2[0]}",
                f"Sub title is: {list_expected2[1]}",
                "Format time is correct",
                f"Label timezone is: {list_expected2[3]}",
                f"Label daylight is: {list_expected2[4]}",
                f"Label ntp is: {list_expected2[5]}",
                f"Label ntp server is: {list_expected2[6]}",
                f"Label ntp server desc is: {list_expected2[7]}",
                f"ntp server edit is: {list_expected2[8]}",
                f"ntp server delete is: {list_expected2[9]}",
                "icon Add is appear"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            time.sleep(1)
            # Click to time zone
            date_time.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            # Choose time zone in drop down
            ls_time_zone = date_time.find_elements_by_css_selector(secure_value_in_drop_down)
            stt = 0
            for index, t in enumerate(ls_time_zone):
                ActionChains(driver).move_to_element(t).perform()
                if t.text == exp_time_zone:
                    t.click()
                    break

            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            URL_DATETIME = URL_LOGIN + '/api/v1/gateway/datetime'
            _METHOD = 'GET'
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            _BODY = ''
            res_datetime = call_api(URL_DATETIME, _METHOD, _BODY, _TOKEN)
            check_time_zone = res_datetime['timeZone']

            list_actual4 = [check_time_zone]
            list_expected4 = [index]
            step_4_name = "4. Check TimeZone index with API. "
            list_check_in_step_4 = [
                "Time Zone setting will be applied and current date time is changed as response API"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    # =======================================================REPEATER MODE=============================================
    def test_R_55_MAIN_System_Extender_mode_Check_Manual_Firmware_Update_operation(self):
        self.key = 'MAIN_55'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        grand_login(driver)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver, force=True)
        wait_popup_disappear(driver, icon_loading)
        # ===========================================================

        try:
            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(1)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)
            popup_title = driver.find_element_by_css_selector(ele_check_for_update_title).text
            popup_sub_title = driver.find_element_by_css_selector(sub_title_popup_cls).text

            dialog = driver.find_element_by_css_selector(dialog_content)
            list_labels = dialog.find_elements_by_css_selector('.wrap-label')
            list_labels_text = [l.text for l in list_labels]
            expected_list_label = ['Model Name', 'Current Version', 'Build Time', 'Auto Update', 'Manual Update']
            btn_apply_text = dialog.find_element_by_css_selector(apply).text

            list_actual1 = [popup_title, popup_sub_title, list_labels_text, btn_apply_text]
            list_expected1 = ['Firmware Update', exp_sub_title_update_firmware, expected_list_label, 'Update']
            step_1_name = "1. Goto firmware update. Check title and subtitle of popup. "
            list_check_in_step_2 = [
                f"Popup title is: {list_expected1[0]}",
                f"Popup sub title is: {list_expected1[1]}",
                f"List label in popup is:{list_expected1[2]}",
                f"Text of button apply is: {list_expected1[3]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_40012_path = os.path.join(os.getcwd(), 't10x_fullimage_4.00.12_rev11.img')
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40012_path)
            os.chdir(test_t10x_path)
            # Check firmware btn activated
            check_firmware_btn = driver.find_element_by_css_selector(apply).is_enabled()

            list_actual2 = [check_firmware_btn]
            list_expected2 = [return_true]
            step_2_name = "2. Choose firmware file: t10x_fullimage_4.00.12_rev11.img. "
            list_check_in_step_2 = [
                "Button firmware is enabled"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(150)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            wait_ethernet_available()
            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [check_login_page]
            list_expected4 = [return_true]
            step_3_4_name = "3, 4. Click Firmware Update button. After reboot. Check login popup displayed. "
            list_check_in_step_3_4 = [
                "Login popup is appear"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()
            grand_login(driver)
            firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
            check_firmware = True if firmware_version.endswith(expected_firmware_40012) else False
            print(check_firmware)

            list_actual5 = [check_firmware]
            list_expected5 = [return_true]
            step_5_name = "5. Login again. Check firmware version."
            list_check_in_step_5 = [
                f"Condition 'firmware version end with {expected_firmware_40012}' is correct"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        list_step_fail.append('5. Assertion wong')

        change_firmware_version(driver, version='t10x_fullimage_3.00.12_rev11.img')
        self.assertListEqual(list_step_fail, [])

    def test_R_56_MAIN_System_Extender_mode_Check_Manual_downgrade_firmware(self):
        self.key = 'MAIN_56'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        detect_firmware_version(driver)
        # ===========================================================
        grand_login(driver)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver, force=True)
        wait_popup_disappear(driver, icon_loading)
        # ===========================================================

        try:
            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(1)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)
            popup_title = driver.find_element_by_css_selector(ele_check_for_update_title).text
            popup_sub_title = driver.find_element_by_css_selector(sub_title_popup_cls).text

            list_actual1 = [popup_title, popup_sub_title]
            list_expected1 = ['Firmware Update', exp_sub_title_update_firmware]
            step_1_name = "1. Goto firmware update. Check title and subtitle of popup"
            list_check_in_step_1 = [
                f"Popup title is: {list_expected1[0]}",
                f"Popup sub title is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_path = os.path.join(os.getcwd(), 't10x_fullimage_3.00.05_rev09.img')
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_path)
            os.chdir(test_t10x_path)
            # Check firmware btn activated
            check_firmware_btn = driver.find_element_by_css_selector(apply).is_enabled()

            list_actual2 = [check_firmware_btn]
            list_expected2 = [return_true]
            step_2_name = "2. Choose firmware file: t10x_fullimage_3.00.05_rev09.img. "
            list_check_in_step_2 = [
                "Firmware button is enabled"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(150)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [check_login_page]
            list_expected4 = [return_true]
            step_3_4_name = "3, 4. Click Firmware Update button. After reboot. Check login popup displayed. "
            list_check_in_step_3_4 = [
                "Login popup is appear"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            time.sleep(50)
            wait_ethernet_available()
            url_login = get_config('URL', 'url')
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')
            call_api_login_old_firmware(user_request, pass_word)
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)
            driver.find_element_by_css_selector(el_lg_user_down_firm).send_keys(user_request)
            time.sleep(1)
            driver.find_element_by_css_selector(el_lg_pw_down_firm).send_keys(pass_word)
            time.sleep(1)
            driver.find_element_by_css_selector(el_lg_button_down_firm).click()
            wait_visible(driver, el_home_wrap_down_firm)
            time.sleep(3)
            wait_ethernet_available()
            firmware_version = driver.find_element_by_css_selector(ele_home_info_old_firm_version).text
            check_firmware = True if firmware_version.endswith(expected_firmware_30005) else False
            print(check_firmware)
            wait_ethernet_available()
            list_actual5 = [check_firmware]
            list_expected5 = [return_true]
            step_5_name = "5. Login again. Check firmware version"
            list_check_in_step_5 = [
                f"Condition' firmware version end with {expected_firmware_30005}' is correct"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        list_step_fail.append('5. Assertion wong')

        detect_firmware_version(driver)
        self.assertListEqual(list_step_fail, [])

    def test_R_57_MAIN_System_Extender_mode_Check_the_exception_message_when_firmware_update(self):
        self.key = 'MAIN_57'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        detect_firmware_version(driver)
        factory_dut()
        # save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        file_no_format = 'wifi_default_file.xml'
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        time.sleep(2)
        connect_repeater_mode(driver, force=True)
        # ===========================================================
        try:
            time.sleep(30)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(1)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)
            popup_title = driver.find_element_by_css_selector(ele_check_for_update_title).text
            popup_sub_title = driver.find_element_by_css_selector(sub_title_popup_cls).text

            list_actual1 = [popup_title, popup_sub_title]
            list_expected1 = ['Firmware Update', exp_sub_title_update_firmware]
            step_1_name = "1. Goto firmware update. Check title and subtitle of popup"
            list_check_in_step_1 = [
                f"Title popup is: {list_expected1[0]}",
                f"Subtitle Title popup is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            os.chdir(files_path)
            no_format_path = os.path.join(os.getcwd(), file_no_format)
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(no_format_path)
            # Check firmware btn activated

            error_warning = driver.find_element_by_css_selector(err_dialog_msg_cls).text
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()

            list_actual2 = [error_warning]
            list_expected2 = [exp_msg_invalid_file_firmware]
            step_2_name = "2. Up wrong file. Check Error warning message. "
            list_check_in_step_2 = [
                f"Error warning message: {exp_msg_invalid_file_firmware}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_path = os.path.join(os.getcwd(), 't5_t7_t9_fullimage_4.00.11_rev25.img')
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_path)
            os.chdir(test_t10x_path)

            manual_update_value = driver.find_element_by_css_selector(el_firmware_manual_box_value).text

            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, icon_loading)
            time.sleep(20)
            wait_visible(driver, dialog_content)
            time.sleep(1)
            cpt_popup_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            list_actual3 = [manual_update_value, cpt_popup_msg]
            list_expected3 = ['t5_t7_t9_fullimage_4.00.11_rev25.img', exp_msg_update_fail_file_firmware]
            step_3_name = "3. Update invalid firmware. Check error message. "
            list_check_in_step_3 = [
                f"File name firmware update is: {list_expected3[0]}",
                f"Error message is: exp_msg_update_fail_file_firmware"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_40012_path = os.path.join(os.getcwd(), 't10x_fullimage_4.00.12_rev11.img')
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40012_path)
            os.chdir(test_t10x_path)

            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(150)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(20)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version)
            ActionChains(driver).move_to_element(firmware_version).perform()
            firmware_version = firmware_version.text
            check_firmware = True if firmware_version.endswith(expected_firmware_40012) else False

            list_actual4 = [check_firmware]
            list_expected4 = [return_true]
            step_4_name = "4. Update firmware 4.00.12. Check update successfully. "
            list_check_in_step_4 = [
                f"Condition 'name of firmware after update is end with {expected_firmware_40012}' is correct"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')
        change_firmware_version(driver)
        self.assertListEqual(list_step_fail, [])



    def test_R_83_MAIN_Verification_of_Repeater_Mesh_Menu_Tree(self):
        self.key = 'MAIN_83'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        # ===========================================================

        try:
            grand_login(driver)
            time.sleep(1)

            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = [
                "Home page is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            ls_menu_enable = driver.find_elements_by_css_selector(ele_home_tree_menu_enable)
            ls_menu_enable_text = [i.text for i in ls_menu_enable]

            ls_menu_disable = driver.find_elements_by_css_selector(ele_home_tree_menu_disable)
            ls_menu_disable_text = [i.text for i in ls_menu_disable]

            list_actual2 = [ls_menu_enable_text, ls_menu_disable_text]
            list_expected2 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE'],
                              ['QOS', 'SECURITY', 'ADVANCED']]
            step_2_name = "2. Check list tree menu Enable, list tree menu disable. "
            list_check_in_step_2 = [
                f"List enable menu is: {list_expected2[0]}",
                f"List disable menu is: {list_expected2[1]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            # Click Network
            goto_menu(driver, network_tab, 0)
            wait_popup_disappear(driver, icon_loading)
            network_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click WL
            goto_menu(driver, wireless_tab, 0)
            wireless_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click MS
            goto_menu(driver, media_share_tab, 0)
            media_share_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)

            list_actual3 = [network_submenu, wireless_submenu, media_share_submenu]
            list_expected3 = [['Operation Mode'], ['Repeater Setting', 'WPS'],
                              ['USB', 'Server Settings']]
            step_3_4_5_name = "3, 4, 5. Check Sub menu of NETWORK, WIRELESS, MS. "
            list_check_in_step_3_4_5 = [
                f"List network submenu is: {list_expected3[0]}",
                f"List wrieless submenu is: {list_expected3[0]}",
                f"List media share submenu is: {list_expected3[0]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4, 5. Assertion wong')

        try:
            # CLick system button
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()

            time.sleep(1)
            sys_button_text = [i.text for i in driver.find_elements_by_css_selector(ele_sys_list_button)]

            list_actual6 = [";".join(sorted(sys_button_text))]
            list_expected6 = [";".join(sorted(['Language', 'Firmware Update', 'Change Password', 'Backup/Restore',
                              'Restart/Factory Reset', 'Power Saving Mode', 'LED Mode', 'Date/Time', 'Wizard']))]
            step_6_name = "6. Check list button in System button. "
            list_check_in_step_6 = [
                f"List system button is: {list_expected6[0]}"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_R_85_MAIN_Verification_of_Login_page_on_Extender_mode(self):
        self.key = 'MAIN_85'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # Disconenct WAN
        # disconnect_or_connect_wan(disconnected=True)
        grand_login(driver)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        wait_ethernet_available()
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
            wait_visible(driver, home_view_wrap)
            # Check Privacy Policy
            policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) > 0
            welcome_popup = len(driver.find_elements_by_css_selector(lg_welcome_header)) > 0
            home_view = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            check_tab_true = False
            if any([policy_popup, welcome_popup, home_view]):
                check_tab_true = True

            list_actual1 = [check_tab_true]
            list_expected1 = [return_true]
            step_1_2_3_name = "1,2,3. Check function TAB key in login: TAB step by step, Click login check. Check login ok"
            list_check_in_step_1_2_3 = [
                "After fill login by tab and click login, login success"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1,2,3. Assertion wong')

        try:
            time.sleep(5)
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
            step_4_name = "4. Check Login page component: Welcome, user holder, pw holder, captcha holer, extra info."
            list_check_in_step_4 = [
                f"Wellcome text is: {expected_welcome_text_en}",
                f"User holder text is: {exp_lg_id_holder}",
                f"Password holder text is: {exp_lg_password_holder}",
                f"Captcha holder text is: {exp_lg_captcha_holder}",
                f"Extra info is: {exp_lg_extra_info}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append(
                '4. Assertion wong.')

        try:
            # Connect wifi
            wifi_name_mesh_2g = get_config('REPEATER', 'repeater_name', input_data_path)
            wifi_pw_mesh_2g = get_config('REPEATER', 'repeater_pw', input_data_path)
            connect_wifi_by_command(wifi_name_mesh_2g, wifi_pw_mesh_2g)
            time.sleep(10)
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)

            check_connected_2g_name = current_connected_wifi()
            driver.get(url_login)
            time.sleep(2)
            check_lg_page_2g = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual5 = [check_connected_2g_name, check_lg_page_2g]
            list_expected5 = [wifi_name_mesh_2g, return_true]
            step_5_name = "5. Check Connect wifi 2g. Check login page displayed. "
            list_check_in_step_5 = [
                f"Connect wifi name is: {wifi_name_mesh_2g}",
                "Page login is appear"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append(
                '5. Assertion wong.')

        try:
            os.system('netsh wlan disconnect')
            # Connect wifi
            wifi_name_mesh_5g = get_config('REPEATER', 'repeater_name_5g', input_data_path)
            wifi_pw_mesh_5g = get_config('REPEATER', 'repeater_pw_5g', input_data_path)
            connect_wifi_by_command(wifi_name_mesh_5g, wifi_pw_mesh_5g)


            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            check_connected_5g_name = current_connected_wifi()
            # driver.get(url_login)
            # time.sleep(2)
            # check_lg_page_5g = len(driver.find_elements_by_css_selector(lg_page)) > 0
            check_lg_page_5g = check_connect_to_web_admin_page()

            list_actual6 = [check_connected_5g_name, check_lg_page_5g]
            list_expected6 = [wifi_name_mesh_5g, return_true]
            step_6_name = "6. Check Connect wifi 5g. Check login page displayed. "
            list_check_in_step_6 = [
                f"Connected wifi name is: {wifi_name_mesh_5g}",
                "Login page is appear"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append(
                '6. Assertion wong.')
            self.list_steps.append('[END TC]')
        # disconnect_or_connect_wan(disconnected=False)
        self.assertListEqual(list_step_fail, [])

    def test_R_82_MAIN_Verification_of_Repeater_Mode_Third_Party_menu_tree(self):
        self.key = 'MAIN_82'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        THIRD_NAME = get_config('REPEATER', 'third_party_name', input_data_path)
        THIRD_PW = get_config('REPEATER', 'third_party_pw', input_data_path)
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        time.sleep(1)
        connect_repeater_mode_third_party(driver, UPPER=THIRD_NAME, PW=THIRD_PW)
        # ===========================================================

        try:
            grand_login(driver)
            time.sleep(1)

            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = [
                "Home page is appear"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')


        try:
            ls_menu_enable = driver.find_elements_by_css_selector(ele_home_tree_menu_enable)
            ls_menu_enable_text = [i.text for i in ls_menu_enable]

            ls_menu_disable = driver.find_elements_by_css_selector(ele_home_tree_menu_disable)
            ls_menu_disable_text = [i.text for i in ls_menu_disable]

            list_actual2 = [ls_menu_enable_text, ls_menu_disable_text]
            list_expected2 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE'],
                              ['QOS', 'SECURITY', 'ADVANCED']]
            step_2_name = "2. Check list tree menu Enable, list tree menu disable. "
            list_check_in_step_2 = [
                f"List menu enable is: {list_expected2[0]}",
                f"List menu disable is: {list_expected2[1]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            # Click Network
            goto_menu(driver, network_tab, 0)
            network_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click WL
            goto_menu(driver, wireless_tab, 0)
            wireless_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click MS
            goto_menu(driver, media_share_tab, 0)
            media_share_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)

            list_actual3 = [network_submenu, wireless_submenu, media_share_submenu]
            list_expected3 = [['Operation Mode'], ['Primary Network', 'Repeater Setting', 'WPS'],
                              ['USB', 'Server Setting']]
            step_3_4_5_name = "3, 4, 5. Check Sub menu of NETWORK, WIRELESS, MS. "
            list_check_in_step_3_4_5 = [
                f"Sub menu of network is: {list_expected3[0]}",
                f"Sub menu of wireless is: {list_expected3[1]}",
                f"Sub menu of media share is: {list_expected3[2]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4, 5. Assertion wong')

        try:
            # CLick system button
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()

            time.sleep(1)
            sys_button_text = [i.text for i in driver.find_elements_by_css_selector(ele_sys_list_button)]

            list_actual6 = [";".join(sorted(sys_button_text))]
            list_expected6 = [";".join(sorted(['Language', 'Firmware Update', 'Change Password', 'Backup/Restore',
                              'Restart/Factory Reset', 'Power Saving Mode', 'LED Mode', 'Date/Time', 'Wizard']))]
            step_6_name = "6. Check list button in System button. "
            list_check_in_step_6 = [
                f"List system button is: {list_expected6[0]}"
            ]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')
        self.assertListEqual(list_step_fail, [])



if __name__ == '__main__':
    unittest.main()
