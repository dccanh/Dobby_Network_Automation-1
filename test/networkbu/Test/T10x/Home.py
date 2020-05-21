import sys
sys.path.append('../../')
import unittest
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
            connect_wifi_by_command('HVNWifi', 'Wifihvn12@!')
            time.sleep(1)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
            time.sleep(5)
            # Connect by LAN again
            os.system('netsh wlan disconnect')
            time.sleep(1)
        write_to_excel(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        # write_to_excel_tmp(self.key, self.list_steps, self.def_name)
        save_duration_time(test_case_key=type(self).__name__,
                           test_case_name=self.def_name,
                           test_case_steps=self.list_steps,
                           start_time=self.start_time)
        self.driver.quit()
    # OK
    def test_01_HOME_Check_Internet_Image_Operation_when_Dual_WAN_is_off(self):
        self.key = 'HOME_01'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()

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
            goto_menu(driver, home_tab, 0)
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
            URL_LOGIN = get_config('URL', 'url')
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            URL_API = URL_LOGIN + '/api/v1/network/wan/0'
            METHOD = 'GET'
            BODY = None
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
            step_1_2_name = "1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. "
            list_check_in_step_1_2 = [
                f"Check IPv4 Information is: {list_expected[0]}",
                "Check WAN type and Connection Type list option are correct"
            ]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_3_name = "3. Check btn + is displayed when click btn |||."
            list_check_in_step_3 = ["Check Button more tab is appear"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_4_name = "4. Click + btn. Check re-direct Network>Internet"
            list_check_in_step_4 = [f"Check Current URL is {list_expected3[0]}"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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


        URL_API_DUAL_WAN = URL_LOGIN + '/api/v1/network/dualwan'
        URL_NETWORK_WAN = '/api/v1/network/wan/'
        METHOD = 'GET'
        BODY = None
        # Handle API

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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            _token = get_token(USER_LOGIN, PW_LOGIN)
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
            step_1_2_name = "Check IPv4 Information; Check WAN type in options, and Connection Type in options. "
            list_check_in_step_1_2 = [
                "Check IPv4 information for primary is correct",
                "Check IPv4 information for secondary is correct",
                "Check WAN type and Connection Type are correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check btn + is displayed when click btn |||. "
            list_check_in_step_3 = ["Check button more fab is appear"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_4_name = "4. Click + btn. Check re-direct Network>Internet. "
            list_check_in_step_4 = [f"Check current URL is: {list_expected4[0]}"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
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
            step_5_name = "5. Home page is displayed. "
            list_check_in_step_5 = ["Check Home page is appear"]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
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
            step_6_name = "6. Check btn + is displayed when click btn |||. "
            list_check_in_step_6 = ["Check Button more fab is appear"]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
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
            step_7_name = "7. Click + btn. Check re-direct Network>Internet. "
            list_check_in_step_7 = [f"Check current URL is: {list_expected7[0]}"]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
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
                             and (dict_wan['Connection Type'] in ['Dynamic IP', 'Satatic IP', 'PPPoE']) else False
            time.sleep(1)

            list_actual = [_actual, _check]
            list_expected = [_expected, return_true]
            step_1_2_name = "1,2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. "
            list_check_in_step_1_2 = [
                f"Check ipv4 information is: {list_expected[0]}",
                " Check WAN types and Connection Types are correct"
            ]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_1_name = "1. Check Internet Image is high light. "
            list_check_in_step_1 = ["Check Internet Image is active"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
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
            step_2_name = "2. Check IPv4 Information; Check WAN type in options, and Connection Type in options. "
            list_check_in_step_2 = [
                "Check IPv4 Information is correct",
                "Check WAN type and connection type are correct"
            ]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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

        # ===========================================================
        factory_dut()
        # ===========================================================

        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API_WAN_V4 = URL_LOGIN + '/api/v1/network/wan/0'
        METHOD = 'GET'
        BODY = None
        VALUE_DNS2 = '0.0.0.0'
        VALUE_DNS2_SPLIT = VALUE_DNS2.split('.')
        # _token = get_token(USER_LOGIN, PW_LOGIN)
        # Call API
        # get_wan = call_api(URL_API_WAN_V4, METHOD, BODY, _token)['ipv4']['address']
        # ==================================================
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
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
            step_1_name = "1. Check Internet Image is high light. "
            list_check_in_step_1 = ["Check Internet Image is active"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_name = " 2. Check Information display. Check WAN type in options, and Connection Type in options. "
            list_check_in_step_2 = [
                "Check Information display is correct",
                "Check WAN type and connection types are correct"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_08_HOME_Check_Router_Wireless_Image_operation(self):
        self.key = 'HOME_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        # ================================================
        try:
            grand_login(driver)
            time.sleep(1)

            router_wireless_icon = driver.find_element_by_css_selector(home_img_lan_connection)
            router_wireless_icon_check_active = 'active' in router_wireless_icon.get_attribute('class')
            router_wireless_icon.click()

            time.sleep(1)
            #
            check_2g_active = len(
                driver.find_elements_by_css_selector('.lan-connection>a.active:not(.disconnect24)')) > 0
            check_5g_active = len(
                driver.find_elements_by_css_selector('.lan-connection>a.active:not(.disconnect5)')) > 0

            list_actual1 = [router_wireless_icon_check_active, check_2g_active, check_5g_active]
            list_expected1 = [return_true] * 3
            step_1_2_name = "1, 2. Check Icon is active, Color of 2.4GHz and 5GHz. "
            list_check_in_step_1_2 = [
                "Check Router wireless icon is active",
                "Check 2G is active",
                "Check 5G is active",
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            #
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            block_2g = driver.find_elements_by_css_selector(ele_adv_wireless_card)[0]

            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Radio':
                    v.find_element_by_css_selector(select).click()
                    break

            block_2g.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            block_2g = driver.find_elements_by_css_selector(ele_adv_wireless_card)[0]
            labels_2 = block_2g.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'Radio':
                    check_radio_box = v.find_element_by_css_selector(input).is_selected()
                    break

            list_actual3 = [check_radio_box]
            list_expected3 = [return_false]
            step_3_name = "3. Goto Advanced> Wireless. Disabled 2G Radio. Check Disabled. "
            list_check_in_step_3 = ["Check 2G Radio is disabled"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong.')

        try:
            # Go home
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            check_2g_active_2 = len(
                driver.find_elements_by_css_selector('.lan-connection>a.active.disconnect24')) > 0
            check_5g_active_2 = len(
                driver.find_elements_by_css_selector('.lan-connection>a.active:not(.disconnect5)')) > 0

            list_actual4 = [check_2g_active_2, check_5g_active_2]
            list_expected4 = [return_true] * 2
            step_4_name = "4. Check 2GHz image is disconnected, 5GHz image is connected. "
            list_check_in_step_4 = [
                "Check 2GHz image is not connect",
                "Check 5GHz image is connect"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4. Assertion wong.')

        try:
            #
            goto_menu(driver, advanced_tab, advanced_wireless_tab)

            block_5g = driver.find_elements_by_css_selector(ele_adv_wireless_card)[1]

            labels_3 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_3 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_3, values_3):
                if l.text == 'Radio':
                    v.find_element_by_css_selector(select).click()
                    break

            block_5g.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            block_5g = driver.find_elements_by_css_selector(ele_adv_wireless_card)[1]
            labels_4 = block_5g.find_elements_by_css_selector(label_name_in_2g)
            values_4 = block_5g.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_4, values_4):
                if l.text == 'Radio':
                    check_radio_box = v.find_element_by_css_selector(input).is_selected()
                    break

            list_actual5 = [check_radio_box]
            list_expected5 = [return_false]
            step_5_name = "5. Goto Advanced> Wireless. Disabled 5G Radio. Check Disabled. "
            list_check_in_step_5 = ["Check 5G radio is disabled"]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5. Assertion wong.')

        try:
            # Go home
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            check_2g_active_3 = len(
                driver.find_elements_by_css_selector('.lan-connection>a.active.disconnect24')) > 0
            check_5g_active_3 = len(
                driver.find_elements_by_css_selector('.lan-connection>a.active.disconnect5')) > 0

            list_actual6 = [check_2g_active_3, check_5g_active_3]
            list_expected6 = [return_true] * 2
            step_6_name = "6. Check 2GHz image is disconnected, 5GHz image is disconnected."
            list_check_in_step_6 = ["Check 2GHz image is not connect", "Check 5GHz image is not connect"]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_09_HOME_Check_Router_Wireless_page(self):
        self.key = 'HOME_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)

            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(5)

            block_left = driver.find_element_by_css_selector(left)
            block_card = block_left.find_elements_by_css_selector(card_cls)

            lan_title = block_card[0].find_element_by_css_selector(title_tabs_cls).text
            lan_card_tabs = block_card[0].find_elements_by_css_selector(card_tabs_cls)
            lan_card_tabs_v4 = lan_card_tabs[0].text
            lan_card_tabs_v6 = lan_card_tabs[1].text
            icon_fab = len(block_card[0].find_elements_by_css_selector(home_icon_fab)) != 0

            list_actual1 = [lan_title, lan_card_tabs_v4, lan_card_tabs_v6, icon_fab]
            list_expected1 = ['LAN', 'IPv4', 'IPv6', return_true]
            step_3_1_name = "3.1 Check LAN block: Title, IPv4, IPv6, Icon ||| displayed. "
            list_check_in_step_3_1 = [
                f"Check LAN title is: {list_expected1[0]}",
                f"Check LAN card tabs v4 label is: {list_expected1[1]}",
                f"Check LAN card tabs v6 label is: {list_expected1[2]}",
                f"Check Icon fab is appear",
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_1_name,
                    list_check_in_step=list_check_in_step_3_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_1_name,
                    list_check_in_step=list_check_in_step_3_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_2_name = "3.2 Check Wireless block: Title, 2.4GHz, 5GHz, Icon ||| displayed. "
            list_check_in_step_3_2 = [
                f"Check Title is: {list_expected2[0]}",
                f"Check 2G card tabs label is: {list_expected2[1]}",
                f"Check 5G card tabs label is: {list_expected2[2]}",
                f"Check Icon fab is appear",
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_2_name,
                    list_check_in_step=list_check_in_step_3_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_2_name,
                    list_check_in_step=list_check_in_step_3_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3.2 Assertion wong.')

        try:
            information_title = block_card[1].find_element_by_css_selector(title_tabs_cls).text
            cpu_status_title = block_card[2].find_element_by_css_selector('h3').text

            ethernet_title = block_card_right[1].find_element_by_css_selector(title_tabs_cls).text
            memory_status_title = block_card_right[2].find_element_by_css_selector('h3').text

            list_actual3 = [information_title, cpu_status_title, ethernet_title, memory_status_title]
            list_expected3 = ['Information', 'CPU Status', 'Ethernet Port Status', 'Memory Status']
            step_3_3_name = "3.3 Check Information, CPU Status, Ethernet Port Status, Memory Status. "
            list_check_in_step_3_3 = [
                f"Check label information is: {list_expected3[0]}",
                f"Check label CPU status is: {list_expected3[1]}"
                f"Check label Ethernet Port Status is: {list_expected3[2]}"
                f"Check label Memory Status is: {list_expected3[3]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_3_name,
                    list_check_in_step=list_check_in_step_3_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_3_name,
                    list_check_in_step=list_check_in_step_3_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
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
            step_3_name = "3 Check LAN block information"
            list_check_in_step_3 = [
                "Check List LAN value is correct",
                "Check List LAN label is correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_4_name = "4. Check LAN block information IPv6: Check Label. "
            list_check_in_step_4 = ["Check List label is correct"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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

        try:
            grand_login(driver)
            time.sleep(1)

            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(home_icon_fab)) == 0:
                driver.find_element_by_css_selector(home_img_connection).click()
                time.sleep(1)
                driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(1)
            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == 'IPv4':
                    t.click()
                    break
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
            step_3_4_name = "3, 4. Click ||| btn; Check Display +; Click +; Check Display target IPv4 page. "
            list_check_in_step_3_4 = [
                "Check button more fab appear",
                f"Check Current tab is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('3, 4. Assertion wong.')

        try:
            goto_menu(driver, ele_home_tab, 0)
            time.sleep(1)
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(home_icon_fab)) == 0:
                driver.find_element_by_css_selector(home_img_connection).click()
                time.sleep(1)
                driver.find_element_by_css_selector(home_img_lan_connection).click()
                time.sleep(1)
            card_tabs = driver.find_elements_by_css_selector(card_tabs_cls)
            for t in card_tabs:
                if t.text == 'IPv6':
                    t.click()
                    break
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
            step_5_name = "5. Click ||| btn; Check Display +; Click +; Check Display target IPv6 page"
            list_check_in_step_5 = [
                "Check Icon more fab is appear",
                f"Check Current tab is: {list_expected2[1]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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

        # ===========================================================
        factory_dut()
        # ===========================================================

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
            step_3_name = "3. Check Information of WL 2.4GHZ: SSID, Sercurity, PW, MAC address. "
            list_check_in_step_3 = [
                f"Check SSID is :{list_expected1[0]}",
                f"Check Sercurity is :{list_expected1[1]}",
                "Check password is existed",
                "Check MAC address format is valid"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_4_name = "4. Check Information of WL 5GHZ: SSID, Sercurity, PW, MAC address"
            list_check_in_step_4 = [
                f"Check SSID is :{list_expected2[0]}",
                f"Check Sercurity is :{list_expected2[1]}",
                "Check password is existed",
                "Check MAC address format is valid"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_3_name = "3. Click + btn. Check re-direct Network>LAN. "
            list_check_in_step_3 = [f"Check current tab URL is: {list_expected[0]}"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_3_name = "3. Check Information title, Model name, End of Serial number, " \
                          "type of build time, firm version,  Text of button, Color. "
            list_check_in_step_3 = [
                f"Check block title is: {list_expected1[0]}",
                [
                    "Check model name is correct",
                    f"Check Condition Serial number end with '{SERIAL_NUMBER}' is correct",
                    f"Check Firmware version is: {firmware_version}",
                    "Check Condition 'Build time match has %Y.%m.%d %H:%M:%S format' is correct'"
                ],
                f"Check text of button update is: {list_expected1[2]}",
                f"Check button of date color is: {list_expected1[3]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('3. Assertion wong.')

        try:
            ActionChains(driver).move_to_element(check_for_update).click().perform()
            time.sleep(3)
            check_popup = len(driver.find_elements_by_css_selector(ele_check_for_update_title)) != 0

            list_actual2 = [check_popup]
            list_expected2 = [return_true]
            step_4_name = "4. Check pop up appear. "
            list_check_in_step_4 = ["Check After click update, a popup is appear"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_15_HOME_Check_Memory_Status_Table(self):
        self.key = 'HOME_15'
        self.def_name = get_func_name()
        self.list_steps = []
        list_step_fail = []
        try:
            from seleniumwire import webdriver
        except:
            os.system('pip install selenium-wire')
            from seleniumwire import webdriver
        driver2 = webdriver.Chrome(driver_path)  # open chrome
        driver2.maximize_window()


        try:
            grand_login(driver2)
            time.sleep(1)

            # CLick Wireless Image
            driver2.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)
            memory_block = driver2.find_element_by_css_selector(ele_memory_card)
            memory_label = [i.text for i in memory_block.find_elements_by_css_selector('.legend-name')]

            memory_chart_displayed = len(memory_block.find_elements_by_css_selector('#memory-chart')) > 0
            # Get information API
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/gateway/statuses/memoryUsage'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res3 = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_has_key_memory = [
                res3.get('total') is not None,
                res3.get('free') is not None
            ]

            list_actual1 = [[memory_label, memory_chart_displayed],
                            check_has_key_memory]
            list_expected1 = [[['Free Memory', 'Total Memory'], return_true],
                              [return_true] * 2]
            step_1_2_1_name = "1, 2.1 Login. Check list label, Graph displayed, API has key total and free. "
            list_check_in_step_1_2_1 = [
                [
                    "Check list label is correct",
                    "Check graph is appear"
                ],
                [
                    "Check Condition 'API has key total' is correct",
                    "Check Condition 'API has key free' is correct",
                ]
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_1_name,
                    list_check_in_step=list_check_in_step_1_2_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_1_name,
                    list_check_in_step=list_check_in_step_1_2_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2.1 . Assertion wong.')

        try:
            check_request_update = False
            del driver2.requests
            while True:
                _tmp_rq = driver2.requests
                _tmp_rq_path = [r.path for r in _tmp_rq if r.path == _URL_API]
                if len(_tmp_rq_path) > 0:
                    time.sleep(2)
                    _tmp_rq_after = driver2.requests
                    _tmp_rq_after_path = [r.path for r in _tmp_rq_after if r.path == _URL_API]
                    if _tmp_rq_path.count(_URL_API) + 1 == _tmp_rq_after_path.count(_URL_API):
                        check_request_update = True
                    break
            driver2.quit()
            list_actual2 = [check_request_update]
            list_expected2 = [return_true]
            step_2_2_name = "2.2 Check Request recalled each 2 seconds.  "
            list_check_in_step_2_2 = ["Check Request recalled each 2 seconds success"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2.2. Assertion wong.')
            self.list_steps.append('[END TC]')

        self.assertListEqual(list_step_fail, [])

    def test_16_HOME_Check_CPU_Status_Table(self):
        self.key = 'HOME_16'
        self.def_name = get_func_name()
        self.list_steps = []
        list_step_fail = []
        try:
            from seleniumwire import webdriver
        except:
            os.system('pip install selenium-wire')
            from seleniumwire import webdriver
        driver3 = webdriver.Chrome(driver_path)  # open chrome
        driver3.maximize_window()
        try:
            grand_login(driver3)
            time.sleep(1)
            # CLick Wireless Image
            driver3.find_element_by_css_selector(home_img_lan_connection).click()
            time.sleep(2)
            cpu_block = driver3.find_element_by_css_selector(ele_cpu_card)
            cpu_core_1_label = cpu_block.find_element_by_css_selector('.text-1').text
            cpu_core_2_label = cpu_block.find_element_by_css_selector('.text-2').text
            cpu_chart_displayed = len(cpu_block.find_elements_by_css_selector('#cpu-chart')) > 0
            time.sleep(2)
            # Get information API
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/gateway/statuses/cpuUsage'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            res2 = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_has_key = [
                res2[0].get('name') == 'Core 1',
                res2[0].get('percentage') is not None,
                res2[1].get('name') == 'Core 2',
                res2[1].get('percentage') is not None
            ]

            list_actual1 = [[cpu_core_1_label, cpu_core_2_label, cpu_chart_displayed],
                            check_has_key]
            list_expected1 = [['Core1', 'Core2', return_true],
                              [return_true] * 4]
            step_1_2_1_name = "1, 2.1 Login. Check list label, Graph displayed, API has key total and free. "
            list_check_in_step_1_2_1 = [
                [
                    "Check cpu core1 label is correct",
                    "Check cpu core2 label is correct",
                    "Check cpu chart is appear"
                ],
                [
                    "Check Condition 'API has key name core 1' is correct",
                    "Check Condition 'API has key percentage core 1' is correct",
                    "Check Condition 'API has key name core 2' is correct",
                    "Check Condition 'API has key percentage core 2' is correct",
                ]

            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_1_name,
                    list_check_in_step=list_check_in_step_1_2_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_1_name,
                    list_check_in_step=list_check_in_step_1_2_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2.1 . Assertion wong.')

        try:
            check_request_update = False
            time.sleep(1)
            del driver3.requests
            while True:
                _tmp_rq = driver3.requests
                print(_tmp_rq)
                _tmp_rq_path = [r.path for r in _tmp_rq if r.path == _URL_API]
                if len(_tmp_rq_path) > 0:
                    time.sleep(2)
                    _tmp_rq_after = driver3.requests
                    print(_tmp_rq_after)
                    _tmp_rq_after_path = [r.path for r in _tmp_rq_after if r.path == _URL_API]
                    if (_tmp_rq_after_path.count(_URL_API) - _tmp_rq_path.count(_URL_API)) >= 1:
                        check_request_update = True
                    break
            time.sleep(1)
            list_actual2 = [check_request_update]
            list_expected2 = [return_true]
            step_2_2_name = "2.2 Check Request recalled each 2 seconds.  "
            list_check_in_step_2_2 = ["Check Request recalled each 2 seconds success"]
            driver3.quit()
            time.sleep(1)
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2.2. Assertion wong.')
            self.list_steps.append('[END TC]')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_18_HOME_Check_USB_Image_Operation(self):
        self.key = 'HOME_18'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
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
            step_2_name = "2. Check USB Image selected, Check number of USB. "
            list_check_in_step_2 = [
                "Check USB Image is selected",
                f"Check number of USB is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check Title, Exist button |||, Device name, Total size, not null, " \
                          "space used, availabled, space bar not null, Btn Remove text. "
            list_check_in_step_3 = [
                f"Check Title is: {list_expected1[0]}",
                "Check icon fab is appear",
                [
                    "Check device name value is not null",
                    "Check total size value is not null",
                ],
                "Check space used not null",
                "Check space available not null",
                "Check space bar not null",
                "Check text of button remove correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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

            # Click to =
            icon_fab_displayed = False
            icon_more_fab_displayed = False
            if len(usb_card.find_elements_by_css_selector(home_icon_fab)) > 0:
                usb_card.find_element_by_css_selector(home_icon_fab).click()
                icon_fab_displayed = True
                # Btn more fab is displayed
                time.sleep(1)
                if len(usb_card.find_elements_by_css_selector(home_icon_more_fab)) > 0:
                    # more_fab = usb_card.find_element_by_css_selector(home_icon_more_fab).is_displayed()
                    icon_more_fab_displayed = True
                    # Click to icon more fab
                    driver.find_element_by_css_selector(home_icon_more_fab).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)

            current_tab = detect_current_menu(driver)

            list_actual1 = [icon_fab_displayed, icon_more_fab_displayed, current_tab]
            list_expected1 = [return_true, return_true, ('MEDIA SHARE', 'USB')]
            step_1_2_3_name = "1,2,3. Click and check display icon ||| btn; Click and check display icon +; " \
                              "Check Display target USB page. "
            list_check_in_step_1_2_3 = [
                "Check icon fab is appear",
                "Check icon more fab is appear",
                f"Check Current tab is: {list_expected1[2]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1,2, 3. Assertion wong.')

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
            step_3_4_5_name = "3,4,5. Check popup confirm text, popup complete text, popup disappear. "
            list_check_in_step_3_4_5 = [
                f"Check confirm text is: {list_expected1[0]}",
                f"Check confirm remove text is: {list_expected1[1]}",
                "Check popup is not displayed"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check Server title, icon fab, value fields."
            list_check_in_step_3 = [
                f"Check Server title is: {list_expected1[0]}",
                "Check icon fab is exist",
                "Check FTP Server is off",
                "Check Windows Network (Samba) is off",
                "Check Media Server (DLNA) is off"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click ||| btn; Check Display +; Click +; Check Display target USB Server page. "
            list_check_in_step_3 = [
                "Check button more fab is appear",
                f"Check current tab is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Click Device icon, Check number of device. "
            list_check_in_step_3 = [f"Check number of device is: {list_expected1[0]}"]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_2_name = "2. Check title of table."
            list_check_in_step_2 = [
                f"Check text of button 1 in table device connectivity is: {list_expected1[0]}",
                f"Check text of button 2 in table device connectivity is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )

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
            step_3_1_name = " 3.1 Check value rows displayed on Connected Devices Page."
            list_check_in_step_3_1 = [
                f"Check Value rows displayed on Connected Devices Page are: {list_expected3[0]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_1_name,
                    list_check_in_step=list_check_in_step_3_1,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_1_name,
                    list_check_in_step=list_check_in_step_3_1,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_3_2_name = "3.2 Check value rows displayed on Disconnected Devices Page."
            list_check_in_step_3_2 = [
                f"Check value rows displayed on Disconnected Devices Page are: {list_expected4[0]}"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_2_name,
                    list_check_in_step=list_check_in_step_3_2,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_2_name,
                    list_check_in_step=list_check_in_step_3_2,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
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
            step_1_2_3_name = "1, 2, 3. Check Connected Devices, [Refresh], Local Network, Device name, " \
                              "Interface, MAC Address, IP Address, Edit icon are displayed"
            list_check_in_step_1_2_3 = [
                "Check Title tab is correct",
                "Check Button refresh is displayed",
                f"Check Local network title is: {list_expected1[2]}",
                f"Check connect columns title are: {list_expected1[3]}",
                "Check edit button is displayed"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')

            list_step_fail.append('1, 2, 3. Assertion wong.')

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
            step_1_2_name = "1, 2. Check default tab in Devices, number of devices."
            list_check_in_step_1_2 = [
                f"Check label of 'default tab in Devices' is: {list_expected1[0]}",
                f"Check number of devices is: {list_expected1[1]}"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2. Assertion wong.')

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
            step_3_name = "3. Check default tab in Devices, number of devices."
            list_check_in_step_3 = [
                f"Check image dispalyed is: {list_expected3[0]}",
                "Check format of MAC address is valid",
                "Check format of IP address is valid",
                "Check Condition 'Port is start with LAN Port' is correct",
                f"Check List label is: {list_expected3[4]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3. Assertion wong.')

        try:
            time.sleep(5)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(10)
            write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
            time.sleep(3)

            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(1)
            self.list_steps.append('[Pass] 3.2 Connect wifi Successfully.')
        except:
            self.list_steps.append('[Fail] 3.2 Connect wifi Fail')
            list_step_fail.append('3.2 Assertion wong.')

        try:
            time.sleep(5)
            # Re-Load
            driver.refresh()
            time.sleep(7)
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
            list_check_in_step_4 = [
                f"Check image dispalyed is: {list_expected5[0]}",
                "Check format of MAC address is valid",
                "Check format of IP address is valid",
                "Check Condition 'Wifi is Wi-Fi 2.4GHz' is correct",
                f"Check List label is: {list_expected5[4]}"
            ]
            step_4_name = "4. Check default tab in Devices, number of devices."
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_31_HOME_Reserved_IP_registration_deletion_confirmation(self):
        self.key = 'HOME_31'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
        # current_pw = get_config('ACCOUNT', 'password')
        factory_dut()

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            # time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            wait_popup_disappear(driver, dialog_loading)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual1 = [check_dialog_display]
            list_expected1 = [return_true]
            step_2_name = "2. Click Edit; Check popup display."
            list_check_in_step_2 = [
                "Check popup is displayed"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check confirm add reserved IP msg, Click Cancel-> Check popup disappear. " \
                          "Click add again -> Click OK -> Check add icon change to delete icon"
            list_check_in_step_3 = [
                f"Check confirm message is: {exp_confirm_msg_add_resserve_ip}",
                "Check popup confirm is not displayed",
                "Check Condition 'Add icon change to delete icon' is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_4_name = "4. Add reserved IP -> Check add successfully in Network Lan"
            list_check_in_step_4 = ["Check Add reserved IP in network lan success"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4. Assertion wong.')

        # Delete Reserved IP, Check delete in Network LAN
        try:
            time.sleep(0.5)
            # Goto Home
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            # time.sleep(2)
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
            wait_popup_disappear(driver, dialog_loading)

            check_add_in_lan = True
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = False

            list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
            list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
            step_5_6_7_name = "5,6,7. Delete reserved IP -> Check Delete successfully in Network Lan"
            list_check_in_step_5_6_7 = [
                "Check Delete reserved IP in network lan success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_7_name,
                    list_check_in_step=list_check_in_step_5_6_7,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_7_name,
                    list_check_in_step=list_check_in_step_5_6_7,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5,6,7. Assertion wong.')

        # Connect Wifi
        try:
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
            wifi_2g_password = wireless_check_pw_eye(driver, block_2g, change_pw=False)

            check_connect = connect_wifi_by_command(wifi_2g_name, wifi_2g_password)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)

            list_actual8 = [check_connect]
            list_expected8 = [wifi_2g_name]
            step_8_0_name = "8.0 Connect wifi Successfully."
            list_check_in_step_8_0 = [f"Check connected wifi name is: {wifi_2g_name}"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_0_name,
                    list_check_in_step=list_check_in_step_8_0,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_0_name,
                    list_check_in_step=list_check_in_step_8_0,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('8.0 Assertion wong.')

        try:
            # Refresh page
            driver.refresh()
            wait_popup_disappear(driver,dialog_loading)

            goto_menu(driver, home_tab, 0)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(2)

            check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0

            list_actual8 = [check_dialog_display]
            list_expected8 = [return_true]
            step_8_1_name = "8.1. Click Edit; Check popup display."
            list_check_in_step_8_1 = ["Check popup is displayed"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_1_name,
                    list_check_in_step=list_check_in_step_8_1,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_1_name,
                    list_check_in_step=list_check_in_step_8_1,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
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

            list_actual9 = [check_confirm_msg, check_confirm_pop_disappear, check_delete_icon]
            list_expected9 = [exp_confirm_msg_add_resserve_ip, return_true, return_true]
            step_8_2_name = "8.2. Check confirm add reserved IP msg, Click Cancel-> Check popup disappear. " \
                            "Click add again -> Click OK -> Check add icon change to delete icon"
            list_check_in_step_8_2 = [
                f"Check confirm add reserved IP is: {exp_confirm_msg_add_resserve_ip}",
                f"Check confirm add reserved IP is not displayed",
                "Check Condition 'add icon change to delete icon' is correct"
            ]
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_2_name,
                    list_check_in_step=list_check_in_step_8_2,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_2_name,
                    list_check_in_step=list_check_in_step_8_2,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            list_step_fail.append('8.2. Assertion wong.')

        try:
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.5)
            # Table first row
            first_row = driver.find_element_by_css_selector(ele_table_row)
            # Get information
            device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
            device_ip = first_row.find_element_by_css_selector(ip_address_cls).text

            goto_menu(driver, network_tab, network_lan_tab)
            wait_popup_disappear(driver, dialog_loading)

            check_add_in_lan = False
            reserved_block_rows = driver.find_elements_by_css_selector(rows)
            if len(reserved_block_rows) > 0:
                for r in reserved_block_rows:
                    if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
                        if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
                            check_add_in_lan = True

            list_actual10 = [check_add_in_lan]
            list_expected10 = [return_true]
            step_8_3_name = "8.3. Add reserved IP -> Check add successfully in Network Lan"
            list_check_in_step_8_3 = [
                "Check Add reserved IP success"
            ]
            check = assert_list(list_actual10, list_expected10)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_3_name,
                    list_check_in_step=list_check_in_step_8_3,
                    list_actual=list_actual10,
                    list_expected=list_expected10
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_3_name,
                    list_check_in_step=list_check_in_step_8_3,
                    list_actual=list_actual10,
                    list_expected=list_expected10
                )
            )
            list_step_fail.append('8.3. Assertion wong.')

        try:
            # Goto Home
            goto_menu(driver, home_tab, 0)
            wait_popup_disappear(driver, dialog_loading)
            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            # time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            # Click Edit
            driver.find_element_by_css_selector(edit_cls).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
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

            list_actual11 = [check_confirm_delete_msg, check_add_in_lan]
            list_expected11 = [exp_confirm_msg_delete_resserve_ip, return_true]
            step_8_4_name = "8.4. Delete reserved IP -> Check Delete successfully in Network Lan"
            list_check_in_step_8_4 = [
                f"Check confirm message delete reserved IP is: {exp_confirm_msg_delete_resserve_ip}",
                "Check Delete reserved IP success"
            ]
            check = assert_list(list_actual11, list_expected11)
            interface_connect_disconnect('Ethernet', 'Enable')
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_4_name,
                    list_check_in_step=list_check_in_step_8_4,
                    list_actual=list_actual11,
                    list_expected=list_expected11
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_4_name,
                    list_check_in_step=list_check_in_step_8_4,
                    list_actual=list_actual11,
                    list_expected=list_expected11
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('8.4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    # # HOME 32 chua dc
    # def test_32_HOME_Mac_Filtering_registration_deletion_confirmation(self):
    #     self.key = 'HOME_32'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
    #     current_pw = get_config('ACCOUNT', 'password')
    #
    #     # Disconnect Wireless, connect LAN
    #     try:
    #         os.system(f'netsh wlan disconnect')
    #         time.sleep(5)
    #
    #         os.system(f'python {nw_interface_path} -i Ethernet -a enable')
    #         time.sleep(10)
    #         self.list_steps.append('[Pass] Precondition Successfully.')
    #     except:
    #         self.list_steps.append('[Fail] Precondition Fail')
    #         list_step_fail.append('Assertion wong.')
    #
    #     # Check popup appear after click Edit
    #     try:
    #         grand_login(driver)
    #
    #         # CLick Device Image
    #         driver.find_element_by_css_selector(home_img_device_connection).click()
    #         time.sleep(2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Table first row
    #         first_row = driver.find_element_by_css_selector(ele_table_row)
    #         # Get information
    #         before_device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
    #
    #         # Click Edit
    #         driver.find_element_by_css_selector(edit_cls).click()
    #         time.sleep(2)
    #
    #         check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0
    #
    #         list_actual1 = [check_dialog_display]
    #         list_expected1 = [return_true]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 2. Click Edit; Check popup display.'
    #                                f'Actual: {str(list_actual1)}. '
    #                                f'Expected: {str(list_expected1)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2. Click Edit; Check popup display. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         list_step_fail.append('2. Assertion wong.')
    #
    #     # Mac Filtering OK
    #     try:
    #         # Click Mac Filtering
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
    #                 break
    #         if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
    #             # Click
    #             add_mac_btn.click()
    #         time.sleep(0.2)
    #         # Check confirm message
    #         check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
    #         time.sleep(0.2)
    #         # Click Cancel
    #         driver.find_element_by_css_selector(btn_cancel).click()
    #         time.sleep(0.2)
    #         # Check popup confirm disappear
    #         check_confirm_pop_disappear = len(driver.find_elements_by_css_selector(confirm_dialog_msg)) == 0
    #
    #         # Click Mac Filtering
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
    #                 break
    #         # Click mac
    #         if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
    #             add_mac_btn.click()
    #         time.sleep(0.2)
    #         # Click OK
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(0.2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Switch to disconnect devices
    #         driver.find_element_by_css_selector(ele_second_tab).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #
    #         # Table first row
    #         first_row = driver.find_element_by_css_selector(ele_table_row)
    #         # Get information
    #         after_device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
    #
    #         list_actual3 = [check_confirm_msg, check_confirm_pop_disappear, before_device_mac]
    #         list_expected3 = [exp_confirm_msg_add_mac_filtering, return_true, after_device_mac]
    #         check = assert_list(list_actual3, list_expected3)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 3, 4. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
    #                                'Click add again -> Click OK -> Check MAC display in Disconnect Devices'
    #                                f'Actual: {str(list_actual3)}. '
    #                                f'Expected: {str(list_expected3)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 3, 4. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
    #             'Click add again -> Click OK -> Check MAC display in Disconnect Devices'
    #             f'Actual: {str(list_actual3)}. '
    #             f'Expected: {str(list_expected3)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('3, 4. Assertion wong.')
    #
    #         # Connect Wifi
    #     try:
    #         time.sleep(5)
    #         new_2g_wf_name = api_change_wifi_setting(URL_2g)
    #         time.sleep(3)
    #         write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
    #         time.sleep(3)
    #
    #         # Connect Default 2GHz
    #         os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
    #         time.sleep(5)
    #
    #         os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
    #         time.sleep(110)
    #
    #         os.system(f'python {nw_interface_path} -i Ethernet -a disable')
    #         time.sleep(1)
    #         self.list_steps.append('8.0 [Pass] Connect wifi Successfully.')
    #     except:
    #         self.list_steps.append('8.0 [Fail] Connect wifi Fail')
    #         list_step_fail.append('8.0 Assertion wong.')
    #
    #
    #
    #
    #
    #
    #
    #     # Verify Mac Filtering in Network Lan
    #     try:
    #         # Click Cancel
    #         driver.find_element_by_css_selector(btn_cancel).click()
    #         time.sleep(1)
    #         # Table first row
    #         first_row = driver.find_element_by_css_selector(ele_table_row)
    #         # Get information
    #         device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
    #         device_ip = first_row.find_element_by_css_selector(ip_address_cls).text
    #
    #         goto_menu(driver, network_tab, network_lan_tab)
    #         time.sleep(1)
    #
    #         check_add_in_lan = False
    #         reserved_block_rows = driver.find_elements_by_css_selector(rows)
    #         if len(reserved_block_rows) > 0:
    #             for r in reserved_block_rows:
    #                 if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
    #                     if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
    #                         check_add_in_lan = True
    #
    #         list_actual4 = [check_add_in_lan]
    #         list_expected4 = [return_true]
    #         check = assert_list(list_actual4, list_expected4)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 4. Add Mac Filtering -> Check add successfully in Network Lan'
    #                                f'Actual: {str(list_actual4)}. '
    #                                f'Expected: {str(list_expected4)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 4. Add Mac Filtering -> Check add successfully in Network Lan'
    #             f'Actual: {str(list_actual4)}. '
    #             f'Expected: {str(list_expected4)}')
    #         list_step_fail.append('4. Assertion wong.')
    #
    #     # Delete Mac Filtering, Check delete in Network LAN
    #     try:
    #         time.sleep(3)
    #         # Goto Home
    #         goto_menu(driver, home_tab, 0)
    #         time.sleep(1)
    #         wait_popup_disappear(driver, dialog_loading)
    #         # CLick Device Image
    #         driver.find_element_by_css_selector(home_img_device_connection).click()
    #         time.sleep(2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Click Edit
    #         driver.find_element_by_css_selector(edit_cls).click()
    #         time.sleep(2)
    #         # Click Mac Filtering
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
    #                 break
    #         # Click
    #         if len(add_mac_btn.find_elements_by_css_selector(delete_cls)) > 0:
    #             add_mac_btn.click()
    #
    #         time.sleep(0.2)
    #         # Check confirm message
    #         check_confirm_delete_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
    #         time.sleep(0.2)
    #         # Click ok
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(0.2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #          # Click Cancel reserved Popup
    #         driver.find_element_by_css_selector(btn_cancel).click()
    #         time.sleep(1)
    #         # Table first row
    #         first_row = driver.find_element_by_css_selector(ele_table_row)
    #         # Get information
    #         device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
    #         device_ip = first_row.find_element_by_css_selector(ip_address_cls).text
    #
    #         goto_menu(driver, network_tab, network_lan_tab)
    #         time.sleep(1)
    #
    #         check_add_in_lan = True
    #         reserved_block_rows = driver.find_elements_by_css_selector(rows)
    #         if len(reserved_block_rows) > 0:
    #             for r in reserved_block_rows:
    #                 if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
    #                     if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
    #                         check_add_in_lan = False
    #
    #         list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
    #         list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
    #         check = assert_list(list_actual5, list_expected5)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 5,6,7. Delete Mac Filtering -> Check Delete successfully in Network Lan'
    #                                f'Actual: {str(list_actual5)}. '
    #                                f'Expected: {str(list_expected5)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 5,6,7. Delete Mac Filtering -> Check Delete successfully in Network Lan'
    #             f'Actual: {str(list_actual5)}. '
    #             f'Expected: {str(list_expected5)}')
    #         list_step_fail.append('5,6,7. Assertion wong.')
    #
    #     # Connect Wifi
    #     try:
    #         time.sleep(5)
    #         new_2g_wf_name = api_change_wifi_setting(URL_2g)
    #         time.sleep(3)
    #         write_data_to_xml(default_wifi_2g_path, new_name=new_2g_wf_name, new_pw=current_pw)
    #         time.sleep(3)
    #
    #         # Connect Default 2GHz
    #         os.system(f'netsh wlan add profile filename="{default_wifi_2g_path}"')
    #         time.sleep(5)
    #
    #         os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
    #         time.sleep(110)
    #
    #         os.system(f'python {nw_interface_path} -i Ethernet -a disable')
    #         time.sleep(1)
    #         self.list_steps.append('8.0 [Pass] Connect wifi Successfully.')
    #     except:
    #         self.list_steps.append('8.0 [Fail] Connect wifi Fail')
    #         list_step_fail.append('8.0 Assertion wong.')
    #
    #     try:
    #         # Refresh page
    #         driver.refresh()
    #         time.sleep(5)
    #
    #         goto_menu(driver, home_tab, 0)
    #         time.sleep(2)
    #         wait_popup_disappear(driver, dialog_loading)
    #         # CLick Device Image
    #         driver.find_element_by_css_selector(home_img_device_connection).click()
    #         time.sleep(2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Click Edit
    #         driver.find_element_by_css_selector(edit_cls).click()
    #         time.sleep(2)
    #
    #         check_dialog_display = len(driver.find_elements_by_css_selector(dialog_content)) > 0
    #
    #         list_actual1 = [check_dialog_display]
    #         list_expected1 = [return_true]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 8.1. Click Edit; Check popup display.'
    #                                f'Actual: {str(list_actual1)}. '
    #                                f'Expected: {str(list_expected1)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 8.1. Click Edit; Check popup display. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         list_step_fail.append('8.1. Assertion wong.')
    #
    #     try:
    #         # Click Mac Filtering
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
    #                 break
    #         # Click
    #         if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
    #             add_mac_btn.click()
    #         time.sleep(0.2)
    #         # Check confirm message
    #         check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
    #         time.sleep(0.2)
    #         # Click Cancel
    #         driver.find_element_by_css_selector(btn_cancel).click()
    #         time.sleep(0.2)
    #         # Check popup confirm disappear
    #         check_confirm_pop_disappear = len(driver.find_elements_by_css_selector(confirm_dialog_msg)) == 0
    #
    #         # Click Mac Filtering
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
    #                 break
    #         # Click reserved
    #         if len(add_mac_btn.find_elements_by_css_selector(add_class)) > 0:
    #             add_mac_btn.click()
    #         time.sleep(0.2)
    #         # Click OK
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(0.2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Check Reserved to "-"
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 check_delete_icon = f.find_element_by_css_selector(ele_icon_cls).get_attribute('class')
    #                 break
    #         check_delete_icon = check_delete_icon == 'icon delete'
    #
    #         list_actual3 = [check_confirm_msg, check_confirm_pop_disappear, check_delete_icon]
    #         list_expected3 = [exp_confirm_msg_add_mac_filtering, return_true, return_true]
    #         check = assert_list(list_actual3, list_expected3)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 8.2. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
    #                                'Click add again -> Click OK -> Check add icon change to delete icon'
    #                                f'Actual: {str(list_actual3)}. '
    #                                f'Expected: {str(list_expected3)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 8.2. Check confirm add Mac Filtering msg, Click Cancel-> Check popup disappear. '
    #             'Click add again -> Click OK -> Check add icon change to delete icon'
    #             f'Actual: {str(list_actual3)}. '
    #             f'Expected: {str(list_expected3)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('8.2. Assertion wong.')
    #
    #     try:
    #         # Click Cancel
    #         driver.find_element_by_css_selector(btn_cancel).click()
    #         time.sleep(1)
    #         # Table first row
    #         first_row = driver.find_element_by_css_selector(ele_table_row)
    #         # Get information
    #         device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
    #         device_ip = first_row.find_element_by_css_selector(ip_address_cls).text
    #
    #         goto_menu(driver, network_tab, network_lan_tab)
    #         time.sleep(1)
    #
    #         check_add_in_lan = False
    #         reserved_block_rows = driver.find_elements_by_css_selector(rows)
    #         if len(reserved_block_rows) > 0:
    #             for r in reserved_block_rows:
    #                 if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
    #                     if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
    #                         check_add_in_lan = True
    #
    #         list_actual4 = [check_add_in_lan]
    #         list_expected4 = [return_true]
    #         check = assert_list(list_actual4, list_expected4)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 8.3. Add Mac Filtering -> Check add successfully in Network Lan'
    #                                f'Actual: {str(list_actual4)}. '
    #                                f'Expected: {str(list_expected4)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 8.3 Mac Filtering -> Check add successfully in Network Lan'
    #             f'Actual: {str(list_actual4)}. '
    #             f'Expected: {str(list_expected4)}')
    #         list_step_fail.append('8.3. Assertion wong.')
    #
    #     try:
    #         # Goto Home
    #         goto_menu(driver, home_tab, 0)
    #         time.sleep(2)
    #         # CLick Device Image
    #         driver.find_element_by_css_selector(home_img_device_connection).click()
    #         time.sleep(2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Click Edit
    #         driver.find_element_by_css_selector(edit_cls).click()
    #         time.sleep(2)
    #         # Click Mac Filtering
    #         all_wrap_form = driver.find_elements_by_css_selector(home_wan_ls_fields)
    #         for f in all_wrap_form:
    #             if f.find_element_by_css_selector(home_wan_ls_label).text == 'MAC Filtering':
    #                 add_mac_btn = f.find_element_by_css_selector(ele_advanced_button)
    #                 break
    #         # Click
    #         if len(add_mac_btn.find_elements_by_css_selector(delete_cls)) > 0:
    #             add_mac_btn.click()
    #         time.sleep(0.2)
    #         # Check confirm message
    #         check_confirm_delete_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
    #         time.sleep(0.2)
    #         # Click ok
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(0.2)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Click Cancel reserved Popup
    #         driver.find_element_by_css_selector(btn_cancel).click()
    #         time.sleep(1)
    #         # Table first row
    #         first_row = driver.find_element_by_css_selector(ele_table_row)
    #         # Get information
    #         device_mac = first_row.find_element_by_css_selector(wol_mac_addr).text
    #         device_ip = first_row.find_element_by_css_selector(ip_address_cls).text
    #
    #         goto_menu(driver, network_tab, network_lan_tab)
    #         time.sleep(1)
    #
    #         check_add_in_lan = True
    #         reserved_block_rows = driver.find_elements_by_css_selector(rows)
    #         if len(reserved_block_rows) > 0:
    #             for r in reserved_block_rows:
    #                 if r.find_element_by_css_selector(ip_address_cls).text == device_ip:
    #                     if r.find_element_by_css_selector(mac_desc_cls).text.splitlines()[1] == device_mac:
    #                         check_add_in_lan = False
    #
    #         list_actual5 = [check_confirm_delete_msg, check_add_in_lan]
    #         list_expected5 = [exp_confirm_msg_delete_resserve_ip, return_true]
    #         check = assert_list(list_actual5, list_expected5)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 8.4. Delete Mac Filtering -> Check Delete successfully in Network Lan'
    #                                f'Actual: {str(list_actual5)}. '
    #                                f'Expected: {str(list_expected5)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 8.4. Delete Mac Filtering -> Check Delete successfully in Network Lan'
    #             f'Actual: {str(list_actual5)}. '
    #             f'Expected: {str(list_expected5)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('8.4. Assertion wong.')
    #
    #     self.assertListEqual(list_step_fail, [])
    # OK
    def test_33_HOME_Confirm_Parental_Control_information_display(self):
        self.key = 'HOME_33'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_API = get_config('URL', 'url') + '/api/v1/gateway/devices/1'

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
            step_2_name = "2. Click Edit; Check popup display."
            list_check_in_step_2 = ["Check popup is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_3_name = "3. Check Parental Control value in Web UI and API."
            list_check_in_step_3 = [
                f"Check Parental Control value in Web UI is: {list_expected3[0]}",
                f"Check Parental Control value in API is: false",
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_38_HOME_Check_Disconnected_Devices_information(self):
        self.key = 'HOME_38'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            # Connect client to DUT via wired
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            # Connect wireless
            _user = get_config('ACCOUNT', 'user')
            _pw = get_config('ACCOUNT', 'password')
            _token = get_token(_user, _pw)
            URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
            _res = call_api(URL_2g, 'GET', '', _token)
            ssid_2g = _res['name']

            write_data_to_xml(wifi_default_file_path,
                              new_name=ssid_2g)
            time.sleep(1)
            os.system(f'netsh wlan delete profile name="{ssid_2g}"')
            time.sleep(1)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(1)
            os.system(f'netsh wlan connect ssid="{ssid_2g}" name="{ssid_2g}"')
            time.sleep(10)

            # Disconnect wireless
            os.system('netsh wlan disconnect')
            time.sleep(3)

            self.list_steps.append('[Pass] Precondition successfully. Connect then disconnect wireless. Connect wired')
        except:
            self.list_steps.append('[Fail] Precondition fail. Connect then disconnect wireless. Connect wired')
            list_step_fail.append('Assertion wong.')

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            device_img = driver.find_element_by_css_selector(home_img_device)
            check_device_active = len(device_img.find_elements_by_css_selector(ele_active_cls)) > 0
            try:
                check_device_number = int(device_img.find_element_by_css_selector(ele_more_info_cls).text) > 0
            except:
                check_device_number = False
            # Click disconnected device
            driver.find_element_by_css_selector(ele_disconnect_device_tab).click()

            disconnect_table_display = len(driver.find_elements_by_css_selector(ele_disconnect_table)) > 0

            list_actual1 = [check_device_active, check_device_number, disconnect_table_display]
            list_expected1 = [return_true] * 3
            step_1_2_name = "1, 2. Login. Click Devices Image. " \
                            "Check device image active, Check device number > 0, Check Disconnect table display. "
            list_check_in_step_1_2 = [
                "Check Device is active",
                "Check Device number is correct",
                "Check Disconnect table is displayed"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            disconnect_table = driver.find_element_by_css_selector(ele_disconnect_table)
            list_disconnect_label = [i.text for i in
                                     disconnect_table.find_elements_by_css_selector(ele_disconnect_header)]
            btn_refresh_display = len(driver.find_elements_by_css_selector(ele_btn_refresh)) > 0
            disconnect_device_text = driver.find_elements_by_css_selector(card_tabs_cls)[1].text
            # API
            _user = get_config('ACCOUNT', 'user')
            _pw = get_config('ACCOUNT', 'password')
            _token = get_token(_user, _pw)
            URL_2g = get_config('URL', 'url') + '/api/v1/gateway/devices?connected=false'
            _res = call_api(URL_2g, 'GET', '', _token)

            _res_connected = _res[0]['connected'] is False
            _check_key_id = _res[0]['id'] is not None
            _check_key_name = _res[0].get("name") is not None
            _check_key_mac = _res[0].get("macAddress") is not None
            _check_key_last_connected = _res[0].get("lastConnected") is not None

            list_actual2 = [disconnect_device_text, btn_refresh_display, list_disconnect_label,
                            [_check_key_id, _res_connected, _check_key_name, _check_key_mac, _check_key_last_connected]]
            list_expected2 = ['Disconnected Devices', return_true,
                              ['Device Name', 'MAC Address', 'Last Access Date', 'Block'],
                              [return_true]*5]
            step_3_name = "3. Check client disconnected displayed: " \
                          "Disconnected Devices text, Existed refresh button, List header text. " \
                          "Check API: Connected value, Key id, name, mac, last connected. "
            list_check_in_step_3 = [
                f"Check card tab is: {list_expected2[0]}",
                "Check button refresh is displayed",
                f"Check list disconnect labels is: {list_expected2[2]}",
                [
                    "Check client id is not null",
                    "Check res connected is false",
                    "Check client name is not null",
                    "Check client mac is not null",
                    "Check client last connected is not null"
                ]
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3. Assertion wong.')

        try:
            write_data_to_xml(wifi_default_file_path,
                              new_name=ssid_2g)
            time.sleep(1)
            os.system(f'netsh wlan delete profile name="{ssid_2g}"')
            time.sleep(1)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(1)
            os.system(f'netsh wlan connect ssid="{ssid_2g}" name="{ssid_2g}"')
            time.sleep(10)

            #
            get_current_wifi_name = current_connected_wifi()

            list_actual4 = [get_current_wifi_name]
            list_expected4 = [ssid_2g]
            step_5_name = "5. Connect wireless of DUT. Check connect wireless successfully. "
            list_check_in_step_5 = [f"Check current wifi name is: {ssid_2g}"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('5. Assertion wong.')


        try:
            # Connect client to DUT via wired
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            #
            interface = subprocess.check_output('ipconfig', shell=True)
            check_ethernet_disconnected = 'Ethernet adapter Ethernet:' not in interface.decode('utf8')

            list_actual3 = [check_ethernet_disconnected]
            list_expected3 = [return_true]
            step_4_name = "4. Disconnect Ethernet."
            list_check_in_step_4 = ["Check Condition 'Ethernet is disconnected' is correct"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('4. Assertion wong.')

        try:
            driver.refresh()
            time.sleep(5)
            driver.find_element_by_css_selector(ele_disconnect_device_tab).click()
            time.sleep(1)
            disconnect_table = driver.find_element_by_css_selector(ele_disconnect_table)
            list_disconnect_label = [i.text for i in
                                     disconnect_table.find_elements_by_css_selector(ele_disconnect_header)]
            btn_refresh_display = len(driver.find_elements_by_css_selector(ele_btn_refresh)) > 0
            disconnect_device_text = driver.find_elements_by_css_selector(card_tabs_cls)[1].text
            # API
            _user = get_config('ACCOUNT', 'user')
            _pw = get_config('ACCOUNT', 'password')
            _token = get_token(_user, _pw)
            URL_2g = get_config('URL', 'url') + '/api/v1/gateway/devices?connected=false'
            _res_ = call_api(URL_2g, 'GET', '', _token)

            _res_connected = _res_[0]['connected'] is False
            _check_key_id = _res_[0]['id'] is not None
            _check_key_name = _res_[0].get("name") is not None
            _check_key_mac = _res_[0].get("macAddress") is not None
            _check_key_last_connected = _res_[0].get("lastConnected") is not None

            list_actual5 = [disconnect_device_text, btn_refresh_display, list_disconnect_label,
                            [_check_key_id, _res_connected, _check_key_name, _check_key_mac, _check_key_last_connected]]
            list_expected5 = ['Disconnected Devices', return_true,
                              ['Device Name', 'MAC Address', 'Last Access Date', 'Block'],
                              [return_true]*5]
            step_6_name = "6. Check client disconnected displayed: " \
                          "Disconnected Devices text, Existed refresh button, List header text. " \
                          "Check API: Connected value, Key id, name, mac, last connected. "
            list_check_in_step_6 = [
                f"Check card tab is: {list_expected2[0]}",
                "Check button refresh is displayed",
                f"Check list disconnect labels is: {list_expected2[2]}",
                [
                    "Check client id is not null",
                    "Check res connected is false",
                    "Check client name is not null",
                    "Check client mac is not null",
                    "Check client last connected is not null"
                ]
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_39_HOME_Check_Block_Setting_operation(self):
        self.key = 'HOME_39'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            time.sleep(1)
            wireless_change_ssid_name(block_2g, 'Wifi_2G_SSID')
            if block_2g.find_element_by_css_selector(apply).is_displayed():
                block_2g.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, icon_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, icon_loading)

            time.sleep(0.5)
            wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
            print(wifi_2g_name)
            wifi_2g_password = wireless_check_pw_eye(driver, block_2g, change_pw=False)
            print(wifi_2g_password)
            check_connect = connect_wifi_by_command(wifi_2g_name, wifi_2g_password)
            # Disconnect wireless
            os.system('netsh wlan disconnect')
            time.sleep(3)

            list_actual0 = [check_connect]
            list_expected0 = [wifi_2g_name]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 0. Precondition. '
                f'Connect wire and wireless. Then disconnect wireless')
        except:
            self.list_steps.append(
                f'[Fail] 0. Precondition. '
                f'Connect wire and wireless. Then disconnect wireless')
            list_step_fail.append('Assertion wong.')

        try:
            grand_login(driver)

            # CLick Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            wait_popup_disappear(driver, dialog_loading)

            device_img = driver.find_element_by_css_selector(home_img_device)
            check_device_active = len(device_img.find_elements_by_css_selector(ele_active_cls)) > 0
            try:
                check_device_number = int(device_img.find_element_by_css_selector(ele_more_info_cls).text) > 0
            except:
                check_device_number = False
            # Click disconnected device
            driver.find_element_by_css_selector(ele_disconnect_device_tab).click()

            disconnect_table_display = len(driver.find_elements_by_css_selector(ele_disconnect_table)) > 0

            list_actual1 = [check_device_active, check_device_number, disconnect_table_display]
            list_expected1 = [return_true] * 3
            step_1_2_name = "1, 2. Login. Click Devices Image. " \
                            "Check device image active, Check device number > 0, Check Disconnect table display. "
            list_check_in_step_1_2 = [
                "Check device image is active",
                "Check Condition 'Check device number > 0' is correct",
                "Check Disconnect table is displayed"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            disconnect_table = driver.find_element_by_css_selector(ele_disconnect_table)
            list_disconnect_label = [i.text for i in disconnect_table.find_elements_by_css_selector(ele_disconnect_header)]
            btn_refresh_display = len(driver.find_elements_by_css_selector(ele_btn_refresh)) > 0
            disconnect_device_text = driver.find_elements_by_css_selector(card_tabs_cls)[1].text

            list_actual2 = [disconnect_device_text, btn_refresh_display, list_disconnect_label]
            list_expected2 = ['Disconnected Devices', return_true,
                              ['Device Name', 'MAC Address', 'Last Access Date', 'Block']]
            step_3_name = "3. Check client disconnected displayed: " \
                          "Disconnected Devices text, Existed refresh button, List header text. "
            list_check_in_step_3 = [
                "Check label Disconnected Devices is correct",
                "Check Button refresh is displayed",
                f"Check List disconnect label is: {list_expected2[2]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('3. Assertion wong.')

        try:
            list_block_icon = disconnect_table.find_elements_by_css_selector(ele_block_button_cls)
            check_block_enable = list()
            for i in list_block_icon:
                if not i.find_element_by_css_selector(select).find_element_by_css_selector(input).is_selected():
                    i.find_element_by_css_selector(select).click()
                    wait_popup_disappear(driver, icon_loading)
                    check_block_enable.append(i.find_element_by_css_selector(input).is_selected())

            check_block_enable = all(check_block_enable)

            list_actual3 = [check_block_enable]
            list_expected3 = [return_true]
            step_4_name = "4. Enabled all block. "
            list_check_in_step_4 = ["Check Block button is enabled"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('4. Assertion wong.')

        try:

            interface_connect_disconnect('Ethernet', 'disable')
            get_current_wifi_name = connect_wifi_by_command(wifi_2g_name, wifi_2g_password)
            print(get_current_wifi_name)
            # check_gg = check_connect_to_google()

            check_connect_wireless = get_value_from_ipconfig('Wireless LAN adapter Wi-Fi', 'IPv4 Address') == 'Block or field error.'

            list_actual4 = [check_connect_wireless]
            list_expected4 = [True]
            step_5_name = "5. Connect wireless of DUT. Check can not wireless. "
            list_check_in_step_5 = ["Check Condition 'Can not access to internet' is correct"]
            check = assert_list(list_actual4, list_expected4)
            interface_connect_disconnect('Ethernet', 'enable')
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_07_HOME_Check_Connection_Status_if_unplug_WAN_port(self):
        self.key = 'HOME_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        save_config(config_path, 'URL', 'url', 'http://192.168.1.1')
        URL_LOGIN = get_config('URL', 'url')
        # factory_dut()
        try:
            # ===================================================================
            URL_DISCONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/disconnect'
            _PW = get_config('ACCOUNT', 'password')
            _USER = get_config('ACCOUNT', 'user')
            _METHOD = 'POST'
            _BODY = ''
            _TOKEN = get_token(_USER, _PW)
            call_api(URL_DISCONNECT_WAN, _METHOD, _BODY, _TOKEN)
            time.sleep(10)
            # ===================================================================
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            # ===================================================================
            URL_WAN = URL_LOGIN + '/api/v1/network/wan'
            _PW = get_config('ACCOUNT', 'password')
            _USER = get_config('ACCOUNT', 'user')
            _METHOD = 'GET'
            _BODY = ''
            _TOKEN = get_token(_USER, _PW)
            _res = call_api(URL_WAN, _METHOD, _BODY, _TOKEN)
            expected_api = [_res['interfaces'][0]['connectivity'] == 'disconnected',
                            _res['interfaces'][0]['ipv4']['mode'] == 'dynamic',
                            _res['interfaces'][0]['ipv4']['address'] == '-',
                            _res['interfaces'][0]['ipv4']['subnet'] == '-',
                            _res['interfaces'][0]['ipv4']['gateway'] == '-',
                            _res['interfaces'][0]['ipv4']['dnsServer1'] == '-',
                            _res['interfaces'][0]['ipv4']['dnsServer2'] == '-'
                            ]
            # ===================================================================
            wan_card = driver.find_elements_by_css_selector(ele_wan_block)[0]
            labels = wan_card.find_elements_by_css_selector(label_name_in_2g)
            values = wan_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'WAN Type':
                    _wan_type = v.text == 'Ethernet'
                    continue
                if l.text == 'Connection Type':
                    _connection_type = v.text in ['Dynamic IP', 'Static IP', 'PPPoE']
                    continue
                if l.text == 'WAN IP Address':
                    _wan_ip_address = v.text == '0.0.0.0'
                    continue
                if l.text == 'Subnet Mask':
                    _subnet_mask = v.text == '0.0.0.0'
                    continue
                if l.text == 'Gateway':
                    _gateway = v.text == '0.0.0.0'
                    continue
                if l.text == 'DNS Server 1':
                    _dns_1 = v.text == '0.0.0.0'
                    continue
                if l.text == 'DNS Server 2':
                    _dns_2 = v.text == '0.0.0.0'
                    break
            expected_web = [_wan_type,
                            _connection_type,
                            _wan_ip_address,
                            _subnet_mask,
                            _gateway,
                            _dns_1,
                            _dns_2]

            list_actual3 = [expected_api, expected_web]
            list_expected3 = [[return_true]*7]*2
            step_1_2_name = "1, 2. Login. Check WAN api (Connectivity is disconnected, mode, address, subnet, " \
                            "gateway, dns1, dns2). Web UI (Wan Type is Ethernet, Connection Type, Wan IP, " \
                            "Subnet Mask, Gateway, DNS server 1, DNS server 2). "
            list_check_in_step_1_2 = [
                [
                    "Check api Condition 'connectivity is disconnected' is correct",
                    "Check api Condition 'mode is dynamic' is correct",
                    "Check api Condition 'address is -' is correct",
                    "Check api Condition 'subnet is -' is correct",
                    "Check api Condition 'gateway is -' is correct",
                    "Check api Condition 'DNS Server 1 is -' is correct"
                    "Check api Condition 'DNS Server 2 is -' is correct"
                ],
                [
                    "Check UI Condition 'Wan Type in list (Ethernet / USB Broadband / Android Tethering)' is correct",
                    "Check UI Condition 'Connection Type in list (Dynamic IP / Satatic IP / PPPoE)' is correct",
                    "Check UI Condition 'WAN IP Address is 0.0.0.0' is correct",
                    "Check UI Condition 'Subnet Mask is 0.0.0.0' is correct",
                    "Check UI Condition 'Gateway is 0.0.0.0' is correct",
                    "Check UI Condition 'DNS Server 1 is 0.0.0.0' is correct"
                    "Check UI Condition 'DNS Server 2 is 0.0.0.0' is correct"
                ]
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            URL_CONNECT_WAN = URL_LOGIN + '/api/v1/network/wan/0/connect'
            _METHOD = 'POST'
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            _BODY = ''
            call_api(URL_CONNECT_WAN, _METHOD, _BODY, _TOKEN)
            time.sleep(10)
            self.list_steps.append(
                f'[Pass] API Connect WAN Success After test. Check Status code. ')
        except:
            self.list_steps.append(
                f'[Fail] Connect WAN Fail After test. Check Status code. ')

        self.assertListEqual(list_step_fail, [])

    def test_40_HOME_Verification_of_Home_Screen(self):
        self.key = 'HOME_40'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            repeater_name = get_config('REPEATER', 'repeater_name', input_data_path)
            repeater_pw = get_config('REPEATER', 'repeater_pw', input_data_path)

            time.sleep(1)
            grand_login(driver)
            time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            connect_repeater_mode(driver)
            time.sleep(3)

            # Verify_connect successfully
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/wifi/0/ssid/0'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            time.sleep(1)
            _TOKEN = get_token(_USER, _PW)

            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)

            list_actual0 = [res['name']]
            list_expected0 = [repeater_name]
            step_0_name = "Precondition successfully. Check Upper name. "
            list_check_in_step_0 = [f"Check Upper name is: {repeater_name}"]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
            list_step_fail.append('0. Precondition wong')

        try:
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, home_tab, 0)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed."
            list_check_in_step_1 = ["Check Home page is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Check network map image
            check_wan_img = len(driver.find_elements_by_css_selector(home_img_connection)) > 0
            check_router_img = len(driver.find_elements_by_css_selector(home_img_lan_connection)) > 0
            check_usb_img = len(driver.find_elements_by_css_selector(home_img_usb_connection)) > 0
            check_device = len(driver.find_elements_by_css_selector(home_img_device_connection)) > 0

            list_actual2 = [check_wan_img, check_router_img, check_usb_img, check_device]
            list_expected2 = [return_true] * 4
            step_2_name = "2. Check Network map image: WAN, Router and Wireless, USB, Device image. "
            list_check_in_step_2 = [
                "Check WAN image is displayed",
                "Check Router & Wireless image is displayed",
                "Check USB image is displayed",
                "Check Connected Devices image is displayed"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_41_HOME_Verification_of_Host_Network_information(self):
        self.key = 'HOME_41'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            repeater_name = get_config('REPEATER', 'repeater_name', input_data_path)
            repeater_pw = get_config('REPEATER', 'repeater_pw', input_data_path)

            time.sleep(1)
            grand_login(driver)
            # time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            connect_repeater_mode(driver, repeater_name, repeater_pw)
            time.sleep(3)
            wait_ethernet_available()
            # # Verify_connect successfully
            # URL_LOGIN = get_config('URL', 'url')
            # _URL_API = URL_LOGIN + '/api/v1/wifi/0/ssid/0'
            # _METHOD = 'GET'
            # _BODY = ''
            # _USER = get_config('ACCOUNT', 'user')
            # _PW = get_config('ACCOUNT', 'password')
            # _TOKEN = get_token(_USER, _PW)
            # time.sleep(1)
            # res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            # time.sleep(1)
            # list_actual0 = [res['name']]
            # list_expected0 = [repeater_name]
            # check = assert_list(list_actual0, list_expected0)
            # self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] Precondition change to Repeater mode. ')
        except:
            self.list_steps.append(
                f'[Fail] Precondition change to Repeater mode. ')
            list_step_fail.append('0. Precondition wong')

        try:
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, home_tab, 0)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = ["Check Home page is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Click WAN image in network map image
            driver.find_element_by_css_selector(home_img_connection).click()
            # Check icon is highlight
            wan_connection = driver.find_element_by_css_selector(home_img_connection).get_attribute('class').split()
            check_wan_image_highlight = 'active' in wan_connection
            # Check Host Network is displayed
            check_host_network_table = len(driver.find_elements_by_css_selector(ele_host_network)) > 0

            list_actual2 = [check_wan_image_highlight, check_host_network_table]
            list_expected2 = [return_true] * 2
            step_2_1_name = "2.1 Click WAN image. Check WAN image highlight. Host Network table displayed. "
            list_check_in_step_2_1 = [
                "Check WAN image is highlight",
                "Check Host Network table is displayed"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_1_name,
                    list_check_in_step=list_check_in_step_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_1_name,
                    list_check_in_step=list_check_in_step_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2.1 Assertion wong.')

        try:
            # Get information from WEB
            host_nw_block = driver.find_element_by_css_selector(ele_host_network)
            host_nw_title = host_nw_block.find_element_by_css_selector(title_tabs_cls).text
            # Check Sub items displayed
            sub_label = host_nw_block.find_elements_by_css_selector(label_name_in_2g)
            sub_label_text = [i.text for i in sub_label]
            # Check Connection status
            labels = host_nw_block.find_elements_by_css_selector(label_name_in_2g)
            values = host_nw_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Connection status':
                    check_conn_status = v.text in ['Connected (2.4GHz)', 'Connected (5GHz)']
                    continue
                if l.text == 'Signal Strength':
                    check_signal = v.text != ''
                    continue
                if l.text == 'Network Name(SSID)':
                    check_nw_name = v.text != ''
                    continue
                if l.text == 'Security':
                    check_security = v.text != ''
                    continue
                if l.text == 'Password':
                    check_pw = wireless_check_pw_eye(driver, host_nw_block, change_pw=False) == repeater_pw
                    continue
                if l.text == 'BSSID':
                    check_bssid = checkMACAddress(v.text)
                    break

            list_actual3 = [host_nw_title, sub_label_text,
                            [check_conn_status, check_signal, check_nw_name, check_security, check_pw, check_bssid]]
            list_expected3 = ['Host Network',
                              ['Connection status', 'Signal Strength', 'Network Name(SSID)', 'Security', 'Password', 'MAC Address'],
                              [return_true]*6]
            step_2_2_name = "2.2 Check WebUI Host network component. Title, List Sub title, Values of subtitle. "
            list_check_in_step_2_2 = [
                "Check host network title is displayed",
                f"Check Sub title is: {list_expected3[1]}",
                [
                    "Check Condition 'Connection status is Connected (2.4GHz) or Connected (5GHz)'",
                    "Check Signal Strength is not null",
                    "Check Network name is not null",
                    "Check Security is not null",
                    f"Check Condition 'password is: {repeater_pw}' is correct",
                    "Check Format of BSSID is valid"
                ]
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('2.2 Assertion wong.')

        try:
            # Get information API
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/network/qmode'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res2 = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_has_key = [
                res2.get('qmode') == 'extender',
                res2.get('operation') == 'mesh slave',
                res2.get('connection') is not None,
                res2['connection'].get('ssid') is not None,
                res2['connection'].get('securityType') is not None,
                res2['connection'].get('password') is not None,
                res2['connection'].get('status') is not None,

            ]

            list_actual4 = check_has_key
            list_expected4 = [return_true]*7
            step_2_3_name = "2.3 Check API Host network component: " \
                            "qmode, operation, connection, ssid, securityType, pw, status. "
            list_check_in_step_2_3 = [
                "Check Condition 'qmode is extender' is correct",
                "Check Condition 'operation is mesh slave' is correct",
                "Check Connection is not null",
                "Check ssid is not null",
                "Check securityType is not null",
                "Check password is not null",
                "Check status is not null",
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2.3 Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_42_HOME_Verification_of_Network_Map_Router_Wireless_Information(self):
        self.key = 'HOME_42'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            repeater_name = get_config('REPEATER', 'repeater_name', input_data_path)
            repeater_pw = get_config('REPEATER', 'repeater_pw', input_data_path)

            grand_login(driver)
            time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            connect_repeater_mode(driver, REPEATER_UPPER=repeater_name, PW=repeater_pw)
            time.sleep(3)

            # Verify_connect successfully
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/wifi/0/ssid/0'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(1)
            list_actual0 = [res['name']]
            list_expected0 = [repeater_name]
            step_0_name = "Precondition successfully. Check Upper name. "
            list_check_in_step_0 = [f"Check Upper name is: {repeater_name}"]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
            list_step_fail.append('0. Precondition wong')

        try:
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, home_tab, 0)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = ["Check Home page is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Click Router and Wireless image in network map image
            driver.find_element_by_css_selector(home_img_lan_connection).click()
            # Check icon is highlight
            lan_connection = driver.find_element_by_css_selector(home_img_lan_connection).get_attribute('class').split()
            check_lan_image_highlight = 'active' in lan_connection

            list_actual2 = [check_lan_image_highlight]
            list_expected2 = [return_true]
            step_2_1_name = "2.1 Click LAN image. Check LAN image highlight active. "
            list_check_in_step_2_1 = ["Check LAN image is highlight"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_1_name,
                    list_check_in_step=list_check_in_step_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_1_name,
                    list_check_in_step=list_check_in_step_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2.1 Assertion wong.')

        try:
            lan_block = driver.find_element_by_css_selector(ele_lan_card)
            # IP v4
            lan_label_ipv4 = [i.text for i in lan_block.find_elements_by_css_selector(label_name_in_2g)]

            # IP v6
            lan_block.find_element_by_css_selector(ele_second_tab).click()
            time.sleep(1)
            lan_label_ipv6 = [i.text for i in lan_block.find_elements_by_css_selector(label_name_in_2g)]

            list_actual3 = [lan_label_ipv4, lan_label_ipv6]
            list_expected3 = [['LAN IP Address', 'Subnet Mask', 'DHCP Server', 'MAC Address'],
                              ['LAN IPv6 Address', 'Prefix Length', 'Assigned Type', 'MAC Address']]
            step_2_3_name = "2.2 Check LAN card component. Label text of IPv4 and IPv6. "
            list_check_in_step_2_3 = [
                "Check list lan label for ipv4 is correct",
                "Check list lan label for ipv6 is correct"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('2.2 Assertion wong.')

        try:
            wireless_block = driver.find_element_by_css_selector(ele_wireless_card)
            # IP v4
            wireless_label_ipv4 = [i.text for i in wireless_block.find_elements_by_css_selector(label_name_in_2g)]

            # IP v6
            wireless_block.find_element_by_css_selector(ele_second_tab).click()
            time.sleep(1)
            wireless_label_ipv6 = [i.text for i in wireless_block.find_elements_by_css_selector(label_name_in_2g)]

            list_actual4 = [wireless_label_ipv4, wireless_label_ipv6]
            list_expected4 = [['Network Name(SSID)', 'Security', 'Password', 'MAC Address'],
                              ['Network Name(SSID)', 'Security', 'Password', 'MAC Address']]
            step_2_3_name = "2.3 Check Wireless card component. Label text of 2.4GHz and 5GHz. "
            list_check_in_step_2_3 = [
                "Check Label text of 2.4GHz is correct",
                "Check Label text of 5GHz is correct"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('2.3 Assertion wong.')

        try:
            information_block = driver.find_element_by_css_selector(ele_information_card)
            information_label = [i.text for i in information_block.find_elements_by_css_selector(label_name_in_2g)]

            list_actual5 = [information_label]
            list_expected5 = [['Model Name', 'Serial Number', 'Firmware Version', 'Build Time', 'Operation Time']]
            step_2_4_name = "2.4 Check Information card component. Check Information Label text. "
            list_check_in_step_2_4 = ["Check Information Label text is correct"]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_4_name,
                    list_check_in_step=list_check_in_step_2_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_4_name,
                    list_check_in_step=list_check_in_step_2_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('2.4 Assertion wong.')

        try:
            ethernet_status_block = driver.find_element_by_css_selector(ele_ethernet_port_status)
            ethernet_label = [i.text for i in ethernet_status_block.find_elements_by_css_selector(label_name_in_2g)]

            list_actual6 = [ethernet_label]
            list_expected6 = [['Internet Port', 'LAN Port 1', 'LAN Port 2', 'LAN Port 3', 'LAN Port 4']]
            step_2_5_name = "2.5 Check Ethernet Port Status card component. Check Ethernet Port Status Label text. "
            list_check_in_step_2_5 = ["Check Ethernet Port Status label are: Internet Port, LAN Port 1,2,3,4"]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_5_name,
                    list_check_in_step=list_check_in_step_2_5,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_5_name,
                    list_check_in_step=list_check_in_step_2_5,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('2.5 Assertion wong.')

        try:
            cpu_block = driver.find_element_by_css_selector(ele_cpu_card)
            cpu_core_1_label = cpu_block.find_element_by_css_selector('.text-1').text
            cpu_core_2_label = cpu_block.find_element_by_css_selector('.text-2').text
            cpu_chart_displayed = len(cpu_block.find_elements_by_css_selector('#cpu-chart')) > 0
            # Get information API
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/gateway/statuses/cpuUsage'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res2 = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_has_key = [
                res2[0].get('name') == 'Core 1',
                res2[0].get('percentage') is not None,
                res2[1].get('name') == 'Core 2',
                res2[1].get('percentage') is not None
            ]

            list_actual7 = [[cpu_core_1_label, cpu_core_2_label, cpu_chart_displayed],
                            check_has_key]
            list_expected7 = [['Core1', 'Core2', return_true],
                              [return_true] *4]
            step_2_6_name = "2.6 Check CPU Status card: Check Label text, Chart display. " \
                            "API: Check Name and Percent of Core 1 and Core 2'"
            list_check_in_step_2_6 = [
                [
                    "Check CPU core 1 label is correct",
                    "Check CPU core 1 label is correct",
                    "Check CPU chart is displayed"
                ],
                [
                    "Check api Condition 'name of core 1 is Core 1' is correct",
                    "Check api percentage of Core 1 is not null",
                    "Check api Condition 'name of core 2 is Core 2' is correct",
                    "Check api percentage of Core 2 is not null",
                ]
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_6_name,
                    list_check_in_step=list_check_in_step_2_6,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_6_name,
                    list_check_in_step=list_check_in_step_2_6,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('2.6 Assertion wong.')

        try:
            memory_block = driver.find_element_by_css_selector(ele_memory_card)
            memory_label = [i.text for i in memory_block.find_elements_by_css_selector('.legend-name')]

            memory_chart_displayed = len(memory_block.find_elements_by_css_selector('#memory-chart')) > 0
            # Get information API
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/gateway/statuses/memoryUsage'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res3 = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_has_key_memory = [
                res3.get('total') is not None,
                res3.get('free') is not None
            ]

            list_actual8 = [memory_label, memory_chart_displayed,
                            check_has_key_memory]
            list_expected8 = [['Free Memory', 'Total Memory'], return_true,
                              [return_true] *2]
            step_2_7_name = "2.7 Check Memory Status card: Check Label text, Chart display. API: Check Total and Free. "
            list_check_in_step_2_7 = [
                "Check memory label is correct",
                "Check memory chart is displayed",
                [
                    "Check api get memory total is not null",
                    "Check api get memory free is not null",
                ]
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_7_name,
                    list_check_in_step=list_check_in_step_2_7,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_7_name,
                    list_check_in_step=list_check_in_step_2_7,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2.7 Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_43_HOME_Verification_of_Network_Map_USB_Information(self):
        self.key = 'HOME_43'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            repeater_name = get_config('REPEATER', 'repeater_name', input_data_path)
            repeater_pw = get_config('REPEATER', 'repeater_pw', input_data_path)
            grand_login(driver)
            time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            connect_repeater_mode(driver, REPEATER_UPPER=repeater_name, PW=repeater_pw)

            # Verify_connect successfully
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/wifi/0/ssid/0'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(1)
            list_actual0 = [res['name']]
            list_expected0 = [repeater_name]
            step_0_name = "1, 2. Get result by command success."
            list_check_in_step_0 = ["Get result by command success"]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
            list_step_fail.append('0. Precondition wong')

        try:
            grand_login(driver)
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = ["Check Home page is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Click USB image in network map image
            driver.find_element_by_css_selector(home_img_usb_connection).click()
            time.sleep(2)
            # Check icon is highlight
            check_usb_image = driver.find_element_by_css_selector(home_img_usb_connection).get_attribute('class').split()
            check_usb_image_highlight = 'active' in check_usb_image

            list_actual2 = [check_usb_image_highlight]
            list_expected2 = [return_true]
            step_2_1_name = "2.1 Click USB image. Check USB image highlight. "
            list_check_in_step_2_1 = ["Check USB image is highlight"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_1_name,
                    list_check_in_step=list_check_in_step_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_1_name,
                    list_check_in_step=list_check_in_step_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2.1 Assertion wong.')

        try:
            time.sleep(1)
            # Check USB Card Component
            usb_block = driver.find_elements_by_css_selector(ele_usb_card)[0]
            time.sleep(1)
            device_name_text = usb_block.find_elements_by_css_selector(label_name_in_2g)[0].text
            total_size_text = usb_block.find_elements_by_css_selector(label_name_in_2g)[1].text
            graph_display = len(usb_block.find_elements_by_css_selector(ele_space_bar)) > 0
            available_space = len(usb_block.find_elements_by_css_selector(ele_usb_space_available)) > 0
            icon_fab_displayed = len(usb_block.find_elements_by_css_selector(home_icon_fab)) > 0
            button_text = usb_block.find_element_by_css_selector(apply).text
            #

            list_actual3 = [device_name_text, graph_display, available_space,
                            total_size_text, button_text, icon_fab_displayed]
            list_expected3 = ['Device Name', return_true, return_true,
                              'Total Size', 'Remove', return_true]
            step_2_2_name = "[Pass] 2.2 Check USB card component. Device name text, Graph displayed, " \
                            "Available Space displayed, Total Size label text, button remove text, icon fab displayed. "
            list_check_in_step_2_2 = [
                "Check Device name text correct",
                "Check Graph is displayed",
                "Check Available Space is displayed",
                "Check label total size is correct",
                "Check text of button remove is remove",
                "Check icon fab is displayed"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_2_name,
                    list_check_in_step=list_check_in_step_2_2,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('2.2 Assertion wong.')

        try:
            # Get information API
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/mediashare/usb'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res2 = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_has_key = [
                res2.get('usbs') is not None,
                res2['usbs'][0].get('id') is not None,
                res2['usbs'][0].get('name') is not None,
                res2['usbs'][0].get('available') is not None,
                res2['usbs'][0].get('total') is not None
            ]

            list_actual4 = check_has_key
            list_expected4 = [return_true]*5
            step_2_3_name = "2.3 Check API USB component: usb, id, name, available, total. "
            list_check_in_step_2_3 = [
                "Check api response of get usbs information is not null",
                "Check api response information usbs id is not null",
                "Check api response information usbs name is not null",
                "Check api response information usbs available is not null",
                "Check api response information usbs total is not null",
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('2.3 Assertion wong.')

        try:
            # Check Server Card Component
            server_block = driver.find_element_by_css_selector(ele_server_card)
            label_servers = server_block.find_elements_by_css_selector(label_name_in_2g)
            label_servers_text = [i.text for i in label_servers]
            icon_fab_server_displayed = len(server_block.find_elements_by_css_selector(home_icon_fab)) > 0

            list_actual5 = [label_servers_text, icon_fab_server_displayed]
            list_expected5 = [['FTP Server', 'Windows Network (Samba)', 'Media Server (DLNA)'], return_true]
            step_2_4_name = "2.4 Check Server card component. List label text and icon fab displayed. "
            list_check_in_step_2_4 = [
                "Check label server text is correct",
                "Check Icon fab is displayed"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_4_name,
                    list_check_in_step=list_check_in_step_2_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_4_name,
                    list_check_in_step=list_check_in_step_2_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2.4 Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_44_HOME_Verification_of_Network_Map_Connected_Disconnected_Device(self):
        self.key = 'HOME_44'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            repeater_name = get_config('REPEATER', 'repeater_name', input_data_path)
            repeater_pw = get_config('REPEATER', 'repeater_pw', input_data_path)
            grand_login(driver)
            time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            connect_repeater_mode(driver, REPEATER_UPPER=repeater_name, PW=repeater_pw)

            # Verify_connect successfully
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/wifi/0/ssid/0'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(1)
            list_actual0 = [res['name']]
            list_expected0 = [repeater_name]
            step_0_name = "Precondition successfully. Check Upper name. "
            list_check_in_step_0 = [f"Check Upper name is: {repeater_name}"]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_0_name,
                    list_check_in_step=list_check_in_step_0,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
            list_step_fail.append('0. Precondition wong')

        try:
            grand_login(driver)
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = ["Check Home page is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Check icon is dimmed
            check_device_image = driver.find_element_by_css_selector(home_img_device).get_attribute('class').split()
            check_device_image_highlight = 'disabled' in check_device_image

            list_actual2 = [check_device_image_highlight]
            list_expected2 = [return_true]
            step_2_name = "2. Check Device image is disabled"
            list_check_in_step_2 = ["Check Device image is disabled"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_35_HOME_Check_Connected_Devices_show_in_Mesh_Network(self):
        self.key = 'HOME_35'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        try:
            repeater_name = get_config('REPEATER', 'repeater_name', input_data_path)
            repeater_pw = get_config('REPEATER', 'repeater_pw', input_data_path)
            grand_login(driver)
            wait_visible(driver, home_view_wrap)
            time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            # connect_repeater_mode(driver, REPEATER_UPPER=repeater_name, PW=repeater_pw, force=True)
            connect_repeater_mode(driver, REPEATER_UPPER=repeater_name, PW=repeater_pw)
            wait_ethernet_available()
            # Verify_connect successfully
            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/wifi/0/ssid/0'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            time.sleep(1)
            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            time.sleep(1)
            list_actual0 = [res['name']]
            list_expected0 = [repeater_name]
            step_1_2_name = "1, 2. Get result by command success."
            list_check_in_step_1_2 = ["Get result by command success"]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual0,
                    list_expected=list_expected0
                )
            )
            list_step_fail.append('0. Precondition wong')

        try:
            wait_ethernet_available()
            time.sleep(1)
            # Input data of Upper
            url_upper = get_config('REPEATER', 'url', input_data_path)
            user_upper = get_config('REPEATER', 'user', input_data_path)
            pw_upper = get_config('REPEATER', 'pw', input_data_path)
            wait_ethernet_available()
            grand_login(driver, url_login=url_upper,user_request=user_upper, pass_word=pw_upper)
            time.sleep(0.5)
            goto_menu(driver, home_tab, 0)
            time.sleep(1)
            # Click to Device Image
            driver.find_element_by_css_selector(home_img_device_connection).click()
            time.sleep(2)
            # Check access to Device Connection
            check_device_page = len(driver.find_elements_by_css_selector(ele_active_connected_device)) > 0

            list_actual1 = [check_device_page]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Click to Device Image. Check Device Connection page is displayed. "
            list_check_in_step_1 = ["Check Device Connection page is displayed"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1. Assertion wong')

        try:
            # Check Connected devices shows in Mesh Mode
            router_model_name = get_config('REPEATER', 'repeater_model', input_data_path)
            ls_row = driver.find_elements_by_css_selector(ele_device_row_connected)
            # Check Device Name
            for r in ls_row:
                if r.find_element_by_css_selector(name_cls).text == router_model_name:
                    # Check icon dot
                    check_icon_dot = len(r.find_elements_by_css_selector(ele_icon_dot)) > 0
                    # Check Upgrade button and version
                    check_upgrade_button = len(r.find_elements_by_css_selector(ele_upgrade_btn)) > 0
                    check_version = len(r.find_elements_by_css_selector(ele_version)) > 0
                else:
                    check_edit_btn = len(r.find_elements_by_css_selector(edit_cls)) > 0

            # Check Interface
            ls_interfaces = [i.find_element_by_css_selector(ele_ssid_cls) for i in ls_row]
            check_interfaces = all([True if i.text.startswith('Wireless') or i.text.startswith('LAN Port') else False for i in ls_interfaces])

            # Check MAC Address
            ls_macs = [m.find_element_by_css_selector(wol_mac_addr) for m in ls_row]
            check_macs = all([True if checkMACAddress(m.text) else False for m in ls_macs])

            # Check IP address
            ls_ip_address = [i.find_element_by_css_selector(ip_address_cls) for i in ls_row]
            check_ips = all([True if checkIPAddress(i.text) else False for i in ls_ip_address])

            list_actual2 = [check_icon_dot, check_interfaces, check_macs, check_ips,
                            check_upgrade_button, check_version, check_edit_btn]
            list_expected2 = [return_true] * 7
            step_2_name = "2. Check Dot icon of Mesh; Interfaces is Wireless and Lan " \
                          "Port; MAC; IP; Upgrade btn; Version; Edit button displayed. "
            list_check_in_step_2 = [
                "Check Dot icon of Mesh is displayed",
                "Check Condition 'Interfaces is start with Wireless or Lan' is correct",
                "Check Format of MAC address is valid",
                "Check Format of IP address is valid",
                "Check Upgrade button is displayed",
                "Check Version is displayed",
                "Check Edit button is displayed",
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong.')

        try:
            # Click to Mesh mode IP address.
            router_model_name = get_config('REPEATER', 'repeater_model', input_data_path)
            ls_row = driver.find_elements_by_css_selector(ele_device_row_connected)
            # Check Device Name
            for r in ls_row:
                if r.find_element_by_css_selector(name_cls).text == router_model_name:
                    get_ip = r.find_element_by_css_selector(ip_address_cls).text
                    r.find_element_by_css_selector(ip_address_cls).find_element_by_css_selector('a').click()
                    break
            time.sleep(2)
            driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(1)
            current_url = driver.current_url

            list_actual3 = [current_url]
            list_expected3 = ['http://'+get_ip + '/']
            step_3_name = "3. Click to Upper Ip address link. Check URL. "
            list_check_in_step_3 = [f"Check current URL is: {list_expected3[0]}"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_06_HOME_Check_Connection_Status_of_PPPoE(self):
        self.key = 'HOME_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ====================================================
        factory_dut()
        # ======================================================
        NEW_PASSWORD_1 = get_config('COMMON', 'new_pw', input_data_path)
        PPPOE_USER = get_config('PPPOE', 'pppoe_user', input_data_path)
        PPPOE_PW = get_config('PPPOE', 'pppoe_pw', input_data_path)
        try:
            time.sleep(1)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD_1, NEW_PASSWORD_1]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)

            internet_setup = driver.find_element_by_css_selector(ele_welcome_connection_box)
            internet_setup.click()
            time.sleep(1)
            ls_option = internet_setup.find_elements_by_css_selector(secure_value_in_drop_down)
            for o in ls_option:
                if o.text == 'PPPoE':
                    o.click()

            form = driver.find_element_by_css_selector('.form-container>div:nth-child(2)')
            labels = form.find_elements_by_css_selector(label_name_in_2g)
            values = form.find_elements_by_css_selector(label_value_in_2g)
            for l, v in zip(labels, values):
                if l.text == 'User Name':
                    v.send_keys(PPPOE_USER)
                    time.sleep(1)
                if l.text == 'Password':
                    v.send_keys(PPPOE_PW)
                    break

            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            time.sleep(3)
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            # Write config
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            wait_visible(driver, home_view_wrap)

            self.list_steps.append(
                f'[Pass] 0. Precondition. ')
        except:
            self.list_steps.append(
                f'[Fail] 0. Precondition')
            list_step_fail.append('0. Assertion wong')

        try:
            driver.refresh()
            time.sleep(5)
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(2)

            card = driver.find_element_by_css_selector('.tabs-information')
            ls_label = [i.text for i in card.find_elements_by_css_selector(label_name_in_2g)]
            labels = card.find_elements_by_css_selector(label_name_in_2g)
            fields = card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, f in zip(labels, fields):
                if l.text == 'Connection Type':
                    get_connection_type = f.text
                    time.sleep(1)

            check_card_title = card.find_element_by_css_selector(title_tabs_cls).text
            check_icon_more = len(card.find_elements_by_css_selector(home_icon_fab)) > 0
            factory_dut()
            list_actual4 = [ls_label, get_connection_type, check_card_title, check_icon_more]
            list_expected4 = [['WAN Type', 'Connection Type', 'WAN IP Address', 'Subnet Mask',
                               'Gateway', 'DNS Server 1', 'DNS Server 2'], 'PPPoE', 'Internet', True
                              ]
            step_2_name = "2. Set to PPPoE. Click to WAN image. " \
                          "Check list label, Check Connection Type, Card title, Icon more. "
            list_check_in_step_2 = [
                "Check list label is correct",
                "Check connection type is: PPPoE",
                "Check card title is: Internet",
                "Check icon more is displayed"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2.  Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_37_HOME_Check_Edit_icon_works_in_connected_devices_of_Mesh_Network(self):
        self.key = 'HOME_37'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        REPEATER_WIFI_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_WIFI_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        try:
            grand_login(driver)
            time.sleep(2)
            goto_menu(driver, network_tab, network_operationmode_tab)
            connect_repeater_mode(driver, REPEATER_WIFI_NAME, REPEATER_WIFI_PW)
            time.sleep(3)
            wait_ethernet_available()

            connect_wifi_by_command(REPEATER_WIFI_NAME, REPEATER_WIFI_PW)
            self.list_steps.append(
                f'[Pass] Precondition successfully. Set Repeater mode. Connect wifi repeater. ')
        except:
            self.list_steps.append(
                f'[Fail] Precondition Fail. Set Repeater mode. Connect wifi repeater. ')
            list_step_fail.append('0. Precondition wong')

        try:
            UPPER_URL = get_config('REPEATER', 'url', input_data_path)
            UPPER_USER = get_config('REPEATER', 'user', input_data_path)
            UPPER_PW = get_config('REPEATER', 'pw', input_data_path)
            wait_ethernet_available()
            time.sleep(2)
            grand_login(driver, url_login=UPPER_URL, user_request=UPPER_USER, pass_word=UPPER_PW)
            time.sleep(1)
            driver.refresh()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(home_img_device_connection).click()
            wait_popup_disappear(driver, dialog_loading)

            nw_items = driver.find_elements_by_css_selector('.network-item')
            for i in nw_items:
                if len(i.find_elements_by_css_selector(title_cls)) > 0:
                    if i.find_element_by_css_selector(title_cls).text == 'Mesh Network':
                        i.find_element_by_css_selector(edit_cls).click()
                        time.sleep(2)
                        break

            check_device_name = driver.find_element_by_css_selector(ele_mac_device_name+ ' input').get_attribute('value').startswith('DESKTOP')
            check_device_type_image = len(driver.find_elements_by_css_selector('.basic-info .thumb')) > 0
            check_device_type = len(driver.find_elements_by_css_selector('.custom-select-box')) > 0
            check_device_mac = checkMACAddress(driver.find_elements_by_css_selector('.info')[0].text)
            check_device_ip = checkIPAddress(driver.find_elements_by_css_selector('.info')[1].text)
            check_device_interface = driver.find_elements_by_css_selector('.info')[2].text.startswith('LAN Port')

            check_label = [i.text for i in driver.find_elements_by_css_selector(label_name_in_2g)]

            list_actual1 = [check_device_name, check_device_type_image, check_device_type,
                            check_device_mac, check_device_ip, check_device_interface, check_label]
            list_expected1 = [return_true] * 6 + [['Reserved IP', 'MAC Filtering', 'Parental Control', 'WoL (Wake on LAN)']]
            step_1_2_name = "1, 2. Goto Device image. Click Edit of Mesh Network. " \
                            "Check Device name, Device, Type image, Device Type, MAC address, IP address, Interface and List Labels."
            list_check_in_step_1_2 = [
                "Check Condition 'Device name start with DESKTOP' is correct",
                "Check device type image is appear",
                "Check device type is appear",
                "Check format mac address is valid",
                "Check format id address is valid",
                "Check Condition 'Device interface start with Lan port' is correct",
                "Check list label is correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # def test_36_HOME_Check_Firmware_Update_icon_works_when_firmware_file_in_extender_DUT_is_not_latest_version(self):
    #     self.key = 'HOME_36'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     disconnect_or_connect_wan(disconnected=True)
    #     factory_dut()
    #
    #     # ======================================================
    #     REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
    #     REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
    #     NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
    #     try:
    #         time.sleep(1)
    #         login(driver)
    #         wait_popup_disappear(driver, dialog_loading)
    #         wait_popup_disappear(driver, dialog_loading)
    #         # Click start btn
    #         driver.find_element_by_css_selector(welcome_start_btn).click()
    #         wait_visible(driver, welcome_change_pw_fields)
    #
    #         change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)
    #
    #         # A list contain values: Current Password, New Password, Retype new pw
    #         ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
    #         for p, v in zip(change_pw_fields, ls_change_pw_value):
    #             ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
    #             time.sleep(0.5)
    #         # Next Change pw
    #         wait_visible(driver, welcome_next_btn)
    #         next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    #         if not next_btn.get_property('disabled'):
    #             next_btn.click()
    #             wait_popup_disappear(driver, dialog_loading)
    #
    #         # Change Operation Mode
    #         driver.find_element_by_css_selector(ele_welcome_router_box).click()
    #         time.sleep(0.5)
    #         operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
    #         list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
    #         # Choose
    #         for o in list_options:
    #             if o.text == 'Repeater Mode':
    #                 o.click()
    #                 break
    #
    #         # Next
    #         wait_visible(driver, welcome_next_btn)
    #         next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    #         if not next_btn.get_property('disabled'):
    #             next_btn.click()
    #             time.sleep(3)
    #             wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(10)
    #         wait_popup_disappear(driver, icon_loading)
    #
    #
    #         time.sleep(5)
    #         _rows = driver.find_elements_by_css_selector(rows)
    #         # Choose Network name
    #         for r in _rows:
    #             if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
    #                 r.click()
    #                 time.sleep(1)
    #                 break
    #         # Fill Password
    #         pw_box = driver.find_element_by_css_selector(ele_input_pw)
    #         ActionChains(driver).click(pw_box).send_keys(REPEATER_MESH_PW).perform()
    #         time.sleep(1)
    #
    #         # Get info
    #         for r in _rows:
    #             if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
    #                 get_security = r.find_element_by_css_selector(security_page).text
    #
    #         while True:
    #             time.sleep(1)
    #             wait_visible(driver, welcome_next_btn)
    #             next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    #             if not next_btn.get_property('disabled'):
    #                 next_btn.click()
    #             time.sleep(3)
    #
    #             if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
    #                 break
    #
    #         # Click Let go
    #         driver.find_element_by_css_selector(welcome_let_go_btn).click()
    #         time.sleep(100)
    #         wait_popup_disappear(driver, icon_loading)
    #         save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
    #         save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
    #         time.sleep(1)
    #         # os.system(f'python {nw_interface_path} -i Ethernet -a enable')
    #         # time.sleep(10)
    #         # connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
    #         # time.sleep(5)
    #         # print(current_connected_wifi())
    #         # driver.get('http://dearmyextender.net')
    #         os.system(f'netsh wlan delete profile name="{REPEATER_MESH_NAME}"')
    #         time.sleep(10)
    #         wait_ethernet_available()
    #         time.sleep(5)
    #         wait_ethernet_available()
    #
    #         grand_login(driver)
    #         time.sleep(2)
    #
    #         change_firmware_version(driver, version='t10x_fullimage_3.00.12_rev11.img')
    #
    #         time.sleep(10)
    #         self.list_steps.append(
    #             f'[Pass] Precondition successfully. '
    #             f'Set Repeater mode. Connect wifi repeater. Up to low firmware version. ')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] Precondition Fail. '
    #             f'Set Repeater mode. Connect wifi repeater. Up to low firmware version.  ')
    #         list_step_fail.append('0. Precondition wong')
    #
    #     try:
    #         UPPER_URL = get_config('REPEATER', 'url', input_data_path)
    #         UPPER_USER = get_config('REPEATER', 'user', input_data_path)
    #         UPPER_PW = get_config('REPEATER', 'pw', input_data_path)
    #         wait_ethernet_available()
    #         time.sleep(10)
    #         wait_ethernet_available()
    #         grand_login(driver, url_login=UPPER_URL, user_request=UPPER_USER, pass_word=UPPER_PW)
    #         time.sleep(1)
    #
    #         driver.find_element_by_css_selector(home_img_device_connection).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(2)
    #         connected_devices = driver.find_element_by_css_selector(ele_device_tab_titles)
    #         connected_devices.find_element_by_css_selector(ele_upgrade_btn).click()
    #         time.sleep(1)
    #         check_message = driver.find_element_by_css_selector(confirm_dialog_msg).text
    #         time.sleep(0.5)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(150)
    #
    #         list_actual1 = [check_message]
    #         list_expected1 = [exp_msg_upgrade_extender]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 1, 2, 3. Goto Device image. CLick Upgrade. Check message. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail]  1, 2. Goto Device image. CLick Upgrade. Check message. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         list_step_fail.append('1, 2, 3. Assertion wong')
    #
    #     try:
    #         wait_ethernet_available()
    #         time.sleep(10)
    #         # Login
    #         wait_ethernet_available()
    #         grand_login(driver)
    #         wait_popup_disappear(driver, home_view_wrap)
    #
    #         goto_system(driver, ele_sys_firmware_update)
    #         time.sleep(1)
    #         check_text = driver.find_element_by_css_selector(ele_firm_update_msg).text
    #
    #         list_actual2 = [check_text]
    #         list_expected2 = ['The current version is up to date.']
    #         check = assert_list(list_actual2, list_expected2)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 4, 5. Goto Extender. Goto System. Check Version is lastest. '
    #             f'Actual: {str(list_actual2)}. '
    #             f'Expected: {str(list_expected2)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 4, 5.  Goto Extender. Goto System. Check Version is lastest. '
    #             f'Actual: {str(list_actual2)}. '
    #             f'Expected: {str(list_expected2)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('4, 5. Assertion wong')
    #
    #     self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
