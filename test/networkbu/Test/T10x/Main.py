import sys
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.captcha import *
from Helper.t10x.config.data_expected import *
from Helper.t10x.config.elements import *
# from Helper.t10x.config.read_config import *
from Helper.t10x.secure_crt.common import *
from Helper.t10x.common import *
from selenium import webdriver
from selenium.webdriver.support.select import Select


class Main(unittest.TestCase):
    def setUp(self):
        try:
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            self.driver = webdriver.Chrome(driver_path)  # open chrome
            self.driver.maximize_window()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        end_time = datetime.now()
        duration = str((end_time - self.start_time))
        write_ggsheet(self.key, self.list_steps, self.def_name, duration)
        self.driver.quit()

    def test_Verify_the_Web_UI_connection_through_Gateway_IP(self):
        global list_actual, list_expected, password_config, url_config, user_config
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
            list_actual = [check_url]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Get result by command success\n')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Get result by command success\nActual: {str(list_actual)}. \nExpected: Actual not None')
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

            list_actual = [check_lg_page_displayed,
                           check_lg_id_field,
                           check_lg_password_field,
                           check_lg_captcha_img,
                           check_lg_captcha_field]
            list_expected = [return_true]*5
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check login Page displayed, id, password, captcha img, captcha input field\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check login Page displayed, id, password, captcha img, captcha input field\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

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
                '[Pass] 4. Check Msg connect wifi successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Msg connect wifi successfully\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
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
                '[Pass] 5 Check login Page displayed, id, password, captcha img, captcha input field\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check login Page displayed, id, password, captcha img, captcha input field\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_Verify_the_Default_setting_of_Language(self):
        global list_actual, list_expected, password_config, url_config, user_config
        self.key = 'MAIN_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url = get_config('URL', 'url')
        set_language_1 = 'English'
        set_language_2 = 'Vietnamese'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            # Goto Homepage
            driver.get(url+homepage)
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
            visible = driver.find_elements_by_css_selector(dialog_loading)
            count = 0
            # Check time out = True mean time <= 5 mins
            check_time_out = True
            while len(visible) != 0:
                time.sleep(1)
                visible = driver.find_elements_by_css_selector(dialog_loading)
                count += 1
                # neu time > 300s => step2 fail
                if count == 100:
                    check_time_out = False

            if check_time_out:
                driver.refresh()
                login(driver)
            # wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            list_actual = [check_time_out]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Login and Restore successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Login and Restore fail\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~ Change Language
        try:
            # Goto Homepage
            driver.get(url + homepage)
            time.sleep(1)

            # System > Language
            driver.find_element_by_css_selector(system_btn).click()
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

            list_actual = [welcome_text]
            list_expected = [expected_welcome_text_en]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3,4. Change language and check in login\n')
        except:
            self.list_steps.append(
                f'[Fail] 3,4. Change language and check in login\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            list_step_fail.append(
                '3,4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Again
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(url+homepage)
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
            visible = driver.find_elements_by_css_selector(dialog_loading)
            count = 0
            # Check time out = True mean time <= 5 mins
            check_time_out = True
            while len(visible) != 0:
                time.sleep(1)
                visible = driver.find_elements_by_css_selector(dialog_loading)
                count += 1
                # neu time > 300s => step2 fail
                if count == 100:
                    check_time_out = False

            if check_time_out:
                driver.refresh()
                login(driver)
            # wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            list_actual = [check_time_out]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Login and Restore successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Login and Restore fail\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~ Change Language and verify
        try:
            # Goto Homepage
            driver.get(url + homepage)
            time.sleep(1)

            # System > Language
            driver.find_element_by_css_selector(system_btn).click()
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

            list_actual = [welcome_text]
            list_expected = [expected_welcome_text_vi]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6,7. Change language and check in login\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6,7. Change language and check in login\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '6,7. Assertion wong.')


        self.assertListEqual(list_step_fail, [])

    def test_Verify_the_Web_UI_connection_through_domain_address(self):
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
                f'[Fail] 1, 2. Get result by command success\nActual: {str(list_actual)}. \nExpected: Actual not None')
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
                f'[Fail] 3. Check Msg connect wifi successfully\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check login again ~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(sub_url)
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
                f'[Fail] 4. Check login Page displayed, id, password, captcha img, captcha input field\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_Verify_the_Login_page(self):
        global list_actual, list_expected, password_config, url_config, user_config
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

            list_actual = [check_login]
            list_expected = [return_true]

            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check function TAB key in login')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check function TAB key in login\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
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

            list_actual = [welcome_text,
                           id_holder,
                           password_holder,
                           captcha_holder,
                           extra_lg_info]
            list_expected = [expected_welcome_text_en,
                             exp_lg_id_holder,
                             exp_lg_password_holder,
                             exp_lg_captcha_holder,
                             exp_lg_extra_info]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Change language and check in login\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change language and check in login\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_Verify_the_Humax_Retail_CPE_Site_operation(self):
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
                f'[Fail] 1. Check tooltip in Company Img\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
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
                f'[Fail] 2. Check current URL\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    # def test_Verify_the_Login_operation(self):
    #     global list_actual, list_expected
    #     self.key = 'MAIN_09'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     url_login = get_config('URL', 'url')
    #
    #     commmand = 'factorycfg.sh -a'
    #     run_cmd(commmand, filename=False)
    #     # Wait 5 mins
    #     time.sleep(300)
    #
    #     filename = 'account.txt'
    #     commmand = 'capitest get Device.Users.User.2. leaf'
    #     run_cmd(commmand, filename)
    #     time.sleep(3)
    #     # Get account information from web server and write to config.txt
    #     get_result_command_from_server(url_ip=url_config, filename=filename)
    #
    #     user_new = get_config('ACCOUNT', 'user')
    #     password_new = get_config('ACCOUNT', 'password')
    #     # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         login(driver)
    #         # Input Welcome pop up
    #
    #
    #
    #
    #
    #         list_actual = []
    #         list_expected = [exp_tooltip_img]
    #
    #         check = assert_list(list_actual, list_expected)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 1. Check tooltip in Company Img')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1. Check tooltip in Company Img\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
    #         list_step_fail.append('1. Assertion wong')
    #     # ~~~~~~~~~~~~~~~~~~ Click to image
    #     try:
    #
    #         list_actual = []
    #         list_expected = [return_true]
    #         check = assert_list(list_actual, list_expected)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 2. Check current URL\n')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2. Check current URL\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('2. Assertion wong.')
    #     self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
