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
            os.system('netsh wlan delete profile name=*')
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
            # _check_apply = btn_apply.is_displayed()
            if btn_apply.is_displayed():
                btn_apply.click()
                time.sleep(0.5)
                # Click OK
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(5)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(5)
                wait_ethernet_available()
            wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)
            _check_type = driver.find_element_by_css_selector('[name=connectionType]').text
            list_actual = [_check_type]
            list_expected = ['Dynamic IP']
            check = assert_list(list_actual, list_expected)

            step_1_2_name = "1,2. Goto Network>Internet: Change values of Internet Settings: Dynamic IP. "
            list_check_in_step_1_2 = ["Change values of Internet Settings success"]
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
            # wait_ethernet_available()
            # Login
            grand_login(driver)
            # time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            # Get Wan IP address
            # wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
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
            step_3_name = "3. Check information changed: Dynamic IP. "
            list_check_in_step_3 = [
                "Check WAN information of Dynamic show same as api api/v1/network/wan/0"
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
                wait_ethernet_available()
            # _check_apply = internet_setting.find_element_by_css_selector(apply).is_displayed()
            # list_actual4 = [_check_apply]
            # list_expected4 = [return_true]
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, network_tab, network_internet_tab)
            wait_popup_disappear(driver, dialog_loading)
            _check_type = driver.find_element_by_css_selector('[name=connectionType]').text
            list_actual4 = [_check_type]
            list_expected4 = ['Static IP']
            step_4_name = "4. Goto Network>Internet: Change values of Internet Settings: Static IP. "
            list_check_in_step_4 = ["Change values of Internet Settings to 'Static IP' success"]
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
            wait_ethernet_available()
            # Login
            grand_login(driver)
            time.sleep(1)

            # Get Wan IP address
            wan_ip = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
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

            list_actual5 = [_actual]
            list_expected5 = [_expected]
            step_5_name = "5. Check information changed: Static IP. "
            list_check_in_step_5 = [
                 "Check WAN information of Static show same as api api/v1/network/wan/0"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
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
            step_1_2_3_name = "1,2,3. Delete DNS server info: Check text This field is required display. "
            list_check_in_step_1_2_3 = ["Warning message 'This field is required' appear"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
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
            step_4_5_name = "4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. "
            list_check_in_step_4_5 = ["Network internet settings page is appear"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
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
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
                # Click OK
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            step_6_name = "6. Apply and Wait for reboot"
            list_check_in_step_6 = ["Apply and Wait for reboot success"]
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=[True],
                    list_expected=[return_true]
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=[False],
                    list_expected=[return_true]
                )
            )
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
            step_7_name = "7. Check Information of WAN IP. "
            list_check_in_step_7 = [
                "Information of WAN correct",
            ]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append(
                '7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)

            list_actual8 = [check_ping]
            list_expected8 = [return_true]
            step_8_name = "8. Ping to Google. "
            list_check_in_step_8 = ["Ping to Google success"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
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
        factory_dut()
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
            step_1_2_3_name = "1,2,3. Delete DNS server info: Check text This field is required. "
            list_check_in_step_1_2_3 = ["Warning message: This field is required appear"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_4_5_name = "4,5. Disbaled DNS. Apply>Cancel: Check Page NW kept. "
            list_check_in_step_4_5 = ["Page network settings is appear"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_6_name = "6. Apply and Wait for reboot"
            list_check_in_step_6 = ["Apply and Wait for reboot success"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            list_step_fail.append(
                '6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            # Login
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            # Click icons Internet connection
            driver.find_element_by_css_selector(home_img_connection).click()
            wait_popup_disappear(driver, dialog_loading)

            primary = driver.find_element_by_css_selector('.card')
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
            step_7_name = "7. Check Information of WAN IP. "
            list_check_in_step_7 = ["Information of WAN is correct"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            list_step_fail.append(
                '7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            # Ping to google
            check_ping = ping_to_url(URL_PING_CHECK)
            time.sleep(4)
            list_actual = [check_ping]
            list_expected = [return_true]
            step_8_name = "8. Ping to Google. "
            list_check_in_step_8 = ["Ping to Google success"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_1_2_name = "1, 2. Login and Check title of Network Internet. "
            list_check_in_step_1_2 = ["Network Internet wrap is correct"]
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
            step_3_name = "3. Enable Dual WAN then click Apply. Check Default Dual WAN enabled, "
            list_check_in_step_3 = [
                "Default dual wan is selected",
                f"Default primary wan is: {list_expected3[1]}",
                f"List options primary is: {list_expected3[2]}",
                f"Default second wan is: {list_expected3[3]}",
                f"List options secondary is: {list_expected3[4]}",
                f"Default dual wan type is: {list_expected3[5]}",
                f"List options dual wan type is: {list_expected3[6]}"
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
            step_4_name = "4 Disable Dual WAN then click Apply. Check Dual WAN disabled. "
            list_check_in_step_4 = ["Dual WAN disabled"]
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
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
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
            step_1_2_name = "1, 2. Login and Check title of Network Internet. "
            list_check_in_step_1_2 = [f"Network wrap title is: {list_expected[0]}"]
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

            exp_secondary_1 = 'USB Broadband'
            exp_secondary_2 = 'Ethernet'
            exp_secondary_3 = 'Ethernet'
            list_actual = [check_secondary_1, check_secondary_2, check_secondary_3]
            list_expected = [exp_secondary_1, exp_secondary_2, exp_secondary_3]
            step_3_4_5_6_name = "3, 4, 5, 6. Enabled Dual WAN. Verify relate between Primary to Secondary WAN. "
            list_check_in_step_3_4_5_6 = [
                f"When set primary wan is 'Ethernet', Secondary wan is selected as '{list_expected[0]}'",
                f"When set primary wan is 'USB Broadband', Secondary wan is selected as '{list_expected[1]}'",
                f"When set primary wan is 'Android Tethering', secondary wan is selected as '{list_expected[2]}'"
            ]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_6_name,
                    list_check_in_step=list_check_in_step_3_4_5_6,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_6_name,
                    list_check_in_step=list_check_in_step_3_4_5_6,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_1_2_name = "1, 2. Login and Check title of Network Internet. "
            list_check_in_step_1_2 = [f"Network wrap title is: {list_expected[0]}"]
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

            exp_primary_1 = 'USB Broadband'
            exp_primary_2 = 'Ethernet'
            exp_primary_3 = 'Ethernet'
            list_actual = [check_primary_1, check_primary_2, check_primary_3]
            list_expected = [exp_primary_1, exp_primary_2, exp_primary_3]
            step_3_4_5_6_name = "3, 4, 5, 6. Enabled Dual WAN. Verify relate between Primary to Secondary WAN. "
            list_check_in_step_3_4_5_6 = [
                f"When set secondary wan is 'Ethernet', primary wan is selected as '{list_expected[0]}'",
                f"When set secondary wan is 'USB Broadband', primary wan is selected as '{list_expected[1]}'",
                f"When set secondary wan is 'Android Tethering', primary wan is selected as '{list_expected[2]}'"
            ]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_6_name,
                    list_check_in_step=list_check_in_step_3_4_5_6,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_6_name,
                    list_check_in_step=list_check_in_step_3_4_5_6,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '3, 4, 5, 6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_17_NETWORK_Check_operation_of_changing_Gateway_address(self):
        self.key = 'NETWORK_17'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        IP1 = '192.168.10.1'
        IP1_VALUE = IP1.split('.')

        IP2 = '172.16.1.1'
        IP2_VALUE = IP2.split('.')

        IP3 = '10.0.1.1'
        IP3_VALUE = IP3.split('.')
        factory_dut()
        # ===========================================================
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
                        if o.text == IP1_VALUE[0]:
                            o.click()

                    # Change IP range to 192.168.10.1
                    ip_address_range = driver.find_elements_by_css_selector(ele_ip_address_range_input)
                    for i in range(2):
                        ip_address_range[0].clear()
                        ip_address_range[0].send_keys(IP1_VALUE[2])
                    for i in range(2):
                        ip_address_range[1].clear()
                        ip_address_range[1].send_keys(IP1_VALUE[3])
                    break

            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    start_ip_value = f.text
                    end_val = f.find_element_by_css_selector(input).get_attribute('value')
                    start_ip_value = start_ip_value + end_val
                    start_ip_value = start_ip_value.replace(' ', '')
                if l.text == 'End IP Address':
                    end_ip_value = f.text
                    end_val = f.find_element_by_css_selector(input).get_attribute('value')
                    end_ip_value = end_ip_value + end_val
                    end_ip_value = end_ip_value.replace(' ', '')
                    break

            list_actual2 = [start_ip_value.split('.')[:3], end_ip_value.split('.')[:3]]
            list_expected2 = [IP1_VALUE[:3]]*2
            step_1_2_1_name = f"1, 2._1 Set: {IP1}. Login. Change IP Address. Check Start IP and End IP according to bandwidth. "
            list_check_in_step_1_2_1 = [
                f"Start IP is {list_expected2[0]}",
                f"End IP is {list_expected2[0]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_1_name,
                    list_check_in_step=list_check_in_step_1_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_1_name,
                    list_check_in_step=list_check_in_step_1_2_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('1, 2._1 Assertion wong.')

        try:
            # Click Apply
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(2)
            # Get confirm message
            check_confirm_message = driver.find_element_by_css_selector(confirm_dialog_msg).text
            exp_confirm_message = f'In order to complete the setup of the system must be restart. After restarting, move to new LAN IP Address ({IP1}). Continue?'

            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(120)
            wait_ping(IP1)
            wait_ethernet_available()
            time.sleep(5)

            list_actual3 = [check_confirm_message]
            list_expected3 = [exp_confirm_message]
            step_3_1_name = "3._1 Click Apply. Check Confirm message. "
            list_check_in_step_3_1 = [f"Confirm message is '{exp_confirm_message}'"]
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
            list_step_fail.append('3._1 Assertion wong.')

        try:

            # Check connect with external communication
            check_google = check_connect_to_google()

            check_youtube = check_connect_to_youtube()

            # Check in command line
            check_ip_in_cmd = get_url_ipconfig(ipconfig_field='Default Gateway')
            # Check connect
            URL_NEW = 'http://' + check_ip_in_cmd
            USER_ = get_config('ACCOUNT', 'user')
            PW_ = get_config('ACCOUNT', 'password')
            login(driver, URL_NEW, USER_, PW_)
            check_login_new_url = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual4 = [check_ip_in_cmd, check_login_new_url, check_google, check_youtube]
            list_expected4 = [IP1] + [return_true] * 3
            step_4_1_name = "4._1 Check IP in cmd, Check login by New IP Address, Check goto GOOGLE and YOUTUBE. "
            list_check_in_step_4_1 = [
                f"IP is: {list_expected4[0]}",
                "Login in to new URL success",
                "Goto google success",
                "Goto youtube success"
            ]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_1_name,
                    list_check_in_step=list_check_in_step_4_1,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_1_name,
                    list_check_in_step=list_check_in_step_4_1,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('4._1 Assertion wong.')

        # ===========================================================
        try:
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
                        if o.text == IP2_VALUE[0]:
                            o.click()

                    # Change IP range to 176.16.1.1
                    ip_address_range = driver.find_elements_by_css_selector(ele_ip_address_range_input)
                    for i in range(2):
                        ip_address_range[0].clear()
                        ip_address_range[0].send_keys(IP2_VALUE[2])
                    for i in range(2):
                        ip_address_range[1].clear()
                        ip_address_range[1].send_keys(IP2_VALUE[3])
                    break

            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    start_ip_value = f.text
                    end_val = f.find_element_by_css_selector(input).get_attribute('value')
                    start_ip_value = start_ip_value + end_val
                    start_ip_value = start_ip_value.replace(' ', '')
                if l.text == 'End IP Address':
                    end_ip_value = f.text
                    end_val = f.find_element_by_css_selector(input).get_attribute('value')
                    end_ip_value = end_ip_value + end_val
                    end_ip_value = end_ip_value.replace(' ', '')
                    break

            list_actual5 = [start_ip_value.split('.')[:3], end_ip_value.split('.')[:3]]
            list_expected5 = [IP2_VALUE[:3]] * 2
            step_1_2_2_name = f"1, 2._2 Set: {IP2}. Login. Change IP Address. Check Start IP and End IP according to bandwidth. "
            list_check_in_step_1_2_2 = [
                f"Start IP is {list_expected5[0]}",
                f"End IP is {list_expected5[0]}"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_2_name,
                    list_check_in_step=list_check_in_step_1_2_2,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_2_name,
                    list_check_in_step=list_check_in_step_1_2_2,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('1, 2._2 Assertion wong.')


        try:
            # Click Apply
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(2)
            # Get confirm message
            check_confirm_message = driver.find_element_by_css_selector(confirm_dialog_msg).text
            exp_confirm_message = f'In order to complete the setup of the system must be restart. After restarting, move to new LAN IP Address ({IP2}). Continue?'

            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(120)
            wait_ethernet_available()
            time.sleep(5)

            list_actual6 = [check_confirm_message]
            list_expected6 = [exp_confirm_message]
            step_3_2_name = "3._2 Click Apply. Check Confirm message. "
            list_check_in_step_3_2 = [f"Confirm message is: {exp_confirm_message}"]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_2_name,
                    list_check_in_step=list_check_in_step_3_2,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_2_name,
                    list_check_in_step=list_check_in_step_3_2,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('3._2 Assertion wong.')

        try:

            # Check connect with external communication
            check_google = check_connect_to_google()

            check_youtube = check_connect_to_youtube()

            # Check in command line
            check_ip_in_cmd = get_url_ipconfig(ipconfig_field='Default Gateway')
            # Check connect
            URL_NEW_2 = 'http://' + IP2
            USER_ = get_config('ACCOUNT', 'user')
            PW_ = get_config('ACCOUNT', 'password')
            login(driver, URL_NEW_2, USER_, PW_)
            check_login_new_url = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual7 = [check_ip_in_cmd, check_login_new_url, check_google, check_youtube]
            list_expected7 = [IP2] + [return_true] * 3
            step_4_2_name = "4._2 Check IP in cmd, Check login by New IP Address, Check goto GOOGLE and YOUTUBE. "
            list_check_in_step_4_2 = [
                f"IP is: {list_expected7[0]}",
                "Login in to new URL success",
                "Goto google success",
                "Goto youtube success"
            ]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_2_name,
                    list_check_in_step=list_check_in_step_4_2,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_2_name,
                    list_check_in_step=list_check_in_step_4_2,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('4._2 Assertion wong.')

        # ===========================================================
        try:
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
                        if o.text == IP3_VALUE[0]:
                            o.click()

                    # Change IP range to 10.0.1.1
                    ip_address_range = driver.find_elements_by_css_selector(ele_ip_address_range_input)
                    for i in range(2):
                        ip_address_range[0].clear()
                        ip_address_range[0].send_keys(IP3_VALUE[2])
                    for i in range(2):
                        ip_address_range[1].clear()
                        ip_address_range[1].send_keys(IP3_VALUE[3])
                    break

            for l, f in zip(lan_label, lan_fields):
                if l.text == 'Start IP Address':
                    start_ip_value = f.text
                    end_val = f.find_element_by_css_selector(input).get_attribute('value')
                    start_ip_value = start_ip_value + end_val
                    start_ip_value = start_ip_value.replace(' ', '')
                if l.text == 'End IP Address':
                    end_ip_value = f.text
                    end_val = f.find_element_by_css_selector(input).get_attribute('value')
                    end_ip_value = end_ip_value + end_val
                    end_ip_value = end_ip_value.replace(' ', '')
                    break

            list_actual8 = [start_ip_value.split('.')[:3], end_ip_value.split('.')[:3]]
            list_expected8 = [IP3_VALUE[:3]] * 2
            step_1_2_3_name = f"1, 2._3 Set: {IP3}. Login. Change IP Address. Check Start IP and End IP according to bandwidth. "
            list_check_in_step_1_2_3 = [
                f"Start IP is {list_expected2[0]}",
                f"End IP is {list_expected2[0]}"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('1, 2._3 Assertion wong.')

        try:
            # Click Apply
            lan_block = driver.find_element_by_css_selector(network_lan_card)
            lan_block.find_element_by_css_selector(submit_btn).click()
            time.sleep(2)
            # Get confirm message
            check_confirm_message = driver.find_element_by_css_selector(confirm_dialog_msg).text
            exp_confirm_message = f'In order to complete the setup of the system must be restart. After restarting, move to new LAN IP Address ({IP3}). Continue?'

            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(120)
            wait_ping(IP3)
            wait_ethernet_available()
            time.sleep(5)

            list_actual9 = [check_confirm_message]
            list_expected9 = [exp_confirm_message]
            step_3_3_name = "3._3 Click Apply. Check Confirm message. "
            list_check_in_step_3_3 = [f"Confirm message is: {exp_confirm_message}"]
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_3_name,
                    list_check_in_step=list_check_in_step_3_3,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_3_name,
                    list_check_in_step=list_check_in_step_3_3,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            list_step_fail.append('3._3 Assertion wong.')

        try:
            # Check connect with external communication
            check_google = check_connect_to_google()

            check_youtube = check_connect_to_youtube()

            # Check in command line
            check_ip_in_cmd = get_url_ipconfig(ipconfig_field='Default Gateway')
            # Check connect
            URL_NEW_3 = 'http://' + IP3
            USER_ = get_config('ACCOUNT', 'user')
            PW_ = get_config('ACCOUNT', 'password')
            login(driver, URL_NEW_3, USER_, PW_)

            check_login_new_url = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual10 = [check_ip_in_cmd, check_login_new_url, check_google, check_youtube]
            list_expected10 = [IP3] + [return_true] * 3
            step_4_3_name = "4._3 Check IP in cmd, Check login by New IP Address, Check goto GOOGLE and YOUTUBE. "
            list_check_in_step_4_3 = [
                f"IP is: {list_expected10[0]}",
                "Login in to new URL success",
                "Goto google success",
                "Goto youtube success"
            ]
            check = assert_list(list_actual10, list_expected10)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_3_name,
                    list_check_in_step=list_check_in_step_4_3,
                    list_actual=list_actual10,
                    list_expected=list_expected10
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_3_name,
                    list_check_in_step=list_check_in_step_4_3,
                    list_actual=list_actual10,
                    list_expected=list_expected10
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4._3 Assertion wong.')
        # ===========================================================
        factory_dut()
        # ===========================================================
        self.assertListEqual(list_step_fail, [])
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
            step_1_name = "1. Check Subnet Mask value when Ip Address is class C. "
            list_check_in_step_1 = [f"Subnet mask is fixed: {exp_nw_subnet_type_c}"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected))
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
                            time.sleep(0.5)
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
            list_actual2 = check_subnet_b + [start_ip_16, end_ip_16]
            list_expected2 = exp_nw_subnet_type_b + [return_true, return_true]
            step_2_3_name = "2,3. Check Subnet Mask value when Ip Address is class B and verify en Start/End Ip <16 bits. "
            list_check_in_step_2_3 = [
                f"Subnet Mask is: {list_expected2[0]}",
                f"Subnet Mask is: {list_expected2[1]}",
                "Condition 'Start IP less than 16 bits' is correct",
                "Condition 'End IP less than 16 bits' is correct"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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

            list_actual4 = check_subnet_a + [start_ip_16, end_ip_16, start_ip_24, end_ip_24]
            list_expected4 = exp_nw_subnet_type_a + [return_true, return_true, return_true, return_true]
            step_4_5_6_name = "4,5,6. Check Subnet Mask value when Ip Address is class A " \
                              "and verify en Start/End Ip <16, 24 bits. "
            list_check_in_step_4_5_6 = [
                f"Subnet Mask is: {list_expected4[0]}",
                f"Subnet Mask is: {list_expected4[1]}",
                f"Subnet Mask is: {list_expected4[2]}",
                "Condition 'Start IP less than 16 bits' is correct",
                "Condition 'End IP less than 16 bits' is correct",
                "Condition 'Start IP less than 24 bits' is correct",
                "Condition 'End IP less than 24 bits' is correct"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_6_name,
                    list_check_in_step=list_check_in_step_4_5_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_6_name,
                    list_check_in_step=list_check_in_step_4_5_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
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
            step_1_name = "1. Login and Check title of Network > LAN. "
            list_check_in_step_1 = [f"Page wrap title is: {list_expected[0]}"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_2_name = "2. Change Start IP and End IP. Check apply successfully. "
            list_check_in_step_2 = [
                f"New start ip is: {list_expected2[0]}",
                f"New end ip is: {list_expected2[1]}"
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
            step_3_name = f"3. Command: ipconfig/release > ipconfig/renew > ipconfig/all: {ipv4_address} " \
                          f"- Check IPv4 between range Start IP and End IP. "
            list_check_in_step_3 = ["Condition 'IPv4 between range Start IP and End IP' is correct"]
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
            step_1_name = "1. Set start IP Address more than End IP Address: Check Error Message. "
            list_check_in_step_1 = [f"Error message is: {exp_error_msg_start_less_end}"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_2_name = "2. Set start IP Address, End IP Address Small: Check Error Message. "
            list_check_in_step_2= [f"Error message is: {exp_error_msg_start_end_small}"]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_3_name = "3. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message. "
            list_check_in_step_3 = [f"Error message is: {exp_error_msg_start_end_same_lan_ip}"]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
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
            step_4_name = "4. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message. "
            list_check_in_step_4 = [f"Error message is: {exp_error_msg_start_end_include_lan_ip}"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_24_NETWORK_Reserved_IP_Address_Add_a_rule(self):
        self.key = 'NETWORK_24'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        get_mac_address = get_value_from_ipconfig('Ethernet adapter Ethernet', 'Physical Address')
        correct_mac_address = get_mac_address.replace('-', ':')
        RESERVED_IP_ADDRESS = get_config('NETWORK', 'nw24_reserved_ip', input_data_path)
        try:
            grand_login(driver)
            time.sleep(1)
            # Network Lan Tab
            goto_menu(driver, network_tab, network_lan_tab)

            wait_popup_disappear(driver, dialog_loading)
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)

            nw_add_reserved_ip(driver, correct_mac_address, RESERVED_IP_ADDRESS)

            reserved_ip_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.2)
            reserved_ip_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [correct_mac_address, RESERVED_IP_ADDRESS]
            step_1_2_3_name = "1, 2, 3. Login. Goto LAN. Registering a reserved IP. Check Registered successfully. "
            list_check_in_step_1_2_3 = [
                f"Mac address is: {list_expected1[0]}",
                f"Reserved ip address is: {list_actual1[1]}"
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            list_step_fail.append('1, 2, 3. Assertion wong.')

        try:
            # Release
            subprocess.check_output('ipconfig/release', shell=True)
            time.sleep(2)
            # Renew
            subprocess.check_output('ipconfig/renew', shell=True)
            time.sleep(15)

            get_current_ipv4 = get_value_from_ipconfig('Ethernet adapter Ethernet', 'IPv4 Address')

            ipv4_address = get_current_ipv4.split('(Preferred)')[0]

            list_actual3 = [ipv4_address]
            list_expected3 = [RESERVED_IP_ADDRESS]
            step_4_name = "4. Command: ipconfig/release > ipconfig/renew > ipconfig/all. "
            list_check_in_step_4 = [f"Reserved ip address is: {list_expected3[0]}"]
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
            list_step_fail.append('4. Assertion wong.')

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
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [MAC_2, IP_2]
            step_1_2_name = "1, 2. Check Add Reserved IP successfully. "
            list_check_in_step_1_2 = [
                f"Mac address is: {list_expected1[0]}",
                f"IP address is: {list_expected1[1]}"
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
            step_3_name = "3. Check Add a new Reserved IP same IP address: Check error msg. "
            list_check_in_step_3 = [f"Check error message is: {exp_ip_address_exists}"]
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
            step_4_name = "4. Check Add a new Reserved IP same MAC address: Check error msg."
            list_check_in_step_4 = [f"Check error msg is {exp_mac_address_exists}"]
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
            step_5_name = "5. Check Error msg displayed, Check Mac same as input, Check IP same as input. "
            list_check_in_step_5 = [
                "Check Error msg is appear",
                f"Check MAC address is: {list_expected5[1]}",
                f"Check IP address is: {list_expected5[2]}"
            ]
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
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
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
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [MAC_2, IP_2]
            step_1_2_name = "1, 2. Check Add Reserved IP successfully. "
            list_check_in_step_1_2 = [
                f"Check MAC address is: {list_expected1[0]}",
                f"Check IP address is: {list_expected1[1]}"
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
            list_step_fail.append('1. Assertion wong.')

        try:
            # Add 32 items
            for i in range(12, 43):
                mac = f'12:12:12:12:12:{str(i+1)}'
                ip = f'192.168.1.{str(i)}'
                nw_add_reserved_ip(driver, mac, ip)
                reserved_ip_block.find_element_by_css_selector(btn_save).click()
                time.sleep(0.2)
            time.sleep(1)
            check_add_disabled = reserved_ip_block.find_element_by_css_selector(add_class).get_attribute('disabled') == 'true'

            reserved_ip_block.find_element_by_css_selector(add_class).click()
            check_add_to_edit = len(reserved_ip_block.find_elements_by_css_selector(edit_mode)) == 0

            list_actual1 = [check_add_disabled, check_add_to_edit]
            list_expected1 = [return_true]*2
            step_3_name = "3. Add 32 reserved IP. Check ADD button disabled " \
                          "and Click add -> Check edit form not display. "
            list_check_in_step_3 = [
                "Check Add button is disabled",
                "Check After click add, edit form is not appear"
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

    def test_27_NETWORK_Verify_update_Reserved_IP_address_follow_changing_Lan_IP(self):
        self.key = 'NETWORK_27'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        factory_dut()
        # ===============================================
        URL_PING_CHECK = '172.16.1.1'
        URL_B = 'http://172.16.1.1'
        EXPECTED_B_IP_ADDR = '172.16.1.10'
        MAC_2 = get_config('NETWORK', 'nw27_mac2', input_data_path)
        IP_2 = get_config('NETWORK', 'nw27_ip2', input_data_path)

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
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual1 = [mac_address, ip_addr]
            list_expected1 = [MAC_2, IP_2]
            step_1_2_name = "1, 2. Check Add Reserved IP successfully. "
            list_check_in_step_1_2 = [
                f"Check MAC address is: '{list_expected1[0]}'",
                f"Check IP address is: '{list_expected1[1]}'"
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
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            # wait_popup_disappear(driver, dialog_loading)
            # wait_popup_disappear(driver, dialog_loading)
            time.sleep(100)
            # wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()
            # wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()
            # wait_popup_disappear(driver, dialog_loading)
            # wait_DUT_activated(URL_PING_CHECK)
            time.sleep(10)
            # wait_ping(URL_B)
            # driver.get(URL_B)
            save_config(config_path, 'URL', 'url', URL_B)
            time.sleep(1)
            wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, network_tab, network_lan_tab)
            wait_ethernet_available()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)
            wait_popup_disappear(driver, dialog_loading)
            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual = [ip_addr]
            list_expected = [EXPECTED_B_IP_ADDR]
            step_2_3_name = "2,3. Change LAN IP to 172.16.1.1: Check update successfully"
            list_check_in_step_2_3 = [f"Check IP address is: {EXPECTED_B_IP_ADDR}"]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2,3. Assertion wong.')
        # ===============================================
        factory_dut()

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
            step_1_name = "1. Check Network LAN title display. "
            list_check_in_step_1 = [f"Check network wrap title is: {list_expected1[0]}"]
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
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
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
            step_2_name = "2. Change information. Check result between web and api: " \
                          "Ip address, Subnet, DHCP, Start IP, End IP, Lease time convert to second."
            list_check_in_step_2 = [
                f"Check new ip address is: {list_expected2[0]}",
                f"Check new subnet address is: {list_expected2[1]}",
                f"Check new dhcp server is: {list_expected2[2]}",
                f"Check new start ip address is: {list_expected2[3]}",
                f"Check new end ip address is: {list_expected2[4]}",
                f"Check new lease time (second) is: {list_expected2[5]}",
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
            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)
            nw_add_reserved_ip(driver, IP_ADDRESS_MAC, IP_ADDRESS_MORE_END_IP)

            time.sleep(0.2)
            # Check Error message display and button Save Dimmed
            error_msg_display = len(reserved_ip_block.find_elements_by_css_selector(custom_error_cls)) > 0
            # button_save_dimmed = not reserved_ip_block.find_element_by_css_selector(btn_save).is_enabled()

            list_actual3 = [error_msg_display]
            list_expected3 = [return_true]
            step_3_name = "3. Change IP address out of range. Check Error message display. "
            list_check_in_step_3 = ["Check Error message is appear"]
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
            # Click Cancel
            reserved_ip_block.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)

            reserved_ip_block = driver.find_element_by_css_selector(network_reserved_ip_card)
            nw_add_reserved_ip(driver, IP_ADDRESS_MAC, IP_ADDRESS_LESS_END_IP)
            reserved_ip_block.find_element_by_css_selector(btn_save).click()

            time.sleep(0.2)
            reserved_ip_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            # Get info of first row
            first_row = reserved_ip_block.find_elements_by_css_selector(rows)[0]
            mac_address = first_row.find_element_by_css_selector(mac_desc_cls).text
            mac_address = mac_address.splitlines()[1]
            ip_addr = first_row.find_element_by_css_selector(ip_address_cls).text

            list_actual4 = [mac_address, ip_addr]
            list_expected4 = [IP_ADDRESS_MAC, IP_ADDRESS_LESS_END_IP]
            step_4_name = "4. Add a reserved IP in range. Check Add successfully. "
            list_check_in_step_4 = [
                f"Check MAC address is: {list_expected4[0]}",
                f"Check IP address is: {list_expected4[0]}",
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
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)

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
            step_5_name = "5. Change End IP address less than IP of Reserved IP address. "
            list_check_in_step_5 = [f"Check IP address is: {list_expected5[0]}"]
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
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    def test_32_NETWORK_Verify_operation_of_Router_Mode(self):
        self.key = 'NETWORK_32'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        UPPER_5G_NAME = get_config('REPEATER', 'repeater_name_5g', input_data_path)
        UPPER_5G_PW = get_config('REPEATER', 'repeater_pw_5g', input_data_path)
        # ===========================================================
        try:
            grand_login(driver)
            time.sleep(1)

            check_google = check_connect_to_google()

            list_actual1 = [check_google]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check external communication is successfully. "
            list_check_in_step_1 = ["Connect to google success"]
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
            disconnect_or_connect_wan(disconnected=True)
            time.sleep(5)
            goto_menu(driver, network_tab, network_operationmode_tab)
            time.sleep(2)
            connect_repeater_mode(driver, UPPER_5G_NAME, UPPER_5G_PW)
            time.sleep(5)
            # Login
            driver.refresh()
            time.sleep(5)
            grand_login(driver)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            check_repeater_active = driver.find_element_by_css_selector(ele_repeater_mode_input).is_selected()

            list_actual2 = [check_repeater_active]
            list_expected2 = [return_true]
            step_2_name = "2. Disconnect WAN. Change to Repeater mode. Login again. Check Repeater Mode activated."
            list_check_in_step_2 = ["Check Repeater Mode is activated"]
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
            list_step_fail.append('2. Assertion wong')

        try:
            # Select Router mode
            driver.find_element_by_css_selector(ele_select_router_mode).click()
            # Apply
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, lg_page)
            save_config(config_path, 'URL', 'url', 'http://dearmyrouter.net')
            time.sleep(5)
            grand_login(driver)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            check_router_active = driver.find_element_by_css_selector(ele_router_mode_input).is_selected()

            list_actual3 = [check_router_active]
            list_expected3 = [return_true]
            step_3_name = "3. Select Router mode. Login again. Check Router mode activated."
            list_check_in_step_3 = ["Check Router mode is activated"]
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
            list_step_fail.append('3. Assertion wong')

        try:
            disconnect_or_connect_wan(disconnected=False)
            time.sleep(5)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            check_ip_assigned = driver.find_element_by_css_selector(home_conection_img_wan_ip).text != '0.0.0.0'

            list_actual4 = [check_ip_assigned]
            list_expected4 = [return_true]
            step_4_name = "4. Enabled WAN. Login. Check IP assigned (difference 0.0.0.0). "
            list_check_in_step_4 = [
                "Check Condition 'IP assigned difference 0.0.0.0' is correct"
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
            list_step_fail.append('4. Assertion wong')

        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            check_google = check_connect_to_google()
            time.sleep(2)

            list_actual5 = [check_google]
            list_expected5 = [return_true]
            step_5_name = "5. Login. Check external communication with Google is successfully."
            list_check_in_step_5 = ["Check connect google success"]
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
            list_step_fail.append('5. Assertion wong')

        try:
            goto_system(driver, sys_reset)
            time.sleep(0.5)
            apply_btn = driver.find_element_by_css_selector(apply)
            if apply_btn.text == 'Restart':
                apply_btn.click()
                time.sleep(2)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            time.sleep(150)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, lg_page)
            wait_ethernet_available()

            check_google = check_connect_to_google()

            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            check_router_active = driver.find_element_by_css_selector(ele_router_mode_input).is_selected()

            URL_LOGIN = get_config('URL', 'url')
            _URL_API = URL_LOGIN + '/api/v1/network/qmode'
            _METHOD = 'GET'
            _BODY = ''
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _TOKEN = get_token(_USER, _PW)

            res = call_api(_URL_API, _METHOD, _BODY, _TOKEN)
            is_qmode_equal_router = res.get('qmode') == 'router'
            is_operation_equal_router = res.get('operation') == 'router'

            list_actual6 = [check_google, check_router_active, is_qmode_equal_router, is_operation_equal_router]
            list_expected6 = [return_true, return_true, return_true, return_true]
            step_6_name = "6. Restart DUT. Check access Google success. Check operation mode is Router mode." \
                         " Check API /network/qmode. qmode is router, operation is router."
            list_check_in_step_6 = [
                "Check Connect google success",
                "Check Router is activated",
                "Check Condition 'qmode is router' correct",
                "Check Condition 'operation is router' correct"]
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
            list_step_fail.append('6. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_33_NETWORK_Repeater_Verify_of_menu_tree(self):
        self.key = 'NETWORK_33'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        # ===========================================================

        try:
            # time.sleep(20)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            # Check Home screen displayed
            check_home = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            list_actual1 = [check_home]
            list_expected1 = [return_true]
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = ["Home page is appear"]
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
            ls_menu_enable = driver.find_elements_by_css_selector(ele_home_tree_menu_enable)
            ls_menu_enable_text = [i.text for i in ls_menu_enable]

            ls_menu_disable = driver.find_elements_by_css_selector(ele_home_tree_menu_disable)
            ls_menu_disable_text = [i.text for i in ls_menu_disable]

            list_actual2 = [ls_menu_enable_text, ls_menu_disable_text]
            list_expected2 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE'],
                              ['QOS', 'SECURITY', 'ADVANCED']]
            step_2_name = "2. Check list tree menu Enable, list tree menu disable."
            list_check_in_step_2 = [
                f"list tree menu Enable is: {list_expected2[0]}",
                f"list tree menu disable is: {list_expected2[1]}"
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
            list_step_fail.append('2. Assertion wong')

        try:
            # Click Network
            goto_menu(driver, network_tab, 0)
            time.sleep(1)
            network_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click WL
            goto_menu(driver, wireless_tab, 0)
            time.sleep(1)
            wireless_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click MS
            goto_menu(driver, media_share_tab, 0)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            media_share_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)

            list_actual3 = [network_submenu, wireless_submenu, media_share_submenu]
            list_expected3 = [['Operation Mode'], ['Primary Network', 'Repeater Setting', 'WPS'],
                              ['USB', 'Server Setting']]
            step_3_4_5_name = "3, 4, 5. Check Sub menu of NETWORK, WIRELESS, MS. "
            list_check_in_step_3_4_5 = [
                f"Check Sub menu of NETWORK is: {list_expected3[0]}",
                f"Check Sub menu of WIRELESS is: {list_expected3[1]}",
                f"Check Sub menu of MS is: {list_expected3[2]}"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_5_name,
                    list_check_in_step=list_check_in_step_3_4_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4, 5. Assertion wong')

        try:
            # CLick system button
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()

            time.sleep(1)
            sys_button_text = [i.text for i in driver.find_elements_by_css_selector(ele_sys_list_button)]

            list_actual6 = [' - '.join(sorted(sys_button_text))]
            list_expected6 = [' - '.join(sorted(['Language', 'Firmware Update', 'Change Password', 'Back Up/Restore',
                                     'Restart/Factory Reset', 'Power Saving Mode', 'LED Mode', 'Date/Time', 'Wizard']))]
            step_6_name = "6. Check list button in System button."
            list_check_in_step_6 = [
                f"List button in System is: {list_expected6[0]}"
            ]
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
            list_step_fail.append('6. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_36_NETWORK_Easy_Setup_Verification_of_upper_router_and_extender_connection_by_wireless_2g(self):
        self.key = 'NETWORK_36'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        # disconnect_or_connect_wan(disconnected=True)
        factory_dut()
        # ======================================================
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            time.sleep(1)
            wait_ethernet_available()
            login(driver)

            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            # Choose
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break

            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)
            wait_popup_disappear(driver, '.loading-wizard')
            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            wait_popup_disappear(driver, '.loading-wizard')
            time.sleep(1)
            list_column = [i.text for i in driver.find_elements_by_css_selector('thead .col')]

            list_actual1 = [title_repeater_setting_1, list_column]
            list_expected1 = ['Repeater Setting',
                              ['Network Name(SSID)', 'CH', 'RSSI', 'Security', 'MAC Address', 'Band']]
            step_1_2_name = "1, 2. Login. Next to Repeater Setting. "
            list_check_in_step_1_2 = [
                f"Check title page is: {list_expected1[0]}",
                f"Check list column is: {list_expected1[1]}"
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(5)
            wait_popup_disappear(driver, dialog_loading)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_MESH_PW).perform()
            time.sleep(1)

            # Get info
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
                    get_security = r.find_element_by_css_selector(security_page).text

            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            # Click Let go
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')

            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()

            check_home_page = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            check_google = check_connect_to_google()

            list_actual3 = [check_home_page, check_google]
            list_expected3 = [return_true] * 2
            step_3_4_name = "3, 4. Click Let go. Login again with Repeater. " \
                            "Check home page display. Check can connect to google. "
            list_check_in_step_3_4 = [
                "Check Home page is appear",
                "Check Connect to google success"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            # Check Network
            wireless_card = driver.find_element_by_css_selector(ele_wireless_card)
            labels = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values = wireless_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'Network Name(SSID)':
                    nw_name_value = v.text
                if l.text == 'Security':
                    nw_security = v.text
                    break
            time.sleep(2)
            list_actual6 = [nw_name_value, nw_security]
            list_expected6 = [REPEATER_MESH_NAME, get_security]
            step_6_name = "6. Check HOME wireless Network Name SSID. "
            list_check_in_step_6 = [
                f"Repeater mesh name is: {list_expected6[0]}",
                f"Security is: {list_expected6[1]}"
            ]
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
            list_step_fail.append('6. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            time.sleep(1)
            check_repeater_mode = driver.find_element_by_css_selector(ele_repeater_mode_input).is_selected()

            list_actual7 = [check_repeater_mode]
            list_expected7 = [return_true]
            check = assert_list(list_actual7, list_expected7)
            step_7_name = "7. Click Let go. Check Wan mode is Repeater Mode. Check connect to Google. "
            list_check_in_step_7 = ["Check Condition 'Check Wan mode is Repeater Mode' is correct"]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )

            list_step_fail.append('7. Assertion wong')

        try:
            wait_ethernet_available()
            goto_menu(driver, home_tab, 0)
            URL_wifi_2g = 'http://dearmyextender.net/api/v1/wifi/0/ssid/0'
            extender_MAC = api_change_wifi_setting(URL_wifi_2g, get_only_mac=True)

            interface_connect_disconnect('Ethernet', 'disable')
            wifi_connect = connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
            os.system('netsh wlan show interface mode=BSSID')

            interface_connect_disconnect('Ethernet', 'disable')
            connected_mac = get_current_wifi_MAC()
            print(connected_mac)
            if extender_MAC != connected_mac:
                os.system('netsh wlan delete profile name=*')
                wifi = connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
            connected_mac = get_current_wifi_MAC()

            ip_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google_2 = check_connect_to_google()

            list_actual8 = [wifi_connect, connected_mac, ip_assigned, check_google_2]
            list_expected8 = [REPEATER_MESH_NAME, extender_MAC, return_true, return_true]
            step_8_name = "8. Connect Wifi (Wifi name and MAC). Check IP assigned and can connect to google."
            list_check_in_step_8 = [
                f"Check Connect Wifi (Wifi name) is: {list_expected8[0]}",
                f"Check Connect Wifi (MAC) is: {list_expected8[1]}",
                "Check IP is assigned",
                "Check connect to google success"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('8. Assertion wong')
        # disconnect_or_connect_wan(disconnected=False)

        self.assertListEqual(list_step_fail, [])

    def test_37_NETWORK_Easy_Setup_Verification_of_upper_router_and_extender_connection_by_wireless_5g(self):
        self.key = 'NETWORK_37'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        # disconnect_or_connect_wan(disconnected=True)
        factory_dut()


        # ======================================================
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name_5g', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw_5g', input_data_path)

        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            time.sleep(1)
            login(driver)

            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            driver.find_element_by_css_selector(welcome_start_btn).click()
            wait_visible(driver, welcome_change_pw_fields)

            change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

            # A list contain values: Current Password, New Password, Retype new pw
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            # Choose
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break

            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)
            wait_popup_disappear(driver, '.loading-wizard')
            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            wait_popup_disappear(driver, '.loading-wizard')
            list_column = [i.text for i in driver.find_elements_by_css_selector('thead .col')]

            list_actual1 = [title_repeater_setting_1, list_column]
            list_expected1 = ['Repeater Setting',
                              ['Network Name(SSID)', 'CH', 'RSSI', 'Security', 'MAC Address', 'Band']]
            step_1_2_name = "1, 2. Login. Next to Repeater Setting. "
            list_check_in_step_1_2 = [
                f"Check Title page is: {list_expected1[0]}",
                f"Check List columns is: {list_expected1[1]}"
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_MESH_PW).perform()
            time.sleep(1)

            # Get info
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_MESH_NAME:
                    get_security = r.find_element_by_css_selector(security_page).text

            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            # Click Let go
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(5)
            # connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()

            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()
            check_home_page = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            check_google = check_connect_to_google()

            list_actual3 = [check_home_page, check_google]
            list_expected3 = [return_true] * 2
            step_3_4_name = "3, 4. Click Let go. Login again with Repeater. " \
                            "Check home page display. Check can connect to google."
            list_check_in_step_3_4 = [
                "Check Home page is appear",
                "Check Connect to google success"
            ]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            # Check Network
            wireless_card = driver.find_element_by_css_selector(ele_wireless_card)
            wireless_card.find_element_by_css_selector(ele_disconnect_device_tab).click()
            time.sleep(0.5)
            labels = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values = wireless_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'Network Name(SSID)':
                    nw_name_value = v.text
                if l.text == 'Security':
                    nw_security = v.text
                    break

            list_actual6 = [nw_name_value, nw_security]
            list_expected6 = [REPEATER_MESH_NAME, get_security]
            step_6_name = "6. Check HOME wireless Network Name SSID. "
            list_check_in_step_6 = [
                f"Check Repeater mesh name is: {list_expected6[0]}",
                f"Check Security is: {list_expected6[1]}",
            ]
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
            list_step_fail.append('6. Assertion wong')

        try:
            wait_ethernet_available()
            wait_popup_disappear(driver, dialog_loading)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            check_repeater_mode = driver.find_element_by_css_selector(ele_repeater_mode_input).is_selected()

            list_actual7 = [check_repeater_mode]
            list_expected7 = [return_true]
            step_7_name = "7. Click Let go. Check Wan mode is Repeater Mode. Check connect to Google. "
            list_check_in_step_7 = [
                "Check Repeater mode is selected"
            ]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )

            list_step_fail.append('7. Assertion wong')

        try:
            wait_ethernet_available()
            goto_menu(driver, home_tab, 0)
            wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()
            URL_wifi_5g = 'http://dearmyextender.net/api/v1/wifi/1/ssid/0'
            extender_MAC = api_change_wifi_setting(URL_wifi_5g, get_only_mac=True)
            interface_connect_disconnect('Wi-Fi', 'enable')
            interface_connect_disconnect('Ethernet', 'disable')
            wifi_connect = connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
            os.system('netsh wlan show interface mode=BSSID')

            interface_connect_disconnect('Ethernet', 'disable')
            connected_mac = get_current_wifi_MAC()
            print(connected_mac)
            if extender_MAC != connected_mac:
                os.system('netsh wlan delete profile name=*')
                wifi = connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
            connected_mac = get_current_wifi_MAC()

            ip_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google_2 = check_connect_to_google()

            list_actual8 = [wifi_connect, connected_mac, ip_assigned, check_google_2]
            list_expected8 = [REPEATER_MESH_NAME, extender_MAC, return_true, return_true]
            step_8_name = "8. Connect Wifi. Check IP assigned and can connect to google. "
            list_check_in_step_8 = [
                f"Check Connect Wifi (repeater mesh name) is {list_expected8[0]}",
                f"Check Connect Wifi (repeater mac) is {list_expected8[1]}",
                "Check IP is assigned",
                "Check Connect to google success"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('8. Assertion wong')
        # disconnect_or_connect_wan(disconnected=False)

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
            step_1_name = "1. Login. Check Home page is displayed. "
            list_check_in_step_1 = ["Home page is appear"]
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
            qmode = res.get('qmode')
            operation = res.get('operation')

            list_actual2 = [get_mode_name, qmode, operation]
            list_expected2 = ['Repeater Mode', "extender", "mesh slave"]
            step_2_name = "2. Check current operation Mode. " \
                          "Check API /network/qmode. qmode is extender, operation is mesh salve. "
            list_check_in_step_2 = [
                f"Check mode name is: {list_expected2[0]}",
                f"Check qmode is: {list_expected2[1]}",
                f"Check operation is: {list_expected2[2]}"
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
            expected_access_point_mode = {"name": "Access Point Mode",
                                          "meshIcon": True,
                                          "active": False,
                                          "description": exp_access_point_mode_description}
            list_actual3 = list_card_info
            list_expected3 = [expected_router_mode, expected_bridge_mode,
                              expected_repeater_mode, expected_access_point_mode]
            step_3_name = "3. Check Card information of Router mode, Bridge mode, " \
                          "Repeater Mode, AP mode: name, meshIcon, active, description. "
            list_check_in_step_3 = [
                f"Check Router mode information is: {list_expected3[0]}",
                f"Check Bridge mode information is: {list_expected3[1]}",
                f"Check Repeater mode information is: {list_expected3[2]}",
                f"Check Access point mode information is: {list_expected3[3]}",
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
            step_4_name = "4. Select Router mode. Check Apply button enabled. "
            list_check_in_step_4 = ["Check button apply is enabled"]
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
            step_5_name = "5. Select Bridge mode. Check Apply button enabled. "
            list_check_in_step_5 = ["Check button apply is enabled"]
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
            step_6_name = "6. Select Access Point mode. Check Apply button enabled. "
            list_check_in_step_6 = ["Check button apply is enabled"]
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
            step_7_name = "7. Select Repeater mode. Check Reapeater mode is enabled. "
            list_check_in_step_7 = ["Check button apply is selected",
                                    "Check content button next"]
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
            list_step_fail.append('7. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_41_NETWORK_Repeater_Verify_operation_of_Manual_Scan(self):
        self.key = 'NETWORK_41'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        # ===========================================================
        grand_login(driver)
        wait_popup_disappear(driver, dialog_loading)
        goto_menu(driver, network_tab, network_operationmode_tab)
        wait_popup_disappear(driver, dialog_loading)
        connect_repeater_mode(driver, force=True)
        wait_ethernet_available()
        #
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        # connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
        URL_UPPER = get_config('REPEATER', 'url', input_data_path)
        USER_UPPER = get_config('REPEATER', 'user', input_data_path)
        PW_UPPER = get_config('REPEATER', 'pw', input_data_path)
        #
        wait_ethernet_available()
        grand_login(driver, URL_UPPER, USER_UPPER, PW_UPPER)
        wait_popup_disappear(driver, dialog_loading)
        goto_menu(driver, wireless_tab, wireless_guestnetwork_tab)
        wait_popup_disappear(driver, dialog_loading)
        block_2g = driver.find_elements_by_css_selector(guest_network_block)[0]
        while len(block_2g.find_elements_by_css_selector(delete_cls)) > 0:
            block_2g.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)

        wait_ethernet_available()
        block_2g.find_element_by_css_selector(add_class).click()
        time.sleep(0.5)
        # Check Default Value
        edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
        wl_2g_ssid = wireless_get_default_ssid(edit_2g_block, 'Network Name(SSID)')
        wireless_change_choose_option(driver, secure_value_field, 'WEP')
        PW_NEW_WIFI = '12345'
        edit_2g_block = driver.find_elements_by_css_selector(wl_primary_card)[0]
        edit_2g_block.find_element_by_css_selector(ele_input_pw).send_keys(PW_NEW_WIFI)
        wait_ethernet_available()
        # Apply
        edit_2g_block.find_element_by_css_selector(apply).click()
        wait_popup_disappear(driver, dialog_loading)
        wait_ethernet_available()
        # ===========================================================

        try:
            os.system(f'netsh wlan delete profile name=*')
            time.sleep(20)
            wait_ethernet_available()
            grand_login(driver)
            # time.sleep(1)
            goto_menu(driver, network_tab, network_operationmode_tab)
            time.sleep(1)
            # Select Repeater mode
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            # wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()
            # Click Manual scan
            driver.find_element_by_css_selector(ele_manual_scan_btn).click()
            time.sleep(0.5)

            check_title = driver.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual1 = [check_title]
            list_expected1 = ['Manual AP Scan']
            step_1_2_name = "1, 2. Login. Goto Operation Mode. Choose Repeater Mode. Click Next. Click Manual Scan."
            list_check_in_step_1_2 = ["Check title is: Manual AP Scan"]
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            driver.find_element_by_css_selector(input).send_keys(REPEATER_MESH_NAME)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_button_scan_ap).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)

            scan_table = scan_wifi_repeater_mode_table(driver)

            check_result = True
            for r in scan_table:
                if REPEATER_MESH_NAME != r[0].strip():
                    check_result = False

            list_actual2 = [check_result]
            list_expected2 = [return_true]
            step_3_4_name = "3, 4. Scan Exactly SSID name.Check result in scan table."
            list_check_in_step_3_4 = ["Check result in scan table is correct"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            driver.find_element_by_css_selector(ele_manual_scan_btn).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(input).send_keys('Wifi_not_exist')
            time.sleep(1)
            driver.find_element_by_css_selector(ele_button_scan_ap).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)

            scan_table = scan_wifi_repeater_mode_table(driver)

            check_result_2 = True
            for r in scan_table:
                if 'Wifi_not_exist' == r[0].strip():
                    check_result_2 = False

            list_actual3 = [check_result_2]
            list_expected3 = [return_true]
            step_5_name = "5. Scan Not existed SSID. Check searched wifi SSID not in list. "
            list_check_in_step_5 = ["Check Condition 'Only show SSID arround' is correct"]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            driver.find_element_by_css_selector(ele_manual_scan_btn).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(input).send_keys(wl_2g_ssid)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_button_scan_ap).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)

            scan_table = scan_wifi_repeater_mode_table(driver)

            check_result_3 = True
            for r in scan_table:
                if wl_2g_ssid == r[0].strip():
                    check_result_3 = False

            list_actual6 = [check_result_3]
            list_expected6 = [return_true]
            step_6_name = "6. Scan WiFi has Security is WEP. Check searched wifi SSID not in list. "
            list_check_in_step_6 = ["Check Condition 'Don’t show SSID whose security is set to WEP' is correct"]
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
            list_step_fail.append('6. Assertion wong')

        try:
            goto_menu(driver, wireless_tab, wireless_repeater_setting_tab)
            time.sleep(10)
            wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, icon_loading)
            # ==========================================================
            driver.find_element_by_css_selector(ele_manual_scan_btn).click()
            time.sleep(0.5)

            driver.find_element_by_css_selector(input).send_keys(REPEATER_MESH_NAME)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_button_scan_ap).click()
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            scan_table = scan_wifi_repeater_mode_table(driver)

            check_result_4 = True
            for r in scan_table:
                if REPEATER_MESH_NAME != r[0].strip():
                    check_result_4 = False
            # ==========================================================
            driver.find_element_by_css_selector(ele_manual_scan_btn).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(input).send_keys('Wifi_not_exist')
            time.sleep(1)
            driver.find_element_by_css_selector(ele_button_scan_ap).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            scan_table = scan_wifi_repeater_mode_table(driver)

            check_result_5 = True
            for r in scan_table:
                if 'Wifi_not_exist' == r[0].strip():
                    check_result_5 = False
            # ==========================================================
            driver.find_element_by_css_selector(ele_manual_scan_btn).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(input).send_keys(wl_2g_ssid)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_button_scan_ap).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            scan_table = scan_wifi_repeater_mode_table(driver)
            wait_ethernet_available()
            check_result_6 = True
            for r in scan_table:
                if wl_2g_ssid == r[0].strip():
                    check_result_6 = False

            list_actual7 = [check_result_4, check_result_5, check_result_6]
            list_expected7 = [return_true] * 3
            step_7_name = "7. Re-do All step in Wireless > Repeater Setting Page. "
            list_check_in_step_7 = [
                f"Check In table result '{REPEATER_MESH_NAME}' is appear",
                f"Check Condition 'Only show SSID arround' is correct",
                f"Check Condition 'Don’t show SSID whose security is set to WEP' is correct"
            ]
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
            list_step_fail.append('7. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_R3_46_NETWORK_Repeater_Security_WPA2_WPA_PSK(self):
        self.key = 'NETWORK_46'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        disconnect_or_connect_wan(disconnected=True)
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        time.sleep(3)
        wait_ethernet_available()
        #
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        # connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
        URL_UPPER = get_config('REPEATER', 'url', input_data_path)
        USER_UPPER = get_config('REPEATER', 'user', input_data_path)
        PW_UPPER = get_config('REPEATER', 'pw', input_data_path)
        wait_ethernet_available()
        os.system(f'netsh wlan delete profile name=*')

        time.sleep(5)
        wait_ethernet_available()
        grand_login(driver, URL_UPPER, USER_UPPER, PW_UPPER)
        goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
        wait_popup_disappear(driver, dialog_loading)

        block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
        wl_2g_ssid = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
        wireless_change_choose_option(driver, secure_value_field, 'WPA2/WPA-PSK')
        wireless_change_choose_option(driver, encryption_value_field, 'AES')
        wl_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=REPEATER_MESH_PW)
        # Apply
        if block_2g.find_element_by_css_selector(apply).is_displayed():
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(0.5)
        wait_ethernet_available()
        driver.refresh()
        wait_popup_disappear(driver, icon_loading)
        wait_ethernet_available()

        block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
        wl_5g_ssid = wireless_get_default_ssid(block_5g, 'Network Name(SSID)')
        wireless_change_choose_option(block_5g, secure_value_field, 'WPA2/WPA-PSK')
        wireless_change_choose_option(block_5g, encryption_value_field, 'AES')
        wl_5g_pw = wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=REPEATER_MESH_PW)
        # Apply
        wait_ethernet_available()
        if block_5g.find_element_by_css_selector(apply).is_displayed():
            block_5g.find_element_by_css_selector(apply).click()
            wait_ethernet_available()
            wait_popup_disappear(driver, dialog_loading)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(0.5)
            wait_ethernet_available()
        # ===========================================================
        driver.refresh()
        wait_popup_disappear(driver, icon_loading)
        wait_ethernet_available()
        try:
            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == wl_2g_ssid:
                    r.click()
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(wl_2g_pw).perform()
            time.sleep(1)
            # Apply
            driver.find_element_by_css_selector(ele_apply_highlight).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, lg_page)
            time.sleep(20)
            wait_ethernet_available()
            check_connect_web_2 = check_connect_to_web_admin_page()
            check_connect_google_2 = check_connect_to_google()
            # print(requests.get('http://dearmyextender.net').status_code)
            # print(requests.get('http://google.com').status_code)

            list_actual1 = [check_connect_web_2, check_connect_google_2]
            list_expected1 = [return_true] * 2
            step_1_2_name = "1, 2. Change Security to WPA2/WPA-PSK of 2G. Check connect to WEB and connect to Google. "
            list_check_in_step_1_2 = [
                "Check connect web success",
                "Check connect google success"
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == wl_5g_ssid:
                    r.click()
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(wl_5g_pw).perform()
            time.sleep(1)
            # Apply
            driver.find_element_by_css_selector(ele_apply_highlight).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(10)
            wait_ethernet_available()
            # check_connect_web_5 = requests.get('http://dearmyextender.net').status_code
            # check_connect_google_5 = requests.get('http://google.com').status_code
            check_connect_web_5 = check_connect_to_web_admin_page()
            check_connect_google_5 = check_connect_to_google()
            list_actual3 = [check_connect_web_5, check_connect_google_5]
            list_expected3 = [return_true] * 2
            step_3_name = "3. Change Security to WPA2/WPA-PSK of 5G. Check connect to WEB and connect to Google."
            list_check_in_step_3 = [
                "Check Connect to WEB success",
                "Check Connect to google success"
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
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_R2_47_NETWORK_Repeater_Security_WPA2_PSK(self):
        self.key = 'NETWORK_47'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================

        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        connect_repeater_mode(driver)
        wait_ethernet_available()
        time.sleep(5)
        #
        REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        # connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
        URL_UPPER = get_config('REPEATER', 'url', input_data_path)
        USER_UPPER = get_config('REPEATER', 'user', input_data_path)
        PW_UPPER = get_config('REPEATER', 'pw', input_data_path)

        #
        time.sleep(10)
        wait_ethernet_available()
        grand_login(driver, URL_UPPER, USER_UPPER, PW_UPPER)
        goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
        wait_popup_disappear(driver, dialog_loading)

        block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
        wl_2g_ssid = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
        wireless_change_choose_option(driver, secure_value_field, 'WPA2-PSK')
        wireless_change_choose_option(driver, encryption_value_field, 'AES')
        wl_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=REPEATER_MESH_PW)
        # Apply
        if block_2g.find_element_by_css_selector(apply).is_displayed():
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(0.5)
        wait_ethernet_available()
        driver.refresh()
        wait_popup_disappear(driver, icon_loading)
        wait_ethernet_available()

        block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
        wl_5g_ssid = wireless_get_default_ssid(block_5g, 'Network Name(SSID)')
        wireless_change_choose_option(block_5g, secure_value_field, 'WPA2-PSK')
        wireless_change_choose_option(block_5g, encryption_value_field, 'AES')
        wl_5g_pw = wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=REPEATER_MESH_PW)
        # Apply
        wait_ethernet_available()
        if block_5g.find_element_by_css_selector(apply).is_displayed():
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            wait_ethernet_available()
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(0.5)
            wait_ethernet_available()
        # ===========================================================
        driver.refresh()
        wait_popup_disappear(driver, icon_loading)
        wait_ethernet_available()
        # wl_2g_ssid='wifi_upper_16_2G!'
        # wl_2g_pw= 'humax_0001'
        # wl_5g_ssid='wifi_upper_16_5G!'
        # wl_5g_pw = 'humax_0001'
        try:
            wait_ethernet_available()
            os.system(f'netsh wlan delete profile name=*')
            time.sleep(10)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == wl_2g_ssid:
                    r.click()
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(wl_2g_pw).perform()
            time.sleep(1)
            # Apply
            driver.find_element_by_css_selector(ele_apply_highlight).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()
            time.sleep(2)
            wait_ethernet_available()
            wait_ethernet_available()
            check_connect_web_2 = check_connect_to_web_admin_page()
            check_connect_google_2 = check_connect_to_google()

            list_actual1 = [check_connect_web_2, check_connect_google_2]
            list_expected1 = [return_true] * 2
            step_1_2_name = "1, 2. Change Security to WPA2-PSK of 2G. Check connect to WEB and connect to Google. "
            list_check_in_step_1_2 = [
                "Check Connect web success",
                "Check Connect google success",
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(10)
            wait_ethernet_available()
            time.sleep(5)
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == wl_5g_ssid:
                    r.click()
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(wl_5g_pw).perform()
            time.sleep(1)
            # Apply
            driver.find_element_by_css_selector(ele_apply_highlight).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(10)
            wait_ethernet_available()

            check_connect_web_5 = check_connect_to_web_admin_page()
            check_connect_google_5 = check_connect_to_google()

            list_actual3 = [check_connect_web_5, check_connect_google_5]
            list_expected3 = [return_true] * 2
            step_3_name = "3. Change Security to WPA2-PSK of 5G. Check connect to WEB and connect to Google"
            list_check_in_step_3 = [
                "Check connect to web success",
                "Check connect to google success"
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
            list_step_fail.append('3. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # def test_R1_49_NETWORK_Repeater_Security_None(self):
    #     self.key = 'NETWORK_49'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     # ===========================================================
    #     # disconnect_or_connect_wan(disconnected=True)
    #     grand_login(driver)
    #     time.sleep(2)
    #     goto_menu(driver, network_tab, network_operationmode_tab)
    #     time.sleep(1)
    #     wait_popup_disappear(driver, dialog_loading)
    #     connect_repeater_mode(driver)
    #     wait_ethernet_available()
    #     time.sleep(5)
    #     REPEATER_MESH_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
    #     REPEATER_MESH_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
    #     # connect_wifi_by_command(REPEATER_MESH_NAME, REPEATER_MESH_PW)
    #     URL_UPPER = get_config('REPEATER', 'url', input_data_path)
    #     USER_UPPER = get_config('REPEATER', 'user', input_data_path)
    #     PW_UPPER = get_config('REPEATER', 'pw', input_data_path)
    #     os.system(f'netsh wlan delete profile name=*')
    #     time.sleep(5)
    #     wait_ethernet_available()
    #     #
    #     grand_login(driver, URL_UPPER, USER_UPPER, PW_UPPER)
    #     goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
    #     wait_popup_disappear(driver, dialog_loading)
    #
    #     block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
    #     wl_2g_ssid = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
    #     wireless_change_choose_option(driver, secure_value_field, 'NONE')
    #
    #     # Apply
    #     if block_2g.find_element_by_css_selector(apply).is_displayed():
    #         block_2g.find_element_by_css_selector(apply).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(0.5)
    #         if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             time.sleep(0.5)
    #     wait_ethernet_available()
    #     driver.refresh()
    #     wait_popup_disappear(driver, icon_loading)
    #     wait_ethernet_available()
    #     block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
    #     wl_5g_ssid = wireless_get_default_ssid(block_5g, 'Network Name(SSID)')
    #     wireless_change_choose_option(block_5g, secure_value_field, 'NONE')
    #     wait_ethernet_available()
    #     if block_5g.find_element_by_css_selector(apply).is_displayed():
    #         block_5g.find_element_by_css_selector(apply).click()
    #         wait_ethernet_available()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(0.5)
    #         if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             time.sleep(0.5)
    #         wait_ethernet_available()
    #     # ===========================================================
    #     driver.refresh()
    #     wait_popup_disappear(driver, icon_loading)
    #     wait_ethernet_available()
    #     try:
    #         time.sleep(10)
    #         wait_ethernet_available()
    #         grand_login(driver)
    #         time.sleep(1)
    #         goto_menu(driver, network_tab, network_operationmode_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #         driver.find_element_by_css_selector(ele_select_repeater_mode).click()
    #         time.sleep(0.5)
    #         driver.find_element_by_css_selector(apply).click()
    #         time.sleep(0.5)
    #         wait_popup_disappear(driver, dialog_loading)
    #         _rows = driver.find_elements_by_css_selector(rows)
    #         # Choose Network name
    #         for r in _rows:
    #             if r.find_element_by_css_selector(ele_network_name).text.strip() == wl_2g_ssid:
    #                 r.click()
    #                 break
    #         # # Fill Password
    #         # pw_box = driver.find_element_by_css_selector(ele_input_pw)
    #         # ActionChains(driver).click(pw_box).send_keys(wl_2g_pw).perform()
    #         # time.sleep(1)
    #         # Apply
    #         driver.find_element_by_css_selector(ele_apply_highlight).click()
    #         time.sleep(0.5)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(100)
    #         wait_popup_disappear(driver, icon_loading)
    #         time.sleep(1)
    #         wait_popup_disappear(driver, icon_loading)
    #         wait_visible(driver, lg_page)
    #
    #         wait_ethernet_available()
    #         time.sleep(10)
    #         time.sleep(5)
    #         check_connect_web_2 = check_connect_to_web_admin_page()
    #         check_connect_google_2 = check_connect_to_google()
    #         # print(requests.get('http://dearmyextender.net').status_code)
    #         # print(requests.get('http://google.com').status_code)
    #
    #         list_actual1 = [check_connect_web_2, check_connect_google_2]
    #         list_expected1 = [return_true] * 2
    #         step_1_2_name = "1, 2. Change Security to None of 2G. Check connect to WEB and connect to Google. "
    #         list_check_in_step_1_2 = [
    #             "Connect to WEB success",
    #             "Connect to Google success",
    #         ]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             generate_step_information(
    #                 step_name=step_1_2_name,
    #                 list_check_in_step=list_check_in_step_1_2,
    #                 list_actual=list_actual1,
    #                 list_expected=list_expected1
    #             )
    #         )
    #     except:
    #         self.list_steps.append(
    #             generate_step_information(
    #                 step_name=step_1_2_name,
    #                 list_check_in_step=list_check_in_step_1_2,
    #                 list_actual=list_actual1,
    #                 list_expected=list_expected1
    #             )
    #         )
    #         list_step_fail.append('1, 2. Assertion wong')
    #
    #     try:
    #         time.sleep(10)
    #         wait_ethernet_available()
    #         grand_login(driver)
    #         time.sleep(1)
    #         goto_menu(driver, network_tab, network_operationmode_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #         driver.find_element_by_css_selector(ele_select_repeater_mode).click()
    #         time.sleep(0.5)
    #         driver.find_element_by_css_selector(apply).click()
    #         time.sleep(0.5)
    #         wait_popup_disappear(driver, dialog_loading)
    #         _rows = driver.find_elements_by_css_selector(rows)
    #         # Choose Network name
    #         for r in _rows:
    #             if r.find_element_by_css_selector(ele_network_name).text.strip() == wl_5g_ssid:
    #                 r.click()
    #                 break
    #         # # Fill Password
    #         # pw_box = driver.find_element_by_css_selector(ele_input_pw)
    #         # ActionChains(driver).click(pw_box).send_keys(wl_5g_pw).perform()
    #         # time.sleep(1)
    #         # Apply
    #         driver.find_element_by_css_selector(ele_apply_highlight).click()
    #         time.sleep(0.5)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(100)
    #         wait_popup_disappear(driver, icon_loading)
    #         time.sleep(1)
    #         wait_popup_disappear(driver, icon_loading)
    #         wait_visible(driver, lg_page)
    #         time.sleep(20)
    #         wait_ethernet_available()
    #
    #         check_connect_web_5 = check_connect_to_web_admin_page()
    #         check_connect_google_5 = check_connect_to_google()
    #         list_actual3 = [check_connect_web_5, check_connect_google_5]
    #         list_expected3 = [return_true] * 2
    #         step_3_name = "3. Change Security to None of 5G. Check connect to WEB and connect to Google. "
    #         list_check_in_step_3 = [
    #             "Check connect to web success",
    #             "Check connect to google success"
    #         ]
    #         check = assert_list(list_actual3, list_expected3)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             generate_step_information(
    #                 step_name=step_3_name,
    #                 list_check_in_step=list_check_in_step_3,
    #                 list_actual=list_actual3,
    #                 list_expected=list_expected3
    #             )
    #         )
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             generate_step_information(
    #                 step_name=step_3_name,
    #                 list_check_in_step=list_check_in_step_3,
    #                 list_actual=list_actual3,
    #                 list_expected=list_expected3
    #             )
    #         )
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('3. Assertion wong')
    #
    #     self.assertListEqual(list_step_fail, [])

    def test_51_NETWORK_Verify_Bridge_Mode_operation(self):
        self.key = 'NETWORK_51'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # FIX bug of handle Upper ò NETWORK 46>47>49. Connect wifi upper.
        os.system('netsh wlan disconnect')
        interface_connect_disconnect('Wi-Fi', 'Enable')
        interface_connect_disconnect('Ethernet', 'Disable')

        # Connect Wifi Upper
        UPPER_URL = get_config('REPEATER', 'url', input_data_path)
        UPPER_USER = get_config('REPEATER', 'user', input_data_path)
        UPPER_PW = get_config('REPEATER', 'pw', input_data_path)
        UPPER_WIFI_5G_SSID = get_config('REPEATER', 'repeater_name_5g', input_data_path)
        UPPER_WIFI_5G_PW = get_config('REPEATER', 'repeater_pw_5g', input_data_path)
        UPPER_WIFI_2G_SSID = get_config('REPEATER', 'repeater_name', input_data_path)
        UPPER_WIFI_2G_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        # UPPER_MESH_2G_PW = get_config('REPEATER', 'repeater_pw', input_data_path)

        connect_upper = connect_wifi_by_command(UPPER_WIFI_2G_SSID, UPPER_WIFI_2G_PW)
        time.sleep(5)
        if connect_upper != UPPER_WIFI_2G_SSID:
            other_connection = connect_wifi_by_command(UPPER_WIFI_2G_SSID, UPPER_WIFI_2G_PW, xml_file=wifi_none_secure_path)
            print(other_connection)

        grand_login(driver, UPPER_URL, UPPER_USER, UPPER_PW)
        goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

        block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
        wireless_get_default_ssid(block_5g, 'Network Name(SSID)')
        wireless_change_choose_option(block_5g, secure_value_field, 'WPA2/WPA-PSK')
        wireless_change_choose_option(block_5g, encryption_value_field, 'AES')
        wireless_check_pw_eye(driver, block_5g, change_pw=True, new_pw=UPPER_WIFI_5G_PW)

        if block_5g.find_element_by_css_selector(apply).is_displayed():
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)


        block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
        wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
        wireless_change_choose_option(driver, secure_value_field, 'WPA2/WPA-PSK')
        wireless_change_choose_option(driver, encryption_value_field, 'AES')
        wireless_check_pw_eye(driver, block_2g, change_pw=True, new_pw=UPPER_WIFI_2G_PW)

        if block_2g.find_element_by_css_selector(apply).is_displayed():
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # driver.find_element_by_css_selector(btn_ok).click()
            # wait_popup_disappear(driver, dialog_loading)



        os.system('netsh wlan disconnect')
        os.system('netsh wlan delete profile name=*')
        interface_connect_disconnect('Ethernet', 'Enable')
        # ===========================================================
        NEW_SSID_2G_NAME = get_config('NETWORK', 'nw_51_new_ssid_2g', input_data_path)
        NEW_SSID_5G_NAME = get_config('NETWORK', 'nw_51_new_ssid_5g', input_data_path)
        # ===========================================================
        factory_dut()
        try:
            grand_login(driver)
            time.sleep(1)
            goto_menu(driver, network_tab, network_operationmode_tab)
            time.sleep(1)
            current_page = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [current_page]
            list_expected1 = ['Advanced > Operation Mode']
            check = assert_list(list_actual1, list_expected1)
            step_1_2_name = "1, 2. Login. Goto Operation mode page. Check current page. "
            list_check_in_step_1_2 = [f"Check wrap title page is: {list_expected1[0]}"]
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            driver.find_element_by_css_selector(ele_select_bridge_mode).click()
            # Apply
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, lg_page)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            # ==========================================================================
            time.sleep(5)
            # Login
            # driver.refresh()
            time.sleep(5)
            grand_login(driver)
            goto_menu(driver, network_tab, network_operationmode_tab)
            time.sleep(5)
            check_bridge_mode_active = driver.find_element_by_css_selector(ele_bridge_mode_input).is_selected()

            list_actual3 = [check_bridge_mode_active]
            list_expected3 = [return_true]
            step_3_name = "3. Change to Bridge mode. Check change successfully in Operation mode. "
            list_check_in_step_3 = ["Bridge mode is selected"]
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
            list_step_fail.append('3. Assertion wong')

        try:
            get_ip_v4 = get_value_from_ipconfig('Ethernet adapter Ethernet', 'IPv4 Address')
            if '(Preferred)' in get_ip_v4:
                get_ip_v4 = get_ip_v4.replace('(Preferred)', '')
            check_ipv4 = get_ip_v4 != 'Block or field error.'
            check_access_google = check_connect_to_google()

            list_actual4 = [check_ipv4, check_access_google]
            list_expected4 = [return_true] *2
            step_4_name = "4. Check IPv4 address assigned (difference 0.0.0.0). "
            list_check_in_step_4 = ["Check Condition 'IPv4 address assigned difference 0.0.0.0' is correct"]
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
            list_step_fail.append('4. Assertion wong')

        try:
            # Get information
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            # Get information of wireless
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
            wifi_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=False)

            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wifi_5g_name = wireless_get_default_ssid(block_5g, 'Network Name(SSID)')
            wifi_5g_pw = wireless_check_pw_eye(driver, block_5g, change_pw=False)

            # Disconnect Wire
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)

            # Connect wireless 2G
            write_data_to_xml(wifi_default_file_path, new_name=wifi_2g_name, new_pw=wifi_2g_pw)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wifi_2g_name}"')
            time.sleep(3)
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{wifi_2g_name}" name="{wifi_2g_name}"')
            time.sleep(10)

            # Check IP assigned
            wifi_2g_ip = get_value_from_ipconfig('Wireless LAN adapter Wi-Fi', 'IPv4 Address').replace('(Preferred)', '')
            wifi_2g_ip = wifi_2g_ip != 'Block or field error.'
            wifi_2g_check_google = check_connect_to_google()
            current_connected_wifi_2g_name = current_connected_wifi()

            list_actual5 = [wifi_2g_ip, wifi_2g_check_google, current_connected_wifi_2g_name]
            list_expected5 = [return_true, return_true, exp_ssid_2g_default_val]
            step_5_name = "[Pass] 5.1 Connect Wifi 2G. " \
                          "Check IP address assigned. " \
                          "Check connect to Google. " \
                          "Check Current connected Wifi. '"
            list_check_in_step_5 = [
                "Check IP address assigned",
                "Connect to google success",
                f"Current conected wifi is: {exp_ssid_2g_default_val}"
            ]
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
            list_step_fail.append('5.1 Assertion wong')


        try:
            os.system(f'netsh wlan disconnect')
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path, new_name=wifi_5g_name, new_pw=wifi_5g_pw)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{wifi_5g_name}"')
            time.sleep(3)
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(3)
            os.system(f'netsh wlan connect ssid="{wifi_5g_name}" name="{wifi_5g_name}"')
            time.sleep(3)

            # Check IP assigned
            wifi_5g_ip = get_value_from_ipconfig('Wireless LAN adapter Wi-Fi', 'IPv4 Address').replace('(Preferred)', '')
            wifi_5g_ip = wifi_5g_ip != 'Block or field error.'
            wifi_5g_check_google = check_connect_to_google()
            current_connected_wifi_5g_name = current_connected_wifi()
            # =============================================================
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

            list_actual6 = [wifi_5g_ip, wifi_5g_check_google, current_connected_wifi_5g_name]
            list_expected6 = [return_true, return_true, exp_ssid_5g_default_val]
            step_5_2_name = "5.2 Connect Wifi 5G. " \
                            "Check IP address assigned. " \
                            "Check connect to Google. " \
                            "Check Current connected Wifi."
            list_check_in_step_5_2 = ["Get result by command success"]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_2_name,
                    list_check_in_step=list_check_in_step_5_2,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )

        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_2_name,
                    list_check_in_step=list_check_in_step_5_2,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append('5.2 Assertion wong')

        try:

            grand_login(driver)
            time.sleep(3)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(3)
            # Get information of wireless
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            edit_2g_label = block_2g.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = block_2g.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    f.click()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(NEW_SSID_2G_NAME).perform()
                    break
            time.sleep(1)
            block_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
            edit_2g_label = block_5g.find_elements_by_css_selector(label_name_in_2g)
            edit_2g_fields = block_5g.find_elements_by_css_selector(wrap_input)
            for l, f in zip(edit_2g_label, edit_2g_fields):
                # Connection type
                if l.text == 'Network Name(SSID)':
                    f.click()
                    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(NEW_SSID_5G_NAME).perform()
                break
            time.sleep(3)
            block_5g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            # =================================================================================
            # Disconnect Wire
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            os.system(f'netsh wlan disconnect')

            # Connect wireless 2G
            write_data_to_xml(wifi_default_file_path, new_name=NEW_SSID_2G_NAME, new_pw=wifi_2g_pw)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{NEW_SSID_2G_NAME}"')
            time.sleep(3)
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'netsh wlan connect ssid="{NEW_SSID_2G_NAME}" name="{NEW_SSID_2G_NAME}"')
            time.sleep(10)

            # Check IP assigned
            wifi_2g_ip_2 = get_value_from_ipconfig('Wireless LAN adapter Wi-Fi', 'IPv4 Address')
            wifi_2g_ip_2 = wifi_2g_ip_2.replace('(Preferred)','') != 'Block or field error.'
            wifi_2g_check_google_2 = check_connect_to_google()
            current_connected_wifi_2g_name_2 = current_connected_wifi()
            # =================================================================================
            os.system(f'netsh wlan disconnect')
            time.sleep(3)
            write_data_to_xml(wifi_default_file_path, new_name=NEW_SSID_5G_NAME, new_pw=wifi_5g_pw)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{NEW_SSID_5G_NAME}"')
            time.sleep(3)
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(3)
            os.system(f'netsh wlan connect ssid="{NEW_SSID_5G_NAME}" name="{NEW_SSID_5G_NAME}"')
            time.sleep(10)

            # Check IP assigned
            wifi_5g_ip_2 = get_value_from_ipconfig('Wireless LAN adapter Wi-Fi', 'IPv4 Address')
            wifi_5g_ip_2 = wifi_5g_ip_2.replace('(Preferred)','') != 'Block or field error.'
            wifi_5g_check_google_2 = check_connect_to_google()
            current_connected_wifi_5g_name_2 = current_connected_wifi()

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            list_actual7 = [wifi_2g_ip_2, wifi_2g_check_google_2, current_connected_wifi_2g_name_2,
                            wifi_5g_ip_2, wifi_5g_check_google_2, current_connected_wifi_5g_name_2]
            list_expected7 = [return_true, return_true, NEW_SSID_2G_NAME,
                              return_true, return_true, NEW_SSID_5G_NAME]
            step_6_name = "6. Change SSID 2G/5G. Check 2G IPv4, Connect Google, Current connected wifi. " \
                          "Check 5G IPv4, Connect Google, Current connected wifi. "
            list_check_in_step_6 = [
                "When use 2G, ipv4 is correct",
                "When use 2G, connect google success",
                f"When use 2G, current conected wifi name is: {current_connected_wifi_2g_name_2}",
                "When use 5G, ipv4 is correct",
                "When use 5G, connect google success",
                f"When use 5G, current conected wifi name is: {current_connected_wifi_5g_name_2}",
            ]
            check = assert_list(list_actual7, list_expected7)
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
            list_step_fail.append('6. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_34_NETWORK_Easy_Setup_Verification_of_upper_router_and_extender_connection_by_wireless_2g_third_party(self):
        self.key = 'NETWORK_34'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        # disconnect_or_connect_wan(disconnected=True)
        factory_dut()
        # ======================================================
        THIRD_PARTY_NAME = get_config('REPEATER', 'third_party_name', input_data_path)
        THIRD_PARTY_PW = get_config('REPEATER', 'third_party_pw', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
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
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            # Choose
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break

            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)
            wait_popup_disappear(driver, '.loading-wizard')
            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            wait_popup_disappear(driver, '.loading-wizard')
            list_column = [i.text for i in driver.find_elements_by_css_selector('thead .col')]

            list_actual1 = [title_repeater_setting_1, list_column]
            list_expected1 = ['Repeater Setting',
                              ['Network Name(SSID)', 'CH', 'RSSI', 'Security', 'MAC Address', 'Band']]
            step_1_2_name = "1,2. Login. Next to Repeater Setting. Check title. Check list columns in Repeater Setting."
            list_check_in_step_1_2 = [
                f"Title page is: {list_expected1[0]}",
                f"List column is: {list_expected1[1]}"
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == THIRD_PARTY_NAME:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(THIRD_PARTY_PW).perform()
            time.sleep(1)

            # Get info
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == THIRD_PARTY_NAME:
                    get_security = r.find_element_by_css_selector(security_page).text

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(3)

            title_popup = driver.find_element_by_css_selector(lg_welcome_header).text
            # Check SSID tag
            network_name = driver.find_elements_by_css_selector('.input-wrap input[name="input-field"]')
            check_network_name_2g = network_name[0].get_attribute('value')
            check_network_name_5g = network_name[1].get_attribute('value')
            expected_check_network_name_2g = THIRD_PARTY_NAME
            # expected_check_network_name_2g = THIRD_PARTY_NAME + '_Ext2G'
            expected_check_network_name_5g = THIRD_PARTY_NAME+'_Ext5G'
            check_same_pw = driver.find_element_by_css_selector(ele_wizard_check_same_pw_input).is_selected()

            list_actual3 = [title_popup, check_network_name_2g, check_network_name_5g, check_same_pw]
            list_expected3 = ['Repeater Setting',
                              expected_check_network_name_2g,
                              expected_check_network_name_5g,
                              return_true]
            step_3_name = "3. Select Third Party Wifi. Input Password. Next. " \
                          "Check popup title. Check Repeater Wifi name of 2G and 5G. " \
                          "Check box Same as 2.4GHz password is checked. "
            list_check_in_step_3 = [
                f"Check Title page is: {list_expected3[0]}",
                f"Network 2g name is: {expected_check_network_name_2g}",
                f"Network 5g mame is: {expected_check_network_name_5g}",
                f"Check box Same as 2.4GHz password is check"
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
            list_step_fail.append('3. Assertion wong')

        try:
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            # Get value form Summary page
            summary_card = driver.find_element_by_css_selector('.summary>.content-box')

            internet_card = summary_card.find_element_by_css_selector(internet_cls)
            ls_internet_values = [i.find_element_by_css_selector(right).text for i in
                                  internet_card.find_elements_by_css_selector(rows)]
            ls_internet_values.pop(2)

            wireless_2g_card = summary_card.find_elements_by_css_selector('.wireless')[0]
            ls_2g_values = [i.find_element_by_css_selector(right).text for i in
                                  wireless_2g_card.find_elements_by_css_selector(rows)]

            wireless_5g_card = summary_card.find_elements_by_css_selector('.wireless')[1]
            ls_5g_values = [i.find_element_by_css_selector(right).text for i in
                            wireless_5g_card.find_elements_by_css_selector(rows)]
            # Click Let go
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            wait_popup_disappear(driver, icon_loading)
            # load_content = driver.find_element_by_css_selector(content).text
            time.sleep(100)
            wait_ethernet_available()
            wait_popup_disappear(driver, icon_loading)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(20)
            wait_ethernet_available()

            list_actual4 = [ls_internet_values, ls_2g_values, ls_5g_values]
            list_expected4 = [['Repeater Mode', THIRD_PARTY_NAME, THIRD_PARTY_PW],
                              [expected_check_network_name_2g, THIRD_PARTY_PW],
                              [expected_check_network_name_5g, THIRD_PARTY_PW]]
            step_4_name = "4. CLick next until Let Go display. Click Let Go. Check Loading popup content. "
            list_check_in_step_4 = [
                f"Check ls Internet values is: {list_expected4[0]}",
                f"Check ls 2g values is: {list_expected4[1]}",
                f"Check ls 5g values is: {list_expected4[2]}",
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
            list_step_fail.append('4. Assertion wong')

        try:
            wait_ethernet_available()
            time.sleep(10)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            check_home_page = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            check_wan_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)

            list_actual5 = [check_home_page, check_wan_assigned]
            list_expected5 = [return_true] *2
            step_5_6_name = " 5, 6. Login again. " \
                            "Check Home page is display and Wan IP assigned. "
            list_check_in_step_5_6 = [
                "Home page is appear",
                "Wan IP is assigned"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5, 6. Assertion wong')

        try:
            # Check Network
            wireless_card = driver.find_element_by_css_selector(ele_wireless_card)
            labels = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values = wireless_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'Network Name(SSID)':
                    nw_name_value_2g = v.text
                if l.text == 'Security':
                    nw_security_2g = v.text
                    break
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[1].click()
            wireless_card = driver.find_element_by_css_selector(ele_wireless_card)
            labels = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values = wireless_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'Network Name(SSID)':
                    nw_name_value_5g = v.text
                if l.text == 'Security':
                    nw_security_5g = v.text
                    break

            # CLick Home wan
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            host_nw_block = driver.find_element_by_css_selector(ele_host_network)

            labels = host_nw_block.find_elements_by_css_selector(label_name_in_2g)
            values = host_nw_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Connection status':
                    check_conn_status = v.text
                    break

            list_actual7 = [[nw_name_value_2g, nw_security_2g], [nw_name_value_5g, nw_security_5g], check_conn_status]
            list_expected7 = [[check_network_name_2g, get_security],
                              [check_network_name_5g, get_security],
                              'Connected (2.4GHz)']
            step_7_name = "7. Check SSID and Security of Wireless 2.4GHz and 5GHz and check connection status. "
            list_check_in_step_7 = [
                f"Check SSID and Security of Wireless 2.4GHz is: {list_expected7[0]}",
                f"Check SSID and Security of Wireless 5GHz is: {list_expected7[1]}",
                f"Check connection status is: {list_expected7[2]}"
            ]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('7. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            check_repeater_mode = driver.find_element_by_css_selector(ele_repeater_mode_input).is_selected()

            list_actual8 = [check_repeater_mode]
            list_expected8 = [return_true]
            step_8_name = "8. Goto Network > Operation Mode. Check Repeater mode is selected. "
            list_check_in_step_8 = ["Repeater mode is selected"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('8. Assertion wong')

        try:
            interface_connect_disconnect('Ethernet', 'disable')
            connect_wifi_by_command(check_network_name_2g, THIRD_PARTY_PW)
            os.system('netsh wlan show interface mode=BSSID')
            goto_menu(driver, home_tab, 0)

            ip_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google_2 = check_connect_to_google()
            check_youtube_2 = check_connect_to_youtube()

            interface_connect_disconnect('Ethernet', 'enable')

            list_actual9 = [ip_assigned, check_google_2, check_youtube_2]
            list_expected9 = [return_true] * 3
            step_9_name = "9. Connect Wifi. Check IP assigned and can connect to google and youtube. "
            list_check_in_step_9 = [
                "Check IP is assigned",
                "Check Connect to google success",
                "Check Connect to youtube success"
            ]
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong')
        # disconnect_or_connect_wan(disconnected=False)

        self.assertListEqual(list_step_fail, [])

    def test_35_NETWORK_Easy_Setup_Verification_of_upper_router_and_extender_connection_by_wireless_5g_third_party(self):
        self.key = 'NETWORK_35'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        # disconnect_or_connect_wan(disconnected=True)
        factory_dut()


        # ======================================================
        THIRD_PARTY_NAME_5G = get_config('REPEATER', 'third_party_name_5g', input_data_path)
        THIRD_PARTY_PW_5G = get_config('REPEATER', 'third_party_pw_5g', input_data_path)

        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
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
            ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
            for p, v in zip(change_pw_fields, ls_change_pw_value):
                ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                time.sleep(0.5)
            # Next Change pw
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                wait_popup_disappear(driver, dialog_loading)

            # Change Operation Mode
            driver.find_element_by_css_selector(ele_welcome_router_box).click()
            time.sleep(0.5)
            operation_block = driver.find_element_by_css_selector(ele_welcome_router_box)
            list_options = operation_block.find_elements_by_css_selector(secure_value_in_drop_down)
            # Choose
            for o in list_options:
                if o.text == 'Repeater Mode':
                    o.click()
                    break

            # Next
            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
                time.sleep(3)
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(10)
            wait_popup_disappear(driver, icon_loading)
            wait_popup_disappear(driver, '.loading-wizard')
            title_repeater_setting_1 = driver.find_element_by_css_selector(lg_welcome_header).text
            wait_popup_disappear(driver, '.loading-wizard')
            list_column = [i.text for i in driver.find_elements_by_css_selector('thead .col')]

            list_actual1 = [title_repeater_setting_1, list_column]
            list_expected1 = ['Repeater Setting',
                              ['Network Name(SSID)', 'CH', 'RSSI', 'Security', 'MAC Address', 'Band']]
            step_1_2_name = "1, 2. Login. Next to Repeater Setting. " \
                            "Check title. Check list columns in Repeater Setting. "
            list_check_in_step_1_2 = [
                f"Check Title page is: {list_expected1[0]}",
                f"Check List column  page is: {list_expected1[1]}",
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == THIRD_PARTY_NAME_5G:
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(THIRD_PARTY_PW_5G).perform()
            time.sleep(1)

            # Get info
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == THIRD_PARTY_NAME_5G:
                    get_security = r.find_element_by_css_selector(security_page).text

            wait_visible(driver, welcome_next_btn)
            next_btn = driver.find_element_by_css_selector(welcome_next_btn)
            if not next_btn.get_property('disabled'):
                next_btn.click()
            time.sleep(3)

            title_popup = driver.find_element_by_css_selector(lg_welcome_header).text
            # Check SSID tag
            network_name = driver.find_elements_by_css_selector('.input-wrap input[name="input-field"]')
            check_network_name_2g = network_name[0].get_attribute('value')
            check_network_name_5g = network_name[1].get_attribute('value')
            expected_check_network_name_2g = THIRD_PARTY_NAME_5G+'_Ext2G'
            expected_check_network_name_5g = THIRD_PARTY_NAME_5G
            # expected_check_network_name_5g = THIRD_PARTY_NAME_5G + '_Ext5G'
            check_same_pw = driver.find_element_by_css_selector(ele_wizard_check_same_pw_input).is_selected()

            list_actual3 = [title_popup, check_network_name_2g, check_network_name_5g, check_same_pw]
            list_expected3 = ['Repeater Setting',
                              expected_check_network_name_2g,
                              expected_check_network_name_5g,
                              return_true]
            step_3_name = "3. Select Third Party Wifi. Input Password. Next. " \
                          "Check popup title. Check Repeater Wifi name of 2G and 5G. " \
                          "Check box Same as 2.4GHz password is checked. ."
            list_check_in_step_3 = [
                f"Check popup title is: {list_expected3[0]}",
                f"Check Repeater Wifi name of 2G is: {expected_check_network_name_2g}",
                f"Check Repeater Wifi name of 5G is: {expected_check_network_name_5g}",
                "Check checkbox Same as 2.4GHz password is check"
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
            list_step_fail.append('3. Assertion wong')

        try:
            while True:
                time.sleep(1)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(3)

                if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
                    break

            # Get value form Summary page
            summary_card = driver.find_element_by_css_selector('.summary>.content-box')

            internet_card = summary_card.find_element_by_css_selector(internet_cls)
            ls_internet_values = [i.find_element_by_css_selector(right).text for i in
                                  internet_card.find_elements_by_css_selector(rows)]
            ls_internet_values.pop(2)

            wireless_2g_card = summary_card.find_elements_by_css_selector('.wireless')[0]
            ls_2g_values = [i.find_element_by_css_selector(right).text for i in
                                  wireless_2g_card.find_elements_by_css_selector(rows)]

            wireless_5g_card = summary_card.find_elements_by_css_selector('.wireless')[1]
            ls_5g_values = [i.find_element_by_css_selector(right).text for i in
                            wireless_5g_card.find_elements_by_css_selector(rows)]
            # Click Let go
            driver.find_element_by_css_selector(welcome_let_go_btn).click()
            wait_popup_disappear(driver, icon_loading)
            # load_content = driver.find_element_by_css_selector(content).text
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(20)
            wait_ethernet_available()

            list_actual4 = [ls_internet_values, ls_2g_values, ls_5g_values]
            list_expected4 = [['Repeater Mode', THIRD_PARTY_NAME_5G, THIRD_PARTY_PW_5G],
                              [expected_check_network_name_2g, THIRD_PARTY_PW_5G],
                              [expected_check_network_name_5g, THIRD_PARTY_PW_5G]]
            step_4_name = "4. CLick next until Let Go display. Click Let Go. " \
                          "Check Loading popup content."
            list_check_in_step_4 = [
                f"Check ls internet values is: {list_expected4[0]}",
                f"Check ls 2g values is: {list_expected4[1]}",
                f"Check ls 5g values is: {list_expected4[2]}"
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
            list_step_fail.append('4. Assertion wong')

        try:
            wait_ethernet_available()
            time.sleep(10)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            check_home_page = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            check_wan_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)

            list_actual5 = [check_home_page, check_wan_assigned]
            list_expected5 = [return_true] *2
            step_5_6_name = "5, 6. Login again. " \
                            "Check Home page is display and Wan IP assigned. "
            list_check_in_step_5_6 = [
                "Home page is appear",
                "Wan IP is assigned"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5, 6. Assertion wong')

        try:
            # Check Network
            wireless_card = driver.find_element_by_css_selector(ele_wireless_card)
            labels = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values = wireless_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'Network Name(SSID)':
                    nw_name_value_2g = v.text
                if l.text == 'Security':
                    nw_security_2g = v.text
                    break
            wireless_card.find_elements_by_css_selector(card_tabs_cls)[1].click()
            wireless_card = driver.find_element_by_css_selector(ele_wireless_card)
            labels = wireless_card.find_elements_by_css_selector(label_name_in_2g)
            values = wireless_card.find_elements_by_css_selector(ele_wrap_input_label)
            for l, v in zip(labels, values):
                if l.text == 'Network Name(SSID)':
                    nw_name_value_5g = v.text
                if l.text == 'Security':
                    nw_security_5g = v.text
                    break

            # CLick Home wan
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            host_nw_block = driver.find_element_by_css_selector(ele_host_network)

            labels = host_nw_block.find_elements_by_css_selector(label_name_in_2g)
            values = host_nw_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Connection status':
                    check_conn_status = v.text
                    break

            list_actual7 = [[nw_name_value_2g, nw_security_2g], [nw_name_value_5g, nw_security_5g], check_conn_status]
            list_expected7 = [[check_network_name_2g, get_security],
                              [check_network_name_5g, get_security],
                              'Connected (5GHz)']
            step_7_name = "7. Check SSID and Security of Wireless 2.4GHz and 5GHz and check connection status. "
            list_check_in_step_7 = [
                f"Check SSID and Security of Wireless 2.4GHz is: {list_expected7[0]}",
                f"Check SSID and Security of Wireless 5GHz is: {list_expected7[1]}"
                f"Check Connection status is: {list_expected7[2]}"
            ]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('7. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            check_repeater_mode = driver.find_element_by_css_selector(ele_repeater_mode_input).is_selected()

            list_actual8 = [check_repeater_mode]
            list_expected8 = [return_true]
            step_8_name = "8. Goto Network > Operation Mode. Check Repeater mode is selected."
            list_check_in_step_8 = ["Check Repeater mode is selected"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('8. Assertion wong')
        try:
            interface_connect_disconnect('Ethernet', 'disable')
            connect_wifi_by_command(check_network_name_2g, THIRD_PARTY_PW_5G)
            time.sleep(5)
            goto_menu(driver, home_tab, 0)

            ip_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google_2 = check_connect_to_google()
            check_youtube_2 = check_connect_to_youtube()
            interface_connect_disconnect('Ethernet', 'enable')

            list_actual9 = [ip_assigned, check_google_2, check_youtube_2]
            list_expected9 = [return_true] * 3
            step_9_name = "9. Connect Wifi. Check IP assigned and can connect to google and youtube."
            list_check_in_step_9 = [
                "Check IP is assigned",
                "Check connect google success",
                "Check connect youtube success",
            ]
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong')
        # disconnect_or_connect_wan(disconnected=False)

        self.assertListEqual(list_step_fail, [])

    def test_39_NETWORK_Network_Operation_Mode_Verification_of_third_party_upper_router_and_extender_connection(self):
        self.key = 'NETWORK_39'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        disconnect_or_connect_wan(disconnected=False)
        factory_dut()


        # ======================================================
        THIRD_PARTY_NAME = get_config('REPEATER', 'third_party_name', input_data_path)
        THIRD_PARTY_PW = get_config('REPEATER', 'third_party_pw', input_data_path)
        THIRD_PARTY_NAME_5G = get_config('REPEATER', 'third_party_name_5g', input_data_path)
        THIRD_PARTY_PW_5G = get_config('REPEATER', 'third_party_pw_5g', input_data_path)
        try:
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Click to Repeater mode
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, icon_loading)
            #
            repeater_card = driver.find_element_by_css_selector(ele_repeater_mode_card)
            check_title = repeater_card.find_element_by_css_selector(ele_card_title).text
            check_description = repeater_card.find_element_by_css_selector(description).text
            check_guide_line = repeater_card.find_element_by_css_selector(ele_guideline).text
            check_btn_refresh = len(repeater_card.find_elements_by_css_selector(ele_btn_refresh)) > 0

            list_column = [i.text for i in driver.find_elements_by_css_selector('thead .col')]

            check_btn_scan = len(repeater_card.find_elements_by_css_selector(ele_manual_scan_btn)) > 0
            check_btn_back = len(repeater_card.find_elements_by_css_selector(ele_back_btn)) > 0
            check_btn_next = len(repeater_card.find_elements_by_css_selector(ele_btn_next)) > 0

            list_actual1 = [check_title,
                            check_description,
                            check_guide_line,
                            check_btn_refresh,
                            list_column,
                            check_btn_scan,
                            check_btn_back,
                            check_btn_next]
            list_expected1 = ['Repeater Mode',
                              exp_repeater_mode_scan_desc,
                              exp_repeater_mode_scan_guide,
                              return_true,
                              ['Network Name(SSID)', 'CH', 'RSSI', 'Security', 'MAC Address', 'Band'],
                              return_true,
                              return_true,
                              return_true]
            step_1_name = "1. Check Repeater Mode page components: " \
                          "Check Title, Description, Guideline, Button Refresh displayed, " \
                          "List column, Button Scan, Back, Next displayed. "
            list_check_in_step_1 = [
                f"Check Title is: {list_expected1[0]}",
                f"Check Description is: {list_expected1[1]}",
                f"Check Guideline is: {list_expected1[2]}",
                "Check Button refresh is appear",
                f"Check List column is: {list_expected1[4]}",
                "Check Butonn Scan is appear",
                f"Check Button Back is appear",
                f"Check Button Next is appear",
            ]
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
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == THIRD_PARTY_NAME:
                    ActionChains(driver).move_to_element(r).perform()
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(THIRD_PARTY_PW).perform()
            time.sleep(1)

            driver.find_element_by_css_selector(ele_apply_highlight).click()

            network_name = driver.find_elements_by_css_selector('.input-wrap input[name="input-field"]')
            check_network_name_2g = network_name[0].get_attribute('value')
            check_network_name_5g = network_name[1].get_attribute('value')
            expected_check_network_name_2g = THIRD_PARTY_NAME+'_Ext2G'
            expected_check_network_name_5g = THIRD_PARTY_NAME+'_Ext5G'
            check_same_pw = driver.find_element_by_css_selector(ele_wizard_check_same_pw_input).is_selected()

            card_wizard = driver.find_elements_by_css_selector(ele_wizard_wl_block)
            check_pw_2g = wireless_check_pw_eye(driver, card_wizard[0], change_pw=False)
            check_pw_5g = wireless_check_pw_eye(driver, card_wizard[1], change_pw=False)

            list_actual2 = [check_network_name_2g, check_network_name_5g, check_same_pw, check_pw_2g, check_pw_5g]
            list_expected2 = [expected_check_network_name_2g,
                              expected_check_network_name_5g,
                              return_true,
                              THIRD_PARTY_PW,
                              THIRD_PARTY_PW]
            step_2_name = "2. Select Third Party Wifi. Input Password. Next. " \
                          "Check popup title. Check Repeater Wifi name of 2G and 5G. " \
                          "Check box Same as 2.4GHz password is checked. " \
                          "Check Password of 2G and 5G same as Host password. "
            list_check_in_step_2 = [
                f"Check Repeater Wifi name of 2G is: {expected_check_network_name_2g}",
                f"Check Repeater Wifi name of 5G is: {expected_check_network_name_5g}",
                "Check Checkbox Same as 2.4GHz password is check",
                f"Check Password of 2G is: {THIRD_PARTY_PW}",
                f"Check Password of 5G is: {THIRD_PARTY_PW}"
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
            list_step_fail.append('2. Assertion wong')

        try:
            # CLick Apply
            driver.find_element_by_css_selector(ele_btn_next).click()
            time.sleep(0.5)
            check_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()

            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)

            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(20)
            wait_ethernet_available()

            list_actual3 = [check_confirm_msg]
            list_expected3 = [exp_repeater_mode_confirm_msg]
            step_3_name = "3. Click Apply. Click OK. Check Confirm message content."
            list_check_in_step_3 = [f"Check Confirm message is: {exp_repeater_mode_confirm_msg}"]
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
            list_step_fail.append('3. Assertion wong')

        try:
            wait_ethernet_available()
            time.sleep(10)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            check_home_page = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            check_wan_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google = check_connect_to_google()

            list_actual5 = [check_home_page, check_wan_assigned, check_google]
            list_expected5 = [return_true] * 3
            step_4_5_name = "4, 5. Login again. " \
                            "Check Home page is display, Wan IP assigned and can connect to google. "
            list_check_in_step_4_5 = [
                "Check Home page is appear",
                "Check Wan IP is assigned",
                "Check Connect to google success"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('4, 5. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Change to Router mode
            driver.find_element_by_css_selector(ele_select_router_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)

            save_config(config_path, 'URL', 'url', 'http://dearmyrouter.net')
            time.sleep(1)
            wait_ethernet_available()

            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            check_change_mode = driver.find_element_by_css_selector(home_connection_description).text

            list_actual7 = [check_change_mode]
            list_expected7 = ['Dynamic IP']
            step_7_name = "7. Change to router mode. Check Change success by check WAN description."
            list_check_in_step_7 = [f"Check WAN description is: {list_expected7[0]}"]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('7. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(5)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            check_title_2 = driver.find_element_by_css_selector(ele_title_page).text

            list_actual8 = [check_title_2]
            list_expected8 = ['Advanced > Operation Mode']
            step_8_name = "8. Goto Network > Operation Mode. Check Title page."
            list_check_in_step_8 = [f"Check wrap title page is: {list_expected8[0]}"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('8. Assertion wong')

        try:
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == THIRD_PARTY_NAME_5G:
                    ActionChains(driver).move_to_element(r).perform()
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(THIRD_PARTY_PW_5G).perform()
            time.sleep(1)

            driver.find_element_by_css_selector(ele_apply_highlight).click()

            network_name = driver.find_elements_by_css_selector('.input-wrap input[name="input-field"]')
            check_network_name_2g_2 = network_name[0].get_attribute('value')
            check_network_name_5g_2 = network_name[1].get_attribute('value')
            expected_check_network_name_2g_2 = THIRD_PARTY_NAME_5G + '_Ext2G'
            expected_check_network_name_5g_2 = THIRD_PARTY_NAME_5G + '_Ext5G'
            check_same_pw_2 = driver.find_element_by_css_selector(ele_wizard_check_same_pw_input).is_selected()

            driver.find_element_by_css_selector(ele_btn_next).click()
            time.sleep(0.5)
            check_confirm_msg_2 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()

            list_actual8 = [check_network_name_2g_2, check_network_name_5g_2, check_same_pw_2, check_confirm_msg_2]
            list_expected8 = [expected_check_network_name_2g_2,
                              expected_check_network_name_5g_2,
                              return_true,
                              exp_repeater_mode_confirm_msg]
            step_8_2_name = "8.2. Select Third Party Wifi. Input Password. Next. " \
                            "Check popup title. Check Repeater Wifi name of 2G and 5G. " \
                            "Check box Same as 2.4GHz password is checked. " \
                            "Click Apply. Check confirm message. Click OK'"
            list_check_in_step_8_2 = [
                f"Check Repeater Wifi name of 2G is: {list_expected8[0]}",
                f"Check Repeater Wifi name of 5G is: {list_expected8[1]}",
                "Check checkbox Same as 2.4GHz password is check",
                f"Check confirm message is: {exp_repeater_mode_confirm_msg}"
            ]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_2_name,
                    list_check_in_step=list_check_in_step_8_2,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_2_name,
                    list_check_in_step=list_check_in_step_8_2,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('8. Assertion wong')

        try:
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)

            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(20)
            wait_ethernet_available()
            connect_wifi_by_command(expected_check_network_name_2g_2, THIRD_PARTY_PW_5G)
            time.sleep(5)
            wait_ethernet_available()
            time.sleep(10)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            check_wan_assigned_2 = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google_2 = check_connect_to_google()

            list_actual9 = [check_wan_assigned_2, check_google_2]
            list_expected9 = [return_true] * 2
            check = assert_list(list_actual9, list_expected9)
            step_9_10_name = "9, 10. Wait until reboot finish. " \
                             "Connect Wifi. Login. Check IP assigned and check connect to Google. "
            list_check_in_step_9_10 = [
                "Check WAN IP is assigned",
                "Check Connect to google success"
            ]
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_10_name,
                    list_check_in_step=list_check_in_step_9_10,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_10_name,
                    list_check_in_step=list_check_in_step_9_10,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('9, 10. Assertion wong')
        disconnect_or_connect_wan(disconnected=False)

        self.assertListEqual(list_step_fail, [])

    def test_40_NETWORK_Network_Operation_Mode_Verification_of_mesh_network_upper_router_and_extender_connection(self):
        self.key = 'NETWORK_40'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        # disconnect_or_connect_wan(disconnected=False)
        # factory_dut()
        # ======================================================
        REPEATER_2G_NAME = get_config('REPEATER', 'repeater_name', input_data_path)
        REPEATER_2G_PW = get_config('REPEATER', 'repeater_pw', input_data_path)
        REPEATER_5G_NAME = get_config('REPEATER', 'repeater_name_5g', input_data_path)
        REPEATER_5G_PW = get_config('REPEATER', 'repeater_pw_5g', input_data_path)
        try:
            wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            # Click start btn
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Click to Repeater mode
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()
            #
            repeater_card = driver.find_element_by_css_selector(ele_repeater_mode_card)
            check_title = repeater_card.find_element_by_css_selector(ele_card_title).text
            check_description = repeater_card.find_element_by_css_selector(description).text
            check_guide_line = repeater_card.find_element_by_css_selector(ele_guideline).text
            check_btn_refresh = len(repeater_card.find_elements_by_css_selector(ele_btn_refresh)) > 0

            list_column = [i.text for i in driver.find_elements_by_css_selector('thead .col')]

            check_btn_scan = len(repeater_card.find_elements_by_css_selector(ele_manual_scan_btn)) > 0
            check_btn_back = len(repeater_card.find_elements_by_css_selector(ele_back_btn)) > 0
            check_btn_next = len(repeater_card.find_elements_by_css_selector(ele_btn_next)) > 0

            list_actual1 = [check_title,
                            check_description,
                            check_guide_line,
                            check_btn_refresh,
                            list_column,
                            check_btn_scan,
                            check_btn_back,
                            check_btn_next]
            list_expected1 = ['Repeater Mode',
                              exp_repeater_mode_scan_desc,
                              exp_repeater_mode_scan_guide,
                              return_true,
                              ['Network Name(SSID)', 'CH', 'RSSI', 'Security', 'MAC Address', 'Band'],
                              return_true,
                              return_true,
                              return_true]
            step_1_name = "1. Check Repeater Mode page components:" \
                          "Check Title, Description, Guideline, Button Refresh displayed, " \
                          "List column, Button Scan, Back, Next displayed. "
            list_check_in_step_1 = [
                f"Check Title is: {list_expected1[0]}",
                f"Check Description is: {list_expected1[1]}",
                f"Check Guideline is: {list_expected1[2]}",
                "Check Button refresh is appear",
                f"Check List column is: {list_expected1[4]}",
                "Check Button Scan is appear",
                f"Check Button Back is appear",
                f"Check Button Next is appear",
            ]
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
            wait_ethernet_available()
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_2G_NAME:
                    ActionChains(driver).move_to_element(r).perform()
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_2G_PW).perform()
            time.sleep(1)

            driver.find_element_by_css_selector(ele_apply_highlight).click()
            time.sleep(1)
            check_confirm_msg_1 = driver.find_element_by_css_selector(confirm_dialog_msg).text

            list_actual2 = [check_confirm_msg_1]
            list_expected2 = [exp_repeater_mode_confirm_msg_2]
            step_2_name = "2. Select Mesh 2G Wifi. Input Password. Next. " \
                          "Check confirm message. "
            list_check_in_step_2 = [f"Check confirm message is: {exp_repeater_mode_confirm_msg_2}"]
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
            list_step_fail.append('2. Assertion wong')

        try:
            driver.find_element_by_css_selector(btn_ok).click()

            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(10)
            wait_ethernet_available()
            wait_ethernet_available()
            time.sleep(10)
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            check_wan_assigned = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)

            list_actual4 = [check_wan_assigned]
            list_expected4 = [return_true]
            step_4_name = "4. Click OK. Re-login. Check IP assgined. "
            list_check_in_step_4 = ["Check WAN IP is assigned"]
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
            list_step_fail.append('4. Assertion wong')

        try:
            check_google = check_connect_to_google()

            list_actual5 = [check_google]
            list_expected5 = [return_true]
            step_5_name = "5. Check can connect to google. "
            list_check_in_step_5 = ["Check Connect to google success"]
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
            list_step_fail.append('5. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Change to Router mode
            driver.find_element_by_css_selector(ele_select_router_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)

            save_config(config_path, 'URL', 'url', 'http://dearmyrouter.net')
            time.sleep(1)
            wait_ethernet_available()
            wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)
            check_change_mode = driver.find_element_by_css_selector(home_connection_description).text

            list_actual6 = [check_change_mode]
            list_expected6 = ['Dynamic IP']
            step_6_name = "6. Change to router mode. Check Change success by check WAN description. "
            list_check_in_step_6 = [f"check WAN description is: {list_expected6[0]}"]
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
            list_step_fail.append('6. Assertion wong')

        try:
            goto_menu(driver, network_tab, network_operationmode_tab)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(ele_select_repeater_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(5)
            wait_popup_disappear(driver, icon_loading)
            time.sleep(1)
            check_title_2 = driver.find_element_by_css_selector(ele_title_page).text

            list_actual7 = [check_title_2]
            list_expected7 = ['Advanced > Operation Mode']
            step_7_name = "7. Goto Network > Operation Mode. Check Title page.'"
            list_check_in_step_7 = [f"Check Wrap Title page is: {list_expected7[0]}"]
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
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7
                )
            )
            list_step_fail.append('7. Assertion wong')

        try:
            time.sleep(5)
            _rows = driver.find_elements_by_css_selector(rows)
            # Choose Network name
            for r in _rows:
                if r.find_element_by_css_selector(ele_network_name).text.strip() == REPEATER_5G_NAME:
                    ActionChains(driver).move_to_element(r).perform()
                    r.click()
                    time.sleep(1)
                    break
            # Fill Password
            pw_box = driver.find_element_by_css_selector(ele_input_pw)
            ActionChains(driver).click(pw_box).send_keys(REPEATER_5G_PW).perform()
            time.sleep(1)

            driver.find_element_by_css_selector(ele_apply_highlight).click()
            time.sleep(1)
            check_confirm_msg_2 = driver.find_element_by_css_selector(confirm_dialog_msg).text

            list_actual8 = [check_confirm_msg_2]
            list_expected8 = [exp_repeater_mode_confirm_msg_2]
            step_8_name = "8. Select Mesh 5G Wifi. Input Password. Next. Check confirm message. "
            list_check_in_step_8 = [f"Check confirm message is: {exp_repeater_mode_confirm_msg_2}"]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8
                )
            )
            list_step_fail.append('8. Assertion wong')

        try:
            driver.find_element_by_css_selector(btn_ok).click()

            time.sleep(100)
            wait_popup_disappear(driver, icon_loading)

            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
            time.sleep(20)
            wait_ethernet_available()
            time.sleep(5)
            wait_ethernet_available()
            connect_wifi_by_command(REPEATER_5G_NAME, REPEATER_5G_PW)
            time.sleep(5)
            wait_ethernet_available()
            time.sleep(10)
            # wait_ethernet_available()
            grand_login(driver)
            wait_popup_disappear(driver, dialog_loading)

            check_wan_assigned_2 = checkIPAddress(driver.find_element_by_css_selector(home_conection_img_wan_ip).text)
            check_google_2 = check_connect_to_google()

            list_actual9 = [check_wan_assigned_2, check_google_2]
            list_expected9 = [return_true] * 2
            step_9_10_name = "9, 10. Wait until reboot finish. " \
                             "Connect Wifi. Login. Check IP assigned and check connect to Google. "
            list_check_in_step_9_10 = [
                "Check WAN IP assigned",
                "Check Connect to google sucess"
            ]
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_10_name,
                    list_check_in_step=list_check_in_step_9_10,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_10_name,
                    list_check_in_step=list_check_in_step_9_10,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('9, 10. Assertion wong')
        # disconnect_or_connect_wan(disconnected=False)

        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
