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

class MediaShare(unittest.TestCase):
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

    def test_04_Confirmation_Network_Folder_Creation(self):
        self.key = 'MEDIA_SHARE_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

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
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            time.sleep(2)
            # Goto media share USB
            goto_menu(driver, media_share_tab, media_share_usb_tab)
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
            list_actual = [before_add+1]
            list_expected = [after_add]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check Add NW folder successfully: Quantity before and after ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check Add NW folder successfully: Quantity before and after. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            list_actual = [err_msg]
            list_expected = [exp_nw_folder_exist]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change same network folder: Check error message')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change same network folder: Check error message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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


            list_actual = [after_add + 1]
            list_expected = [after_add_2]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Check Add NW folder successfully: Quantity before and after')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Add NW folder successfully: Quantity before and after. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [add_btn_disabled, after_add_final]
            list_expected = [return_true, exp_max_row_usb_nw]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Check Add NW folder successfully: Check Quantity')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Add NW folder successfully: Check Quantity. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

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
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)
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

            # Get value
            desc_check = network_table[0].find_element_by_css_selector(description).text
            path_check = network_table[0].find_element_by_css_selector(path).text.split('/')[-1]

            per_write = network_table[0].find_element_by_css_selector(permission_write_check_box_first_row).is_selected()

            list_actual = [desc_check, path_check, permission_status_before]
            list_expected = [fake_name, PATH_FILE_9, not(per_write)]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3,4. Check edit NW folder successfully: Result same as configuration. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3,4. Check edit NW folder successfully: Result same as configuration. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [before_delete - 1]
            list_expected = [after_delete]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Delete a rule: Check quantity decrease 1')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Delete a rule: Check quantity decrease 1 '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

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
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)
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

            # Check and verify value
            account_value = media_fields[0].find_element_by_css_selector(input).get_attribute('value')
            nw_folder_value = media_fields[1].find_element_by_css_selector(input).get_attribute('value')


            list_actual = [account_value, nw_folder_value]
            list_expected = [ACCOUNT_FTP, option_value]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Edit FTP server: Check result same as configuration. ')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Edit FTP server: Check result same as configuration. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [check_folder_status]
            list_expected = [SERVER_FTP]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Check status of network folder should be FTP')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check status of network folder should be FTP. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            list_actual = [confirm_msg_edit]
            list_expected = [exp_confirm_msg_edit]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check content of confirm message. ')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check content of confirm message. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [confirm_msg_delete, check_delete]
            list_expected = [exp_confirm_msg_delete, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Delete a rule: Check pop-up content; check folder path not in total path')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Delete a rule: Check pop-up content; check folder path not in total path'
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')


        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
