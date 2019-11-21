import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver


class Home(unittest.TestCase):
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

    def test_01_Check_Internet_Image_Operation_when_Dual_WAN_is_off(self):
        global list_actual, list_expected
        self.key = 'HOME_01'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API = URL_LOGIN + '/api/v1/network/wan/0'
        METHOD = 'GET'
        BODY = None
        # Handle API
        _token = get_token(USER_LOGIN, PW_LOGIN)
        # Call API
        res = call_api(URL_API, METHOD, BODY, _token)

        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            time.sleep(1)
            _check_dual_selected = driver.find_element_by_css_selector('.dual-wan-card .wrap-input input')
            if _check_dual_selected.is_selected():
                driver.find_element_by_css_selector('.dual-wan-card .wrap-input').click()
                # Click Apply
                driver.find_element_by_css_selector('.dual-wan-card button.active-button').click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(5)
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)

            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            ls_wan_field = driver.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label: value})

            translate_key_api2ui = {"mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            ipv4 = res['ipv4']

            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]


            _expected = [ipv4[i] for i in translate_key_api2ui.keys()]
            if ipv4['mode'] == 'dynamic':
                _expected[0] = 'Dynamic IP'
            if ipv4['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'

            _check = True if (dict_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Satatic IP', 'PPPoE']) else False
            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check WAN IPv4\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check WAN IPv4. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Click to icon fab
            driver.find_element_by_css_selector(home_icon_fab).click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            list_actual = [more_fab]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check btn + is displayed when click btn |||\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual = [current_tab]
            list_expected = [URL_LOGIN + network_internet]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Click + btn. Check re-direct Network>Internet\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_02_Check_Internet_Image_Operation_when_Dual_WAN_is_on(self):
        global list_actual, list_expected
        self.key = 'HOME_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')

        URL_API_DUAL_WAN = URL_LOGIN + '/api/v1/network/dualwan'
        URL_NETWORK_WAN = '/api/v1/network/wan/'
        METHOD = 'GET'
        BODY = None
        # Handle API
        _token = get_token(USER_LOGIN, PW_LOGIN)
        # Call API

        try:
            login(driver)
            time.sleep(3)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)
            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            time.sleep(2)
            _check_dual_selected = driver.find_element_by_css_selector(dual_wan_input)
            if not _check_dual_selected.is_selected():
                driver.find_element_by_css_selector(dual_wan_button).click()
                fill_info = driver.find_elements_by_css_selector(dual_wan_ls_fields)
                # Primary WAN
                fill_info[1].click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == 'Ethernet':
                        o.click()
                # Secondary WAN
                fill_info[2].click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == 'Android Tethering':
                        o.click()
                time.sleep(0.2)
                driver.find_element_by_css_selector(dual_wan_apply_btn).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(5)

            driver.get(URL_LOGIN + homepage)
            time.sleep(2)

            res_dual_wan = call_api(URL_API_DUAL_WAN, METHOD, BODY, _token)
            URL_API_WAN_PRIMARY = URL_LOGIN + URL_NETWORK_WAN + str(res_dual_wan['primary']['interface'])
            URL_API_WAN_SECONDARY = URL_LOGIN + URL_NETWORK_WAN + str(res_dual_wan['secondary']['interface'])
            res_wan_primary = call_api(URL_API_WAN_PRIMARY, METHOD, BODY, _token)
            res_wan_secondary = call_api(URL_API_WAN_SECONDARY, METHOD, BODY, _token)

            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            # ~~~~~~~~~~~~~~~~~~~~~ Primary
            primary = driver.find_element_by_css_selector(left)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_primary_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_primary_wan.update({label: value})

            translate_key_api2ui = {"mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            primary_info = res_wan_primary['ipv4']

            primary_actual = [dict_primary_wan[i] for i in translate_key_api2ui.values()]
            primary_expected = [primary_info[i] for i in translate_key_api2ui.keys()]
            if primary_info['mode'] == 'dynamic':
                primary_expected[0] = 'Dynamic IP'
            if primary_info['dnsServer2'] == '':
                primary_expected[-1] = '0.0.0.0'

            # ~~~~~~~~~~~~~~~~~~~~~ Secondary
            secondary = driver.find_element_by_css_selector(right)
            ls_wan_field = secondary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_secondary_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_secondary_wan.update({label: value})

            translate_key_api2ui = {"mode": "Connection status",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            secondary_info = res_wan_secondary

            secondary_actual = [dict_secondary_wan[i] for i in translate_key_api2ui.values()]
            secondary_expected = [secondary_info['ipv4'][i] for i in translate_key_api2ui.keys()]
            if secondary_info['connectivity'] == 'connected':
                secondary_expected[0] = 'Connected'
            if secondary_info['ipv4']['dnsServer2'] == '':
                secondary_expected[-1] = '0.0.0.0'

            _check = True if (dict_primary_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_primary_wan['Connection Type'] in ['Dynamic IP', 'Satatic IP', 'PPPoE']) else False
            list_actual = [primary_actual, secondary_actual, _check]
            list_expected = [primary_expected, secondary_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check WAN IPv4\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check WAN IPv4. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Click to icon fab
            driver.find_elements_by_css_selector(home_icon_fab)[0].click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            list_actual = [more_fab]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check btn + is displayed when click btn |||\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual = [current_tab]
            list_expected = [URL_LOGIN + network_internet]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Click + btn. Check re-direct Network>Internet\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            # Home
            driver.find_element_by_css_selector(home_tab).click()
            time.sleep(1)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            check_home_displayed = driver.find_element_by_css_selector(home_view_wrap).is_displayed()

            list_actual = [check_home_displayed]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Home page is displayed\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Home page is displayed. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            # Click to icon fab
            driver.find_elements_by_css_selector(home_icon_fab)[1].click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            list_actual = [more_fab]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check btn + is displayed when click btn |||\n')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual = [current_tab]
            list_expected = [URL_LOGIN + network_internet]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Click + btn. Check re-direct Network>Internet\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '7. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_03_Check_Connection_Internet_Information(self):

        global list_actual, list_expected
        self.key = 'HOME_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')

        URL_API_WAN_V4 = URL_LOGIN + '/api/v1/network/wan/0'
        METHOD = 'GET'
        BODY = None

        # Handle API
        _token = get_token(USER_LOGIN, PW_LOGIN)
        # Call API
        res_wan_v4 = call_api(URL_API_WAN_V4, METHOD, BODY, _token)

        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            # Get information of WAN to a dictionary
            ls_wan_field = driver.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label: value})

            translate_key_api2ui = {"mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            ipv4 = res_wan_v4['ipv4']
            # Get values of Web UI and API based on translate diction
            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
            _expected = [ipv4[i] for i in translate_key_api2ui.keys()]

            # Fix some values did not match
            if ipv4['mode'] == 'dynamic':
                _expected[0] = 'Dynamic IP'
            if ipv4['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'
            # Check value of Wan type and Connection Type
            _check = True if (dict_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Satatic IP', 'PPPoE']) else False
            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check WAN IPv4\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check WAN IPv4. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
