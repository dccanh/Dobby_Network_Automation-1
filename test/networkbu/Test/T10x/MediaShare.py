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


class MEDIASHARE(unittest.TestCase):
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
        save_duration_time(test_case_key=type(self).__name__,
                           test_case_name=self.def_name,
                           test_case_steps=self.list_steps,
                           start_time=self.start_time)
        self.driver.quit()

    def test_02_MS_Check_USB_connection(self):
        self.key = 'MEDIA_SHARE_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        # ========================================================================

        try:
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            time.sleep(3)
            wait_popup_disappear(driver, dialog_loading)

            usb_title_text = driver.find_element_by_css_selector(ele_usb_title).text
            usb_sub_title_text = driver.find_element_by_css_selector(ele_sub_title).text
            list_usb_block_title = [i.text for i in driver.find_elements_by_css_selector(ele_usb_mediashare_block_title)]

            ls_row = driver.find_elements_by_css_selector(rows)
            web_list_usb = list()
            for row in ls_row:
                id = row.find_element_by_css_selector(ele_index_cls).text
                name = row.find_element_by_css_selector(name_cls).text
                dict_usb = {'id': int(id), "name": name}
                web_list_usb.append(dict_usb)
            # API
            URL_API = get_config('URL', 'url') + '/api/v1/mediashare/usb'
            _METHOD = 'GET'
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _BODY = ''
            _TOKEN = get_token(_USER, _PW)
            _res = call_api(URL_API, _METHOD, _BODY, _TOKEN)

            api_list_usb = list()
            for u in _res['usbs']:
                dict_usb = {'id': u['id'], "name": u['name']}
                api_list_usb.append(dict_usb)

            list_actual3 = [usb_title_text, usb_sub_title_text, list_usb_block_title, web_list_usb]
            list_expected3 = ['Media Share > USB', exp_subtitle_ms_usb,
                              ['Connected USB', 'Network Folder', 'Account Settings'], api_list_usb]
            check = assert_list(list_actual3, list_expected3)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     '[Pass] 3. Check title, subtitle, list block title, api of return of id and name. '
            #     f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            step_1_2_3_name = '''1. Access and login Web UI\n2. Go to Wireless -> Media Share -> USB\n3. Check output page information'''
            list_check_in_step_1_2_3 = ['Check page title',
                                        'Check sub title',
                                        'Check list block title',
                                        'Check api of return of id and name']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_3_name,
                    list_check_in_step=list_check_in_step_1_2_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_04_MS_Confirmation_Network_Folder_Creation(self):
        self.key = 'MEDIA_SHARE_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================
        DESCRIPTION_3 = get_config('MEDIA_SHARE', 'ms04_desc_3', input_data_path)
        DESCRIPTION_4 = get_config('MEDIA_SHARE', 'ms04_desc_4', input_data_path)
        PATH_FILE_1 = get_config('MEDIA_SHARE', 'ms04_file_1', input_data_path)
        PATH_FILE_2 = get_config('MEDIA_SHARE', 'ms04_file_2', input_data_path)
        LS_PATH_FILE = [
            get_config('MEDIA_SHARE', 'ms04_file_3', input_data_path),
            get_config('MEDIA_SHARE', 'ms04_file_4', input_data_path),
            get_config('MEDIA_SHARE', 'ms04_file_5', input_data_path),
            get_config('MEDIA_SHARE', 'ms04_file_6', input_data_path),
            get_config('MEDIA_SHARE', 'ms04_file_7', input_data_path),
            get_config('MEDIA_SHARE', 'ms04_file_8', input_data_path)
        ]

        try:
            grand_login(driver)
            time.sleep(5)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            time.sleep(3)
            wait_popup_disappear(driver, dialog_loading)

            # Network block
            network_block = driver.find_element_by_css_selector(usb_network)

            network_table = network_block.find_elements_by_css_selector(tbody)
            if len(network_table) == 0:
                before_add = 0
            else:
                # Remove all
                num_rule = len(network_block.find_elements_by_css_selector(tbody))
                for r in range(num_rule):
                    network_table[0].find_element_by_css_selector(action_delete).click()
                    time.sleep(0.2)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(0.5)
                before_add = 0

            # Click Add 1
            network_block.find_element_by_css_selector(add_class).click()
            time.sleep(0.2)

            # Edit mode
            edit_field = network_block.find_element_by_css_selector(edit_mode)

            # Description
            description_field = edit_field.find_element_by_css_selector(description)
            description_field.find_element_by_css_selector(input).send_keys(DESCRIPTION_3)

            # Folder path
            path_field = edit_field.find_element_by_css_selector(path)
            path_field.find_element_by_css_selector(input).click()
            time.sleep(0.5)
            # Choose path
            driver.find_element_by_css_selector(tree_icon).click()
            time.sleep(0.2)

            ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
            for o in ls_path_lv1:
                if o.text == PATH_FILE_1:
                    ActionChains(driver).move_to_element(o).click().perform()
                    break

            # OK
            driver.find_element_by_css_selector(btn_ok).click()

            # Permission
            per_write = edit_field.find_element_by_css_selector(permission_write_check_box)
            if not per_write.is_selected():
                driver.find_element_by_css_selector(permission_write_check_box_radio).click()

            # Save
            driver.find_element_by_css_selector(btn_save).click()

            # Check quantity of record
            after_add = len(network_block.find_elements_by_css_selector(tbody))
            # after_add = len(network_table.find_elements_by_css_selector(table_row))

            # Before + 1 = After
            list_actual1 = [before_add+1]
            list_expected1 = [after_add]
            check = assert_list(list_actual1, list_expected1)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     '[Pass] 1,2,3. Check Add NW folder successfully: Quantity before and after. '
            #     f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            step_1_2_3_name = '''1. Access and login Web UI\n
                            2. Go to Wireless -> Media Share -> USB\n
                            3. Click the Add button in Network Folder and change below settings:
                            - Description: 123!@ abcd #^&*
                            - Select an any folder on USB
                            - Permission: Write/Read
                            click Save'''
            list_check_in_step_1_2_3 = ['Check number before and after Add']
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
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Click Add 1
            network_block.find_element_by_css_selector(add_class).click()
            # Edit mode
            edit_field = network_block.find_element_by_css_selector(edit_mode)

            # Description
            description_field = edit_field.find_element_by_css_selector(description)
            description_field.find_element_by_css_selector(input).send_keys(DESCRIPTION_4)

            # Folder path
            path_field = edit_field.find_element_by_css_selector(path)
            path_field.find_element_by_css_selector(input).click()
            time.sleep(0.5)
            # Choose path
            driver.find_element_by_css_selector(tree_icon).click()
            time.sleep(0.2)

            ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
            for o in ls_path_lv1:
                if o.text == PATH_FILE_1:
                    ActionChains(driver).move_to_element(o).click().perform()
                    break
            # OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            err_msg = network_block.find_element_by_css_selector(error_message).text
            list_actual2 = [err_msg]
            list_expected2 = [exp_nw_folder_exist]
            check = assert_list(list_actual2, list_expected2)
            # self.assertTrue(check["result"])
            # self.list_steps.append('[Pass] 4. Change same network folder: Check error message. '
            #                        f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            step_4_name = '''4. Click the Add button in Network Folder and change below settings:
            - Description: 123!@ abcd
            - Select a folder on USB is as same as the step 3'''
            list_check_in_step_4 = ['Check error message']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            # Edit mode
            edit_field = network_block.find_element_by_css_selector(edit_mode)

            # Folder path
            path_field = edit_field.find_element_by_css_selector(path)
            path_field.find_element_by_css_selector(input).click()
            time.sleep(0.5)
            # Choose path
            driver.find_element_by_css_selector(tree_icon).click()
            time.sleep(0.2)

            ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
            for o in ls_path_lv1:
                if o.text == PATH_FILE_2:
                    ActionChains(driver).move_to_element(o).click().perform()
                    break
            # OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            # Permission
            per_read = edit_field.find_element_by_css_selector(permission_read_check_box)
            if not per_read.is_selected():
                driver.find_element_by_css_selector(permission_read_check_box_radio).click()

            # Save
            driver.find_element_by_css_selector(btn_save).click()

            # Check quantity of record
            after_add_2 = len(network_block.find_elements_by_css_selector(tbody))
            # after_add_2 = len(network_table.find_elements_by_css_selector(table_row))

            list_actual3 = [after_add + 1]
            list_expected3 = [after_add_2]
            check = assert_list(list_actual3, list_expected3)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 5. Check Add NW folder successfully: Quantity before and after. '
            #     f'Actual: {str(list_actual34)}. Expected: {str(list_expected34)}')
            step_5_name = '''5. Change below settings:
                - Select a different folder on USB 
                - Permission: Read
                and click Save'''
            list_check_in_step_5 = ['Check number before and after Add']
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
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            for i in range(6):
                # Click Add 1
                network_block.find_element_by_css_selector(add_class).click()
                # Edit mode
                edit_field = network_block.find_element_by_css_selector(edit_mode)
                # Description

                description_field = edit_field.find_element_by_css_selector(description)
                description_field.find_element_by_css_selector(input).send_keys(str(i))
                # Folder path
                path_field = edit_field.find_element_by_css_selector(path)
                path_field.find_element_by_css_selector(input).click()
                time.sleep(0.5)
                # Choose path
                driver.find_element_by_css_selector(tree_icon).click()
                time.sleep(0.2)

                ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
                for o in ls_path_lv1:
                    if o.text == LS_PATH_FILE[i]:
                        ActionChains(driver).move_to_element(o).click().perform()
                        break
                # OK
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

                if i <= 2:
                    # Permission: 3 READ
                    per_read = edit_field.find_element_by_css_selector(permission_read_check_box)
                    if not per_read.is_selected():
                        driver.find_element_by_css_selector(permission_read_check_box_radio).click()
                else:
                    # Permission: 3 WRITE
                    per_write = edit_field.find_element_by_css_selector(permission_write_check_box)
                    if not per_write.is_selected():
                        driver.find_element_by_css_selector(permission_write_check_box_radio).click()

                # Save
                driver.find_element_by_css_selector(btn_save).click()

            add_btn_disabled = network_block.find_element_by_css_selector(add_class).get_property('disabled')

            # Apply
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Check quantity of record
            after_add_final = len(network_block.find_elements_by_css_selector(tbody))


            list_actual4 = [add_btn_disabled, after_add_final]
            list_expected4 = [return_true, exp_max_row_usb_nw]
            check = assert_list(list_actual4, list_expected4)

            step_6_name = '''6. Add more 3 share folder rules with Read permission and 3 share folder rules with Write/Read permission
            and apply setting'''
            list_check_in_step_6 = ['Check Add button is disabled',
                                    'Check number of network folder rule = max rules']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_05_MS_Edit_Delete_Network_Folder(self):
        self.key = 'MEDIA_SHARE_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===================================================================
        PATH_FILE_9 = get_config('MEDIA_SHARE', 'ms04_file_9', input_data_path)
        fake = Faker()
        DESCRIPTION_4 = get_config('MEDIA_SHARE', 'ms04_desc_4', input_data_path)
        PATH_FILE_1 = get_config('MEDIA_SHARE', 'ms04_file_1', input_data_path)
        USB_PAGE_TITLE = "Media Share > USB"
        try:
            grand_login(driver)
            time.sleep(5)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            # wait_popup_disappear(driver, dialog_loading)
            is_dialog_loading_disappear = wait_popup_disappear(driver, dialog_loading)
            is_correct_page_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual0 = [is_correct_page_title]
            list_expected0 = [USB_PAGE_TITLE]
            check = assert_list(list_actual0, list_expected0)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 1, 2. Login. Goto USB page. '
            #     f'Check Dialog loading is disappeared after login.'
            #     f'Check title USB page:'
            #     f'Actual: {str(list_actual0)}.'
            #     f'Expected: {str(list_expected0)}.'
            # )
            step_1_2_name = '''1. Access and login Web UI\n2. Go to Wireless -> Media Share -> USB'''
            list_check_in_step_1_2 = ['Check page title']
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
            list_step_fail.append('1,2. Assertion wong.')

        try:
            # Network block
            network_block = driver.find_element_by_css_selector(usb_network)
            # Before delete
            network_table = network_block.find_elements_by_css_selector(tbody)
            if len(network_table) == 0:
                network_block.find_element_by_css_selector(add_class).click()
                # Edit mode
                edit_field = network_block.find_element_by_css_selector(edit_mode)

                # Description
                description_field = edit_field.find_element_by_css_selector(description)
                description_field.find_element_by_css_selector(input).send_keys(DESCRIPTION_4)

                # Folder path
                path_field = edit_field.find_element_by_css_selector(path)
                path_field.find_element_by_css_selector(input).click()
                time.sleep(0.5)
                # Choose path
                driver.find_element_by_css_selector(tree_icon).click()
                time.sleep(0.2)

                ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
                for o in ls_path_lv1:
                    if o.text == PATH_FILE_1:
                        ActionChains(driver).move_to_element(o).click().perform()
                        break
                # OK
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
                driver.find_element_by_css_selector(btn_save).click()
                time.sleep(1)
                driver.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                before_delete = 1

            else:
                before_delete = len(network_block.find_elements_by_css_selector(tbody))
            # Ke thua tu Media share 04
            network_table = network_block.find_elements_by_css_selector(tbody)
            # Get first row> Click edit
            network_table[0].find_element_by_css_selector(action_edit).click()
            time.sleep(0.5)
            # Edit mode
            edit_field = network_block.find_element_by_css_selector(edit_mode)

            # Description
            fake_name = fake.name()
            description_field = edit_field.find_element_by_css_selector(description)
            desc_value = description_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(desc_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(fake_name).perform()

            # Folder path
            path_field = edit_field.find_element_by_css_selector(path)
            path_field.find_element_by_css_selector(input).click()
            time.sleep(0.5)
            # Choose path
            driver.find_element_by_css_selector(tree_icon).click()
            time.sleep(0.2)

            ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
            for o in ls_path_lv1:
                if o.text == PATH_FILE_9:
                    ActionChains(driver).move_to_element(o).click().perform()
                    break
            # OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            # Permission
            per_write = edit_field.find_element_by_css_selector(permission_write_check_box_first_row)
            permission_status_before = per_write.is_selected()
            if permission_status_before:
                driver.find_element_by_css_selector(permission_read_check_box_radio_first_row).click()
            else:
                driver.find_element_by_css_selector(permission_write_check_box_radio_first_row).click()
            # Save
            driver.find_element_by_css_selector(btn_save).click()
            time.sleep(2)
            # Apply
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            # Get value
            desc_check = network_table[0].find_element_by_css_selector(description).text
            path_check = network_table[0].find_element_by_css_selector(path).text.split('/')[-1]
            time.sleep(0.5)
            per_write_first_row_check = len(network_table[0].find_elements_by_css_selector(permission_write_check_box_first_row)) > 0

            list_actual1 = [desc_check, path_check, permission_status_before]
            list_expected1 = [fake_name, PATH_FILE_9, not(per_write_first_row_check)]
            check = assert_list(list_actual1, list_expected1)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 3,4. Check edit NW folder successfully: Result same as configuration. '
            #     f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            step_3_4_name = '''3. Click the Edit button and change below settings:
                - Description: change to a new value
                - Select an other folder on USB
                - Permission: change to a new value (Write/Read or Read)
                and click Save 
                4. Click the Apply button'''
            list_check_in_step_3_4 = ['Check Description text',
                                      'Check folder path',
                                      'Check Read permision of status is check']
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
            list_step_fail.append('3,4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Get first row> Click delete
            network_table[0].find_element_by_css_selector(action_delete).click()
            time.sleep(2)

            # OK
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            after_delete = len(network_block.find_elements_by_css_selector(tbody))

            list_actual2 = [before_delete - 1]
            list_expected2 = [after_delete]
            check = assert_list(list_actual2, list_expected2)
            # self.assertTrue(check["result"])
            # self.list_steps.append(f'[Pass] 5. Delete a rule: Check quantity decrease 1. '
            #                        f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            step_5_name = '''5. Click the Delete button and click OK'''
            list_check_in_step_5 = ['Check number rule decrease 1']
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
    def test_06_MS_Edit_Delete_Network_Folder_while_server_is_running(self):
        self.key = 'MEDIA_SHARE_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        ACCOUNT_FTP = 'Anonymous'
        SERVER_FTP = "FTP"
        EXPECTED_SERVER_SETTING_PAGE_TITLE = "Media Share > Server Settings"
        try:
            grand_login(driver)
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)
            network_block = driver.find_element_by_css_selector(usb_network)
            network_table = network_block.find_elements_by_css_selector(tbody)
            if len(network_table) == 0:
                DESCRIPTION_3 = 'Test01'
                PATH_FILE_1 = get_config('MEDIA_SHARE', 'ms04_file_1', input_data_path)
                add_a_usb_network_folder(driver, DESCRIPTION_3, PATH_FILE_1, WRITE=True)


            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            # wait_popup_disappear(driver, dialog_loading)
            is_dialog_loading_disappear = wait_popup_disappear(driver, dialog_loading)
            is_correct_page_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual0 = [is_correct_page_title]
            list_expected0 = [EXPECTED_SERVER_SETTING_PAGE_TITLE]
            check = assert_list(list_actual0, list_expected0)

            step_1_2_name = '''1. Access and login Web UI\n2. Go to Wireless -> Media Share -> Server Settings'''
            list_check_in_step_1_2 = ['Check title page']
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
            list_step_fail.append('1,2. Assertion wong.')

        try:
            # Enable FTP server
            server_ftp = driver.find_element_by_css_selector(ftp_server)
            server_ftp_btn = server_ftp.find_element_by_css_selector(select)
            server_ftp_input = server_ftp_btn.find_element_by_css_selector(input)
            # If FTP is not enable => Enable
            if not server_ftp_input.is_selected():
                server_ftp_btn.click()
            time.sleep(0.2)

            media_fields = server_ftp.find_elements_by_css_selector(media_item)
            # Account
            media_fields[0].find_element_by_css_selector(input).click()
            time.sleep(1)
            ls_account = media_fields[0].find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_account:
                if o.text == ACCOUNT_FTP:
                    o.click()
                    break

            # Network folder
            media_fields[1].find_element_by_css_selector(input).click()
            time.sleep(1)
            ls_folder = media_fields[1].find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            choice = random.choice(ls_folder)
            option_value = choice.text
            time.sleep(0.5)
            choice.click()

            # Apply
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Check and verify value
            account_value = media_fields[0].find_element_by_css_selector(input).get_attribute('value')
            nw_folder_value = media_fields[1].find_element_by_css_selector(input).get_attribute('value')

            list_actual1 = [account_value, nw_folder_value]
            list_expected1 = [ACCOUNT_FTP, option_value]
            check = assert_list(list_actual1, list_expected1)

            step_3_name = '''3. Enable FTP server and change below settings:
                - Account: Anonymous
                - Network Folder: choose a network folder
                and Apply setting'''
            list_check_in_step_3 = ['Check Account value',
                                    'Check network folder value']
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
            list_step_fail.append(
                '3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Network block
            network_block = driver.find_element_by_css_selector(usb_network)
            # Before delete
            network_table = network_block.find_elements_by_css_selector(tbody)

            for r in network_table:
                if r.find_element_by_css_selector(description).text == nw_folder_value:
                    check_folder_status = r.find_element_by_css_selector(status).text
                    break

            list_actual2 = [check_folder_status]
            list_expected2 = [SERVER_FTP]
            check = assert_list(list_actual2, list_expected2)

            step_4_name = '''4. Go to Wireless -> Media Share -> USB'''
            list_check_in_step_4 = ['Check status of network folder should be FTP']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            for r in network_table:
                if r.find_element_by_css_selector(description).text == nw_folder_value:
                    r.find_element_by_css_selector(action_edit).click()
            time.sleep(0.5)
            # Check content of pop up
            confirm_msg_edit = driver.find_element_by_css_selector(complete_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            # Verify

            list_actual3 = [confirm_msg_edit]
            list_expected3 = [exp_confirm_msg_edit]
            check = assert_list(list_actual3, list_expected3)

            step_5_name = '''5. Click the Edit button of the network folder in step 3'''
            list_check_in_step_5 = ['Check content of confirm message']
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
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            # Get first row> Click delete
            time.sleep(1)
            for r in network_table:
                if r.find_element_by_css_selector(description).text == nw_folder_value:
                    folder_path_delete = r.find_element_by_css_selector(path).text
                    r.find_element_by_css_selector(action_delete).click()

            time.sleep(1)
            confirm_msg_delete = driver.find_element_by_css_selector(confirm_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            network_table = network_block.find_elements_by_css_selector(tbody)
            total_path = []
            for r in network_table:
                total_path.append(r.find_element_by_css_selector(path).text)
            # True if folder not in total folder => delete sucessfully
            check_delete = True if folder_path_delete not in total_path else False

            list_actual4 = [confirm_msg_delete, check_delete]
            list_expected4 = [exp_confirm_msg_delete, return_true]
            check = assert_list(list_actual4, list_expected4)

            step_6_name = '''6. Click the Delete button of the network folder in step 3 and click OK'''
            list_check_in_step_6 = ['Delete a rule: Check pop-up content',
                                    'Check folder path not in total path: deleted']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_11_MS_Check_message_when_creating_server_without_network_folder_account(self):
        self.key = 'MEDIA_SHARE_11'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================

        try:
            grand_login(driver)
            time.sleep(2)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)


            # Network Folder
            network_block = driver.find_element_by_css_selector(usb_network)
            ActionChains(driver).move_to_element(network_block).perform()
            network_table = network_block.find_elements_by_css_selector(tbody)
            if len(network_table) > 0:
                for r in range(len(network_table)):
                    network_table[0].find_element_by_css_selector(action_delete).click()
                    time.sleep(0.2)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(0.5)
            # Account block
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)
            ActionChains(driver).move_to_element(account_setting_block).perform()
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            if len(ls_account) > 0:
                for r in range(len(ls_account)):
                    ls_account[0].find_element_by_css_selector(delete_cls).click()
                    time.sleep(0.2)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(0.5)

            # Goto Sever setting
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            is_correct_page_title = driver.find_element_by_css_selector(ele_title_page).text
            list_actual0 = [is_correct_page_title]
            list_expected0 = ['Media Share > Server Settings']
            check = assert_list(list_actual0, list_expected0)
            step_0_name = '''1. Access and login Web UI\n2. Go to Wireless -> Media Share -> Server Settings'''
            list_check_in_step_0 = ['Check title page']
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
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Prepare done precondition

        try:


            exp_account_and_folder_msg = [exp_server_account_warning, exp_server_folder_warning]
            exp_account_msg = [exp_server_account_warning]
            exp_folder_msg = [exp_server_folder_warning]
            ls_card = [{"locator": ftp_server, "messages": exp_account_and_folder_msg},
                       {"locator": samba_server_card, "messages": exp_account_and_folder_msg},
                       {"locator": dlna_server_card, "messages": exp_folder_msg},
                       {"locator": dev_dav_server_card, "messages": exp_account_and_folder_msg},
                       {"locator": torrent_server_card, "messages": exp_account_msg},
                       {"locator": time_machine_server_card, "messages": exp_account_and_folder_msg}]

            _check_warning_msg = []
            for i in ls_card:

                server = driver.find_element_by_css_selector(i["locator"])
                ActionChains(driver).move_to_element(server).perform()
                server_btn = server.find_element_by_css_selector(select)
                server_input = server_btn.find_element_by_css_selector(input)
                if not server_input.is_selected():
                    server_btn.click()

                list_warnings = server.find_elements_by_css_selector(account_link_cls)
                list_warnings_text = [warning.text for warning in list_warnings]
                _check_warning_msg.append(i["messages"] == list_warnings_text)


            list_actual = _check_warning_msg
            list_expected = [return_true]*6
            check = assert_list(list_actual, list_expected)

            step_45678_name = '''3. Enable FTP Server\n
            4. Enable Samba Server\n
            5. Enable DLNA Server\n
            6. Enable WebDAV Server\n
            7. Enable Torrent Server\n
            8. Enable Time Machine Server\n'''
            list_check_in_step_45678 = [
                'Check Message server account and network folder are not available of FTP is displayed',
                'Check Message server account and network folder are not available of Samba is displayed',
                'Check Message server account and network folder are not available of DLNA is displayed',
                'Check Message server account and network folder are not available of WebDAV is displayed',
                'Check Message server account and network folder are not available of Torrent is displayed',
                'Check Message server account and network folder are not available of Time machine is displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_45678_name,
                    list_check_in_step=list_check_in_step_45678,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_45678_name,
                    list_check_in_step=list_check_in_step_45678,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('45678. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_08_MS_Create_account_for_file_sharing(self):
        self.key = 'MEDIA_SHARE_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        TEST_STRING_ID = 'Test01!'
        TEST_STRING = get_config('MEDIA_SHARE', 'ms08_test_string', input_data_path)
        KEY_WORDS = ['admin', 'Admin', 'root', 'Anonymous']
        ID_1 = '01234567890123456789012345678901'
        ID_2 = '012345678901234567890123456789012'
        PASSWORD_1 = '01234567890123456789012345678901'
        PASSWORD_2 = '012345678901234567890123456789012'
        LIST_ACCOUNT_ADD = [['Test02!', 'abc2'], ['Test03!', 'abc3'], ['Test04!', 'abc4'], ['Test05!', 'abc5']]
        try:
            grand_login(driver)
            time.sleep(2)

            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Media Share > USB']
            check = assert_list(list_actual1, list_expected1)
            step_1_name = '''1. Access and login Web UI\n2. Go to Media Share > USB > Account Settings'''
            list_check_in_step_1 = ['Check title page']
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
            list_step_fail.append('1, 2. Assertion wrong.')


        try:
            # Network block
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)
            while len(account_setting_block.find_elements_by_css_selector(delete_cls)) > 0:
                account_setting_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Click Add 1
            account_setting_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)

            check_id_holder = account_setting_block.find_element_by_css_selector('.id input').get_attribute(
                'placeholder')
            check_pw_holder = account_setting_block.find_element_by_css_selector('.password input').get_attribute(
                'placeholder')

            list_actual3 = [check_id_holder, check_pw_holder]
            list_expected3 = ['Enter the ID', 'Enter the Password']
            check = assert_list(list_actual3, list_expected3)
            step_3_name = '''3. Click "+ADD" button to add account.'''
            list_check_in_step_3 = ['Check ID placeholder',
                                    'Check Password placeholder']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3))
            list_step_fail.append('3. Assertion wrong.')

        try:
            # Edit mode
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)
            time.sleep(1)
            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL+'a').key_up(
                Keys.CONTROL).send_keys(ID_1).perform()
            time.sleep(2)

            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_1).perform()
            # Verify

            id_account_1 = edit_field.find_element_by_css_selector('.id input').get_attribute('value')
            time.sleep(3)
            pw_eye = edit_field.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye)
            time.sleep(2)
            pw_account_1 = edit_field.find_element_by_css_selector('.password input').get_attribute('value')
            time.sleep(1)
            act.release(pw_eye)
            act.perform()
            # ===================================================================================
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)
            time.sleep(1)
            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL + 'a').key_up(
                Keys.CONTROL).send_keys(ID_2).perform()
            time.sleep(2)

            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(PASSWORD_2).perform()
            # Verify

            id_account_2 = edit_field.find_element_by_css_selector('.id input').get_attribute('value')
            time.sleep(3)
            pw_eye = edit_field.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye)
            time.sleep(2)
            pw_account_2 = edit_field.find_element_by_css_selector('.password input').get_attribute('value')
            time.sleep(1)
            act.release(pw_eye)
            act.perform()

            list_actual4 = [[id_account_1, pw_account_1], [id_account_2, pw_account_2]]
            list_expected4 = [[ID_1[:32], PASSWORD_1[:32]], [ID_2[:32], PASSWORD_2[:32]]]
            check = assert_list(list_actual4, list_expected4)
            step_4_name = '''4. Check max length of ID and Password can be inputed
                - Enter 32 characters into ID field.
                - Enter 33 characters into ID field
                - Enter 32 characters into Password field.
                - Enter 33 characters into Password field'''
            list_check_in_step_4 = ['Check max length ID and Password account 1',
                                    'Check max length ID and Password account 2']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4))
            list_step_fail.append('4. Assertion wrong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Edit mode
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING_ID).perform()
            time.sleep(1)
            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING).perform()
            time.sleep(0.5)

            account_setting_block.find_element_by_css_selector(btn_save).click()
            time.sleep(1)
            account_setting_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()

            # ================================================
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            verify_just_created_rows = ls_account[-1]
            id_account_3 = verify_just_created_rows.find_element_by_css_selector(id_cls).text
            time.sleep(3)
            pw_eye = verify_just_created_rows.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye)
            time.sleep(2)
            pw_account_3 = verify_just_created_rows.find_elements_by_css_selector(input_pw)[-1].get_attribute('value')
            time.sleep(1)
            act.release(pw_eye)
            act.perform()

            list_actual5 = [id_account_3, pw_account_3]
            list_expected5 = [TEST_STRING_ID, TEST_STRING]
            check = assert_list(list_actual5, list_expected5)

            step_5_name = '''5. Enter ID and Password then click on "Save" button
                            - ID/Password with number (0-9), letters (a-z, A-Z) and special characters is valid.
                            - Click "Apply" button then click "OK" button'''
            list_check_in_step_5 = ['Check ID account 1',
                                    'Check Password account 2']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5))
            list_step_fail.append('5. Assertion wong.')

        try:
            # Click Add 1
            account_setting_block.find_element_by_css_selector(add_class).click()
            time.sleep(0.2)

            # Edit mode
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING_ID).perform()
            time.sleep(1)
            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING).perform()
            time.sleep(0.5)
            error_msg_1 = account_setting_block.find_element_by_css_selector(error_message).text

            time.sleep(1)
            # Click Cancel
            account_setting_block.find_element_by_css_selector(btn_cancel).click()

            list_actual6 = [error_msg_1]
            list_expected6 = [exp_account_id_exist]
            check = assert_list(list_actual6, list_expected6)

            step_6_name = '''6. Add new account with same ID of existed account'''
            list_check_in_step_6 = ['Check Message “The same ID exists.” is displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6))
            list_step_fail.append('6. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            account_setting_block.find_element_by_css_selector(add_class).click()
            time.sleep(0.2)

            # Edit mode
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING).perform()
            time.sleep(0.2)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(Keys.DELETE).perform()
            time.sleep(1)
            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING).perform()
            time.sleep(0.5)
            error_msg_2 = account_setting_block.find_element_by_css_selector(error_message).text

            time.sleep(1)
            # Click Cancel
            account_setting_block.find_element_by_css_selector(btn_cancel).click()

            list_actual7 = [error_msg_2]
            list_expected7 = [exp_account_null_id]
            check = assert_list(list_actual7, list_expected7)

            step_7_name = '''7. Add new account with empty ID field by erased ID before. '''
            list_check_in_step_7 = ['Check Message  “This field is required" displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_7_name,
                    list_check_in_step=list_check_in_step_7,
                    list_actual=list_actual7,
                    list_expected=list_expected7))
            list_step_fail.append('7. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 8
        try:
            account_setting_block.find_element_by_css_selector(add_class).click()
            time.sleep(0.2)

            # Edit mode
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            check_key_words = []
            for k in KEY_WORDS:
                ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(k).perform()
                time.sleep(0.2)
                password_field = edit_field.find_element_by_css_selector(password_cls)
                password_value = password_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(str(1)).perform()
                time.sleep(0.2)
                error_msg_3 = account_setting_block.find_element_by_css_selector(error_message).text
                ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(Keys.DELETE).perform()
                time.sleep(0.2)
                check_key_words.append(error_msg_3 == exp_account_not_available)

            time.sleep(0.5)
            check_key_words = all(check_key_words)

            time.sleep(1)
            # Click Cancel
            account_setting_block.find_element_by_css_selector(btn_cancel).click()

            list_actual8 = [check_key_words]
            list_expected8 = [return_true]
            check = assert_list(list_actual8, list_expected8)

            step_8_name = '''8. Add new account with ID "admin" or "ADmin" or "root" or "Anonymous" '''
            list_check_in_step_8 = ['Check error msg key words not available']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_8_name,
                    list_check_in_step=list_check_in_step_8,
                    list_actual=list_actual8,
                    list_expected=list_expected8))
            list_step_fail.append('8. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            # ls_account = len(account_setting_block.find_elements_by_css_selector(rows))
            for i in LIST_ACCOUNT_ADD:
                # Click Add 1
                account_setting_block.find_element_by_css_selector(add_class).click()
                time.sleep(0.2)

                # Edit mode
                edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

                id_field = edit_field.find_element_by_css_selector(id_cls)
                id_value = id_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(i[0]).perform()
                time.sleep(0.2)

                password_field = edit_field.find_element_by_css_selector(password_cls)
                password_value = password_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys(
                    'a').key_up(Keys.CONTROL).send_keys(i[1]).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_save).click()
                time.sleep(0.2)
            ls_account = len(account_setting_block.find_elements_by_css_selector(rows))

            list_actual9 = [ls_account]
            list_expected9 = [5]
            check = assert_list(list_actual9, list_expected9)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 9. Add max rule: Check max rule. '
            #     f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
            step_9_name = '''9. Check max rule is added '''
            list_check_in_step_9 = ['Check Max rule account is added up to 5. ']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9))
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9))
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_09_MS_Edit_Delete_account(self):
        self.key = 'MEDIA_SHARE_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        TEST_STRING = str(random.randint(10, 100))
        TEST_STRING_EDIT = str(random.randint(1, 10))
        EDIT_ID = 'Test06!'
        EDIT_PW = 'abc12345'
        try:
            grand_login(driver)
            time.sleep(2)

            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            time.sleep(2)
            wait_popup_disappear(driver, dialog_loading)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Media Share > USB']
            check = assert_list(list_actual1, list_expected1)

            step_1_name = '''1. Access and login Web UI\n2. Go to Media Share > USB '''
            list_check_in_step_1 = ['Check title page']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1))
            list_step_fail.append('1, 2. Assertion wrong.')

        try:
            time.sleep(5)
            # Network block
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)

            ls_account = len(account_setting_block.find_elements_by_css_selector(rows))
            if ls_account == 0:
                # Click Add 1
                account_setting_block.find_element_by_css_selector(add_class).click()
                time.sleep(0.2)
                # Edit mode
                edit_field = account_setting_block.find_element_by_css_selector(edit_mode)
                time.sleep(1)
                id_field = edit_field.find_element_by_css_selector(id_cls)
                id_value = id_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(TEST_STRING).perform()
                time.sleep(1)
                password_field = edit_field.find_element_by_css_selector(password_cls)
                password_value = password_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(TEST_STRING).perform()
                time.sleep(2)
                driver.find_element_by_css_selector(btn_save).click()
                time.sleep(1)
                account_setting_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(0.4)

            # Verify
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            random_account = random.choice(ls_account)
            old_id_account = random_account.find_element_by_css_selector(id_cls).text
            index_chosen = [i.find_element_by_css_selector(id_cls).text for i in ls_account].index(old_id_account)

            # Click Edit
            random_account.find_element_by_css_selector(edit_cls).click()
            time.sleep(0.5)
            edit_field = driver.find_element_by_css_selector(edit_mode)
            # Change ID, PW
            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(EDIT_PW).perform()
            time.sleep(1)
            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(EDIT_ID).perform()

            account_setting_block.find_element_by_css_selector(btn_save).click()
            time.sleep(1)
            if account_setting_block.find_element_by_css_selector(apply).is_displayed():
                account_setting_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            verify_id_account = ls_account[index_chosen].find_element_by_css_selector(id_cls).text

            pw_eye = ls_account[index_chosen].find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye)
            time.sleep(1)
            verify_pw_account = ls_account[index_chosen].find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye)
            act.perform()

            list_actual3 = [verify_id_account, verify_pw_account]
            list_expected3 = [EDIT_ID, EDIT_PW]
            check = assert_list(list_actual3, list_expected3)

            step_3_name = '''3. Click "Edit" button on existed account, edit to new ID/ Password then click "Save" button
                    - Click "Apply" button to apply it '''
            list_check_in_step_3 = ['Check ID account',
                                    'Check password account']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual3,
                    list_expected=list_expected3))
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
        try:
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            # Click Edit
            ls_account[index_chosen].find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            check_confirm_msg_1 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            check_popup_close = len(driver.find_elements_by_css_selector(content)) == 0
            check_usb_page = len(driver.find_elements_by_css_selector(usb_class)) > 0

            list_actual4 = [check_confirm_msg_1, check_popup_close, check_usb_page]
            list_expected4 = ['Do you want to delete this item?', True, True]
            check = assert_list(list_actual4, list_expected4)
            step_4_name = '''4. Click "Delete" button on existed account.
                    - Click "Cancel" button '''
            list_check_in_step_4 = ['Click "Delete". Check Confirm message',
                                    'Check Popup disappear',
                                    'Check USB page is displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4))
            list_step_fail.append('4. Assertion wong.')

        try:
            ls_account[index_chosen].find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            check_confirm_msg_2 = driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver,dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            ls_account_id = [i.find_element_by_css_selector(id_cls).text for i in ls_account]
            check_delete = verify_id_account not in ls_account_id

            list_actual5 = [check_confirm_msg_2, check_delete]
            list_expected5 = ['Do you want to delete this item?', True]
            check = assert_list(list_actual5, list_expected5)

            step_5_name = '''5. Click "Delete" button on existed account.
                    - Click "OK" button on confirmation message.
                    - Click "OK" button then check account list'''
            list_check_in_step_5 = ['Click "Delete". Check Confirm message',
                                    'Check the rule is deleted']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5))
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5))
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_10_MS_Edit_Delete_account_while_server_is_running(self):
        self.key = 'MEDIA_SHARE_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        TEST_STRING = str(random.randint(10, 100))
        TEST_STRING_EDIT = str(random.randint(1, 10))

        DESCRIPTION_3 = get_config('MEDIA_SHARE', 'ms10_desc_3', input_data_path)
        PATH_FILE_1 = get_config('MEDIA_SHARE', 'ms04_file_1', input_data_path)
        fake = Faker()
        # Pre-pare precondition
        try:
            grand_login(driver)
            time.sleep(2)

            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Network Folder
            network_block = driver.find_element_by_css_selector(usb_network)

            network_table = network_block.find_elements_by_css_selector(tbody)
            if len(network_table) == 0:
                add_a_usb_network_folder(driver, DESCRIPTION_3, PATH_FILE_1, WRITE=True)
            #     # Click Add 1
            #     network_block.find_element_by_css_selector(add_class).click()
            #     time.sleep(0.2)
            #     # Edit mode
            #     edit_field = network_block.find_element_by_css_selector(edit_mode)
            #     # Description
            #     description_field = edit_field.find_element_by_css_selector(description)
            #     description_field.find_element_by_css_selector(input).send_keys(DESCRIPTION_3)
            #     # Folder path
            #     path_field = edit_field.find_element_by_css_selector(path)
            #     path_field.find_element_by_css_selector(input).click()
            #     time.sleep(0.5)
            #     # Choose path
            #     driver.find_element_by_css_selector(tree_icon).click()
            #     time.sleep(0.2)
            #     ls_path_lv1 = driver.find_elements_by_css_selector(path_name_lv1)
            #     for o in ls_path_lv1:
            #         if o.text == PATH_FILE_1:
            #             ActionChains(driver).move_to_element(o).click().perform()
            #             break
            #     # OK
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     # Permission
            #     per_write = edit_field.find_element_by_css_selector(permission_write_check_box)
            #     if not per_write.is_selected():
            #         driver.find_element_by_css_selector(permission_write_check_box_radio).click()
            #     # Save
            #     driver.find_element_by_css_selector(btn_save).click()
            #     wait_popup_disappear(driver, dialog_loading)
            #     driver.find_element_by_css_selector(apply).click()
            #     wait_popup_disappear(driver, dialog_loading)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)
            # time.sleep(1)
            # Account block
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)

            ls_account = len(account_setting_block.find_elements_by_css_selector(rows))
            if ls_account == 0:
                add_a_usb_account_setting(driver, 'Test06!', 'abc12345')
                # Click Add 1
                # account_setting_block.find_element_by_css_selector(add_class).click()
                # time.sleep(0.2)
                # # Edit mode
                # edit_field = account_setting_block.find_element_by_css_selector(edit_mode)
                # time.sleep(1)
                # id_field = edit_field.find_element_by_css_selector(id_cls)
                # id_value = id_field.find_element_by_css_selector(input)
                # ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                #     Keys.CONTROL).send_keys('Test06!').perform()
                # time.sleep(1)
                # password_field = edit_field.find_element_by_css_selector(password_cls)
                # password_value = password_field.find_element_by_css_selector(input)
                # ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                #     Keys.CONTROL).send_keys('abc12345').perform()
                # time.sleep(2)
                # driver.find_element_by_css_selector(btn_save).click()
                # time.sleep(1)
                # account_setting_block.find_element_by_css_selector(apply).click()
                # wait_popup_disappear(driver, dialog_loading)
                # driver.find_element_by_css_selector(btn_ok).click()
                # time.sleep(0.4)

            # Verify
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            random_account = random.choice(ls_account)
            id_account = random_account.find_element_by_css_selector(id_cls).text

            # Enable server
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Enable FTP server
            server_ftp = driver.find_element_by_css_selector(ftp_server)
            server_ftp_btn = server_ftp.find_element_by_css_selector(select)
            server_ftp_input = server_ftp_btn.find_element_by_css_selector(input)
            # If FTP is not enable => Enable
            if not server_ftp_input.is_selected():
                server_ftp_btn.click()
            time.sleep(0.2)
            # Server Account
            server_ftp = driver.find_element_by_css_selector(ftp_server)
            input_label = server_ftp.find_elements_by_css_selector(' '.join([media_item, label]))
            input_value = server_ftp.find_elements_by_css_selector(' '.join([media_item, wrap_input]))
            for l, v in zip(input_label, input_value):
                if l.text == 'Account':
                    v.find_element_by_css_selector(input).click()
                    time.sleep(0.3)
                    ls_account_drop = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.3)
                    for o in ls_account_drop:
                        if o.text == id_account:
                            o.click()
                            break
                if l.text == 'Network Folder':
                    v.find_element_by_css_selector(input).click()
                    time.sleep(0.3)
                    ls_folder = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.3)
                    choice = random.choice(ls_folder)
                    time.sleep(0.3)
                    choice.click()
                    break
            # Apply
            if server_ftp.find_element_by_css_selector(apply).is_displayed() is True:
                server_ftp.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)

            # Enable Windows Network Samba
            server_samba = driver.find_element_by_css_selector(samba_server_card)
            server_samba_btn = server_samba.find_element_by_css_selector(select)
            server_samba_input = server_samba_btn.find_element_by_css_selector(input)
            # If  not enable => Enable
            if not server_samba_input.is_selected():
                server_samba_btn.click()
            time.sleep(0.2)
            # Server Account
            server_samba = driver.find_element_by_css_selector(samba_server_card)
            input_label = server_samba.find_elements_by_css_selector(label)
            input_value = server_samba.find_elements_by_css_selector(wrap_input)
            for l, v in zip(input_label, input_value):
                if l.text == 'Connection Name':
                    v.find_element_by_css_selector(input).send_keys(fake.name())
                if l.text == 'Account':
                    v.find_element_by_css_selector(input).click()
                    time.sleep(0.3)
                    ls_account_drop = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.3)
                    for o in ls_account_drop:
                        if o.text == id_account:
                            o.click()
                            break
                if l.text == 'Network Folder':
                    v.find_element_by_css_selector(input).click()
                    time.sleep(0.3)
                    ls_folder = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.3)
                    choice = random.choice(ls_folder)
                    time.sleep(0.3)
                    choice.click()
                    time.sleep(0.3)
                    break
            # Apply
            if server_samba.find_element_by_css_selector(apply).is_displayed() is True:
                server_samba.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)

            self.list_steps.append(
                '[Pass] Precondition: Existed an account that is using in server (exp: FPT server/ Samba)')
        except:
            self.list_steps.append(
                '[Fail] Precondition: Existed an account that is using in server (exp: FPT server/ Samba)')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Prepare done precondition
        try:
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.3)
            driver.refresh()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Verify
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)
            ActionChains(driver).move_to_element(account_setting_block).perform()
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            random_account = random.choice(ls_account)

            # Click Edit
            random_account.find_element_by_css_selector(edit_cls).click()
            time.sleep(0.3)

            if len(driver.find_elements_by_css_selector(complete_dialog_msg)) > 0:
                edit_confirm_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
                time.sleep(0.3)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.3)

            # Click Delete
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            random_account = random.choice(ls_account)
            time.sleep(0.3)
            random_account.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)

            if len(driver.find_elements_by_css_selector(confirm_dialog_msg)) > 0:
                delete_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
                time.sleep(0.3)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.2)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(0.3)

            list_actual1 = [edit_confirm_msg, delete_confirm_msg]
            list_expected1 = [exp_confirm_msg_edit, exp_delete_account_when_server_running]
            check = assert_list(list_actual1, list_expected1)

            step_1_name = '''1. Click Edit button on existed account. \n2. Click Delete button on existed account. '''
            list_check_in_step_1 = ['Check Edit confirm message',
                                    'Check Delete confirm message']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1))
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual1,
                    list_expected=list_expected1))
            list_step_fail.append('1, 2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
        try:
            # Goto Sever setting
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)

            server_ftp = driver.find_element_by_css_selector(ftp_server)
            ftp_account_enable = server_ftp.find_element_by_css_selector(ele_toggle_input).is_selected()

            server_samba = driver.find_element_by_css_selector(samba_server_card)
            samba_account_enable = server_samba.find_element_by_css_selector(ele_toggle_input).is_selected()

            list_actual2 = [ftp_account_enable, samba_account_enable]
            list_expected2 = [return_false]*2
            check = assert_list(list_actual2, list_expected2)

            step_3_name = '''3. Click OK button then check server that using account'''
            list_check_in_step_3 = ['Check FPT Server is not available: not available',
                                    'Check Samba Server is not available: not available']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_3_name,
                                          list_check_in_step=list_check_in_step_3,
                                          list_actual=list_actual2,
                                          list_expected=list_expected2))
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_3_name,
                                          list_check_in_step=list_check_in_step_3,
                                          list_actual=list_actual2,
                                          list_expected=list_expected2))
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_16_MS_Verify_Samba_Behavior(self):
        self.key = 'MEDIA_SHARE_16'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        try:
            grand_login(driver)
            time.sleep(2)

            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # ===================================================== Enable FTP server
            card_block = driver.find_elements_by_css_selector(card_cls)
            for b in card_block:
                if b.find_element_by_css_selector(' '.join([select, input])).is_selected():
                    b.find_element_by_css_selector(select).click()
                    time.sleep(1)
                    b.find_element_by_css_selector(apply).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(1)

            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Check Title page
            page_title = driver.find_element_by_css_selector(ele_title_page).text
            # ===================================================== Delete
            network_block = driver.find_element_by_css_selector(usb_network)
            while len(network_block.find_elements_by_css_selector(delete_cls)) > 0:
                network_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            account_settings_block = driver.find_element_by_css_selector(account_setting_card)
            while len(account_settings_block.find_elements_by_css_selector(delete_cls)) > 0:
                account_settings_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            # =====================================================
            add_a_usb_network_folder(driver,
                                     DESC_VALUE='Test123',
                                     PATH_FILE='network_file_5',
                                     WRITE=True)
            add_a_usb_account_setting(driver,
                                      ID_VALUE='Humax',
                                      PASSWORD_VALUE='12345')

            list_actual1 = [page_title]
            list_expected1 = ['Media Share > USB']
            check = assert_list(list_actual1, list_expected1)
            step_1_name = '''1. Access and login Web UI and Go to Media Share > USB'''
            list_check_in_step_1 = ['Check title page']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_1_name,
                                          list_check_in_step=list_check_in_step_1,
                                          list_actual=list_actual1,
                                          list_expected=list_expected1))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_1_name,
                                          list_check_in_step=list_check_in_step_1,
                                          list_actual=list_actual1,
                                          list_expected=list_expected1))
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # ===================================================== Enable FTP server
            samba_block = driver.find_element_by_css_selector(samba_server_card)
            default_samba = samba_block.find_element_by_css_selector(' '.join([select, input])).is_selected()

            URL_API = get_config('URL', 'url') + '/api/v1/mediashare/samba'
            _METHOD = 'GET'
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            _BODY = ''
            _TOKEN = get_token(_USER, _PW)
            _res = call_api(URL_API, _METHOD, _BODY, _TOKEN)
            expected_res = _res['active']

            list_actual2 = [default_samba]
            list_expected2 = [expected_res]
            check = assert_list(list_actual2, list_expected2)
            step_2_name = '''2. Go to Media Share > Server Settings > Windows Network (Samba)'''
            list_check_in_step_2 = ['Check default Status of Samba server with API is true']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_2_name,
                                          list_check_in_step=list_check_in_step_2,
                                          list_actual=list_actual2,
                                          list_expected=list_expected2))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_2_name,
                                          list_check_in_step=list_check_in_step_2,
                                          list_actual=list_actual2,
                                          list_expected=list_expected2))
            list_step_fail.append('2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            samba_block = driver.find_element_by_css_selector(samba_server_card)
            time.sleep(0.5)
            samba_block.find_element_by_css_selector(select).click()
            time.sleep(1)

            samba_enable_2 = samba_block.find_element_by_css_selector(' '.join([select, input])).is_selected()
            time.sleep(1)
            list_actual3 = [samba_enable_2]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            step_3_name = '''3. Enable Windows Network (Samba)'''
            list_check_in_step_3 = ['Check Window Network (Samba) should be enabled']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_3_name,
                                          list_check_in_step=list_check_in_step_3,
                                          list_actual=list_actual3,
                                          list_expected=list_expected3))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_3_name,
                                          list_check_in_step=list_check_in_step_3,
                                          list_actual=list_actual3,
                                          list_expected=list_expected3))
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
        try:
            samba_block = driver.find_element_by_css_selector(samba_server_card)
            labels = samba_block.find_elements_by_css_selector(label_name_in_2g)
            values = samba_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Connection Name':
                    v.click()
                    time.sleep(0.5)
                    l.click()
                    time.sleep(0.5)
                    conn_name_error = samba_block.find_element_by_css_selector(error_message).text
                    break

            list_actual4 = [conn_name_error]
            list_expected4 = ['This field is required']
            check = assert_list(list_actual4, list_expected4)
            step_4_name = '''4. Not enter Connection Name: 
                - The cussor click on input box of Connection Name then click out side it.'''
            list_check_in_step_4 = ['Check Error message displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_4_name,
                                          list_check_in_step=list_check_in_step_4,
                                          list_actual=list_actual4,
                                          list_expected=list_expected4))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_4_name,
                                          list_check_in_step=list_check_in_step_4,
                                          list_actual=list_actual4,
                                          list_expected=list_expected4))
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            samba_block = driver.find_element_by_css_selector(samba_server_card)
            labels = samba_block.find_elements_by_css_selector(label_name_in_2g)
            values = samba_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Connection Name':
                    v.click()
                    time.sleep(0.5)
                    v.find_element_by_css_selector(input).send_keys('hoa')
                    break

            samba_block = driver.find_element_by_css_selector(samba_server_card)
            labels = samba_block.find_elements_by_css_selector(label_name_in_2g)
            values = samba_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Connection Name':
                    get_conn_name = v.find_element_by_css_selector(input).get_attribute('value')
                    break

            list_actual5 = [get_conn_name]
            list_expected5 = ['hoa']
            check = assert_list(list_actual5, list_expected5)
            step_5_name = '''5. Enter valid connection name'''
            list_check_in_step_5 = ['Check value in input box']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_5_name,
                                          list_check_in_step=list_check_in_step_5,
                                          list_actual=list_actual5,
                                          list_expected=list_expected5))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_5_name,
                                          list_check_in_step=list_check_in_step_5,
                                          list_actual=list_actual5,
                                          list_expected=list_expected5))
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            samba_block = driver.find_element_by_css_selector(samba_server_card)
            labels = samba_block.find_elements_by_css_selector(label_name_in_2g)
            values = samba_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Account':
                    v.click()
                    time.sleep(0.5)
                    ls_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in ls_options:
                        if o.text == 'Humax':
                            o.click()
                            time.sleep(0.5)
                            break
                if l.text == 'Network Folder':
                    v.click()
                    time.sleep(0.5)
                    ls_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in ls_options:
                        if o.text == 'Test123':
                            o.click()
                            time.sleep(0.5)
                            break
            samba_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(3)

            # Access via http
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            time.sleep(1)
            login(driver, url_login='http://hoa', user_request=_USER, pass_word=_PW)
            time.sleep(1)
            check_home_page = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            time.sleep(1)
            list_actual6 = [check_home_page]
            list_expected6 = [return_true]
            check = assert_list(list_actual6, list_expected6)
            step_67_name = '''6, 7. Enter Network Folder. Apply. Access DUT login via connection name.'''
            list_check_in_step_67 = ['Check access success home page is displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_67_name,
                                          list_check_in_step=list_check_in_step_67,
                                          list_actual=list_actual6,
                                          list_expected=list_expected6))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_67_name,
                                          list_check_in_step=list_check_in_step_67,
                                          list_actual=list_actual6,
                                          list_expected=list_expected6))
            list_step_fail.append('6, 7. Assertion wong.')

        try:
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)

            samba_block = driver.find_element_by_css_selector(samba_server_card)
            labels = samba_block.find_elements_by_css_selector(label_name_in_2g)
            values = samba_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Account':
                    v.click()
                    time.sleep(0.5)
                    ls_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in ls_options:
                        if o.text == 'Anonymous':
                            o.click()
                            time.sleep(0.5)
                            break
            samba_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(3)

            # Access via http
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            time.sleep(1)
            login(driver, url_login='http://hoa', user_request=_USER, pass_word=_PW)
            time.sleep(1)
            check_home_page_2 = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0
            time.sleep(1)
            list_actual7 = [check_home_page_2]
            list_expected7 = [return_true]
            check = assert_list(list_actual7, list_expected7)

            step_89_name = '''8, 9. Enter Account to  Anonymous. Apply. Access DUT login via connection name.'''
            list_check_in_step_89 = ['Check access success home page is displayed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_89_name,
                                          list_check_in_step=list_check_in_step_89,
                                          list_actual=list_actual7,
                                          list_expected=list_expected7))
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_89_name,
                                          list_check_in_step=list_check_in_step_89,
                                          list_actual=list_actual7,
                                          list_expected=list_expected7))
            self.list_steps.append('[END TC]')
            list_step_fail.append('8, 9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_07_MS_Check_Read_Write_permission(self):
        self.key = 'MEDIA_SHARE_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        try:
            grand_login(driver)
            time.sleep(2)
            # Get WAN
            get_wan = driver.find_element_by_css_selector(home_conection_img_wan_ip).text

            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # ===================================================== Enable FTP server
            card_block = driver.find_elements_by_css_selector(card_cls)
            for b in card_block:
                if b.find_element_by_css_selector(' '.join([select, input])).is_selected():
                    b.find_element_by_css_selector(select).click()
                    time.sleep(1)
                    b.find_element_by_css_selector(apply).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(1)

            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Check Title page
            page_title = driver.find_element_by_css_selector(ele_title_page).text
            # ===================================================== Delete
            network_block = driver.find_element_by_css_selector(usb_network)
            while len(network_block.find_elements_by_css_selector(delete_cls)) > 0:
                network_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            account_settings_block = driver.find_element_by_css_selector(account_setting_card)
            while len(account_settings_block.find_elements_by_css_selector(delete_cls)) > 0:
                account_settings_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            driver.refresh()
            time.sleep(5)
            # =====================================================
            add_a_usb_network_folder(driver,
                                     DESC_VALUE='Test123',
                                     PATH_FILE='network_file_5',
                                     WRITE=True)
            add_a_usb_account_setting(driver,
                                      ID_VALUE='Humax',
                                      PASSWORD_VALUE='12345')

            list_actual1 = [page_title]
            list_expected1 = ['Media Share > USB']
            check = assert_list(list_actual1, list_expected1)
            step_1_name = '''1. Access and login Web UI and Go to Media Share > USB'''
            list_check_in_step_1 = ['Check title page']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_1_name,
                                          list_check_in_step=list_check_in_step_1,
                                          list_actual=list_actual1,
                                          list_expected=list_expected1))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_1_name,
                                          list_check_in_step=list_check_in_step_1,
                                          list_actual=list_actual1,
                                          list_expected=list_expected1))
            list_step_fail.append('1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)

            check_title_server = driver.find_element_by_css_selector(ele_title_page).text

            list_actual2 = [check_title_server]
            list_expected2 = ['Media Share > Server Settings']
            check = assert_list(list_actual2, list_expected2)
            step_2_name = '''2. Go to Wireless -> Media Share -> Server Settings'''
            list_check_in_step_2 = ['Check Server Settings page displays']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_2_name,
                                          list_check_in_step=list_check_in_step_2,
                                          list_actual=list_actual2,
                                          list_expected=list_expected2))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_2_name,
                                          list_check_in_step=list_check_in_step_2,
                                          list_actual=list_actual2,
                                          list_expected=list_expected2))
            list_step_fail.append('2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            ftp_block = driver.find_element_by_css_selector(ftp_server)
            if not ftp_block.find_element_by_css_selector(input).is_selected():
                ftp_block.find_element_by_css_selector(select).click()
                time.sleep(0.5)
            ftp_block = driver.find_element_by_css_selector(ftp_server)
            labels = ftp_block.find_elements_by_css_selector(label_name_in_2g)
            values = ftp_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Account':
                    v.click()
                    time.sleep(0.5)
                    ls_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in ls_options:
                        if o.text == 'Humax':
                            o.click()
                            time.sleep(0.5)
                            break
                    continue
                elif l.text == 'Network Folder':
                    v.click()
                    time.sleep(0.5)
                    ls_options = ftp_block.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in ls_options:
                        if o.text == 'Test123':
                            o.click()
                            time.sleep(0.5)
                            break
                    break
            ftp_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            ftp_block = driver.find_element_by_css_selector(ftp_server)
            check_ftp_on = ftp_block.find_element_by_css_selector(' '.join([select, input])).is_selected()

            list_actual3 = [check_ftp_on]
            list_expected3 = [return_true]
            check = assert_list(list_actual3, list_expected3)
            step_3_name = '''3. Enable FTP server and change below settings: Select a Account ; Network Folder: choose a network folder and Apply setting'''
            list_check_in_step_3 = ['Check FTP server is activated']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_3_name,
                                          list_check_in_step=list_check_in_step_3,
                                          list_actual=list_actual3,
                                          list_expected=list_expected3))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_3_name,
                                          list_check_in_step=list_check_in_step_3,
                                          list_actual=list_actual3,
                                          list_expected=list_expected3))
            list_step_fail.append('3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            import ftplib
            # Precondition
            ftp_pre = ftplib.FTP(get_wan, 'Humax', '12345')
            if 'run.png' in ftp_pre.nlst():
                ftp_pre.delete('run.png')
            ftp_pre.quit()
            # Put file
            ftp = ftplib.FTP(get_wan, 'Humax', '12345')
            file = open(run_image_photo, 'rb')
            ftp.storbinary('STOR run.png', file)
            file.close()
            ftp.quit()
            # Check Put file success ?
            check_put_ftp = ftplib.FTP(get_wan, 'Humax', '12345')
            check_put = 'run.png' in check_put_ftp.nlst()
            check_put_ftp.quit()

            # Now, Check file in local
            pre_local = os.listdir()
            file_ = 'run_tmp.png'
            if file_ in pre_local:
                os.remove(file_)
            # Download
            ftp = ftplib.FTP(get_wan, 'Humax', '12345')
            with open(file_, 'wb') as local_file:
                ftp.retrbinary('RETR run.png', local_file.write)
            ftp.quit()
            # Check
            check_get = file_ in os.listdir()

            list_actual4 = [check_put, check_get]
            list_expected4 = [return_true]*2
            check = assert_list(list_actual4, list_expected4)
            step_4_name = '''4. Connect FTP. Put a *.png file then Get that file to local.'''
            list_check_in_step_4 = ['Check file in server is existed',
                                    'Check file in download is existed']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_4_name,
                                          list_check_in_step=list_check_in_step_4,
                                          list_actual=list_actual4,
                                          list_expected=list_expected4))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_4_name,
                                          list_check_in_step=list_check_in_step_4,
                                          list_actual=list_actual4,
                                          list_expected=list_expected4))
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Disabled all running server
            card_block = driver.find_elements_by_css_selector(card_cls)
            for b in card_block:
                if b.find_element_by_css_selector(' '.join([select, input])).is_selected():
                    b.find_element_by_css_selector(select).click()
                    time.sleep(1)
                    b.find_element_by_css_selector(apply).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(1)

            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)

            network_block = driver.find_element_by_css_selector(usb_network)
            network_block.find_elements_by_css_selector(edit_cls)[0].click()
            time.sleep(0.5)
            network_block = driver.find_element_by_css_selector(usb_network)
            edit_field = network_block.find_element_by_css_selector(edit_mode)

            edit_field.find_element_by_css_selector('.read-write #custom-checkbox-read-0+label').click()

            network_block.find_element_by_css_selector(btn_save).click()
            time.sleep(1)
            network_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # check
            network_block = driver.find_element_by_css_selector(usb_network)
            first_row = network_block.find_elements_by_css_selector(rows)[0]
            check_read = first_row.find_element_by_css_selector(permission_read_check_box_first_row).is_selected()

            list_actual5 = [check_read]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            step_5_name = '''5. Click the Edit button of the network folder then change to select Read permission only, click "Apply" , click OK'''
            list_check_in_step_5 = ['Check Permission to Read is enabled']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_5_name,
                                          list_check_in_step=list_check_in_step_5,
                                          list_actual=list_actual5,
                                          list_expected=list_expected5))
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_5_name,
                                          list_check_in_step=list_check_in_step_5,
                                          list_actual=list_actual5,
                                          list_expected=list_expected5))
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # On server
            ftp_block = driver.find_element_by_css_selector(ftp_server)
            if not ftp_block.find_element_by_css_selector(input).is_selected():
                ftp_block.find_element_by_css_selector(select).click()
                time.sleep(0.5)
            ftp_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(5)

            import ftplib
            # Put file
            ftp = ftplib.FTP(get_wan, 'Humax', '12345')
            file = open(run_image_photo, 'rb')
            try:
                ftp.storbinary('STOR run.png', file)
                check_put_perm = False
            except ftplib.error_perm:
                check_put_perm = True
            file.close()
            ftp.quit()

            # Now, Check file in local
            pre_local = os.listdir()
            file_ = 'run_tmp.png'
            if file_ in pre_local:
                os.remove(file_)
            # Download
            ftp = ftplib.FTP(get_wan, 'Humax', '12345')
            with open(file_, 'wb') as local_file:
                ftp.retrbinary('RETR run.png', local_file.write)
            ftp.quit()
            # Check
            check_get_perm = file_ in os.listdir()

            list_actual6 = [check_put_perm, check_get_perm]
            list_expected6 = [return_true] * 2
            check = assert_list(list_actual6, list_expected6)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] Enable FTP server '
            #     f'Check can not put file to server cause no permission. Check can get file from server. '
            #     f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            step_6_name = '''6. Enable FTP server'''
            list_check_in_step_6 = ['Check can not put file to server cause no permission: available',
                                    'Check can get file from server is available']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(step_name=step_6_name,
                                          list_check_in_step=list_check_in_step_6,
                                          list_actual=list_actual6,
                                          list_expected=list_expected6))
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(step_name=step_6_name,
                                          list_check_in_step=list_check_in_step_6,
                                          list_actual=list_actual6,
                                          list_expected=list_expected6))
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')
        self.assertListEqual(list_step_fail, [])

    # def test_17_MS_Verify_Samba_File_Upload_Download_operation(self):
    #     self.key = 'MEDIA_SHARE_17'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     # factory_dut()
    #     try:
    #         grand_login(driver)
    #         time.sleep(2)
    #         # Get WAN
    #         get_wan = driver.find_element_by_css_selector(home_conection_img_wan_ip).text
    #
    #         goto_menu(driver, media_share_tab, media_share_server_settings_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #         # =====================================================
    #         card_block = driver.find_elements_by_css_selector(card_cls)
    #         for b in card_block:
    #             if b.find_element_by_css_selector(' '.join([select, input])).is_selected():
    #                 b.find_element_by_css_selector(select).click()
    #                 time.sleep(1)
    #                 b.find_element_by_css_selector(apply).click()
    #                 wait_popup_disappear(driver, dialog_loading)
    #                 time.sleep(1)
    #                 driver.find_element_by_css_selector(btn_ok).click()
    #                 time.sleep(1)
    #
    #         goto_menu(driver, media_share_tab, media_share_usb_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         # Check Title page
    #         page_title = driver.find_element_by_css_selector(ele_title_page).text
    #         # ===================================================== Delete
    #         network_block = driver.find_element_by_css_selector(usb_network)
    #         while len(network_block.find_elements_by_css_selector(delete_cls)) > 0:
    #             network_block.find_element_by_css_selector(delete_cls).click()
    #             time.sleep(0.5)
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             wait_popup_disappear(driver, dialog_loading)
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             time.sleep(1)
    #         account_settings_block = driver.find_element_by_css_selector(account_setting_card)
    #         while len(account_settings_block.find_elements_by_css_selector(delete_cls)) > 0:
    #             account_settings_block.find_element_by_css_selector(delete_cls).click()
    #             time.sleep(0.5)
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             wait_popup_disappear(driver, dialog_loading)
    #             driver.find_element_by_css_selector(btn_ok).click()
    #             time.sleep(1)
    #         # =====================================================
    #         add_a_usb_network_folder(driver,
    #                                  DESC_VALUE='Test123',
    #                                  PATH_FILE='network_file_5',
    #                                  WRITE=True)
    #         add_a_usb_account_setting(driver,
    #                                   ID_VALUE='Humax',
    #                                   PASSWORD_VALUE='12345')
    #
    #         # Enabled samba server
    #         samba_block = driver.find_element_by_css_selector(samba_server_card)
    #         default_samba = samba_block.find_element_by_css_selector(' '.join([select, input])).is_selected()
    #
    #
    #         list_actual1 = [page_title]
    #         list_expected1 = ['Media Share > USB']
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 1. Login. Goto USB page. Check page title. '
    #             f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1. Login. Goto USB page. Check page title. '
    #             f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
    #         list_step_fail.append('1. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
    #     try:
    #         goto_menu(driver, media_share_tab, media_share_server_settings_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         check_title_server = driver.find_element_by_css_selector(ele_title_page).text
    #
    #         list_actual2 = [check_title_server]
    #         list_expected2 = ['Media Share > Server Settings']
    #         check = assert_list(list_actual2, list_expected2)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 2. Goto Server setting. Check title. '
    #             f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 2. Goto Server setting. Check title. '
    #             f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
    #         list_step_fail.append('2. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
    #     try:
    #         ftp_block = driver.find_element_by_css_selector(ftp_server)
    #         if not ftp_block.find_element_by_css_selector(input).is_selected():
    #             ftp_block.find_element_by_css_selector(select).click()
    #             time.sleep(0.5)
    #         ftp_block = driver.find_element_by_css_selector(ftp_server)
    #         labels = ftp_block.find_elements_by_css_selector(label_name_in_2g)
    #         values = ftp_block.find_elements_by_css_selector(wrap_input)
    #         for l, v in zip(labels, values):
    #             if l.text == 'Account':
    #                 v.click()
    #                 time.sleep(0.5)
    #                 ls_options = driver.find_elements_by_css_selector(secure_value_in_drop_down)
    #                 for o in ls_options:
    #                     if o.text == 'Humax':
    #                         o.click()
    #                         time.sleep(0.5)
    #                         break
    #                 continue
    #             elif l.text == 'Network Folder':
    #                 v.click()
    #                 time.sleep(0.5)
    #                 ls_options = ftp_block.find_elements_by_css_selector(secure_value_in_drop_down)
    #                 for o in ls_options:
    #                     if o.text == 'Test123':
    #                         o.click()
    #                         time.sleep(0.5)
    #                         break
    #                 break
    #         ftp_block.find_element_by_css_selector(apply).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(1)
    #
    #         ftp_block = driver.find_element_by_css_selector(ftp_server)
    #         check_ftp_on = ftp_block.find_element_by_css_selector(' '.join([select, input])).is_selected()
    #
    #         list_actual3 = [check_ftp_on]
    #         list_expected3 = [return_true]
    #         check = assert_list(list_actual3, list_expected3)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 3. Create a FTP server. Check create success. '
    #             f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 3.  Create a FTP server. Check create success. '
    #             f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
    #         list_step_fail.append('3. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
    #     try:
    #         import ftplib
    #         # Precondition
    #         ftp_pre = ftplib.FTP(get_wan, 'Humax', '12345')
    #         if 'run.png' in ftp_pre.nlst():
    #             ftp_pre.delete('run.png')
    #         ftp_pre.quit()
    #         # Put file
    #         ftp = ftplib.FTP(get_wan, 'Humax', '12345')
    #         file = open(run_image_photo, 'rb')
    #         ftp.storbinary('STOR run.png', file)
    #         file.close()
    #         ftp.quit()
    #         # Check Put file success ?
    #         check_put_ftp = ftplib.FTP(get_wan, 'Humax', '12345')
    #         check_put = 'run.png' in check_put_ftp.nlst()
    #         check_put_ftp.quit()
    #
    #         # Now, Check file in local
    #         pre_local = os.listdir()
    #         file_ = 'run_tmp.png'
    #         if file_ in pre_local:
    #             os.remove(file_)
    #         # Download
    #         ftp = ftplib.FTP(get_wan, 'Humax', '12345')
    #         with open(file_, 'wb') as local_file:
    #             ftp.retrbinary('RETR run.png', local_file.write)
    #         ftp.quit()
    #         # Check
    #         check_get = file_ in os.listdir()
    #
    #         list_actual4 = [check_put, check_get]
    #         list_expected4 = [return_true]*2
    #         check = assert_list(list_actual4, list_expected4)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 4. Connect FTP. Put a *.png file. Check that file in server. '
    #             f'Get that file to local. Check that file downloaded. '
    #             f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 4. Connect FTP. Put a *.png file. Check that file in server. '
    #             f'Get that file to local. Check that file downloaded. '
    #             f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
    #         list_step_fail.append('4. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
    #     try:
    #         goto_menu(driver, media_share_tab, media_share_server_settings_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #         # Disabled all running server
    #         card_block = driver.find_elements_by_css_selector(card_cls)
    #         for b in card_block:
    #             if b.find_element_by_css_selector(' '.join([select, input])).is_selected():
    #                 b.find_element_by_css_selector(select).click()
    #                 time.sleep(1)
    #                 b.find_element_by_css_selector(apply).click()
    #                 wait_popup_disappear(driver, dialog_loading)
    #                 time.sleep(1)
    #                 driver.find_element_by_css_selector(btn_ok).click()
    #                 time.sleep(1)
    #
    #         goto_menu(driver, media_share_tab, media_share_usb_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #
    #         network_block = driver.find_element_by_css_selector(usb_network)
    #         network_block.find_elements_by_css_selector(edit_cls)[0].click()
    #         time.sleep(0.5)
    #         network_block = driver.find_element_by_css_selector(usb_network)
    #         edit_field = network_block.find_element_by_css_selector(edit_mode)
    #
    #         edit_field.find_element_by_css_selector('.read-write #custom-checkbox-read-0+label').click()
    #
    #         network_block.find_element_by_css_selector(btn_save).click()
    #         time.sleep(1)
    #         network_block.find_element_by_css_selector(apply).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #
    #         # check
    #         network_block = driver.find_element_by_css_selector(usb_network)
    #         first_row = network_block.find_elements_by_css_selector(rows)[0]
    #         check_read = first_row.find_element_by_css_selector(permission_read_check_box_first_row).is_selected()
    #
    #
    #         list_actual5 = [check_read]
    #         list_expected5 = [return_true]
    #         check = assert_list(list_actual5, list_expected5)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 5. Disabled Server. Change Permission to Read. '
    #             f'Check Read is checked. '
    #             f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 5. Disabled Server. Change Permission to Read. '
    #             f'Check Read is checked. '
    #             f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
    #         list_step_fail.append('5. Assertion wong.')
    #
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
    #     try:
    #         goto_menu(driver, media_share_tab, media_share_server_settings_tab)
    #         wait_popup_disappear(driver, dialog_loading)
    #         # On server
    #         ftp_block = driver.find_element_by_css_selector(ftp_server)
    #         if not ftp_block.find_element_by_css_selector(input).is_selected():
    #             ftp_block.find_element_by_css_selector(select).click()
    #             time.sleep(0.5)
    #         ftp_block.find_element_by_css_selector(apply).click()
    #         wait_popup_disappear(driver, dialog_loading)
    #         time.sleep(1)
    #         driver.find_element_by_css_selector(btn_ok).click()
    #         time.sleep(5)
    #
    #         import ftplib
    #         # Put file
    #         ftp = ftplib.FTP(get_wan, 'Humax', '12345')
    #         file = open(run_image_photo, 'rb')
    #         try:
    #             ftp.storbinary('STOR run.png', file)
    #             check_put_perm = False
    #         except ftplib.error_perm:
    #             check_put_perm = True
    #         file.close()
    #         ftp.quit()
    #
    #         # Now, Check file in local
    #         pre_local = os.listdir()
    #         file_ = 'run_tmp.png'
    #         if file_ in pre_local:
    #             os.remove(file_)
    #         # Download
    #         ftp = ftplib.FTP(get_wan, 'Humax', '12345')
    #         with open(file_, 'wb') as local_file:
    #             ftp.retrbinary('RETR run.png', local_file.write)
    #         ftp.quit()
    #         # Check
    #         check_get_perm = file_ in os.listdir()
    #
    #         list_actual6 = [check_put_perm, check_get_perm]
    #         list_expected6 = [return_true] * 2
    #         check = assert_list(list_actual6, list_expected6)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 6. Enable FTP server. '
    #             f'Check can not put file to server cause no permission. Check can get file from server. '
    #             f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 6.  Enable FTP server. '
    #             f'Check can not put file to server cause no permission. Check can not get file from server. '
    #             f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('6. Assertion wong.')
    #     self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
