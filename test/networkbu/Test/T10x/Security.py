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


class SECURITY(unittest.TestCase):
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
            connect_wifi_by_command('HVNWifi', 'Wifihvn12@!')
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.start_time)
            os.system('netsh wlan disconnect')
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

    def test_01_SECURITY_Check_Parental_Code_setting(self):
        self.key = 'SECURITY_01'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        factory_dut()
        # ===========================================================
        PARENTAL_CODE_KEY = '1234'
        PARENTAL_WRONG_CODE_KEY = '4321'

        try:
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, security_tab, security_parentalcontrol_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Enable parental code
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_code_btn = parental_code.find_element_by_css_selector(select)
            parental_code_btn.click()

            parental_filed_name = driver.find_elements_by_css_selector(parental_popup_label)
            ls_parental_name = [i.text for i in parental_filed_name]

            parental_field_input = driver.find_elements_by_css_selector(parental_popup_input)
            #  New
            time.sleep(0.5)
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            ActionChains(driver).click(parental_field_input[4]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_CODE_KEY)

            list_actual1 = ls_parental_name
            list_expected1 = exp_ls_parental_label
            check = assert_list(list_actual1, list_expected1)

            step_1_2_3_name = '''1. Access and login Web UI
                                2. Go to Security -> Parental Control
                                3. Enable Parental Code and set up new parental code'''
            list_check_in_step_1_2_3 = ['Check  "New Parental Code" field',
                                        'Check "Retype New Parental Code" field']
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
            # Disable
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_code_btn = parental_code.find_element_by_css_selector(select)
            parental_code_btn.click()
            wait_popup_disappear(driver, dialog_loading)
            # Enable
            time.sleep(1)
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_code_btn = parental_code.find_element_by_css_selector(select)
            parental_code_btn.click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            pop_up_title = driver.find_element_by_css_selector(parental_popup_title).text

            list_actual2 = [pop_up_title]
            list_expected2 = [exp_parental_pop_up_title]
            check = assert_list(list_actual2, list_expected2)
            # self.assertTrue(check["result"])
            # self.list_steps.append('[Pass] 4. Refresh Parental control: Check title pop up. '
            #                        f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            step_4_name = '''4. Refresh the Parental Control page'''
            list_check_in_step_4 = ['Check title pop up']
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
            # Input invalid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_WRONG_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)

            error_msg = driver.find_element_by_css_selector(error_text).text

            list_actual3 = [error_msg]
            list_expected3 = [exp_parental_error_msg]
            check = assert_list(list_actual3, list_expected3)
            # self.assertTrue(check["result"])
            # self.list_steps.append('[Pass] 5. Input wrong parental code: Check error message. '
            #                        f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            step_5_name = '''5. Input an invalid parental code'''
            list_check_in_step_5 = ['Check error message']
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
            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)
            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0

            list_actual4 = [check_page_security]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            # self.assertTrue(check["result"])
            # self.list_steps.append('[Pass] 6. Input valid code. Check page Security displayed. '
            #                        f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            step_6_name = '''6. Input a valid parental code'''
            list_check_in_step_6 = ['Check page Security displayed.']
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

    def test_02_SECURITY_Parental_code_Change_Confirmation(self):
        self.key = 'SECURITY_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        PARENTAL_NEW_CODE_KEY = str(random.randint(1000, 9999))
        PARENTAL_INIT_KEY = '!@#$'
        PARENTAL_NEW_CODE_KEY_2 = '1111'
        try:
            grand_login(driver)

            # Goto Security
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)

            if len(parental_field_input) > 0:
                #  New
                ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            else:
                parental_code = driver.find_element_by_css_selector(parental_code_card)
                parental_code_select = parental_code.find_element_by_css_selector(select)
                if not parental_code_select.find_element_by_css_selector(input).is_selected():
                    parental_code_select.click()
                    wait_popup_disappear(driver, dialog_loading)

                    ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                    time.sleep(0.5)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)

            check_page_security = len(driver.find_elements_by_css_selector(security_page)) > 0
            time.sleep(1)
            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual1 = [check_page_security, check_pop_up_disable]
            list_expected1 = [return_true, return_true]
            check = assert_list(list_actual1, list_expected1)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     '[Pass] 1,2,3. Check Security page displayed'
            #     f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            step_1_2_3_name = '''1. Access and login Web UI
                                2. Go to Security -> Parental Control
                                3. Enable Parental Code'''
            list_check_in_step_1_2_3 = ['Check Security page is displayed',
                                        'Check apply without error. Check popup disappear']
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

        try:
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_input = parental_code.find_elements_by_css_selector(input)
            time.sleep(0.5)
            # New parental code
            parental_input[1].send_keys(PARENTAL_NEW_CODE_KEY)
            time.sleep(0.5)
            # Retype parental code
            parental_input[2].send_keys(PARENTAL_NEW_CODE_KEY)

            # Apply
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)

            # Refresh
            driver.refresh()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_NEW_CODE_KEY).perform()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            check_page_security = len(driver.find_elements_by_css_selector(security_page)) > 0
            time.sleep(3)
            # Save to config file
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_NEW_CODE_KEY)

            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual2 = [check_page_security, check_pop_up_disable]
            list_expected2 = [return_true, return_true]
            check = assert_list(list_actual2, list_expected2)

            step_4_5_name = '''4. Input new parental code and click Apply setting
                               5. Refresh the parental control page and input the new parental code'''
            list_check_in_step_4_5 = ['Check Security page is displayed',
                                      'Check popup disappear']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_5_name,
                    list_check_in_step=list_check_in_step_4_5,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('4, 5. Assertion wong.')

        try:
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_input = parental_code.find_elements_by_css_selector(input)

            parental_code_select = parental_code.find_element_by_css_selector(select)
            if parental_code_select.find_element_by_css_selector(input).is_selected():
                parental_code_select.click()
                wait_popup_disappear(driver, dialog_loading)

            check_parental_code_disabled = parental_code_select.find_element_by_css_selector(input).is_selected()

            list_actual6 = [check_parental_code_disabled]
            list_expected6 = [return_false]
            check = assert_list(list_actual6, list_expected6)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 6. Disable Parental code: Check Parental Code disabled. '
            #     f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            step_6_name = '''6. Disable Parental Code button'''
            list_check_in_step_6 = ['Check Parental Code should be disabled']
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
            list_step_fail.append('6. Assertion wong.')

        try:
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_code_select = parental_code.find_element_by_css_selector(select)
            if not parental_code_select.find_element_by_css_selector(input).is_selected():
                parental_code_select.click()
                wait_popup_disappear(driver, dialog_loading)

            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_INIT_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            check_popup_content= driver.find_element_by_css_selector(confirm_dialog_msg).text
            time.sleep(1)

            # Click OK
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            check_create_new_parental = len(driver.find_elements_by_css_selector('#parental-create-password-id')) > 0

            list_actual7 = [check_popup_content, check_create_new_parental]
            list_expected7 = [exp_confirm_msg_init_parental_key, return_true]
            check = assert_list(list_actual7, list_expected7)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 7. Input Init parental code. '
            #     f'Check confirm message. Click OK. Check popup parental create code display. '
            #     f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            step_7_name = '''7. Enable Parental Code, then input code to reset parental code : !@#$ then click OK button'''
            list_check_in_step_7 = ['Check confirm message.',
                                    'Check popup parental create code is displayed.']
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
            list_step_fail.append('7 Assertion wong.')

        try:
            parental_field_input = driver.find_elements_by_css_selector(parental_popup_input)
            #  New
            time.sleep(0.5)
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_NEW_CODE_KEY_2).perform()
            time.sleep(0.5)
            ActionChains(driver).click(parental_field_input[4]).send_keys(PARENTAL_NEW_CODE_KEY_2).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_NEW_CODE_KEY_2)

            check_dialog_parental_display = len(driver.find_elements_by_css_selector('.parental-login-dialog')) > 0

            list_actual8 = [check_dialog_parental_display]
            list_expected8 = [return_true]
            check = assert_list(list_actual8, list_expected8)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 8. Input new parental code key. Click OK.'
            #     f'Check popup login parental display. '
            #     f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
            step_8_name = '''8. Input New Parental Code
                            Input Retype New Parental Code
                            - Click OK'''
            list_check_in_step_8 = ['Check popup login parental is displayed.']
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
            list_step_fail.append('8. Assertion wong.')

        try:
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_NEW_CODE_KEY_2).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            check_page_security_2 = len(driver.find_elements_by_css_selector(security_page)) > 0

            list_actual9 = [check_page_security_2]
            list_expected9 = [return_true]
            check = assert_list(list_actual9, list_expected9)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 9. Input parental code key. Click OK.'
            #     f'Check Security page display. '
            #     f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
            step_9_name = '''9. Refresh the parental control page and input the new parental code in step8
                            - Click OK, then check page display'''
            list_check_in_step_9 = ['CheckThe "Parental Control" page should be displayed.']
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
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_03_SECURITY_Confirmation_Parental_code_Initialization(self):
        self.key = 'SECURITY_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        PARENTAL_NEW_CODE_KEY = str(random.randint(1000, 9999))
        PARENTAL_INIT_CODE_KEY = '!@#$'
        try:
            grand_login(driver)

            # Goto media share USB
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            #
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_input = parental_code.find_elements_by_css_selector(input)

            # New parental code
            time.sleep(0.5)
            parental_input[1].send_keys(PARENTAL_NEW_CODE_KEY)
            # Retype parental code
            time.sleep(0.5)
            parental_input[2].send_keys(PARENTAL_NEW_CODE_KEY)

            # Apply
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)

            #
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_NEW_CODE_KEY)

            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0
            time.sleep(3)
            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual1 = [check_page_security, check_pop_up_disable]
            list_expected1 = [return_true, return_true]
            check = assert_list(list_actual1, list_expected1)

            step_1_2_3_name = '''1. Access and login Web UI
                                2. Go to Security -> Parental Control
                                3. Enable Parental Code and set up new parental code'''
            list_check_in_step_1_2_3 = ['Check Security page is displayed',
                                        'Check apply without error. Check popup disappear']
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
            list_step_fail.append('1,2,3. Assertion wong.')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
        try:
            # Refresh
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_code_btn = parental_code.find_element_by_css_selector(select)
            parental_code_btn.click()
            wait_popup_disappear(driver, dialog_loading)
            # Enable
            time.sleep(1)
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_code_btn = parental_code.find_element_by_css_selector(select)
            parental_code_btn.click()
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_INIT_CODE_KEY).perform()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(0.5)
            check_pop_init = len(driver.find_elements_by_css_selector(parental_pop_init_pw))>0

            list_actual2 = [check_pop_init]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)

            step_4_name = '''4. Refresh the parental control page and input the parental code: !@#$'''
            list_check_in_step_4 = ['Check pop-up init is displayed']
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

        # ~~~~~~~~~~~~~~~~ 5
        try:
            parental_field_name = driver.find_elements_by_css_selector(parental_popup_label)
            ls_parental_name = [i.text for i in parental_field_name]
            time.sleep(1)
            parental_field_input = driver.find_elements_by_css_selector(parental_popup_input)
            #  New
            time.sleep(1)
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            ActionChains(driver).click(parental_field_input[4]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Save
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_CODE_KEY)

            list_actual3 = ls_parental_name
            list_expected3 = exp_ls_parental_label
            check = assert_list(list_actual3, list_expected3)

            step_5_name = '''5. Enter a new parental code'''
            list_check_in_step_5 = ['Check Parental pop up labels "New Parental Code" field',
                                    'Check Parental pop up labels "Retype New Parental Code" field']
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
            list_step_fail.append('. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 6
        try:
            time.sleep(0.5)
            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            time.sleep(0.5)
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            time.sleep(3)
            check_page_security_2 = len(driver.find_elements_by_css_selector(security_page)) > 0
            check_pop_up_disable_2 = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual4 = [check_page_security_2, check_pop_up_disable_2]
            list_expected4 = [return_true, return_true]
            check = assert_list(list_actual4, list_expected4)

            step_6_name = '''6. Refresh the parental control page and input the new parental code'''
            list_check_in_step_6 = ['Check Security page is displayed',
                                    'Check popup content is displayed']
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

    def test_04_SECURITY_Parental_Control_function_On_Off_check(self):
        self.key = 'SECURITY_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        SOCIAL_NW = get_config('SECURITY', 'security4_social_nw', input_data_path)
        USER_DEFINE = get_config('SECURITY', 'security4_user_define', input_data_path)
        FACEBOOK = get_config('SECURITY', 'security4_facebook', input_data_path)
        GOOGLE = get_config('SECURITY', 'security4_google', input_data_path)
        try:
            grand_login(driver)

            # Goto media share USB
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_element_by_css_selector(parental_wrap_input)

            #  New
            ActionChains(driver).click(parental_field_input).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Control Rule
            rule_block = driver.find_element_by_css_selector(parental_rule_card)

            # Click Add 1
            rule_block.find_element_by_css_selector(add_class).click()
            time.sleep(0.2)

            # Edit mode
            edit_field = rule_block.find_element_by_css_selector(edit_mode)

            device_name_field = edit_field.find_element_by_css_selector(name_cls)
            device_name_field.find_element_by_css_selector(input).click()

            # Select all
            opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)

            for i in range(len(opts)-1):
                opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
                opts[0].click()
                device_name_field.find_element_by_css_selector(input).click()

            # Setup the filter
            edit_field.find_element_by_css_selector('.service-filter').find_element_by_css_selector(apply).click()
            time.sleep(0.5)

            # ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            # for f in ls_service:
            #     if f.text == SOCIAL_NW:
            #         f.click()
            #         break
            #
            # ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            # for s in ls_service_sub:
            #     if s.text == FACEBOOK:
            #         if not len(s.find_elements_by_css_selector('.selected-icon')) > 0:
            #             s.click()
            #             break
            #
            # ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            # for f in ls_service:
            #     if f.text == USER_DEFINE:
            #         f.click()
            #         check_item_inner = driver.find_elements_by_css_selector('.child-item .item-inner')
            #         check_item_exist = any([i.text == GOOGLE for i in check_item_inner])
            #         if not check_item_exist:
            #             # Add url
            #             driver.find_element_by_css_selector(add_class).click()
            #             f.find_element_by_css_selector(input).send_keys(GOOGLE)
            #             time.sleep(1)
            #             f.find_element_by_css_selector(btn_save).click()
            #             time.sleep(1)
            #
            # ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            # for f in ls_service:
            #     if f.text == USER_DEFINE:
            #         f.click()
            #         break
            #
            # ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            # for s in ls_service_sub:
            #     if s.text == GOOGLE:
            #         if not len(s.find_elements_by_css_selector('.selected-icon')) > 0:
            #             s.click()
            #             break

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == SOCIAL_NW:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()

                    ls_service_sub = f.find_elements_by_css_selector('.service-sub-item-wrap')
                    for s in ls_service_sub:
                        ActionChains(driver).move_to_element(s).perform()
                        if s.text == 'facebook':
                            s.click()

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == USER_DEFINE:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()
                    check_item_inner = driver.find_elements_by_css_selector('.child-item .item-inner')
                    ActionChains(driver).move_to_element(check_item_inner[-1]).perform()
                    time.sleep(0.5)
                    check_item_exist = any([i.text == 'google.com' for i in check_item_inner])
                    print(check_item_exist)
                    time.sleep(1)
                    if not check_item_exist:
                        # Add url
                        driver.find_element_by_css_selector(add_class).click()
                        f.find_element_by_css_selector(input).send_keys('google.com')
                        time.sleep(1)
                        f.find_element_by_css_selector(btn_save).click()
            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == USER_DEFINE:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()
            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                ActionChains(driver).move_to_element(s).perform()
                if s.text == 'google.com':
                    s.click()
                    break
            # Save
            time.sleep(2)
            driver.find_element_by_css_selector(btn_ok).click()

            # Schedule
            edit_field.find_element_by_css_selector('.set-schedule').find_element_by_css_selector(apply).click()
            time.sleep(1)

            # +++++++++++++++
            now = datetime.now()
            weekdays = now.strftime('%a').upper()
            hourday = int(now.strftime('%H'))

            dict_transfer = {
                "SUN": 1,
                "MON": 2,
                "TUE": 3,
                "WED": 4,
                "THU": 5,
                "FRI": 6,
                "SAT": 7
            }
            weekday_index = [dict_transfer[i] for i in dict_transfer.keys() if i == weekdays][0]
            hourday_index_1 = hourday + 3
            hourday_index_2 = hourday_index_1 + 1
            # +++++++++++++++
            # Click ALL to set avalable
            week_day_all = driver.find_elements_by_css_selector(f'tr:nth-child({weekday_index})>.all.hight-light')
            if len(week_day_all) > 0:
                week_day_all[0].click()
            time.sleep(1)

            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_1})').click()
            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_2})').click()
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_save).click()
            wait_popup_disappear(driver, dialog_loading)
            # driver.find_element_by_css_selector(btn_ok).click()
            # wait_popup_disappear(driver, dialog_loading)
            # Check Service Filter
            ls_service_filter_items = driver.find_elements_by_css_selector(service_filter_items)
            ls_service_filter_items_value = [s.text for s in ls_service_filter_items]
            # Check block schedule
            block_schedule_value = driver.find_element_by_css_selector(block_schedule).text

            list_actual1 = [ls_service_filter_items_value, block_schedule_value]
            list_expected1 = [['Social Network[1]', 'User Define[1]'], exp_block_schedule_value]
            check = assert_list(list_actual1, list_expected1)

            step_1_2_3_name = '''1, 2, 3. Login. Goto parental control.
                At Control Rule, click the Add button and change below settings:
                - Device Name/MAC Address: Select a connected device from dropdown list or enter a MAC address manually (need to check both methods)
                - Service Filters:
                + Click "Setup the Filters" and choose "facebook" in Social Network category
                + Add a "User Define" filter for "google.com" and select the created filter then save the filter
                - Block Schedule: Click "Setup the Schedule" and choose the schedule contains the testing time
                and click Save the rule'''
            list_check_in_step_1_2_3 = ['Check list of Social Network[1] User Define[1]',
                                        'Check Block Schedule text']
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
            list_step_fail.append('1,2,3. Assertion wong.')

        FACEBOOK = 'http://facebook.com'
        FACEBOOK_S = 'https://facebook.com'
        GOOGLE = 'http://google.com'
        GOOGLE_S = 'https://google.com'
        for i in range(1, 7):
            driver2 = webdriver.Chrome(driver_path)
            time.sleep(5)
            try:
                driver2.get(FACEBOOK)
                time.sleep(3)
                fb_http_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(1)

                driver2.get(FACEBOOK_S)
                time.sleep(3)
                fb_https_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(1)

                driver2.get(GOOGLE)
                time.sleep(3)
                gg_http_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(1)

                driver2.get(GOOGLE_S)
                time.sleep(3)
                gg_https_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(1)

                # check_step_4 = all([i != 200 for i in [fb_http_4, fb_https_4, gg_http_4, gg_https_4]])
                check_step_4 = [fb_http_4, fb_https_4, gg_http_4, gg_https_4]
                # ======================================================================================
                parental_rule = driver.find_element_by_css_selector('tbody>tr>td.toggle-col')
                parental_rule_btn = parental_rule.find_element_by_css_selector(select)
                parental_rule_check = parental_rule.find_element_by_css_selector(input)
                if parental_rule_check.is_selected():
                    parental_rule_btn.click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                else:
                    parental_rule_btn.click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                # ======================================================================================
                driver2.get(FACEBOOK)
                time.sleep(3)
                fb_http_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(1)

                driver2.get(FACEBOOK_S)
                time.sleep(3)
                fb_https_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(1)

                driver2.get(GOOGLE)
                time.sleep(3)
                gg_http_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(1)

                driver2.get(GOOGLE_S)
                time.sleep(3)
                gg_https_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(1)

                check_step_6 = [fb_http_6, fb_https_6, gg_http_6, gg_https_6]
                # check_step_6 = all([i == 200 for i in [fb_http_6, fb_https_6, gg_http_6, gg_https_6]])
                # ======================================================================================

                # Enable
                parental_rule = driver.find_element_by_css_selector('tbody>tr>td.toggle-col')
                parental_rule_btn = parental_rule.find_element_by_css_selector(select)
                parental_rule_check = parental_rule.find_element_by_css_selector(input)
                if parental_rule_check.is_selected():
                    parental_rule_btn.click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                else:
                    parental_rule_btn.click()
                    wait_popup_disappear(driver, dialog_loading)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                # ======================================================================================
                driver2.get(FACEBOOK)
                time.sleep(3)
                fb_http_8 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(1)

                driver2.get(FACEBOOK_S)
                time.sleep(3)
                fb_https_8 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(1)

                driver2.get(GOOGLE)
                time.sleep(3)
                gg_http_8 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(1)

                driver2.get(GOOGLE_S)
                time.sleep(3)
                gg_https_8 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(1)

                check_step_8 = [fb_http_8, fb_https_8, gg_http_8, gg_https_8]

                list_actual2 = [check_step_4, check_step_6, check_step_8]
                list_expected2 = [[return_false]*4, [return_true]*4, [return_false]*4]
                check = assert_list(list_actual2, list_expected2)

                step_2_name = f'''4-8. -Repeat: {str(i+1)} From the registered device in step 3, access below URL from web browser:
                                    http://facebook.com, https://facebook.com, http://google.com, https://google.com.\n
                                    Disabled Parental Rule. Then check this site again.\n
                                    Enabled Parental Rule. Then check this site again'''
                list_check_in_step_2 = [['Check can not access http://facebook.com: not access',
                                         'Check can not access https://facebook.com: not access',
                                         'Check can not access http://google.com: not access',
                                         'Check can not access https://google.com: not access.'],
                                        ['Check can access http://facebook.com: access',
                                         'Check can access https://facebook.com: access',
                                         'Check can access http://google.com: access',
                                         'Check can access https://google.com: access.'],
                                        ['Check can not access http://facebook.com:not access',
                                         'Check can not access https://facebook.com:not access',
                                         'Check can not access http://google.com:not access',
                                         'Check can not access https://google.com:not access.']
                                        ]
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
                list_step_fail.append(f'4-8. -{str(i+1)}- Assertion wong.')
            driver2.quit()

        self.list_steps.append('[END TC]')
        self.assertListEqual(list_step_fail, [])

    def test_05_SECURITY_Add_Parental_Control_rule_and_check_Disabled(self):
        self.key = 'SECURITY_05'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        SOCIAL_NW = get_config('SECURITY', 'security4_social_nw', input_data_path)
        USER_DEFINE = get_config('SECURITY', 'security4_user_define', input_data_path)
        FACEBOOK = get_config('SECURITY', 'security4_facebook', input_data_path)
        GOOGLE = get_config('SECURITY', 'security4_google', input_data_path)
        try:
            grand_login(driver)

            # Goto media share USB
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            if len(parental_field_input) > 0:
                #  New
                ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Parental Control']
            check = assert_list(list_actual1, list_expected1)

            step_1_2_name = '1, 2. Go to Security > Parental Control, enable the Parental Control function and set a parental code.'
            list_check_in_step_1_2 = ['Security > Parental Control page should be displayed.']
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
            rule_block = driver.find_element_by_css_selector(parental_rule_card)

            while len(rule_block.find_elements_by_css_selector(delete_cls)) > 0:
                rule_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            driver.refresh()
            time.sleep(3)
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            if len(parental_field_input) > 0:
                #  New
                ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            # Control Rule
            rule_block = driver.find_element_by_css_selector(parental_rule_card)
            # Click Add 1
            rule_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)
            # Edit mode
            edit_field = rule_block.find_element_by_css_selector(edit_mode)

            device_name_field = edit_field.find_element_by_css_selector(name_cls)
            device_name_field.find_element_by_css_selector(input).click()

            # Select all
            opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
            for i in range(len(opts)-1):
                opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
                opts[0].click()
                break

            device_name_field.find_element_by_css_selector(input).click()
            driver.find_element_by_css_selector('.user-define').click()
            driver.find_element_by_css_selector('input[name="input-field"]').send_keys('1A2B3C4D5E6F')


            # Setup the filter
            edit_field.find_element_by_css_selector('.service-filter').find_element_by_css_selector(apply).click()
            time.sleep(0.5)

            time.sleep(1)
            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == SOCIAL_NW:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()

                    ls_service_sub = f.find_elements_by_css_selector('.service-sub-item-wrap')
                    for s in ls_service_sub:
                        ActionChains(driver).move_to_element(s).perform()
                        if s.text == 'facebook':
                            s.click()

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == USER_DEFINE:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()
                    check_item_inner = driver.find_elements_by_css_selector('.child-item .item-inner')
                    ActionChains(driver).move_to_element(check_item_inner[0]).perform()
                    time.sleep(0.5)
                    check_item_exist = any([i.text == 'google.com' for i in check_item_inner])
                    print(check_item_exist)
                    time.sleep(1)
                    if not check_item_exist:
                        # Add url
                        driver.find_element_by_css_selector(add_class).click()
                        f.find_element_by_css_selector(input).send_keys('google.com')
                        time.sleep(1)
                        f.find_element_by_css_selector(btn_save).click()
            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                ActionChains(driver).move_to_element(s).perform()
                if s.text == 'google.com':
                    s.click()
                    break

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for s in ls_service:
                ActionChains(driver).move_to_element(s).perform()
                if s.find_element_by_css_selector('span').text not in ['Social Network', 'User Define']:
                    s.click()
                    ls_service_sub = s.find_elements_by_css_selector('.service-sub-item-wrap')
                    random_sub = random.choice(ls_service_sub)
                    ActionChains(driver).move_to_element(random_sub).perform()
                    random_sub.click()

            sub_title = driver.find_element_by_css_selector('.sub-title').text
            # Save
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()

            # Schedule
            edit_field.find_element_by_css_selector('.set-schedule').find_element_by_css_selector(apply).click()
            time.sleep(1)

            # +++++++++++++++
            now = datetime.now()
            weekdays = now.strftime('%a').upper()
            hourday = int(now.strftime('%H'))

            dict_transfer = {
                "SUN": 1,
                "MON": 2,
                "TUE": 3,
                "WED": 4,
                "THU": 5,
                "FRI": 6,
                "SAT": 7
            }
            weekday_index = [dict_transfer[i] for i in dict_transfer.keys() if i == weekdays][0]
            hourday_index_1 = hourday + 3
            hourday_index_2 = hourday_index_1 + 1

            # Click ALL to set avalable
            week_day_all = driver.find_elements_by_css_selector(f'tr:nth-child({weekday_index})>.all.hight-light')
            if len(week_day_all) > 0:
                week_day_all[0].click()
            time.sleep(1)

            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_1})').click()
            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_2})').click()
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_save).click()
            wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)
            # driver.find_element_by_css_selector('.filter-count').click()
            time.sleep(1)
            exp_service = ['Social Network[1]', 'User Define[1]']
            number_of_total_nw = [i.text for i in driver.find_elements_by_css_selector('.filter-item')]
            check_service_filter = all([i in number_of_total_nw for i in exp_service])

            # Check block schedule
            block_schedule_value = driver.find_elements_by_css_selector('.schedule')[-1].text

            list_actual3 = [sub_title, check_service_filter, block_schedule_value]
            list_expected3 = [exp_subtitle_set_website_app, True, exp_block_schedule_value]
            check = assert_list(list_actual3, list_expected3)

            step_3_name = '''3. Click the Add button and change below settings:
                        - Device Name/MAC Address: Select a connected device from dropdown list or enter a MAC address manually (need to check both methods)
                        - Service Filters:
                        + Click "Setup the Filters" and choose "facebook" in Social Network category
                        + Add a "User Define" filter for "google.com" and select the created filter 
                        + Select 9 other service for the dropdown list then save the filter
                        - Block Schedule: Click "Setup the Schedule" and choose the schedule contains the testing time
                        and click Save the rule'''
            list_check_in_step_3 = ['Check Set the Websites/Apps Sub title',
                                    'Check list Social Network[1] and User Filter[1] is displayed',
                                    'Check Block schedule text']
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

        FACEBOOK = 'http://facebook.com'
        FACEBOOK_S = 'https://facebook.com'
        GOOGLE = 'http://google.com'
        GOOGLE_S = 'https://google.com'

        try:
            driver2 = webdriver.Chrome(driver_path)
            time.sleep(1)
            driver2.get(FACEBOOK)
            time.sleep(3)
            fb_http_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(1)

            driver2.get(FACEBOOK_S)
            time.sleep(3)
            fb_https_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(1)

            driver2.get(GOOGLE)
            time.sleep(3)
            gg_http_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(1)

            driver2.get(GOOGLE_S)
            time.sleep(3)
            gg_https_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(1)

            driver2.quit()

            list_actual4 = [fb_http_4, fb_https_4, gg_http_4, gg_https_4]
            list_expected4 = [return_false] * 4
            check = assert_list(list_actual4, list_expected4)

            step_4_name = '''4. From the registered device in step 3, access below URL from web browser:
                            - http://facebook.com
                            - https://facebook.com
                            - http://google.com 
                            - https://google.com'''
            list_check_in_step_4 = ['Check can not access to http://facebook.com: not access',
                                    'Check can not access to https://facebook.com: not access',
                                    'Check can not access to http://google.com: not access',
                                    'Check can not access to https://google.com: not access']
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
            # ======================================================================================
            time.sleep(1)
            # Disable Parental control
            parental_rule = driver.find_element_by_css_selector(parental_rule_card)
            ls_rows = parental_rule.find_elements_by_css_selector(rows)
            for r in ls_rows:
                row_active = r.find_element_by_css_selector(input)
                if row_active.is_selected():
                    r.find_element_by_css_selector(select).click()
                    wait_popup_disappear(driver, dialog_loading)
                    time.sleep(1)
                    driver.find_element_by_css_selector(btn_ok).click()
                    time.sleep(1)
                    break

            parental_rule = driver.find_element_by_css_selector(parental_rule_card)
            ls_rows = parental_rule.find_elements_by_css_selector(rows)
            for r in ls_rows:
                check_row_active = r.find_element_by_css_selector(input).is_selected()
            list_actual5 = [check_row_active]
            list_expected5 = [return_false]
            check = assert_list(list_actual5, list_expected5)

            step_5_name = '''5. Disable the Parental Control rule function'''
            list_check_in_step_5 = ['Check rule disabled']
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

            # ======================================================================================

        try:
            driver2 = webdriver.Chrome(driver_path)
            driver2.get(FACEBOOK)
            time.sleep(3)
            fb_http_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(1)

            driver2.get(FACEBOOK_S)
            time.sleep(3)
            fb_https_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(1)

            driver2.get(GOOGLE)
            time.sleep(3)
            gg_http_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(1)

            driver2.get(GOOGLE_S)
            time.sleep(3)
            gg_https_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(1)
            driver2.quit()
            list_actual6 = [fb_http_6, fb_https_6, gg_http_6, gg_https_6]
            list_expected6 = [return_true] * 4
            check = assert_list(list_actual6, list_expected6)

            step_6_name = '''6. From the registered device in step 3, access below URL from web browser:
                            - http://facebook.com
                            - https://facebook.com
                            - http://google.com 
                            - https://google.com'''
            list_check_in_step_6 = ['Check can access to http://facebook.com: access',
                                    'Check can access to https://facebook.com: access',
                                    'Check can access to http://google.com: access',
                                    'Check can access to https://google.com: access']
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
            list_step_fail.append('6. Assertion wong.')

        try:
            for i in range(5):
                add_a_parental_control_rule(driver)

            check_add_btn_disabled = driver.find_element_by_css_selector(add_class).is_enabled()
            list_actual7 = [check_add_btn_disabled]
            list_expected7 = [return_false]
            check = assert_list(list_actual7, list_expected7)

            step_7_name = '''7. Add more 5 rules
                                Then click Add button'''
            list_check_in_step_7 = ['After add 5 rules. Check ADD button disabled']
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
            list_step_fail.append('7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_06_SECURITY_Confirm_Parental_Control_rule_Modification(self):
        self.key = 'SECURITY_06'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        SOCIAL_NW = get_config('SECURITY', 'security4_social_nw', input_data_path)
        USER_DEFINE = get_config('SECURITY', 'security4_user_define', input_data_path)
        FACEBOOK = get_config('SECURITY', 'security4_facebook', input_data_path)
        GOOGLE = get_config('SECURITY', 'security4_google', input_data_path)

        MAC_1 = '1A:2B:3C:4D:5E:6F'
        MAC1_VALUE = MAC_1.replace(':', '')
        MAC_2 = '22:22:22:22:22:22'
        MAC2_VALUE = MAC_2.replace(':', '')
        try:
            grand_login(driver)

            # Goto media share USB
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            if len(parental_field_input) > 0:
                #  New
                ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Parental Control']
            check = assert_list(list_actual1, list_expected1)

            step_1_2_name = '1, 2. Go to Security > Parental Control, enable the Parental Control function and set a parental code.'
            list_check_in_step_1_2 = ['Security > Parental Control page should be displayed.']
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
            rule_block = driver.find_element_by_css_selector(parental_rule_card)

            while len(rule_block.find_elements_by_css_selector(delete_cls)) > 0:
                rule_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            driver.refresh()
            wait_popup_disappear(driver, dialog_loading)
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            if len(parental_field_input) > 0:
                #  New
                ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            # Control Rule
            rule_block = driver.find_element_by_css_selector(parental_rule_card)
            # Click Add 1
            rule_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)
            # Edit mode
            edit_field = rule_block.find_element_by_css_selector(edit_mode)

            device_name_field = edit_field.find_element_by_css_selector(name_cls)
            device_name_field.find_element_by_css_selector(input).click()

            # Select all
            opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
            for i in range(len(opts) - 1):
                opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
                opts[0].click()
                break

            device_name_field.find_element_by_css_selector(input).click()
            driver.find_element_by_css_selector('.user-define').click()
            driver.find_element_by_css_selector('input[name="input-field"]').send_keys(MAC1_VALUE)

            # Setup the filter
            edit_field.find_element_by_css_selector('.service-filter').find_element_by_css_selector(apply).click()
            time.sleep(0.5)

            time.sleep(1)
            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == SOCIAL_NW:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()

                    ls_service_sub = f.find_elements_by_css_selector('.service-sub-item-wrap')
                    for s in ls_service_sub:
                        ActionChains(driver).move_to_element(s).perform()
                        if s.text == 'facebook':
                            s.click()

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == USER_DEFINE:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()
                    check_item_inner = driver.find_elements_by_css_selector('.child-item .item-inner')
                    ActionChains(driver).move_to_element(check_item_inner[0]).perform()
                    time.sleep(0.5)
                    check_item_exist = any([i.text == 'google.com' for i in check_item_inner])
                    print(check_item_exist)
                    time.sleep(1)
                    if not check_item_exist:
                        # Add url
                        driver.find_element_by_css_selector(add_class).click()
                        f.find_element_by_css_selector(input).send_keys('google.com')
                        time.sleep(1)
                        f.find_element_by_css_selector(btn_save).click()
            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                ActionChains(driver).move_to_element(s).perform()
                if s.text == 'google.com':
                    s.click()
                    break

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for s in ls_service:
                ActionChains(driver).move_to_element(s).perform()
                if s.find_element_by_css_selector('span').text not in ['Social Network', 'User Define']:
                    s.click()
                    ls_service_sub = s.find_elements_by_css_selector('.service-sub-item-wrap')
                    random_sub = random.choice(ls_service_sub)
                    ActionChains(driver).move_to_element(random_sub).perform()
                    random_sub.click()
            sub_title = driver.find_element_by_css_selector('.sub-title').text

            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()

            # Schedule
            edit_field.find_element_by_css_selector('.set-schedule').find_element_by_css_selector(apply).click()
            time.sleep(1)

            # +++++++++++++++
            now = datetime.now()
            weekdays = now.strftime('%a').upper()
            hourday = int(now.strftime('%H'))

            dict_transfer = {
                "SUN": 1,
                "MON": 2,
                "TUE": 3,
                "WED": 4,
                "THU": 5,
                "FRI": 6,
                "SAT": 7
            }
            weekday_index = [dict_transfer[i] for i in dict_transfer.keys() if i == weekdays][0]
            hourday_index_1 = hourday + 3
            hourday_index_2 = hourday_index_1 + 1

            # Click ALL to set avalable
            week_day_all = driver.find_elements_by_css_selector(f'tr:nth-child({weekday_index})>.all.hight-light')
            if len(week_day_all) > 0:
                week_day_all[0].click()
            time.sleep(1)

            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_1})').click()
            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_2})').click()
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_save).click()
            wait_popup_disappear(driver, dialog_loading)



            exp_service = ['Social Network[1]', 'User Define[1]']
            number_of_total_nw = [i.text for i in driver.find_elements_by_css_selector('.filter-item')]
            time.sleep(0.5)
            check_service_filter = all([i in number_of_total_nw for i in exp_service])

            # Check block schedule
            block_schedule_value = driver.find_elements_by_css_selector('.schedule')[-1].text

            list_actual3 = [sub_title, check_service_filter, block_schedule_value]
            list_expected3 = [exp_subtitle_set_website_app, True, exp_block_schedule_value]
            check = assert_list(list_actual3, list_expected3)

            step_3_name = '''3. Click the Add button and change below settings:
                - Device Name/MAC Address: Select a connected device from dropdown list or enter a MAC address manually (need to check both methods)
                - Service Filters:
                + Click "Setup the Filters" and choose "facebook" in Social Network category
                + Add a "User Define" filter for "google.com" and select the created filter 
                + Select 9 other service for the dropdown list then save the filter
                - Block Schedule: Click "Setup the Schedule" and choose the schedule contains the testing time
                and click Save the rule'''
            list_check_in_step_3 = ['Check Set the Websites/Apps Sub title',
                                    'Check Social Network[1] and User Define[1] is displayed',
                                    'Check Block schedule text. ']
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
            # CLick Edit
            parental_rule = driver.find_element_by_css_selector(parental_rule_card)
            created_row = parental_rule.find_elements_by_css_selector(rows)[-1]
            created_row.find_element_by_css_selector(edit_cls).click()
            time.sleep(1)

            rule_block = driver.find_element_by_css_selector(parental_rule_card)
            edit_field = rule_block.find_element_by_css_selector(edit_mode)
            device_name_field = edit_field.find_element_by_css_selector(name_cls)
            device_name_field.find_element_by_css_selector(input).click()
            driver.find_element_by_css_selector('.user-define').click()
            driver.find_element_by_css_selector('input[name="input-field"]').send_keys(MAC2_VALUE)

            # Setup the filter
            edit_field.find_element_by_css_selector('.service-filter').find_element_by_css_selector(apply).click()
            time.sleep(0.5)

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if len(f.find_elements_by_css_selector('.selected-icon')) > 0:
                    f.click()
                    ls_service_sub = f.find_elements_by_css_selector('.service-sub-item-wrap')
                    for s in ls_service_sub:
                        ActionChains(driver).move_to_element(s).perform()
                        if len(s.find_elements_by_css_selector('.selected-icon')) > 0:
                            s.click()


            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == USER_DEFINE:
                    ActionChains(driver).move_to_element(f).perform()
                    f.click()
                    check_item_inner = driver.find_elements_by_css_selector('.child-item .item-inner')
                    ActionChains(driver).move_to_element(check_item_inner[0]).perform()
                    time.sleep(0.5)
                    check_item_exist = any([i.text == 'google.com' for i in check_item_inner])
                    print(check_item_exist)
                    time.sleep(1)
                    if not check_item_exist:
                        # Add url
                        driver.find_element_by_css_selector(add_class).click()
                        f.find_element_by_css_selector(input).send_keys('google.com')
                        time.sleep(1)
                        f.find_element_by_css_selector(btn_save).click()
            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                ActionChains(driver).move_to_element(s).perform()
                if s.text == 'google.com':
                    s.click()
                    break

            time.sleep(1)
            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:

                if f.find_element_by_css_selector('span').text == 'Mail':
                    # print(f.text)
                    ActionChains(driver).move_to_element(f).perform()

                    if len(f.find_elements_by_css_selector('.on-show')) == 0:
                        f.click()
                    else:
                        ls_service_sub = f.find_elements_by_css_selector('.service-sub-item-wrap')
                        for s in ls_service_sub:
                            ActionChains(driver).move_to_element(s).perform()
                            print(s.text)
                            if s.text in ['gmail', 'outlook']:
                                s.click()
                                time.sleep(0.5)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            # Schedule
            edit_field.find_element_by_css_selector('.set-schedule').find_element_by_css_selector(apply).click()
            time.sleep(1)
            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>.all').click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_save).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            ls_mac_device = [i.text.splitlines()[-1] for i in driver.find_elements_by_css_selector('.name .device-item')]
            check_mac = MAC_2 in ls_mac_device

            # ls_mac_device = [i.text.splitlines()[-1] for i in
            #                  driver.find_elements_by_css_selector('.name .device-item')]
            # check_mac = MAC_2 in ls_mac_device
            block_schedule_value = driver.find_elements_by_css_selector('.schedule')[-1].text

            list_actual4 = [check_mac, check_service_filter, block_schedule_value]
            list_expected4 = [return_true, True, 'Always Block']
            check = assert_list(list_actual4, list_expected4)

            step_4_name = '''4. Click on Edit icon to change the setting of item in control rule.
                        - Change the setting for MAC address/ Filters/ schedule and Save.
                        + Service Filters: gmail, outlook
                        + Schedule: Always Block.
                        - Then check Paretal Control list information.'''
            list_check_in_step_4 = ['Check MAC is correct',
                                    'Check Mail[2] and User Define[1] is displayed',
                                    'Check Block schedule text. ']
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

    def test_07_SECURITY_Confirm_Parental_Control_rule_Deletion(self):
        self.key = 'SECURITY_07'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        SOCIAL_NW = get_config('SECURITY', 'security4_social_nw', input_data_path)
        USER_DEFINE = get_config('SECURITY', 'security4_user_define', input_data_path)
        FACEBOOK = get_config('SECURITY', 'security4_facebook', input_data_path)
        GOOGLE = get_config('SECURITY', 'security4_google', input_data_path)

        MAC_1 = '1A:2B:3C:4D:5E:6F'
        MAC1_VALUE = MAC_1.replace(':', '')
        MAC_2 = '22:22:22:22:22:22'
        MAC2_VALUE = MAC_2.replace(':', '')
        try:
            grand_login(driver)

            # Goto media share USB
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            if len(parental_field_input) > 0:
                #  New
                ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Parental Control']
            check = assert_list(list_actual1, list_expected1)

            step_1_2_name = '1, 2. Go to Security > Parental Control, enable the Parental Control function and set a parental code.'
            list_check_in_step_1_2 = ['Security > Parental Control page should be displayed.']
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
            rule_block = driver.find_element_by_css_selector(parental_rule_card)

            while len(rule_block.find_elements_by_css_selector(delete_cls)) > 0:
                rule_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Control Rule
            rule_block = driver.find_element_by_css_selector(parental_rule_card)
            # Click Add 1
            rule_block.find_element_by_css_selector(add_class).click()
            time.sleep(1)
            # Edit mode
            edit_field = rule_block.find_element_by_css_selector(edit_mode)

            device_name_field = edit_field.find_element_by_css_selector(name_cls)
            device_name_field.find_element_by_css_selector(input).click()

            # Select all
            opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
            for i in range(len(opts) - 1):
                opts = device_name_field.find_elements_by_css_selector(secure_value_in_drop_down)
                opts[0].click()
                break

            device_name_field.find_element_by_css_selector(input).click()
            driver.find_element_by_css_selector('.user-define').click()
            driver.find_element_by_css_selector('input[name="input-field"]').send_keys(MAC1_VALUE)

            # Setup the filter
            edit_field.find_element_by_css_selector('.service-filter').find_element_by_css_selector(apply).click()
            time.sleep(0.5)

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == SOCIAL_NW:
                    f.click()
                    break
            sub_title = driver.find_element_by_css_selector('.sub-title').text
            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                if s.text == FACEBOOK:
                    if not len(s.find_elements_by_css_selector('.selected-icon')) > 0:
                        s.click()

                else:
                    time.sleep(0.2)
                    s.click()

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == USER_DEFINE:
                    f.click()
                    check_item_inner = driver.find_elements_by_css_selector('.child-item .item-inner')
                    check_item_exist = any([i.text == GOOGLE for i in check_item_inner])
                    if not check_item_exist:
                        # Add url
                        driver.find_element_by_css_selector(add_class).click()
                        f.find_element_by_css_selector(input).send_keys(GOOGLE)
                        time.sleep(1)
                        f.find_element_by_css_selector(btn_save).click()
                        time.sleep(1)

            # Save
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()

            # Schedule
            edit_field.find_element_by_css_selector('.set-schedule').find_element_by_css_selector(apply).click()
            time.sleep(1)

            # +++++++++++++++
            now = datetime.now()
            weekdays = now.strftime('%a').upper()
            hourday = int(now.strftime('%H'))

            dict_transfer = {
                "SUN": 1,
                "MON": 2,
                "TUE": 3,
                "WED": 4,
                "THU": 5,
                "FRI": 6,
                "SAT": 7
            }
            weekday_index = [dict_transfer[i] for i in dict_transfer.keys() if i == weekdays][0]
            hourday_index_1 = hourday + 3
            hourday_index_2 = hourday_index_1 + 1

            # Click ALL to set avalable
            week_day_all = driver.find_elements_by_css_selector(f'tr:nth-child({weekday_index})>.all.hight-light')
            if len(week_day_all) > 0:
                week_day_all[0].click()
            time.sleep(1)

            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_1})').click()
            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>:nth-child({hourday_index_2})').click()
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_save).click()
            wait_popup_disappear(driver, dialog_loading)

            time.sleep(1)
            driver.find_element_by_css_selector('.filter-count').click()
            time.sleep(1)
            number_of_total_nw = len(driver.find_elements_by_css_selector('.service-item'))
            # Check block schedule
            block_schedule_value = driver.find_elements_by_css_selector('.schedule')[-1].text

            list_actual3 = [sub_title, number_of_total_nw, block_schedule_value]
            list_expected3 = [exp_subtitle_set_website_app, 10, exp_block_schedule_value]
            check = assert_list(list_actual3, list_expected3)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
            #     f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            step_3_name = '''3. Click the Add button and change below settings:
                        - Device Name/MAC Address: Select a connected device from dropdown list or enter a MAC address manually (need to check both methods)
                        - Service Filters:
                        + Click "Setup the Filters" and choose "facebook" in Social Network category
                        + Add a "User Define" filter for "google.com" and select the created filter 
                        + Select 9 other service for the dropdown list then save the filter
                        - Block Schedule: Click "Setup the Schedule" and choose the schedule contains the testing time
                        and click Save the rule'''
            list_check_in_step_3 = ['Check Websites/Apps Sub title',
                                    'Check number of Social NW',
                                    'Check Block schedule text']
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
            # CLick Delete
            parental_rule = driver.find_element_by_css_selector(parental_rule_card)
            created_row = parental_rule.find_elements_by_css_selector(rows)[-1]
            created_row.find_element_by_css_selector(delete_cls).click()
            time.sleep(1)
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            parental_rule = driver.find_element_by_css_selector(parental_rule_card)
            remain_row = len(parental_rule.find_elements_by_css_selector(rows))

            list_actual4 = [remain_row]
            list_expected4 = [0]
            check = assert_list(list_actual4, list_expected4)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 4. Delete rule: Check number of remain row = 0. '
            #     f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            step_4_name = '''4. Click on Delete icon to delete item in control rule and select OK.'''
            list_check_in_step_4 = ['Check number of remain row = 0']
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

    def test_23_SECURITY_Edit_IP_Port_Filtering(self):
        self.key = 'SECURITY_23'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        DESC_VALUE = 'Test01'
        IP_ADDRESS_1 = '192.168.1.5'
        IP_ADDRESS_1_SPLIT = IP_ADDRESS_1.split('.')[-1]
        PORT_START_END_1 = '10-10'
        PORT_START_END_1_SPLIT = PORT_START_END_1.split('-')
        PROTOCOL_TYPE = 'TCP'

        IP_ADDRESS_2 = '192.168.1.6'
        IP_ADDRESS_2_SPLIT = IP_ADDRESS_2.split('.')[-1]
        try:
            grand_login(driver)

            try:
                goto_menu(driver, security_tab, security_filtering_tab)
            except:
                parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
                if len(parental_field_input) > 0:
                    #  New
                    ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                    time.sleep(0.5)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    parental_code = driver.find_element_by_css_selector(parental_code_card)
                    parental_code_select = parental_code.find_element_by_css_selector(select)
                    if parental_code_select.find_element_by_css_selector(input).is_selected():
                        parental_code_select.click()
                        wait_popup_disappear(driver, dialog_loading)
                    goto_menu(driver, security_tab, security_filtering_tab)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Filtering']
            check = assert_list(list_actual1, list_expected1)
            step_1_2_name = '1, 2. Access and Login. Go to home page > Security > Filtering.'
            list_check_in_step_1_2 = ['Security > Filtering page should be displayed.']
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
            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)

            while len(filter_block.find_elements_by_css_selector(delete_cls)) > 0:
                filter_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Add  a IP Port Filtering
            add_a_ip_port_filtering(driver, DESC_VALUE, IP_ADDRESS_1_SPLIT, PORT_START_END_1_SPLIT, PROTOCOL_TYPE)

            time.sleep(1)
            get_table_value = get_ip_port_filtering_table(driver)

            list_actual3 = get_table_value[-1]
            list_expected3 = [return_true, DESC_VALUE, IP_ADDRESS_1, PORT_START_END_1, PROTOCOL_TYPE]
            check = assert_list(list_actual3, list_expected3)

            step_3_name = '3. Add a IP/Port Filtering: Description/ IP Address/ Port(Start - End)/ Protocol. Then click Save.'
            list_check_in_step_3 = ['Check rule row is active',
                                    'Check description',
                                    'Check IP address',
                                    'Check Port Start-End',
                                    'Check Protocol type']
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
            # CLick Edit
            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)
            created_row = filter_block.find_elements_by_css_selector(rows)[-1]
            created_row.find_element_by_css_selector(edit_cls).click()
            time.sleep(1)
            # Change IP
            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)
            # Edit mode
            edit_field = filter_block.find_element_by_css_selector(edit_mode)
            for i in range(2):
                ip_address = edit_field.find_element_by_css_selector(ip_address_cls)
                ip_address_box = ip_address.find_element_by_css_selector(input)
                ip_address_box.clear()
                ip_address_box.clear()
                ip_address_box.send_keys(IP_ADDRESS_2_SPLIT)

            driver.find_element_by_css_selector(btn_save).click()
            time.sleep(2)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            # Get Value
            get_table_value = get_ip_port_filtering_table(driver)

            list_actual4 = get_table_value[-1]
            list_expected4 = [return_true, DESC_VALUE, IP_ADDRESS_2, PORT_START_END_1, PROTOCOL_TYPE]
            check = assert_list(list_actual4, list_expected4)

            step_4_name = '4, 5. Edit IP/Port filtering then save. Check row.'
            list_check_in_step_4 = ['Check rule row is active',
                                    'Check description',
                                    'Check IP address',
                                    'Check Port Start-End',
                                    'Check Protocol type']
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
            list_step_fail.append('4, 5. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_24_SECURITY_Delete_IP_Port_Filtering(self):
        self.key = 'SECURITY_24'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        DESC_VALUE = 'Test01'
        IP_ADDRESS_1 = get_value_from_ipconfig('Ethernet adapter Ethernet', 'IPv4 Address').replace('(Preferred)', '')
        IP_ADDRESS_1_SPLIT = IP_ADDRESS_1.split('.')[-1]
        PORT_START_END_1 = '10-10'
        PORT_START_END_1_SPLIT = PORT_START_END_1.split('-')
        PROTOCOL_TYPE = 'TCP'

        try:
            grand_login(driver)

            try:
                goto_menu(driver, security_tab, security_filtering_tab)
            except:
                parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
                if len(parental_field_input) > 0:
                    #  New
                    ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                    time.sleep(0.5)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    parental_code = driver.find_element_by_css_selector(parental_code_card)
                    parental_code_select = parental_code.find_element_by_css_selector(select)
                    if parental_code_select.find_element_by_css_selector(input).is_selected():
                        parental_code_select.click()
                        wait_popup_disappear(driver, dialog_loading)
                    goto_menu(driver, security_tab, security_filtering_tab)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Filtering']
            check = assert_list(list_actual1, list_expected1)
            step_1_2_name = '1, 2. Access and Login. Go to Homepage > Security > Filtering page.'
            list_check_in_step_1_2 = ['Check page Security > Filtering is displayed.']
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
            # self.list_steps.append(
            #     f'[Fail] 1, 2. Login. Goto Filtering page. Check page title. '
            #     f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong.')

        try:
            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)

            while len(filter_block.find_elements_by_css_selector(delete_cls)) > 0:
                filter_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Add  a IP Port Filtering
            add_a_ip_port_filtering(driver, DESC_VALUE, IP_ADDRESS_1_SPLIT, PORT_START_END_1_SPLIT, PROTOCOL_TYPE)

            time.sleep(1)
            get_table_value = get_ip_port_filtering_table(driver)

            list_actual3 = get_table_value[-1]
            list_expected3 = [return_true, DESC_VALUE, IP_ADDRESS_1, PORT_START_END_1, PROTOCOL_TYPE]
            check = assert_list(list_actual3, list_expected3)
            step_3_name = '3. Click +ADD. Input Description/ IP Address/ Port(Start-End)/Protocol. Then Click Save. Click Apply. Click OK.'
            list_check_in_step_3 = ['Check rule Is active',
                                    'Check Description',
                                    'Check IP address',
                                    'Check Start - End port',
                                    'Check Protocol type.']
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
            # self.list_steps.append(
            #     f'[Fail] 3. Add a IP/Port Filtering: Check Row have just added. '
            #     f'Is active, Description, IP, Port Start End, Portocol Type. '
            #     f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            # CLick Delete
            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)
            created_row = filter_block.find_elements_by_css_selector(rows)[-1]

            created_row.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_cancel).click()

            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)
            remain_row = len(filter_block.find_elements_by_css_selector(rows))

            list_actual = [remain_row]
            list_expected = [1]
            check = assert_list(list_actual, list_expected)

            step_4_name = '4. Click on Delete on list then click Cancel.'
            list_check_in_step_4 = ['Check the row was not deleted']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
        except:
            # self.list_steps.append(
            #     f'[Fail] 4. Delete IP Port Filtering. Click Cancel: Check number of remain row = 1. '
            #     f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual,
                    list_expected=list_expected
                )
            )
            list_step_fail.append('4. Assertion wong.')

        try:
            # CLick Delete
            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)
            created_row = filter_block.find_elements_by_css_selector(rows)[-1]

            created_row.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            filter_block = driver.find_element_by_css_selector(ele_ip_port_filtering)
            remain_row = len(filter_block.find_elements_by_css_selector(rows))

            list_actual4 = [remain_row]
            list_expected4 = [0]
            check = assert_list(list_actual4, list_expected4)

            step_5_6_name = '5, 6. Click on Delete on list then click OK.'
            list_check_in_step_5_6 = ['Check the row was deleted']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )

            self.list_steps.append('[END TC]')
        except:
            # self.list_steps.append(
            #     f'[Fail] 5, 6. Delete IP Port Filtering. Click OK: Check number of remain row = 0. '
            #     f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_name,
                    list_check_in_step=list_check_in_step_5_6,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5, 6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_25_SECURITY_Check_MAC_Filtering_operation(self):
        self.key = 'SECURITY_25'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===============================================================
        PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
        PHYSICAL_MAC = get_value_from_ipconfig('Ethernet adapter Ethernet', 'Physical Address').replace('-', ':')
        HOST_NAME = get_value_from_ipconfig('Windows IP Configuration', 'Host Name')

        grand_login(driver)
        goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
        # Get Wireless 2G Information
        block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]

        wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
        wifi_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=False)

        try:
            grand_login(driver)
            # Goto media share USB
            try:
                goto_menu(driver, security_tab, security_filtering_tab)
            except:
                parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
                if len(parental_field_input) > 0:
                    #  New
                    ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                    time.sleep(0.5)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    parental_code = driver.find_element_by_css_selector(parental_code_card)
                    parental_code_select = parental_code.find_element_by_css_selector(select)
                    if parental_code_select.find_element_by_css_selector(input).is_selected():
                        parental_code_select.click()
                        wait_popup_disappear(driver, dialog_loading)
                    goto_menu(driver, security_tab, security_filtering_tab)

            wait_popup_disappear(driver, dialog_loading)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Filtering']
            check = assert_list(list_actual1, list_expected1)

            step_1_2_name = '1, 2. Access and Login. Go to Homepage > Security > Filtering page.'
            list_check_in_step_1_2 = ['Check page Security > Filtering is displayed.']
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
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)

            while len(mac_block.find_elements_by_css_selector(delete_cls)) > 0:
                mac_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Add  a IP Port Filtering
            add_a_mac_filtering(driver)
            time.sleep(1)
            get_table_value = get_mac_filtering_table(driver)

            list_actual3 = get_table_value[-1]
            list_expected3 = [return_true, HOST_NAME, PHYSICAL_MAC]
            check = assert_list(list_actual3, list_expected3)

            step_3_name = '3. Click +ADD. Input Host name/ Physical MAC. Then Click Save. Click Apply.'
            list_check_in_step_3 = ['Check MAC filtering Is active',
                                    'Check Host name',
                                    'Check Check Physical MAC']
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
            check_google = check_connect_to_google()
            check_youtube = check_connect_to_youtube()

            list_actual4 = [check_google, check_youtube]
            list_expected4 = [return_false] * 2
            check = assert_list(list_actual4, list_expected4)

            step_4_name = '4. External communication from registered PC.'
            list_check_in_step_4 = ['Check Can not access to external to Google: not access',
                                    'Check Can not access to external to Youtube: not access']
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
            # Disconnect Ethernet
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            interface_connect_disconnect('Wi-Fi', 'enable')
            connect_wifi_by_command(wifi_2g_name, wifi_2g_pw)
            time.sleep(5)
            # Login again
            grand_login(driver)
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Get table
            get_table_value_2 = get_mac_filtering_table(driver)

            list_actual5 = get_table_value_2[-1]
            list_expected5 = [return_true, HOST_NAME, PHYSICAL_MAC]
            check = assert_list(list_actual5, list_expected5)

            step_5_name = '5. Disconnect ethernet then connect client PC to wireless of DUT. Login then Go to Security > Filtering page. Check list MAC Filtering list.'
            list_check_in_step_5 = ['Check MAC filtering Is active',
                                    'Check Host name',
                                    'Check Check Physical MAC']
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
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            mac_block.find_elements_by_css_selector(select)[0].click()

            mac_block.find_element_by_css_selector(apply).click()
            time.sleep(2)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(2)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            get_table_value_3 = get_mac_filtering_table(driver)

            list_actual6 = get_table_value_3[-1]
            list_expected6 = [return_false, HOST_NAME, PHYSICAL_MAC]
            check = assert_list(list_actual6, list_expected6)

            step_6_name = '6 . Disable a rule was added at step 3 and lick "Apply" button > OK button'
            list_check_in_step_6 = ['Check MAC filtering Is deactive',
                                    'Check Host name',
                                    'Check Check Physical MAC']
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
            list_step_fail.append('6. Assertion wong.')

        try:
            os.system('netsh wlan disconnect')
            time.sleep(2)
            # Disconnect Wireless
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            check_ethernet = get_value_from_ipconfig('Ethernet adapter Ethernet', 'Physical Address')
            check_ethernet = check_ethernet != 'Block or field error.'

            list_actual7 = [check_ethernet]
            list_expected7 = [return_true]
            check = assert_list(list_actual7, list_expected7)
            step_7_name = '7. Disable wireless, enable LAN port of PC '
            list_check_in_step_7 = ['Check ethernet available']
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
            list_step_fail.append('7. Assertion wong.')

        try:
            check_google_2 = check_connect_to_google()
            check_youtube_2 = check_connect_to_youtube()

            list_actual8 = [check_google_2, check_youtube_2]
            list_expected8 = [return_true] * 2
            check = assert_list(list_actual8, list_expected8)
            step_8_name = '8. External communication from registerd PC.'
            list_check_in_step_8 = ['Check Can access to external to Google: access',
                                    'Check Can access to external to Youtube: access']
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
            list_step_fail.append('8. Assertion wong.')

        try:
            grand_login(driver)
            #
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)
            ls_mac = list()
            for i in range(31):
                tmp_mac = random_mac_address()
                if tmp_mac not in ls_mac:
                    add_a_mac_filtering(driver, tmp_mac)
                    ls_mac.append(tmp_mac)
                else:
                    tmp_mac = random_mac_address()
                    add_a_mac_filtering(driver, tmp_mac)
                    ls_mac.append(tmp_mac)
                # while tmp_mac in ls_mac:
                #     tmp_mac = random_mac_address()
                #     if tmp_mac in ls_mac:
                #         tmp_mac = random_mac_address()
                #     ls_mac.append(tmp_mac)
                #     while tmp_mac in ls_mac:
                #         tmp_mac = random_mac_address()
                #         ls_mac.append(tmp_mac)
                #     add_a_mac_filtering(driver, tmp_mac)
                #     time.sleep(1).append(tmp_mac)
                # add_a_mac_filtering(driver, tmp_mac)
                # time.sleep(1)

            time.sleep(1)
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            check_add_btn_disabled = mac_block.find_element_by_css_selector(add_class).is_enabled()

            list_actual9 = [check_add_btn_disabled]
            list_expected9 = [return_false]
            check = assert_list(list_actual9, list_expected9)
            step_9_name = '9. Re-do step 3 check the creation of 32 max entry'
            list_check_in_step_9 = ['After 32 rules are added, "+ADD" button is not clickable']
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
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_26_SECURITY_Delete_MAC_Filtering_rule(self):
        self.key = 'SECURITY_26'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        PHYSICAL_MAC = get_value_from_ipconfig('Ethernet adapter Ethernet', 'Physical Address').replace('-', ':')
        HOST_NAME = get_value_from_ipconfig('Windows IP Configuration', 'Host Name')

        grand_login(driver)
        goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
        # Get Wireless 2G Information
        block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]

        wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
        wifi_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=False)


        try:
            grand_login(driver)
            # Goto media share USB
            try:
                goto_menu(driver, security_tab, security_filtering_tab)
            except:
                parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
                if len(parental_field_input) > 0:
                    #  New
                    ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                    time.sleep(0.5)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    parental_code = driver.find_element_by_css_selector(parental_code_card)
                    parental_code_select = parental_code.find_element_by_css_selector(select)
                    if parental_code_select.find_element_by_css_selector(input).is_selected():
                        parental_code_select.click()
                        wait_popup_disappear(driver, dialog_loading)
                    goto_menu(driver, security_tab, security_filtering_tab)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security > Filtering']
            check = assert_list(list_actual1, list_expected1)
            step_1_2_name = '1, 2. Access and Login. Go to Homepage > Security > Filtering page.'
            list_check_in_step_1_2 = ['Check page Security > Filtering is displayed.']
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
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)

            while len(mac_block.find_elements_by_css_selector(delete_cls)) > 0:
                mac_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # Add  a IP Port Filtering
            add_a_mac_filtering(driver)
            time.sleep(1)
            get_table_value = get_mac_filtering_table(driver)

            list_actual3 = get_table_value[-1]
            list_expected3 = [return_true, HOST_NAME, PHYSICAL_MAC]
            check = assert_list(list_actual3, list_expected3)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 3. Add a MAC Filtering: Check Row have just added. '
            #     f'Is active, Host name and MAC address. '
            #     f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            step_3_name = '3. Click "+ADD" button > click on "Select the device" list box > select MAC address of PC connected to DUT via LAN port. Click Save and Apply.'
            list_check_in_step_3 = ['Check MAC filtering Is active',
                                    'Check Host name',
                                    'Check Check Physical MAC']
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
            # Disconnect Ethernet
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
            # Connect Wifi 2.4 Ghz
            connect_wifi_by_command(wifi_2g_name, wifi_2g_pw)
            time.sleep(5)
            # Login again
            grand_login(driver)
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Get table
            get_table_value_2 = get_mac_filtering_table(driver)

            list_actual5 = get_table_value_2[-1]
            list_expected5 = [return_true, HOST_NAME, PHYSICAL_MAC]
            check = assert_list(list_actual5, list_expected5)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 4.0. Disconnect LAN. Connect 2GHz Wifi. Login again. '
            #     f'Check Mac filtering table: Is active, Device Name, MAC address.  '
            #     f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            step_4_name = '4.0. Disconnect LAN. Connect 2GHz Wifi. Login again. Go to Mac filtering. Verify information have just created'
            list_check_in_step_4 = ['Check MAC filtering Is active',
                                    'Check Host name',
                                    'Check Check Physical MAC']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('4.0. Assertion wong.')

        try:
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)

            # CLick Delete
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            created_row = mac_block.find_elements_by_css_selector(rows)[-1]

            created_row.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_cancel).click()

            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            remain_row = len(mac_block.find_elements_by_css_selector(rows))

            list_actual = [remain_row]
            list_expected = [1]
            check = assert_list(list_actual, list_expected)

            step_6_name = '4.1 Click "Delete" icon on the rule > select "Cancel" button'
            list_check_in_step_6 = ['Number of remain row = 1']
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
            list_step_fail.append('4. Assertion wong.')

        try:
            # CLick Delete
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            created_row = mac_block.find_elements_by_css_selector(rows)[-1]

            created_row.find_element_by_css_selector(delete_cls).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            remain_row = len(mac_block.find_elements_by_css_selector(rows))

            list_actual7 = [remain_row]
            list_expected7 = [0]
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)

            check = assert_list(list_actual7, list_expected7)
            # self.assertTrue(check["result"])
            # self.list_steps.append(
            #     f'[Pass] 5, 6. Delete MAC Filtering. Click OK: Check number of remain row = 0. '
            #     f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            step_7_name = f'5, 6. Click "Delete" icon on the rule > select "OK" button. Check MAC Filtering list after delete rule'
            list_check_in_step_7 = ['Check Number of remain row = 0']
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
            list_step_fail.append('5, 6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_27_SECURITY_Security_Check(self):
        self.key = 'SECURITY_27'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        NEW_PW_1 = '1qaz'
        NEW_PW_2 = 'abc123@'
        factory_dut()
        try:
            grand_login(driver)
            # Goto media share USB
            try:
                goto_menu(driver, security_tab, security_selfcheck_tab)
            except:
                parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                PARENTAL_CODE_KEY = get_config('SECURITY', 'parental_code')
                if len(parental_field_input) > 0:
                    #  New
                    ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                    time.sleep(0.5)
                    driver.find_element_by_css_selector(btn_ok).click()
                    wait_popup_disappear(driver, dialog_loading)
                    parental_code = driver.find_element_by_css_selector(parental_code_card)
                    parental_code_select = parental_code.find_element_by_css_selector(select)
                    if parental_code_select.find_element_by_css_selector(input).is_selected():
                        parental_code_select.click()
                        wait_popup_disappear(driver, dialog_loading)
                    goto_menu(driver, security_tab, security_selfcheck_tab)

            check_title = driver.find_element_by_css_selector(ele_title_page).text

            list_actual1 = [check_title]
            list_expected1 = ['Security check']
            check = assert_list(list_actual1, list_expected1)

            step_1_2_name = '1, 2. Access and Login.  Go to Home page > Security > Security Check.'
            list_check_in_step_1_2 = ['Check page Security > Filtering is displayed.']
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
            # Check Security list
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            list_secure_label = secure_card.find_elements_by_css_selector(label_name_in_2g)
            list_secure_label_text = [i.text for i in list_secure_label]

            list_actual3 = list_secure_label_text
            list_expected3 = ['Login Password Changed',
                              'Login Password Security Level',
                              '2.4GHz Wireless Password Security Type',
                              '5GHz Wireless Password Security Type',
                              'UPnP Service',
                              'Remote Access',
                              'Ping from WAN',
                              'DMZ',
                              'Port Triggering',
                              'Port Forwarding',
                              'Anonymous Login to FTP Server']
            check = assert_list(list_actual3, list_expected3)
            step_3_name = '3. Check the Security list.'
            list_check_in_step_3 = [f'Check Login Password Changed',
                                    f'Check Login Password Security Level',
                                    f'Check 2.4GHz Wireless Password Security Type',
                                    f'Check 5GHz Wireless Password Security Type',
                                    f'Check UPnP Service',
                                    f'Check Remote Access',
                                    f'Check Ping from WAN',
                                    f'Check DMZ',
                                    f'Check Port Triggering',
                                    f'Check Port Forwarding',
                                    f'Check Anonymous Login to FTP Server']
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
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Login Password Changed':
                    check_lg_pw_changed_value = v.text
                    break

            list_actual4 = [check_lg_pw_changed_value]
            list_expected4 = ['Yes']
            check = assert_list(list_actual4, list_expected4)

            step_4_name = '4. Check value of Login Password Changed.'
            list_check_in_step_4 = [f'Check value is Yes']
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
            CURRENT_PW = get_config('ACCOUNT', 'password')

            goto_system(driver, ele_sys_change_pw)
            change_password(driver, CURRENT_PW, NEW_PW_1)
            time.sleep(1)
            #
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PW_1)
            time.sleep(1)
            # =======================================================
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Login Password Security Level':
                    check_lg_pw_changed_value_2 = v.text
                    break

            list_actual5 = [check_lg_pw_changed_value_2]
            list_expected5 = ['Medium']
            check = assert_list(list_actual5, list_expected5)

            step_5_name = '5. Go to "System" in the header > select Change Password , set new password is Good. Re-do step 2 to check value of Login Password Security Level'
            list_check_in_step_5 = [f'Check value of Login Password Security Level is: Medium']
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
            CURRENT_PW = get_config('ACCOUNT', 'password')

            goto_system(driver, ele_sys_change_pw)
            change_password(driver, CURRENT_PW, NEW_PW_2)
            time.sleep(1)
            #
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PW_2)
            time.sleep(1)
            # =======================================================
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Login Password Security Level':
                    check_lg_pw_changed_value_3 = v.text
                    break

            list_actual6 = [check_lg_pw_changed_value_3]
            list_expected6 = ['Strong']
            check = assert_list(list_actual6, list_expected6)

            step_6_name = '6. Re-do step 5 to set new password is Strong. Check value of Login Password Security Level'
            list_check_in_step_6 = [f'Value of Login Password Security Level is: Strong']
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
            list_step_fail.append('6. Assertion wong.')
        # Step 7
        try:
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)

            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            # Change Security type
            wireless_change_choose_option(block_2g_card, secure_value_field, VALUE_OPTION='NONE')

            block_2g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '2.4GHz Wireless Password Security Type':
                    check_24g_wireless = v.text
                    time.sleep(1)
                    v.click()
                    time.sleep(1)
                    break
            check_current_screen = detect_current_menu(driver)

            list_actual7 = [check_24g_wireless, check_current_screen]
            list_expected7 = ['Weak(None)', ('WIRELESS', 'Primary Network')]
            check = assert_list(list_actual7, list_expected7)
            step_7_name = '7. Change Wifi 24GHz to NONE. Re-do step 2 to check value of 2.4GHz Wireless Password Security Type. Click to link text. Check Re-direct to Wireless > Primary Network.'
            list_check_in_step_7 = [f'Value of  2.4GHz Wireless Password Security Type is: Weak(None)',
                                    'Move to the Wireless > Primary Network screen']
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
            list_step_fail.append('7. Assertion wong.')
        # Step 8
        try:
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            # =======================================================
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            # Change Security type
            wireless_change_choose_option(block_2g_card, secure_value_field, VALUE_OPTION='WEP')
            wireless_check_pw_eye(driver, block_2g_card, change_pw=True, new_pw='123@!')

            block_2g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '2.4GHz Wireless Password Security Type':
                    check_24g_wireless = v.text
                    time.sleep(1)
                    v.click()
                    time.sleep(1)
                    break
            check_current_screen = detect_current_menu(driver)

            list_actual8 = [check_24g_wireless, check_current_screen]
            list_expected8 = ['Weak(WEP)', ('WIRELESS', 'Primary Network')]
            check = assert_list(list_actual8, list_expected8)
            step_8_name = '8. Re-do step 7 to set Security is WEP. Click to link text.'
            list_check_in_step_8 = ['Check value of 2.4GHz Wireless Password Security Type',
                                    'Check Re-direct to Wireless > Primary Network when click to link text']
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
            list_step_fail.append('8. Assertion wong.')
        # Step 9
        try:
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            #
            wireless_change_choose_option(block_2g_card, secure_value_field, VALUE_OPTION='WPA2-PSK')
            #
            block_2g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '2.4GHz Wireless Password Security Type':
                    check_24g_1 = v.text
                    break
            # ========================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            #
            wireless_change_choose_option(block_2g_card, secure_value_field, VALUE_OPTION='WPA2/WPA-PSK')
            #
            block_2g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '2.4GHz Wireless Password Security Type':
                    check_24g_2 = v.text
                    break

            # ========================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            wireless_change_choose_option(block_2g_card, secure_value_field, VALUE_OPTION='WPA2-Enterprise')
            #
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            labels_2 = block_2g_card.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'RADIUS Key':
                    v.find_element_by_css_selector(input).send_keys('5')
                    break
            #
            block_2g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '2.4GHz Wireless Password Security Type':
                    check_24g_3 = v.text
                    break

            # ========================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            wireless_change_choose_option(block_2g_card, secure_value_field, VALUE_OPTION='WPA2/WPA-Enterprise')
            #
            block_2g_card = driver.find_element_by_css_selector(wl_primary_card)
            labels_2 = block_2g_card.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_2g_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'RADIUS Key':
                    v.find_element_by_css_selector(input).send_keys('5')
                    break
            #
            block_2g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '2.4GHz Wireless Password Security Type':
                    check_24g_4 = v.text
                    break

            list_actual9 = [check_24g_1, check_24g_2, check_24g_3, check_24g_4]
            list_expected9 = ['Good(WPA2-PSK)',
                              'Good(WPA2/WPA-PSK)',
                              'Good(WPA2-Enterprise)',
                              'Good(WPA2/WPA-Enterprise)']
            check = assert_list(list_actual9, list_expected9)

            step_9_name = '9. Re-do step 7 to set Security is: WPA2-PSK, WPA2/WPA-PSK, WPA2-ENTERPRISE, WPA2/WPA-ENTERPRISE'
            list_check_in_step_9 = ['Check value of 2.4GHz Wireless Password Security Type is WPA2-PSK.',
                                    'Check value of 2.4GHz Wireless Password Security Type is WPA2/WPA-PSK.',
                                    'Check value of 2.4GHz Wireless Password Security Type is WPA2-ENTERPRISE.',
                                    'Check value of 2.4GHz Wireless Password Security Type is WPA2/WPA-ENTERPRISE.']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_9_name,
                    list_check_in_step=list_check_in_step_9,
                    list_actual=list_actual9,
                    list_expected=list_expected9
                )
            )
            list_step_fail.append('9. Assertion wong.')
        # Step 10
        try:
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            #
            wireless_change_choose_option(block_5g_card, secure_value_field, VALUE_OPTION='NONE')
            #
            block_5g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '5GHz Wireless Password Security Type':
                    check_5g_wireless_1 = v.text
                    time.sleep(1)
                    v.click()
                    time.sleep(1)
                    break
            check_current_screen_5 = detect_current_menu(driver)
            # =======================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            #
            wireless_change_choose_option(block_5g_card, secure_value_field, VALUE_OPTION='WEP')
            wireless_check_pw_eye(driver, block_5g_card, change_pw=True, new_pw='123@!')
            #
            block_5g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '5GHz Wireless Password Security Type':
                    check_5g_wireless_2 = v.text
                    time.sleep(1)
                    break
            # =======================================================

            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            #
            wireless_change_choose_option(block_5g_card, secure_value_field, VALUE_OPTION='WPA2-PSK')
            #
            block_5g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '5GHz Wireless Password Security Type':
                    check_5g_3 = v.text
                    break
            # ========================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            #
            wireless_change_choose_option(block_5g_card, secure_value_field, VALUE_OPTION='WPA2/WPA-PSK')
            #
            block_5g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '5GHz Wireless Password Security Type':
                    check_5g_4 = v.text
                    break

            # ========================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g_card, secure_value_field, VALUE_OPTION='WPA2-Enterprise')
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            labels_2 = block_5g_card.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'RADIUS Key':
                    v.find_element_by_css_selector(input).send_keys('5')
                    break
            #
            block_5g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '5GHz Wireless Password Security Type':
                    check_5g_5 = v.text
                    break

            # ========================================================
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            wireless_change_choose_option(block_5g_card, secure_value_field, VALUE_OPTION='WPA2/WPA-Enterprise')
            #
            block_5g_card = driver.find_elements_by_css_selector(wl_primary_card)[1]
            labels_2 = block_5g_card.find_elements_by_css_selector(label_name_in_2g)
            values_2 = block_5g_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels_2, values_2):
                if l.text == 'RADIUS Key':
                    v.find_element_by_css_selector(input).send_keys('5')
                    break
            #
            block_5g_card.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            #
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)
            #
            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == '5GHz Wireless Password Security Type':
                    check_5g_6 = v.text
                    break

            list_actual10 = [check_5g_wireless_1,
                             check_5g_wireless_2,
                             check_5g_3,
                             check_5g_4,
                             check_5g_5,
                             check_5g_6,
                             ' > '.join(check_current_screen_5)]
            list_expected10 = ['Weak(None)',
                               'Weak(WEP)',
                               'Good(WPA2-PSK)',
                               'Good(WPA2/WPA-PSK)',
                               'Good(WPA2-Enterprise)',
                               'Good(WPA2/WPA-Enterprise)',
                               ' > '.join(('WIRELESS', 'Primary Network'))]
            check = assert_list(list_actual10, list_expected10)

            step_10_name = '10. 5GHz Wireless Password Security Type check same as 2.4GHz'
            list_check_in_step_10 = ['Check value of 5GHz Wireless Security Type is NONE.',
                                     'Check value of 5GHz Wireless Security Type is WEP.',
                                     'Check value of 5GHz Wireless Security Type is WPA2-PSK.',
                                     'Check value of 5GHz Wireless Security Type is WPA2/WPA-PSK.',
                                     'Check value of 5GHz Wireless Security Type is WPA2-ENTERPRISE.',
                                     'Check value of 5GHz Wireless Security Type is WPA2/WPA-ENTERPRISE.',
                                     'Click to link text. Check re-direct to Wireless > Primary Network']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_10_name,
                    list_check_in_step=list_check_in_step_10,
                    list_actual=list_actual10,
                    list_expected=list_expected10
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_10_name,
                    list_check_in_step=list_check_in_step_10,
                    list_actual=list_actual10,
                    list_expected=list_expected10
                )
            )
            list_step_fail.append('10. Assertion wong.')

        # Step 11
        try:
            goto_menu(driver, advanced_tab, advanced_upnp_tab)
            time.sleep(1)
            # =======================================================
            block_unpn = driver.find_element_by_css_selector(ele_upnp_card)
            upnp_check_box = block_unpn.find_element_by_css_selector(select)
            if upnp_check_box.find_element_by_css_selector(input).is_selected():
                upnp_check_box.click()
                block_unpn.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'UPnP Service':
                    check_disabled_upnp = v.text
                    break
            # =======================================================
            goto_menu(driver, advanced_tab, advanced_upnp_tab)
            time.sleep(1)
            # =======================================================
            block_unpn = driver.find_element_by_css_selector(ele_upnp_card)
            upnp_check_box = block_unpn.find_element_by_css_selector(select)
            if not upnp_check_box.find_element_by_css_selector(input).is_selected():
                upnp_check_box.click()
                block_unpn.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'UPnP Service':
                    check_enabled_upnp = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(0.5)
                    break
            check_upnp_redirect = detect_current_menu(driver)

            list_actual11 = [check_disabled_upnp, check_enabled_upnp, ' > '.join(check_upnp_redirect)]
            list_expected11 = ['Disable', 'Enable', ' > '.join(('ADVANCED', 'UPnP'))]
            check = assert_list(list_actual11, list_expected11)

            step_11_name = '11. Disable UPnp. Check status in Security Check. Enable UPnP. Check Status in Security Check. Click to link text.'
            list_check_in_step_11 = ['Check status in Security Check when disable UPnp.',
                                     'Check status in Security Check when enable UPnp.',
                                     'Click to link text. Check Redirect to ADVANCED > UPnP']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_11_name,
                    list_check_in_step=list_check_in_step_11,
                    list_actual=list_actual11,
                    list_expected=list_expected11
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_11_name,
                    list_check_in_step=list_check_in_step_11,
                    list_actual=list_actual11,
                    list_expected=list_expected11
                )
            )
            list_step_fail.append('11. Assertion wong.')

        # Step 12
        try:
            goto_menu(driver, advanced_tab, advanced_network_tab)
            time.sleep(1)
            # =======================================================
            block_options = driver.find_element_by_css_selector(ele_options_card)
            labels = block_options.find_elements_by_css_selector(label_name_in_2g)
            values = block_options.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Remote Access':
                    if not v.find_element_by_css_selector(input).is_selected():
                        v.find_element_by_css_selector(select).click()
                        time.sleep(1)

                        block_options.find_element_by_css_selector(apply).click()
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(1)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(1)

                        grand_login(driver)
                        break


            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Remote Access':
                    check_enable_remote = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(0.5)
                    break
            check_remote_redirect = detect_current_menu(driver)
            # =======================================================
            goto_menu(driver, advanced_tab, advanced_network_tab)
            time.sleep(1)
            # =======================================================
            block_options = driver.find_element_by_css_selector(ele_options_card)
            labels = block_options.find_elements_by_css_selector(label_name_in_2g)
            values = block_options.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Remote Access':
                    if v.find_element_by_css_selector(input).is_selected():
                        v.find_element_by_css_selector(select).click()
                        block_options.find_element_by_css_selector(apply).click()
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(1)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(1)

                        grand_login(driver)
                        break

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Remote Access':
                    check_disable_remote = v.text
                    break

            list_actual12 = [check_enable_remote, check_disable_remote, ' > '.join(check_remote_redirect)]
            list_expected12 = ['Enable', 'Disable', ' > '.join(('ADVANCED', 'Network'))]
            check = assert_list(list_actual12, list_expected12)

            step_12_name = '12. Enable Remote Access. Check status in Security. Disable Remote Access. Check Status in Security Check. Click to link text.'
            list_check_in_step_12 = ['Check status in Security Check when enable Remote Access.',
                                     'Check status in Security Check when disable Remote Access.',
                                     'Click to link text. Check Redirect to ADVANCED > Network']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_12_name,
                    list_check_in_step=list_check_in_step_12,
                    list_actual=list_actual12,
                    list_expected=list_expected12
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_12_name,
                    list_check_in_step=list_check_in_step_12,
                    list_actual=list_actual12,
                    list_expected=list_expected12
                )
            )
            list_step_fail.append('12. Assertion wong.')

        # Step 13
        try:
            goto_menu(driver, advanced_tab, advanced_network_tab)
            time.sleep(1)
            # =======================================================
            block_options = driver.find_element_by_css_selector(ele_options_card)
            labels = block_options.find_elements_by_css_selector(label_name_in_2g)
            values = block_options.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'WAN ICMP Blocking':
                    if not v.find_element_by_css_selector(input).is_selected():
                        v.find_element_by_css_selector(select).click()
                        block_options.find_element_by_css_selector(apply).click()
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(1)
                        driver.find_element_by_css_selector(btn_ok).click()
                        time.sleep(1)
                        break

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Ping from WAN':
                    check_disable_ping = v.text
                    break

            # =======================================================
            goto_menu(driver, advanced_tab, advanced_network_tab)
            time.sleep(1)
            # =======================================================
            block_options = driver.find_element_by_css_selector(ele_options_card)
            labels = block_options.find_elements_by_css_selector(label_name_in_2g)
            values = block_options.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'WAN ICMP Blocking':
                    if v.find_element_by_css_selector(input).is_selected():
                        v.find_element_by_css_selector(select).click()
                        block_options.find_element_by_css_selector(apply).click()
                        wait_popup_disappear(driver, dialog_loading)
                        time.sleep(1)
                        driver.find_element_by_css_selector(btn_ok).click()
                        time.sleep(1)
                        break

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Ping from WAN':
                    check_enable_ping = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(0.5)
                    break
            check_ping_redirect = detect_current_menu(driver)

            list_actual13 = [check_disable_ping, check_enable_ping, ' > '.join(check_ping_redirect)]
            list_expected13 = ['Disable', 'Enable', ' > '.join(('ADVANCED', 'Network'))]
            check = assert_list(list_actual13, list_expected13)
            step_13_name = '13. Enable WAN ICMP Blocking. Check status in Security. Disable WAN ICMP Blocking. Check Status in Security Check. Click to link text.'
            list_check_in_step_13 = ['Check status in Security Check when enable  WAN ICMP Blocking.',
                                     'Check status in Security Check when disable  WAN ICMP Blocking.',
                                     'Click to link text. Check Redirect to ADVANCED > Network']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_13_name,
                    list_check_in_step=list_check_in_step_13,
                    list_actual=list_actual13,
                    list_expected=list_expected13
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_13_name,
                    list_check_in_step=list_check_in_step_13,
                    list_actual=list_actual13,
                    list_expected=list_expected13
                )
            )
            list_step_fail.append('13. Assertion wong.')

        # Step 14
        try:
            goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
            time.sleep(1)
            # =======================================================
            block_dmz = driver.find_element_by_css_selector(dmz_card)
            if block_dmz.find_element_by_css_selector(input).is_selected():
                block_dmz.find_element_by_css_selector(select).click()
                block_dmz.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'DMZ':
                    check_disable_dmz = v.text
                    break

            # =======================================================
            goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
            time.sleep(1)
            # =======================================================
            block_dmz = driver.find_element_by_css_selector(dmz_card)
            if not block_dmz.find_element_by_css_selector(input).is_selected():
                block_dmz.find_element_by_css_selector(select).click()
                block_dmz.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'DMZ':
                    check_enable_dmz = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(0.5)
                    break
            check_dmz_redirect = detect_current_menu(driver)

            list_actual14 = [check_disable_dmz, check_enable_dmz, ' > '.join(check_dmz_redirect)]
            list_expected14 = ['Disable', 'Enable', ' > '.join(('ADVANCED', 'Port Forwarding/DMZ'))]
            check = assert_list(list_actual14, list_expected14)

            step_14_name = '14. Disabled DMZ. Check status in Security. Disable DMZ. Check Status in Security Check. Click to link text.'
            list_check_in_step_14 = ['Check status in Security Check when enable DMZ.',
                                     'Check status in Security Check when disable DMZ.',
                                     'Click to link text. Check Redirect to ADVANCED > Port Forwarding/DMZ']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_14_name,
                    list_check_in_step=list_check_in_step_14,
                    list_actual=list_actual14,
                    list_expected=list_expected14
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_14_name,
                    list_check_in_step=list_check_in_step_14,
                    list_actual=list_actual14,
                    list_expected=list_expected14
                )
            )
            list_step_fail.append('14. Assertion wong.')

        # Step 15
        try:
            goto_menu(driver, advanced_tab, advanced_porttriggering_tab)
            time.sleep(1)

            triggering_block = driver.find_element_by_css_selector(port_triggering_card)
            while len(triggering_block.find_elements_by_css_selector(delete_cls)) > 0:
                triggering_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Port Triggering':
                    check_disable_trigger = v.text
                    break

            # =======================================================
            goto_menu(driver, advanced_tab, advanced_porttriggering_tab)
            time.sleep(1)
            # =======================================================
            add_a_port_triggering(driver,
                                  DESC_VALUE='Test',
                                  TRIGGERED_START_END=['10', '10'],
                                  PROTOCOL_TYPE_TRIGGERED='UDP',
                                  FORWARDED_START_END=['100', '100'],
                                  PROTOCOL_TYPE_FORWARDED='TCP')
            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Port Triggering':
                    check_enable_trigger = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(0.5)
                    break
            check_trigger_redirect = detect_current_menu(driver)

            list_actual15 = [check_disable_trigger, check_enable_trigger, ' > '.join(check_trigger_redirect)]
            list_expected15 = ['Disable', 'Enable', ' > '.join(('ADVANCED', 'Port Triggering'))]
            check = assert_list(list_actual15, list_expected15)

            step_15_name = '15. Delete all Triggering rule. Check status in Security. Add a Triggering rule. Check Status in Security Check. Click to link text.'
            list_check_in_step_15 = ['Check status in Security Check when delete all Triggering rule.',
                                     'Check status in Security Check when add a Triggering rule.',
                                     'Click to link text. Check Redirect to ADVANCED > Port Triggering']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_15_name,
                    list_check_in_step=list_check_in_step_15,
                    list_actual=list_actual15,
                    list_expected=list_expected15
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_15_name,
                    list_check_in_step=list_check_in_step_15,
                    list_actual=list_actual15,
                    list_expected=list_expected15
                )
            )
            list_step_fail.append('15. Assertion wong.')

        # Step 16
        try:
            goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
            time.sleep(1)

            forwarding_block = driver.find_element_by_css_selector(port_forwarding_card)
            while len(forwarding_block.find_elements_by_css_selector(delete_cls)) > 0:
                forwarding_block.find_element_by_css_selector(delete_cls).click()
                time.sleep(0.5)
                driver.find_element_by_css_selector(btn_ok).click()
                wait_popup_disappear(driver, dialog_loading)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)
            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Port Forwarding':
                    check_disable_forwarding = v.text
                    break

            # =======================================================
            goto_menu(driver, advanced_tab, advanced_portforwarding_tab)
            time.sleep(1)
            # =======================================================
            add_port_forwarding(driver,
                                SERVICE_TYPE='HTTP',
                                IP_ADDRESS_SPLIT='100',
                                LOCAL_START_END=['80', '80'],
                                EXTERNAL_START_END=['80', '80'],
                                PROTOCOL_TYPE='TCP')
            driver.find_element_by_css_selector(btn_save).click()
            time.sleep(2)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Port Forwarding':
                    check_enable_forwarding = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(0.5)
                    break
            check_forwarding_redirect = detect_current_menu(driver)

            list_actual16 = [check_disable_forwarding, check_enable_forwarding, ' > '.joincheck_forwarding_redirect()]
            list_expected16 = ['Disable', 'Enable', ' > '.join(('ADVANCED', 'Port Forwarding/DMZ'))]
            check = assert_list(list_actual16, list_expected16)

            step_16_name = '16. Delete all Forwarding rule. Check status in Security. Add a Forwarding rule. Check Status in Security Check. Click to link text.'
            list_check_in_step_16 = ['Check status in Security Check when delete all Forwarding rule.',
                                     'Check status in Security Check when add a Forwarding rule.',
                                     'Click to link text. Check Redirect to ADVANCED > Port Forwarding/DMZ']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_16_name,
                    list_check_in_step=list_check_in_step_16,
                    list_actual=list_actual16,
                    list_expected=list_expected16
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_16_name,
                    list_check_in_step=list_check_in_step_16,
                    list_actual=list_actual16,
                    list_expected=list_expected16
                )
            )
            list_step_fail.append('16. Assertion wong.')

        # Step 17
        try:
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # ===================================================== Enable FTP server
            ftp_block = driver.find_element_by_css_selector(ftp_server)
            if ftp_block.find_element_by_css_selector(input).is_selected():
                ftp_block.find_element_by_css_selector(select).click()
                time.sleep(0.5)
                ftp_block.find_element_by_css_selector(apply).click()
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(1)
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(1)

            goto_menu(driver, media_share_tab, media_share_usb_tab)
            wait_popup_disappear(driver, dialog_loading)
            # # ===================================================== Delete
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
            # ===================================================== Goto
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            # ===================================================== Enable FTP server
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
                        if o.text == 'Anonymous':
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

            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Anonymous Login to FTP Server':
                    check_enable_server = v.text
                    time.sleep(0.5)
                    v.click()
                    time.sleep(2)
                    break
            check_server_redirect = detect_current_menu(driver)
            # =======================================================
            goto_menu(driver, media_share_tab, media_share_server_settings_tab)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # =======================================================
            ftp_block = driver.find_element_by_css_selector(ftp_server)
            labels = ftp_block.find_elements_by_css_selector(label_name_in_2g)
            values = ftp_block.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Account':
                    v.click()
                    time.sleep(0.5)
                    ls_options = ftp_block.find_elements_by_css_selector(secure_value_in_drop_down)
                    for o in ls_options:
                        if o.text != 'Anonymous':
                            o.click()
                            time.sleep(0.5)
                            break
                    break
            ftp_block.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            # =======================================================
            goto_menu(driver, security_tab, security_selfcheck_tab)
            time.sleep(1)

            secure_card = driver.find_element_by_css_selector(ele_security_check_block)
            labels = secure_card.find_elements_by_css_selector(label_name_in_2g)
            values = secure_card.find_elements_by_css_selector(wrap_input)
            for l, v in zip(labels, values):
                if l.text == 'Anonymous Login to FTP Server':
                    check_disable_server = v.text
                    time.sleep(0.5)
                    break

            list_actual17 = [check_enable_server, check_disable_server, ' > '.join(check_server_redirect)]
            list_expected17 = ['Enable', 'Disable', ' > '.join(('MEDIA SHARE', 'Server Settings'))]
            check = assert_list(list_actual17, list_expected17)

            step_17_name = f'17.  Add USB Network Folder and Account Settings. Change Settings FTP server info.' \
                f'Change Account to Anonymous. Check status in Security. Change Account to other option of Anonymous. Check Status in Security Check. Click to link text.'
            list_check_in_step_17 = ['Check status in Security Check when delete all Forwarding rule.',
                                     'Check status in Security Check when add a Forwarding rule.',
                                     'Click to link text. Check Redirect to MEDIA SHARE > Server Settings']
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_17_name,
                    list_check_in_step=list_check_in_step_17,
                    list_actual=list_actual17,
                    list_expected=list_expected17
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_17_name,
                    list_check_in_step=list_check_in_step_17,
                    list_actual=list_actual17,
                    list_expected=list_expected17
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('17. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
