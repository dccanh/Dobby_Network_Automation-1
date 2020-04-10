import sys
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
from Helper.t10x.config.data_expected import *
from Helper.t10x.common import *
from selenium import webdriver


class NETWORK(unittest.TestCase):
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
        # try:
        #     end_time = datetime.now()
        #     duration = str((end_time - self.start_time))
        #     write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        # except:
        #     # Connect by wifi if internet is down to handle exception for PPPoE
        #     os.system('netsh wlan connect ssid=HVNWifi name=HVNWifi')
        #     time.sleep(1)
        #     end_time = datetime.now()
        #     duration = str((end_time - self.start_time))
        #     write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        #     time.sleep(5)
        #     # Connect by LAN again
        #     os.system('netsh wlan disconnect')
        #     time.sleep(1)
        # write_to_excel(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
        write_to_excel_tmp(self.key, self.list_steps, self.def_name)
        self.driver.quit()

    def test_01_NETWORK_Check_Internet_Status(self):
        self.key = 'NETWORK_01'
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
        URL_API = URL_LOGIN + '/api/v1/network/wan/0'
        METHOD = 'GET'
        BODY = None
        VALUE_DNS1 = '1'
        VALUE_DNS2 = '8'
        PPPoE_USER = 'admin'
        PPPoE_PW = 'admin'
        # Handle API

        try:
            grand_login(driver)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
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
                    f.click()
                    time.sleep(0.2)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Dynamic IP':
                            o.click()
                            break
                    break

            time.sleep(0.5)
            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # Manual DNS
                if l.text == 'Manual DNS':
                    _check_manual_dns_selected = f.find_element_by_css_selector(input)
                    if not _check_manual_dns_selected.is_selected():
                        f.click()
                        time.sleep(0.5)
                        break
                    break
            # Get again
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # DNS server 1
                if l.text == 'DNS Server 1':
                    dns_1 = f.find_elements_by_css_selector(input)
                    for i in dns_1:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(VALUE_DNS1).perform()
                # DNS server 2
                elif l.text == 'DNS Server 2':
                    dns_2 = f.find_elements_by_css_selector(input)
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

            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2. Goto Network>Internet: Change values of Internet Settings: Dynamic IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Goto Network>Internet: Change values of Internet Settings: Dynamic IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Login
            grand_login(driver)
            time.sleep(1)

            # Get Wan IP address
            wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(ele_wan_block)
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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            _token = get_token(USER_LOGIN, PW_LOGIN)
            time.sleep(2)
            res_wan_primary = call_api(URL_API, METHOD, BODY, _token)
            time.sleep(2)
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

            list_actual2 = [_actual]
            list_expected2 = [_expected]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check information changed: Dynamic IP. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check information changed: Dynamic IP. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            wan_ip_addr_value = dict_wan['WAN IP Address'].split('.')
            wan_gateway_value = dict_wan['Gateway'].split('.')

            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
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
                    f.click()
                    time.sleep(0.2)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Static IP':
                            o.click()
                            break
                    break

            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # WAN IP Address
                if l.text == 'WAN IP Address':
                    # WAN IP Address
                    wan_ip_addr = f.find_elements_by_css_selector(input)
                    for d, w in zip(wan_ip_addr, wan_ip_addr_value):
                        ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(w).perform()
                if l.text == 'Gateway':
                    # Gateway
                    gateway_ = f.find_elements_by_css_selector(input)
                    for d, w in zip(gateway_, wan_gateway_value):
                        ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(Keys.DELETE).send_keys(w).perform()

                # DNS server 1
                if l.text == 'DNS Server 1':
                    dns_1 = f.find_elements_by_css_selector(input)
                    for i in dns_1:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(VALUE_DNS1).perform()
                # DNS server 2
                elif l.text == 'DNS Server 2':
                    dns_2 = f.find_elements_by_css_selector(input)
                    for i in dns_2:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(VALUE_DNS2).perform()
                    break
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

                list_actual3 = [_check_apply]
                list_expected3 = [return_true]
                check = assert_list(list_actual3, list_expected3)
            else:
                check = assert_list([return_true], [return_true])

            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Goto Network>Internet: Change values of Internet Settings: Static IP. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Goto Network>Internet: Change values of Internet Settings: Static IP '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append(
                '4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            # Login
            grand_login(driver)
            time.sleep(1)

            # Get Wan IP address
            wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_elements_by_css_selector(card_cls)[0]
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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
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
            if res_wan_primary['ipv4']['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'

            list_actual4 = [_actual]
            list_expected4 = [_expected]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check information changed: Static IP. ' 
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check information changed: Static IP. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append(
                '5. Assertion wong.')
            self.list_steps.append('[END TC]')
        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        # try:
        #     goto_menu(driver, network_tab, network_internet_tab)
        #     wait_popup_disappear(driver, dialog_loading)
        #     if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
        #         internet_setting = driver.find_element_by_css_selector(internet_setting_block_single)
        #     else:
        #         internet_setting = driver.find_element_by_css_selector(internet_setting_block)
        #     ActionChains(driver).move_to_element(internet_setting).perform()
        #
        #     # Settings
        #     internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
        #     internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
        #     for l, f in zip(internet_setting_label, internet_setting_fields):
        #         # Connection type
        #         if l.text == 'Connection Type':
        #             f.click()
        #             time.sleep(0.2)
        #             ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
        #             for o in ls_option:
        #                 if o.text == 'PPPoE':
        #                     o.click()
        #                     break
        #             break
        #     time.sleep(1)
        #     internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
        #     internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
        #     for l, f in zip(internet_setting_label, internet_setting_fields):
        #         # User name
        #         if l.text == 'User Name':
        #             user_box = f.find_element_by_css_selector(input)
        #             ActionChains(driver).move_to_element(user_box).click().key_down(Keys.CONTROL).send_keys('a').key_up(
        #                 Keys.CONTROL).send_keys(Keys.DELETE).send_keys(PPPoE_USER).perform()
        #         if l.text == 'Password':
        #             # pw_box
        #             pw_box = f.find_element_by_css_selector(input)
        #             ActionChains(driver).move_to_element(pw_box).click().key_down(Keys.CONTROL).send_keys('a').key_up(
        #                 Keys.CONTROL).send_keys(Keys.DELETE).send_keys(PPPoE_PW).perform()
        #             break
        #
        #     # Click Apply of this enable
        #     time.sleep(0.2)
        #     btn_apply = internet_setting.find_element_by_css_selector(apply)
        #     _check_apply = btn_apply.is_displayed()
        #     if _check_apply:
        #         btn_apply.click()
        #         time.sleep(0.5)
        #         # Click OK
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(1)
        #         wait_popup_disappear(driver, dialog_loading)
        #         time.sleep(5)
        #         wait_popup_disappear(driver, dialog_loading)
        #         time.sleep(5)
        #
        #         list_actual5 = [_check_apply]
        #         list_expected5 = [return_true]
        #         check = assert_list(list_actual5, list_expected5)
        #
        #     self.assertTrue(check["result"])
        #     self.list_steps.append(
        #         '[Pass] 6. Goto Network>Internet: Change values of Internet Settings: PPPoE '
        #         f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        # except:
        #     self.list_steps.append(
        #         f'[Fail] 6. Goto Network>Internet: Change values of Internet Settings: PPPoE . '
        #         f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        #     list_step_fail.append(
        #         '6. Assertion wong.')
        #
        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        # try:
        #     # Login
        #     grand_login(driver)
        #     time.sleep(1)
        #     # Get Wan IP address
        #     wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
        #     # Click icons Internet connection
        #     driver.find_element_by_css_selector(home_img_connection).click()
        #     time.sleep(1)
        #
        #     primary = driver.find_elements_by_css_selector(card_cls)[0]
        #     ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
        #     dict_wan = {}
        #     for w in ls_wan_field:
        #         label = w.find_element_by_css_selector(home_wan_ls_label).text
        #         value = w.find_element_by_css_selector(home_wan_ls_value).text
        #         dict_wan.update({label: value})
        #
        #     translate_key_api2ui = {"linkType": "WAN Type",
        #                             "mode": "Connection Type",
        #                             "address": "WAN IP Address",
        #                             "subnet": "Subnet Mask",
        #                             "gateway": "Gateway",
        #                             "dnsServer1": "DNS Server 1",
        #                             "dnsServer2": "DNS Server 2"}
        #     USER_LOGIN = get_config('ACCOUNT', 'user')
        #     PW_LOGIN = get_config('ACCOUNT', 'password')
        #     _token = get_token(USER_LOGIN, PW_LOGIN)
        #     res_wan_primary = call_api(URL_API, METHOD, BODY, _token)
        #
        #     _actual = [dict_wan[i] for i in translate_key_api2ui.values()]
        #     _expected = []
        #     for i in translate_key_api2ui.keys():
        #         if i != 'linkType':
        #             _expected.append(res_wan_primary['ipv4'][i])
        #         else:
        #             _expected.append(res_wan_primary[i])
        #
        #     if res_wan_primary['linkType'] == 'ethernet':
        #         _expected[0] = 'Ethernet'
        #     if res_wan_primary['ipv4']['mode'] == 'static':
        #         _expected[1] = 'Static IP'
        #     if res_wan_primary['ipv4']['dnsServer2'] == '':
        #         _expected[-1] = '0.0.0.0'
        #     time.sleep(5)
        #
        #     list_actual6 = [_actual]
        #     list_expected6 = [_expected]
        #     check = assert_list(list_actual6, list_expected6)
        #     self.assertTrue(check["result"])
        #     self.list_steps.append(
        #         '[Pass] 7. Check information changed: PPPoE. '
        #         f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        #     self.list_steps.append('[END TC]')
        # except:
        #     self.list_steps.append(
        #         f'[Fail] 7. Check information changed: PPPoE. '
        #         f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        #     self.list_steps.append('[END TC]')
        #     list_step_fail.append('7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_02_NETWORK_Check_Dynamic_IP_Operation(self):
        self.key = 'NETWORK_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================
        URL_LOGIN = get_config('URL', 'url')
        USER_LOGIN = get_config('ACCOUNT', 'user')
        PW_LOGIN = get_config('ACCOUNT', 'password')
        URL_API = URL_LOGIN + '/api/v1/network/wan/0'
        URL_PING_CHECK = 'google.com'
        METHOD = 'GET'
        BODY = None

        try:
            grand_login(driver)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

            if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
                internet_setting = driver.find_element_by_css_selector(internet_setting_block_single)
            else:
                internet_setting = driver.find_element_by_css_selector(internet_setting_block)
            ActionChains(driver).move_to_element(internet_setting).perform()

            # Settings
            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # Connection type
                if l.text == 'Connection Type':
                    f.click()
                    time.sleep(0.2)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Dynamic IP':
                            o.click()
                            break
                    break

            time.sleep(0.5)
            # Settings
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # Manual DNS
                if l.text == 'Manual DNS':
                    _check_manual_dns_selected = f.find_element_by_css_selector(input)
                    if not _check_manual_dns_selected.is_selected():
                        f.click()
                        time.sleep(0.5)
                        break

            # Get again
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            time.sleep(1)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # DNS server 1
                if l.text == 'DNS Server 1':
                    dns_1 = f.find_elements_by_css_selector(input)
                    for i in dns_1:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(0).perform()
                # DNS server 2
                elif l.text == 'DNS Server 2':
                    dns_2 = f.find_elements_by_css_selector(input)
                    for i in dns_2:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(0).perform()

            check_require_warning = len(driver.find_elements_by_xpath(text_field_required)) > 0

            list_actual3 = [check_require_warning]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Delete DNS server info: Check text This field is required display. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Delete DNS server info: Check text This field is required display. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Disable Manual DNS
        try:
            # Disabled Manual DNS
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # Manual DNS
                if l.text == 'Manual DNS':
                    _check_manual_dns_selected = f.find_element_by_css_selector(input)
                    if _check_manual_dns_selected.is_selected():
                        f.click()
                        time.sleep(0.5)
                        break
                    break

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

            list_actual4 = [check_page_nw]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            grand_login(driver)
            time.sleep(1)
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(ele_wan_block)
            ls_wan_field = primary.find_elements_by_css_selector(home_wan_ls_fields)
            dict_wan = {}
            for w in ls_wan_field:
                label_wan = w.find_element_by_css_selector(home_wan_ls_label).text
                value = w.find_element_by_css_selector(home_wan_ls_value).text
                dict_wan.update({label_wan: value})
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            _token = get_token(USER_LOGIN, PW_LOGIN)
            time.sleep(2)
            translate_key_api2ui = {"linkType": "WAN Type",
                                    "mode": "Connection Type",
                                    "address": "WAN IP Address",
                                    "subnet": "Subnet Mask",
                                    "gateway": "Gateway",
                                    "dnsServer1": "DNS Server 1",
                                    "dnsServer2": "DNS Server 2"}
            res_wan_primary = call_api(URL_API, METHOD, BODY, _token)
            time.sleep(2)
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


            list_actual7 = [_actual]
            list_expected7 = [_expected]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Check Information of WAN IP. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_actual7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Check Information of WAN IP. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_actual7)}')
            list_step_fail.append(
                '7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)

            list_actual8 = [check_ping]
            list_expected8 = [return_true]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 8. Ping to Google successfully. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8. Ping to Google successfully. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '8. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_03_NETWORK_Check_Static_IP_Operation(self):
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
        SUBNET_MASK = '255.255.255.0'
        SUBNET_MASK_SPLIT = SUBNET_MASK.split('.')

        try:
            grand_login(driver)
            time.sleep(1)

            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)

            primary = driver.find_element_by_css_selector(ele_wan_block)
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

            if len(driver.find_elements_by_css_selector(internet_setting_block)) == 0:
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
                    f.click()
                    time.sleep(0.2)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Static IP':
                            o.click()
                            break
                    break

            # Get again
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # WAN IP Address
                if l.text == 'WAN IP Address':
                    wan_addr = f.find_elements_by_css_selector(input)
                    for i in wan_addr:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
                # Gateway
                if l.text == 'Gateway':
                    wan_addr = f.find_elements_by_css_selector(input)
                    for i in wan_addr:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
                # DNS server 1
                if l.text == 'DNS Server 1':
                    dns_1 = f.find_elements_by_css_selector(input)
                    for i in dns_1:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
                # DNS server 2
                elif l.text == 'DNS Server 2':
                    dns_2 = f.find_elements_by_css_selector(input)
                    for i in dns_2:
                        ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()

            # Verify This field is required
            check_required_warning = len(driver.find_elements_by_xpath(text_field_required)) > 0

            list_actual = [check_required_warning]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Delete DNS server info: Check text This field is required. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Delete DNS server info: Check text This field is required. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Disable Manual DNS
        try:
            # Get again
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # WAN IP Address
                if l.text == 'WAN IP Address':
                    wan_ip_addr = f.find_elements_by_css_selector(input)
                    for d, v in zip(wan_ip_addr, wan_ip_addr_value):
                        ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(v).perform()
                # Gateway
                if l.text == 'Gateway':
                    gateway_ = f.find_elements_by_css_selector(input)
                    for d, v in zip(gateway_, wan_gateway_value):
                        ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(v).perform()
                # DNS server 1
                if l.text == 'DNS Server 1':
                    dns_1 = f.find_elements_by_css_selector(input)
                    for d, v in zip(dns_1, VALUE_DNS1_SPLIT):
                        ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(v).perform()
                # DNS server 2
                elif l.text == 'DNS Server 2':
                    dns_2 = f.find_elements_by_css_selector(input)
                    for d, v in zip(dns_2, VALUE_DNS2_SPLIT):
                        ActionChains(driver).move_to_element(d).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                            Keys.CONTROL).send_keys(v).perform()
                    break

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
                '[Pass] 4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            grand_login(driver)
            time.sleep(1)

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
            USER_LOGIN = get_config('ACCOUNT', 'user')
            PW_LOGIN = get_config('ACCOUNT', 'password')
            _token = get_token(USER_LOGIN, PW_LOGIN)
            time.sleep(1)
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
                '[Pass] 7. Check Information of WAN IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
                '[Pass] 8. Ping to Google successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8. Ping to Google successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '8. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_05_NETWORK_Dual_WAN_Enable_Disable(self):
        self.key = 'NETWORK_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            # Title
            nw_title_page = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [nw_title_page]
            list_expected = ['Network > Internet']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login and Check title of Network Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2.Login and Check title of Network Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            _check_dual_selected = driver.find_element_by_css_selector(dual_wan_input)
            if not _check_dual_selected.is_selected():
                driver.find_element_by_css_selector(dual_wan_button).click()

            dual_wan_block = driver.find_element_by_css_selector(dual_wan_block_ele)
            # Apply
            dual_wan_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            dual_wan_block = driver.find_element_by_css_selector(dual_wan_block_ele)
            # Settings
            dual_wan_labels = dual_wan_block.find_elements_by_css_selector(label_name_in_2g)
            dual_wan_fields = dual_wan_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(dual_wan_labels, dual_wan_fields):
                if l.text == 'Dual WAN':
                    default_dual_wan = f.find_element_by_css_selector(input).is_selected()
                    continue

                if l.text == 'Primary WAN':
                    default_primary_wan = f.find_element_by_css_selector(ele_data_placeholder).text
                    f.click()
                    time.sleep(0.5)
                    ls_option = f.find_elements_by_css_selector(active_drop_down_values)
                    total_value_primary = [o.text for o in ls_option]
                    f.click()
                    time.sleep(0.5)
                    continue

                if l.text == 'Secondary WAN':
                    default_secondary_wan = f.find_element_by_css_selector(ele_data_placeholder).text
                    f.click()
                    time.sleep(0.5)
                    ls_option = f.find_elements_by_css_selector(active_drop_down_values)
                    total_value_secondary = [o.text for o in ls_option]
                    f.click()
                    time.sleep(0.5)
                    continue

                if l.text == 'Dual WAN Type':
                    default_dual_wan_type = f.find_element_by_css_selector(ele_data_placeholder).text
                    f.click()
                    time.sleep(0.5)
                    ls_option = f.find_elements_by_css_selector(active_drop_down_values)
                    total_value_dual_wan_type = [o.text for o in ls_option]
                    f.click()
                    time.sleep(0.5)
                    break

            list_actual3 = [default_dual_wan,
                           default_primary_wan, total_value_primary,
                           default_secondary_wan, total_value_secondary,
                           default_dual_wan_type, total_value_dual_wan_type]
            list_expected3 = [return_true,
                             'Ethernet', ['Ethernet', 'USB Broadband', 'Android Tethering'],
                             'USB Broadband', ['Ethernet', 'USB Broadband', 'Android Tethering'],
                             'Fail Over', ['Load Balance', 'Fail Over']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Enable Dual WAN then click Apply. Check Default Dual WAN enabled, '
                f'Default Primary WAN value and list options,'
                f'Default Secondary WAN value and list options'
                f'Default Dual WAN Type value and list options. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Enable Dual WAN then click Apply. Check Default Dual WAN enabled, '
                f'Default Primary WAN value and list options, '
                f'Default Secondary WAN value and list options, '
                f'Default Dual WAN Type value and list options. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            _check_dual_selected = driver.find_element_by_css_selector(dual_wan_input)
            if _check_dual_selected.is_selected():
                driver.find_element_by_css_selector(dual_wan_button).click()

            dual_wan_block = driver.find_element_by_css_selector(dual_wan_block_ele)
            # Apply
            dual_wan_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            dual_wan_block = driver.find_element_by_css_selector(dual_wan_block_ele)
            # Settings
            dual_wan_labels = dual_wan_block.find_elements_by_css_selector(label_name_in_2g)
            dual_wan_fields = dual_wan_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(dual_wan_labels, dual_wan_fields):
                if l.text == 'Dual WAN':
                    default_dual_wan_2 = f.find_element_by_css_selector(input).is_selected()
                    break

            list_actual4 = [default_dual_wan_2]
            list_expected4 = [return_false]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4 Disable Dual WAN then click Apply. Check Dual WAN disabled. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Disable Dual WAN then click Apply. Check Dual WAN disabled. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_06_NETWORK_Dual_WAN_Check_Primary_Setting(self):
        self.key = 'NETWORK_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            # Title
            nw_title_page = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [nw_title_page]
            list_expected = ['Network > Internet']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login and Check title of Network Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2.Login and Check title of Network Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            _check_dual_selected = driver.find_element_by_css_selector(dual_wan_input)
            if not _check_dual_selected.is_selected():
                driver.find_element_by_css_selector(dual_wan_button).click()

            dual_wan_block = driver.find_element_by_css_selector(dual_wan_block_ele)

            # Settings
            dual_wan_fields = dual_wan_block.find_elements_by_css_selector(wrap_input)
            dual_wan_label = dual_wan_block.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(dual_wan_label, dual_wan_fields):
                # Primary = Ethernet
                if l.text == 'Primary WAN':
                    f.click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Ethernet':
                            o.click()
                            for sl, sv in zip(dual_wan_label, dual_wan_fields):
                                if sl.text == 'Secondary WAN':
                                    check_secondary_1 = sv.text
                                    break
                            break
                    break

            for l, f in zip(dual_wan_label, dual_wan_fields):
                # Primary = Ethernet
                if l.text == 'Primary WAN':
                    f.click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'USB':
                            o.click()
                            for sl, sv in zip(dual_wan_label, dual_wan_fields):
                                if sl.text == 'Secondary WAN':
                                    check_secondary_2 = sv.text
                                    break
                            break
                    break

            for l, f in zip(dual_wan_label, dual_wan_fields):
                # Primary = Ethernet
                if l.text == 'Primary WAN':
                    f.click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Android Tethering':
                            o.click()
                            for sl, sv in zip(dual_wan_label, dual_wan_fields):
                                if sl.text == 'Secondary WAN':
                                    check_secondary_3 = sv.text
                                    break
                            break
                    break

            exp_secondary_1 = 'USB'
            exp_secondary_2 = 'Ethernet'
            exp_secondary_3 = 'Ethernet'
            list_actual = [check_secondary_1, check_secondary_2, check_secondary_3]
            list_expected = [exp_secondary_1, exp_secondary_2, exp_secondary_3]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3, 4, 5, 6. Enabled Dual WAN. Verify relate between Primary to Secondary WAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4, 5, 6. Enabled Dual WAN. Verify relate between Primary to Secondary WAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3, 4, 5, 6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_07_NETWORK_Dual_WAN_Check_Secondary_Setting(self):
        self.key = 'NETWORK_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)
            # Title
            nw_title_page = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [nw_title_page]
            list_expected = ['Network > Internet']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1, 2. Login and Check title of Network Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2.Login and Check title of Network Internet. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            _check_dual_selected = driver.find_element_by_css_selector(dual_wan_input)
            if not _check_dual_selected.is_selected():
                driver.find_element_by_css_selector(dual_wan_button).click()

            dual_wan_block = driver.find_element_by_css_selector(dual_wan_block_ele)

            # Settings
            dual_wan_fields = dual_wan_block.find_elements_by_css_selector(wrap_input)
            dual_wan_label = dual_wan_block.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(dual_wan_label, dual_wan_fields):
                # Primary = Ethernet
                if l.text == 'Secondary WAN':
                    f.click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Ethernet':
                            o.click()
                            for sl, sv in zip(dual_wan_label, dual_wan_fields):
                                if sl.text == 'Primary WAN':
                                    check_primary_1 = sv.text
                                    break
                            break
                    break

            for l, f in zip(dual_wan_label, dual_wan_fields):
                # Primary = Ethernet
                if l.text == 'Secondary WAN':
                    f.click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'USB':
                            o.click()
                            for sl, sv in zip(dual_wan_label, dual_wan_fields):
                                if sl.text == 'Primary WAN':
                                    check_primary_2 = sv.text
                                    break
                            break
                    break

            for l, f in zip(dual_wan_label, dual_wan_fields):
                # Primary = Ethernet
                if l.text == 'Secondary WAN':
                    f.click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == 'Android Tethering':
                            o.click()
                            for sl, sv in zip(dual_wan_label, dual_wan_fields):
                                if sl.text == 'Primary WAN':
                                    check_primary_3 = sv.text
                                    break
                            break
                    break

            exp_primary_1 = 'USB'
            exp_primary_2 = 'Ethernet'
            exp_primary_3 = 'Ethernet'
            list_actual = [check_primary_1, check_primary_2, check_primary_3]
            list_expected = [exp_primary_1, exp_primary_2, exp_primary_3]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3, 4, 5, 6. Enabled Dual WAN. Verify relate between Secondary to Primary WAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4, 5, 6. Verify relate between Secondary to Primary WAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3, 4, 5, 6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    # def test_17_NETWORK_Check_operation_of_changing_Gateway_address(self):
    #     self.key = 'NETWORK_17'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     IP1 = '192.168.10.1'
    #     IP1_VALUE = IP1.split('.')
    #     GOOGLE_URL = get_config('COMMON', 'google_url', input_data_path)
    #     YOUTUBE_URL = get_config('COMMON', 'youtube_url', input_data_path)
    #     # ===========================================================
    #     try:
    #         grand_login(driver)
    #         time.sleep(1)
    #         # Network Lan Tab
    #         goto_menu(driver, network_tab, network_lan_tab)
    #
    #         lan_block = driver.find_element_by_css_selector(network_lan_card)
    #         # Settings
    #         lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
    #         lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)
    #
    #         for l, f in zip(lan_label, lan_fields):
    #             if l.text == 'IP Address':
    #                 f.find_element_by_css_selector(option_select).click()
    #                 time.sleep(0.5)
    #                 ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
    #                 for o in ls_option:
    #                     # Type C
    #                     if o.text == IP1_VALUE[0]:
    #                         o.click()
    #
    #                 # Change IP range to 192.168.10.1
    #                 ip_address_range = driver.find_elements_by_css_selector(ele_ip_address_range_input)
    #                 for i in range(2):
    #                     ip_address_range[0].clear()
    #                     ip_address_range[0].send_keys(IP1_VALUE[2])
    #                 for i in range(2):
    #                     ip_address_range[1].clear()
    #                     ip_address_range[1].send_keys(IP1_VALUE[3])
    #                 break
    #
    #         for l, f in zip(lan_label, lan_fields):
    #             if l.text == 'Start IP Address':
    #                 start_ip_value = f.text
    #                 end_val = f.find_element_by_css_selector(input).get_attribute('value')
    #                 start_ip_value = start_ip_value + end_val
    #                 start_ip_value = start_ip_value.replace(' ', '')
    #             if l.text == 'End IP Address':
    #                 end_ip_value = f.text
    #                 end_val = f.find_element_by_css_selector(input).get_attribute('value')
    #                 end_ip_value = end_ip_value + end_val
    #                 end_ip_value = end_ip_value.replace(' ', '')
    #                 break
    #
    #         list_actual2 = [start_ip_value.split('.')[:3], end_ip_value.split('.')[:3]]
    #         list_expected2 = [IP1.split('.')[:3]]*2
    #         check = assert_list(list_actual2, list_expected2)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 1, 2. Login. Change IP Address. Check Start IP and End IP according to bandwidth. '
    #             f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1, 2. Login. Change IP Address. Check Start IP and End IP according to bandwidth. '
    #             f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
    #         list_step_fail.append('1, 2. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         # Click Apply
    #         lan_block = driver.find_element_by_css_selector(network_lan_card)
    #         lan_block.find_element_by_css_selector(submit_btn).click()
    #         # Get confirm message
    #         check_confirm_message = driver.find_element_by_css_selector(confirm_dialog_msg).text
    #         exp_confirm_message = f'In order to complete the setup of the system must be restart. After restarting, move to new LAN IP Address ({IP1}). Continue?'
    #         # Click OK
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(100)
    #         wait_visible(driver, lg_page)
    #
    #         list_actual3 = [check_confirm_message]
    #         list_expected3 = [exp_confirm_message]
    #         check = assert_list(list_actual3, list_expected3)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 3. Click Apply. Check Confirm message. '
    #             f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 3. Check Subnet Mask value when Ip Address is class B and verify en Start/End Ip <16 bits. '
    #             f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
    #         list_step_fail.append('3. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         # Check in command line
    #         check_ip_in_cmd = get_url_ipconfig(ipconfig_field='Default Gateway')
    #         # Check connect
    #         URL_NEW = 'http://' + check_ip_in_cmd
    #         USER_ = get_config('ACCOUNT', 'user')
    #         PW_ = get_config('ACCOUNT', 'password')
    #         grand_login(driver, URL_NEW, USER_, PW_)
    #
    #         check_login_new_url = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
    #         # Check connect with external communication
    #         driver.get(GOOGLE_URL)
    #         time.sleep(5)
    #         check_google = len(driver.find_elements_by_css_selector(google_img)) > 0
    #
    #         driver.get(YOUTUBE_URL)
    #         time.sleep(5)
    #         check_youtube = len(driver.find_elements_by_css_selector('#logo-icon-container')) != 0
    #
    #         list_actual4 = [check_ip_in_cmd, check_login_new_url, check_google, check_youtube]
    #         list_expected4 = [IP1] + [return_true] * 3
    #         check = assert_list(list_actual4, list_expected4)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 4. Check IP in cmd, Check login by New IP Address, Check goto GOOGLE and YOUTUBE. '
    #             f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 4. Check IP in cmd, Check login by New IP Address, Check goto GOOGLE and YOUTUBE..'
    #             f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append(
    #             '4. Assertion wong.')
    #
    #     self.assertListEqual(list_step_fail, [])
    # OK
    def test_18_NETWORK_LAN_Change_Subnet_Mask(self):
        self.key = 'NETWORK_18'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(1)
            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)

            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Settings
            lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
            lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)

            for l, f in zip(lan_label, lan_fields):
                if l.text == 'IP Address':
                    f.find_element_by_css_selector(option_select).click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        # Type C
                        if o.text == '192':
                            o.click()
                            for sl, sv in zip(lan_label, lan_fields):
                                if sl.text == 'Subnet Mask':
                                    check_subnet_c = sv.find_element_by_css_selector(option_select).text
                                    break
                            break
                    break

            list_actual = [check_subnet_c]
            list_expected = exp_nw_subnet_type_c
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Check Subnet Mask value when Ip Address is class C. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Subnet Mask value when Ip Address is class C. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'IP Address':
                    f.find_element_by_css_selector(option_select).click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        # Type B
                        if o.text == '172':
                            o.click()
                            for sl, sv in zip(lan_label, lan_fields):
                                if sl.text == 'Subnet Mask':
                                    sv.click()
                                    time.sleep(0.5)
                                    ls_option_subnet = driver.find_elements_by_css_selector(active_drop_down_values)
                                    check_subnet_b = [i.text for i in ls_option_subnet]
                                    for so in ls_option_subnet:
                                        if so.text == '255.255.0.0':
                                            so.click()
                                            time.sleep(1)
                                    break
                            break
                    break

            # Verify lower than 16 bit
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    start_ip_16 = len(f.find_elements_by_css_selector(input_filed)) == 2
                if l.text == 'End IP Address':
                    end_ip_16 = len(f.find_elements_by_css_selector(input_filed)) == 2
            list_actual = check_subnet_b + [start_ip_16, end_ip_16]
            list_expected = exp_nw_subnet_type_b + [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2,3. Check Subnet Mask value when Ip Address is class B and verify en Start/End Ip <16 bits. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 2,3. Check Subnet Mask value when Ip Address is class B and verify en Start/End Ip <16 bits. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'IP Address':
                    f.find_element_by_css_selector(option_select).click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        # Type B
                        if o.text == '10':
                            o.click()
                            for sl, sv in zip(lan_label, lan_fields):
                                if sl.text == 'Subnet Mask':
                                    sv.click()
                                    time.sleep(0.5)
                                    ls_option_subnet = driver.find_elements_by_css_selector(active_drop_down_values)
                                    check_subnet_a = [i.text for i in ls_option_subnet]
                                    for so in ls_option_subnet:
                                        if so.text == '255.255.0.0':
                                            so.click()
                                            time.sleep(0.5)
                                            # Verify lower than 16 bit
                                            for l, f in zip(lan_label, lan_fields):
                                                if l.text == 'Start IP Address':
                                                    start_ip_16 = len(f.find_elements_by_css_selector(input_filed)) == 2
                                                if l.text == 'End IP Address':
                                                    end_ip_16 = len(f.find_elements_by_css_selector(input_filed)) == 2
                                                    break
                                    sv.click()
                                    time.sleep(0.5)
                                    ls_option_subnet = driver.find_elements_by_css_selector(active_drop_down_values)
                                    for so in ls_option_subnet:
                                        if so.text == '255.0.0.0':
                                            so.click()
                                            time.sleep(0.5)
                                            # Verify lower than 16 bit
                                            for l, f in zip(lan_label, lan_fields):
                                                if l.text == 'Start IP Address':
                                                    start_ip_24 = len(f.find_elements_by_css_selector(input_filed)) == 3
                                                if l.text == 'End IP Address':
                                                    end_ip_24 = len(f.find_elements_by_css_selector(input_filed)) == 3
                                                    break

                                    break
                            break
                    break

            list_actual = check_subnet_a + [start_ip_16, end_ip_16, start_ip_24, end_ip_24]
            list_expected = exp_nw_subnet_type_a + [return_true, return_true, return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4,5,6. Check Subnet Mask value when Ip Address is class A and verify en Start/End Ip <16, 24 bits. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')

            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4,5,6. Check Subnet Mask value when Ip Address is class A and verify en Start/End Ip <16, 24 bits.'
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4,5,6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_20_NETWORK_Change_IP_assignment_range(self):
        self.key = 'NETWORK_20'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            # Enable Dual WAN
            goto_menu(driver, network_tab, network_lan_tab)
            # Title
            nw_title_page = driver.find_element_by_css_selector(ele_title_page).text

            list_actual = [nw_title_page]
            list_expected = ['Network > LAN']
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Login and Check title of Network > LAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Login and Check title of Network > LAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1. Assertion wong.')

        try:
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Verify LAN block information
            labels = lan_block.find_elements_by_css_selector(label_name_in_2g)
            values = lan_block.find_elements_by_css_selector(ele_dtim_textbox_cls)
            for l, v in zip(labels, values):
                if l.text == 'Start IP Address':
                    start_ip_modify = v.find_element_by_css_selector(ele_wl_ssid_value_field)
                    for j in range(2):
                        start_ip_modify.clear()
                        start_ip_modify.send_keys('5')

                if l.text == 'End IP Address':
                    end_ip_modify = v.find_element_by_css_selector(ele_wl_ssid_value_field)
                    for j in range(2):
                        end_ip_modify.clear()
                        end_ip_modify.send_keys('37')
                    break

            # Click Apply
            if len(lan_block.find_elements_by_css_selector(ele_btn_close)) > 0:
                if lan_block.find_element_by_css_selector(ele_btn_close).is_displayed():
                    lan_block.find_element_by_css_selector(ele_btn_close).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(0.5)

            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Verify LAN block information
            labels = lan_block.find_elements_by_css_selector(label_name_in_2g)
            values = lan_block.find_elements_by_css_selector(ele_dtim_textbox_cls)
            for l, v in zip(labels, values):
                if l.text == 'Start IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    new_start_ip_address = _123 + _4_value
                    new_start_ip_address = new_start_ip_address.replace(' ', '')
                    continue

                if l.text == 'End IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    new_end_ip_address = _123 + _4_value
                    new_end_ip_address = new_end_ip_address.replace(' ', '')
                    break

            list_actual2 = [new_start_ip_address, new_end_ip_address]
            list_expected2 = ['192.168.1.5', '192.168.1.37']
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Change Start IP and End IP. Check apply successfully. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Change Start IP and End IP. Check apply successfully. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            # Release
            subprocess.check_output('ipconfig/release', shell=True)
            time.sleep(2)
            # Renew
            subprocess.check_output('ipconfig/renew', shell=True)
            time.sleep(8)
            # All
            config_all = subprocess.check_output('ipconfig/all', shell=True)
            time.sleep(2)

            ethernet = config_all.decode('utf8').split('Ethernet adapter Ethernet:')[1]
            for i in ethernet.splitlines():
                if i.strip().startswith('IPv4 Address'):
                    ipv4_address = i.split(': ')[1].split('(Preferred)')[0]
                    break
            ip_value = int(ipv4_address.split('.')[-1])
            start_value = int(new_start_ip_address.split('.')[-1])
            end_value = int(new_end_ip_address.split('.')[-1])

            check = start_value <= ip_value <= end_value

            list_actual3 = [check]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Command: ipconfig/release > ipconfig/renew > ipconfig/all: {ipv4_address} - '
                f'Check IPv4 between range Start IP and End IP. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Command: ipconfig/release > ipconfig/renew > ipconfig/all: {ipv4_address} - '
                f'Check IPv4 between range Start IP and End IP. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_21_NETWORK_Verify_Start_End_Ip_Address_input_value(self):
        self.key = 'NETWORK_21'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        LAN_IP_ADDRESS = '192.168.1.10'
        LAN_IP_ADDRESS_SPLIT = LAN_IP_ADDRESS.split('.')

        try:
            grand_login(driver)
            time.sleep(1)
            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)

            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Settings
            lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
            lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)

            for l, f in zip(lan_label, lan_fields):
                if l.text == 'IP Address':
                    f.find_element_by_css_selector(option_select).click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        # Type C
                        if o.text == '192':
                            o.click()
                            break
                    # Init precondition
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, LAN_IP_ADDRESS_SPLIT[2:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                        time.sleep(0.2)
                    break

            # 1 Edit Start IP address > End IP address
            START_IP_ADDRESS = '192.168.1.100'
            START_IP_ADDRESS_SPLIT = START_IP_ADDRESS.split('.')
            END_IP_ADDRESS = '192.168.1.99'
            END_IP_ADDRESS_SPLIT = END_IP_ADDRESS.split('.')

            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    # Init precondition
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, START_IP_ADDRESS_SPLIT[3:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                        break
                if l.text == 'End IP Address':
                    # Init precondition
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, END_IP_ADDRESS_SPLIT[3:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                    break
            # Click Apply
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(0.5)

            # Verify Message
            error_msg = lan_block.find_element_by_css_selector(error_message).text

            list_actual = [error_msg]
            list_expected = [exp_error_msg_start_less_end]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Set start IP Address more than End IP Address: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Set start IP Address more than End IP Address: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            IP_SMALL = str(random.randint(1, 32))
            # Settings
            lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
            lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f in ip_addr_fields:
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(IP_SMALL).perform()
                if l.text == 'End IP Address':
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f in ip_addr_fields:
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(IP_SMALL).perform()
                    break
            # Click Apply
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(0.5)

            # Verify Message
            error_msg = lan_block.find_element_by_css_selector(error_message).text

            list_actual = [error_msg]
            list_expected = [exp_error_msg_start_end_small]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 2. Set start IP Address, End IP Address Small: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Set start IP Address, End IP Address Small: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Settings
            lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
            lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, LAN_IP_ADDRESS_SPLIT[3:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                if l.text == 'End IP Address':
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, LAN_IP_ADDRESS_SPLIT[3:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                    break
            # Click Apply
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(0.5)

            # Verify Message
            error_msg = lan_block.find_element_by_css_selector(error_message).text

            list_actual = [error_msg]
            list_expected = [exp_error_msg_start_end_same_lan_ip]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # 1 Edit Start IP address > End IP address
            START_IP_ADDRESS = '192.168.1.3'
            START_IP_ADDRESS_SPLIT = START_IP_ADDRESS.split('.')
            END_IP_ADDRESS = '192.168.1.100'
            END_IP_ADDRESS_SPLIT = END_IP_ADDRESS.split('.')

            # Settings
            lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
            lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, START_IP_ADDRESS_SPLIT[3:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                if l.text == 'End IP Address':
                    ip_addr_fields = f.find_elements_by_css_selector(input_not_disabled)
                    for f, v in zip(ip_addr_fields, END_IP_ADDRESS_SPLIT[3:]):
                        ActionChains(driver).move_to_element(f).click().key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).send_keys(v).perform()
                    break
            # Click Apply
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(0.5)

            # Verify Message
            error_msg = driver.find_element_by_css_selector(dialog_content).text

            list_actual = [error_msg]
            list_expected = [exp_error_msg_start_end_include_lan_ip]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_25_NETWORK_Reserved_IP_Confirm_duplicate_registration_prevention(self):
        self.key = 'NETWORK_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================
        MAC_2 = get_config('NETWORK', 'nw25_mac2', input_data_path)
        IP_2 = get_config('NETWORK', 'nw25_ip2', input_data_path)
        MAC_4 = get_config('NETWORK', 'nw25_mac4', input_data_path)
        IP_4 = get_config('NETWORK', 'nw25_ip4', input_data_path)
        MAC_6 = get_config('NETWORK', 'nw25_mac6', input_data_path)
        IP_6 = get_config('NETWORK', 'nw25_ip6', input_data_path)
        try:
            grand_login(driver)
            time.sleep(1)

            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)

            wait_popup_disappear(driver, dialog_loading)
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)

            nw_add_reserved_ip(driver, MAC_2, IP_2)

            reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.2)
            reserved_ip_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [MAC_2, IP_2]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Add Reserved IP successfully. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Add Reserved IP successfully. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            nw_add_reserved_ip(driver, MAC_4, IP_4)
            time.sleep(1)
            reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(1)
            error_msg = reserved_ip_block.find_element_by_css_selector(custom_error_cls).text
            # Cancel
            reserved_ip_block.find_element_by_css_selector(btn_cancel).click()

            list_actual2 = [error_msg]
            list_expected2 = [exp_ip_address_exists]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 3. Check Add a new Reserved IP same IP address: Check error msg. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Add a new Reserved IP same IP address: Check error msg. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            nw_add_reserved_ip(driver, MAC_2, IP_6)
            time.sleep(1)
            # reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(1)
            error_msg = reserved_ip_block.find_element_by_css_selector(error_message).text
            # Cancel
            reserved_ip_block.find_element_by_css_selector(btn_cancel).click()

            list_actual3 = [error_msg]
            list_expected3 = [exp_mac_address_exists]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Check Add a new Reserved IP same MAC address: Check error msg. . '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Error message: MAC address same Lan IP. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            nw_add_reserved_ip(driver, MAC_6, IP_6)
            time.sleep(1)
            reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(1)
            error_msg_existed= len(reserved_ip_block.find_elements_by_css_selector(custom_error_cls)) > 0

            time.sleep(1)

            # Get info of first row
            second_row = reserved_ip_block.find_elements_by_css_selector(rows)[1]
            mac_address2 = second_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address2 = mac_address2.splitlines()[1]
            ip_addr2 = second_row.find_element_by_css_selector(ip_address_cls).text

            list_actual5 = [error_msg_existed, mac_address2, ip_addr2]
            list_expected5 = [return_true, MAC_6, IP_6]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Check Error msg displayed, Check Mac same as input, Check IP same as input. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Error msg displayed, Check Mac same as input, Check IP same as input. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_26_NETWORK_Verify_Max_entry_Registration(self):
        self.key = 'NETWORK_26'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        MAC_2 = get_config('NETWORK', 'nw26_mac2', input_data_path)
        IP_2 = get_config('NETWORK', 'nw26_ip2', input_data_path)

        try:
            grand_login(driver)
            time.sleep(1)

            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)

            wait_popup_disappear(driver, dialog_loading)
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)

            nw_add_reserved_ip(driver, MAC_2, IP_2)

            reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.2)
            reserved_ip_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [MAC_2, IP_2]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Add Reserved IP successfully. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Add Reserved IP successfully. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        try:
            # Add 32 items
            for i in range(12, 43):
                mac = f'12:12:12:12:12:{str(i+1)}'
                ip = f'192.168.1.{str(i)}'
                nw_add_reserved_ip(driver, mac, ip)
                reserved_ip_block.find_element_by_css_selector(btn_save).click()
                time.sleep(0.2)

            check_add_disabled = reserved_ip_block.find_element_by_css_selector(add_class).get_attribute('disabled') == 'true'

            reserved_ip_block.find_element_by_css_selector(add_class).click()
            check_add_to_edit = len(reserved_ip_block.find_elements_by_css_selector(edit_mode)) == 0

            list_actual1 = [check_add_disabled, check_add_to_edit]
            list_expected1 = [return_true]*2
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add 32 reserved IP. Check ADD button disabled and Click add -> Check edit form not display. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add 32 reserved IP. Check ADD button disabled and Click add -> Check edit form not display. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_27_NETWORK_Verify_update_Reserved_IP_address_follow_changing_Lan_IP(self):
        self.key = 'NETWORK_27'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        factory_dut()
        # ===============================================
        URL_PING_CHECK = '172.16.1.1'
        URL_B = 'http://172.16.1.1'
        EXPECTED_B_IP_ADDR = '172.16.1.10'
        MAC_2 = get_config('NETWORK', 'nw27_mac2', input_data_path)
        IP_2 = get_config('NETWORK', 'nw27_mac2', input_data_path)

        try:
            grand_login(driver)
            time.sleep(1)

            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)

            wait_popup_disappear(driver, dialog_loading)
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)

            nw_add_reserved_ip(driver, MAC_2, IP_2)

            reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.2)
            reserved_ip_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [MAC_2, IP_2]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Add Reserved IP successfully. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Add Reserved IP successfully. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Settings
            lan_fields = lan_block.find_elements_by_css_selector(wrap_input)
            lan_label = lan_block.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(lan_label, lan_fields):
                if l.text == 'IP Address':
                    f.find_element_by_css_selector(option_select).click()
                    time.sleep(0.5)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        # Type C
                        if o.text == '172':
                            o.click()
                            break
                    break
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(btn_ok).click()
            # wait_popup_disappear(driver, dialog_loading)
            # wait_popup_disappear(driver, dialog_loading)
            time.sleep(120)
            # wait_popup_disappear(driver, dialog_loading)
            wait_DUT_activated(URL_PING_CHECK)
            time.sleep(10)
            # wait_ping(URL_B)
            # driver.get(URL_B)
            save_config(config_path, 'URL', 'url', URL_B)
            time.sleep(5)
            grand_login(driver)

            goto_menu(driver, network_tab, network_lan_tab)
            wait_popup_disappear(driver, dialog_loading)
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual = [ip_addr]
            list_expected = [EXPECTED_B_IP_ADDR]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2,3. Change LAN IP to 172.16.1.1: Check update successfully')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2,3. Change LAN IP to 172.16.1.1: Check update successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2,3. Assertion wong.')
        # ===============================================
        factory_dut()
        save_config(config_path, 'URL', 'url', 'http://192.168.1.1')

        self.assertListEqual(list_step_fail, [])

    def test_28_NETWORK_Verify_Reserved_IP_address_when_changing_of_DHCP_range(self):
        self.key = 'NETWORK_28'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        IP_ADDRESS_MAC = get_config('NETWORK', 'nw_28_step3_mac', input_data_path)
        IP_ADDRESS_MORE_END_IP = get_config('NETWORK', 'nw28_step3_ip_address', input_data_path)
        IP_ADDRESS_LESS_END_IP = get_config('NETWORK', 'nw28_step4_ip_address', input_data_path)
        # ======================================================================
        try:
            grand_login(driver)

            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)
            wait_popup_disappear(driver, dialog_loading)
            title_text = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [title_text]
            list_expected1 = ['Network > LAN']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Check Network LAN title display. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Check Network LAN title display. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        try:
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Verify LAN block information
            labels = lan_block.find_elements_by_css_selector(label_name_in_2g)
            values = lan_block.find_elements_by_css_selector(ele_dtim_textbox_cls)
            for l, v in zip(labels, values):
                if l.text == 'IP Address':
                    _1 = v.find_element_by_css_selector(key_type_value_field).text
                    _234_ele = v.find_elements_by_css_selector(ele_wl_ssid_value_field)
                    _234_value = [i.get_attribute('value') for i in _234_ele]
                    current_ip_address = '.'.join([_1] + _234_value)
                    if not current_ip_address == '192.168.1.1':
                        # 192
                        v.find_element_by_css_selector(option_select).click()
                        time.sleep(0.5)
                        ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                        for o in ls_option:
                            # Type C
                            if o.text == '192':
                                o.click()
                                break
                        # .1.1
                        _1_1 = v.find_elements_by_css_selector(ele_lan_ip_input_not_disabled)
                        for i in _1_1:
                            for j in range(2):
                                i.clear()
                                i.send_keys('1')

                if l.text == 'Start IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    current_start_ip_address = _123 + _4_value
                    if not current_start_ip_address == '192.168.1.2':
                        start_ip_modify = v.find_element_by_css_selector(ele_wl_ssid_value_field)
                        for j in range(2):
                            start_ip_modify.clear()
                            start_ip_modify.send_keys('2')

                if l.text == 'End IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    current_end_ip_address = _123 + _4_value
                    if not current_end_ip_address == '192.168.1.100':
                        end_ip_modify = v.find_element_by_css_selector(ele_wl_ssid_value_field)
                        for j in range(2):
                            end_ip_modify.clear()
                            end_ip_modify.send_keys('100')
                    break

            # Click Apply
            if len(lan_block.find_elements_by_css_selector(ele_btn_close)) > 0:
                lan_block.find_element_by_css_selector(ele_btn_close).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()

            # Handle API
            _URL_API = get_config('URL', 'url') + '/api/v1/network/lan'
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)
            _METHOD = 'GET'
            _BODY = ''
            _res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)

            _api_ip_address = _res['ipv4']['ipAddress']
            _api_subnet_mask = _res['ipv4']['subnet']
            _api_dhcp_active = _res['ipv4']['dhcp']['active']
            _api_start_ip_address = _res['ipv4']['dhcp']['startIP']
            _api_end_ip_address = _res['ipv4']['dhcp']['endIP']
            _api_lease_time = _res['ipv4']['dhcp']['leaseTime']

            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Verify LAN block information
            labels = lan_block.find_elements_by_css_selector(label_name_in_2g)
            values = lan_block.find_elements_by_css_selector(ele_dtim_textbox_cls)
            for l, v in zip(labels, values):
                if l.text == 'IP Address':
                    _1 = v.find_element_by_css_selector(key_type_value_field).text
                    _234_ele = v.find_elements_by_css_selector(ele_wl_ssid_value_field)
                    _234_value = [i.get_attribute('value') for i in _234_ele]
                    new_ip_address = '.'.join([_1] + _234_value)

                if l.text == 'Subnet Mask':
                    new_subnet = v.text

                if l.text == 'DHCP Server':
                    new_dhcp_server = v.find_element_by_css_selector(input).is_enabled()

                if l.text == 'Start IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    new_start_ip_address = _123 + _4_value
                    new_start_ip_address = new_start_ip_address.replace(' ', '')

                if l.text == 'End IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    new_end_ip_address = _123 + _4_value
                    new_end_ip_address = new_end_ip_address.replace(' ', '')

                if l.text == 'Lease Time':
                    # Lease time by Minutes
                    new_lease_time = v.find_element_by_css_selector(input).get_attribute('value')
                    new_lease_time_to_second = int(new_lease_time) * 60
                    break

            list_actual2 = [new_ip_address, new_subnet, new_dhcp_server,
                            new_start_ip_address, new_end_ip_address, new_lease_time_to_second]
            list_expected2 = [_api_ip_address, _api_subnet_mask, _api_dhcp_active,
                              _api_start_ip_address, _api_end_ip_address, _api_lease_time]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Change information. Check result between web and api: '
                f'Ip address, Subnet, DHCP, Start IP, End IP, Lease time convert to second. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Change information. Check result between web and api: '
                f'Ip address, Subnet, DHCP, Start IP, End IP, Lease time convert to second. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong.')

        try:
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)
            nw_add_reserved_ip(driver, IP_ADDRESS_MAC, IP_ADDRESS_MORE_END_IP)

            time.sleep(0.2)
            # Check Error message display and button Save Dimmed
            error_msg_display = len(reserved_ip_block.find_elements_by_css_selector(custom_error_cls)) > 0
            # button_save_dimmed = not reserved_ip_block.find_element_by_css_selector(btn_save).is_enabled()

            list_actual3 = [error_msg_display]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Change IP address out of range. Check Error message display. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change IP address out of range. Check Error message display. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            # Click Cancel
            reserved_ip_block.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)

            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)
            nw_add_reserved_ip(driver, IP_ADDRESS_MAC, IP_ADDRESS_LESS_END_IP)
            reserved_ip_block.find_element_by_css_selector(btn_save).click()

            time.sleep(0.2)
            reserved_ip_block.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual4 = [mac_address, ip_addr]
            list_expected4 = [IP_ADDRESS_MAC, IP_ADDRESS_LESS_END_IP]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Add a reserved IP in range. Check Add successfully. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Add a reserved IP in range. Check Add successfully. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            # Change END IP Address Less than reserved IP
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Verify LAN block information
            labels = lan_block.find_elements_by_css_selector(label_name_in_2g)
            values = lan_block.find_elements_by_css_selector(ele_dtim_textbox_cls)
            for l, v in zip(labels, values):
                if l.text == 'End IP Address':
                    end_ip_modify = v.find_element_by_css_selector(ele_wl_ssid_value_field)
                    for j in range(2):
                        end_ip_modify.clear()
                        end_ip_modify.send_keys('80')
                    break

            # Click Apply
            if len(lan_block.find_elements_by_css_selector(ele_btn_close)) > 0:
                lan_block.find_element_by_css_selector(ele_btn_close).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()

            # Verify
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            # Verify LAN block information
            labels = lan_block.find_elements_by_css_selector(label_name_in_2g)
            values = lan_block.find_elements_by_css_selector(ele_dtim_textbox_cls)
            for l, v in zip(labels, values):
                if l.text == 'End IP Address':
                    _123 = v.find_element_by_css_selector(ele_lan_ip_first_start_end_ip).text
                    _4_value = v.find_element_by_css_selector(ele_wl_ssid_value_field).get_attribute('value')
                    change_end_ip_address = _123 + _4_value
                    change_end_ip_address = change_end_ip_address.replace(' ', '')
                    break
            time.sleep(2)

            list_actual5 = [change_end_ip_address]
            list_expected5 = ['192.168.1.80']
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Change End IP address less than IP of Reserved IP address. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Change End IP address less than IP of Reserved IP address. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_33_NETWORK_Repeater_Verify_of_menu_tree(self):
        self.key = 'NETWORK_33'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        # ===========================================================

        try:
            grand_login(driver)
            time.sleep(1)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Login. Check Home page is displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Login. Check Home page is displayed. . '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        try:
            ls_menu_enable = driver.find_elements_by_css_selector(ele_home_tree_menu_enable)
            ls_menu_enable_text = [i.text for i in ls_menu_enable]

            ls_menu_disable = driver.find_elements_by_css_selector(ele_home_tree_menu_disable)
            ls_menu_disable_text = [i.text for i in ls_menu_disable]

            list_actual2 = [ls_menu_enable_text, ls_menu_disable_text]
            list_expected2 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE'],
                              ['QOS', 'SECURITY', 'ADVANCED']]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Check list tree menu Enable, list tree menu disable. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check list tree menu Enable, list tree menu disable. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            # Click Network
            goto_menu(driver, network_tab, 0)
            network_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click WL
            goto_menu(driver, wireless_tab, 0)
            wireless_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click MS
            goto_menu(driver, media_share_tab, 0)
            media_share_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)

            list_actual3 = [network_submenu, wireless_submenu, media_share_submenu]
            list_expected3 = [['Operation Mode'], ['Primary Network', 'Repeater Setting', 'WPS'],
                              ['USB', 'Server Setting']]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3, 4, 5. Check Sub menu of NETWORK, WIRELESS, MS. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4, 5. Check Sub menu of NETWORK, WIRELESS, MS. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3, 4, 5. Assertion wong')

        try:
            # CLick system button
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()

            time.sleep(1)
            sys_button_text = [i.text for i in driver.find_elements_by_css_selector(ele_sys_list_button)]

            list_actual6 = sorted(sys_button_text)
            list_expected6 = sorted(['Language', 'Firmware Update', 'Change Password', 'Backup/Restore',
                              'Restart/Factory Reset', 'Power Saving Mode', 'LED Mode', 'Date/Time', 'Wizard'])
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Check list button in System button. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check list button in System button. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_38_NETWORK_Operation_Mode_Verify_of_Network_operation(self):
        self.key = 'NETWORK_38'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        # ===========================================================

        try:
            grand_login(driver)
            time.sleep(1)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Login. Check Home page is displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Login. Check Home page is displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            # Check Current Operation mode
            mode_cards = driver.find_elements_by_css_selector(ele_operation_mode_card)
            for m in mode_cards:
                if m.find_element_by_css_selector(input).is_selected():
                    get_mode_name = m.find_element_by_css_selector('h3').text
                    break


            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/network/qmode'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            check_api = [
                res.get('qmode') == 'extender',
                res.get('operation') == 'mesh slave'
            ]

            list_actual2 = [get_mode_name, check_api]
            list_expected2 = ['Repeater Mode', [return_true] * 2]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Check current operation Mode. '
                f'Check API /network/qmode. qmode is extender, operation is mesh salve. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check current operation Mode. '
                f'Check API /network/qmode. qmode is extender, operation is mesh salve. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            mode_cards = driver.find_elements_by_css_selector(ele_operation_mode_card)
            # Router mode
            list_card_info = list()
            for m in mode_cards:
                mode_name = m.find_element_by_css_selector('h3').text
                mesh_icon = len(m.find_elements_by_css_selector(ele_mesh_mode_icon)) == 1
                check_active = m.find_element_by_css_selector(input).is_selected()
                mode_desc = m.find_element_by_css_selector(ele_description_text).text
                _tmp_dict = {"name": mode_name,
                             "meshIcon": mesh_icon,
                             "active": check_active,
                             "description": mode_desc}
                list_card_info.append(_tmp_dict)

            expected_router_mode = {"name": "Router Mode",
                                    "meshIcon": True,
                                    "active": False,
                                    "description": exp_router_mode_description}
            expected_bridge_mode = {"name": "Bridge Mode",
                                    "meshIcon": False,
                                    "active": False,
                                    "description": exp_bridge_mode_description}
            expected_repeater_mode = {"name": "Repeater Mode",
                                      "meshIcon": True,
                                      "active": True,
                                      "description": exp_repeater_mode_description}
            expected_access_point_mode = {"name": "AP Mode",
                                          "meshIcon": True,
                                          "active": False,
                                          "description": exp_access_point_mode_description}
            list_actual3 = list_card_info
            list_expected3 = [expected_router_mode, expected_bridge_mode,
                              expected_repeater_mode, expected_access_point_mode]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check Card information of Router mode, Bridge mode, Repeater Mode, AP mode:'
                f'name, meshIcon, active, description. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Card information of Router mode, Bridge mode, Repeater Mode, AP mode. '
                f'name, meshIcon, active, description. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong')

        try:
            # Select Router mode
            mode_cards = driver.find_elements_by_css_selector(ele_operation_mode_card)
            for m in mode_cards:
                if m.find_element_by_css_selector('h3').text == 'Router Mode':
                    m.find_element_by_css_selector(ele_select_router_mode).click()
                    time.sleep(1)
                    apply_router_mode = driver.find_element_by_css_selector(apply).is_enabled()
                    time.sleep(0.5)
                    break

            list_actual4 = [apply_router_mode]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Select Router mode. Check Apply button enabled. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Select Router mode. Check Apply button enabled. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong')

        try:
            mode_cards = driver.find_elements_by_css_selector(ele_operation_mode_card)
            for m in mode_cards:
                if m.find_element_by_css_selector('h3').text == 'Bridge Mode':
                    m.find_element_by_css_selector(ele_select_bridge_mode).click()
                    time.sleep(1)
                    apply_bridge_mode = driver.find_element_by_css_selector(apply).is_enabled()
                    time.sleep(0.5)
                    break

            list_actual5 = [apply_bridge_mode]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Select Bridge mode. Check Apply button enabled. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Select Bridge mode. Check Apply button enabled. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong')

        try:
            mode_cards = driver.find_elements_by_css_selector(ele_operation_mode_card)
            for m in mode_cards:
                if m.find_element_by_css_selector('h3').text == 'Access Point Mode':
                    m.find_element_by_css_selector(ele_select_ap_mode).click()
                    time.sleep(0.5)
                    apply_ap_mode = driver.find_element_by_css_selector(apply).is_enabled()
                    time.sleep(0.5)
                    break

            list_actual6 = [apply_ap_mode]
            list_expected6 = [return_true]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Select Access Point mode. Check Apply button enabled. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Select Access Point mode. Check Apply button enabled. '
                f'Actual: {str(list_actual6)}. '
                f'Expected: {str(list_expected6)}')
            list_step_fail.append('6. Assertion wong')

        try:
            mode_cards = driver.find_elements_by_css_selector(ele_operation_mode_card)
            for m in mode_cards:
                if m.find_element_by_css_selector('h3').text == 'Repeater Mode':
                    m.find_element_by_css_selector(ele_select_repeater_mode).click()
                    time.sleep(1)
                    apply_repeater_mode = driver.find_element_by_css_selector(apply).is_enabled()
                    apply_repeater_mode_text = driver.find_element_by_css_selector(apply).text
                    time.sleep(0.5)
                    break

            list_actual7 = [apply_repeater_mode, apply_repeater_mode_text]
            list_expected7 = [return_true, 'Next']
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Select Repeater mode. Check Apply button enabled. '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Select Repeater mode. Check Apply button enabled. '
                f'Actual: {str(list_actual7)}. '
                f'Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('7. Assertion wong')
        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
