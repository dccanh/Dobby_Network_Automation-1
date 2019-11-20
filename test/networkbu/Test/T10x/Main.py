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
                f'[Fail] 1, 2. Get result by command success. Actual: {str(list_actual)}. Expected: Actual not None')
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
                f'[Fail] 3. Check login Page displayed, id, password, captcha img, captcha input field. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 4. Check Msg connect wifi successfully. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 5. Check login Page displayed, id, password, captcha img, captcha input field. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 1,2. Check Login and Restore fail. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 3,4. Change language and check in login. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 5. Check Login and Restore fail. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 6,7. Change language and check in login. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 4. Check login Page displayed, id, password, captcha img, captcha input field. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 1,2,3. Check function TAB key in login. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                f'[Fail] 4. Change language and check in login. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

    def test_Verify_the_Login_operation(self):
        global list_actual, list_expected
        self.key = 'MAIN_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        NEW_PASSWORD = 'Dinhcongcanh1'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(300)

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        url_login = get_config('URL', 'url')
        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)

        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            # Welcome pop up displayed
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0

            list_actual = [check_login]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check pop-up welcome appear')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check pop-up welcome appear. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            list_actual = [check_dialog_disappear, check_home_displayed]
            list_expected = [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check Welcome dialog disappear, Home page display\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4.Check Welcome dialog disappear, Home page display. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_Verify_the_operation_at_Login(self):
        global list_actual, list_expected
        self.key = 'MAIN_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 3 mins for factory
        time.sleep(250)

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        url_login = get_config('URL', 'url')
        get_result_command_from_server(url_ip=url_login, filename=filename_2)

        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
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
            check_policy_popup = driver.find_element_by_css_selector(lg_privacy_policy_pop).is_displayed()

            list_actual = [check_policy_popup]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check pop-up Privacy is displayed')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check pop-up Privacy is displayed. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1,2. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~ Check Privacy
        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            # Check Privacy Policy disappear
            check_policy_popup = driver.find_element_by_css_selector(lg_privacy_policy_pop).is_displayed()
            # Check Login page appear
            check_lg_page = driver.find_element_by_css_selector(lg_page).is_displayed()
            list_actual = [check_policy_popup, check_lg_page]
            list_expected = [return_false, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Send: ESC. Check Privacy disappear, Home page displayed\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Send: ESC. Check Privacy disappear, Home page displayed. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            check_policy_popup = driver.find_element_by_css_selector(lg_privacy_policy_pop).is_displayed()
            check_btn_agree = driver.find_element_by_css_selector(btn_ok).get_property('disabled')

            list_actual = [check_policy_popup, check_btn_agree]
            list_expected = [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check pop-up Privacy is displayed, Agree disabled')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check pop-up Privacy is displayed, Agree disabled. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            # Check btn Agree enabled
            check_btn_agree = driver.find_element_by_css_selector(btn_ok).get_property('disabled')

            list_actual = [check_btn_agree]
            list_expected = [return_false]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Send key: PAGE_UP, DOWN. Check Agree enabled')
        except:
            self.list_steps.append(
                f'[Fail] 5. Send key: PAGE_UP, DOWN. Check Agree enabled. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('5. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~ Check Welcome ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Click Agree
            driver.find_element_by_css_selector(btn_ok).click()
            # Check Welcome Dialog appear
            time.sleep(3)
            check_welcome = driver.find_element_by_css_selector(lg_welcome_header).is_displayed()
            list_actual = [check_welcome]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Click Agree. Check Welcome dialog displayed')
        except:
            self.list_steps.append(
                f'[Fail] 6. Click Agree. Check Welcome dialog displayed. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('6. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~ Logout and Login Again ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Logout
            driver.get(url_login)
            check_lg_page = driver.find_element_by_css_selector(lg_page).is_displayed()
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
            list_actual = [check_lg_page, check_welcome]
            list_expected = [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Login again. Check Welcome dialog displayed')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Login again. Check Welcome dialog displayed. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_Verify_the_operation_at_Login_page_with_incorrect_id_pw(self):
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

            list_actual = [msg_error, check_lg_page]
            list_expected = [exp_wrong_captcha, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Error Wrong Captcha, Page login displayed.')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Error Wrong Captcha Page login displayed. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            list_actual = [msg_error, check_lg_page]
            list_expected = [exp_wrong_id_pw, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Error wrong ID& PW.')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Error wrong ID& PW. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [check_error_msg, check_error_msg_time, check_lg_btn]
            list_expected = [return_true, check_error_msg_time, return_false]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check Error wrong ID& PW: 9 msg warning, 1 msg count time, lgin btn enabled after count.')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Error wrong ID& PW: 9 msg warning, 1 msg count time, lgin btn enabled after count. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [check_error_msg, check_error_msg_time, check_lg_btn]
            list_expected = [return_true, check_error_msg_time, return_false]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Error wrong ID& PW: 1 msg warning, 1 msg count time, lgin btn enabled after count.')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Error wrong ID& PW: 1 msg warning, 1 msg count time, lgin btn enabled after count. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [check_error_msg, check_error_msg_time, check_lg_btn]
            list_expected = [return_true, check_error_msg_time, return_false]
            check = assert_list(list_actual, list_expected)
            # Wait ultil Done
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
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')
        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
