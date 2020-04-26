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

# save_config(config_path, 'URL', 'url', 'http://192.168.1.1')
class SECURITY(unittest.TestCase):
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
        # write_to_excel_tmp(self.key, self.list_steps, self.def_name)
        self.driver.quit()
    # OK
    def test_01_SECURITY_Check_Parental_Code_setting(self):
        self.key = 'SECURITY_01'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # Factory reset
        # ===========================================================
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
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            ActionChains(driver).click(parental_field_input[4]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_CODE_KEY)

            list_actual1 = ls_parental_name
            list_expected1 = exp_ls_parental_label
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check Parental pop up labels. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check Parental pop up labels. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Refresh Parental control: Check title pop up. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Refresh Parental control: Check title pop up. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Input wrong parental code: Check error message. '
                                   f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Input wrong parental code: Check error mesage. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Input valid code. Check page Security displayed. '
                                   f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Input valid code. Check page Security displayed. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check Security page displayed'
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check Security page displayed. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
            list_step_fail.append(
                '1,2,3. Assertion wong.')

        try:
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_input = parental_code.find_elements_by_css_selector(input)

            # New parental code
            parental_input[1].send_keys(PARENTAL_NEW_CODE_KEY)
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4, 5. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4, 5. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('4, 5. Assertion wong.')


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Disable Parental code: Check Parental Code disabled. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Disable Parental code: Check Parental Code disabled. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Input Init parental code. '
                f'Check confirm message. Click OK. Check popup parental create code display. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Input Init parental code. '
                f'Check confirm message. Click OK. Check popup parental create code display. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            list_step_fail.append('7 Assertion wong.')


        try:
            parental_field_input = driver.find_elements_by_css_selector(parental_popup_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_NEW_CODE_KEY_2).perform()
            ActionChains(driver).click(parental_field_input[4]).send_keys(PARENTAL_NEW_CODE_KEY_2).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_NEW_CODE_KEY_2)

            check_dialog_parental_display = len(driver.find_elements_by_css_selector('.parental-login-dialog')) > 0

            list_actual8 = [check_dialog_parental_display]
            list_expected8 = [return_true]
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 8. Input new parental code key. Click OK.'
                f'Check popup login parental display. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Input new parental code key. Click OK.'
                f'Check popup login parental display. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 9. Input parental code key. Click OK.'
                f'Check Security page display. '
                f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Input parental code key. Click OK.'
                f'Check Security page display. '
                f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])
    # OK
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

            #
            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_input = parental_code.find_elements_by_css_selector(input)

            # New parental code
            parental_input[1].send_keys(PARENTAL_NEW_CODE_KEY)
            # Retype parental code
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Apply successfully: Check Security page displayed and pop-up disappear. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Apply successfully: Check Security page displayed and pop-up disappear. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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

            check_pop_init = driver.find_element_by_css_selector(parental_pop_init_pw).is_displayed()

            list_actual2 = [check_pop_init]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Send INIT key. Check pop-up init is displayed. '
                                   f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('4. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 5
        try:
            parental_field_name = driver.find_elements_by_css_selector(parental_popup_label)
            ls_parental_name = [i.text for i in parental_field_name]

            parental_field_input = driver.find_elements_by_css_selector(parental_popup_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            ActionChains(driver).click(parental_field_input[4]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # Save
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_CODE_KEY)

            list_actual3 = ls_parental_name
            list_expected3 = exp_ls_parental_label
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Parental pop up labels. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Parental pop up labels. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('. Assertion wong.')

        # ~~~~~~~~~~~~~~~~ 6
        try:
            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            # parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            # ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            # time.sleep(0.5)
            # driver.find_element_by_css_selector(btn_ok).click()
            # wait_popup_disappear(driver, dialog_loading)

            check_page_security = driver.find_element_by_css_selector(security_page).is_displayed()
            time.sleep(3)
            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual4 = [check_page_security, check_pop_up_disable]
            list_expected4 = [return_true, return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check Parental pop up labels. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Parental pop up labels. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap')
            for f in ls_service:
                if f.text == SOCIAL_NW:
                    f.click()
                    break

            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                if s.text == FACEBOOK:
                    if not len(s.find_elements_by_css_selector('.selected-icon')) > 0:
                        s.click()
                        break

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
            list_expected1 = [exp_ls_service_filter_items_value, exp_block_schedule_value]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1,2,3. Add rule: Check list of Service Filter and Block Schedule. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Add rule: Check list of Service Filter and Block Schedule. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
                time.sleep(10)
                fb_http_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(2)

                driver2.get(FACEBOOK_S)
                time.sleep(10)
                fb_https_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(2)

                driver2.get(GOOGLE)
                time.sleep(10)
                gg_http_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(2)

                driver2.get(GOOGLE_S)
                time.sleep(10)
                gg_https_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(2)

                # check_step_4 = all([i != 200 for i in [fb_http_4, fb_https_4, gg_http_4, gg_https_4]])
                check_step_4 = [fb_http_4, fb_https_4, gg_http_4, gg_https_4]
                # ======================================================================================
                time.sleep(1)
                # Disable Parental control
                # parental_code = driver.find_element_by_css_selector(parental_code_card)
                # parental_code_btn = parental_code.find_element_by_css_selector(select)
                # parental_code_check = parental_code.find_element_by_css_selector(input)
                # if parental_code_check.is_selected():
                #     parental_code_btn.click()
                #     time.sleep(5)
                #     # Input valid
                #     parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                #     if len(parental_field_input) > 0:
                #         #  New
                #         ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                #         time.sleep(0.5)
                #         driver.find_element_by_css_selector(btn_ok).click()
                #         wait_popup_disappear(driver, dialog_loading)
                parental_control = driver.find_element_by_css_selector(ele_security_check_parental)
                parental_control_btn = parental_control.find_element_by_css_selector(select)
                parental_control_check = parental_control.find_element_by_css_selector(input)
                if parental_control_check.is_selected():
                    parental_control_btn.click()
                    time.sleep(2)
                else:
                    parental_control_btn.click()
                    time.sleep(2)
                    parental_input_popup = driver.find_elements_by_css_selector(parental_wrap_input)
                    if len(parental_input_popup) > 0:
                        #  New
                        ActionChains(driver).click(parental_input_popup[0]).send_keys(PARENTAL_CODE_KEY).perform()
                        time.sleep(0.5)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)
                time.sleep(3)
                # ======================================================================================
                driver2.get(FACEBOOK)
                time.sleep(5)
                fb_http_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(2)

                driver2.get(FACEBOOK_S)
                time.sleep(5)
                fb_https_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(2)

                driver2.get(GOOGLE)
                time.sleep(5)
                gg_http_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(2)

                driver2.get(GOOGLE_S)
                time.sleep(5)
                gg_https_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(2)

                check_step_6 = [fb_http_6, fb_https_6, gg_http_6, gg_https_6]
                # check_step_6 = all([i == 200 for i in [fb_http_6, fb_https_6, gg_http_6, gg_https_6]])
                # ======================================================================================
                time.sleep(1)
                # Enable
                parental_control = driver.find_element_by_css_selector(ele_security_check_parental)
                parental_control_btn = parental_control.find_element_by_css_selector(select)
                parental_control_check = parental_control.find_element_by_css_selector(input)
                if parental_control_check.is_selected():
                    parental_control_btn.click()
                    time.sleep(2)
                else:
                    parental_control_btn.click()
                    time.sleep(2)
                    parental_input_popup = driver.find_elements_by_css_selector(parental_wrap_input)
                    if len(parental_input_popup) > 0:
                        #  New
                        ActionChains(driver).click(parental_input_popup[0]).send_keys(PARENTAL_CODE_KEY).perform()
                        time.sleep(0.5)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)
                time.sleep(3)
                # ======================================================================================
                driver2.get(FACEBOOK)
                time.sleep(10)
                fb_http_8 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(2)

                driver2.get(FACEBOOK_S)
                time.sleep(10)
                fb_https_8 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
                time.sleep(2)

                driver2.get(GOOGLE)
                time.sleep(10)
                gg_http_8 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(2)

                driver2.get(GOOGLE_S)
                time.sleep(10)
                gg_https_8 = len(driver2.find_elements_by_css_selector(google_img)) > 0
                time.sleep(2)

                check_step_8 = [fb_http_8, fb_https_8, gg_http_8, gg_https_8]
                # ======================================================================================
                # check_step_8 = all([i != 200 for i in [fb_http_8, fb_https_8, gg_http_8, gg_https_8]])
                time.sleep(1)

                list_actual2 = [check_step_4, check_step_6, check_step_8]
                list_expected2 = [[return_false]*4, [return_true]*4, [return_false]*4]
                check = assert_list(list_actual2, list_expected2)
                self.assertTrue(check["result"])
                self.list_steps.append(
                    f'[Pass] 4-8. -{str(i+1)}-. Check Access to FB, GG False -> True -> False. '
                    f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            except:
                self.list_steps.append(
                    f'[Fail] 4-8. -{str(i+1)}-. Check Access to FB, GG False -> True -> False. '
                    f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. goto Parental Control page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. goto Parental Control page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        FACEBOOK = 'http://facebook.com'
        FACEBOOK_S = 'https://facebook.com'
        GOOGLE = 'http://google.com'
        GOOGLE_S = 'https://google.com'

        try:
            driver2 = webdriver.Chrome(driver_path)
            time.sleep(5)
            driver2.get(FACEBOOK)
            time.sleep(10)
            fb_http_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(2)

            driver2.get(FACEBOOK_S)
            time.sleep(10)
            fb_https_4 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(2)

            driver2.get(GOOGLE)
            time.sleep(10)
            gg_http_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(2)

            driver2.get(GOOGLE_S)
            time.sleep(10)
            gg_https_4 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(2)

            driver2.quit()

            list_actual4 = [fb_http_4, fb_https_4, gg_http_4, gg_https_4]
            list_expected4 = [return_false] * 4
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Check Can not Access to Facebook, Facebooks, Google, Googles. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Can not Access to Facebook, Facebooks, Google, Googles. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Disabled Control Rule at step 3. Check disabled success. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Disabled Control Rule at step 3. Check disabled success. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append('5. Assertion wong.')

            # ======================================================================================

        try:
            driver2 = webdriver.Chrome(driver_path)
            driver2.get(FACEBOOK)
            time.sleep(5)
            fb_http_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(2)

            driver2.get(FACEBOOK_S)
            time.sleep(5)
            fb_https_6 = len(driver2.find_elements_by_css_selector(ele_verify_facebook)) > 0
            time.sleep(2)

            driver2.get(GOOGLE)
            time.sleep(5)
            gg_http_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(2)

            driver2.get(GOOGLE_S)
            time.sleep(5)
            gg_https_6 = len(driver2.find_elements_by_css_selector(google_img)) > 0
            time.sleep(2)
            driver2.quit()
            list_actual6 = [fb_http_6, fb_https_6, gg_http_6, gg_https_6]
            list_expected6 = [return_true] * 4
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Check can Access to Facebook, Facebooks, Google, Googles. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check can Access to Facebook, Facebooks, Google, Googles. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            list_step_fail.append('6. Assertion wong.')

        try:
            for i in range(5):
                add_a_parental_control_rule(driver)

            check_add_btn_disabled = driver.find_element_by_css_selector(add_class).is_enabled()
            list_actual7 = [check_add_btn_disabled]
            list_expected7 = [return_false]
            check = assert_list(list_actual7, list_expected7)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Add more 6 Parental Control Rule. Check Button Add Disabled. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 7. Add more 6 Parental Control Rule. Check Button Add Disabled. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('7. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_06_SECURITY_Confirm_Parental_Control_rule_Modification(self):
        self.key = 'SECURITY_06'
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. goto Parental Control page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. goto Parental Control page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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

            ls_service = driver.find_elements_by_css_selector('.service-item-wrap>.item-inner>span')
            for f in ls_service:
                if f.text == 'Social Network':
                    f.click()
                    time.sleep(1)
                    ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
                    for s in ls_service_sub:
                        if len(s.find_elements_by_css_selector('.selected-icon')) > 0:
                            s.click()
                    break
            ls_service = driver.find_elements_by_css_selector('.service-item-wrap>.item-inner>span')
            for f in ls_service:
                if f.text == 'Mail':
                    f.click()
                    time.sleep(1)
                    sub_title = driver.find_element_by_css_selector('.sub-title').text
                    ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
                    for s in ls_service_sub:
                        if s.text in ['gmail', 'outlook']:
                            if not len(s.find_elements_by_css_selector('.selected-icon')) > 0:
                                s.click()
                    break
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            # Schedule
            edit_field.find_element_by_css_selector('.set-schedule').find_element_by_css_selector(apply).click()
            time.sleep(1)
            driver.find_element_by_css_selector(f'tr:nth-child({weekday_index})>.all').click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_save).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            ls_mac_device = [i.text.splitlines()[-1] for i in driver.find_elements_by_css_selector('.name .device-item')]
            check_mac = MAC_2 in ls_mac_device
            time.sleep(1)
            driver.find_element_by_css_selector('.filter-count').click()
            time.sleep(1)
            service_filters = [i.text for i in driver.find_elements_by_css_selector('.service-item')]
            # Check block schedule
            block_schedule_value = driver.find_elements_by_css_selector('.schedule')[-1].text

            list_actual4 = [check_mac, service_filters, block_schedule_value]
            list_expected4 = [return_true, ['gmail', 'outlook'], 'Always Block']
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Edit rule: Check Add other mac, 2 service filters, Text of block schedule. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Edit rule: Check Add other mac, 2 service filters, Text of block schedule. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. goto Parental Control page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. goto Parental Control page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add rule: Set the Websites/Apps Sub title, number of Social NW, Block schedule text. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Delete rule: Check number of remain row = 0. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Delete rule: Check number of remain row = 0. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add a IP/Port Filtering: Check Row have just added. '
                f'Is active, Description, IP, Port Start End, Portocol Type. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add a IP/Port Filtering: Check Row have just added. '
                f'Is active, Description, IP, Port Start End, Portocol Type. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4, 5. Edit IP/Port Filtering: Change IP address. Check Row after saved. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4, 5. Edit IP/Port Filtering: Change IP address. Check Row after saved. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add a IP/Port Filtering: Check Row have just added. '
                f'Is active, Description, IP, Port Start End, Portocol Type. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add a IP/Port Filtering: Check Row have just added. '
                f'Is active, Description, IP, Port Start End, Portocol Type. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Delete IP Port Filtering. Click Cancel: Check number of remain row = 1. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Delete IP Port Filtering. Click Cancel: Check number of remain row = 1. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5, 6. Delete IP Port Filtering. Click OK: Check number of remain row = 0. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5, 6. Delete IP Port Filtering. Click OK: Check number of remain row = 0. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
        try:
            grand_login(driver)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            # Get Wireless 2G Information
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]

            wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
            wifi_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=False)

            self.list_steps.append(f'[Pass] Precondition')
        except:
            self.list_steps.append(f'[Fail] Precondition')
            list_step_fail.append('0. Assertion wong.')

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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add a IP/Port Filtering: Check Row have just added. '
                f'Is active, Description, IP, Port Start End, Portocol Type. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add a IP/Port Filtering: Check Row have just added. '
                f'Is active, Description, IP, Port Start End, Portocol Type. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            check_google = check_connect_to_google()
            check_youtube = check_connect_to_youtube()

            list_actual4 = [check_google, check_youtube]
            list_expected4 = [return_false] * 2
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Check Can not Access to Google, Youtube. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Can not Access to Google, Youtube. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong.')

        try:
            # Disconnect Ethernet
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Disconnect LAN. Connect 2GHz Wifi. Login again. '
                f'Check Mac filtering table: Is active, Device Name, MAC address.  '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Disconnect LAN. Connect 2GHz Wifi. Login again. '
                f'Check Mac filtering table: Is active, Device Name, MAC address.  '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Disconnect LAN. Connect 2GHz Wifi. Login again. '
                f'Check Mac filtering table: Is NOT active, Device Name, MAC address.  '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Disconnect LAN. Connect 2GHz Wifi. Login again. '
                f'Check Mac filtering table: Is NOT active, Device Name, MAC address.  '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Disabled Wireless. Re-connect Ethernet. Check Ethernet enabled. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Disabled Wireless. Re-connect Ethernet. Check Ethernet enabled. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
            list_step_fail.append('7. Assertion wong.')

        try:
            check_google_2 = check_connect_to_google()
            check_youtube_2 = check_connect_to_youtube()

            list_actual8 = [check_google_2, check_youtube_2]
            list_expected8 = [return_true] * 2
            check = assert_list(list_actual8, list_expected8)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 8. Check Can Access to Google, Youtube normally. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Check Can Access to Google, Youtube normally. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
            list_step_fail.append('8. Assertion wong.')

        try:
            grand_login(driver)
            # Goto media share USB
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)
            for i in range(31):
                tmp_mac = random_mac_address()
                add_a_mac_filtering(driver, tmp_mac)
                time.sleep(1)

            time.sleep(1)
            mac_block = driver.find_element_by_css_selector(ele_mac_filtering)
            check_add_btn_disabled = mac_block.find_element_by_css_selector(add_class).is_enabled()

            list_actual9 = [check_add_btn_disabled]
            list_expected9 = [return_false]
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 9. Add more 31 MAC filtering. Check Button Add Disabled. '
                f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Add more 31 MAC filtering. Check Button Add Disabled. '
                f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_26_SECURITY_Delete_MAC_Filtering_rule(self):
        self.key = 'SECURITY_26'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        PHYSICAL_MAC = get_value_from_ipconfig('Ethernet adapter Ethernet', 'Physical Address').replace('-', ':')
        HOST_NAME = get_value_from_ipconfig('Windows IP Configuration', 'Host Name')
        try:
            grand_login(driver)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            # Get Wireless 2G Information
            block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]

            wifi_2g_name = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
            wifi_2g_pw = wireless_check_pw_eye(driver, block_2g, change_pw=False)

            self.list_steps.append(f'[Pass] Precondition')
        except:
            self.list_steps.append(f'[Fail] Precondition')
            list_step_fail.append('0. Assertion wong.')

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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Filtering page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Add a MAC Filtering: Check Row have just added. '
                f'Is active, Host name and MAC address. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Add a MAC Filtering: Check Row have just added. '
                f'Is active, Host name and MAC address. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong.')

        try:
            # Disconnect Ethernet
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            # Connect Wifi 2.4 Ghz
            connect_wifi_by_command(wifi_2g_name, wifi_2g_pw)
            # Login again
            grand_login(driver)
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)
            # Get table
            get_table_value_2 = get_mac_filtering_table(driver)

            list_actual5 = get_table_value_2[-1]
            list_expected5 = [return_true, HOST_NAME, PHYSICAL_MAC]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4.0. Disconnect LAN. Connect 2GHz Wifi. Login again. '
                f'Check Mac filtering table: Is active, Device Name, MAC address.  '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 4.0. Disconnect LAN. Connect 2GHz Wifi. Login again. '
                f'Check Mac filtering table: Is active, Device Name, MAC address.  '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Delete MAC Filtering. Click Cancel: Check number of remain row = 1. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Delete MAC Filtering. Click Cancel: Check number of remain row = 1. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual4 = [remain_row]
            list_expected4 = [0]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5, 6. Delete MAC Filtering. Click OK: Check number of remain row = 0. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5, 6. Delete MAC Filtering. Click OK: Check number of remain row = 0. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            list_expected1 = ['Security check']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Login. Goto Security > Security Check page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Login. Goto Security > Security Check page. Check page title. '
                f'Actual: {str(list_actual1)}. Expected: {str(list_expected1)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check list label of Security Check Block. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3.Check list label of Security Check Block. '
                f'Actual: {str(list_actual3)}. Expected: {str(list_expected3)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Check Value of Login Password Changed. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Value of Login Password Changed. '
                f'Actual: {str(list_actual4)}. Expected: {str(list_expected4)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Change PW to Good Password. '
                f'Check value of Login Password Security Level. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Change PW to Good Password. '
                f'Check value of Login Password Security Level. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 6. Change PW to Strong Password. '
                f'Check value of Login Password Security Level. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
        except:
            self.list_steps.append(
                f'[Fail] 6. Change PW to Strong Password. '
                f'Check value of Login Password Security Level. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 7. Change Wifi 24GHz to NONE. '
                f'Check value of 2.4GHz Wireless Password Security Type. '
                f'Click to link text. Check Re-direct to Wireless > Primary Network. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
        except:
            self.list_steps.append(
                f'[Fail] 7. Change Wifi 24GHz to NONE. '
                f'Check value of 2.4GHz Wireless Password Security Type. '
                f'Click to link text. Check Re-direct to Wireless > Primary Network. '
                f'Actual: {str(list_actual7)}. Expected: {str(list_expected7)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 8. Change Wifi 24GHz to WEP. '
                f'Check value of 2.4GHz Wireless Password Security Type. '
                f'Click to link text. Check Re-direct to Wireless > Primary Network. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
        except:
            self.list_steps.append(
                f'[Fail] 8. Change Wifi 24GHz to WEP. '
                f'Check value of 2.4GHz Wireless Password Security Type. '
                f'Click to link text. Check Re-direct to Wireless > Primary Network. '
                f'Actual: {str(list_actual8)}. Expected: {str(list_expected8)}')
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
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 9. Change Wifi 24GHz Security to WPA2-PSK, WPA2/WPA-PSK, WPA2-ENTERPRISE, WPA2/WPA-ENTERPRISE. '
                f'Check value of 2.4GHz Wireless Password Security Type. '
                f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
        except:
            self.list_steps.append(
                f'[Fail] 9. Change Wifi 24GHz Security to WPA2-PSK, WPA2/WPA-PSK, WPA2-ENTERPRISE, WPA2/WPA-ENTERPRISE. '
                f'Check value of 2.4GHz Wireless Password Security Type. '
                f'Actual: {str(list_actual9)}. Expected: {str(list_expected9)}')
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
                             check_current_screen_5]
            list_expected10 = ['Weak(None)',
                               'Weak(WEP)',
                               'Good(WPA2-PSK)',
                               'Good(WPA2/WPA-PSK)',
                               'Good(WPA2-Enterprise)',
                               'Good(WPA2/WPA-Enterprise)',
                               ('WIRELESS', 'Primary Network')]
            check = assert_list(list_actual10, list_expected10)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 10. Change Wifi 5GHz Security to NONE, WEP, WPA2-PSK, WPA2/WPA-PSK, WPA2-ENTERPRISE, WPA2/WPA-ENTERPRISE. '
                f'Check value of 5GHz Wireless Password Security Type. '
                f'Check click to link text to Re-direct to Wireless > Primary Network. '
                f'Actual: {str(list_actual10)}. Expected: {str(list_expected10)}')
        except:
            self.list_steps.append(
                f'[Fail] 10. Change Wifi 5GHz Security to NONE, WEP, WPA2-PSK, WPA2/WPA-PSK, WPA2-ENTERPRISE, WPA2/WPA-ENTERPRISE. '
                f'Check value of 5GHz Wireless Password Security Type. '
                f'Check click to link text to Re-direct to Wireless > Primary Network. '
                f'Actual: {str(list_actual10)}. Expected: {str(list_expected10)}')
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

            list_actual11 = [check_disabled_upnp, check_enabled_upnp, check_upnp_redirect]
            list_expected11 = ['Disable', 'Enable', ('ADVANCED', 'UPnP')]
            check = assert_list(list_actual11, list_expected11)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 11. Disable UPnp. Check status in Security Check. '
                f'Enable UPnP. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > UPnP. '
                f'Actual: {str(list_actual11)}. Expected: {str(list_expected11)}')
        except:
            self.list_steps.append(
                f'[Fail] 11. Disable UPnp. Check status in Security Check. '
                f'Enable UPnP. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > UPnP. '
                f'Actual: {str(list_actual11)}. Expected: {str(list_expected11)}')
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

            list_actual12 = [check_enable_remote, check_disable_remote, check_remote_redirect]
            list_expected12 = ['Enable', 'Disable', ('ADVANCED', 'Network')]
            check = assert_list(list_actual12, list_expected12)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 12. Enable Remote Access. Check status in Security Check. '
                f'Disable Remote Access. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Network. '
                f'Actual: {str(list_actual12)}. Expected: {str(list_expected12)}')
        except:
            self.list_steps.append(
                f'[Fail] 12. Enable Remote Access. Check status in Security Check. '
                f'Disable Remote Access. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Network. '
                f'Actual: {str(list_actual12)}. Expected: {str(list_expected12)}')
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

            list_actual13 = [check_disable_ping, check_enable_ping, check_ping_redirect]
            list_expected13 = ['Disable', 'Enable', ('ADVANCED', 'Network')]
            check = assert_list(list_actual13, list_expected13)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 13. Enable WAN ICMP Blocking. Check status in Security Check. '
                f'Disable WAN ICMP Blocking. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Network. '
                f'Actual: {str(list_actual13)}. Expected: {str(list_expected13)}')
        except:
            self.list_steps.append(
                f'[Fail] 13.  Enable WAN ICMP Blocking. Check status in Security Check. '
                f'Disable WAN ICMP Blocking. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Network. '
                f'Actual: {str(list_actual13)}. Expected: {str(list_expected13)}')
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

            list_actual14 = [check_disable_dmz, check_enable_dmz, check_dmz_redirect]
            list_expected14 = ['Disable', 'Enable', ('ADVANCED', 'Port Forwarding/DMZ')]
            check = assert_list(list_actual14, list_expected14)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 14. Disabled DMZ. Check status in Security Check. '
                f'Enabled DMZ. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Port Forwarding/DMZ. '
                f'Actual: {str(list_actual14)}. Expected: {str(list_expected14)}')
        except:
            self.list_steps.append(
                f'[Fail] 14. Disabled DMZ. Check status in Security Check. '
                f'Enabled DMZ. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Port Forwarding/DMZ. '
                f'Actual: {str(list_actual14)}. Expected: {str(list_expected14)}')
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

            list_actual15 = [check_disable_trigger, check_enable_trigger, check_trigger_redirect]
            list_expected15 = ['Disable', 'Enable', ('ADVANCED', 'Port Triggering')]
            check = assert_list(list_actual15, list_expected15)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 15. Delete all Triggering rule. Check status in Security Check. '
                f'Add a Triggering rule. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Port Triggering. '
                f'Actual: {str(list_actual15)}. Expected: {str(list_expected15)}')
        except:
            self.list_steps.append(
                f'[Fail] 15. Delete all Triggering rule. Check status in Security Check. '
                f'Add a Triggering rule. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Port Triggering. '
                f'Actual: {str(list_actual15)}. Expected: {str(list_expected15)}')
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

            list_actual16 = [check_disable_forwarding, check_enable_forwarding, check_forwarding_redirect]
            list_expected16 = ['Disable', 'Enable', ('ADVANCED', 'Port Forwarding/DMZ')]
            check = assert_list(list_actual16, list_expected16)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 16. Delete all Forwarding rule. Check status in Security Check. '
                f'Add a Forwarding rule. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Port Forwarding/DMZ. '
                f'Actual: {str(list_actual16)}. Expected: {str(list_expected16)}')
        except:
            self.list_steps.append(
                f'[Fail] 16. Delete all Forwarding rule. Check status in Security Check. '
                f'Add a Forwarding rule. Check Status in Security Check. '
                f'Click to link text. Check Redirect to ADVANCED > Port Forwarding/DMZ. '
                f'Actual: {str(list_actual16)}. Expected: {str(list_expected16)}')
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

            list_actual17 = [check_enable_server, check_disable_server, check_server_redirect]
            list_expected17 = ['Enable', 'Disable', ('MEDIA SHARE', 'Server Settings')]
            check = assert_list(list_actual17, list_expected17)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 17. Add USB Network Folder and Account Settings. Change Settings FTP server info. '
                f'Change Account to Anonymous. Check status in Security Check. '
                f'Change Account to other option of Anonymous. Check Status in Security Check. '
                f'Click to link text. Check Redirect to MEDIA SHARE > Server Settings. '
                f'Actual: {str(list_actual17)}. Expected: {str(list_expected17)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 17.  Add USB Network Folder and Account Settings. Change Settings FTP server info. '
                f'Change Account to Anonymous. Check status in Security Check. '
                f'Change Account to other option of Anonymous. Check Status in Security Check. '
                f'Click to link text. Check Redirect to MEDIA SHARE > Server Settings. '
                f'Actual: {str(list_actual17)}. Expected: {str(list_expected17)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('17. Assertion wong.')
        self.assertListEqual(list_step_fail, [])
if __name__ == '__main__':
    unittest.main()
