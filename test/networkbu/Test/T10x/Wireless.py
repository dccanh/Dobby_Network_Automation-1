import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver
import binascii
# from binascii import

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
    # OK
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
        time.sleep(150)
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
        SSID_NAME = '123! @ # ^  * ( ) + _ - = { } [ ] | 456:789 . ? ` $ % \ ;  , /'

        try:
            grand_login(driver)
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
                '[Pass] 1,2. Check Default SSID name and placeholder of 2G, 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default SSID name and placeholder of 2G, 5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

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
            self.list_steps.append('[Pass] 3. Change name of SSID 2G/5G. '
                                   f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change name of SSID 2G/5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    # Can setup Radius
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
    # OK F
    def test_04_Verification_of_the_setting_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(150)
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
        PASSWORD_4 = '123!@ abcd #^*()+_-={}[]|456:789.?`$%\;,/123!@ abcd #^*()+_-={}[]|456:789.?`$%\,/'

        try:
            grand_login(driver)
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

            list_actual1 = [pw_default_2g, pw_default_5g]
            list_expected1 = [expected_default_pw]*2
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Password of 2G, 5G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default Password of 2G, 5G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [error_msg_2g, error_msg_5g]
            list_expected2 = [exp_password_error_msg]*2
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Change password < 8 char of  2G/5G. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change password < 8 char of  2G/5G . '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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

            list_actual4 = [pw_2g, pw_5g]
            list_expected4 = [expected_pw]*2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password > 63 chars of  2G/5G. '
                                   f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password > 63 chars of  2G/5G . '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=exp_ssid_2g_default_val, new_pw=PASSWORD_4[:63],
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) >= 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=exp_ssid_5g_default_val, new_pw=PASSWORD_4[:63],
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(5)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true]*2
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_05_Verification_of_the_setting_WPA_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(120)
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
        SECURITY_TYPE = 'WPA2/WPA-PSK'
        PASSWORD_3 = '12345'
        PASSWORD_4 = '123!@ abcd #^*()+_-={}[]|456:789.?`$%\;,/123!@ abcd #^*()+_-={}[]|456:789.?`$%\;,/'
        try:
            grand_login(driver)

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
            list_expected = [expected_default_pw]*2
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
            # change_nw_profile(wifi_2g_path, 'Password', expected_pw)
            # change_nw_profile(wifi_5g_path, 'Password', expected_pw)


            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=exp_ssid_2g_default_val, new_pw=PASSWORD_4[:63], new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) >= 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=exp_ssid_5g_default_val, new_pw=PASSWORD_4[:63],
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(5)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            os.system('netsh wlan disconnect')
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual)}. '
                                   f'Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_08_Primary_Network_Verification_of_WEP64_setting(self):
        self.key = 'WIRELESS_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(120)
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
        SECURITY_TYPE = 'WEP'
        ENCRYPTION_TYPE = 'WEP64'
        KEY_TYPE = 'Character String'
        KEY_TYPE_2 = 'Hexadecimal'
        PASSWORD_3 = '123'
        PASSWORD_4 = '123@!12'
        PASSWORD_5 = '@!a1b2c3d4e5@!'

        try:
            grand_login(driver)

            time.sleep(1)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # Default Pw
            block_2g = driver.find_element_by_css_selector(left)
            # 2G Change security
            security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            security_2g.click()
            ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_2g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_2g = driver.find_element_by_css_selector(left)
            # Encryption
            encryption_2g = block_2g.find_element_by_css_selector(encryption_value_field)
            encryption_2g.click()
            ls_encryption_2g = encryption_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_2g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_2g = block_2g.find_element_by_css_selector(key_type_value_field)
            key_type_2g.click()
            ls_key_type_2g = key_type_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_2g:
                if o.get_attribute('option-value') == KEY_TYPE:
                    o.click()

            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text


            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            # 5G Change security
            security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            security_5g.click()
            ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_5g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_5g = driver.find_element_by_css_selector(right)
            # Encryption
            encryption_5g = block_5g.find_element_by_css_selector(encryption_value_field)
            encryption_5g.click()
            ls_encryption_5g = encryption_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_5g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_5g = block_5g.find_element_by_css_selector(key_type_value_field)
            key_type_5g.click()
            ls_key_type_5g = key_type_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_5g:
                if o.get_attribute('option-value') == KEY_TYPE:
                    o.click()

            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual3 = [error_msg_2g, error_msg_5g]
            list_expected3 = [exp_short_pw_error_msg]*2
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Change Secirity, Encryption, Keytype  and password  of  2G/5G '
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change Secirity, Encryption, Keytype  and password of  2G/5G . '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
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

            expected_pw = PASSWORD_4[:5]
            save_config(config_path, 'GENERAL', 'wifi_pw', expected_pw)

            list_actual4 = [pw_2g, pw_5g]
            list_expected4 = [expected_pw]*2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Ma hoa mat khau
            byte_pw_2g = expected_pw.encode("utf8")
            hex_pw_2g = binascii.hexlify(byte_pw_2g)
            decode_pw_2g = hex_pw_2g.decode('utf8')
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_2g_default_val,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_5g_default_val,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true]*2

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)
            check_ota_auto_update(driver)

            time.sleep(1)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # Default Pw
            block_2g = driver.find_element_by_css_selector(left)
            # 2G Change security
            security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            security_2g.click()
            ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_2g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_2g = driver.find_element_by_css_selector(left)
            # Encryption
            encryption_2g = block_2g.find_element_by_css_selector(encryption_value_field)
            encryption_2g.click()
            ls_encryption_2g = encryption_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_2g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_2g = block_2g.find_element_by_css_selector(key_type_value_field)
            key_type_2g.click()
            ls_key_type_2g = key_type_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_2g:
                if o.get_attribute('option-value') == KEY_TYPE_2:
                    o.click()

            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g_hex = block_2g.find_element_by_css_selector(password_error_msg).text


            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            # 5G Change security
            security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            security_5g.click()
            ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_5g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_5g = driver.find_element_by_css_selector(right)
            # Encryption
            encryption_5g = block_5g.find_element_by_css_selector(encryption_value_field)
            encryption_5g.click()
            ls_encryption_5g = encryption_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_5g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_5g = block_5g.find_element_by_css_selector(key_type_value_field)
            key_type_5g.click()
            ls_key_type_5g = key_type_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_5g:
                if o.get_attribute('option-value') == KEY_TYPE_2:
                    o.click()

            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_5g_hex = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual7 = [error_msg_2g_hex, error_msg_5g_hex]
            list_expected7 = [exp_short_pw_error_msg]*2
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 7. Change Secirity, Encryption, Keytype  and password  of  2G/5G '
                                   f'Actual: {str(list_actual7)}. '
                                   f'Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Change Secirity, Encryption, Keytype  and password of  2G/5G . '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            list_step_fail.append('7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # 2G Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_5).perform()
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # 5G Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_5).perform()
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


            for i in PASSWORD_5:
                if (not i.isalpha()) and (not i.isnumeric()):
                    PASSWORD_5 = PASSWORD_5.replace(i, '')
            expected_pw = PASSWORD_5[:10]
            save_config(config_path, 'GENERAL', 'wifi_pw', expected_pw)

            list_actual8 = [pw_2g, pw_5g]
            list_expected8 = [expected_pw]*2
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual8)}. '
                                   f'Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual8)}. '
                f'Expected: {str(list_expected8)}')
            list_step_fail.append('8. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')

            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_2g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)


            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_5g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual9 = [check_2g, check_5g]
            list_expected9 = [return_true]*2

            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 9. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual9)}. '
                                   f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_09_Primary_Network_Verification_of_WEP128_setting(self):
        self.key = 'WIRELESS_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(120)
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
        SECURITY_TYPE = 'WEP'
        ENCRYPTION_TYPE = 'WEP128'
        KEY_TYPE = 'Character String'
        KEY_TYPE_2 = 'Hexadecimal'
        PASSWORD_3 = '123'
        PASSWORD_4 = '123!@aA123@!aA1'
        PASSWORD_5 = '1234567890aaaaaAAAAA123aaabbb'

        try:
            grand_login(driver)

            time.sleep(1)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # Default Pw
            block_2g = driver.find_element_by_css_selector(left)
            # 2G Change security
            security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            security_2g.click()
            ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_2g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_2g = driver.find_element_by_css_selector(left)
            # Encryption
            encryption_2g = block_2g.find_element_by_css_selector(encryption_value_field)
            encryption_2g.click()
            ls_encryption_2g = encryption_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_2g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_2g = block_2g.find_element_by_css_selector(key_type_value_field)
            key_type_2g.click()
            ls_key_type_2g = key_type_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_2g:
                if o.get_attribute('option-value') == KEY_TYPE:
                    o.click()

            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text


            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            # 5G Change security
            security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            security_5g.click()
            ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_5g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_5g = driver.find_element_by_css_selector(right)
            # Encryption
            encryption_5g = block_5g.find_element_by_css_selector(encryption_value_field)
            encryption_5g.click()
            ls_encryption_5g = encryption_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_5g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_5g = block_5g.find_element_by_css_selector(key_type_value_field)
            key_type_5g.click()
            ls_key_type_5g = key_type_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_5g:
                if o.get_attribute('option-value') == KEY_TYPE:
                    o.click()

            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual3 = [error_msg_2g, error_msg_5g]
            list_expected3 = [exp_short_pw_error_msg]*2
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Change Secirity, Encryption, Keytype  and password  of  2G/5G '
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change Secirity, Encryption, Keytype  and password of  2G/5G . '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
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

            expected_pw = PASSWORD_4[:13]
            save_config(config_path, 'GENERAL', 'wifi_pw', expected_pw)

            list_actual4 = [pw_2g, pw_5g]
            list_expected4 = [expected_pw]*2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Ma hoa mat khau
            byte_pw_2g = expected_pw.encode("utf8")
            hex_pw_2g = binascii.hexlify(byte_pw_2g)
            decode_pw_2g = hex_pw_2g.decode('utf8')
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_2g_default_val,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_5g_default_val,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true]*2

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)
            check_ota_auto_update(driver)

            time.sleep(1)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # Default Pw
            block_2g = driver.find_element_by_css_selector(left)
            # 2G Change security
            security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            security_2g.click()
            ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_2g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_2g = driver.find_element_by_css_selector(left)
            # Encryption
            encryption_2g = block_2g.find_element_by_css_selector(encryption_value_field)
            encryption_2g.click()
            ls_encryption_2g = encryption_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_2g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_2g = block_2g.find_element_by_css_selector(key_type_value_field)
            key_type_2g.click()
            ls_key_type_2g = key_type_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_2g:
                if o.get_attribute('option-value') == KEY_TYPE_2:
                    o.click()

            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g_hex = block_2g.find_element_by_css_selector(password_error_msg).text


            # Default Pw
            block_5g = driver.find_element_by_css_selector(right)
            # 5G Change security
            security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            security_5g.click()
            ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_security_5g:
                if o.get_attribute('option-value') == SECURITY_TYPE:
                    o.click()
                    break

            # Encryption
            block_5g = driver.find_element_by_css_selector(right)
            # Encryption
            encryption_5g = block_5g.find_element_by_css_selector(encryption_value_field)
            encryption_5g.click()
            ls_encryption_5g = encryption_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_encryption_5g:
                if o.get_attribute('option-value') == ENCRYPTION_TYPE:
                    o.click()
                    break

            # Key Type
            key_type_5g = block_5g.find_element_by_css_selector(key_type_value_field)
            key_type_5g.click()
            ls_key_type_5g = key_type_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_key_type_5g:
                if o.get_attribute('option-value') == KEY_TYPE_2:
                    o.click()

            # Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_5g_hex = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual7 = [error_msg_2g_hex, error_msg_5g_hex]
            list_expected7 = [exp_short_pw_error_msg]*2
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 7. Change Secirity, Encryption, Keytype  and password  of  2G/5G '
                                   f'Actual: {str(list_actual7)}. '
                                   f'Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Change Secirity, Encryption, Keytype  and password of  2G/5G . '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            list_step_fail.append('7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # 2G Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_5).perform()
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # 5G Change password
            pw_5g = block_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_5).perform()
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

            for i in PASSWORD_5:
                if (not i.isalpha()) and (not i.isnumeric()):
                    PASSWORD_5 = PASSWORD_5.replace(i, '')
            expected_pw = PASSWORD_5[:26]
            save_config(config_path, 'GENERAL', 'wifi_pw', expected_pw)

            list_actual8 = [pw_2g, pw_5g]
            list_expected8 = [expected_pw]*2
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual8)}. '
                                   f'Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual8)}. '
                f'Expected: {str(list_expected8)}')
            list_step_fail.append('8. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 9
        try:
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')

            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_2g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)


            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_5g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual9 = [check_2g, check_5g]
            list_expected9 = [return_true]*2

            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 9. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual9)}. '
                                   f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_10_Verification_of_Hide_SSID_function(self):
        self.key = 'WIRELESS_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(150)
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
        # Get mac
        URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        mac_2g = api_change_wifi_setting(URL_2g, get_only_mac=True)
        name_with_mac_2g = '_'.join(['wifi', mac_2g.replace(':', '_')])

        URL_5g = get_config('URL', 'url') + '/api/v1/wifi/1/ssid/0'
        mac_5g = api_change_wifi_setting(URL_5g, get_only_mac=True)
        name_with_mac_5g = '_'.join(['wifi', mac_5g.replace(':', '_')])

        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # 2G
            block_2g = driver.find_element_by_css_selector(left)
            # Hide SSID
            hide_ssid_2g = block_2g.find_elements_by_css_selector(select)[0]
            check_hide_ssid_2g = hide_ssid_2g.find_element_by_css_selector(input).is_selected() is False

            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            # Hide SSID
            hide_ssid_5g = block_5g.find_elements_by_css_selector(select)[0]
            check_hide_ssid_5g = hide_ssid_5g.find_element_by_css_selector(input).is_selected() is False

            list_actual = [check_hide_ssid_2g, check_hide_ssid_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Hide SSID of 2G/5G. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Enable Hide SSID of 2G/5G. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            hide_ssid_2g.click()
            time.sleep(0.2)
            dialog_title_2g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()

            # Change WF name for scan Wi-Fi
            block_2g = driver.find_element_by_css_selector(left)
            ssid_2g = block_2g.find_element_by_css_selector(ele_wl_ssid_value_field)
            ssid_2g.click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).send_keys(name_with_mac_2g).perform()
            time.sleep(2)

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
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()

            # Change WF name for scan Wi-Fi
            block_5g = driver.find_element_by_css_selector(right)
            ssid_5g = block_5g.find_element_by_css_selector(ele_wl_ssid_value_field)
            ssid_5g.click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).send_keys(name_with_mac_5g).perform()
            time.sleep(2)

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
            time.sleep(5)
            if name_with_mac_2g not in ls_current_wifi and name_with_mac_5g not in ls_current_wifi:
                check_wf = True

            list_actual = [check_wf]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Scan current wifi: Check 2G and 5G not in wifi list'
                                   f'Actual: {str(list_actual)}. '
                                   f'Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Scan current wifi: Check 2G and 5G not in wifi list. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')

            write_data_to_xml(wifi_default_file_path,
                              new_name=name_with_mac_2g)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{name_with_mac_2g}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{name_with_mac_2g}" name="{name_with_mac_2g}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path,
                              new_name=name_with_mac_5g)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{name_with_mac_5g}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{name_with_mac_5g}" name="{name_with_mac_5g}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true] * 2

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
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

    def test_15_Guest_Network_Multi_SSID_operation_check(self):
        self.key = 'WIRELESS_15'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # Factory reset

        URL_LOGIN = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(150)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')

        filename_2 = 'account1.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'
        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)

            # 2G
            ls_add_7_ssid_2g = list()
            for i in range(7):
                block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
                # Click Add
                block_2g.find_element_by_css_selector(add_class).click()
                time.sleep(0.5)
                # Check Default Value
                edit_2g_block = driver.find_element_by_css_selector(wl_primary_card)
                # Settings
                wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')

                edit_2g_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)

                ls_add_7_ssid_2g.append(wl_2g_ssid)

            # Check Can not add more than 7 Guest NW
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]

            check_add_7_nw_2g = block_2g.find_element_by_css_selector(add_class).is_enabled() is False

            list_actual1 = [check_add_7_nw_2g]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1,2. Add 7 Guest NW 2G. Check can not add more.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Add 7 Guest NW 2G. Check can not add more. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        try:
            random_guest_nw = random.choice(ls_add_7_ssid_2g)
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)

            os.system(f'netsh wlan delete profile name="{random_guest_nw}"')

            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == random_guest_nw:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break

            wl_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            guest_security = wl_2g_block.find_element_by_css_selector(secure_value_field).text
            if guest_security == 'None':
                write_data_to_none_secure_xml(wifi_none_secure_path, new_name=random_guest_nw)
                os.system(f'netsh wlan add profile filename="{wifi_none_secure_path}"')
            elif guest_security == 'WPA2/WPA-PSK':
                guest_encryption = wl_2g_block.find_element_by_css_selector(encryption_value_field).text
                guest_pw = wireless_check_pw_eye(driver, wl_2g_block)
                write_data_to_xml(default_wifi_2g_path,
                                  new_name=random_guest_nw,
                                  new_pw=guest_pw,
                                  new_secure='WPA2PSK',
                                  new_encryption=guest_encryption,
                                  new_key_type='passPhrase')
                os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')


            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{random_guest_nw}" name="{random_guest_nw}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            os.system(f'netsh wlan disconnect')
            time.sleep(2)

            list_actual3 = [check_2g]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Connect to Google using of  2G GUEST NW wifi. '
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)

            # 2G
            ls_add_7_ssid_5g = list()
            for i in range(7):
                block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
                # Click Add
                block_5g.find_element_by_css_selector(add_class).click()
                time.sleep(0.5)
                # Check Default Value
                edit_5g_block = driver.find_element_by_css_selector(wl_primary_card)
                # Settings
                wl_5g_ssid = wireless_get_default_ssid(edit_5g_block, 'Network Name(SSID)')

                edit_5g_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)

                ls_add_7_ssid_5g.append(wl_5g_ssid)

            # Check Can not add more than 7 Guest NW
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]

            check_add_7_nw_5g = block_5g.find_element_by_css_selector(add_class).is_enabled() is False

            list_actual14 = [check_add_7_nw_5g]
            list_expected4 = [return_true]
            check = assert_list(list_actual14, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] Re-do: 1,2. Add 7 Guest NW 5G. Check can not add more.'
                                   f'Actual: {str(list_actual14)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] Re-do: 1,2. Add 7 Guest NW 5G. Check can not add more. '
                f'Actual: {str(list_actual14)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append(
                'Re-do: 1,2. Assertion wong.')

        try:
            random_guest_nw = random.choice(ls_add_7_ssid_5g)
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            row_5g = block_5g.find_elements_by_css_selector(rows)

            os.system(f'netsh wlan delete profile name="{random_guest_nw}"')

            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == random_guest_nw:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break

            wl_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            guest_security = wl_5g_block.find_element_by_css_selector(secure_value_field).text
            if guest_security == 'None':
                write_data_to_none_secure_xml(wifi_none_secure_path, new_name=random_guest_nw)
                os.system(f'netsh wlan add profile filename="{wifi_none_secure_path}"')
            elif guest_security == 'WPA2/WPA-PSK':
                guest_encryption = wl_5g_block.find_element_by_css_selector(encryption_value_field).text
                guest_pw = wireless_check_pw_eye(driver, wl_5g_block)
                write_data_to_xml(default_wifi_2g_path,
                                  new_name=random_guest_nw,
                                  new_pw=guest_pw,
                                  new_secure='WPA2PSK',
                                  new_encryption=guest_encryption,
                                  new_key_type='passPhrase')
                os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{random_guest_nw}" name="{random_guest_nw}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            os.system(f'netsh wlan disconnect')
            time.sleep(2)

            list_actual5 = [check_5g]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] Re-do: 3. Connect to Google using of  5G GUEST NW wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] Re-do: 3. Connect to Google using of 5G GUEST NW wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('Re-do:3 . Assertion wong.')
            self.list_steps.append('[END TC]')

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

    def test_23_Guest_Network_Verification_of_WEP64_setting(self):
        self.key = 'WIRELESS_23'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(150)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')

        filename_2 = 'account1.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WEP'
        ENCRYPTION_TYPE = 'WEP64'
        KEY_TYPE = 'Character String'
        KEY_TYPE_2 = 'Hexadecimal'
        PASSWORD_3 = '123'
        PASSWORD_4 = '123@!12'
        PASSWORD_5 = '@!a1b2c3d4e5@!'
        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')

            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_5g_ssid = wireless_get_default_ssid(edit_5g_block, 'Network Name(SSID)')

            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check Add OK?
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)
            check_guest_2g = False
            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    check_guest_2g = True
                    break

            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            row_5g = block_5g.find_elements_by_css_selector(rows)
            check_guest_5g = False
            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    check_guest_5g = True
                    break

            list_actual1 = [check_guest_2g, check_guest_5g]
            list_expected1 = [return_true]*2
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1,2. Add a Guest 2G/5G Wireless successfully.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Add a Guest 2G/5G Wireless failure. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)

            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, key_type_value_field, KEY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_5g = block_5g.find_elements_by_css_selector(rows)

            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, key_type_value_field, KEY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual3 = [error_msg_2g, error_msg_5g]
            list_expected3 = [exp_short_pw_error_msg]*2
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check PW too short warning message of 2G/5G. '
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check PW too short warning message of 2G/5G. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Change PW again
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_4)
            # 2G
            pw_2g = wireless_check_pw_eye(driver, block_2g)
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_4)
            # 5G Pw
            pw_5g = wireless_check_pw_eye(driver, block_5g)
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            expected_pw = PASSWORD_4[:5]

            list_actual4 = [pw_2g, pw_5g]
            list_expected4 = [expected_pw] * 2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')
            # ~~~~~~~~~~~~~~~~ 5

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Ma hoa mat khau
            byte_pw_2g = expected_pw.encode("utf8")
            hex_pw_2g = binascii.hexlify(byte_pw_2g)
            decode_pw_2g = hex_pw_2g.decode('utf8')
            time.sleep(3)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Push to xml file
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_2g_ssid,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_2g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_5g_ssid,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_5g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            os.system(f'netsh wlan disconnect')
            time.sleep(1)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true] * 2

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')

            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_5g_ssid = wireless_get_default_ssid(edit_5g_block, 'Network Name(SSID)')

            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check Add OK?
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)
            check_guest_2g = False
            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    check_guest_2g = True
                    break

            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            row_5g = block_5g.find_elements_by_css_selector(rows)
            check_guest_5g = False
            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    check_guest_5g = True
                    break

            list_actual6 = [check_guest_2g, check_guest_5g]
            list_expected6 = [return_true]*2
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Re-do Step 1, 2: Add more 2G/5G guest.'
                                   f'Actual: {str(list_actual6)}. '
                                   f'Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Re-do Step 1, 2: Add more 2G/5G guest. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            list_step_fail.append(
                '6. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)

            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, key_type_value_field, KEY_TYPE_2)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_5g = block_5g.find_elements_by_css_selector(rows)

            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, key_type_value_field, KEY_TYPE_2)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual7 = [error_msg_2g, error_msg_5g]
            list_expected7 = [exp_short_pw_error_msg]*2
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 7. Check PW too short warning message of 2G/5G. '
                                   f'Actual: {str(list_actual7)}. '
                                   f'Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Check PW too short warning message of 2G/5G. '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            list_step_fail.append('7. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Change PW again
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_5)
            # 2G Pw
            pw_2g = wireless_check_pw_eye(driver, block_2g)
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_5)
            # 5G Pw
            pw_5g = wireless_check_pw_eye(driver, block_5g)
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            for i in PASSWORD_5:
                if (not i.isalpha()) and (not i.isnumeric()):
                    PASSWORD_5 = PASSWORD_5.replace(i, '')
            expected_pw_hex = PASSWORD_5[:10]

            list_actual8 = [pw_2g, pw_5g]
            list_expected8 = [expected_pw_hex] * 2
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual8)}. '
                                   f'Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual8)}. '
                f'Expected: {str(list_expected8)}')
            list_step_fail.append('8. Assertion wong.')

        try:

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Push to xml file
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_2g_ssid,
                              new_pw=expected_pw_hex.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_2g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g_hex = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_5g_ssid,
                              new_pw=expected_pw_hex.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_5g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g_hex = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            os.system(f'netsh wlan disconnect')
            time.sleep(1)

            list_actual9 = [check_2g_hex, check_5g_hex]
            list_expected9 = [return_true] * 2

            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 9. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual9)}. '
                                   f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_24_Guest_Network_Verification_of_WEP128_setting(self):
        self.key = 'WIRELESS_24'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(150)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')

        filename_2 = 'account1.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'
        SECURITY_TYPE = 'WEP'
        ENCRYPTION_TYPE = 'WEP128'
        KEY_TYPE = 'Character String'
        KEY_TYPE_2 = 'Hexadecimal'
        PASSWORD_3 = '123'
        PASSWORD_4 = '123!@aA123@!aA1'
        PASSWORD_5 = '1234567890aaaaaAAAAA123aaabbb'
        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')

            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_5g_ssid = wireless_get_default_ssid(edit_5g_block, 'Network Name(SSID)')

            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check Add OK?
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)
            check_guest_2g = False
            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    check_guest_2g = True
                    break

            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            row_5g = block_5g.find_elements_by_css_selector(rows)
            check_guest_5g = False
            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    check_guest_5g = True
                    break

            list_actual1 = [check_guest_2g, check_guest_5g]
            list_expected1 = [return_true] * 2
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1,2. Add a Guest 2G/5G Wireless successfully.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Add a Guest 2G/5G Wireless failure. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)

            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, key_type_value_field, KEY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_5g = block_5g.find_elements_by_css_selector(rows)

            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, key_type_value_field, KEY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual3 = [error_msg_2g, error_msg_5g]
            list_expected3 = [exp_short_pw_error_msg] * 2
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check PW too short warning message of 2G/5G. '
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check PW too short warning message of 2G/5G. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Change PW again
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_4)
            # 2G
            pw_2g = wireless_check_pw_eye(driver, block_2g)
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_4)
            # 5G Pw
            pw_5g = wireless_check_pw_eye(driver, block_5g)
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            expected_pw = PASSWORD_4[:13]

            list_actual4 = [pw_2g, pw_5g]
            list_expected4 = [expected_pw] * 2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')
            # ~~~~~~~~~~~~~~~~ 5

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Ma hoa mat khau
            byte_pw_2g = expected_pw.encode("utf8")
            hex_pw_2g = binascii.hexlify(byte_pw_2g)
            decode_pw_2g = hex_pw_2g.decode('utf8')
            time.sleep(3)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Push to xml file
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_2g_ssid,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_2g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_5g_ssid,
                              new_pw=decode_pw_2g,
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_5g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            os.system(f'netsh wlan disconnect')
            time.sleep(1)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true] * 2

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')

            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_5g_ssid = wireless_get_default_ssid(edit_5g_block, 'Network Name(SSID)')

            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check Add OK?
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)
            check_guest_2g = False
            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    check_guest_2g = True
                    break

            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            row_5g = block_5g.find_elements_by_css_selector(rows)
            check_guest_5g = False
            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    check_guest_5g = True
                    break

            list_actual6 = [check_guest_2g, check_guest_5g]
            list_expected6 = [return_true] * 2
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Re-do Step 1, 2: Add more 2G/5G guest.'
                                   f'Actual: {str(list_actual6)}. '
                                   f'Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Re-do Step 1, 2: Add more 2G/5G guest. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            list_step_fail.append(
                '6. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)

            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_change_choose_option(block_2g, key_type_value_field, KEY_TYPE_2)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_5g = block_5g.find_elements_by_css_selector(rows)

            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Secure
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, secure_value_field, SECURITY_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encryption
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, encryption_value_field, ENCRYPTION_TYPE)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Key Type
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g, key_type_value_field, KEY_TYPE_2)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Password
            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_3)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Check password error message
            error_msg_5g = block_5g.find_element_by_css_selector(password_error_msg).text

            list_actual7 = [error_msg_2g, error_msg_5g]
            list_expected7 = [exp_short_pw_error_msg] * 2
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 7. Check PW too short warning message of 2G/5G. '
                                   f'Actual: {str(list_actual7)}. '
                                   f'Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Check PW too short warning message of 2G/5G. '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            list_step_fail.append('7. Assertion wong.')

        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Change PW again
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=PASSWORD_5)
            # 2G Pw
            pw_2g = wireless_check_pw_eye(driver, block_2g)
            # Apply
            time.sleep(0.2)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=PASSWORD_5)
            # 5G Pw
            pw_5g = wireless_check_pw_eye(driver, block_5g)
            # Apply
            time.sleep(0.2)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            for i in PASSWORD_5:
                if (not i.isalpha()) and (not i.isnumeric()):
                    PASSWORD_5 = PASSWORD_5.replace(i, '')
            expected_pw_hex = PASSWORD_5[:26]

            list_actual8 = [pw_2g, pw_5g]
            list_expected8 = [expected_pw_hex] * 2
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8. Change password again of  2G/5G '
                                   f'Actual: {str(list_actual8)}. '
                                   f'Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Change password again chars of  2G/5G . '
                f'Actual: {str(list_actual8)}. '
                f'Expected: {str(list_expected8)}')
            list_step_fail.append('8. Assertion wong.')

        try:

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Push to xml file
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_2g_ssid,
                              new_pw=expected_pw_hex.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_2g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g_hex = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=wl_5g_ssid,
                              new_pw=expected_pw_hex.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wl_5g_ssid}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g_hex = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            os.system(f'netsh wlan disconnect')
            time.sleep(1)

            list_actual9 = [check_2g_hex, check_5g_hex]
            list_expected9 = [return_true] * 2

            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 9. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual9)}. '
                                   f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    # Buoc 5 Sai o connect vs 5G
    def test_25_Verification_of_Hide_SSID_action(self):
        self.key = 'WIRELESS_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        # time.sleep(10)
        # # Factory reset
        # URL_LOGIN = get_config('URL', 'url')
        # NEW_PASSWORD = 'abc123'
        # filename = '1'
        # commmand = 'factorycfg.sh -a'
        # run_cmd(commmand, filename=filename)
        # # Wait 5 mins for factory
        # time.sleep(150)
        # wait_DUT_activated(URL_LOGIN)
        # wait_ping('192.168.1.1')
        #
        # filename_2 = 'account1.txt'
        # commmand_2 = 'capitest get Device.Users.User.2. leaf'
        # run_cmd(commmand_2, filename_2)
        # time.sleep(3)
        # # Get account information from web server and write to config.txt
        # user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        GOOGLE_URL = 'http://google.com'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login((driver))
            # Enable Dual WAN
            goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            # 2G
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 2G
            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            # Click Add
            block_2g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')
            # Click Hide SSID
            edit_2g_block.find_elements_by_css_selector(select)[0].click()
            time.sleep(0.5)
            confirm_msg_2g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            # Apply
            edit_2g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Add Guest 5G
            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            # Click Add
            block_5g.find_element_by_css_selector(add_class).click()
            time.sleep(0.5)
            # Check Default Value
            edit_5g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
            # Settings
            wl_5g_ssid = wireless_get_default_ssid(edit_5g_block, 'Network Name(SSID)')
            # Click Hide SSID
            edit_5g_block.find_elements_by_css_selector(select)[0].click()
            time.sleep(0.5)
            confirm_msg_5g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            # Apply
            edit_5g_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

            list_actual = [confirm_msg_2g, confirm_msg_5g]
            list_expected = [exp_dialog_hide_ssid_title]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2 ,3. Enable Hide SSID: Check Confirm message. ')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2, 3. Enable Hide SSID: Check Confirm message. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
            list_step_fail.append('1, 2, 3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            time.sleep(5)
            ls_current_wifi = scan_wifi()
            check_wf = False
            time.sleep(5)
            if wl_2g_ssid not in ls_current_wifi and wl_5g_ssid not in ls_current_wifi:
                check_wf = True

            list_actual = [check_wf]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Scan current wifi: Check 2G and 5G not in wifi list'
                                   f'Actual: {str(list_actual)}. '
                                   f'Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Scan current wifi: Check 2G and 5G not in wifi list. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        try:

            block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
            row_2g = block_2g.find_elements_by_css_selector(rows)

            for r in row_2g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_2g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break

            wl_2g_block = driver.find_element_by_css_selector(wl_primary_card)
            guest_security_2g = wl_2g_block.find_element_by_css_selector(secure_value_field).text

            if guest_security_2g == 'WPA2/WPA-PSK':
                guest_encryption_2g = wl_2g_block.find_element_by_css_selector(encryption_value_field).text
                guest_pw_2g = wireless_check_pw_eye(driver, wl_2g_block)
            driver.find_element_by_css_selector(btn_cancel).click()

            block_5g = driver.find_elements_by_css_selector(guest_network_block)[1]
            row_5g = block_5g.find_elements_by_css_selector(rows)

            for r in row_5g:
                if r.find_element_by_css_selector(ele_wl_nw_name_ssid).text == wl_5g_ssid:
                    r.find_element_by_css_selector(edit_cls).click()
                    time.sleep(1)
                    break

            wl_5g_block = driver.find_element_by_css_selector(wl_primary_card)
            guest_security_5g = wl_5g_block.find_element_by_css_selector(secure_value_field).text

            if guest_security_5g == 'WPA2/WPA-PSK':
                guest_encryption_5g = wl_5g_block.find_element_by_css_selector(encryption_value_field).text
                guest_pw_5g = wireless_check_pw_eye(driver, wl_5g_block)
            driver.find_element_by_css_selector(btn_cancel).click()


            os.system(f'netsh wlan delete profile name="{wl_2g_ssid}"')
            os.system(f'netsh wlan delete profile name="{wl_5g_ssid}"')
            time.sleep(3)

            if guest_security_2g == 'None':
                write_data_to_none_secure_xml(wifi_none_secure_path, new_name=wl_2g_ssid)
                time.sleep(2)
                os.system(f'netsh wlan add profile filename="{wifi_none_secure_path}"')
            elif guest_security_2g == 'WPA2/WPA-PSK':
                write_data_to_xml(default_wifi_2g_path,
                                  new_name=wl_2g_ssid,
                                  new_pw=guest_pw_2g,
                                  new_secure='WPA2PSK',
                                  new_encryption=guest_encryption_2g,
                                  new_key_type='passPhrase')
                time.sleep(2)
                os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')

            time.sleep(5)
            # Connect Default 2GHz
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            os.system('netsh wlan disconnect')
            time.sleep(1)
            # 5G Connect wifi
            time.sleep(3)

            if guest_security_5g == 'None':
                write_data_to_none_secure_xml(wifi_none_secure_path, new_name=wl_5g_ssid)
                os.system(f'netsh wlan add profile filename="{wifi_none_secure_path}"')
            elif guest_security_5g == 'WPA2/WPA-PSK':
                write_data_to_xml(default_wifi_2g_path,
                                  new_name=wl_5g_ssid,
                                  new_pw=guest_pw_5g,
                                  new_secure='WPA2PSK',
                                  new_encryption=guest_encryption_5g,
                                  new_key_type='passPhrase')
                os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')

            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            os.system('netsh wlan disconnect')
            time.sleep(1)

            list_actual5 = [check_2g, check_5g]
            list_expected5 = [return_true] * 2
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Connect to Google using of  2G/5G wifi. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_40_WPS_Verify_Hide_SSID(self):
        self.key = 'WIRELESS_40'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system(f'python {nw_interface_path} -i Ethernet -a enable')
        time.sleep(10)
        os.system('netsh wlan disconnect')
        time.sleep(1)
        # Factory reset
        # URL_LOGIN = get_config('URL', 'url')
        # URL_PING_CHECK = '192.168.1.1'
        # filename = '1'
        # command = 'factorycfg.sh -a'
        # run_cmd(command, filename=filename)
        # time.sleep(150)
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

        # Get mac
        URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        mac_2g = api_change_wifi_setting(URL_2g, get_only_mac=True)
        name_with_mac_2g = '_'.join(['wifi', mac_2g.replace(':', '_')])

        URL_5g = get_config('URL', 'url') + '/api/v1/wifi/1/ssid/0'
        mac_5g = api_change_wifi_setting(URL_5g, get_only_mac=True)
        name_with_mac_5g = '_'.join(['wifi', mac_5g.replace(':', '_')])

        try:
            grand_login(driver)

            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            # 2G
            block_2g = driver.find_element_by_css_selector(left)
            # Hide SSID
            hide_ssid_2g = block_2g.find_elements_by_css_selector(select)[0]

            hide_ssid_2g.click()
            time.sleep(0.2)
            dialog_title_2g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()

            # Change WF name for scan Wi-Fi
            block_2g = driver.find_element_by_css_selector(left)
            ssid_2g = block_2g.find_element_by_css_selector(ele_wl_ssid_value_field)
            ssid_2g.click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).send_keys(name_with_mac_2g).perform()
            time.sleep(2)

            # Click Apply
            block_2g = driver.find_element_by_css_selector(left)
            time.sleep(0.5)

            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            check_hide_ssid_2g = hide_ssid_2g.find_element_by_css_selector(input).is_selected()


            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            # Hide SSID
            hide_ssid_5g = block_5g.find_elements_by_css_selector(select)[0]

            hide_ssid_5g.click()
            time.sleep(0.2)
            dialog_title_5g = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()

            # Change WF name for scan Wi-Fi
            block_5g = driver.find_element_by_css_selector(right)
            ssid_5g = block_5g.find_element_by_css_selector(ele_wl_ssid_value_field)
            ssid_5g.click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).send_keys(name_with_mac_5g).perform()
            time.sleep(2)

            # Click Apply
            block_5g = driver.find_element_by_css_selector(right)
            time.sleep(0.5)

            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            check_hide_ssid_5g = hide_ssid_5g.find_element_by_css_selector(input).is_selected()


            list_actual = [dialog_title_2g, dialog_title_5g, check_hide_ssid_2g, check_hide_ssid_5g]
            list_expected = [exp_dialog_hide_ssid_title] * 2 + [return_true] * 2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3.Check Enable Hide SSID of 2G/5G: Check popup title, enable hide ssid. ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Enable Hide SSID of 2G/5G: Check popup title, enable hide ssid. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')


        try:

            goto_menu(driver, wireless_tab, wireless_wps_tab)
            time.sleep(2)
            wps_form_text = driver.find_element_by_css_selector(ele_wl_wps_inform).text

            list_actual5 = [wps_form_text]
            list_expected5 = [exp_wps_red_message]

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5.Go to WPS: Check red message in WPS. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. 5.Go to WPS: Check red message in WPS. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
