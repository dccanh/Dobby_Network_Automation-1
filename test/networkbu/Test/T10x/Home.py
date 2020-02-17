import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver


class HOME(unittest.TestCase):
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
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            time.sleep(1)
            _check_dual_selected = driver.find_element_by_css_selector(dual_wan_input)
            if _check_dual_selected.is_selected():
                driver.find_element_by_css_selector(dual_wan_button).click()
                # Click Apply
                driver.find_element_by_css_selector(dual_wan_apply_btn).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(5)
            time.sleep(5)
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)

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
            # Handle API
            _token = get_token(USER_LOGIN, PW_LOGIN)
            # Call API
            res = call_api(URL_API, METHOD, BODY, _token)
            ipv4 = res['ipv4']

            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]


            _expected = [ipv4[i] for i in translate_key_api2ui.keys()]
            if ipv4['mode'] == 'dynamic':
                _expected[0] = 'Dynamic IP'
            elif ipv4['mode'] == 'staticc':
                _expected[0] = 'Static IP'
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
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
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
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
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

    def test_04_Verify_connection_status_according_to_WAN_connection_type_Dynamic_IP(self):
        self.key = 'HOME_04'
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
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)

            if not len(driver.find_elements_by_css_selector(internet_setting_block)):
                internet_setting = driver.find_element_by_css_selector(internet_setting_block_single)
            else:
                internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            ActionChains(driver).move_to_element(internet_setting).perform()
            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # Connection type
                if l.text == 'Connection Type':
                    if f.text != 'Dynamic IP':
                        f.click()
                        time.sleep(0.2)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == 'Dynamic IP':
                                o.click()
                                break
                        btn_apply = internet_setting.find_element_by_css_selector(apply)
                        btn_apply.click()
                        time.sleep(0.5)
                        # Click OK
                        driver.find_element_by_css_selector(btn_ok).click()
                        time.sleep(1)
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(5)
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(5)

                    break
            self.list_steps.append('[PASS] Set Precondition Success')
        except:
            self.list_steps.append('[FAIL] Set Precondition fail')
            list_step_fail.append('Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            driver.find_element_by_css_selector(home_tab).click()
            wait_popup_disappear(driver, dialog_loading)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            check_active = driver.find_element_by_css_selector(home_img_connection).is_enabled()
            list_actual = [check_active]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Check Internet Image is high light')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Internet Image is high light. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
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
            # Handle API
            _token = get_token(USER_LOGIN, PW_LOGIN)
            # Call API
            res_wan_v4 = call_api(URL_API_WAN_V4, METHOD, BODY, _token)
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
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Static IP', 'PPPoE']) else False
            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check WAN IPv4\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check WAN IPv4. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_05_Verify_connection_status_according_to_WAN_connection_type_Static_IP(self):
        self.key = 'HOME_05'
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
        VALUE_DNS2 = '1.1.1.1'
        VALUE_DNS2_SPLIT = VALUE_DNS2.split('.')
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)

            if not len(driver.find_elements_by_css_selector(internet_setting_block)):
                internet_setting = driver.find_element_by_css_selector(internet_setting_block_single)
            else:
                internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            ActionChains(driver).move_to_element(internet_setting).perform()
            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # Connection type
                if l.text == 'Connection Type':
                    if f.text != 'Static IP':
                        f.click()
                        time.sleep(0.2)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            if o.text == 'Static IP':
                                o.click()
                                break
                        btn_apply = internet_setting.find_element_by_css_selector(apply)
                        _check_apply = btn_apply.is_enabled()
                        if _check_apply:
                            btn_apply.click()
                            time.sleep(0.5)
                            # Click OK
                            driver.find_element_by_css_selector(btn_ok).click()
                            time.sleep(1)
                            wait_popup_disappear(driver, dialog_loading)
                            time.sleep(5)
                            wait_popup_disappear(driver, dialog_loading)
                            time.sleep(5)
                        else:
                            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
                            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
                            for l, f in zip(internet_setting_label, internet_setting_fields):
                                # DNS server 2
                                if l.text == 'DNS Server 2':
                                    dns_2 = f.find_elements_by_css_selector(input)
                                    for d, v in zip(dns_2, VALUE_DNS2_SPLIT):
                                        ActionChains(driver).move_to_element(d).click().key_down(
                                            Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(
                                            v).perform()
                            btn_apply = internet_setting.find_element_by_css_selector(apply)
                            btn_apply.click()
                            time.sleep(0.5)
                            # Click OK
                            driver.find_element_by_css_selector(btn_ok).click()
                            time.sleep(1)
                            wait_popup_disappear(driver, dialog_loading)
                            time.sleep(5)
                            wait_popup_disappear(driver, dialog_loading)
                            time.sleep(5)
                    break
            self.list_steps.append('[PASS] Set Precondition Success')
        except:
            self.list_steps.append('[FAIL] Set Precondition fail')
            list_step_fail.append('Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            driver.find_element_by_css_selector(home_tab).click()
            wait_popup_disappear(driver, dialog_loading)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            check_active = driver.find_element_by_css_selector(home_img_connection).is_enabled()
            list_actual = [check_active]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Check Internet Image is high light')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Internet Image is high light. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
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
            # Handle API
            _token = get_token(USER_LOGIN, PW_LOGIN)
            # Call API
            res_wan_v4 = call_api(URL_API_WAN_V4, METHOD, BODY, _token)
            ipv4 = res_wan_v4['ipv4']
            # Get values of Web UI and API based on translate diction
            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
            _expected = [ipv4[i] for i in translate_key_api2ui.keys()]

            # Fix some values did not match
            if ipv4['mode'] == 'dynamic':
                _expected[0] = 'Dynamic IP'
            elif ipv4['mode'] == 'staticc':
                _expected[0] = 'Static IP'
            if ipv4['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'
            # Check value of Wan type and Connection Type
            _check = True if (dict_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Static IP', 'PPPoE']) else False
            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check Information display')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check Information display. Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_09_Check_Router_Wireless_page(self):
        self.key = 'HOME_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)

            block_left = driver.find_element_by_css_selector(left)
            block_card = block_left.find_elements_by_css_selector(card_cls)

            lan_title = block_card[0].find_element_by_css_selector(title_tabs_cls).text
            lan_card_tabs = block_card[0].find_elements_by_css_selector(card_tabs_cls)
            lan_card_tabs_v4 = lan_card_tabs[0].text
            lan_card_tabs_v6 = lan_card_tabs[1].text
            icon_fab = len(block_card[0].find_elements_by_css_selector(home_icon_fab)) != 0

            list_actual1 = [lan_title, lan_card_tabs_v4, lan_card_tabs_v6, icon_fab]
            list_expected1 = ['LAN', 'IPv4', 'IPv6', return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3.1 Check LAN block: Title, IPv4, IPv6, Icon ||| displayed')
        except:
            self.list_steps.append(
                f'[Fail] 3.1 Check LAN block: Title, IPv4, IPv6, Icon ||| displayed. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('3.1 Assertion wong.')

        try:

            block_right = driver.find_element_by_css_selector(right)
            block_card_right = block_right.find_elements_by_css_selector(card_cls)

            lan_title = block_card_right[0].find_element_by_css_selector(title_tabs_cls).text
            lan_card_tabs = block_card_right[0].find_elements_by_css_selector(card_tabs_cls)
            lan_card_tabs_24 = lan_card_tabs[0].text
            lan_card_tabs_5 = lan_card_tabs[1].text
            icon_fab = len(block_card_right[0].find_elements_by_css_selector(home_icon_fab)) != 0

            list_actual2 = [lan_title, lan_card_tabs_24, lan_card_tabs_5, icon_fab]
            list_expected2 = ['Wireless', '2.4GHz', '5GHz', return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3.2 Check Wireless block: Title, 2.4GHz, 5GHz, Icon ||| displayed')
        except:
            self.list_steps.append(
                f'[Fail] 3.2 Check Wireless block: Title, 2.4GHz, 5GHz, Icon ||| displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('3.2 Assertion wong.')

        try:
            information_title = block_card[1].find_element_by_css_selector(title_tabs_cls).text
            cpu_status_title = block_card[2].find_element_by_css_selector('h3').text

            ethernet_title = block_card_right[1].find_element_by_css_selector(title_tabs_cls).text
            memory_status_title = block_card_right[2].find_element_by_css_selector('h3').text

            list_actual3 = [information_title, cpu_status_title, ethernet_title, memory_status_title]
            list_expected3 = ['Information', 'CPU Status', 'Ethernet Port Status', 'Memory Status']
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3.3 Check Information, CPU Status, Ethernet Port Status, Memory Status. ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3.3 Check Information, CPU Status, Ethernet Port Status, Memory Status. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3.3 Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_10_Check_LAN_information(self):
        self.key = 'HOME_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API = URL_LOGIN + '/api/v1/network/lan'
        METHOD = 'GET'
        BODY = None
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)

            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == 'IPv4':
                    t.click()
                    time.sleep(1)

            lan_block = driver.find_elements_by_css_selector(card_cls)[0]
            ls_wan_field = lan_block.find_elements_by_css_selector(home_wan_ls_fields)
            actual_lan_v4_value = list()
            actual_lan_v4_label = list()
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                actual_lan_v4_value.append(value)
                actual_lan_v4_label.append(label)

            # Handle API
            _token = get_token(USER_LOGIN, PW_LOGIN)
            # Call API
            res = call_api(URL_API, METHOD, BODY, _token)

            api_lan_ip = res['ipv4']['ipAddress']
            api_subnet = res['ipv4']['subnet']
            api_dhcp_active = 'Enabled' if res['ipv4']['dhcp']['active']==True else 'Disabled'
            api_dhcp_start_IP = res['ipv4']['dhcp']['startIP']
            api_dhcp_end_IP = res['ipv4']['dhcp']['endIP']
            api_mac_address = res['macAddress']
            expected_lan_v4_value = [api_lan_ip, api_subnet, api_dhcp_active,
                              api_dhcp_start_IP, api_dhcp_end_IP, api_mac_address]
            expected_lan_v4_label = ['LAN IP Address', 'Subnet Mask', 'DHCP Server',
                                     'Start IP Address', 'End IP Address', 'MAC Address']
            list_actual1 = [actual_lan_v4_value, actual_lan_v4_label]
            list_expected1 = [expected_lan_v4_value, expected_lan_v4_label]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3 Check LAN block information')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check LAN block information. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('3. Assertion wong.')

        try:

            for t in card_tabs:
                if t.text == 'IPv6':
                    t.click()
                    time.sleep(1)

            lan_block = driver.find_elements_by_css_selector(card_cls)[0]
            ls_wan_field = lan_block.find_elements_by_css_selector(home_wan_ls_fields)

            actual_lan_v6_label = list()
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                actual_lan_v6_label.append(label)

            expected_lan_v6_label = ['LAN IPv6 Address', 'Prefix Length',
                                     'Assigned Type', 'MAC Address']
            list_actual1 = [actual_lan_v6_label]
            list_expected1 = [expected_lan_v6_label]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check LAN block information IPv6: Check Label')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check LAN block information IPv6: Check Label. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_11_Check_the_operation_of_LAN_Table_Icon(self):
        self.key = 'HOME_11'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)

            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == 'IPv4':
                    t.click()
                    time.sleep(1)

            # Click to icon fab
            driver.find_elements_by_css_selector(home_icon_fab)[0].click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = detect_current_menu(driver)

            list_actual1 = [more_fab, current_tab]
            list_expected1 = [return_true, ('NETWORK', 'LAN')]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3, 4. Click ||| btn; Check Display +; Click +; Check Display target IPv4 page.')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Click ||| btn; Check Display +; Click +; Check Display target IPv4 page. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('3, 4. Assertion wong.')

        try:
            goto_menu(driver, ele_home_tab, 0)
            time.sleep(1)
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)

            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == 'IPv6':
                    t.click()
                    time.sleep(1)

            # Click to icon fab
            driver.find_elements_by_css_selector(home_icon_fab)[0].click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = detect_current_menu(driver)

            list_actual2 = [more_fab, current_tab]
            list_expected2 = [return_true, ('ADVANCED', 'IPv6')]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Click ||| btn; Check Display +; Click +; Check Display target IPv6 page')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Click ||| btn; Check Display +; Click +; Check Display target IPv6 page. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_12_Check_wireless_table_information(self):
        self.key = 'HOME_12'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        # Prepare DUT in default stage
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(100)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # CLick Wireless Image
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)

            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == '2.4GHz':
                    t.click()
                    time.sleep(1)

            right_side = driver.find_element_by_css_selector(right)
            wl_block = right_side.find_elements_by_css_selector(card_cls)[0]
            ls_wan_field = wl_block.find_elements_by_css_selector(home_wan_ls_fields)

            actual_wl_2g_value = list()
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                if label == 'Network Name(SSID)':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_wl_2g_value.append(value)
                if label == 'Security':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_wl_2g_value.append(value)
                if label == 'Password':
                    value = len(wl_block.find_elements_by_css_selector(password_eye)) != 0
                    actual_wl_2g_value.append(value)
                if label == 'MAC Address':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    if checkMACAddress(value):
                        actual_wl_2g_value.append(True)
                    else:
                        actual_wl_2g_value.append(False)

            list_actual1 = actual_wl_2g_value
            list_expected1 = ['We Love You So Much_2G!', 'WPA2/WPA-PSK', True, True]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Information of WL 2.4GHZ')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Information of WL 2.4GHZ. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == '5GHz':
                    t.click()
                    time.sleep(1)

            right_side = driver.find_element_by_css_selector(right)
            wl_block = right_side.find_elements_by_css_selector(card_cls)[0]
            ls_wan_field = wl_block.find_elements_by_css_selector(home_wan_ls_fields)

            actual_wl_5g_value = list()
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                if label == 'Network Name(SSID)':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_wl_5g_value.append(value)
                if label == 'Security':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_wl_5g_value.append(value)
                if label == 'Password':
                    value = len(wl_block.find_elements_by_css_selector(password_eye)) != 0
                    actual_wl_5g_value.append(value)
                if label == 'MAC Address':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    if checkMACAddress(value):
                        actual_wl_5g_value.append(True)
                    else:
                        actual_wl_5g_value.append(False)

            list_actual2 = actual_wl_5g_value
            list_expected2 = ['We Love You So Much_5G!', 'WPA2/WPA-PSK', True, True]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check Information of WL 5GHZ')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Information of WL 5GHZ. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_13_Check_Wireless_Table_Icon_operation(self):
        self.key = 'HOME_13'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)

            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(0.2)

            home_wireless = driver.find_element_by_css_selector(wireless_block)
            # Click to icon fab
            home_wireless.find_element_by_css_selector(home_icon_fab).click()
            time.sleep(0.2)
            # Click to icon more fab
            home_wireless.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual = [current_tab]
            list_expected = [URL_LOGIN + wireless_primary]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Click + btn. Check re-direct Network>LAN\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click + btn. Check re-direct Network>LAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_14_Check_Information_table_information(self):
        self.key = 'HOME_14'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        SERIAL_NUMBER = get_config('GENERAL', 'serial_number')
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # CLick Wireless Image
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)

            left_side = driver.find_element_by_css_selector(left)
            information_block = left_side.find_elements_by_css_selector(card_cls)[1]

            info_block_title = information_block.find_element_by_css_selector(title_tabs_cls).text
            ls_info_field = information_block.find_elements_by_css_selector(home_wan_ls_fields)

            actual_info_value = list()
            for w in ls_info_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                if label == 'Model Name':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_info_value.append(value)
                if label == 'Serial Number':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text.endswith(SERIAL_NUMBER)
                    actual_info_value.append(value)
                # if label == 'Firmware Vesion':
                #     value = w.find_element_by_css_selector(home_wan_ls_value).text
                #     actual_info_value.append(value)
                if label == 'Build Time':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    try:
                        datetime.strptime(value, '%Y.%m.%d %H:%M:%S')
                        actual_info_value.append(True)
                    except ValueError:
                        actual_info_value.append(False)
            # Check for update
            check_for_update = information_block.find_element_by_css_selector(apply)
            check_for_update_text = check_for_update.text
            check_for_update_color = check_for_update.value_of_css_property('background-color')

            list_actual1 = [info_block_title, actual_info_value, check_for_update_text, check_for_update_color]
            list_expected1 = ['Information', ['HUMAX T10X', True, True], 'Check for Update', 'rgba(23, 143, 230, 1)']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Information title, Model name, End of Serial number, '
                                   'type of build time, Tex of button, Color')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Information title, Model name, End of Serial number, '
                                   'type of build time, Tex of button, Color. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            ActionChains(driver).move_to_element(check_for_update).click().perform()
            time.sleep(3)
            check_popup = len(driver.find_elements_by_css_selector(ele_check_for_update_title)) != 0

            list_actual2 = [check_popup]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check pop up appear')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check pop up appear. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_18_Check_USB_Image_Operation(self):
        self.key = 'HOME_18'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # CLick Wireless Image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(2)
            check_high_light = len(driver.find_elements_by_css_selector(''.join([home_img_usb_connection, '.active'])))
            check_high_light = check_high_light != 0

            check_num_usb = driver.find_element_by_css_selector('div.usb-connection .more-info').text
            # Set default is 2 USB.

            list_actual1 = [check_high_light, check_num_usb]
            list_expected1 = [return_true, '2']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check USB Image selected, Check number of USB')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check USB Image selected, Check number of USB. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_20_Check_USB_Table_information(self):
        self.key = 'HOME_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # CLick USB Image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(3)
            # Check USB block components
            usb_card = driver.find_element_by_css_selector(ele_usb_card)

            usb_title = usb_card.find_element_by_css_selector(title_tabs_cls).text
            exist_btn_fab = len(usb_card.find_elements_by_css_selector(home_icon_fab)) == 1

            time.sleep(2)
            ls_info_field = usb_card.find_elements_by_css_selector(home_wan_ls_fields)
            actual_info_value = list()

            value = ls_info_field[0].find_element_by_css_selector(home_wan_ls_value).text
            actual_info_value.append(value != '')
            value = ls_info_field[2].find_element_by_css_selector(home_wan_ls_value).text
            actual_info_value.append(value != '')

            space_used = usb_card.find_element_by_css_selector(ele_space_use).text != ''
            space_available = usb_card.find_element_by_css_selector(ele_space_available).text != ''
            space_bar = len(usb_card.find_elements_by_css_selector(ele_space_bar)) != 0
            btn_remove = usb_card.find_element_by_css_selector(apply).text

            list_actual1 = [usb_title, exist_btn_fab, actual_info_value,
                            space_used, space_available, space_bar, btn_remove]
            list_expected1 = ['USB', return_true, [return_true]*2, return_true, return_true, return_true, 'Remove']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Title, Exist button |||, Device name, Total size, not null, '
                                   'space used, availabled, space bar not null, Btn Remove text')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Title, Exist button |||, Device name, Total size, not null, '
                                   'space used, availabled, space bar not null, Btn Remove text. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_22_Check_the_operation_of_USB_Icon(self):
        self.key = 'HOME_22'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            # CLick USB Image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            # Check USB block components
            usb_card = driver.find_elements_by_css_selector(ele_usb_card)[0]

            # Click to Remove
            usb_card.find_element_by_css_selector(home_icon_fab).click()
            # Btn more fab is displayed
            time.sleep(1)
            more_fab = usb_card.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            current_tab = detect_current_menu(driver)

            list_actual1 = [more_fab, current_tab]
            list_expected1 = [return_true, ('MEDIA SHARE', 'USB')]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Click ||| btn; Check Display +; Click +; Check Display target USB page.')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail]1,2,3. Click ||| btn; Check Display +; Click +; Check Display target USB page. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3, 4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_21_Check_the_Remove_Button_operation_of_USB_Table(self):
        self.key = 'HOME_21'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            # CLick USB Image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Check USB block components
            usb_card = driver.find_elements_by_css_selector(ele_usb_card)[0]

            # Click to Remove
            usb_card.find_element_by_css_selector(apply).click()
            time.sleep(1)
            # Verify confirmation
            confirm_text = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # CLick OK
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)

            confirm_remove_text = driver.find_element_by_css_selector(complete_dialog_msg).text
            wait_popup_disappear(driver, dialog_loading)

            # CLick OK
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)

            check_popup_disappear = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual1 = [confirm_text, confirm_remove_text, check_popup_disappear]
            list_expected1 = ['Do you want to safely remove the USB device?',
                              'Remove the USB device safely from the router.',
                              return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3,4,5. Check popup confirm text, popup complete text, popup disappear.')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3,4,5. Check popup confirm text, popup complete text, popup disappear. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3, 4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_25_Check_the_Server_Table_information(self):
        self.key = 'HOME_25 '
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            # CLick USB Image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Check USB block components
            server_card = driver.find_element_by_css_selector(ele_server_card)

            server_title = server_card.find_element_by_css_selector(title_tabs_cls).text
            exist_btn_fab = len(server_card.find_elements_by_css_selector(home_icon_fab)) == 1

            ls_server_field = server_card.find_elements_by_css_selector(home_wan_ls_fields)

            actual_value = list()
            for w in ls_server_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                if label == 'FTP Server':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_value.append(value)
                if label == 'Windows Network (Samba)':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_value.append(value)
                if label == 'Media Server (DLNA)':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_value.append(value)


            list_actual1 = [server_title, exist_btn_fab] + actual_value
            list_expected1 = ['Server', return_true] + ['Off']*3
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Server title, icon fab, value fields.')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Server title, icon fab, value fields. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_26_Check_Server_Table_Icon_operation(self):
        self.key = 'HOME_26'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            # CLick USB Image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            # Check USB block components
            server_card = driver.find_elements_by_css_selector(ele_server_card)[0]

            # Click to fab
            server_card.find_element_by_css_selector(home_icon_fab).click()
            # Btn more fab is displayed
            time.sleep(1)
            more_fab = server_card.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            current_tab = detect_current_menu(driver)

            list_actual1 = [more_fab, current_tab]
            list_expected1 = [return_true, ('MEDIA SHARE', 'Server Settings')]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Click ||| btn; Check Display +; Click +; Check Display target USB Server page.')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click ||| btn; Check Display +; Click +; Check Display target USB Server page. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_27_Check_the_Devices_Image(self):
        self.key = 'HOME_27'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Goto Homepage
            if len(driver.find_elements_by_css_selector(lg_welcome_header)):
                handle_winzard_welcome(driver)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            # Check USB block components
            num_devices = driver.find_element_by_css_selector(ele_device_more_info).text

            list_actual1 = [num_devices]
            list_expected1 = ['1']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Click Device icon, Check number of device.')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click Device icon, Check number of device. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
