import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver


class Network(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
