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
        URL_LOGIN = get_config('URL', 'url')
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
        try:
            grand_login(driver)

            # Goto Security
            goto_menu(driver, security_tab, 0)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0
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

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 4
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
            time.sleep(1)
            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_NEW_CODE_KEY).perform()
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)

            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0
            time.sleep(3)
            # Save to config file
            save_config(config_path, 'SECURITY', 'parental_code', PARENTAL_NEW_CODE_KEY)

            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual2 = [check_page_security, check_pop_up_disable]
            list_expected2 = [return_true, return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

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
        factory_dut()
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

            # Goto media share USB
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
            # parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            # if len(parental_field_input) > 0:
            #     #  New
            #     ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            #     time.sleep(0.5)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)

            # driver.find_element_by_css_selector(security_filtering_tab).click()
            # wait_popup_disappear(driver, dialog_loading)

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

            # Goto media share USB
            goto_menu(driver, security_tab, security_filtering_tab)
            wait_popup_disappear(driver, dialog_loading)

            # # Input valid
            # parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            # if len(parental_field_input) > 0:
            #     #  New
            #     ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
            #     time.sleep(0.5)
            #     driver.find_element_by_css_selector(btn_ok).click()
            #     wait_popup_disappear(driver, dialog_loading)
            #
            # driver.find_element_by_css_selector(security_filtering_tab).click()
            # wait_popup_disappear(driver, dialog_loading)

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
if __name__ == '__main__':
    unittest.main()
