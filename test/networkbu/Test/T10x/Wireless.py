import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver


class Wireless(unittest.TestCase):
    def setUp(self):
        try:
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            self.driver = webdriver.Chrome(driver_path)  # open chrome
            self.driver.maximize_window()
            self.time_stamp = datetime.now()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        try:
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.time_stamp)
        except:
            # Connect by wifi if internet is down to handle exception for PPPoE
            os.system('netsh wlan connect ssid=HVNWifi name=HVNWifi')
            time.sleep(1)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.time_stamp)
            time.sleep(5)
            # Connect by LAN again
            os.system('netsh wlan disconnect')
            time.sleep(1)
        self.driver.quit()

    def test_02_Verification_of_the_Wifi_On_off_operation(self):
        self.key = 'WIRELESS_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(100)
        wait_DUT_activated(URL_LOGIN)
        wait_ping(URL_PING_CHECK)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        filename_2 = 'account.txt'
        command_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(command_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        SSID_NAME = '123! @ # ^ & * ( ) + _ - = { } [ ] | 456:789 . ? ` $ % \ ; \'" < > , /'
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            # Default SSID
            block_2g = driver.find_element_by_css_selector(left)
            ssid_2g = block_2g.find_elements_by_css_selector(input)[0]
            ssid_2g_name = ssid_2g.get_attribute('value')
            ssid_2g_placeholder = ssid_2g.get_attribute('placeholder')

            block_5g = driver.find_element_by_css_selector(right)
            ssid_5g = block_5g.find_elements_by_css_selector(input)[0]
            ssid_5g_name = ssid_5g.get_attribute('value')
            ssid_5g_placeholder = ssid_5g.get_attribute('placeholder')

            list_actual = [ssid_2g_name, ssid_5g_name, ssid_2g_placeholder, ssid_5g_placeholder]
            list_expected = [exp_ssid_2g_default_val,
                             exp_ssid_5g_default_val,
                             exp_ssid_placeHolder,
                             exp_ssid_placeHolder]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default SSID name and placeholder of 2G, 5G \n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default SSID name and placeholder of 2G, 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # 2G
            ActionChains(driver).move_to_element(ssid_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(SSID_NAME).perform()
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            # 5G
            ActionChains(driver).move_to_element(ssid_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(SSID_NAME).perform()
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(5)

            ssid_2g = block_2g.find_elements_by_css_selector(input)[0]
            ssid_2g_name = ssid_2g.get_attribute('value')
            ssid_5g = block_5g.find_elements_by_css_selector(input)[0]
            ssid_5g_name = ssid_5g.get_attribute('value')

            list_actual = [ssid_2g_name, ssid_5g_name]
            list_expected = [SSID_NAME[:32], SSID_NAME[:32]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Change name of SSID 2G/5G\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change name of SSID 2G/5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])



    def test_04_Verification_of_the_setting_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(100)
        wait_DUT_activated(URL_LOGIN)
        wait_ping(URL_PING_CHECK)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        filename_2 = 'account.txt'
        command_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(command_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WPA2-PSK'
        PASSWORD_3 = '12345'
        PASSWORD_4 = '123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;\'"<>,/123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;\'"<>,/'

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(URL_LOGIN + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)

            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # Default Pw
            block_2g = driver.find_element_by_css_selector(left)
            pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            time.sleep(1)
            pw_default_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye_2g)
            act.perform()

            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            act_5g = ActionChains(driver)
            act_5g.click_and_hold(pw_eye_5g)
            time.sleep(1)
            pw_default_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act_5g.release(pw_eye_5g)
            act_5g.perform()
            # Expected password = humax_ + serial_number
            expected_default_pw = 'humax_' + get_config('GENERAL', 'serial_number')
            list_actual = [pw_default_2g, pw_default_5g]
            list_expected = [expected_default_pw, expected_default_pw]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Password of 2G, 5G \n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default Password of 2G, 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # 2G Change security
            security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            security_2g.click()
            ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_2g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break
            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # 5G Change security
            security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            security_5g.click()
            ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_5g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break
            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text


            list_actual = [error_msg_2g, error_msg_5g]
            list_expected = [exp_password_error_msg, exp_password_error_msg]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Change password < 8 char of  2G/5G ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change password < 8 char of  2G/5G . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # 2G Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_4).perform()
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # 5G Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_4).perform()
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # Verify
            pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            time.sleep(1)
            pw_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye_2g)
            act.perform()

            # 5G Pw
            pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            act_5g = ActionChains(driver)
            act_5g.click_and_hold(pw_eye_5g)
            time.sleep(1)
            pw_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act_5g.release(pw_eye_5g)
            act_5g.perform()

            expected_pw = PASSWORD_4[:63]
            save_config(config_path, 'GENERAL', 'wifi_pw', expected_pw)
            list_actual = [pw_2g, pw_5g]
            list_expected = [expected_pw, expected_pw]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password > 63 chars of  2G/5G ')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password > 63 chars of  2G/5G . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Write to wifi xml file
            change_nw_profile(wifi_2g_path, 'Password', expected_pw)
            change_nw_profile(wifi_5g_path, 'Password', expected_pw)
            # 2G Connect wifi
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) == 0

            # 5G Connect wifi
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) == 0
            os.system('netsh wlan disconnect')
            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_05_Verification_of_the_setting_WPA_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(100)
        wait_DUT_activated(URL_LOGIN)
        wait_ping(URL_PING_CHECK)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        filename_2 = 'account.txt'
        command_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(command_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WPA/WPA2-PSK'
        PASSWORD_3 = '12345'
        PASSWORD_4 = '123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;\'"<>,/123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;\'"<>,/'
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(URL_LOGIN + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            # Default Pw
            block_2g = driver.find_element_by_css_selector(left)
            pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            time.sleep(1)
            pw_default_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye_2g)
            act.perform()

            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            act_5g = ActionChains(driver)
            act_5g.click_and_hold(pw_eye_5g)
            pw_default_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            act_5g.release(pw_eye_5g)
            act_5g.perform()
            # Expected password = humax_ + serial_number
            expected_default_pw = 'humax_' + get_config('GENERAL', 'serial_number')
            list_actual = [pw_default_2g, pw_default_5g]
            list_expected = [expected_default_pw, expected_default_pw]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Password of 2G, 5G \n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default Password of 2G, 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # 2G Change security
            security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            security_2g.click()
            ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_2g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break
            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # 5G Change security
            security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            security_5g.click()
            ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_5g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break
            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text


            list_actual = [error_msg_2g, error_msg_5g]
            list_expected = [exp_password_error_msg, exp_password_error_msg]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Change password < 8 char of  2G/5G ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change password < 8 char of  2G/5G . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # 2G Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_4).perform()
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # 5G Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_4).perform()
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # Verify
            pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            time.sleep(1)
            pw_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye_2g)
            act.perform()

            # 5G Pw
            pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            act_5g = ActionChains(driver)
            act_5g.click_and_hold(pw_eye_5g)
            time.sleep(1)
            pw_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act_5g.release(pw_eye_5g)
            act_5g.perform()

            expected_pw = PASSWORD_4[:63]
            save_config(config_path, 'GENERAL', 'wifi_pw', expected_pw)
            list_actual = [pw_2g, pw_5g]
            list_expected = [expected_pw, expected_pw]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password > 63 chars of  2G/5G ')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password > 63 chars of  2G/5G . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Write to wifi xml file
            change_nw_profile(wifi_2g_path, 'Password', expected_pw)
            change_nw_profile(wifi_5g_path, 'Password', expected_pw)
            # 2G Connect wifi
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) == 0

            # 5G Connect wifi
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) == 0

            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            os.system('netsh wlan disconnect')
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_10_Verification_of_Hide_SSID_function(self):
        self.key = 'WIRELESS_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        # URL_PING_CHECK = '192.168.1.1'
        # filename = '1'
        # command = 'factorycfg.sh -a'
        # run_cmd(command, filename=filename)
        # time.sleep(100)
        # wait_DUT_activated(URL_LOGIN)
        # wait_ping(URL_PING_CHECK)
        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # filename_2 = 'account.txt'
        # command_2 = 'capitest get Device.Users.User.2. leaf'
        # run_cmd(command_2, filename_2)
        # time.sleep(3)
        # # Get account information from web server and write to config.txt
        # get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(URL_LOGIN + homepage)
                time.sleep(2)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # 2G
            block_2g = driver.find_element_by_css_selector(left)
            # Hide SSID
            hide_ssid_2g = block_2g.find_elements_by_css_selector(select)[0]
            check_hide_ssid_2g = hide_ssid_2g.find_element_by_css_selector(input).is_selected()

            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            # Hide SSID
            hide_ssid_5g = block_5g.find_elements_by_css_selector(select)[0]
            check_hide_ssid_5g = hide_ssid_5g.find_element_by_css_selector(input).is_selected()

            pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            time.sleep(1)
            pw_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye_2g)
            act.perform()

            # 5G Pw
            pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            act_5g = ActionChains(driver)
            act_5g.click_and_hold(pw_eye_5g)
            time.sleep(1)
            pw_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act_5g.release(pw_eye_5g)
            act_5g.perform()

            list_actual = [check_hide_ssid_2g, check_hide_ssid_5g]
            list_expected = [return_false]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Hide SSID of 2G/5G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Enable Hide SSID of 2G/5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            hide_ssid_2g.click()
            time.sleep(0.2)
            dialog_title_2g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()
            # Click Apply
            time.sleep(0.5)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            check_hide_ssid_2g = hide_ssid_2g.find_element_by_css_selector(input).is_selected()

            time.sleep(1)
            hide_ssid_5g.click()
            time.sleep(0.2)
            dialog_title_5g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()
            # Click Apply
            time.sleep(0.5)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            check_hide_ssid_5g = hide_ssid_5g.find_element_by_css_selector(input).is_selected()

            list_actual = [dialog_title_2g, dialog_title_5g, check_hide_ssid_2g, check_hide_ssid_5g]
            list_expected = [exp_dialog_hide_ssid_title]*2 + [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3.Check Enable Hide SSID of 2G/5G: Check popup title, enable hide ssid. ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Enable Hide SSID of 2G/5G: Check popup title, enable hide ssid. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            time.sleep(5)
            ls_current_wifi = scan_wifi()
            check_wf = False
            if exp_ssid_2g_default_val not in ls_current_wifi:
                check_wf = True
            elif exp_ssid_5g_default_val not in ls_current_wifi:
                check_wf = True
            list_actual = [check_wf]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Scan current wifi: Check 2G and 5G not in wifi list')
        except:
            self.list_steps.append(
                f'[Fail] 4. Scan current wifi: Check 2G and 5G not in wifi list. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            time.sleep(1)
            # Write to wifi xml file
            change_nw_profile(wifi_2g_path, 'Password', pw_2g)
            change_nw_profile(wifi_5g_path, 'Password', pw_5g)
            # 2G Connect wifi
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) == 0
            time.sleep(3)
            # 5G Connect wifi
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) == 0
            os.system('netsh wlan disconnect')
            list_actual = [check_2g, check_5g]
            list_expected = [return_true] * 2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
