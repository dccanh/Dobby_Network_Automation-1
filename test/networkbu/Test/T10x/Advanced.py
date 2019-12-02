import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver
from faker import Faker


class Advanced(unittest.TestCase):
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
        end_time = datetime.now()
        duration = str((end_time - self.start_time))
        write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.time_stamp)
        self.driver.quit()

    def test_08_Local_Access_and_External_Access_confirmation(self):
        self.key = 'ADVANCED_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        URL_LOGIN_HTTPS = URL_LOGIN.replace('http', 'https')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
                driver.get(URL_LOGIN + homepage)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)
            wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Goto Advanced > Network
            goto_menu(driver, advanced_tab, advanced_network_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Disable Remote Access and HTTPS Access
            options_left = driver.find_element_by_css_selector(left)

            fields_in_options = options_left.find_elements_by_css_selector(select)

            # Check remote access
            if fields_in_options[5].find_element_by_css_selector(input).is_selected():
                fields_in_options[5].click()
            # Check HTTPS Access
            if fields_in_options[6].find_element_by_css_selector(input).is_selected():
                fields_in_options[6].click()
            time.sleep(1)
            local_val = options_left.find_elements_by_css_selector(advanced_extra_info)[0].text
            remote_val = options_left.find_elements_by_css_selector(advanced_extra_info)[1].text

            exp_local = 'Local Access'+URL_LOGIN+','
            exp_remote = 'Remote Access-'

            list_actual = [local_val, remote_val]
            list_expected = [exp_local, exp_remote]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Disabled Remote and HTTPS Access: Check extra text')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Disabled Remote and HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Enable HTTPS Access
            if not fields_in_options[6].find_element_by_css_selector(input).is_selected():
                fields_in_options[6].click()
            time.sleep(1)
            http_port = options_left.find_elements_by_css_selector(input)[8].get_attribute('value')

            local_val = options_left.find_elements_by_css_selector(advanced_extra_info)[0].text
            remote_val = options_left.find_elements_by_css_selector(advanced_extra_info)[1].text

            exp_local = 'Local Access'+URL_LOGIN+', '+URL_LOGIN_HTTPS+':'+http_port
            exp_remote = 'Remote Access-'

            list_actual = [local_val, remote_val]
            list_expected = [exp_local, exp_remote]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Enable HTTPS Access: Check extra text')
        except:
            self.list_steps.append(
                f'[Fail] 4. Enable HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            # Check remote access
            if fields_in_options[5].find_element_by_css_selector(input).is_selected():
                fields_in_options[5].click()
                time.sleep(1)
            # Check HTTPS Access
            if fields_in_options[6].find_element_by_css_selector(input).is_selected():
                fields_in_options[6].click()
            time.sleep(1)
            local_val = options_left.find_elements_by_css_selector(advanced_extra_info)[0].text
            remote_val = options_left.find_elements_by_css_selector(advanced_extra_info)[1].text

            exp_local = 'Local Access' + URL_LOGIN + ','
            exp_remote = 'Remote Access-'

            list_actual = [local_val, remote_val]
            list_expected = [exp_local, exp_remote]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Disabled Remote and HTTPS Access: Check extra text')
        except:
            self.list_steps.append(
                f'[Fail] 5. Disabled Remote and HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            # Enable HTTPS Access
            if not fields_in_options[5].find_element_by_css_selector(input).is_selected():
                fields_in_options[5].click()
            time.sleep(1)
            remote_port = options_left.find_elements_by_css_selector(input)[6].get_attribute('value')

            local_val = options_left.find_elements_by_css_selector(advanced_extra_info)[0].text
            remote_val = options_left.find_elements_by_css_selector(advanced_extra_info)[1].text

            exp_local = 'Local Access' + URL_LOGIN + ','
            exp_remote = 'Remote Access' + 'http://' + wan_ip + ':' + remote_port

            list_actual = [local_val, remote_val]
            list_expected = [exp_local, exp_remote]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Enable Remote Access: Check extra text')
        except:
            self.list_steps.append(
                f'[Fail] 6. Enable Remote Access: Check extra text. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            # Check remote access
            if fields_in_options[5].find_element_by_css_selector(input).is_selected():
                fields_in_options[5].click()
            # Check HTTPS Access
            if fields_in_options[6].find_element_by_css_selector(input).is_selected():
                fields_in_options[6].click()
            time.sleep(1)
            local_val = options_left.find_elements_by_css_selector(advanced_extra_info)[0].text
            remote_val = options_left.find_elements_by_css_selector(advanced_extra_info)[1].text

            exp_local = 'Local Access' + URL_LOGIN + ','
            exp_remote = 'Remote Access-'

            list_actual = [local_val, remote_val]
            list_expected = [exp_local, exp_remote]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Disabled Remote and HTTPS Access: Check extra text')
        except:
            self.list_steps.append(
                f'[Fail] 7. Disabled Remote and HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # Check remote access
            if not fields_in_options[5].find_element_by_css_selector(input).is_selected():
                fields_in_options[5].click()
            # Check HTTPS Access
            if not fields_in_options[6].find_element_by_css_selector(input).is_selected():
                fields_in_options[6].click()
            time.sleep(1)
            remote_port = options_left.find_elements_by_css_selector(input)[6].get_attribute('value')
            http_port = options_left.find_elements_by_css_selector(input)[8].get_attribute('value')

            local_val = options_left.find_elements_by_css_selector(advanced_extra_info)[0].text
            remote_val = options_left.find_elements_by_css_selector(advanced_extra_info)[1].text

            exp_local = 'Local Access' + URL_LOGIN + ', ' + URL_LOGIN_HTTPS + ':' + http_port
            exp_remote = 'Remote Access' + 'https://' + wan_ip + ':' + remote_port

            list_actual = [local_val, remote_val]
            list_expected = [exp_local, exp_remote]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8. Enable Remote, HTTPS Access: Check extra text')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8. Enable Remote, HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('8. Assertion wong.')

        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
