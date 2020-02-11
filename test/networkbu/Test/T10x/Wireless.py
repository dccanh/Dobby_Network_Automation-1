import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver


class WIRELESS(unittest.TestCase):
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

    def test_03_Verification_of_Security_Settings(self):
        self.key = 'WIRELESS_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')

        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'

        VALID_PASSWORD = '0123456789'
        PASSWORD_4 = '123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;\'"<>,/123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;\'"<>,/'
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            block_2g = driver.find_element_by_css_selector(left)
            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            self.list_steps.append(
                '[Pass] 1,2. Goto Primary network \n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Goto Primary network. ')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            SECURITY_TYPE = 'NONE'
            # 2G Change security
            setting_wireless_security(block_2g, SECURITY_TYPE)
            # Apply
            apply(driver, block_2g)

            # 5G Change security
            setting_wireless_security(block_5g, SECURITY_TYPE)
            # Apply
            apply(driver, block_5g)

            list_actual = []
            list_expected = []
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3,4. Change Security is NONE check access Google')
        except:
            self.list_steps.append(
                f'[Fail] 3,4. Change Security is NONE check access Google'
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            SECURITY_TYPE = 'WPA2-PSK'
            # 2G Change security
            setting_wireless_security(block_2g, SECURITY_TYPE)

            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(VALID_PASSWORD).perform()

            # Apply
            apply(driver, block_2g)

            # 5G Change security
            setting_wireless_security(block_5g, SECURITY_TYPE)
            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(VALID_PASSWORD).perform()

            # Apply
            apply(driver, block_2g)

            list_actual = []
            list_expected = []
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 5,6. Change Security is {SECURITY_TYPE} check access Google ')
        except:
            self.list_steps.append(
                f'[Fail] 5,6. Change Security is {SECURITY_TYPE} check access Google . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('5,6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            SECURITY_TYPE = 'WPA2/WPA-PSK'
            # 2G Change security
            setting_wireless_security(block_2g, SECURITY_TYPE)

            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(VALID_PASSWORD).perform()

            # Apply
            apply(driver, block_2g)

            # 5G Change security
            setting_wireless_security(block_5g, SECURITY_TYPE)
            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(VALID_PASSWORD).perform()

            # Apply
            apply(driver, block_2g)

            list_actual = []
            list_expected = [ ]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 5,6. Change Security is {SECURITY_TYPE} check access Google ')
        except:
            self.list_steps.append(
                f'[Fail] 5,6. Change Security is {SECURITY_TYPE} check access Google . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('5,6. Assertion wong.')

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

    def test_11_Verification_of_WebUI_Access_Operation(self):
        self.key = 'WIRELESS_11'
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
            # WebUI
            web_access_2g = block_2g.find_elements_by_css_selector(select)[1]
            check_web_access_2g = web_access_2g.find_element_by_css_selector(input).is_selected()

            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            # WebUI
            web_access_5g = block_5g.find_elements_by_css_selector(select)[1]
            check_web_access_5g = web_access_5g.find_element_by_css_selector(input).is_selected()

            pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            pw_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_2g)
            act.perform()

            # 5G Pw
            pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            act_5g = ActionChains(driver)
            act_5g.click_and_hold(pw_eye_5g)
            pw_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            act_5g.release(pw_eye_5g)
            act_5g.perform()

            list_actual = [check_web_access_2g, check_web_access_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Web UI Access of 2G/5G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Enable Web UI Access of 2G/5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            if not check_web_access_2g:
                # If Default is uncheck => Check
                web_access_2g.click()
                time.sleep(0.2)
                # Click Apply
                time.sleep(0.5)
                block_2g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            if not check_web_access_5g:
                # If Default is uncheck => Check
                web_access_5g.click()
                time.sleep(0.2)
                # Click Apply
                time.sleep(0.5)
                block_5g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            # Connect 2G > Access login page
            change_nw_profile(wifi_2g_path, 'Password', pw_2g)
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(1)
            driver.get(URL_LOGIN)
            wait_popup_disappear(driver, dialog_loading)
            check_2g = len(driver.find_elements_by_css_selector(lg_page)) != 0
            time.sleep(3)

            # Connect 5G > Access login page
            change_nw_profile(wifi_5g_path, 'Password', pw_5g)
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(3)
            driver.get(URL_LOGIN)
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            check_5g = len(driver.find_elements_by_css_selector(lg_page)) != 0
            time.sleep(3)

            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Enable Web UI Access of 2G/5G: Check Access web UI successfully. ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Enable Web UI Access of 2G/5G: Check Access web UI successfully.. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Disconnect Wifi to enable LAN
            os.system('netsh wlan disconnect')
            time.sleep(1)
            # Login
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
            # WebUI
            web_access_2g = block_2g.find_elements_by_css_selector(select)[1]
            check_web_access_2g = web_access_2g.find_element_by_css_selector(input).is_selected()

            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            # WebUI
            web_access_5g = block_5g.find_elements_by_css_selector(select)[1]
            check_web_access_5g = web_access_5g.find_element_by_css_selector(input).is_selected()

            # Disable
            if check_web_access_2g:
                # If Default is check => unCheck
                web_access_2g.click()
                time.sleep(0.2)
                # Click Apply
                time.sleep(0.5)
                block_2g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            if check_web_access_5g:
                # If Default is uncheck => Check
                web_access_5g.click()
                time.sleep(0.2)
                # Click Apply
                time.sleep(0.5)
                block_5g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            # Connect 2G > Access login page
            change_nw_profile(wifi_2g_path, 'Password', pw_2g)
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(1)
            driver.get(URL_LOGIN)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(lg_page)) == 0
            time.sleep(3)

            # Connect 5G > Access login page
            change_nw_profile(wifi_5g_path, 'Password', pw_5g)
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(1)
            driver.get(URL_LOGIN)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(lg_page)) == 0
            time.sleep(3)

            os.system('netsh wlan disconnect')
            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check Disable Web UI Access of 2G/5G: Check Access web UI fail')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Disable Web UI Access of 2G/5G: Check Access web UI fail. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_16_Check_SSID_setting(self):
        self.key = 'WIRELESS_16'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        SSID_TEST = '123!@ abcd #^&*()+_-={}[]|456:789.?`$%\;'
        SSID_2G_DEFAULT_START = 'HUMAX_Guest_2G!_'
        SSID_5G_DEFAULT_START = 'HUMAX_Guest_5G!_'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            # 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_2g_label = edit_2g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = edit_2g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    # Get default value
                    default_ssid_2g_value = f.find_element_by_css_selector(input).get_attribute('value')
                    time.sleep(0.2)
                    # Send key to SSID
                    f.click()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(SSID_TEST).perform()
                    time.sleep(1)
                    changed_ssid_2g_value = f.find_element_by_css_selector(input).get_attribute('value')
                    break
            check_default_ssid_2g_value = default_ssid_2g_value.startswith(SSID_2G_DEFAULT_START)
            list_actual = [check_default_ssid_2g_value, changed_ssid_2g_value]
            list_expected = [return_true, SSID_TEST[:32]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default SSID and Changed SSID of 2G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default SSID and Changed SSID of 2G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')
        try:
            # 5G
            block_5g = driver.find_element_by_css_selector(guest_network_block)
            ActionChains(driver).move_to_element(block_5g).perform()
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[1]
            # Settings
            edit_5g_label = edit_5g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_5g_fields = edit_5g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_5g_label, edit_5g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    # Get default value
                    default_ssid_5g_value = f.find_element_by_css_selector(input).get_attribute('value')
                    time.sleep(0.2)
                    # Send key to SSID
                    f.click()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(SSID_TEST).perform()
                    time.sleep(1)
                    changed_ssid_5g_value = f.find_element_by_css_selector(input).get_attribute('value')
                    break
            check_default_ssid_5g_value = default_ssid_5g_value.startswith(SSID_5G_DEFAULT_START)
            list_actual = [check_default_ssid_5g_value, changed_ssid_5g_value]
            list_expected = [return_true, SSID_TEST[:32]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Default SSID and Changed SSID of 5G. ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Default SSID and Changed SSID of 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_17_Verification_of_Guest_Network_Duplicate_SSID_Registration(self):
        self.key = 'WIRELESS_17'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            # 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_2g_label = edit_2g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = edit_2g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    default_ssid_2g_value = f.find_element_by_css_selector(input).get_attribute('value')
                    break
            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # Click Add
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_2g_label = edit_2g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = edit_2g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    # Send key to SSID
                    f.click()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(default_ssid_2g_value).perform()
                    time.sleep(1)
                    break
            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            error_msg_2g = driver.find_element_by_css_selector(err_dialog_msg_cls).text
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            list_actual = [error_msg_2g]
            list_expected = [exp_dialog_add_same_ssid]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Add same SSID of 2G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Add same SSID of 2G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')
        try:
            # 5G
            block_5g = driver.find_element_by_css_selector(guest_network_block)
            ActionChains(driver).move_to_element(block_5g).perform()
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[1]
            # Settings
            edit_5g_label = edit_5g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_5g_fields = edit_5g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_5g_label, edit_5g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    # Get default value
                    default_ssid_5g_value = f.find_element_by_css_selector(input).get_attribute('value')
                    break
            # Apply
            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            block_5g = driver.find_element_by_css_selector(guest_network_block)
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[1]
            # Settings
            edit_5g_label = edit_5g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_5g_fields = edit_5g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_5g_label, edit_5g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    # Send key to SSID
                    f.click()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(default_ssid_5g_value).perform()
                    time.sleep(1)
                    break
            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            error_msg_5g = driver.find_element_by_css_selector(err_dialog_msg_cls).text
            time.sleep(0.5)
            list_actual = [error_msg_5g]
            list_expected = [exp_dialog_add_same_ssid]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Add same SSID of 5G. ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Add same SSID of 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_19_Verification_of_setting_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_19'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WPA2-PSK'
        PASSWORD_SHORT_STR = '123$%'
        PASSWORD_LONG_STR = '123!@ abcd #^&*()+_-={}[]|456:789.?`$%<>,/123!@ abcd #^&*()+_-={}[]|456:789.?`$%<>,/'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            # 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)


            # Check Default Value
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_2g_label = edit_2g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = edit_2g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                if l.text == 'Network Name(SSID)':
                    default_ssid_2g_value = f.find_element_by_css_selector(input).get_attribute('value')
                # Check Security
                if l.text == 'Security':
                    default_security_2g = f.find_element_by_css_selector(secure_value_field).get_attribute('value')
                    if default_security_2g != SECURITY_TYPE:
                        f.click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == SECURITY_TYPE:
                                o.click()
                                time.sleep(1)
                    break
            # Verify Default Password
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_2g = edit_2g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            pw_default_2g = edit_2g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_2g)
            act.perform()
            # Change password
            pw_2g = edit_2g_block.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_SHORT_STR).perform()
            error_msg_2g = edit_2g_block.find_element_by_css_selector(password_error_msg).text

            # 2G Change long password
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_LONG_STR).perform()

            # 2G New pw
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_2g = edit_2g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            new_pw_2g = edit_2g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_2g)
            act.perform()

            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            list_actual = [pw_default_2g, error_msg_2g, new_pw_2g]
            list_expected = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Change security type: Check Default Password and Message too short 2G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Change security type: Check Default Password and Message too short 2G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            ActionChains(driver).move_to_element(block_5g).perform()
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_5g_label = edit_5g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_5g_fields = edit_5g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_5g_label, edit_5g_fields):
                if l.text == 'Network Name(SSID)':
                    default_ssid_5g_value = f.find_element_by_css_selector(input).get_attribute('value')
                # Security type
                if l.text == 'Security':
                    default_security_5g = f.find_element_by_css_selector(secure_value_field).get_attribute('value')
                    if default_security_5g != SECURITY_TYPE:
                        f.click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == SECURITY_TYPE:
                                o.click()
                                time.sleep(1)
                    break
            # Verify Default Password
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_5g = edit_5g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_5g)
            pw_default_5g = edit_5g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_5g)
            act.perform()
            # Change password
            pw_5g = edit_5g_block.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_SHORT_STR).perform()
            error_msg_5g = edit_5g_block.find_element_by_css_selector(password_error_msg).text

            # 5G Change long password
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_LONG_STR).perform()

            # 5G New pw
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_5g = edit_5g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_5g)
            new_pw_5g = edit_5g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_5g)
            act.perform()

            # Apply
            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            list_actual = [pw_default_5g, error_msg_5g, new_pw_5g]
            list_expected = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3, 4. Change security type: Check Default Password and Message too short of 5G. ')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Change security type: Check Default Password and Message too short of 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3, 4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Write to wifi xml file
            change_nw_profile(wifi_2g_path, 'Ssid', default_ssid_2g_value)
            change_nw_profile(wifi_2g_path, 'Password', new_pw_2g)
            change_nw_profile(wifi_2g_path, 'Security', 'WPA2PSK')

            change_nw_profile(wifi_5g_path, 'Ssid', default_ssid_5g_value)
            change_nw_profile(wifi_5g_path, 'Password', new_pw_5g)
            change_nw_profile(wifi_5g_path, 'Security', 'WPA2PSK')
            # 2G Connect wifi
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) != 0

            # 5G Connect wifi
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) != 0
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

    def test_20_Verification_of_setting_WPA_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WPA2/WPA-PSK'
        PASSWORD_SHORT_STR = '123$%'
        PASSWORD_LONG_STR = '123!@ abcd #^&*()+_-={}[]|456:789.?`$%<>,/123!@ abcd #^&*()+_-={}[]|456:789.?`$%<>,/'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            # 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_2g_label = edit_2g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = edit_2g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                if l.text == 'Network Name(SSID)':
                    default_ssid_2g_value = f.find_element_by_css_selector(input).get_attribute('value')
                # Check Security
                if l.text == 'Security':
                    default_security_2g = f.find_element_by_css_selector(secure_value_field).get_attribute('value')
                    if default_security_2g != SECURITY_TYPE:
                        f.click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == SECURITY_TYPE:
                                o.click()
                                time.sleep(1)
                    break
            # Verify Default Password
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_2g = edit_2g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            pw_default_2g = edit_2g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_2g)
            act.perform()
            # Change password
            pw_2g = edit_2g_block.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_SHORT_STR).perform()
            error_msg_2g = edit_2g_block.find_element_by_css_selector(password_error_msg).text

            # 2G Change long password
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_LONG_STR).perform()

            # 2G New pw
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_2g = edit_2g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_2g)
            new_pw_2g = edit_2g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_2g)
            act.perform()

            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            list_actual = [pw_default_2g, error_msg_2g, new_pw_2g]
            list_expected = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Change security type: Check Default Password and Message too short 2G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Change security type: Check Default Password and Message too short 2G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            ActionChains(driver).move_to_element(block_5g).perform()
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_5g_label = edit_5g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_5g_fields = edit_5g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_5g_label, edit_5g_fields):
                if l.text == 'Network Name(SSID)':
                    default_ssid_5g_value = f.find_element_by_css_selector(input).get_attribute('value')
                # Security type
                if l.text == 'Security':
                    default_security_5g = f.find_element_by_css_selector(secure_value_field).get_attribute('value')
                    if default_security_5g != SECURITY_TYPE:
                        f.click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == SECURITY_TYPE:
                                o.click()
                                time.sleep(1)
                    break
            # Verify Default Password
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_5g = edit_5g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_5g)
            pw_default_5g = edit_5g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_5g)
            act.perform()
            # Change password
            pw_5g = edit_5g_block.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_SHORT_STR).perform()
            error_msg_5g = edit_5g_block.find_element_by_css_selector(password_error_msg).text

            # 5G Change long password
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_LONG_STR).perform()

            # 5G New pw
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            pw_eye_5g = edit_5g_block.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye_5g)
            new_pw_5g = edit_5g_block.find_element_by_css_selector(input_pw).get_attribute('value')
            act.release(pw_eye_5g)
            act.perform()

            # Apply
            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            list_actual = [pw_default_5g, error_msg_5g, new_pw_5g]
            list_expected = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3, 4. Change security type: Check Default Password and Message too short of 5G. ')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Change security type: Check Default Password and Message too short of 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3, 4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Write to wifi xml file
            change_nw_profile(wifi_2g_path, 'Ssid', default_ssid_2g_value)
            change_nw_profile(wifi_2g_path, 'Password', new_pw_2g)
            change_nw_profile(wifi_2g_path, 'Security', 'WPA2PSK')

            change_nw_profile(wifi_5g_path, 'Ssid', default_ssid_5g_value)
            change_nw_profile(wifi_5g_path, 'Password', new_pw_5g)
            change_nw_profile(wifi_5g_path, 'Security', 'WPA2PSK')
            # 2G Connect wifi
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) != 0

            # 5G Connect wifi
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) != 0
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

    def test_25_Verification_of_Hide_SSID_action(self):
        self.key = 'WIRELESS_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WPA2/WPA-PSK'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            # 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_2g_label = edit_2g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = edit_2g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                if l.text == 'Network Name(SSID)':
                    default_ssid_2g_name = f.find_element_by_css_selector(input).get_attribute('value')
                # Check Security
                if l.text == 'Security':
                    default_security_2g = f.find_element_by_css_selector(secure_value_field).get_attribute('value')
                    if default_security_2g != SECURITY_TYPE:
                        f.click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == SECURITY_TYPE:
                                o.click()
                                time.sleep(1)
                                break
                    # Verify Default Password
                    edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
                    pw_eye_2g = edit_2g_block.find_element_by_css_selector(password_eye)
                    act = ActionChains(driver)
                    act.click_and_hold(pw_eye_2g)
                    pw_default_2g = edit_2g_block.find_element_by_css_selector(input_pw).get_attribute('value')
                    act.release(pw_eye_2g)
                    act.perform()

                if l.text == 'Hide SSID':
                    # Hide SSID
                    hide_ssid_2g = f.find_elements_by_css_selector(select)[0]
                    default_hide_ssid_2g = hide_ssid_2g.find_element_by_css_selector(input).is_selected()

                    hide_ssid_2g.click()
                    time.sleep(0.2)
                    driver.find_element_by_css_selector(btn_ok).click()

                    # Changed SSID
                    hide_ssid_2g = f.find_elements_by_css_selector(select)[0]
                    changed_hide_ssid_2g = hide_ssid_2g.find_element_by_css_selector(input).is_selected()
                    # Apply
                    driver.find_element_by_css_selector(apply).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(0.5)
                    break

            list_actual = [default_hide_ssid_2g, changed_hide_ssid_2g]
            list_expected = [return_false, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check default Hide SSID, Enable Hide SSID: Check Enable successfully of 2G. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check default Hide SSID, Enable Hide SSID: Check Enable successfully of 2G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            ActionChains(driver).move_to_element(block_5g).perform()
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            # Settings
            edit_5g_label = edit_5g_block.find_elements_by_css_selector(label_name_in_2g)
            edit_5g_fields = edit_5g_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_5g_label, edit_5g_fields):
                if l.text == 'Network Name(SSID)':
                    default_ssid_5g_name = f.find_element_by_css_selector(input).get_attribute('value')
                # Security type
                if l.text == 'Security':
                    default_security_5g = f.find_element_by_css_selector(secure_value_field).get_attribute('value')
                    if default_security_5g != SECURITY_TYPE:
                        f.click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == SECURITY_TYPE:
                                o.click()
                                time.sleep(1)
                                break
                    # Verify Default Password
                    edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
                    pw_eye_5g = edit_5g_block.find_element_by_css_selector(password_eye)
                    act = ActionChains(driver)
                    act.click_and_hold(pw_eye_5g)
                    pw_default_5g = edit_5g_block.find_element_by_css_selector(input_pw).get_attribute('value')
                    act.release(pw_eye_5g)
                    act.perform()
                if l.text == 'Hide SSID':
                    # Hide SSID
                    hide_ssid_5g = f.find_elements_by_css_selector(select)[0]
                    default_hide_ssid_5g = hide_ssid_5g.find_element_by_css_selector(input).is_selected()

                    hide_ssid_5g.click()
                    time.sleep(0.2)
                    driver.find_element_by_css_selector(btn_ok).click()
                    # Changed SSID
                    hide_ssid_5g = f.find_elements_by_css_selector(select)[0]
                    changed_hide_ssid_5g = hide_ssid_5g.find_element_by_css_selector(input).is_selected()
                    # Apply
                    driver.find_element_by_css_selector(apply).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(0.5)
                    break

            list_actual = [default_hide_ssid_5g, changed_hide_ssid_5g]
            list_expected = [return_false, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check default Hide SSID, Enable Hide SSID: Check Enable successfully of 5G. ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check default Hide SSID, Enable Hide SSID: Check Enable successfully of 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            time.sleep(5)
            ls_current_wifi = scan_wifi()
            check_wf = False
            if default_ssid_2g_name not in ls_current_wifi:
                check_wf = True
            elif default_ssid_5g_name not in ls_current_wifi:
                check_wf = True
            list_actual = [check_wf]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Scan current wifi: Check 2G and 5G Guest not in wifi list')
        except:
            self.list_steps.append(
                f'[Fail] 4. Scan current wifi: Check 2G and 5G Guest not in wifi list. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')
        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Write to wifi xml file
            change_nw_profile(wifi_2g_path, 'Ssid', default_ssid_2g_name)
            change_nw_profile(wifi_2g_path, 'Password', pw_default_2g)
            change_nw_profile(wifi_2g_path, 'Security', 'WPA2PSK')

            change_nw_profile(wifi_5g_path, 'Ssid', default_ssid_5g_name)
            change_nw_profile(wifi_5g_path, 'Password', pw_default_5g)
            change_nw_profile(wifi_5g_path, 'Security', 'WPA2PSK')
            # 2G Connect wifi
            connect_wifi_from_xml(wifi_2g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) != 0

            # 5G Connect wifi
            connect_wifi_from_xml(wifi_5g_path)
            time.sleep(2)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) != 0
            os.system('netsh wlan disconnect')
            list_actual = [check_2g, check_5g]
            list_expected = [return_true] * 2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of 2G/5G Guest wifi ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of 2G/5G Guest wifi. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
