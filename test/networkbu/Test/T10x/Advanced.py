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


class ADVANCED(unittest.TestCase):
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
    # OK F
    def test_08_ADVANCED_Local_Access_and_External_Access_confirmation(self):
        self.key = 'ADVANCED_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = url_login = get_config('URL', 'url')
        URL_LOGIN_HTTPS = URL_LOGIN.replace('http', 'https')
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(150)
        wait_DUT_activated(url_login)
        wait_ping('192.168.1.1')

        filename_2 = 'account.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(4)
        # Get account information from web server and write to config.txt

        user_pw = get_result_command_from_server(url_ip=url_login, filename=filename_2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)
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

            list_actual1 = [local_val, remote_val]
            list_expected1 = [exp_local, exp_remote]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2,3. Disabled Remote and HTTPS Access: Check extra text' 
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Disabled Remote and HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            list_actual2 = [local_val, remote_val]
            list_expected2 = [exp_local, exp_remote]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Enable HTTPS Access: Check extra text'
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Enable HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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

            list_actual3 = [local_val, remote_val]
            list_expected3 = [exp_local, exp_remote]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Disabled Remote and HTTPS Access: Check extra text'
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Disabled Remote and HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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

            list_actual4 = [local_val, remote_val]
            list_expected4 = [exp_local, exp_remote]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Enable Remote Access: Check extra text'
                                   f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Enable Remote Access: Check extra text. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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

            list_actual5 = [local_val, remote_val]
            list_expected5 = [exp_local, exp_remote]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 7. Disabled Remote and HTTPS Access: Check extra text'
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Disabled Remote and HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
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

            list_actual6 = [local_val, remote_val]
            list_expected6 = [exp_local, exp_remote]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 8. Enable Remote, HTTPS Access: Check extra text'
                                   f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 8. Enable Remote, HTTPS Access: Check extra text. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('8. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_26_ADVANCED_Confirm_WOL_Deletion(self):
        self.key = 'ADVANCED_26'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        MAC_VALUE = ['12', '34', '56', '78', 'AB', 'CD']
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)

            # Goto Advanced > WoL
            goto_menu(driver, advanced_tab, advanced_ddnswol_tab)
            wait_popup_disappear(driver, dialog_loading)

            wol_block = driver.find_element_by_css_selector(right)
            # Click Add button to change setting
            wol_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)

            mac_address = wol_block.find_element_by_css_selector(wol_mac_addr)
            mac_address_input = mac_address.find_element_by_css_selector(input)
            mac_address_input.click()

            # Choose in list drop down
            project_options = wol_block.find_elements_by_css_selector(secure_value_in_drop_down)
            choice = random.choice(project_options)
            ActionChains(driver).move_to_element(choice).perform()
            option_value = choice.text
            choice.click()
            if option_value == 'Enter the MAC address':
                mac_address_input = driver.find_element_by_css_selector(input_mac_addr)
                ActionChains(driver).click(mac_address_input).send_keys(''.join(MAC_VALUE)).perform()
                option_value = ':'.join(MAC_VALUE)
            else:
                option_value = option_value.splitlines()[-1]
            # Save
            driver.find_element_by_css_selector(btn_save).click()
            # Verify
            verify_mac_address_input = wol_block.find_element_by_css_selector(wol_mac_addr).text

            list_actual = [verify_mac_address_input]
            list_expected = [option_value]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2,3. Add a Mac address: Check add successfully: {option_value}'
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3.  Add a Mac address: Check add successfully:  {option_value}'
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            ls_rows = wol_block.find_elements_by_css_selector(rows)
            for i in ls_rows:
                if i.find_element_by_css_selector(wol_mac_addr).text == option_value:
                    i.find_element_by_css_selector(delete_wol).click()
                    time.sleep(1)

            # Check not in
            ls_mac = driver.find_elements_by_css_selector(wol_mac_addr)
            ls_mac = [i.text for i in ls_mac]

            check_delete = option_value not in ls_mac

            list_actual2 = [check_delete]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 4. Delete row just added in previous step: {option_value}'
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Delete row just added in previous step: {option_value}'
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_29_ADVANCED_Check_message_for_exception_case_Port_Forwarding(self):
        self.key = 'ADVANCED_29'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        LOCAL_START_END = ['100', '200']
        EXTERNAL_START_END = ['201', '250']
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)

            # Goto Advanced > WoL
            goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Enable DMZ
            dmz_block = driver.find_element_by_css_selector(dmz_card)
            dmz_btn = dmz_block.find_element_by_css_selector(select)
            dmz_input = dmz_btn.find_element_by_css_selector(input)
            if not dmz_input.is_selected():
                dmz_btn.click()
            # Get block again
            dmz_block = driver.find_element_by_css_selector(dmz_card)
            dmz_block.find_element_by_css_selector(edit_cls).click()
            time.sleep(0.2)
            ip_addr_field = dmz_block.find_element_by_css_selector(ip_address_cls)
            ip_addr_input = ip_addr_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(ip_addr_input).click().key_down(Keys.CONTROL).send_keys(
                'a').key_up(Keys.CONTROL).send_keys('1').perform()
            # Save
            driver.find_element_by_css_selector(btn_save).click()
            time.sleep(0.2)
            error_msg = driver.find_element_by_css_selector(custom_error_cls).text
            # click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()

            list_actual1 = [error_msg]
            list_expected1 = [exp_destination_same_lan_ip_error_msg]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1. Enable DMZ, put Destination same as LAN ip address: Check error message.'
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Enable DMZ, put Destination same as LAN ip address: Check error message. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
        try:
            port_forwarding_block = driver.find_element_by_css_selector(port_forwarding_card)
            # Click Add button to change setting
            port_forwarding_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)
            edit_field = port_forwarding_block.find_element_by_css_selector(edit_mode)
            # Fill Service type
            service_type = edit_field.find_element_by_css_selector(service_type_cls)
            service_type.find_element_by_css_selector(input).send_keys('admin')
            # Local Port
            local_port = edit_field.find_element_by_css_selector(local_port_cls)
            local_port_input = local_port.find_elements_by_css_selector(input)
            for i, v in zip(local_port_input, LOCAL_START_END):
                i.clear()
                i.send_keys(v)
            # External Port
            external_port = edit_field.find_element_by_css_selector(external_port_cls)
            external_port_input = external_port.find_elements_by_css_selector(input)
            for i, v in zip(external_port_input, EXTERNAL_START_END):
                i.clear()
                i.send_keys(v)

            port_forwarding_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.5)
            warning_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            # External Port
            external_port = edit_field.find_element_by_css_selector(external_port_cls)
            external_port_input = external_port.find_elements_by_css_selector(input)
            for i, v in zip(external_port_input, LOCAL_START_END):
                i.clear()
                i.send_keys(v)
            port_forwarding_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.5)

            list_actual2 = [warning_msg]
            list_expected2 = [exp_warning_local_port_same_external]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Put External ports different Local ports: Check Warning message'
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Put External ports different Local ports: Check Warning message. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            port_forwarding_block = driver.find_element_by_css_selector(port_forwarding_card)
            # Click Add button to change setting
            port_forwarding_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)
            edit_field = port_forwarding_block.find_element_by_css_selector(edit_mode)
            # Fill Service type
            service_type = edit_field.find_element_by_css_selector(service_type_cls)
            service_type.find_element_by_css_selector(input).send_keys('admin')
            # Local Port
            local_port = edit_field.find_element_by_css_selector(local_port_cls)
            local_port_input = local_port.find_elements_by_css_selector(input)
            for i, v in zip(local_port_input, LOCAL_START_END):
                i.clear()
                i.send_keys(v)
            # External Port
            external_port = edit_field.find_element_by_css_selector(external_port_cls)
            external_port_input = external_port.find_elements_by_css_selector(input)
            for i, v in zip(external_port_input, LOCAL_START_END):
                i.clear()
                i.send_keys(v)

            port_forwarding_block.find_element_by_css_selector(btn_save).click()
            time.sleep(0.5)
            warning_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)

            list_actual3 = [warning_msg]
            list_expected3 = [exp_add_local_external_port_exist]
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 3. Put Local/External ports same as previous rule: Check Warning message'
                                   f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Put Local/External ports same as previous rule: Check Warning message. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    # # Chưa implement Check forwarding from the external network PC
    # def test_30_Verify_Port_Forwarding_Correction(self):
    #     self.key = 'ADVANCED_30'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #
    #     URL_LOGIN = get_config('URL', 'url')
    #     SERVICE_TEST = 'admin'
    #     IP_ADDRESS_TEST = '192.168.1.3'
    #     IP_ADDRESS_SPLIT = IP_ADDRESS_TEST.split('.')[-1]
    #     START_END_1 = '100 - 200'
    #     START_END_1_SPLIT = START_END_1.split(' - ')
    #     START_END_2 = '201 - 250'
    #     START_END_2_SPLIT = START_END_2.split(' - ')
    #     PROTOCOL_TYPE = 'TCP'
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     try:
    #         # Login
    #         login(driver)
    #         wait_popup_disappear(driver, dialog_loading)
    #         if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
    #             driver.get(URL_LOGIN + homepage)
    #             wait_popup_disappear(driver, dialog_loading)
    #
    #         # Goto Advanced > WoL
    #         goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         port_forwarding_block = driver.find_element_by_css_selector(port_forwarding_card)
    #         # Click Add button to change setting
    #         port_forwarding_block.find_element_by_css_selector(add_class).click()
    #         time.sleep(1)
    #         edit_field = port_forwarding_block.find_element_by_css_selector(edit_mode)
    #         # Fill Service type
    #         service_type = edit_field.find_element_by_css_selector(service_type_cls)
    #         service_type.find_element_by_css_selector(input).send_keys(SERVICE_TEST)
    #         # IP address
    #         ip_address = edit_field.find_element_by_css_selector(ip_address_col_cls)
    #         ip_address_box = ip_address.find_element_by_css_selector(input)
    #         ActionChains(driver).move_to_element(ip_address_box).click().key_down(Keys.CONTROL+'a').\
    #             key_up(Keys.CONTROL).send_keys(IP_ADDRESS_SPLIT).perform()
    #         # Local Port
    #         local_port = edit_field.find_element_by_css_selector(local_port_cls)
    #         local_port_input = local_port.find_elements_by_css_selector(input)
    #         for i, v in zip(local_port_input, START_END_1_SPLIT):
    #             i.clear()
    #             i.send_keys(v)
    #         # External Port
    #         external_port = edit_field.find_element_by_css_selector(external_port_cls)
    #         external_port_input = external_port.find_elements_by_css_selector(input)
    #         for i, v in zip(external_port_input, START_END_1_SPLIT):
    #             i.clear()
    #             i.send_keys(v)
    #         # Protocol
    #         protocol_box = edit_field.find_element_by_css_selector(protocol_col_cls)
    #         protocol_box.find_element_by_css_selector(option_select).click()
    #         time.sleep(0.2)
    #         ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
    #         for o in ls_option:
    #             if o.text == PROTOCOL_TYPE:
    #                 o.click()
    #                 time.sleep(1)
    #                 break
    #
    #         port_forwarding_block.find_element_by_css_selector(btn_save).click()
    #         time.sleep(0.5)
    #         # Apply
    #         port_forwarding_block.find_element_by_css_selector(apply).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(1)
    #         # Verify Last row information
    #         rows_info = port_forwarding_block.find_elements_by_css_selector(rows)[-1]
    #         act_service_type = rows_info.find_element_by_css_selector(service_type_cls).text
    #         act_ip_address = rows_info.find_element_by_css_selector(ip_address_col_cls).text
    #         act_local_port = rows_info.find_element_by_css_selector(local_port_cls).text
    #         act_external_port = rows_info.find_element_by_css_selector(external_port_cls).text
    #         act_protocol = rows_info.find_element_by_css_selector(protocol_col_cls).text
    #
    #         list_actual = [act_service_type, act_ip_address, act_local_port, act_external_port, act_protocol]
    #         list_expected = [SERVICE_TEST, IP_ADDRESS_TEST, START_END_1, START_END_1, PROTOCOL_TYPE]
    #         check = assert_list(list_actual, list_expected)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             '[Pass] 1. Add rule successfully: Check Added information.')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1. Add rule successfully: Check Added information. '
    #             f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
    #         list_step_fail.append(
    #             '1. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
    #     try:
    #         # Edit
    #         rows_info.find_element_by_css_selector(edit_cls).click()
    #         time.sleep(1)
    #         edit_field = port_forwarding_block.find_element_by_css_selector(edit_mode)
    #         # Local Port
    #         local_port = edit_field.find_element_by_css_selector(local_port_cls)
    #         local_port_input = local_port.find_elements_by_css_selector(input)
    #         for i, v in zip(local_port_input, START_END_2_SPLIT):
    #             ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL + 'a'). \
    #                 key_up(Keys.CONTROL).send_keys(v).perform()
    #         # External Port
    #         external_port = edit_field.find_element_by_css_selector(external_port_cls)
    #         external_port_input = external_port.find_elements_by_css_selector(input)
    #         for i, v in zip(external_port_input, START_END_2_SPLIT):
    #             ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL + 'a'). \
    #                 key_up(Keys.CONTROL).send_keys(v).perform()
    #         # Save
    #         port_forwarding_block.find_element_by_css_selector(btn_save).click()
    #         # Apply
    #         port_forwarding_block.find_element_by_css_selector(apply).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(1)
    #         # Verify
    #         rows_info = port_forwarding_block.find_elements_by_css_selector(rows)[-1]
    #         act_local_port = rows_info.find_element_by_css_selector(local_port_cls).text
    #         act_external_port = rows_info.find_element_by_css_selector(external_port_cls).text
    #
    #         list_actual = [act_local_port, act_external_port]
    #         list_expected = [START_END_2, START_END_2]
    #         check = assert_list(list_actual, list_expected)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 2. Put External ports different Local ports: Check Warning message')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2. Put External ports different Local ports: Check Warning message. '
    #             f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
    #         list_step_fail.append('2. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
    #     try:
    #
    #         list_actual = []
    #         list_expected = []
    #         check = assert_list(list_actual, list_expected)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append('[Pass] 3. Put Local/External ports same as previous rule: Check Warning message')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 3. Put Local/External ports same as previous rule: Check Warning message. '
    #             f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('3. Assertion wong.')
    #     self.assertListEqual(list_step_fail, [])
    # OK
    def test_31_ADVANCED_Confirm_Port_Forwarding_Delete(self):
        self.key = 'ADVANCED_31'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        SERVICE_TEST = 'admin'
        IP_ADDRESS_TEST = '192.168.1.3'
        IP_ADDRESS_SPLIT = IP_ADDRESS_TEST.split('.')[-1]
        START_END_1 = '100 - 200'
        START_END_1_SPLIT = START_END_1.split(' - ')
        START_END_2 = '201 - 250'
        START_END_2_SPLIT = START_END_2.split(' - ')
        PROTOCOL_TYPE = 'TCP'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)


            # Goto Advanced > WoL
            goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
            wait_popup_disappear(driver, dialog_loading)

            port_forwarding_block = driver.find_element_by_css_selector(port_forwarding_card)
            if len(port_forwarding_block.find_elements_by_css_selector(rows)) == 0:
                # Click Add button to change setting
                port_forwarding_block.find_element_by_css_selector(add_class).click()
                time.sleep(1)
                edit_field = port_forwarding_block.find_element_by_css_selector(edit_mode)
                # Fill Service type
                service_type = edit_field.find_element_by_css_selector(service_type_cls)
                service_type.find_element_by_css_selector(input).send_keys(SERVICE_TEST)
                # IP address
                ip_address = edit_field.find_element_by_css_selector(ip_address_col_cls)
                ip_address_box = ip_address.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(ip_address_box).click().key_down(Keys.CONTROL+'a').\
                    key_up(Keys.CONTROL).send_keys(IP_ADDRESS_SPLIT).perform()
                # Local Port
                local_port = edit_field.find_element_by_css_selector(local_port_cls)
                local_port_input = local_port.find_elements_by_css_selector(input)
                for i, v in zip(local_port_input, START_END_1_SPLIT):
                    i.clear()
                    i.send_keys(v)
                # External Port
                external_port = edit_field.find_element_by_css_selector(external_port_cls)
                external_port_input = external_port.find_elements_by_css_selector(input)
                for i, v in zip(external_port_input, START_END_1_SPLIT):
                    i.clear()
                    i.send_keys(v)
                # Protocol
                protocol_box = edit_field.find_element_by_css_selector(protocol_col_cls)
                protocol_box.find_element_by_css_selector(option_select).click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == PROTOCOL_TYPE:
                        o.click()
                        time.sleep(1)
                        break

                port_forwarding_block.find_element_by_css_selector(btn_save).click()
                time.sleep(0.5)
                # Apply
                port_forwarding_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            list_rows = port_forwarding_block.find_elements_by_css_selector(rows)
            before_delete = len(list_rows)
            random_rows = random.choice(list_rows)
            # Verify Last row information
            act_service_type = random_rows.find_element_by_css_selector(service_type_cls).text
            act_ip_address = random_rows.find_element_by_css_selector(ip_address_col_cls).text
            act_local_port = random_rows.find_element_by_css_selector(local_port_cls).text
            act_external_port = random_rows.find_element_by_css_selector(external_port_cls).text
            act_protocol = random_rows.find_element_by_css_selector(protocol_col_cls).text

            random_rows.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            after_delete = len(port_forwarding_block.find_elements_by_css_selector(rows))
            list_actual = [before_delete-1]
            list_expected = [after_delete]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Delete rule successfully.'
                                   f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1. Delete rule successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_35_ADVANCED_Edit_Confirm_Delete_Port_Triggering(self):
        self.key = 'ADVANCED_35'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        SERVICE_TEST = 'Description'
        IP_ADDRESS_TEST = '192.168.1.3'
        IP_ADDRESS_SPLIT = IP_ADDRESS_TEST.split('.')[-1]
        START_END_1 = '100-200'
        START_END_1_SPLIT = START_END_1.split('-')
        START_END_2 = '201-250'
        START_END_2_SPLIT = START_END_2.split('-')
        PROTOCOL_TYPE = 'TCP'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)

            # Goto Advanced > port triggering
            goto_menu(driver, advanced_tab, advanced_porttriggering_tab)
            wait_popup_disappear(driver, dialog_loading)

            port_triggering_block = driver.find_element_by_css_selector(port_triggering_card)
            if len(port_triggering_block.find_elements_by_css_selector(rows)) == 0:
                # Click Add button to change setting
                port_triggering_block.find_element_by_css_selector(add_class).click()
                time.sleep(1)
                edit_field = port_triggering_block.find_element_by_css_selector(edit_mode)
                # Fill Description
                description_col = edit_field.find_element_by_css_selector(description_col_cls)
                description_col.find_element_by_css_selector(input).send_keys(SERVICE_TEST)
                # Trigger range
                triggered_range = edit_field.find_element_by_css_selector(triggered_col_cls)
                triggered_range_input = triggered_range.find_elements_by_css_selector(input)
                for i, v in zip(triggered_range_input, START_END_1_SPLIT):
                    ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL + 'a'). \
                        key_up(Keys.CONTROL).send_keys(v).perform()
                # External Port
                forwarded_range = edit_field.find_element_by_css_selector(forwarded_col_cls)
                forwarded_range_input = forwarded_range.find_elements_by_css_selector(input)
                for i, v in zip(forwarded_range_input, START_END_1_SPLIT):
                    ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL + 'a'). \
                        key_up(Keys.CONTROL).send_keys(v).perform()
                # Protocol 1
                protocol_box_trigger = edit_field.find_elements_by_css_selector(protocol_col_cls)[0]
                protocol_box_trigger.find_element_by_css_selector(option_select).click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == PROTOCOL_TYPE:
                        o.click()
                        time.sleep(1)
                        break
                # Protocol 2
                protocol_box_forward = edit_field.find_elements_by_css_selector(protocol_col_cls)[1]
                protocol_box_forward.find_element_by_css_selector(option_select).click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == PROTOCOL_TYPE:
                        o.click()
                        time.sleep(1)
                        break

                port_triggering_block.find_element_by_css_selector(btn_save).click()
                time.sleep(0.5)
                # Apply
                port_triggering_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            list_rows = port_triggering_block.find_elements_by_css_selector(rows)
            random_rows = random.choice(list_rows)
            # Edit
            random_rows.find_element_by_css_selector(edit_cls).click()
            time.sleep(1)
            edit_field = port_triggering_block.find_element_by_css_selector(edit_mode)
            # Trigger range
            triggered_range = edit_field.find_element_by_css_selector(triggered_col_cls)
            triggered_range_input = triggered_range.find_elements_by_css_selector(input)
            for i, v in zip(triggered_range_input, START_END_2_SPLIT):
                ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL + 'a'). \
                    key_up(Keys.CONTROL).send_keys(v).perform()
            # External Port
            forwarded_range = edit_field.find_element_by_css_selector(forwarded_col_cls)
            forwarded_range_input = forwarded_range.find_elements_by_css_selector(input)
            for i, v in zip(forwarded_range_input, START_END_2_SPLIT):
                ActionChains(driver).move_to_element(i).click().key_down(Keys.CONTROL + 'a'). \
                    key_up(Keys.CONTROL).send_keys(v).perform()
            # Save
            port_triggering_block.find_element_by_css_selector(btn_save).click()
            # Apply
            port_triggering_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            # Verify
            rows_info = port_triggering_block.find_elements_by_css_selector(rows)[-1]

            act_triggered_range = rows_info.find_element_by_css_selector(triggered_col_cls).text
            act_forwarded_range = rows_info.find_element_by_css_selector(forwarded_col_cls).text

            list_actual = [act_triggered_range, act_forwarded_range]
            list_expected = [START_END_2]*2
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Delete rule successfully.'
                                   f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1. Delete rule successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_36_ADVANCED_Confirm_Delete_Port_Triggering(self):
        self.key = 'ADVANCED_36'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        SERVICE_TEST = 'Description'
        IP_ADDRESS_TEST = '192.168.1.3'
        IP_ADDRESS_SPLIT = IP_ADDRESS_TEST.split('.')[-1]
        START_END_1 = '100 - 200'
        START_END_1_SPLIT = START_END_1.split(' - ')
        START_END_2 = '201 - 250'
        START_END_2_SPLIT = START_END_2.split(' - ')
        PROTOCOL_TYPE = 'TCP'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)

            # Goto Advanced > port triggering
            goto_menu(driver, advanced_tab, advanced_porttriggering_tab)
            wait_popup_disappear(driver, dialog_loading)

            port_triggering_block = driver.find_element_by_css_selector(port_triggering_card)
            if len(port_triggering_block.find_elements_by_css_selector(rows)) == 0:
                # Click Add button to change setting
                port_triggering_block.find_element_by_css_selector(add_class).click()
                time.sleep(1)
                edit_field = port_triggering_block.find_element_by_css_selector(edit_mode)
                # Fill Description
                description_col = edit_field.find_element_by_css_selector(description_col_cls)
                description_col.find_element_by_css_selector(input).send_keys(SERVICE_TEST)
                # Trigger range
                triggered_range = edit_field.find_element_by_css_selector(triggered_col_cls)
                triggered_range_input = triggered_range.find_elements_by_css_selector(input)
                for i, v in zip(triggered_range_input, START_END_1_SPLIT):
                    i.clear()
                    i.send_keys(v)
                # External Port
                forwarded_range = edit_field.find_element_by_css_selector(forwarded_col_cls)
                forwarded_range_input = forwarded_range.find_elements_by_css_selector(input)
                for i, v in zip(forwarded_range_input, START_END_1_SPLIT):
                    i.clear()
                    i.send_keys(v)
                # Protocol 1
                protocol_box_trigger = edit_field.find_elements_by_css_selector(protocol_col_cls)[0]
                protocol_box_trigger.find_element_by_css_selector(option_select).click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == PROTOCOL_TYPE:
                        o.click()
                        time.sleep(1)
                        break
                # Protocol 2
                protocol_box_forward = edit_field.find_elements_by_css_selector(protocol_col_cls)[1]
                protocol_box_forward.find_element_by_css_selector(option_select).click()
                time.sleep(0.2)
                ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                for o in ls_option:
                    if o.text == PROTOCOL_TYPE:
                        o.click()
                        time.sleep(1)
                        break

                port_triggering_block.find_element_by_css_selector(btn_save).click()
                time.sleep(0.5)
                # Apply
                port_triggering_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            list_rows = port_triggering_block.find_elements_by_css_selector(rows)
            before_delete = len(list_rows)
            random_rows = random.choice(list_rows)

            random_rows.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            after_delete = len(port_triggering_block.find_elements_by_css_selector(rows))
            list_actual = [before_delete-1]
            list_expected = [after_delete]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Delete rule successfully.'
                                   f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1. Delete rule successfully. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append(
                '1. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_47_ADVANCED_Check_Ping_test_operation(self):
        self.key = 'ADVANCED_47'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        UTILITY_TYPE = 'Ping Test'
        PING_TARGET = '192.168.1.1'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)

            # Goto Advanced > port triggering
            goto_menu(driver, advanced_tab, advanced_diagnostics_tab)
            wait_popup_disappear(driver, dialog_loading)
            diagnostic_block = driver.find_element_by_css_selector(diagnostic_card)

            diag_label = diagnostic_block.find_elements_by_css_selector(label_name_in_2g)
            diag_fields = diagnostic_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(diag_label, diag_fields):
                if l.text == 'Utility':
                    f.click()
                    time.sleep(0.2)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == UTILITY_TYPE:
                            o.click()
                            time.sleep(1)
                            break
                elif l.text == 'Target':
                    f.click()
                    ActionChains(driver).send_keys(PING_TARGET).perform()
                elif l.text == 'Ping Size':
                    ping_size = f.find_element_by_css_selector(input).get_attribute('value')
                elif l.text == 'Ping Count':
                    ping_count = f.find_element_by_css_selector(input).get_attribute('value')
                elif l.text == 'Ping Interval':
                    ping_interval = f.find_element_by_css_selector(input).get_attribute('value')
                    break
            diagnostic_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            get_result = driver.find_element_by_css_selector(diagnostic_result).get_attribute('value')
            assert_result = '\n\n'.join([i.split('time')[0] for i in get_result.splitlines() if i != ''])

            result = f"PING {PING_TARGET} ({PING_TARGET}) {ping_size}({str(int(ping_size)+28)}) bytes of data.\n\n"
            for s in range(1, int(ping_count)+1):
                result += f"{str(int(ping_size)+8)} bytes from {PING_TARGET}: icmp_req={str(s)} ttl=64 \n\n"
            result += f"--- {PING_TARGET} ping statistics ---\n\n"
            result += f"{ping_count} packets transmitted, {ping_count} received, 0% packet loss, "

            list_actual1 = [assert_result]
            list_expected1 = [result]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Test result format of Ping test.'
                                   f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Test result format of Ping test. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.find_element_by_css_selector(clear_btn).click()
            time.sleep(0.5)
            clear_result = driver.find_element_by_css_selector(diagnostic_result).get_attribute('value')

            list_actual2 = [clear_result]
            list_expected2 = [exp_none_text]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Clear button: Check delete successfully.'
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Clear button: Check delete successfully. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_48_ADVANCED_Check_Traceroute_operation(self):
        self.key = 'ADVANCED_48'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        UTILITY_TYPE = 'Traceroute'
        PING_TARGET = '192.168.1.1'
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Login
            grand_login(driver)

            # Goto Advanced > port triggering
            goto_menu(driver, advanced_tab, advanced_diagnostics_tab)
            wait_popup_disappear(driver, dialog_loading)
            diagnostic_block = driver.find_element_by_css_selector(diagnostic_card)

            diag_label = diagnostic_block.find_elements_by_css_selector(label_name_in_2g)
            diag_fields = diagnostic_block.find_elements_by_css_selector(wrap_input)
            for l, f in zip(diag_label, diag_fields):
                if l.text == 'Utility':
                    f.click()
                    time.sleep(0.2)
                    ls_option = driver.find_elements_by_css_selector(active_drop_down_values)
                    for o in ls_option:
                        if o.text == UTILITY_TYPE:
                            o.click()
                            time.sleep(1)
                            break
                elif l.text == 'Target':
                    f.click()
                    ActionChains(driver).send_keys(PING_TARGET).perform()
                elif l.text == 'Traceroute Maximum TTL':
                    trace_max = f.find_element_by_css_selector(input).get_attribute('value')
                    break
            diagnostic_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            get_result = driver.find_element_by_css_selector(diagnostic_result).get_attribute('value')
            assert_result = '\n\n'.join([i.split(f"({PING_TARGET})  ")[0] for i in get_result.splitlines() if i != ''])

            result = f"traceroute to {PING_TARGET} ({PING_TARGET}), {trace_max} hops max, 38 byte packets\n\n"
            result += f" 1  dearmyrouter.net "

            list_actual2 = [assert_result]
            list_expected2 = [result]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 1. Test result format of Traceroute.'
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Test result format of Traceroute. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(1)
            driver.find_element_by_css_selector(clear_btn).click()
            time.sleep(0.5)
            clear_result = driver.find_element_by_css_selector(diagnostic_result).get_attribute('value')

            list_actual2 = [clear_result]
            list_expected2 = [exp_none_text]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 2. Clear button: Check delete successfully.'
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Clear button: Check delete successfully. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
