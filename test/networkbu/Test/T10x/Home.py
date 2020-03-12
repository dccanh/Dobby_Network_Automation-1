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
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            self.driver = webdriver.Chrome(driver_path)  # open chrome
            self.driver.maximize_window()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        try:
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        except:
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
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
    def test_01_HOME_Check_Internet_Image_Operation_when_Dual_WAN_is_off(self):
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
            grand_login(driver)
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
            time.sleep(1)
            # Call API
            res = call_api(URL_API, METHOD, BODY, _token)
            ipv4 = res['ipv4']
            time.sleep(1)
            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]

            _expected = [ipv4[i] for i in translate_key_api2ui.keys()]
            if ipv4['mode'] == 'dynamic':
                _expected[0] = 'Dynamic IP'
            elif ipv4['mode'] == 'staticc':
                _expected[0] = 'Static IP'
            if ipv4['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'
            time.sleep(1)
            _check = True if (dict_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Static IP', 'PPPoE']) else False

            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual)}. '
                f'Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Click to icon fab
            driver.find_element_by_css_selector(home_icon_fab).click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            list_actual2 = [more_fab]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual3 = [current_tab]
            list_expected3 = [URL_LOGIN + network_internet]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Click + btn. Check re-direct Network>Internet\1'
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_02_HOME_Check_Internet_Image_Operation_when_Dual_WAN_is_on(self):
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
            grand_login(driver)
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
            time.sleep(1)
            goto_menu(driver, home_tab, 0)
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

            translate_key_api2ui = {"name": "WAN Type",
                                    "mode": "Connection status",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            secondary_info = res_wan_secondary
            time.sleep(1)
            secondary_actual = [''.join(dict_secondary_wan[i].split()) for i in translate_key_api2ui.values()]
            secondary_expected = [secondary_info['name']]

            if secondary_info['connectivity'] == 'connected':
                secondary_expected.append('Connected')
            elif secondary_info['connectivity'] == 'disconnected':
                secondary_expected.append('Disconnected')

            if secondary_info['ipv4']['address'] == '-':
                secondary_expected.append('0.0.0.0')
            if secondary_info['ipv4']['subnet'] == '-':
                secondary_expected.append('0.0.0.0')
            if secondary_info['ipv4']['gateway'] == '-':
                secondary_expected.append('0.0.0.0')
            if secondary_info['ipv4']['dnsServer1'] == '-':
                secondary_expected.append('0.0.0.0')
            if secondary_info['ipv4']['dnsServer2'] == '-':
                secondary_expected.append('0.0.0.0')

            _check = True if (dict_primary_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_primary_wan['Connection Type'] in ['Dynamic IP', 'Static IP', 'PPPoE']) else False

            list_actual1 = [primary_actual, secondary_actual, _check]
            list_expected1 = [primary_expected, secondary_expected, return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Click to icon fab
            driver.find_elements_by_css_selector(home_icon_fab)[0].click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            list_actual3 = [more_fab]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual4 = [current_tab]
            list_expected4 = [URL_LOGIN + network_internet]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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

            list_actual5 = [check_home_displayed]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Home page is displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Home page is displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            # Click to icon fab
            driver.find_elements_by_css_selector(home_icon_fab)[1].click()
            # Btn more fab is displayed
            time.sleep(0.2)
            more_fab = driver.find_element_by_css_selector(home_icon_more_fab).is_displayed()

            list_actual6 = [more_fab]
            list_expected6 = [return_true]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check btn + is displayed when click btn |||. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            list_step_fail.append(
                '6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click to icon more fab
            driver.find_element_by_css_selector(home_icon_more_fab).click()
            time.sleep(1)
            current_tab = driver.find_element_by_css_selector(current_tab_chosen).get_attribute('href')

            list_actual7 = [current_tab]
            list_expected7 = [URL_LOGIN + network_internet]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Click + btn. Check re-direct Network>Internet. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_03_HOME_Check_Connection_Internet_Information(self):
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
            grand_login(driver)
            time.sleep(2)

            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(left)
            # Get information of WAN to a dictionary
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label: value})
            time.sleep(1)

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
            time.sleep(1)

            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_04_HOME_Verify_connection_status_according_to_WAN_connection_type_Dynamic_IP(self):
        self.key = 'HOME_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')

        # filename = '1'
        # commmand = 'factorycfg.sh -a'
        # run_cmd(commmand, filename=filename)
        # # Wait 5 mins for factory
        # time.sleep(150)
        # wait_DUT_activated(URL_LOGIN)
        # wait_ping('192.168.1.1')
        #
        # filename_2 = 'account.txt'
        # commmand_2 = 'capitest get Device.Users.User.2. leaf'
        # run_cmd(commmand_2, filename_2)
        # time.sleep(3)
        # # Get account information from web server and write to config.txt
        # user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API_WAN_V4 = URL_LOGIN + '/api/v1/network/wan/0'
        METHOD = 'GET'
        BODY = None
        try:
            grand_login(driver)
            time.sleep(1)

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
            self.list_steps.append('[Pass] Set Precondition Success')
        except:
            self.list_steps.append('[Fail] Set Precondition fail')
            list_step_fail.append('Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)

            driver.find_element_by_css_selector(home_tab).click()
            wait_popup_disappear(driver, dialog_loading)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            check_active = driver.find_element_by_css_selector(home_img_connection).is_enabled()

            list_actual1 = [check_active]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Check Internet Image is high light. '
                                   f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Internet Image is high light. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            primary = driver.find_element_by_css_selector(ele_wan_block)
            # Get information of WAN to a dictionary
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
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
            self.list_steps.append(
                '[Pass] 2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_05_HOME_Verify_connection_status_according_to_WAN_connection_type_Static_IP(self):
        self.key = 'HOME_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(150)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')
        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API_WAN_V4 = URL_LOGIN + '/api/v1/network/wan/0'
        METHOD = 'GET'
        BODY = None
        VALUE_DNS2 = '0.0.0.0'
        VALUE_DNS2_SPLIT = VALUE_DNS2.split('.')
        _token = get_token(USER_LOGIN, PW_LOGIN)
        # Call API
        get_wan = call_api(URL_API_WAN_V4, METHOD, BODY, _token)['ipv4']['address']

        NEW_PASSWORD = 'abc123'
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
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

            # Next Change pw
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(5)

            # Next Operation Mode
            time.sleep(3)
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(0.5)

            # Click arrow down
            time.sleep(3)
            driver.find_element_by_css_selector(option_select).click()
            time.sleep(2)
            ls_connection_type = driver.find_elements_by_css_selector(
                welcome_internet_setup1_ls_option_connection_type)

            # Click Static IP
            for i in ls_connection_type:
                if i.text == 'Static IP':
                    i.click()
            time.sleep(1)

            dns_2_input = driver.find_elements_by_css_selector('.wrap-form:last-child .wrap-input input')
            for i in dns_2_input:
                ActionChains(driver).move_to_element(i).click().send_keys('0').perform()
                time.sleep(0.5)

            len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))
            while len_let_go == 0:
                # Next Internet Setup 1
                time.sleep(2)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                    time.sleep(3)
                len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))

            # Click Let's Go
            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            wait_visible(driver, home_view_wrap)
            time.sleep(5)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)
            check_ota_auto_update(driver)
            time.sleep(1)

            self.list_steps.append('[Pass] Set Precondition Success')
        except:
            self.list_steps.append('[Fail] Set Precondition fail')
            list_step_fail.append('Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(3)
            driver.find_element_by_css_selector(home_tab).click()
            wait_popup_disappear(driver, dialog_loading)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            check_active = driver.find_element_by_css_selector(home_img_connection).is_enabled()

            list_actual1 = [check_active]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Check Internet Image is high light. '
                                   f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Internet Image is high light. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            primary = driver.find_element_by_css_selector(ele_wan_block)
            # Get information of WAN to a dictionary
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label: value})
            time.sleep(1)
            translate_key_api2ui = {"mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            # Handle API
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            _token = get_token(USER_LOGIN, PW_LOGIN)
            time.sleep(2)
            # Call API
            res_wan_v4 = call_api(URL_API_WAN_V4, METHOD, BODY, _token)
            time.sleep(2)
            ipv4 = res_wan_v4['ipv4']
            time.sleep(2)
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
            time.sleep(1)
            # Check value of Wan type and Connection Type
            _check = True if (dict_wan['WAN Type'] in ['Ethernet','USB Broadband', 'Android Tethering']) \
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Static IP', 'PPPoE']) else False

            list_actual2 = [_actual, _check]
            list_expected2 = [_expected, return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Check Information display. Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check Information display. Check WAN type in options, and Connection Type in options. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_09_HOME_Check_Router_Wireless_page(self):
        self.key = 'HOME_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
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
            self.list_steps.append(f'[Pass] 3.1 Check LAN block: Title, IPv4, IPv6, Icon ||| displayed. '
                                   f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.list_steps.append('[Pass] 3.2 Check Wireless block: Title, 2.4GHz, 5GHz, Icon ||| displayed. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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
            self.list_steps.append('[Pass] 3.3 Check Information, CPU Status, Ethernet Port Status, Memory Status. '
                                   f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3.3 Check Information, CPU Status, Ethernet Port Status, Memory Status. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3.3 Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_10_HOME_Check_LAN_information(self):
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
            grand_login(driver)
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
            time.sleep(2)
            # Handle API
            _token = get_token(USER_LOGIN, PW_LOGIN)
            time.sleep(2)
            # Call API
            res = call_api(URL_API, METHOD, BODY, _token)
            time.sleep(2)

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
            self.list_steps.append('[Pass] 3 Check LAN block information'
                                   f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [actual_lan_v6_label]
            list_expected2 = [expected_lan_v6_label]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check LAN block information IPv6: Check Label. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check LAN block information IPv6: Check Label. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_11_HOME_Check_the_operation_of_LAN_Table_Icon(self):
        self.key = 'HOME_11'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
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
            self.list_steps.append(
                '[Pass] 3, 4. Click ||| btn; Check Display +; Click +; Check Display target IPv4 page. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
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
            self.list_steps.append(
                '[Pass] 5. Click ||| btn; Check Display +; Click +; Check Display target IPv6 page'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Click ||| btn; Check Display +; Click +; Check Display target IPv6 page. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_12_HOME_Check_wireless_table_information(self):
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
        time.sleep(150)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        try:
            grand_login(driver)
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
            self.list_steps.append('[Pass] 3. Check Information of WL 2.4GHZ: SSID, Sercurity, PW, MAC address. '
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Information of WL 2.4GHZ: SSID, Sercurity, PW, MAC address. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
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
            self.list_steps.append('[Pass] 4. Check Information of WL 5GHZ: SSID, Sercurity, PW, MAC address' 
                                   f'Actual: {str(list_actual2)}. '
                                   f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Information of WL 5GHZ: SSID, Sercurity, PW, MAC address. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_13_HOME_Check_Wireless_Table_Icon_operation(self):
        self.key = 'HOME_13'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
            time.sleep(1)

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
                f'[Pass] 3. Click + btn. Check re-direct Network>LAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Click + btn. Check re-direct Network>LAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_14_HOME_Check_Information_table_information(self):
        self.key = 'HOME_14'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        SERIAL_NUMBER = get_config('GENERAL', 'serial_number')

        try:
            grand_login(driver)
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
                if label == 'Firmware Version':
                    value = w.find_element_by_css_selector(home_wan_ls_value).text
                    actual_info_value.append(value)

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

            expected_model_name = get_config('GENERAL', 'model')

            # expected_current_firmware
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            URL_API = URL_LOGIN + '/api/v1/gateway/about'
            METHOD = 'GET'
            BODY = ''
            _token = get_token(USER_LOGIN, PW_LOGIN)
            time.sleep(2)
            # Call API
            res = call_api(URL_API, METHOD, BODY, _token)
            time.sleep(2)
            firmware_version = res['software']['version']

            list_actual1 = [info_block_title,
                            actual_info_value,
                            check_for_update_text,
                            check_for_update_color]
            list_expected1 = ['Information',
                              [expected_model_name, True, firmware_version, True],
                              'Check for Update',
                              'rgba(23, 143, 230, 1)']

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Information title, Model name, End of Serial number, '
                                   'type of build time, firm version,  Text of button, Color. '
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Information title, Model name, End of Serial number, '
                                   'type of build time, firm version,  Text of button, Color. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            ActionChains(driver).move_to_element(check_for_update).click().perform()
            time.sleep(3)
            check_popup = len(driver.find_elements_by_css_selector(ele_check_for_update_title)) != 0

            list_actual2 = [check_popup]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check pop up appear. '
                                   f'Actual: {str(list_actual2)}. '
                                   f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check pop up appear. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_18_HOME_Check_USB_Image_Operation(self):
        self.key = 'HOME_18'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
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
    # OK
    def test_20_HOME_Check_USB_Table_information(self):
        self.key = 'HOME_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
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
                                   'space used, availabled, space bar not null, Btn Remove text. ' 
                                   f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
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
    # OK
    def test_22_HOME_Check_the_operation_of_USB_Icon(self):
        self.key = 'HOME_22'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            grand_login(driver)
            time.sleep(3)
            self.list_steps.append('[Pass] Login successfully')
        except:
            self.list_steps.append('[Fail] Login fail')

        try:
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
    # OK
    def test_21_HOME_Check_the_Remove_Button_operation_of_USB_Table(self):
        self.key = 'HOME_21'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
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
    # OK
    def test_25_HOME_Check_the_Server_Table_information(self):
        self.key = 'HOME_25 '
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
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
    # OK
    def test_26_HOME_Check_Server_Table_Icon_operation(self):
        self.key = 'HOME_26'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)

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
    # OK
    def test_27_HOME_Check_the_Devices_Image(self):
        self.key = 'HOME_27'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)

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
    # OK
    def test_28_HOME_Check_the_Devices_Sub_Menu_Information(self):
        self.key = 'HOME_28'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        # Set precondition
        try:
            time.sleep(5)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name)
            time.sleep(3)

            os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            time.sleep(2)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            self.list_steps.append('[Pass] Set precondition fail: 1 wired + 1 wireless')
        except:
            self.list_steps.append('[Fail] Set precondition fail: 1 wired + 1 wireless')


        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            table = driver.find_element_by_css_selector(ele_device_tab_titles)
            tab_title = [i.text for i in table.find_elements_by_css_selector(ele_button_type)]

            list_actual1 = tab_title
            list_expected1 = ['Connected Devices', 'Disconnected Devices']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Check title of table.'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 2.Check title of table. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')

            list_step_fail.append('2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~ Connected
        try:
            # +++++++++++++++++++++++++++++++++++++++++++++++++++
            URL_API_CONNECTED = get_config('URL', 'url') + '/api/v1/gateway/devices?connected=true'
            USERNAME = get_config('ACCOUNT', 'user')
            PASSWORD = get_config('ACCOUNT', 'password')
            METHOD = 'GET'
            BODY = ''
            _token = get_token(USERNAME, PASSWORD)
            res_connected = call_api(URL_API_CONNECTED, METHOD, BODY, _token)

            ls_expected_connected = list()
            for r in res_connected:
                dict_act = dict()
                dict_act['name'] = r['name']
                dict_act['ssid'] = r['path']
                dict_act['mac'] = r['macAddress']
                dict_act['ip'] = r['ipAddress']
                ls_expected_connected.append(dict_act)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++
            ls_actual_connected = list()
            connected_rows = driver.find_elements_by_css_selector(ele_device_row_connected)
            for r in connected_rows:
                dict_row = dict()
                dict_row['name'] = r.find_element_by_css_selector(name_cls).text
                dict_row['ssid'] = r.find_element_by_css_selector(ele_ssid_cls).text
                dict_row['mac'] = r.find_element_by_css_selector(wol_mac_addr).text
                dict_row['ip'] = r.find_element_by_css_selector(ip_address_cls).text
                ls_actual_connected.append(dict_row)

            list_actual3 = ls_expected_connected
            list_expected3 = ls_expected_connected
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3.1 Check value rows displayed on Connected Devices Page.'
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.1 Check value rows displayed on Connected Devices Page. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3.1 Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~ Disconnected
        try:
            table.find_elements_by_css_selector(ele_button_type)[1].click()
            time.sleep(2)
            # ++++++++++++++++++++++++++++++++++++++++++++++++++
            URL_API_DISCONNECTED = get_config('URL', 'url') + '/api/v1/gateway/devices?connected=false'
            res_disconnected = call_api(URL_API_DISCONNECTED, METHOD, BODY, _token)
            ls_expected_disconnected = list()
            for r in res_disconnected:
                dict_act = dict()
                dict_act['name'] = r['name']
                dict_act['mac'] = r['macAddress']
                ls_expected_disconnected.append(dict_act)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++

            ls_actual_disconnected = list()
            disconnected_rows = driver.find_elements_by_css_selector(ele_device_row_disconnected)
            for r in disconnected_rows:
                dict_row = dict()
                dict_row['name'] = r.find_element_by_css_selector(name_cls).text
                dict_row['mac'] = r.find_element_by_css_selector(wol_mac_addr).text
                ls_actual_disconnected.append(dict_row)

            list_actual4 = ls_actual_disconnected
            list_expected4 = ls_expected_disconnected
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3.2 Check value rows displayed on Disconnected Devices Page.'
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3.2 Check value rows displayed on Disconnected Devices Page. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3.2 Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_29_HOME_Check_the_Connected_Devices_Information(self):
        self.key = 'HOME_29'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            table = driver.find_element_by_css_selector(ele_device_tab_titles)
            check_title_tab = table.find_element_by_css_selector(ele_active_cls).text
            check_btn_refresh = table.find_element_by_css_selector(ele_btn_refresh).is_displayed()
            check_local_nw_title = table.find_element_by_css_selector(ele_device_network_title).text

            check_connect_column_title = table.find_elements_by_css_selector(ele_device_connect_col_title)
            check_connect_column_title_text = [i.text for i in check_connect_column_title]

            check_edit_btn = len(table.find_elements_by_css_selector(edit_cls)) > 0

            list_actual1 = [check_title_tab,
                            check_btn_refresh,
                            check_local_nw_title,
                            check_connect_column_title_text,
                            check_edit_btn]
            list_expected1 = ['Connected Devices',
                              return_true,
                              'Local Network',
                              ['Device Name', 'Interface', 'MAC Address', 'IP Address'],
                              return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Check Connected Devices, [Refresh], Local Network, '
                'Device name, Interface, MAC Address, IP Address, Edit icon are displayed .'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2.Check Connected Devices, [Refresh], Local Network, '
                'Device name, Interface, MAC Address, IP Address, Edit icon are displayed . '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')

            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_30_HOME_Check_a_configuration_list_of_connected_devices_Edit(self):
        self.key = 'HOME_30'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        current_pw = get_config('ACCOUNT', 'password')

        try:
            time.sleep(5)
            os.system(f'netsh wlan disconnect')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            self.list_steps.append('[Pass] Precondition Successfully.')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
            list_step_fail.append('Assertion wong.')

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            default_device_tab = driver.find_element_by_css_selector(ele_active_connected_device)
            default_device_tab_text = default_device_tab.text

            actual_local_network_number = driver.find_element_by_css_selector(ele_count_cls).text

            # Check USB block components
            num_devices = driver.find_element_by_css_selector(ele_device_more_info).text

            list_actual1 = [default_device_tab_text, actual_local_network_number]
            list_expected1 = ['Connected Devices', num_devices]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Check default tab in Devices, number of devices.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check default tab in Devices, number of devices. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(1)

            img = driver.find_element_by_css_selector(ele_edit_device_img).get_attribute('class')

            infor = driver.find_elements_by_css_selector(ele_info_cls)
            infor_text = [i.text for i in infor]

            check_mac = checkMACAddress(infor_text[0])
            check_ip = checkIPAddress(infor_text[1])
            check_port = infor_text[2].startswith('LAN Port')

            ls_label = driver.find_elements_by_css_selector(label_name_in_2g)
            ls_label_text = [i.text for i in ls_label]

            expected_ls_label = ['Reserved IP', 'MAC Filtering', 'Parental Control', 'WoL (Wake on LAN)']

            list_actual3 = [img, check_mac, check_ip, check_port, ls_label_text]
            list_expected3 = ['pc', return_true, return_true, return_true, expected_ls_label]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check default tab in Devices, number of devices.'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check default tab in Devices, number of devices. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            time.sleep(5)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
            time.sleep(3)

            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(1)
            self.list_steps.append('4. [Pass] Connect wifi Successfully.')
        except:
            self.list_steps.append('4. [Fail] Connect wifi Fail')
            list_step_fail.append('4. Assertion wong.')

        try:
            time.sleep(5)
            # Re-Load
            driver.refresh()
            time.sleep(10)
            check_ota_auto_update(driver)
            time.sleep(2)
            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            img = driver.find_element_by_css_selector(ele_edit_device_img).get_attribute('class')

            infor = driver.find_elements_by_css_selector(ele_info_cls)
            infor_text = [i.text for i in infor]

            check_mac = checkMACAddress(infor_text[0])
            check_ip = checkIPAddress(infor_text[1])
            check_wifi = infor_text[2] == 'Wi-Fi 2.4GHz'

            ls_label = driver.find_elements_by_css_selector(label_name_in_2g)
            ls_label_text = [i.text for i in ls_label]

            expected_ls_label = ['Reserved IP', 'MAC Filtering', 'Parental Control', 'WoL (Wake on LAN)']

            list_actual5 = [img, check_mac, check_ip, check_wifi, ls_label_text]
            list_expected5 = ['pc', return_true, return_true, return_true, expected_ls_label]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check default tab in Devices, number of devices.'
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check default tab in Devices, number of devices. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_31_HOME_Reserved_IP_registration_deletion_confirmation(self):
        self.key = 'HOME_31'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        current_pw = get_config('ACCOUNT', 'password')

        # Disconnect Wireless, connect LAN
        try:
            os.system(f'netsh wlan disconnect')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            self.list_steps.append('[Pass] Precondition Successfully.')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
            list_step_fail.append('Assertion wong.')

        # Check popup appear after click Edit
        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Click Edit; Check popup display.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Click Edit; Check popup display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('2. Assertion wong.')

        # Reserved IP OK
        try:
            # Click Reserved IP
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    add_reserved_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            if len(add_reserved_btn.find_elements_by_css_selector(add_class)) > 0:
                # Click
                add_reserved_btn.click()
            time.sleep(0.2)
            # Check confirm message
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.2)
            # Check popup confirm disappear
            check_confirm_pop_disappear = len(driver.find_elements_by_css_selector(confirm_dialog_msg)) == 0

            # Click Reserved IP
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    add_reserved_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click reserved
            if len(add_reserved_btn.find_elements_by_css_selector(add_class)) > 0:
                add_reserved_btn.click()
            time.sleep(0.2)
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            # Check Reserved to "-"
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    check_delete_icon = f.find_element_by_css_selector(ele_icon_cls).get_attribute('class')
                    break
            check_delete_icon = check_delete_icon == 'icon delete'

            list_actual3 = [check_confirm_msg, check_confirm_pop_disappear, check_delete_icon]
            list_expected3 = [exp_confirm_msg_add_resserve_ip, return_true, return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check confirm add reserved IP msg, Click Cancel-> Check popup disappear. '
                                   'Click add again -> Click OK -> Check add icon change to delete icon'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check confirm add reserved IP msg, Click Cancel-> Check popup disappear. '
                'Click add again -> Click OK -> Check add icon change to delete icon'
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        # Verify reserved IP in Network Lan
        try:
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = False
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = True

            list_actual4 = [check_add_in_lan]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Add reserved IP -> Check add successfully in Network Lan'
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Add reserved IP -> Check add successfully in Network Lan'
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        # Delete Reserved IP, Check delete in Network LAN
        try:
            time.sleep(3)
            # Goto Home
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)
            # Click Reserved IP
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    add_reserved_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click
            if len(add_reserved_btn.find_elements_by_css_selector(delete_cls)) > 0:
                add_reserved_btn.click()

            time.sleep(0.2)
            # Check confirm message
            check_confirm_delete_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

             # Click Cancel reserved Popup
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = True
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = False

            list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
            list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5,6,7. Delete reserved IP -> Check Delete successfully in Network Lan'
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5,6,7. Delete reserved IP -> Check Delete successfully in Network Lan'
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5,6,7. Assertion wong.')

        # Connect Wifi
        try:
            time.sleep(5)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
            time.sleep(3)

            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(110)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(1)
            self.list_steps.append('8.0 [Pass] Connect wifi Successfully.')
        except:
            self.list_steps.append('8.0 [Fail] Connect wifi Fail')
            list_step_fail.append('8.0 Assertion wong.')

        try:
            # Refresh page
            driver.refresh()
            time.sleep(5)

            goto_menu(driver, home_tab, 0)
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.1. Click Edit; Check popup display.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 8.1. Click Edit; Check popup display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('8.1. Assertion wong.')

        try:
            # Click Reserved IP
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    add_reserved_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click
            if len(add_reserved_btn.find_elements_by_css_selector(add_class)) > 0:
                add_reserved_btn.click()
            time.sleep(0.2)
            # Check confirm message
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.2)
            # Check popup confirm disappear
            check_confirm_pop_disappear = len(driver.find_elements_by_css_selector(confirm_dialog_msg)) == 0

            # Click Reserved IP
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    add_reserved_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click reserved
            if len(add_reserved_btn.find_elements_by_css_selector(add_class)) > 0:
                add_reserved_btn.click()
            time.sleep(0.2)
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            # Check Reserved to "-"
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    check_delete_icon = f.find_element_by_css_selector(ele_icon_cls).get_attribute('class')
                    break
            check_delete_icon = check_delete_icon == 'icon delete'

            list_actual3 = [check_confirm_msg, check_confirm_pop_disappear, check_delete_icon]
            list_expected3 = [exp_confirm_msg_add_resserve_ip, return_true, return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.2. Check confirm add reserved IP msg, Click Cancel-> Check popup disappear. '
                                   'Click add again -> Click OK -> Check add icon change to delete icon'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8.2. Check confirm add reserved IP msg, Click Cancel-> Check popup disappear. '
                'Click add again -> Click OK -> Check add icon change to delete icon'
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('8.2. Assertion wong.')

        try:
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = False
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = True

            list_actual4 = [check_add_in_lan]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.3. Add reserved IP -> Check add successfully in Network Lan'
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 8.3 reserved IP -> Check add successfully in Network Lan'
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('8.3. Assertion wong.')

        try:
            # Goto Home
            goto_menu(driver, home_tab, 0)
            time.sleep(2)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)
            # Click Reserved IP
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Reserved IP':
                    add_reserved_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click
            if len(add_reserved_btn.find_elements_by_css_selector(delete_cls)) > 0:
                add_reserved_btn.click()
            time.sleep(0.2)
            # Check confirm message
            check_confirm_delete_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Cancel reserved Popup
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = True
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = False

            list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
            list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.4. Delete reserved IP -> Check Delete successfully in Network Lan'
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8.4. Delete reserved IP -> Check Delete successfully in Network Lan'
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('8.4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    # HOME 32 chua dc
    def test_32_HOME_Mac_Filtering_registration_deletion_confirmation(self):
        self.key = 'HOME_32'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        current_pw = get_config('ACCOUNT', 'password')

        # Disconnect Wireless, connect LAN
        try:
            os.system(f'netsh wlan disconnect')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            self.list_steps.append('[Pass] Precondition Successfully.')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
            list_step_fail.append('Assertion wong.')

        # Check popup appear after click Edit
        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            before_device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Click Edit; Check popup display.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Click Edit; Check popup display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('2. Assertion wong.')

        # Mac Filtering OK
        try:
            # Click Mac Filtering
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
                # Click
                add_mac_btn.click()
            time.sleep(0.2)
            # Check confirm message
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.2)
            # Check popup confirm disappear
            check_confirm_pop_disappear = len(driver.find_elements_by_css_selector(confirm_dialog_msg)) == 0

            # Click Mac Filtering
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click mac
            if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
                add_mac_btn.click()
            time.sleep(0.2)
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            # Switch to disconnect devices
            driver.find_element_by_css_selector(ele_second_tab).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            after_device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text

            list_actual3 = [check_confirm_msg, check_confirm_pop_disappear, before_device_mac]
            list_expected3 = [exp_confirm_msg_add_mac_filtering, return_true, after_device_mac]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3, 4. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
                                   'Click add again -> Click OK -> Check MAC display in Disconnect Devices'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
                'Click add again -> Click OK -> Check MAC display in Disconnect Devices'
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3, 4. Assertion wong.')

            # Connect Wifi
        try:
            time.sleep(5)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
            time.sleep(3)

            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(110)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(1)
            self.list_steps.append('8.0 [Pass] Connect wifi Successfully.')
        except:
            self.list_steps.append('8.0 [Fail] Connect wifi Fail')
            list_step_fail.append('8.0 Assertion wong.')







        # Verify Mac Filtering in Network Lan
        try:
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = False
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = True

            list_actual4 = [check_add_in_lan]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Add Mac Filtering -> Check add successfully in Network Lan'
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Add Mac Filtering -> Check add successfully in Network Lan'
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        # Delete Mac Filtering, Check delete in Network LAN
        try:
            time.sleep(3)
            # Goto Home
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)
            # Click Mac Filtering
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click
            if len(add_mac_btn.find_elements_by_css_selector(delete_cls)) > 0:
                add_mac_btn.click()

            time.sleep(0.2)
            # Check confirm message
            check_confirm_delete_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

             # Click Cancel reserved Popup
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = True
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = False

            list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
            list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5,6,7. Delete Mac Filtering -> Check Delete successfully in Network Lan'
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5,6,7. Delete Mac Filtering -> Check Delete successfully in Network Lan'
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5,6,7. Assertion wong.')

        # Connect Wifi
        try:
            time.sleep(5)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(3)
            write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
            time.sleep(3)

            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(110)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(1)
            self.list_steps.append('8.0 [Pass] Connect wifi Successfully.')
        except:
            self.list_steps.append('8.0 [Fail] Connect wifi Fail')
            list_step_fail.append('8.0 Assertion wong.')

        try:
            # Refresh page
            driver.refresh()
            time.sleep(5)

            goto_menu(driver, home_tab, 0)
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.1. Click Edit; Check popup display.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 8.1. Click Edit; Check popup display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('8.1. Assertion wong.')

        try:
            # Click Mac Filtering
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click
            if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
                add_mac_btn.click()
            time.sleep(0.2)
            # Check confirm message
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.2)
            # Check popup confirm disappear
            check_confirm_pop_disappear = len(driver.find_elements_by_css_selector(confirm_dialog_msg)) == 0

            # Click Mac Filtering
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click reserved
            if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
                add_mac_btn.click()
            time.sleep(0.2)
            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            # Check Reserved to "-"
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    check_delete_icon = f.find_element_by_css_selector(ele_icon_cls).get_attribute('class')
                    break
            check_delete_icon = check_delete_icon == 'icon delete'

            list_actual3 = [check_confirm_msg, check_confirm_pop_disappear, check_delete_icon]
            list_expected3 = [exp_confirm_msg_add_mac_filtering, return_true, return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.2. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
                                   'Click add again -> Click OK -> Check add icon change to delete icon'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8.2. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
                'Click add again -> Click OK -> Check add icon change to delete icon'
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('8.2. Assertion wong.')

        try:
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = False
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = True

            list_actual4 = [check_add_in_lan]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.3. Add Mac Filtering -> Check add successfully in Network Lan'
                                   f'Actual: {str(list_actual4)}. '
                                   f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 8.3 Mac Filtering -> Check add successfully in Network Lan'
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('8.3. Assertion wong.')

        try:
            # Goto Home
            goto_menu(driver, home_tab, 0)
            time.sleep(2)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)
            # Click Mac Filtering
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
                    add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
                    break
            # Click
            if len(add_mac_btn.find_elements_by_css_selector(delete_cls)) > 0:
                add_mac_btn.click()
            time.sleep(0.2)
            # Check confirm message
            check_confirm_delete_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(0.2)
            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Cancel reserved Popup
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            time.sleep(1)

            check_add_in_lan = True
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = False

            list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
            list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8.4. Delete Mac Filtering -> Check Delete successfully in Network Lan'
                                   f'Actual: {str(list_actual5)}. '
                                   f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8.4. Delete Mac Filtering -> Check Delete successfully in Network Lan'
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('8.4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_33_HOME_Confirm_Parental_Control_information_display(self):
        self.key = 'HOME_33'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_API = get_config('URL', 'url') + '/api/v1/gateway/devices/1'

        try:

            os.system(f'netsh wlan disconnect')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            self.list_steps.append('[Pass] Precondition Successfully.')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
            list_step_fail.append('Assertion wong.')

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Click Edit; Check popup display.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Click Edit; Check popup display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            # Check parental control
            # Find all wrap form
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Parental Control':
                    parental_value = f.find_element_by_css_selector(home_wan_ls_value).text
                    break

            # Check API
            user = get_config('ACCOUNT', 'user')
            pw = get_config('ACCOUNT', 'password')
            token = get_token(user, pw)
            res = call_api(URL_API, 'GET', body='', token=token)
            check_parental_api = res['advanced']['parentalContrl']

            list_actual3 = [parental_value, check_parental_api]
            list_expected3 = ['Off', False]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Parental Control value in Web UI and API.'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Parental Control value in Web UI and API. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    # HOME 38. Confuse
    def test_38_HOME_Check_Disconnect_Devices_information(self):
        self.key = 'HOME_38'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_API = get_config('URL', 'url') + '/api/v1/gateway/devices/1'

        try:

            os.system(f'netsh wlan disconnect')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            self.list_steps.append('[Pass] Precondition Successfully.')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
            list_step_fail.append('Assertion wong.')

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Click Edit; Check popup display.'
                                   f'Actual: {str(list_actual1)}. '
                                   f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Click Edit; Check popup display. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            # Check parental control
            # Find all wrap form
            all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
            for f in all_wrap_form:
                if f.find_element_by_css_selector(home_wan_ls_label).text == 'Parental Control':
                    parental_value = f.find_element_by_css_selector(home_wan_ls_value).text
                    break

            # Check API
            user = get_config('ACCOUNT', 'user')
            pw = get_config('ACCOUNT', 'password')
            token = get_token(user, pw)
            res = call_api(URL_API, 'GET', body='', token=token)
            check_parental_api = res['advanced']['parentalContrl']

            list_actual3 = [parental_value, check_parental_api]
            list_expected3 = ['Off', False]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Check Parental Control value in Web UI and API.'
                                   f'Actual: {str(list_actual3)}. '
                                   f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Parental Control value in Web UI and API. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
