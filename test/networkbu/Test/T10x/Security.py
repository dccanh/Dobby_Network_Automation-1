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
            self.driver = webdriver.Chrome(driver_path)  # open chrome
            self.driver.maximize_window()
            self.time_stamp = datetime.now()
        except:
            self.tearDown()
            raise

    def tearDown(self):
        try:
            end_time = datetime.now()
            duration = str((end_time - self.start_time))
            write_ggsheet(self.key, self.list_steps, self.def_name, duration, time_stamp=self.time_stamp)
        except:
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

    def test_01_Check_Parental_Code_setting(self):
        self.key = 'SECURITY_01'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        # Factory reset
        URL_LOGIN = get_config('URL', 'url')
        URL_PING_CHECK = '192.168.1.1'
        filename = '1'
        command = 'factorycfg.sh -a'
        run_cmd(command, filename=filename)
        time.sleep(100)
        wait_DUT_activated(URL_LOGIN)
        wait_ping(URL_PING_CHECK)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        filename_2 = 'account.txt'
        command_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(command_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        PARENTAL_CODE_KEY = '1234'
        PARENTAL_WRONG_CODE_KEY = '4321'
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)
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

            list_actual = ls_parental_name
            list_expected = exp_ls_parental_label
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check Parental pop up labels')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check Parental pop up labels. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            pop_up_title = driver.find_element_by_css_selector(parental_popup_title).text

            list_actual = [pop_up_title]
            list_expected = [exp_parental_pop_up_title]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Refresh Parental control: Check title pop up')
        except:
            self.list_steps.append(
                f'[Fail] 4. Refresh Parental control: Check title pop up. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            error_msg = driver.find_element_by_css_selector(error_text).text

            list_actual = [error_msg]
            list_expected = [exp_parental_error_msg]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 5. Input wrong parental code: Check error mesage')
        except:
            self.list_steps.append(
                f'[Fail] 5. Input wrong parental code: Check error mesage. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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
            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0
            list_actual = [check_page_security]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 6. Input valid code. Check page Security displayed')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Input valid code. Check page Security displayed. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_02_Parental_code_Change_Confirmation(self):
        self.key = 'SECURITY_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        PARENTAL_CODE_KEY = '1234'
        PARENTAL_NEW_CODE_KEY = '4321'
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)
            # Goto media share USB
            goto_menu(driver, security_tab, security_parentalcontrol_tab)
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
            list_actual = [check_page_security, check_pop_up_disable]
            list_expected = [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check Security page displayed')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Check Security page displayed. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            # Input valid
            parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
            #  New
            ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_NEW_CODE_KEY).perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0
            time.sleep(1)
            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0

            list_actual = [check_page_security, check_pop_up_disable]
            list_expected = [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Change Parental code: Check Security page displayed. ')
            self.list_steps.append('[END TC]')

            parental_code = driver.find_element_by_css_selector(parental_code_card)
            parental_input = parental_code.find_elements_by_css_selector(input)

            # New parental code
            parental_input[1].send_keys(PARENTAL_CODE_KEY)
            # Retype parental code
            parental_input[2].send_keys(PARENTAL_CODE_KEY)

            # Apply
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)

        except:
            self.list_steps.append(
                f'[Fail] 4. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_03_Confirmation_Parental_code_Initialization(self):
        self.key = 'SECURITY_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        PARENTAL_CODE_KEY = '1234'
        PARENTAL_NEW_CODE_KEY = '4321'
        PARENTAL_INIT_CODE_KEY = '!@#$'
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)
            # Goto media share USB
            goto_menu(driver, security_tab, security_parentalcontrol_tab)
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

            check_page_security = len(driver.find_elements_by_css_selector(security_page)) != 0
            time.sleep(1)
            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0
            list_actual = [check_page_security, check_pop_up_disable]
            list_expected = [return_true, return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Apply successfully: Check Security page displayed and pop-up disappear')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Apply successfully: Check Security page displayed and pop-up disappear. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = [check_pop_init]
            list_expected = [return_true]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append('[Pass] 4. Send INIT key. Check pop-up init is displayed. ')
        except:
            self.list_steps.append(
                f'[Fail] 4. Change Parental code: Check Security page displayed. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            list_actual = ls_parental_name
            list_expected = exp_ls_parental_label
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Parental pop up labels')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Parental pop up labels. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
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

            check_page_security = driver.find_element_by_css_selector(security_page).is_displayed()
            time.sleep(1)
            check_pop_up_disable = len(driver.find_elements_by_css_selector(dialog_content)) == 0
            list_actual = [check_page_security, check_pop_up_disable]
            list_expected = [return_true, return_true]

            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check Parental pop up labels')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Parental pop up labels. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('6. Assertion wong.')

        self.assertListEqual(list_step_fail, [])

    def test_04_Parental_Control_function_On_Off_check(self):
        self.key = 'SECURITY_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        URL_LOGIN = get_config('URL', 'url')
        PARENTAL_CODE_KEY = '1234'

        SOCIAL_NW = 'Social Network'
        USER_DEFINE = 'User Define'
        FACEBOOK = 'facebook'
        GOOGLE = 'google.com'
        try:
            login(driver)
            time.sleep(1)
            # Goto Homepage
            driver.get(URL_LOGIN + homepage)
            wait_popup_disappear(driver, dialog_loading)
            # Goto media share USB
            goto_menu(driver, security_tab, security_parentalcontrol_tab)
            wait_popup_disappear(driver, dialog_loading)

            # Input valid
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

            ls_service_sub = driver.find_elements_by_css_selector('.service-sub-item-wrap')
            for s in ls_service_sub:
                if s.text == FACEBOOK:
                    if not len(s.find_elements_by_css_selector('.selected-icon')) > 0:
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
            driver.find_element_by_css_selector('tr:nth-child(2)>:nth-child(19).hight-light').click()
            driver.find_element_by_css_selector('tr:nth-child(2)>:nth-child(20).hight-light').click()
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
            list_actual = [ls_service_filter_items_value, block_schedule_value]
            list_expected = [exp_ls_service_filter_items_value, exp_block_schedule_value]
            check = assert_list(list_actual, list_expected)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Add rule: Check list of Service Filter and Block Schedule')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3. Add rule: Check list of Service Filter and Block Schedule. '
                f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
            list_step_fail.append('1,2,3. Assertion wong.')

        FACEBOOK = 'http://facebook.com'
        FACEBOOK_S = 'https://facebook.com'
        GOOGLE = 'http://google.com'
        GOOGLE_S = 'https://google.com'
        for i in range(1, 7):
            try:
                try:
                    fb_http_4 = requests.get(url=FACEBOOK, timeout=30).status_code
                except:
                    fb_http_4 = 500

                try:
                    fb_https_4 = requests.get(url=FACEBOOK_S, timeout=30).status_code
                except:
                    fb_https_4 = 500

                try:
                    gg_http_4 = requests.get(url=GOOGLE, timeout=30).status_code
                except:
                    gg_http_4 = 500

                try:
                    gg_https_4 = requests.get(url=GOOGLE_S, timeout=30).status_code
                except:
                    gg_https_4 = 500
                check_step_4 = all([i != 200 for i in [fb_http_4, fb_https_4, gg_http_4, gg_https_4]])
                # Disable Parental control
                parental_code = driver.find_element_by_css_selector(parental_code_card)
                parental_code_btn = parental_code.find_element_by_css_selector(select)
                parental_code_check = parental_code.find_element_by_css_selector(input)
                if parental_code_check.is_selected():
                    parental_code_btn.click()
                    # Input valid
                    parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                    if len(parental_field_input) > 0:
                        #  New
                        ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                        time.sleep(0.5)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)

                try:
                    fb_http_6 = requests.get(url=FACEBOOK, timeout=30).status_code
                except:
                    fb_http_6 = 500

                try:
                    fb_https_6 = requests.get(url=FACEBOOK_S, timeout=30).status_code
                except:
                    fb_https_6 = 500

                try:
                    gg_http_6 = requests.get(url=GOOGLE, timeout=30).status_code
                except:
                    gg_http_6 = 500

                try:
                    gg_https_6 = requests.get(url=GOOGLE_S, timeout=30).status_code
                except:
                    gg_https_6 = 500
                check_step_6 = all([i == 200 for i in [fb_http_6, fb_https_6, gg_http_6, gg_https_6]])

                # Enable
                parental_code = driver.find_element_by_css_selector(parental_code_card)
                parental_code_btn = parental_code.find_element_by_css_selector(select)
                parental_code_check = parental_code.find_element_by_css_selector(input)
                if not parental_code_check.is_selected():
                    parental_code_btn.click()
                    # Input valid
                    parental_field_input = driver.find_elements_by_css_selector(parental_wrap_input)
                    if len(parental_field_input) > 0:
                        #  New
                        ActionChains(driver).click(parental_field_input[0]).send_keys(PARENTAL_CODE_KEY).perform()
                        time.sleep(0.5)
                        driver.find_element_by_css_selector(btn_ok).click()
                        wait_popup_disappear(driver, dialog_loading)

                try:
                    fb_http_8 = requests.get(url=FACEBOOK, timeout=30).status_code
                except:
                    fb_http_8 = 500

                try:
                    fb_https_8 = requests.get(url=FACEBOOK_S, timeout=30).status_code
                except:
                    fb_https_8 = 500

                try:
                    gg_http_8 = requests.get(url=GOOGLE, timeout=30).status_code
                except:
                    gg_http_8 = 500

                try:
                    gg_https_8 = requests.get(url=GOOGLE_S, timeout=30).status_code
                except:
                    gg_https_8 = 500
                check_step_8 = all([i != 200 for i in [fb_http_8, fb_https_8, gg_http_8, gg_https_8]])

                list_actual = [check_step_4, check_step_6, check_step_8]
                list_expected = [return_false]*3
                check = assert_list(list_actual, list_expected)
                self.assertTrue(check["result"])
                self.list_steps.append(f'[Pass] 4-8. -{str(i+1)}-. Check Access to FB, GG. ')
                self.list_steps.append('[END TC]')
            except:
                self.list_steps.append(
                    f'[Fail] 4-8. -{str(i+1)}-. Check Access to FB, GG. '
                    f'Actual: {str(list_actual)}. Expected: {str(list_expected)}')
                self.list_steps.append('[END TC]')
                list_step_fail.append(f'4-8. -{str(i+1)}- Assertion wong.')

        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
