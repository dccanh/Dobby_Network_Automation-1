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


class Pilot(unittest.TestCase):
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

    def test_Login_Through_Gateway_IP(self):
        global list_actual, list_expected, password_config, url_config, user_config
        self.key = 'MAIN_01'
        driver = self.driver
        self.def_name = get_func_name()
        lis_step_fail = []
        self.list_steps = []

        # ~~~~~~~~~~~~~~~~~~~~~~ Get info URL, ACCOUNT ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Get and write URL
            get_url_ipconfig(ipconfig_field='Default Gateway')

            url_config = get_config('URL', 'url')
            time.sleep(3)
            # deploy account to web server
            filename = 'account.txt'
            commmand = 'capitest get Device.Users.User.2. leaf'
            run_cmd(commmand, filename)
            time.sleep(3)
            # Get account information from web server and write to config.txt
            get_result_command_from_server(url_ip=url_config, filename=filename)

            user_config = get_config('ACCOUNT', 'user')
            password_config = get_config('ACCOUNT', 'password')
            ls_config = [url_config, user_config, password_config]
            check_result_command = []
            for i in ls_config:
                if i != '':
                    check_result_command.append(True)
                else:
                    check_result_command.append(False)
            check_result_command = all(check_result_command)
            # Check url, account info is not None
            list_actual = [check_result_command]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Get result by command success\n')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Get result by command success\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            lis_step_fail.append('1, 2. Assertion wong')

        # ~~~~~~~~~~~~~~~~~~~~~~~ Check Login ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.get(url_config)
            time.sleep(2)
            driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_config)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_password)[-1].send_keys(password_config)
            time.sleep(1)
            # Captcha
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
            time.sleep(1)
            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(3)

            verify_header = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual = [verify_header]
            list_expected = [header_login_text]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3, 4. Check login by text Welcome\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Check login by text Welcome\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            lis_step_fail.append(
                '3, 4. Assertion wong.')

        self.assertListEqual(lis_step_fail, [])

    def test_Check_Factory_Reset_Operation(self):
        global list_actual, list_expected, password_config, url_config, user_config
        self.key = 'MAIN_02'
        driver = self.driver
        self.def_name = get_func_name()
        lis_step_fail = []
        self.list_steps = []
        ip_address_value = '2'
        start_ip_address_value = '5'
        network_name = 'Anne_2G!'
        url = get_config('URL', 'url')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)

            # Goto Homepage
            driver.get(url+homepage)
            time.sleep(3)

            # Goto Network > Lan
            goto_menu(driver, network_tab, network_lan_tab)
            # Change ip address 192.168.1.2
            ip_address = driver.find_elements_by_css_selector(ip_address_input_filed)[-1]
            ip_address = driver.find_elements_by_css_selector(ip_address_input_filed)[-1]
            act = ActionChains(driver)
            act.move_to_element(ip_address)
            act.key_down(Keys.CONTROL)
            act.send_keys('a')
            act.key_up(Keys.CONTROL)
            time.sleep(0.5)
            act.send_keys(ip_address_value)
            time.sleep(0.5)
            act.perform()

            # Change Start IP address 192.168.1.5
            start_ip_address = driver.find_elements_by_css_selector(start_end_ip_address)[0]
            # ActionChains(driver).move_to_element(start_ip_address).double_click().send_keys(start_ip_address_value).perform()
            act = ActionChains(driver)
            act.move_to_element(start_ip_address)
            act.key_down(Keys.CONTROL)
            act.send_keys('a')
            act.key_up(Keys.CONTROL)
            time.sleep(0.5)
            act.send_keys(start_ip_address_value)
            time.sleep(0.5)
            act.perform()
            # Goto Wireless > Primary Network
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            field_2g = driver.find_elements_by_css_selector(fields_in_2g)
            for f in field_2g:
                if f.find_element_by_css_selector(label_name_in_2g).text == 'Network Name(SSID)':
                    ssid_value = f.find_element_by_css_selector(label_value_in_2g)
                    ssid_value.clear()
                    ssid_value.send_keys(network_name)
                if f.find_element_by_css_selector(label_name_in_2g).text == 'Security':
                    security_field = f.find_element_by_css_selector(secure_value_field)
                    security_field.click()
                    values_secure = security_field.find_elements_by_css_selector(secure_value_in_drop_down)
                    for s in values_secure:
                        if s.get_attribute('option-value') == 'NONE':
                            s.click()
            verify_header = driver.find_element_by_css_selector(lg_welcome_header).text

            list_actual = [verify_header]
            list_expected = [header_login_text]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3, 4. Check login by text Welcome\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Check login by text Welcome\nActual: {str(list_actual)}. \nExpected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            lis_step_fail.append(
                '3, 4. Assertion wong.')



        self.assertListEqual(lis_step_fail, [])

if __name__ == '__main__':
    unittest.main()
