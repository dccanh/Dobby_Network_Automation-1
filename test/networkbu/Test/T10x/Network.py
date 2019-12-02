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

    def test_01_Check_Internet_Status(self):
        global list_actual, list_expected, wan_ip
        self.key = 'NETWORK_01'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API = URL_LOGIN + '/api/v1/network/wan/0'
        URL_PING_CHECK = 'google.com'
        METHOD = 'GET'
        BODY = None
        VALUE_DNS1 = '1'
        VALUE_DNS2 = '8'
        # Handle API
        _token = get_token(USER_LOGIN, PW_LOGIN)

        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

            internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            ActionChains(driver).move_to_element(internet_setting).perform()

            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # Connection type
            internet_setting_fields[1].click()
            time.sleep(0.2)
            ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
            for o in ls_option:
                if o.text == 'Dynamic IP':
                    o.click()
            # Manual DNS
            _check_manual_dns_selected = internet_setting_fields[2].find_element_by_css_selector(input)
            if not _check_manual_dns_selected.is_selected():
                internet_setting_fields[2].click()
                time.sleep(0.5)
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)

            # DNS server 1
            dns_1 = internet_setting_fields[3].find_elements_by_css_selector(input)
            for i in dns_1:
                ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(VALUE_DNS1).perform()
            # DNS server 2
            dns_2 = internet_setting_fields[4].find_elements_by_css_selector(input)
            for i in dns_2:
                ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(VALUE_DNS2).perform()
            # Click Apply of this enable
            time.sleep(0.2)
            btn_apply = internet_setting.find_element_by_css_selector(apply)
            _check_apply = btn_apply.is_displayed()
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

                list_actual = [_check_apply]
                list_expected = [return_true]
                check = assert_list(list_actual, list_expected)
            else:
                check = assert_list([return_true], [return_true])

            # list_actual = [_check_apply]
            # list_expected = [return_true]
            # check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Goto Network>Internet: Change values of Internet Settings\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Goto Network>Internet: Change values of Internet Settings. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Login
            time.sleep(5)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            # Get Wan IP address
            wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(left)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label: value})

            translate_key_api2ui = {"linkType": "WAN Type",
                                    "mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            res_wan_primary = call_api(URL_API, METHOD, BODY, _token)

            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
            _expected = []
            for i in translate_key_api2ui.keys():
                if i != 'linkType':
                    _expected.append(res_wan_primary['ipv4'][i])
                else:
                    _expected.append(res_wan_primary[i])

            if res_wan_primary['linkType'] == 'ethernet':
                _expected[0] = 'Ethernet'
            if res_wan_primary['ipv4']['mode'] == 'dynamic':
                _expected[1] = 'Dynamic IP'
            if res_wan_primary['ipv4']['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check Information of WAN IP\n')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Information of WAN IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)
            list_actual = [check_ping]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Ping to Google successfully\n')
        except:
            self.list_steps.append(
                f'[Fail] 4. Ping to Google successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

            internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            ActionChains(driver).move_to_element(internet_setting).perform()
            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # Connection type
            internet_setting_fields[1].click()
            time.sleep(0.2)
            ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
            for o in ls_option:
                if o.text == 'Static IP':
                    o.click()

            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)

            # WAN IP
            wan_ip_number = wan_ip.split('.')
            wan_ip_number[-1] = random.choice([str(i) for i in range(200, 254)])
            wan_ip_addr = internet_setting_fields[2].find_elements_by_css_selector(input)
            for el, va in zip(wan_ip_addr, wan_ip_number):
                ActionChains(driver).move_to_element(el).click().send_keys(va).perform()
            # Apply
            btn_apply = internet_setting.find_element_by_css_selector(apply)
            _check_apply = btn_apply.is_displayed()
            if _check_apply:
                btn_apply.click()
                time.sleep(0.5)
                # Click OK
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(5)
                wait_ping(URL_LOGIN)
                # wait_popup_disappear(driver, dialog_loading)
                # time.sleep(5)

            list_actual = [_check_apply]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Goto Network>Internet: Change values of Internet Settings\n')
        except:
            self.list_steps.append(
                f'[Fail] 5. Goto Network>Internet: Change values of Internet Settings. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            # Login
            time.sleep(5)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Get Wan IP address
            wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(left)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label: value})

            translate_key_api2ui = {"linkType": "WAN Type",
                                    "mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            res_wan_primary = call_api(URL_API, METHOD, BODY, _token)

            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
            _expected = []
            for i in translate_key_api2ui.keys():
                if i != 'linkType':
                    _expected.append(res_wan_primary['ipv4'][i])
                else:
                    _expected.append(res_wan_primary[i])

            if res_wan_primary['linkType'] == 'ethernet':
                _expected[0] = 'Ethernet'
            if res_wan_primary['ipv4']['mode'] == 'static':
                _expected[1] = 'Static IP'
            if res_wan_primary['ipv4']['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check Information of WAN IP\n')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Information of WAN IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)
            list_actual = [check_ping]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Ping to Google successfully\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Ping to Google successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '7. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_02_Check_Dynamic_IP_Operation(self):
        global list_actual, list_expected, internet_setting
        self.key = 'NETWORK_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API = URL_LOGIN + '/api/v1/network/wan/0'
        URL_PING_CHECK = 'google.com'
        METHOD = 'GET'
        BODY = None
        VALUE_DNS1 = '1.1.1.1'
        VALUE_DNS2 = '8.8.8.8'
        # Handle API

        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

            internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
                internet_setting = driver.find_element_by_css_selector(internet_setting_block_single)
            ActionChains(driver).move_to_element(internet_setting).perform()

            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # Connection type
            internet_setting_fields[1].click()
            time.sleep(0.2)
            ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
            for o in ls_option:
                if o.text == 'Dynamic IP':
                    o.click()

            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # Manual DNS
            _check_manual_dns_selected = internet_setting_fields[2].find_element_by_css_selector(input)
            if not _check_manual_dns_selected.is_selected():
                internet_setting_fields[2].find_element_by_css_selector(select).click()
                time.sleep(0.5)

            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # DNS server 1
            dns_1 = internet_setting_fields[3].find_elements_by_css_selector(input)
            for d in dns_1:
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()
            # DNS server 2
            dns_2 = internet_setting_fields[4].find_elements_by_css_selector(input)
            for d in dns_2:
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()

            # Verify This field is required
            check_required_warning = len(driver.find_elements_by_xpath(text_field_required)) > 0
            list_actual = [check_required_warning]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Delete DNS server info: Check text This field is required\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Delete DNS server info: Check text This field is required. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Disable Manual DNS
        try:
            # Disabled Manual DNS
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # Manual DNS
            _check_manual_dns_selected = internet_setting_fields[2].find_element_by_css_selector(input)
            if _check_manual_dns_selected.is_selected():
                internet_setting_fields[2].find_element_by_css_selector(select).click()
                time.sleep(0.5)

            time.sleep(0.2)
            btn_apply = internet_setting.find_element_by_css_selector(apply)
            _check_apply = btn_apply.is_displayed()
            # Click Apply
            if _check_apply:
                btn_apply.click()
                time.sleep(0.5)

            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)

            # Check Page network should be kept
            check_page_nw = len(driver.find_elements_by_css_selector(page_network)) > 0

            list_actual = [check_page_nw]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept\n')
        except:
            self.list_steps.append(
                f'[Fail] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '4,5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            time.sleep(0.2)
            btn_apply = internet_setting.find_element_by_css_selector(apply)
            _check_apply = btn_apply.is_displayed()
            # Click Apply
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

            self.list_steps.append(
                '[Pass] 6. Apply and Wait for reboot\n')
        except:
            self.list_steps.append(
                f'[Fail] 6. Apply and Wait for reboot. ')
            list_step_fail.append(
                '6. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            # Login
            time.sleep(10)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(left)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label_wan = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label_wan: value})
            _token = get_token(USER_LOGIN, PW_LOGIN)
            translate_key_api2ui = {"linkType": "WAN Type",
                                    "mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            res_wan_primary = call_api(URL_API, METHOD, BODY, _token)

            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
            _expected = []
            for i in translate_key_api2ui.keys():
                if i != 'linkType':
                    _expected.append(res_wan_primary['ipv4'][i])
                else:
                    _expected.append(res_wan_primary[i])

            if res_wan_primary['linkType'] == 'ethernet':
                _expected[0] = 'Ethernet'
            if res_wan_primary['ipv4']['mode'] == 'dynamic':
                _expected[1] = 'Dynamic IP'
            # if res_wan_primary['ipv4']['dnsServer2'] == '':
            #     _expected[-1] = '0.0.0.0'

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Check Information of WAN IP\n')
        except:
            self.list_steps.append(
                f'[Fail] 7. Check Information of WAN IP. '
                f'Actual: {str(_actual)}. Expected: {str(_expected)}')
            list_step_fail.append(
                '7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)
            list_actual = [check_ping]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 8. Ping to Google successfully\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8. Ping to Google successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '8. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_03_Check_Static_IP_Operation(self):
        global list_actual, list_expected, internet_setting, wan_ip_addr_value, wan_gateway_value
        self.key = 'NETWORK_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API = URL_LOGIN + '/api/v1/network/wan/0'
        URL_PING_CHECK = 'google.com'
        METHOD = 'GET'
        BODY = None
        VALUE_DNS1 = '1.1.1.1'
        VALUE_DNS1_SPLIT = VALUE_DNS1.split('.')
        VALUE_DNS2 = '8.8.8.8'
        VALUE_DNS2_SPLIT = VALUE_DNS2.split('.')

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)

            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(left)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label_wan = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label_wan: value})
            wan_ip_addr_value = dict_wan['WAN IP Address'].split('.')
            wan_gateway_value = dict_wan['Gateway'].split('.')

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

            internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
                internet_setting = driver.find_element_by_css_selector(internet_setting_block_single)
            ActionChains(driver).move_to_element(internet_setting).perform()

            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # Connection type
            internet_setting_fields[1].click()
            time.sleep(0.2)
            ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
            for o in ls_option:
                if o.text == 'Static IP':
                    o.click()

            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # WAN IP Address
            wan_ip_addr = internet_setting_fields[2].find_elements_by_css_selector(input)
            for d in wan_ip_addr:
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()
            # Gateway
            gateway_ = internet_setting_fields[4].find_elements_by_css_selector(input)
            for d in gateway_:
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()

            # DNS server 1
            dns_1 = internet_setting_fields[5].find_elements_by_css_selector(input)
            for d in dns_1:
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()
            # DNS server 2
            dns_2 = internet_setting_fields[6].find_elements_by_css_selector(input)
            for d in dns_2:
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()

            # Verify This field is required
            check_required_warning = len(driver.find_elements_by_xpath(text_field_required)) > 0
            list_actual = [check_required_warning]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Delete DNS server info: Check text This field is required\n')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Delete DNS server info: Check text This field is required. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Disable Manual DNS
        try:
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            # WAN IP Address
            wan_ip_addr = internet_setting_fields[2].find_elements_by_css_selector(input)
            for d, v in zip(wan_ip_addr, wan_ip_addr_value):
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(v).perform()
            # Gateway
            gateway_ = internet_setting_fields[4].find_elements_by_css_selector(input)
            for d, v in zip(gateway_, wan_gateway_value):
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(v).perform()

            # DNS server 1
            dns_1 = internet_setting_fields[5].find_elements_by_css_selector(input)
            for d, v in zip(dns_1, VALUE_DNS1_SPLIT):
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(v).perform()
            # DNS server 2
            dns_2 = internet_setting_fields[6].find_elements_by_css_selector(input)
            for d, v in zip(dns_2, VALUE_DNS2_SPLIT):
                ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(v).perform()

            time.sleep(0.2)
            btn_apply = internet_setting.find_element_by_css_selector(apply)
            _check_apply = btn_apply.is_displayed()
            # Click Apply
            if _check_apply:
                btn_apply.click()
                time.sleep(0.5)

            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)

            # Check Page network should be kept
            check_page_nw = len(driver.find_elements_by_css_selector(page_network)) > 0

            list_actual = [check_page_nw]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept\n')
        except:
            self.list_steps.append(
                f'[Fail] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '4,5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            time.sleep(0.2)
            btn_apply = internet_setting.find_element_by_css_selector(apply)
            _check_apply = btn_apply.is_displayed()
            # Click Apply
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

            list_actual = [_check_apply]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Apply and Wait for reboot\n')
        except:
            self.list_steps.append(
                '[Fail] 6. Apply and Wait for reboot. ')
            list_step_fail.append(
                '6. Assertion wong.')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            # Login
            time.sleep(5)
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(left)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label_wan = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label_wan: value})

            translate_key_api2ui = {"linkType": "WAN Type",
                                    "mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            _token = get_token(USER_LOGIN, PW_LOGIN)
            res_wan_primary = call_api(URL_API, METHOD, BODY, _token)

            _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
            _expected = []
            for i in translate_key_api2ui.keys():
                if i != 'linkType':
                    _expected.append(res_wan_primary['ipv4'][i])
                else:
                    _expected.append(res_wan_primary[i])

            if res_wan_primary['linkType'] == 'ethernet':
                _expected[0] = 'Ethernet'
            if res_wan_primary['ipv4']['mode'] == 'staticc':
                _expected[1] = 'Static IP'
            # if res_wan_primary['ipv4']['dnsServer2'] == '':
            #     _expected[-1] = '0.0.0.0'

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Check Information of WAN IP\n')
        except:
            self.list_steps.append(
                f'[Fail] 7. Check Information of WAN IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)
            list_actual = [check_ping]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 8. Ping to Google successfully\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8. Ping to Google successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '8. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
