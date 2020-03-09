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

save_config(config_path, 'URL', 'url', 'http://192.168.1.1')
class MEDIASHARE(unittest.TestCase):
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
        self.driver.quit()
    # OK
    def test_04_Confirmation_Network_Folder_Creation(self):
        self.key = 'MEDIA_SHARE_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')

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

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        DESCRIPTION_3 = '123!@ abcd #^&*'
        DESCRIPTION_4 = '123!@ abcd'
        PATH_FILE_1 = 'network_file_1'
        PATH_FILE_2 = 'network_file_2'
        LS_PATH_FILE = ['network_file_3', 'network_file_4', 'network_file_5',
                        'network_file_6', 'network_file_7', 'network_file_8']
        fake = Faker()
        try:
            grand_login(driver)
            time.sleep(2)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            time.sleep(1)
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check Add NW folder successfully: Quantity before and after. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check Add NW folder successfully: Quantity before and after. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change same network folder: Check error message. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change same network folder: Check error message. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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

            list_actual34 = [after_add + 1]
            list_expected34 = [after_add_2]
            check = assert_list(list_actual34, list_expected34)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Check Add NW folder successfully: Quantity before and after. '
                f'Actual: {str(list_actual34)}. Expected: {str(list_expected34)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Add NW folder successfully: Quantity before and after. '
                f'Actual: {str(list_actual34)}. Expected: {str(list_expected34)}')
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
            # after_add_final = len(network_table.find_elements_by_css_selector(table_row))

            list_actual4 = [add_btn_disabled, after_add_final]
            list_expected4 = [return_true, exp_max_row_usb_nw]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check Add NW folder successfully: Check Quantity. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Add NW folder successfully: Check Quantity. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_05_Edit_Delete_Network_Folder(self):
        self.key = 'MEDIA_SHARE_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        PATH_FILE_9 = 'network_file_9'
        fake = Faker()

        try:
            grand_login(driver)

            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Network block
            network_block = driver.find_element_by_css_selector(usb_network)
            # Before delete
            network_table = network_block.find_elements_by_css_selector(tbody)
            if len(network_table) == 0:
                before_delete = 0
            else:
                before_delete = len(network_block.find_elements_by_css_selector(tbody))
            # Ke thua tu Media share 04
            network_table = network_block.find_elements_by_css_selector(tbody)
            # Get first row> Click edit
            network_table[0].find_element_by_css_selector(action_edit).click()

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

            # Permission
            per_write = edit_field.find_element_by_css_selector(permission_write_check_box_first_row)
            permission_status_before = per_write.is_selected()
            if permission_status_before:
                driver.find_element_by_css_selector(permission_read_check_box_radio_first_row).click()
            else:
                driver.find_element_by_css_selector(permission_write_check_box_radio_first_row).click()
            # Save
            driver.find_element_by_css_selector(btn_save).click()

            # Apply
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Get value
            desc_check = network_table[0].find_element_by_css_selector(description).text
            path_check = network_table[0].find_element_by_css_selector(path).text.split('/')[-1]
            time.sleep(0.5)
            per_write_first_row = network_table[0].find_element_by_css_selector(permission_write_check_box_first_row)
            per_write_first_row_check = per_write_first_row.is_selected()

            list_actual1 = [desc_check, path_check, permission_status_before]
            list_expected1 = [fake_name, PATH_FILE_9, not(per_write_first_row_check)]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2,3,4. Check edit NW folder successfully: Result same as configuration. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3,4. Check edit NW folder successfully: Result same as configuration. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2,3,4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Get first row> Click delete
            network_table[0].find_element_by_css_selector(action_delete).click()
            time.sleep(0.2)

            # OK
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.2)

            after_delete = len(network_block.find_elements_by_css_selector(tbody))

            list_actual2 = [before_delete - 1]
            list_expected2 = [after_delete]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 5. Delete a rule: Check quantity decrease 1. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Delete a rule: Check quantity decrease 1 '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_06_Edit_Delete_Network_Folder_while_server_is_running(self):
        self.key = 'MEDIA_SHARE_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        ACCOUNT_FTP = 'Anonymous'
        SERVER_FTP = "FTP"

        try:
            grand_login(driver)

            # Goto media share USB
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

            media_fields = server_ftp.find_elements_by_css_selector(media_item)
            # Account
            media_fields[0].find_element_by_css_selector(input).click()
            time.sleep(0.5)
            ls_account = media_fields[0].find_elements_by_css_selector(secure_value_in_drop_down)
            time.sleep(0.5)
            for o in ls_account:
                if o.text == ACCOUNT_FTP:
                    o.click()
                    break

            # Network folder
            media_fields[1].find_element_by_css_selector(input).click()
            time.sleep(0.5)
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2,3. Edit FTP server: Check result same as configuration. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Edit FTP server: Check result same as configuration. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Check status of network folder should be FTP. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check status of network folder should be FTP. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check content of confirm message. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check content of confirm message. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Delete a rule: Check pop-up content; check folder path not in total path. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Delete a rule: Check pop-up content; check folder path not in total path'
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_11_Check_mesage_when_creating_server_without_network_folder_account(self):
        self.key = 'MEDIA_SHARE_11'
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
            self.list_steps.append('[Pass] Precondition')
        except:
            self.list_steps.append('[Fail] Precondition')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Prepare done precondition

        try:
            # Goto Sever setting
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)

            ls_card = [ftp_server,
                       samba_server_card,
                       dlna_server_card,
                       dev_dav_server_card,
                       torrent_server_card,
                       time_machine_server_card]
            exp_msg = [exp_server_account_warning, exp_server_folder_warning]
            _check_warning_msg = []
            for i in ls_card:
                server = driver.find_element_by_css_selector(i)
                ActionChains(driver).move_to_element(server).perform()
                server_btn = server.find_element_by_css_selector(select)
                server_input = server_btn.find_element_by_css_selector(input)
                if not server_input.is_selected():
                    server_btn.click()
                account_warning = server.find_elements_by_css_selector(account_link_cls)
                account_warning_text = [i.text for i in account_warning]
                _check_warning_msg.append(exp_msg == account_warning_text)


            list_actual = _check_warning_msg
            list_expected = [return_true]*6
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Message Server Accounts and Network Folder are not available of '
                f'FTP, Samba, DLNA, WebDAV, Torrent, Time Machine '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Message Server Accounts and Network Folder are not available of '
                f'FTP, Samba, DLNA, WebDAV, Torrent, Time Machine '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_08_Create_account_for_file_sharing(self):
        self.key = 'MEDIA_SHARE_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        TEST_STRING = '123 abc DEF 000222 !@##$&* ():><??+=a,.'
        KEY_WORDS = ['admin', 'Admin', 'root', 'Anonymous']

        try:
            grand_login(driver)
            time.sleep(2)

            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Network block
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)

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
            verify_just_created_rows = ls_account[-1]
            id_account = verify_just_created_rows.find_element_by_css_selector(id_cls).text

            pw_eye = verify_just_created_rows.find_element_by_css_selector(password_eye)
            act = ActionChains(driver)
            act.click_and_hold(pw_eye)
            time.sleep(1)
            pw_account = verify_just_created_rows.find_element_by_css_selector(input_pw).get_attribute('value')
            time.sleep(1)
            act.release(pw_eye)
            act.perform()

            list_actual1 = [id_account, pw_account]
            list_expected1 = [TEST_STRING[:32], TEST_STRING[:32]]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2. Add an account: Check ID and Password is 32 chars. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2. Add an account: Check ID and Password is 32 chars. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3
        try:
            # Click Add 1
            account_setting_block.find_element_by_css_selector(add_class).click()
            time.sleep(0.2)

            # Edit mode
            edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING).perform()
            time.sleep(1)
            password_field = edit_field.find_element_by_css_selector(password_cls)
            password_value = password_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING).perform()
            time.sleep(0.5)
            error_msg = account_setting_block.find_element_by_css_selector(error_message).text

            list_actual2 = [error_msg]
            list_expected2 = [exp_account_id_exist]
            check = assert_list(list_actual2, list_expected2)
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.1)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 3. Change same ID: Check error message. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Change same ID: Check error message. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong.')

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

            list_actual3 = [error_msg_2]
            list_expected3 = [exp_account_null_id]
            check = assert_list(list_actual3, list_expected3)
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.1)
            self.assertTrue(check["result"])
            self.list_steps.append(f'[Pass] 4. Check Add New account with empty ID: Check error message. '
                                   f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Add New account with empty ID: Check error message. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 5
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

            list_actual4 = [check_key_words]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(0.5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check Add KeyWords: Check error msg key words not available. '
                                   f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Add KeyWords: Check error msg key words not available. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append('5. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 6
        try:
            ls_account = len(account_setting_block.find_elements_by_css_selector(rows))
            for i in range(ls_account, 5):
                # Click Add 1
                account_setting_block.find_element_by_css_selector(add_class).click()
                time.sleep(0.2)

                # Edit mode
                edit_field = account_setting_block.find_element_by_css_selector(edit_mode)

                id_field = edit_field.find_element_by_css_selector(id_cls)
                id_value = id_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                    Keys.CONTROL).send_keys(str(i)).perform()
                time.sleep(0.2)

                password_field = edit_field.find_element_by_css_selector(password_cls)
                password_value = password_field.find_element_by_css_selector(input)
                ActionChains(driver).move_to_element(password_value).click().key_down(Keys.CONTROL).send_keys(
                    'a').key_up(Keys.CONTROL).send_keys(str(i)).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_save).click()
                time.sleep(0.2)
            ls_account = len(account_setting_block.find_elements_by_css_selector(rows))

            list_actual5 = [ls_account]
            list_expected5 = [5]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Add max rule: Check max rule. '
                                   f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Add max rule: Check max rule. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK F
    def test_09_Edit_Delete_account(self):
        self.key = 'MEDIA_SHARE_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        TEST_STRING = str(random.randint(10, 100))
        TEST_STRING_EDIT = str(random.randint(1, 10))

        try:
            grand_login(driver)
            time.sleep(2)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)
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
                Keys.CONTROL).send_keys(TEST_STRING_EDIT).perform()
            time.sleep(1)
            id_field = edit_field.find_element_by_css_selector(id_cls)
            id_value = id_field.find_element_by_css_selector(input)
            ActionChains(driver).move_to_element(id_value).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                Keys.CONTROL).send_keys(TEST_STRING_EDIT).perform()

            driver.find_element_by_css_selector(btn_save).click()
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

            list_actual1 = [verify_id_account, verify_pw_account]
            list_expected1 = [TEST_STRING_EDIT, TEST_STRING_EDIT]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Edit an random account: ID and PW changed. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Edit an random account: ID and PW changed. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
        try:
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            # Click Edit
            ls_account[index_chosen].find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver,dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            ls_account_id = [i.find_element_by_css_selector(id_cls).text for i in ls_account]
            check_delete = verify_id_account not in ls_account_id

            list_actual2 = [check_delete]
            list_expected2 = [True]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Delete a rule: Check that rule not in list account. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Delete a rule: Check that rule not in list account. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
    def test_10_Edit_Delete_account_while_server_is_running(self):
        self.key = 'MEDIA_SHARE_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        TEST_STRING = str(random.randint(10, 100))
        TEST_STRING_EDIT = str(random.randint(1, 10))
        DESCRIPTION_3 = '123!@ abcd #^&*'
        PATH_FILE_1 = 'network_file_1'
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
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Account block
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
                    ls_account_drop = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.5)
                    for o in ls_account_drop:
                        if o.text == id_account:
                            o.click()
                            break
                if l.text == 'Network Folder':
                    v.find_element_by_css_selector(input).click()
                    ls_folder = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.5)
                    choice = random.choice(ls_folder)
                    time.sleep(0.5)
                    choice.click()
                    break
            # Apply
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

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
                    ls_account_drop = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.5)
                    for o in ls_account_drop:
                        if o.text == id_account:
                            o.click()
                            break
                if l.text == 'Network Folder':
                    v.find_element_by_css_selector(input).click()
                    ls_folder = v.find_elements_by_css_selector(secure_value_in_drop_down)
                    time.sleep(0.5)
                    choice = random.choice(ls_folder)
                    time.sleep(0.5)
                    choice.click()
                    break
            # Apply
            server_samba.find_element_by_css_selector(apply).click()
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            self.list_steps.append('[Pass] Precondition Successfully')
        except:
            self.list_steps.append('[Fail] Precondition Fail')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Prepare done precondition
        try:
            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Verify
            account_setting_block = driver.find_element_by_css_selector(account_setting_card)
            ActionChains(driver).move_to_element(account_setting_block).perform()
            ls_account = account_setting_block.find_elements_by_css_selector(rows)
            random_account = random.choice(ls_account)
            time.sleep(1)

            # Click Edit
            random_account.find_element_by_css_selector(edit_cls).click()

            check_edit_when_on_server = False
            if len(driver.find_elements_by_css_selector(complete_dialog_msg)) > 0:
                check_edit_when_on_server = True
                time.sleep(5)
                edit_confirm_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Click Delete
            random_account.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)

            check_delete_when_on_server = False
            if len(driver.find_elements_by_css_selector(confirm_dialog_msg)) > 0:
                check_delete_when_on_server = True
                delete_confirm_msg = driver.find_element_by_css_selector(confirm_dialog_msg).text
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            if not (check_delete_when_on_server and check_edit_when_on_server):
                list_actual1 = [check_edit_when_on_server, check_delete_when_on_server]
                list_expected1 = [return_true] * 2
            else:
                list_actual1 = [edit_confirm_msg, delete_confirm_msg]
                list_expected1 = [exp_confirm_msg_edit, exp_delete_account_when_server_running]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Edit and Delete account when server is running: Check Warning. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Edit and Delete account when server is running: Check Warning. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1, 2. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2
        try:
            # Goto Sever setting
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)

            server_ftp = driver.find_element_by_css_selector(ftp_server)
            ftp_account_warning = server_ftp.find_element_by_css_selector(account_link_cls).text

            server_samba = driver.find_element_by_css_selector(samba_server_card)
            samba_account_warning = server_samba.find_element_by_css_selector(account_link_cls).text

            list_actual2 = [ftp_account_warning, samba_account_warning]
            list_expected2 = [exp_server_account_warning]*2
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Delete OK: Check Server Accounts are not available. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 3. Delete OK: Check Server Accounts are not available. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('3. Assertion wong.')

        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
