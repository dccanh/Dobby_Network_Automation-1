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
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            self.driver = webdriver.Chrome(driver_path)  # open chrome
            self.driver.maximize_window()
            self.time_stamp = datetime.now()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        try:
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.time_stamp)
        except:
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            # Connect by wifi if internet is down to handle exception for PPPoE
            os.system('netsh wlan connect ssid=HVNWifi name=HVNWifi')
            time.sleep(1)
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.time_stamp)
            time.sleep(5)
            # Connect by LAN again
            os.system('netsh wlan disconnect')
            time.sleep(1)
        self.driver.quit()

    def test_01_Check_Internet_Status(self):
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

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 3. Check information changed: Dynamic IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check information changed: Dynamic IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

                list_actual = [_check_apply]
                list_expected = [return_true]
                check = assert_list(list_actual, list_expected)
            else:
                check = assert_list([return_true], [return_true])

            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Goto Network>Internet: Change values of Internet Settings: Static IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Goto Network>Internet: Change values of Internet Settings: Static IP '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check information changed: Static IP. ' 
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check information changed: Static IP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
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
                        if o.text == 'PPPoE':
                            o.click()
                            break
                    break
            time.sleep(1)
            internet_setting_fields = internet_setting.find_elements_by_css_selector(wrap_input)
            internet_setting_label = internet_setting.find_elements_by_css_selector(label_name_in_2g)
            for l, f in zip(internet_setting_label, internet_setting_fields):
                # User name
                if l.text == 'User Name':
                    user_box = f.find_element_by_css_selector(input)
                    ActionChains(driver).move_to_element(user_box).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(PPPoE_USER).perform()
                if l.text == 'Password':
                    # pw_box
                    pw_box = f.find_element_by_css_selector(input)
                    ActionChains(driver).move_to_element(pw_box).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(Keys.DELETE).send_keys(PPPoE_PW).perform()
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

                list_actual = [_check_apply]
                list_expected = [return_true]
                check = assert_list(list_actual, list_expected)

            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Goto Network>Internet: Change values of Internet Settings: PPPoE '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Goto Network>Internet: Change values of Internet Settings: PPPoE . '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 7
        try:
            # Login
            grand_login(driver)
            time.sleep(1)
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
            if res_wan_primary['ipv4']['mode'] == 'static':
                _expected[1] = 'Static IP'
            if res_wan_primary['ipv4']['dnsServer2'] == '':
                _expected[-1] = '0.0.0.0'
            time.sleep(5)

            list_actual = [_actual]
            list_expected = [_expected]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Check information changed: PPPoE. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Check information changed: PPPoE. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_02_Check_Dynamic_IP_Operation(self):
        self.key = 'NETWORK_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = url_login = get_config('URL', 'url')
        # filename = '1'
        # commmand = 'factorycfg.sh -a'
        # run_cmd(commmand, filename=filename)
        # # Wait 5 mins for factory
        # time.sleep(150)
        # wait_DUT_activated(url_login)
        # wait_ping('192.168.1.1')
        #
        # filename_2 = 'account.txt'
        # commmand_2 = 'capitest get Device.Users.User.2. leaf'
        # run_cmd(commmand_2, filename_2)
        # time.sleep(3)
        # # Get account information from web server and write to config.txt
        # user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)
        # time.sleep(3)


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

    def test_03_Check_Static_IP_Operation(self):
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
                '[Pass] 1,2,3. Delete DNS server info: Check text This field is required\n')
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
    # OK
    def test_06_Check_Primary_Setting(self):
        self.key = 'NETWORK_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
            time.sleep(1)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

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
                '[Pass] 1,2,3. Verify relate between Primary to Secondary WAN\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Verify relate between Primary to Secondary WAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_07_Check_Secondary_Setting(self):
        self.key = 'NETWORK_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')

        try:
            grand_login(driver)
            time.sleep(1)

            # Enable Dual WAN
            goto_menu(driver, network_tab, network_internet_tab)

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
                '[Pass] 1,2,3. Verify relate between Secondary to Primary WAN\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Verify relate between Secondary to Primary WAN. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_18_LAN_Change_Subnet_Mask(self):
        self.key = 'NETWORK_18'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')

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
                '[Pass] 1. Check Subnet Mask value when Ip Address is class C\n')
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
                '[Pass] 2,3. Check Subnet Mask value when Ip Address is class B and verify en Start/End Ip <16 bits\n')
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
                '[Pass] 4,5,6. Check Subnet Mask value when Ip Address is class A and verify en Start/End Ip <16, 24 bits\n')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4,5,6. Check Subnet Mask value when Ip Address is class A and verify en Start/End Ip <16, 24 bits.'
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '4,5,6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_21_Verify_Start_End_Ip_Address_input_value(self):
        self.key = 'NETWORK_21'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
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

            # 1 Edit Start IP address < End IP address
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
                '[Pass] 1. Set start IP Address < End IP Address: Check Error Message\n')
        except:
            self.list_steps.append(
                f'[Fail] 1. Set start IP Address < End IP Address: Check Error Message. '
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
                '[Pass] 2. Set start IP Address, End IP Address Small: Check Error Message\n')
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
                '[Pass] 3. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message\n')
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
                '[Pass] 4. Set start IP Address, End IP Address Same as Lan IP Address: Check Error Message\n')
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
    def test_25_Reserved_IP_Confirm_duplicate_registration_prevention(self):
        self.key = 'NETWORK_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        MAC_2 = '22:22:22:22:22:22'
        IP_2  = '192.168.1.16'
        MAC_4 = '44:44:44:44:44:44'
        IP_4 = '192.168.1.16'
        MAC_6 = '66:66:66:66:66:66'
        IP_6 = '192.168.1.1'
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
            time.sleep(2)
            error_msg_existed= len(reserved_ip_block.find_elements_by_css_selector(custom_error_cls)) > 0

            time.sleep(3)

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
    def test_26_Verify_Max_entry_Registration(self):
        self.key = 'NETWORK_26'
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
        time.sleep(3)

        MAC_2 = '12:12:12:12:12:12'
        IP_2 = '192.168.1.11'

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
                f'[Pass] 3. Add 32 reserved IP. Check ADD button disabled. Click add -> Check edit form not display. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add 32 reserved IP. Check ADD button disabled. Click add -> Check edit form not display. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_27_Verify_update_Reserved_IP_address_follow_changing_Lan_IP(self):
        self.key = 'NETWORK_27'
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
        time.sleep(3)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        URL_PING_CHECK = '172.16.1.1'
        URL_B = 'http://172.16.1.1'
        EXPECTED_B_IP_ADDR = '172.16.1.10'
        MAC_2 = '88:88:88:88:88:88'
        IP_2 = '192.168.1.10'

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
        time.sleep(3)

        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
