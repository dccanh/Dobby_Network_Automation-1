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

class WIRELESS(unittest.TestCase):
    def setUp(self):
        try:
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            check_enable_ethernet()
            self.driver = webdriver.Chrome(driver_path)  # open chrome
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
            os.system('netsh wlan connect ssid=HVNWifi name=HVNWifi')
            time.sleep(1)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
            time.sleep(5)
            # Connect by LAN again
            os.system('netsh wlan disconnect')
            time.sleep(1)
        write_to_excel(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        self.driver.quit()
    # OK
    def test_02_WIRELESS_Verification_of_the_Wifi_On_off_operation(self):
        self.key = 'WIRELESS_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================
        SSID_NAME = get_config('WIRELESS', 'wl02_ssid_name', input_data_path)

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
            time.sleep(2)

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
    # OK
    def test_04_WIRELESS_Verification_of_the_setting_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================

        GOOGLE_URL = get_config('WIRELESS', 'wl04_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl04_security_type', input_data_path)
        PASSWORD_3 = get_config('WIRELESS', 'wl04_pw_3', input_data_path)
        PASSWORD_4 = get_config('WIRELESS', 'wl04_pw_4', input_data_path)

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
            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

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
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            # 2G Connect wifi
            connect_wifi(exp_ssid_2g_default_val, PASSWORD_4[:63])
            time.sleep(1)
            wifi_2g_connected = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            os.system(f'netsh wlan disconnect')
            connect_wifi(exp_ssid_5g_default_val, PASSWORD_4[:63])
            time.sleep(1)
            wifi_5g_connected = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0

            os.system(f'netsh wlan disconnect')
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

            list_actual5 = [wifi_2g_connected, check_2g, wifi_5g_connected, check_5g]
            list_expected5 = [exp_ssid_2g_default_val, return_true, exp_ssid_5g_default_val, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google successfully. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google successfully. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google fail. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google fail. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_05_WIRELESS_Verification_of_the_setting_WPA_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================
        GOOGLE_URL = get_config('WIRELESS', 'wl05_google_url', input_data_path)
        PASSWORD_3 = get_config('WIRELESS', 'wl05_pw_3', input_data_path)
        PASSWORD_4 = get_config('WIRELESS', 'wl05_pw_4', input_data_path)
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
            # # 2G Change security
            # security_2g = block_2g.find_element_by_css_selector(secure_value_field)
            # security_2g.click()
            # ls_security_2g = security_2g.find_elements_by_css_selector(secure_value_in_drop_down)
            # time.sleep(0.5)
            # for o in ls_security_2g:
            #     if o.get_attribute('option-value') == SECURITY_TYPE:
            #         o.click()
            #         break
            # Change password
            pw_2g = block_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_3).perform()

            error_msg_2g = block_2g.find_element_by_css_selector(password_error_msg).text

            # # 5G Change security
            # security_5g = block_5g.find_element_by_css_selector(secure_value_field)
            # security_5g.click()
            # ls_security_5g = security_5g.find_elements_by_css_selector(secure_value_in_drop_down)
            # time.sleep(0.5)
            # for o in ls_security_5g:
            #     if o.get_attribute('option-value') == SECURITY_TYPE:
            #         o.click()
            #         break
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
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            # 2G Connect wifi
            connect_wifi(exp_ssid_2g_default_val, PASSWORD_4[:63])
            time.sleep(3)
            wifi_2g_connected = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            os.system(f'netsh wlan disconnect')
            connect_wifi(exp_ssid_5g_default_val, PASSWORD_4[:63])
            time.sleep(3)
            wifi_5g_connected = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

            list_actual5 = [wifi_2g_connected, check_2g, wifi_5g_connected, check_5g]
            list_expected5 = [exp_ssid_2g_default_val, return_true, exp_ssid_5g_default_val, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google successfully. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google successfully. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google fail. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google fail. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_08_WIRELESS_Primary_Network_Verification_of_WEP64_setting(self):
        self.key = 'WIRELESS_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        # factory_dut()
        # ===========================================================
        GOOGLE_URL = get_config('WIRELESS', 'wl08_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl08_security_type', input_data_path)
        ENCRYPTION_TYPE = get_config('WIRELESS', 'wl08_encryption_type', input_data_path)
        KEY_TYPE = get_config('WIRELESS', 'wl08_key_type', input_data_path)
        KEY_TYPE_2 = get_config('WIRELESS', 'wl08_key_type_2', input_data_path)
        PASSWORD_3 = get_config('WIRELESS', 'wl08_pw_3', input_data_path)
        PASSWORD_4 = get_config('WIRELESS', 'wl08_pw_4', input_data_path)
        PASSWORD_5 = get_config('WIRELESS', 'wl08_pw_5', input_data_path)

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
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)
            wifi_connected_2g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(15)
            wifi_connected_5g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(5)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual5 = [wifi_connected_2g_name, check_2g, wifi_connected_5g_name, check_5g]
            list_expected5 = [exp_ssid_2g_default_val, return_true, exp_ssid_5g_default_val, return_true]

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google fail. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google fail. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google fail. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google fail. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~
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
            time.sleep(5)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_2g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            time.sleep(3)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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

    def test_09_WIRELESS_Primary_Network_Verification_of_WEP128_setting(self):
        self.key = 'WIRELESS_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        GOOGLE_URL = get_config('WIRELESS', 'wl07_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl07_security_type', input_data_path)
        ENCRYPTION_TYPE = get_config('WIRELESS', 'wl07_encryption_type', input_data_path)
        KEY_TYPE = get_config('WIRELESS', 'wl07_key_type', input_data_path)
        KEY_TYPE_2 = get_config('WIRELESS', 'wl07_key_type_2', input_data_path)
        PASSWORD_3 = get_config('WIRELESS', 'wl07_pw_3', input_data_path)
        PASSWORD_4 = get_config('WIRELESS', 'wl07_pw_4', input_data_path)
        PASSWORD_5 = get_config('WIRELESS', 'wl07_pw_5', input_data_path)

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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

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
            time.sleep(5)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_2g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(5)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            time.sleep(5)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')
            time.sleep(15)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path,
                              new_name=exp_ssid_5g_default_val,
                              new_pw=expected_pw.upper(),
                              new_secure='open',
                              new_encryption=SECURITY_TYPE,
                              new_key_type='networkKey')
            time.sleep(5)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            time.sleep(5)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(15)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

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

    def test_10_WIRELESS_Verification_of_Hide_SSID_function(self):
        self.key = 'WIRELESS_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
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
            time.sleep(5)
            write_data_to_xml(wifi_default_file_path,
                              new_name=name_with_mac_2g)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{name_with_mac_2g}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{name_with_mac_2g}" name="{name_with_mac_2g}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path,
                              new_name=name_with_mac_5g)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{name_with_mac_5g}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{name_with_mac_5g}" name="{name_with_mac_5g}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

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
    # OK
    def test_11_WIRELESS_Verification_of_WebUI_Access_Operation(self):
        self.key = 'WIRELESS_11'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================

        try:
            grand_login(driver)
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

            # pw_eye_2g = block_2g.find_element_by_css_selector(password_eye)
            # act = ActionChains(driver)
            # act.click_and_hold(pw_eye_2g)
            # pw_2g = block_2g.find_element_by_css_selector(input_pw).get_attribute('value')
            # act.release(pw_eye_2g)
            # act.perform()
            #
            # # 5G Pw
            # pw_eye_5g = block_5g.find_element_by_css_selector(password_eye)
            # act_5g = ActionChains(driver)
            # act_5g.click_and_hold(pw_eye_5g)
            # pw_5g = block_5g.find_element_by_css_selector(input_pw).get_attribute('value')
            # act_5g.release(pw_eye_5g)
            # act_5g.perform()

            list_actual = [check_web_access_2g, check_web_access_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check Default Web UI Access of 2G/5G. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            # change_nw_profile(wifi_2g_path, 'Password', pw_2g)
            # connect_wifi_from_xml(wifi_2g_path)
            write_data_to_xml(wifi_default_file_path,
                              new_name=exp_ssid_2g_default_val)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')

            time.sleep(15)
            driver.get(URL_LOGIN)
            wait_popup_disappear(driver, dialog_loading)
            check_2g = len(driver.find_elements_by_css_selector(lg_page)) != 0
            time.sleep(3)

            # Connect 5G > Access login page
            # change_nw_profile(wifi_5g_path, 'Password', pw_5g)
            # connect_wifi_from_xml(wifi_5g_path)
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path,
                              new_name=exp_ssid_5g_default_val)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')

            time.sleep(15)
            driver.get(URL_LOGIN)
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            check_5g = len(driver.find_elements_by_css_selector(lg_page)) != 0
            time.sleep(3)

            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Enable Web UI Access of 2G/5G: Check Access web UI successfully. '
                                   f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Enable Web UI Access of 2G/5G: Check Access web UI successfully.. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Disconnect Wifi to enable LAN
            os.system('netsh wlan disconnect')
            time.sleep(3)
            # Login
            grand_login(driver)

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
            # change_nw_profile(wifi_2g_path, 'Password', pw_2g)
            # connect_wifi_from_xml(wifi_2g_path)
            write_data_to_xml(wifi_default_file_path,
                              new_name=exp_ssid_2g_default_val)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_2g_default_val}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_2g_default_val}" name="{exp_ssid_2g_default_val}"')

            time.sleep(15)
            driver.get(URL_LOGIN)
            time.sleep(3)
            check_2g = len(driver.find_elements_by_css_selector(lg_page)) == 0
            time.sleep(3)

            # Connect 5G > Access login page
            # change_nw_profile(wifi_5g_path, 'Password', pw_5g)
            # connect_wifi_from_xml(wifi_5g_path)
            # 5G Connect wifi
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path,
                              new_name=exp_ssid_5g_default_val)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{exp_ssid_5g_default_val}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{exp_ssid_5g_default_val}" name="{exp_ssid_5g_default_val}"')
            time.sleep(15)

            driver.get(URL_LOGIN)
            time.sleep(3)
            check_5g = len(driver.find_elements_by_css_selector(lg_page)) == 0
            time.sleep(3)

            os.system('netsh wlan disconnect')
            list_actual = [check_2g, check_5g]
            list_expected = [return_true]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check Disable Web UI Access of 2G/5G: Check Access web UI fail. '
                                   f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Disable Web UI Access of 2G/5G: Check Access web UI fail. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_15_WIRELESS_Guest_Network_Multi_SSID_operation_check(self):
        self.key = 'WIRELESS_15'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # Factory reset

        URL_LOGIN = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'
        # ===========================================================
        factory_dut()
        # ===========================================================
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
            time.sleep(3)

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
                time.sleep(5)
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
                time.sleep(5)


            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{random_guest_nw}" name="{random_guest_nw}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
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
                time.sleep(5)
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
                time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{random_guest_nw}" name="{random_guest_nw}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            self.list_steps.append( '[Pass] Re-do: 3. Connect to Google using of  5G GUEST NW wifi. '
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
    # OK
    def test_16_WIRELESS_Check_SSID_setting(self):
        self.key = 'WIRELESS_16'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        SSID_TEST = get_config('WIRELESS', 'wl16_ssid_test', input_data_path)
        SSID_2G_DEFAULT_START = 'HUMAX_Guest_2G!_'
        SSID_5G_DEFAULT_START = 'HUMAX_Guest_5G!_'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        try:
            grand_login(driver)

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

            list_actual1 = [check_default_ssid_2g_value, changed_ssid_2g_value]
            list_expected1 = [return_true, SSID_TEST[:32]]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2. Check Default SSID and Changed SSID of 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Default SSID and Changed SSID of 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [check_default_ssid_5g_value, changed_ssid_5g_value]
            list_expected2 = [return_true, SSID_TEST[:32]]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check Default SSID and Changed SSID of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Default SSID and Changed SSID of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_17_WIRELESS_Verification_of_Guest_Network_Duplicate_SSID_Registration(self):
        self.key = 'WIRELESS_17'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================

        try:
            grand_login(driver)
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

            list_actual1 = [error_msg_2g]
            list_expected1 = [exp_dialog_add_same_ssid]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2. Check Add message same SSID of 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check Add same SSID of 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [error_msg_5g]
            list_expected2 = [exp_dialog_add_same_ssid]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check Add message same SSID of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Add message same SSID of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_19_WIRELESS_Verification_of_setting_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_19'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ==========================================================================
        GOOGLE_URL = get_config('WIRELESS', 'wl19_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl19_security_type', input_data_path)
        PASSWORD_SHORT_STR = get_config('WIRELESS', 'wl19_pw_short', input_data_path)
        PASSWORD_LONG_STR = get_config('WIRELESS', 'wl19_pw_long', input_data_path)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
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

            list_actual1 = [pw_default_2g, error_msg_2g, new_pw_2g]
            list_expected1 = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2. Change security type: Check Default Password and Message too short 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Change security type: Check Default Password and Message too short 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [pw_default_5g, error_msg_5g, new_pw_5g]
            list_expected2 = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3, 4. Change security type: Check Default Password and Message too short of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Change security type: Check Default Password and Message too short of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append(
                '3, 4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:

            write_data_to_xml(wifi_default_file_path,
                              new_name=default_ssid_2g_value,
                              new_pw=new_pw_2g,
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{default_ssid_2g_value}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{default_ssid_2g_value}" name="{default_ssid_2g_value}"')
            time.sleep(10)
            check_connected_2g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            write_data_to_xml(wifi_default_file_path,
                              new_name=default_ssid_5g_value,
                              new_pw=new_pw_5g,
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{default_ssid_5g_value}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{default_ssid_5g_value}" name="{default_ssid_5g_value}"')
            time.sleep(10)
            check_connected_5g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            os.system('netsh wlan disconnect')
            time.sleep(3)

            list_actual3 = [check_connected_2g_name, check_2g, check_connected_5g_name, check_5g]
            list_expected3 = [default_ssid_2g_value, return_true, default_ssid_5g_value, return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google successfully. '
                f'Connect Wifi 5G -> Check connect 2G wifi and access Google successfully. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Pass] 5. Connect Wifi 2G -> Check connect 2G wifi and access Google successfully. '
                f'Connect Wifi 5G -> Check connect 2G wifi and access Google successfully. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_20_WIRELESS_Verification_of_setting_WPA_WPA2_PSK_Password(self):
        self.key = 'WIRELESS_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        os.system('netsh wlan disconnect')

        # ==========================================================================
        GOOGLE_URL = get_config('WIRELESS', 'wl20_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl20_security_type', input_data_path)
        PASSWORD_SHORT_STR = get_config('WIRELESS', 'wl20_pw_short', input_data_path)
        PASSWORD_LONG_STR = get_config('WIRELESS', 'wl20_pw_long', input_data_path)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
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

            list_actual1 = [pw_default_2g, error_msg_2g, new_pw_2g]
            list_expected1 = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2. Change security type: Check Default Password and Message too short 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Change security type: Check Default Password and Message too short 2G. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [pw_default_5g, error_msg_5g, new_pw_5g]
            list_expected2 = [exp_wl_default_pw, exp_password_error_msg, PASSWORD_LONG_STR[:63]]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3, 4. Change security type: Check Default Password and Message too short of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Change security type: Check Default Password and Message too short of 5G. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append(
                '3, 4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            # Write to wifi xml file
            write_data_to_xml(wifi_default_file_path,
                              new_name=default_ssid_2g_value,
                              new_pw=new_pw_2g,
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{default_ssid_2g_value}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{default_ssid_2g_value}" name="{default_ssid_2g_value}"')
            time.sleep(10)
            check_connected_2g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_2g = len(driver.find_elements_by_css_selector(google_img)) > 0

            # 5G Connect wifi
            write_data_to_xml(wifi_default_file_path,
                              new_name=default_ssid_5g_value,
                              new_pw=new_pw_5g,
                              new_secure='WPA2PSK')
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{default_ssid_5g_value}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{default_ssid_5g_value}" name="{default_ssid_5g_value}"')
            time.sleep(10)
            check_connected_5g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            os.system('netsh wlan disconnect')

            list_actual3 = [check_connected_2g_name, check_2g, check_connected_5g_name, check_5g]
            list_expected3 = [default_ssid_2g_value, return_true, default_ssid_5g_value, return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Connect to Google using of  2G/5G wifi. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_23_WIRELESS_Guest_Network_Verification_of_WEP64_setting(self):
        self.key = 'WIRELESS_23'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        GOOGLE_URL = get_config('WIRELESS', 'wl23_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl23_security_type', input_data_path)
        ENCRYPTION_TYPE = get_config('WIRELESS', 'wl23_encryption_type', input_data_path)
        KEY_TYPE = get_config('WIRELESS', 'wl23_key_type', input_data_path)
        KEY_TYPE_2 = get_config('WIRELESS', 'wl23_key_type_2', input_data_path)
        PASSWORD_3 = get_config('WIRELESS', 'wl23_pw_3', input_data_path)
        PASSWORD_4 = get_config('WIRELESS', 'wl23_pw_4', input_data_path)
        PASSWORD_5 = get_config('WIRELESS', 'wl23_pw_5', input_data_path)

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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(5)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(5)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
    # OK
    def test_24_WIRELESS_Guest_Network_Verification_of_WEP128_setting(self):
        self.key = 'WIRELESS_24'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================

        GOOGLE_URL = get_config('WIRELESS', 'wl24_google_url', input_data_path)
        SECURITY_TYPE = get_config('WIRELESS', 'wl24_security_type', input_data_path)
        ENCRYPTION_TYPE = get_config('WIRELESS', 'wl24_encryption_type', input_data_path)
        KEY_TYPE = get_config('WIRELESS', 'wl24_key_type', input_data_path)
        KEY_TYPE_2 = get_config('WIRELESS', 'wl24_key_type_2', input_data_path)
        PASSWORD_3 = get_config('WIRELESS', 'wl24_pw_3', input_data_path)
        PASSWORD_4 = get_config('WIRELESS', 'wl24_pw_4', input_data_path)
        PASSWORD_5 = get_config('WIRELESS', 'wl24_pw_5', input_data_path)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)

            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_2g_ssid}" name="{wl_2g_ssid}"')
            time.sleep(10)
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(2)
            check_connected_2g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wl_5g_ssid}" name="{wl_5g_ssid}"')
            time.sleep(10)
            check_connected_5g_name = current_connected_wifi()
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
            check_5g_hex = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            os.system(f'netsh wlan disconnect')
            time.sleep(1)

            list_actual9 = [check_connected_2g_name, check_2g_hex, check_connected_5g_name, check_5g_hex]
            list_expected9 = [wl_2g_ssid, return_true, wl_5g_ssid, return_true]

            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 9. Connect Wifi 2G -> Check connect 2G wifi and access Google successfully. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google successfully. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Connect Wifi 2G -> Check connect 2G wifi and access Google successfully. '
                f'Connect Wifi 5G -> Check connect 5G wifi and access Google successfully. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_25_WIRELESS_Verification_of_Hide_SSID_action(self):
        self.key = 'WIRELESS_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        factory_dut()
        # ===========================================================
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
            time.sleep(3)
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
            time.sleep(3)
            # Google
            driver.get(GOOGLE_URL)
            time.sleep(10)
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
            time.sleep(10)
            check_5g = len(driver.find_elements_by_css_selector(google_img)) > 0
            # Enable
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
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
    # OK
    def test_36_WIRELESS_Verification_of_WPS_Not_Support_WEB(self):
        self.key = 'WIRELESS_36'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =================================================
        PASSWORD_WL = get_config('WIRELESS', 'wl36_pw', input_data_path)
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            # 2G
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Radio':
                    current_radio_status = v.find_element_by_css_selector(input)
                    if not current_radio_status.is_selected():
                        v.find_element_by_css_selector(select).click()

                        block_2g = driver.find_element_by_css_selector(left)
                        block_2g.find_element_by_css_selector(apply).click()
                        wait_popup_disappear(driver, dialog_loading)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)

                    check_radio_2g = block_2g.find_element_by_css_selector(input).is_selected()
                    break

            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            labels = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Radio':
                    current_radio_status = v.find_element_by_css_selector(input)
                    if not current_radio_status.is_selected():
                        v.find_element_by_css_selector(select).click()

                        block_5g = driver.find_element_by_css_selector(left)
                        block_5g.find_element_by_css_selector(apply).click()
                        wait_popup_disappear(driver, dialog_loading)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)

                    check_radio_5g = block_5g.find_element_by_css_selector(input).is_selected()
                    break

            list_actual2 = [check_radio_2g, check_radio_5g]
            list_expected2 = [return_true] * 2
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Enable Radio of 2G/5G: Check Radio of 2G/5G enabled. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Enable Radio of 2G/5G: Check Radio of 2G/5G enabled. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(2)
            # Change Security to WEB
            block_wl_2g = driver.find_element_by_css_selector(left)
            wireless_change_choose_option(block_wl_2g, secure_value_field, 'WEP')

            block_wl_5g = driver.find_element_by_css_selector(right)
            wireless_change_choose_option(block_wl_5g, secure_value_field, 'WEP')

            block_wl_2g = driver.find_element_by_css_selector(left)
            pw_2g = block_wl_2g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_2g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_WL).perform()
            # Apply
            apply_2g = block_wl_2g.find_element_by_css_selector(apply)
            if apply_2g.is_enabled() and apply_2g.is_displayed():
                time.sleep(0.2)
                block_wl_2g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(2)

            # 5G Change password
            block_wl_5g = driver.find_element_by_css_selector(right)
            pw_5g = block_wl_5g.find_element_by_css_selector(input_pw)
            ActionChains(driver).move_to_element(pw_5g).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_WL).perform()
            # Apply
            apply_5g = block_wl_5g.find_element_by_css_selector(apply)
            if apply_5g.is_enabled() and apply_5g.is_displayed():
                time.sleep(0.2)
                block_wl_5g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(2)

            block_2g = driver.find_element_by_css_selector(left)
            check_values_security_2g = block_2g.find_element_by_css_selector(secure_value_field).text

            block_5g = driver.find_element_by_css_selector(right)
            check_values_security_5g = block_5g.find_element_by_css_selector(secure_value_field).text

            list_actual4 = [check_values_security_2g, check_values_security_5g]
            list_expected4 = ['WEP'] * 2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change Security: Check Change successfully. '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Security: Check Change successfully. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            goto_menu(driver, wireless_tab, wireless_wps_tab)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_wps_button).click()
            time.sleep(1)
            check_error_msg = driver.find_element_by_css_selector(err_dialog_msg_cls).text

            list_actual5 = [check_error_msg]
            list_expected5 = [exp_wps_error_msg]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Goto Wireless > WPS. Click WPS. Check confirm message. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Goto Wireless > WPS. Click WPS. Check confirm message. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_40_WIRELESS_WPS_Verify_Hide_SSID(self):
        self.key = 'WIRELESS_40'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

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
                f'[Pass] 1, 2, 3, 4.Check Enable Hide SSID of 2G/5G: Check popup title, enable hide ssid. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2, 3, 4. Check Enable Hide SSID of 2G/5G: Check popup title, enable hide ssid. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2, 3, 4. Assertion wong.')


        try:
            goto_menu(driver, wireless_tab, wireless_wps_tab)
            time.sleep(2)
            wps_form_text = driver.find_element_by_css_selector(ele_wl_wps_inform).text

            list_actual5 = [wps_form_text]
            list_expected5 = [exp_wps_red_message]

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Go to WPS: Check red message in WPS. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Go to WPS: Check red message in WPS. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_49_WIRELESS_Advanced_Wireless_24G_Radio_On_Off(self):
        self.key = 'WIRELESS_49'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        #
        URL_LOGIN = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'
        # ===========================================================
        factory_dut()
        # ===========================================================
        save_config(config_path, 'URL', 'url', get_config('URL', 'sub_url'))
        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/0/radio'
        _BODY = ''
        _METHOD = 'GET'

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Radio':
                    default_radio = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Channel':
                    default_channel = v.find_element_by_css_selector(ele_channel_field).text.lower()
                    continue
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed).text.lower()
                    continue
                if l.text == 'Bandwidth':
                    default_bandwidth = v.find_element_by_css_selector(ele_bandwidth_field).text.lower()
                    continue
                if l.text == 'Sideband':
                    default_sideband = v.find_element_by_css_selector(ele_sideband_field).text.lower()
                    continue
                if l.text == '802.11n Protection':
                    default_80211_protection = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Short Guard Interval':
                    default_short_guard_interval = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'WMM':
                    default_wmm = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Beamforming':
                    default_beamforming = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Output Power':
                    default_output_power = v.find_element_by_css_selector(ele_output_power_filed).text.lower()
                    continue
                if l.text == 'Beacon Interval':
                    default_beacon = v.find_element_by_css_selector(input).get_attribute('value')
                    continue
                if l.text == 'DTIM Interval':
                    default_dtim = v.find_element_by_css_selector(input).get_attribute('value')
            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)
            api_active = _res['active']
            api_wl_mode = _res['basic']['wirelessMode']
            api_bandwidth = _res['basic']['bandwidth']['set']
            api_sideband = _res['basic']['sideband']
            api_output_power = _res['basic']['outputPower']
            api_channel = _res['basic']['channel']['set']
            api_short_guard = _res['advanced']['shortGuardInterval'] == 'on'
            api_beacon = str(_res['advanced']['beaconInterval'])
            api_dtim = str(_res['advanced']['dtimInterval'])
            api_protection = _res['advanced']['802dot11Protection']
            api_beamforming = _res['advanced']['beamforming']
            api_wmm = _res['wmm']['active']

            list_actual2 = [api_active, api_wl_mode, api_bandwidth, api_sideband,
                            api_output_power, api_channel, api_short_guard, api_beacon,
                            api_dtim, api_protection, api_beamforming, api_wmm]
            list_expected2 = [default_radio, default_wireless_mode,
                              default_bandwidth, default_sideband,
                              default_output_power, default_channel, default_short_guard_interval, default_beacon,
                              default_dtim, default_80211_protection, default_beamforming, default_wmm]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.0 Check API response: '
                f'API active, wireless mode, bandwidth, sideband, output power, channel, '
                f'short guard, beacon, dtim, 802dot11Protection, beamforming, wmm. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.0 Check API response: '
                f'API active, wireless mode, bandwidth, sideband, output power, channel, '
                f'short guard, beacon, dtim, 802dot11Protection, beamforming, wmm. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            # Connect 2.4GHz wifi
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            block_wl_2g = driver.find_element_by_css_selector(left)
            default_2g_ssid = wireless_get_default_ssid(block_wl_2g, 'Network Name(SSID)')
            default_2g_pw = wireless_check_pw_eye(driver, block_wl_2g, change_pw=False)
            # Connect wifi
            time.sleep(1)
            connect_wifi(default_2g_ssid, default_2g_pw)
            time.sleep(2)
            connected_wifi_name = current_connected_wifi()

            list_actual3 = [connected_wifi_name]
            list_expected3 = [default_2g_ssid]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.2 Connect Wifi 2.4GHz. Check Connect successfully'
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.2 Connect Wifi 2.4GHz. Check Connect successfully. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3.2 Assertion wong.')

        try:
            goto_menu(driver, advanced_tab, advanced_wireless_tab)
            wait_popup_disappear(driver, dialog_loading)

            block_2g = driver.find_element_by_css_selector(left)
            choose_specific_radio_box(block_2g, 'Radio', check=False)
            # Apply
            block_2g.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)
            if block_2g.find_element_by_css_selector(apply).is_displayed():
                block_2g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Radio':
                    get_radio = v.find_element_by_css_selector(input).is_selected()
                    break
            time.sleep(1)
            # block_2g.find_element_by_css_selector(apply).click()
            # if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
            #     time.sleep(1)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)
            # if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
            #     time.sleep(1)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)

            list_actual4 = [get_radio]
            list_expected4 = [return_false]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change Security: Check Change  Radio to OFF successfully. '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Security: Check Change  Radio to OFF successfully. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(1)
            api_active = _res['active']

            # Goto Wireless Primary Network
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            time.sleep(1)
            block_wl_2g = driver.find_element_by_css_selector(left)
            check_block_2g_have_no_content = len(block_wl_2g.find_elements_by_css_selector(adv_wl_radio_row)) == 0

            list_actual5 = [api_active, check_block_2g_have_no_content]
            list_expected5 = [return_false, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check disable Radio in API and Wireless 2G have no content. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check disable Radio in API and Wireless 2G have no content. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_50_WIRELESS_Advanced_Wireless_24G_80211_Mode(self):
        self.key = 'WIRELESS_50'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================
        save_config(config_path, 'URL', 'url', get_config('URL', 'sub_url'))
        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/0/radio'
        _BODY = ''
        _METHOD = 'GET'

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text = default_wireless_mode.text.lower()
                    # Get total supported modes
                    default_wireless_mode.click()

                    dropdown_values = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    dropdown_values_text = [i.get_attribute('option-value') for i in dropdown_values]
                    for o in dropdown_values:
                        if o.get_attribute('option-value') == '802.11b':
                            o.click()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode = _res['basic']['wirelessMode']

            list_expected3 = [default_wireless_mode_text, dropdown_values_text]
            list_actual3 = [api_wl_mode, ['802.11b', '802.11b+g', '802.11b+g+n']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check Default Wireless mode and list options supported. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Default Wireless mode and list options supported. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            # Connect 2.4GHz wifi
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text_4 = default_wireless_mode.text.lower()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode_4 = _res['basic']['wirelessMode']

            list_actual4 = [default_wireless_mode_text_4]
            list_expected4 = [api_wl_mode_4]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Change Wireless Mode to 802.11b. Check change successfully. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Wireless Mode to 802.11b. Check change successfully. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    # Get total supported modes
                    default_wireless_mode.click()

                    time.sleep(1)
                    dropdown_values = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in dropdown_values:
                        if o.get_attribute('option-value') == '802.11b+g':
                            o.click()
                    break
            # Connect 2.4GHz wifi
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text_5 = default_wireless_mode.text.lower()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode_5 = _res['basic']['wirelessMode']

            list_actual5 = [default_wireless_mode_text_5]
            list_expected5 = [api_wl_mode_5]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Change Wireless Mode to 802.11b+g. Check change successfully. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Change Wireless Mode to 802.11b+g. Check change successfully. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        try:
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    # Get total supported modes
                    default_wireless_mode.click()

                    time.sleep(1)
                    dropdown_values = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in dropdown_values:
                        if o.get_attribute('option-value') == '802.11b+g+n':
                            o.click()
                    break
            # Connect 2.4GHz wifi
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text_6 = default_wireless_mode.text.lower()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode_6 = _res['basic']['wirelessMode']

            list_actual6 = [default_wireless_mode_text_6]
            list_expected6 = [api_wl_mode_6]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Change Wireless Mode to 802.11b+g+n. Check change successfully. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Change Wireless Mode to 802.11b+g+n. Check change successfully. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_62_WIRELESS_Advanced_Wireless_24G_Verify_Scan_AP(self):
        self.key = 'WIRELESS_62'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =================================================
        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/0/scanResult'
        _BODY = ''
        _METHOD = 'GET'
        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            # 2G
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            block_2g.find_element_by_css_selector(ele_button_scan).click()
            wait_popup_disappear(driver, icon_loading)

            popup = driver.find_element_by_css_selector(dialog_content)
            # Check UI
            popup_title = popup.find_element_by_css_selector(ele_scan_title).text
            popup_refresh_button = len(popup.find_elements_by_css_selector(ele_btn_refresh)) > 0

            # Click to button List
            popup.find_element_by_css_selector(ele_button_list).click()
            check_list_wf = len(popup.find_elements_by_css_selector(ele_wifi_table)) > 0
            time.sleep(0.5)
            # CLick button Chart
            popup.find_element_by_css_selector(ele_button_chart).click()
            check_chart_wf = len(popup.find_elements_by_css_selector(ele_wifi_chart)) > 0

            # Check Close button
            check_btn_close_display = popup.find_element_by_css_selector(ele_btn_close).text

            list_actual2 = [popup_title, popup_refresh_button, check_list_wf, check_chart_wf, check_btn_close_display]
            list_expected2 = ['Nearby Wireless Access Points (2.4GHz)', return_true, return_true, return_true, 'Close']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.0 Check popup scan components: Title, Refresh, List table, Chart table, Close button. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.0 Check popup scan components: Title, Refresh, List table, Chart table, Close button. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('3.0 Assertion wong.')

        try:
            popup.find_element_by_css_selector(ele_button_list).click()
            time.sleep(1)
            # ==================================================
            _TOKEN = get_token(_USER, _PW)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)

            api_ssid = _res[0]['ssid']
            api_channel = _res[0]['channel']
            api_rssi = _res[0]['rssi']
            api_security = _res[0]['security']
            api_mac_address = _res[0]['macAddress']
            # ==================================================
            list_rows = driver.find_elements_by_css_selector(row_table)
            if len(list_rows) > 1:
                for r in list_rows[1:]:
                    get_row_mac = r.find_element_by_css_selector('td:last-child').text
                    if get_row_mac == api_mac_address:
                        get_nw_name = r.find_element_by_css_selector(ele_table_nw_ssid_name).text
                        get_channel = r.find_element_by_css_selector(ele_table_channel).text
                        get_rssi = r.find_element_by_css_selector(ele_table_rssi).text
                        get_security = r.find_element_by_css_selector(ele_table_security).text
                        break

                list_actual3 = [api_ssid, api_channel, api_rssi, api_security, api_mac_address]
                list_expected3 = [get_nw_name, get_channel, get_rssi, get_security, get_row_mac]
            else:
                list_actual3 = []
                list_expected3 = []

            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.2 Check one of wifi scaned information with api: SSID, Channel, RSSI, Security, MAC. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.2 Check one of wifi scaned information with api: SSID, Channel, RSSI, Security, MAC. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3.2 Assertion wong.')

        try:
            # Click Graph
            popup = driver.find_element_by_css_selector(dialog_content)
            popup.find_element_by_css_selector(ele_btn_refresh).click()

            check_scan_load = wait_visible(driver, icon_loading)
            wait_popup_disappear(driver, icon_loading)
            check_list_wf_refresh = len(popup.find_elements_by_css_selector(ele_wifi_table)) > 0

            list_actual4 = [check_scan_load, check_list_wf_refresh]
            list_expected4 = [return_true] * 2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click Refresh button. Check icon scan loading, Table list displayed.  '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click Refresh button. Check icon scan loading, Table list displayed.. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            popup = driver.find_element_by_css_selector(dialog_content)

            popup.find_element_by_css_selector(ele_button_chart).click()
            time.sleep(1)
            check_chart_wf = len(popup.find_elements_by_css_selector(ele_wifi_chart)) > 0

            list_actual5 = [check_chart_wf]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Click Chart button. Check Graph chart displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Click Chart button. Check Graph chart displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append('5 Assertion wong.')

        try:
            # Click Refresh
            popup.find_element_by_css_selector(ele_btn_refresh).click()
            time.sleep(1)
            check_scan_load = wait_visible(driver, icon_loading)
            wait_popup_disappear(driver, icon_loading)

            check_chart_wf_refresh = len(popup.find_elements_by_css_selector(ele_wifi_chart)) > 0

            list_actual6 = [check_scan_load, check_chart_wf_refresh]
            list_expected6 = [return_true]*2
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Click Refresh button. Check icon scan loading, Table Graph Chart displayed.  '
                 f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Click Refresh button. Check icon scan loading, Table Graph Chart displayed. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            list_step_fail.append('6. Assertion wong.')

        try:
            # Click Close
            popup.find_element_by_css_selector(ele_btn_close).click()
            time.sleep(1)
            popup_scan = len(driver.find_elements_by_css_selector(dialog_content)) == 0
            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual7 = [popup_scan, page_title_text]
            list_expected7 = [return_true, 'Advanced > Wireless']
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Click Close button. Check popup disappear, Page Advanced > Wireless display.  '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Click Close button. Check popup disappear, Page Advanced > Wireless display. '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_63_WIRELESS_Advanced_Wireless_24G_Verify_Restore_Default_operation(self):
        self.key = 'WIRELESS_63'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =================================================
        CHANNEL = '1'
        WIRELESS_MODE = '802.11b+g'
        OUTPUT_POWER = 'Medium'
        BEACON = '50'
        DTIM = '3'
        CHECK_WMM = False
        CHECK_BEAMFORMING = False

        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/0/radio'
        _BODY = ''
        _METHOD = 'GET'
        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            # 2G
            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Channel':
                    choose_specific_value_from_dropdown(block_2g, ele_channel_field, CHANNEL)

                if l.text == 'Wireless Mode':
                    choose_specific_value_from_dropdown(block_2g, ele_wireless_mode_filed, WIRELESS_MODE)

                if l.text == 'WMM':
                    choose_specific_radio_box(block_2g, l.text, check=CHECK_WMM)

                if l.text == 'Beamforming':
                    choose_specific_radio_box(block_2g, l.text, check=CHECK_BEAMFORMING)

                if l.text == 'Output Power':
                    choose_specific_value_from_dropdown(block_2g, ele_output_power_filed, OUTPUT_POWER)

                if l.text == 'Beacon Interval':
                    for i in range(2):
                        ActionChains(driver).move_to_element(l).perform()
                        beacon = block_2g.find_element_by_css_selector(ele_beacon_cls)
                        beacon_value = beacon.find_element_by_css_selector(input)
                        beacon_value.clear()
                        beacon_value.send_keys(BEACON)

                if l.text == 'DTIM Interval':
                    for i in range(2):
                        ActionChains(driver).move_to_element(l).perform()
                        dtim_value = v.find_element_by_css_selector(input)
                        dtim_value.clear()
                        dtim_value.send_keys(DTIM)
                    break

            block_2g = driver.find_element_by_css_selector(left)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)


            _TOKEN = get_token(_USER, _PW)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)

            api_active = _res['active']
            api_channel = _res['basic']['channel']['set']
            api_wl_mode = _res['basic']['wirelessMode']
            api_wmm = _res['wmm']['active']
            api_beamforming = _res['advanced']['beamforming']
            api_output_power = _res['basic']['outputPower'].capitalize()
            api_beacon = str(_res['advanced']['beaconInterval'])
            api_dtim = str(_res['advanced']['dtimInterval'])

            list_actual3 = [api_active, api_channel, api_wl_mode, api_wmm,
                            api_beamforming, api_output_power, api_beacon, api_dtim]
            list_expected3 = [return_true, CHANNEL, WIRELESS_MODE, CHECK_WMM,
                              CHECK_BEAMFORMING, OUTPUT_POWER, BEACON, DTIM]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Change 2.4 GHz: Channel, Wireless Mode, WMM, Beamforming, Output Power, Beacon, DTIM. '
                f'Check change successfully with api. Check api active and above option. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change 2.4 GHz: Channel, Wireless Mode, WMM, Beamforming, Output Power, Beacon, DTIM. '
                f'Check change successfully with api. Check api active and above option. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            block_2g = driver.find_element_by_css_selector(left)
            # Click 2GHz Restore
            block_2g.find_element_by_css_selector(ele_button_restore).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            block_2g = driver.find_element_by_css_selector(left)
            # Action
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Radio':
                    default_radio = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Channel':
                    default_channel = v.find_element_by_css_selector(ele_channel_field).text.lower()
                    continue
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed).text.lower()
                    continue
                if l.text == 'Bandwidth':
                    default_bandwidth = v.find_element_by_css_selector(ele_bandwidth_field).text.lower()
                    continue
                if l.text == 'Sideband':
                    default_sideband = v.find_element_by_css_selector(ele_sideband_field).text.lower()
                    continue
                if l.text == '802.11n Protection':
                    default_80211_protection = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Short Guard Interval':
                    default_short_guard_interval = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'WMM':
                    default_wmm = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Beamforming':
                    default_beamforming = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Output Power':
                    default_output_power = v.find_element_by_css_selector(ele_output_power_filed).text.lower()
                    continue
                if l.text == 'Beacon Interval':
                    default_beacon = v.find_element_by_css_selector(input).get_attribute('value')
                    continue
                if l.text == 'DTIM Interval':
                    default_dtim = v.find_element_by_css_selector(input).get_attribute('value')


            _TOKEN4 = get_token(_USER, _PW)
            _res4 = call_api(_URL_API, _METHOD, _BODY, _TOKEN4)

            api_active_4 = _res4['active']
            api_wl_mode_4 = _res4['basic']['wirelessMode']
            api_bandwidth_4 = _res4['basic']['bandwidth']['set']
            api_sideband_4 = _res4['basic']['sideband']
            api_output_power_4 = _res4['basic']['outputPower']
            api_channel_4 = _res4['basic']['channel']['set']
            api_short_guard_4 = _res4['advanced']['shortGuardInterval'] == 'on'
            api_beacon_4 = str(_res4['advanced']['beaconInterval'])
            api_dtim_4 = str(_res4['advanced']['dtimInterval'])
            api_protection_4 = _res4['advanced']['802dot11Protection']
            api_beamforming_4 = _res4['advanced']['beamforming']
            api_wmm_4 = _res4['wmm']['active']

            list_actual4 = [check_confirm_msg, api_active_4, api_wl_mode_4, api_bandwidth_4, api_sideband_4,
                            api_output_power_4, api_channel_4, api_short_guard_4, api_beacon_4,
                            api_dtim_4, api_protection_4, api_beamforming_4, api_wmm_4]
            list_expected4 = [exp_advance_restore_confirm_msg, default_radio, default_wireless_mode, default_bandwidth, default_sideband,
                              default_output_power, default_channel, default_short_guard_interval, default_beacon,
                              default_dtim, default_80211_protection, default_beamforming, default_wmm]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click Restore. Check restore confirm message. Check API restored: '
                f'API active, wireless mode, bandwidth, sideband, output power, channel, '
                f'short guard, beacon, dtim, 802dot11Protection, beamforming, wmm. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click Restore. Check restore confirm message. Check API restored: '
                f'API active, wireless mode, bandwidth, sideband, output power, channel, '
                f'short guard, beacon, dtim, 802dot11Protection, beamforming, wmm. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')

            list_step_fail.append('4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
    # OK
    def test_64_WIRELESS_Advanced_Wireless_5G_Radio_On_Off(self):
        self.key = 'WIRELESS_64'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        save_config(config_path, 'URL', 'url', get_config('URL', 'sub_url'))
        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/1/radio'
        _BODY = ''
        _METHOD = 'GET'

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_5 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_5 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_5, values_5):
                if l.text == 'Radio':
                    default_radio = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Channel':
                    default_channel = v.find_element_by_css_selector(ele_channel_field).text.lower()
                    continue
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed).text.lower()
                    continue
                if l.text == 'Bandwidth':
                    default_bandwidth = v.find_element_by_css_selector(ele_bandwidth_field).text.lower()
                    continue
                if l.text == 'Short Guard Interval':
                    default_short_guard_interval = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'WMM':
                    default_wmm = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Beamforming':
                    default_beamforming = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'MU-MIMO':
                    default_mumimo = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Output Power':
                    default_output_power = v.find_element_by_css_selector(ele_output_power_filed).text.lower()
                    continue
                if l.text == 'Beacon Interval':
                    default_beacon = v.find_element_by_css_selector(input).get_attribute('value')
                    continue
                if l.text == 'DTIM Interval':
                    default_dtim = v.find_element_by_css_selector(input).get_attribute('value')
            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)
            api_active = _res['active']
            api_wl_mode = _res['basic']['wirelessMode']
            api_bandwidth = _res['basic']['bandwidth']['set']
            api_output_power = _res['basic']['outputPower']
            api_channel = _res['basic']['channel']['set']
            api_short_guard = _res['advanced']['shortGuardInterval'] == 'on'
            api_beacon = str(_res['advanced']['beaconInterval'])
            api_dtim = str(_res['advanced']['dtimInterval'])
            api_beamforming = _res['advanced']['beamforming']
            api_mumimo = _res['advanced']['mumimo']
            api_wmm = _res['wmm']['active']

            list_actual2 = [api_active, api_wl_mode, api_bandwidth,
                            api_output_power, api_channel, api_short_guard, api_beacon,
                            api_dtim, api_beamforming, api_mumimo, api_wmm]
            list_expected2 = [default_radio, default_wireless_mode,
                              default_bandwidth,
                              default_output_power, default_channel, default_short_guard_interval, default_beacon,
                              default_dtim, default_beamforming, default_mumimo, default_wmm]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.0 Check API response: '
                f'API active, wireless mode, bandwidth, output power, channel, '
                f'short guard, beacon, dtim, beamforming, mu-mimo, wmm. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.0 Check API response: '
                f'API active, wireless mode, bandwidth, output power, channel, '
                f'short guard, beacon, dtim, beamforming, mu-mimo, wmm. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            # Connect 2.4GHz wifi
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            block_wl_5g = driver.find_element_by_css_selector(right)
            default_5g_ssid = wireless_get_default_ssid(block_wl_5g, 'Network Name(SSID)')
            default_5g_pw = wireless_check_pw_eye(driver, block_wl_5g, change_pw=False)
            # Connect wifi
            time.sleep(1)
            connect_wifi(default_5g_ssid, default_5g_pw)
            connected_wifi_name = current_connected_wifi()

            list_actual3 = [connected_wifi_name]
            list_expected3 = [default_5g_ssid]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.2 Connect Wifi 2.4GHz. Check Connect successfully'
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.2 Connect Wifi 2.4GHz. Check Connect successfully. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3.2 Assertion wong.')

        try:
            goto_menu(driver, advanced_tab, advanced_wireless_tab)
            wait_popup_disappear(driver, dialog_loading)

            block_5g = driver.find_element_by_css_selector(right)
            choose_specific_radio_box(block_5g, 'Radio', check=False)
            # Apply
            block_5g.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)
            if block_5g.find_element_by_css_selector(apply).is_displayed():
                block_5g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_5 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_5 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_5, values_5):
                if l.text == 'Radio':
                    get_radio = v.find_element_by_css_selector(input).is_selected()
                    break
            time.sleep(1)
            # block_5g.find_element_by_css_selector(apply).click()
            # if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
            #     time.sleep(1)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)
            # if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
            #     time.sleep(1)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)

            list_actual4 = [get_radio]
            list_expected4 = [return_false]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change Security: Check Change  Radio to OFF successfully. '
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Security: Check Change  Radio to OFF successfully. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(1)
            api_active = _res['active']

            # Goto Wireless Primary Network
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

            time.sleep(1)
            block_wl_5g = driver.find_element_by_css_selector(right)
            check_block_5g_have_no_content = len(block_wl_5g.find_elements_by_css_selector(adv_wl_radio_row)) == 0

            list_actual5 = [api_active, check_block_5g_have_no_content]
            list_expected5 = [return_false, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check disable Radio in API and Wireless 5G have no content. '
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check disable Radio in API and Wireless 5G have no content. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
    # OK
    def test_65_WIRELESS_Advanced_Wireless_5G_80211_Mode(self):
        self.key = 'WIRELESS_65'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =====================================================================================
        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        save_config(config_path, 'URL', 'url', get_config('URL', 'sub_url'))
        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/1/radio'
        _BODY = ''
        _METHOD = 'GET'

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text = default_wireless_mode.text.lower()
                    # Get total supported modes
                    default_wireless_mode.click()
                    time.sleep(1)
                    dropdown_values = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    dropdown_values_text = [i.get_attribute('option-value') for i in dropdown_values]
                    for o in dropdown_values:
                        if o.get_attribute('option-value') == '802.11a':
                            o.click()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode = _res['basic']['wirelessMode']

            list_expected3 = [default_wireless_mode_text, dropdown_values_text]
            list_actual3 = [api_wl_mode, ['802.11a', '802.11a+n', '802.11a+n+ac']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check Default Wireless mode and list options supported. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Default Wireless mode and list options supported. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            # Connect 2.4GHz wifi
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text_4 = default_wireless_mode.text.lower()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode_4 = _res['basic']['wirelessMode']

            list_actual4 = [default_wireless_mode_text_4]
            list_expected4 = [api_wl_mode_4]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Change Wireless Mode to 802.11a. Check change successfully. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Wireless Mode to 802.11a. Check change successfully. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    # Get total supported modes
                    default_wireless_mode.click()

                    time.sleep(1)
                    dropdown_values = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in dropdown_values:
                        if o.get_attribute('option-value') == '802.11a+n':
                            o.click()
                    break
            # Connect 2.4GHz wifi
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text_5 = default_wireless_mode.text.lower()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode_5 = _res['basic']['wirelessMode']

            list_actual5 = [default_wireless_mode_text_5]
            list_expected5 = [api_wl_mode_5]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Change Wireless Mode to 802.11a+n. Check change successfully. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Change Wireless Mode to 802.11a+n. Check change successfully. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

        try:
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    # Get total supported modes
                    default_wireless_mode.click()

                    time.sleep(1)
                    dropdown_values = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in dropdown_values:
                        if o.get_attribute('option-value') == '802.11a+n+ac':
                            o.click()
                    break
            #
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed)
                    default_wireless_mode_text_6 = default_wireless_mode.text.lower()
                    break

            time.sleep(1)
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(2)

            api_wl_mode_6 = _res['basic']['wirelessMode']

            list_actual6 = [default_wireless_mode_text_6]
            list_expected6 = [api_wl_mode_6]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Change Wireless Mode to 802.11a+n+ac. Check change successfully. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Change Wireless Mode to 802.11a+n+ac. Check change successfully. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_76_WIRELESS_Advanced_Wireless_5G_Scan_AP(self):
        self.key = 'WIRELESS_76'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =================================================
        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/1/scanResult'
        _BODY = ''
        _METHOD = 'GET'
        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            # 5G
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            block_5g.find_element_by_css_selector(ele_button_scan).click()
            wait_popup_disappear(driver, icon_loading)

            popup = driver.find_element_by_css_selector(dialog_content)
            # Check UI
            popup_title = popup.find_element_by_css_selector(ele_scan_title).text
            popup_refresh_button = len(popup.find_elements_by_css_selector(ele_btn_refresh)) > 0

            # Click to button List
            popup.find_element_by_css_selector(ele_button_list).click()
            time.sleep(0.5)
            check_list_wf = len(popup.find_elements_by_css_selector(ele_wifi_table)) > 0

            # CLick button Chart
            popup.find_element_by_css_selector(ele_button_chart).click()
            time.sleep(0.5)
            check_chart_wf = len(popup.find_elements_by_css_selector(ele_wifi_chart_5g)) > 0

            # Check Close button
            check_btn_close_display = popup.find_element_by_css_selector(ele_btn_close).text

            list_actual2 = [popup_title, popup_refresh_button, check_list_wf, check_chart_wf, check_btn_close_display]
            list_expected2 = ['Nearby Wireless Access Points (5GHz)', return_true, return_true, return_true, 'Close']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.0 Check popup scan components: Title, Refresh, List table, Chart table, Close button. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.0 Check popup scan components: Title, Refresh, List table, Chart table, Close button. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('3.0 Assertion wong.')

        try:
            popup.find_element_by_css_selector(ele_button_list).click()
            time.sleep(1)
            # ==================================================
            _TOKEN = get_token(_USER, _PW)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)

            api_ssid = _res[0]['ssid']
            api_channel = _res[0]['channel']
            api_rssi = _res[0]['rssi']
            api_security = _res[0]['security']
            api_mac_address = _res[0]['macAddress']
            # ==================================================
            list_rows = driver.find_elements_by_css_selector(row_table)
            if len(list_rows) > 1:
                for r in list_rows[1:]:
                    get_row_mac = r.find_element_by_css_selector('td:last-child').text
                    if get_row_mac == api_mac_address:
                        get_nw_name = r.find_element_by_css_selector(ele_table_nw_ssid_name).text
                        get_channel = r.find_element_by_css_selector(ele_table_channel).text
                        get_rssi = r.find_element_by_css_selector(ele_table_rssi).text
                        get_security = r.find_element_by_css_selector(ele_table_security).text
                        break

                list_actual3 = [api_ssid, api_channel, api_rssi, api_security, api_mac_address]
                list_expected3 = [get_nw_name, get_channel, get_rssi, get_security, get_row_mac]
            else:
                list_actual3 = []
                list_expected3 = []
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3.2 Check one of wifi scaned information with api: SSID, Channel, RSSI, Security, MAC. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.2 Check one of wifi scaned information with api: SSID, Channel, RSSI, Security, MAC. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3.2 Assertion wong.')

        try:
            # Click Graph
            popup = driver.find_element_by_css_selector(dialog_content)
            popup.find_element_by_css_selector(ele_btn_refresh).click()

            wait_popup_disappear(driver, icon_loading)
            check_list_wf_refresh = len(popup.find_elements_by_css_selector(ele_wifi_table)) > 0

            list_actual4 = [check_list_wf_refresh]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click Refresh button. Table list displayed.  '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click Refresh button. Table list displayed.. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            popup = driver.find_element_by_css_selector(dialog_content)

            popup.find_element_by_css_selector(ele_button_chart).click()
            time.sleep(1)
            check_chart_wf = len(popup.find_elements_by_css_selector(ele_wifi_chart_5g)) > 0

            list_actual5 = [check_chart_wf]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Click Chart button. Check Graph chart displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Click Chart button. Check Graph chart displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append('5 Assertion wong.')

        try:
            # Click Refresh
            popup.find_element_by_css_selector(ele_btn_refresh).click()
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)

            check_chart_wf_refresh = len(popup.find_elements_by_css_selector(ele_wifi_chart_5g)) > 0

            list_actual6 = [check_chart_wf_refresh]
            list_expected6 = [return_true]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Click Refresh button. Table Graph Chart displayed.  '
                 f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Click Refresh button.Table Graph Chart displayed. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            list_step_fail.append('6. Assertion wong.')

        try:
            # Click Close
            popup.find_element_by_css_selector(ele_btn_close).click()
            time.sleep(1)
            popup_scan = len(driver.find_elements_by_css_selector(dialog_content)) == 0
            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual7 = [popup_scan, page_title_text]
            list_expected7 = [return_true, 'Advanced > Wireless']
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Click Close button. Check popup disappear, Page Advanced > Wireless display.  '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Click Close button. Check popup disappear, Page Advanced > Wireless display. '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_77_WIRELESS_Advanced_Wireless_5G_Restore(self):
        self.key = 'WIRELESS_77'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # =================================================
        CHANNEL = '40'
        WIRELESS_MODE = '802.11a+n'
        BANDWIDTH = '20 Mhz'
        CHECK_SHORT_GUARD = False
        CHECK_WMM = False
        CHECK_BEAMFORMING = True
        CHECK_MU_MIMO = True
        OUTPUT_POWER = 'Medium'
        BEACON = '50'
        DTIM = '3'

        _URL_API = get_config('URL', 'url') + '/api/v1/wifi/1/radio'
        _BODY = ''
        _METHOD = 'GET'
        _USER = get_config('ACCOUNT', 'user')
        _PW = get_config('ACCOUNT', 'password')
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            page_title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [page_title_text]
            list_expected = ['Advanced > Wireless']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Advanced > Wireless. Check title page. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            # 2G
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Channel':
                    choose_specific_value_from_dropdown(block_5g, ele_channel_field, CHANNEL)

                if l.text == 'Wireless Mode':
                    choose_specific_value_from_dropdown(block_5g, ele_wireless_mode_filed, WIRELESS_MODE)

                if l.text == 'Bandwidth':
                    choose_specific_value_from_dropdown(block_5g, ele_bandwidth_field, BANDWIDTH)

                if l.text == 'Short Guard Interval':
                    choose_specific_radio_box(block_5g, l.text, check=CHECK_SHORT_GUARD)

                if l.text == 'WMM':
                    choose_specific_radio_box(block_5g, l.text, check=CHECK_WMM)

                if l.text == 'Beamforming':
                    choose_specific_radio_box(block_5g, l.text, check=CHECK_BEAMFORMING)

                if l.text == 'MU-MIMO':
                    choose_specific_radio_box(block_5g, l.text, check=CHECK_MU_MIMO)

                if l.text == 'Output Power':
                    choose_specific_value_from_dropdown(block_5g, ele_output_power_filed, OUTPUT_POWER)

                if l.text == 'Beacon Interval':
                    for i in range(2):
                        ActionChains(driver).move_to_element(l).perform()
                        beacon = block_5g.find_element_by_css_selector(ele_beacon_cls)
                        beacon_value = beacon.find_element_by_css_selector(input)
                        beacon_value.clear()
                        beacon_value.send_keys(BEACON)

                if l.text == 'DTIM Interval':
                    for i in range(2):
                        ActionChains(driver).move_to_element(l).perform()
                        dtim_value = v.find_element_by_css_selector(input)
                        dtim_value.clear()
                        dtim_value.send_keys(DTIM)
                    break

            block_5g = driver.find_element_by_css_selector(right)
            if block_5g.find_element_by_css_selector(apply).is_displayed():
                block_5g.find_element_by_css_selector(apply).click()
                time.sleep(1)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)


            _TOKEN = get_token(_USER, _PW)
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)

            api_active = _res['active']
            api_channel = _res['basic']['channel']['set']
            api_wl_mode = _res['basic']['wirelessMode']
            api_wmm = _res['wmm']['active']
            api_beamforming = _res['advanced']['beamforming']
            api_mumimo = _res['advanced']['mumimo']
            api_output_power = _res['basic']['outputPower'].capitalize()
            api_beacon = str(_res['advanced']['beaconInterval'])
            api_dtim = str(_res['advanced']['dtimInterval'])

            list_actual3 = [api_active, api_channel, api_wl_mode, api_wmm,
                            api_beamforming, api_mumimo, api_output_power, api_beacon, api_dtim]
            list_expected3 = [return_true, CHANNEL, WIRELESS_MODE, CHECK_WMM,
                              CHECK_BEAMFORMING, CHECK_MU_MIMO, OUTPUT_POWER, BEACON, DTIM]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Change 5 GHz: '
                f'Radio active, Channel, Wireless Mode, WMM, Beamforming, MU-MIMO, Output Power, Beacon, DTIM. '
                f'Check change successfully with api. Check api active and above option. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change 5 GHz: '
                f'Radio active, Channel, Wireless Mode, WMM, Beamforming, MU-MIMO, Output Power, Beacon, DTIM. '
                f'Check change successfully with api. Check api active and above option. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            block_5g = driver.find_element_by_css_selector(right)
            # Click 2GHz Restore
            block_5g.find_element_by_css_selector(ele_button_restore).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            list_actual4 = [check_confirm_msg]
            list_expected4 = [exp_advance_restore_confirm_msg]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click Restore. Check restore confirm message. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click Restore. Check restore confirm message. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            block_5g = driver.find_element_by_css_selector(right)
            # Action
            labels_2 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Radio':
                    default_radio = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Channel':
                    default_channel = v.find_element_by_css_selector(ele_channel_field).text.lower()
                    continue
                if l.text == 'Wireless Mode':
                    default_wireless_mode = v.find_element_by_css_selector(ele_wireless_mode_filed).text.lower()
                    continue
                if l.text == 'Bandwidth':
                    default_bandwidth = v.find_element_by_css_selector(ele_bandwidth_field).text.lower()
                    continue
                if l.text == 'Short Guard Interval':
                    default_short_guard_interval = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'WMM':
                    default_wmm = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Beamforming':
                    default_beamforming = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'MU-MIMO':
                    default_mumimo = v.find_element_by_css_selector(input).is_selected()
                    continue
                if l.text == 'Output Power':
                    default_output_power = v.find_element_by_css_selector(ele_output_power_filed).text.lower()
                    continue
                if l.text == 'Beacon Interval':
                    default_beacon = v.find_element_by_css_selector(input).get_attribute('value')
                    continue
                if l.text == 'DTIM Interval':
                    default_dtim = v.find_element_by_css_selector(input).get_attribute('value')


            _TOKEN4 = get_token(_USER, _PW)
            _res4 = call_api(_URL_API, _METHOD, _BODY, _TOKEN4)

            api_active_4 = _res4['active']
            api_wl_mode_4 = _res4['basic']['wirelessMode']
            api_bandwidth_4 = _res4['basic']['bandwidth']['set']
            api_output_power_4 = _res4['basic']['outputPower']
            api_channel_4 = _res4['basic']['channel']['set']
            api_short_guard_4 = _res4['advanced']['shortGuardInterval'] == 'on'
            api_beacon_4 = str(_res4['advanced']['beaconInterval'])
            api_dtim_4 = str(_res4['advanced']['dtimInterval'])
            api_beamforming_4 = _res4['advanced']['beamforming']
            api_mumimo_4 = _res4['advanced']['mumimo']
            api_wmm_4 = _res4['wmm']['active']

            list_actual5 = [api_active_4, api_wl_mode_4, api_bandwidth_4,
                            api_output_power_4, api_channel_4, api_short_guard_4, api_beacon_4,
                            api_dtim_4, api_beamforming_4, api_mumimo_4, api_wmm_4]
            list_expected5 = [default_radio, default_wireless_mode, default_bandwidth,
                              default_output_power, default_channel, default_short_guard_interval, default_beacon,
                              default_dtim, default_beamforming, default_mumimo, default_wmm]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4.2 Click Restore result. Check API restored: '
                f'API active, wireless mode, bandwidth, output power, channel, '
                f'short guard, beacon, dtim, beamforming, MU-MIMO, wmm. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4.2 Click Restore result. Check API restored: '
                f'API active, wireless mode, bandwidth, output power, channel, '
                f'short guard, beacon, dtim, beamforming, MU-MIMO, wmm. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')

            list_step_fail.append('4.2 Assertion wong.')

        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
