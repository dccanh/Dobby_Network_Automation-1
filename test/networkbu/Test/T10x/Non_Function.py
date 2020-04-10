#!/usr/bin/python
# -*- coding: utf8 -*-
import sys, json
sys.path.append('../../')
import unittest
from selenium import webdriver
import time
from datetime import datetime
# from Helper.t10x.config.captcha import *
from Helper.t10x.config.data_expected import *
from Helper.t10x.config.elements import *
# from Helper.t10x.config.read_config import *
from Helper.t10x.secure_crt.common import *
from Helper.t10x.common import *
from selenium import webdriver
from selenium.webdriver.support.select import Select
try:
    import pingparsing
except:
    os.system('pip install pingparsing')
    import pingparsing
import threading

METHOD = 'GET'
USER = get_config('ACCOUNT', 'user')
PW = get_config('ACCOUNT', 'password')
# token = get_token(USER, PW)
URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'

URL_5g = 'http://192.168.1.1/api/v1/wifi/1/ssid/0'


PING_TIMES = int(get_config('NON_FUNCTION', 'nf_ping_time', input_data_path))


class NON_FUNCTION(unittest.TestCase):
    def setUp(self):
        try:
            os.system('netsh wlan disconnect')
            time.sleep(3)
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            check_enable_ethernet()
            self.driver = webdriver.Chrome(driver_path)
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
        self.driver.quit()

    def test_02_NON_FUNC_Dynamic_Wired_Ping_Aging_INTERGRATION_WITH_05(self):
        self.key = 'NON_FUNCTION_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        PING_YOUTUBE = get_config('NON_FUNCTION', 'nf_ping_youtube', input_data_path)
        YOUTUBE_URL = get_config('NON_FUNCTION', 'nf_youtube_url', input_data_path)
        try:
            ping_result = 0.0

            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']

            count_interrupt = 0
            def thread_youtube():
                global count_interrupt, live_time
                # ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                # if ping_result['packet_loss_rate'] != 100.0:
                time.sleep(2)
                driver.get(YOUTUBE_URL)
                time.sleep(5)

                video_form = len(driver.find_elements_by_css_selector(ele_playing))

                count_video = 0
                while video_form == 0:
                    time.sleep(1)
                    video_form = len(driver.find_elements_by_css_selector(ele_playing))
                    # print(count_video)
                    count_video += 1
                    if count_video >= 30:
                        live_time = 0
                        break
                time.sleep(3)
                live_time = 0
                while live_time <= PING_TIMES:
                        buff_time = len(driver.find_elements_by_css_selector(ele_buffering))
                        time.sleep(1)
                        live_time += 1
                        print('Live time ' + str(live_time))
                        if buff_time == 1:
                            count_interrupt += 1

            thread1 = threading.Thread(target=thread_ping)
            thread2 = threading.Thread(target=thread_youtube)
            thread1.start()
            thread2.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            c, in_video_interface = 0, False
            while thread2.is_alive():
                print(str(thread2.is_alive()) + ' th2 - ' + str(c))
                video_form = len(driver.find_elements_by_css_selector(ele_playing))
                if video_form > 0:
                    in_video_interface = True
                time.sleep(1)
                c += 1
            time.sleep(2)

            list_actual2 = [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]
            list_expected2 = [return_true]*3

            check2 = assert_list(list_actual2, list_expected2)
            key = 'NON_FUNCTION_05'
            name = 'test_05_Wire_Streaming_Aging'
            duration = '0'
            if check2['result']:
                test_steps_pass = [f'[Pass] 1. On Stream {YOUTUBE_URL}; '
                                   f'{str(count_interrupt)} interrupt times;'
                                   f'{str(live_time)} live times', '[END TC]']
                write_ggsheet(key, test_steps_pass, name, duration, self.start_time)
            else:
                test_steps_fail = [f'[Fail] 1. On Stream {YOUTUBE_URL}; '
                                   f'{str(count_interrupt)} interrupt times;'
                                   f'{str(live_time)} live times', '[END TC]']
                write_ggsheet(key, test_steps_fail, name, duration, self.start_time)

            list_actual1 = [ping_result <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}'
                f'Loss rate {str(ping_result)}'
                f' on {str(PING_TIMES)} seconds.'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_03_NON_FUNC_Wireless_24GHz_Ping_Aging_INTERGRATION_WITH_06(self):
        self.key = 'NON_FUNCTION_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        PING_YOUTUBE = get_config('NON_FUNCTION', 'nf_ping_youtube', input_data_path)
        YOUTUBE_URL = get_config('NON_FUNCTION', 'nf_youtube_url', input_data_path)

        try:
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
        except:
            self.list_steps.append('[FAIL] Precondition connect 2G Wifi Fail')

        try:
            ping_result = 0.0

            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']

            count_interrupt = 0
            def thread_youtube():
                global count_interrupt, live_time
                # ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                # if ping_result['packet_loss_rate'] != 100.0:
                time.sleep(2)
                driver.get(YOUTUBE_URL)
                time.sleep(5)

                video_form = len(driver.find_elements_by_css_selector(ele_playing))

                count_video = 0
                while video_form == 0:
                    time.sleep(1)
                    video_form = len(driver.find_elements_by_css_selector(ele_playing))
                    # print(count_video)
                    count_video += 1
                    if count_video >= 30:
                        live_time = 0
                        break
                time.sleep(3)
                live_time = 0
                while live_time <= PING_TIMES:
                    buff_time = len(driver.find_elements_by_css_selector(ele_buffering))
                    time.sleep(1)
                    live_time += 1
                    print('Live time ' + str(live_time))
                    if buff_time == 1:
                        count_interrupt += 1

            thread1 = threading.Thread(target=thread_ping)
            thread2 = threading.Thread(target=thread_youtube)
            thread2.start()
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            c, in_video_interface = 0, False

            while thread2.is_alive():
                print(str(thread2.is_alive()) + ' th2 - ' + str(c))
                video_form = len(driver.find_elements_by_css_selector(ele_playing))
                if video_form > 0:
                    in_video_interface = True
                time.sleep(1)
                c += 1

            time.sleep(3)
            print(live_time)
            list_actual2 = [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]
            list_expected2 = [return_true]*3

            check2 = assert_list(list_actual2, list_expected2)
            key = 'NON_FUNCTION_06'
            name = 'test_06_Wireless_24GHz_Streaming_Aging'
            duration = '0'
            if check2['result']:
                test_steps_pass = [f'[Pass] 1. On Stream {YOUTUBE_URL}; '
                                   f'{str(count_interrupt)} interrupt times;'
                                   f'{str(live_time)} live times', '[END TC]']
                write_ggsheet(key, test_steps_pass, name, duration, self.start_time)
            else:
                test_steps_fail = [f'[Fail] 1. On Stream {YOUTUBE_URL}; '
                                   f'{str(count_interrupt)} interrupt times;'
                                   f'{str(live_time)} live times', '[END TC]']
                write_ggsheet(key, test_steps_fail, name, duration, self.start_time)

            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)

            list_actual1 = [ping_result <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {str(ping_result)} on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {str(ping_result)} on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_04_NON_FUNC_Wireless_5GHz_Ping_Aging_INTERGRATION_WITH_07(self):
        self.key = 'NON_FUNCTION_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        PING_YOUTUBE = get_config('NON_FUNCTION', 'nf_ping_youtube', input_data_path)
        YOUTUBE_URL = get_config('NON_FUNCTION', 'nf_youtube_url', input_data_path)

        try:
            new_5g_wf_name = api_change_wifi_setting(URL_5g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_5g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_5g_wf_name}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_5g_wf_name}" name="{new_5g_wf_name}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(4)
        except:
            self.list_steps.append('[FAIL] Precondition connect 5G Wifi Fail')

        try:
            ping_result = 0.0
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']

            count_interrupt = 0
            def thread_youtube():
                global count_interrupt, live_time
                # ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                # if ping_result['packet_loss_rate'] != 100.0:
                time.sleep(2)
                driver.get(YOUTUBE_URL)
                time.sleep(5)

                video_form = len(driver.find_elements_by_css_selector(ele_playing))

                count_video = 0
                while video_form == 0:
                    time.sleep(1)
                    video_form = len(driver.find_elements_by_css_selector(ele_playing))
                    # print(count_video)
                    count_video += 1
                    if count_video >= 30:
                        live_time = 0
                        break
                time.sleep(3)
                live_time = 0
                while live_time <= PING_TIMES:
                        buff_time = len(driver.find_elements_by_css_selector(ele_buffering))
                        time.sleep(1)
                        live_time += 1
                        print('Live time ' + str(live_time))
                        if buff_time == 1:
                            count_interrupt += 1

            thread1 = threading.Thread(target=thread_ping)
            thread2 = threading.Thread(target=thread_youtube)
            thread1.start()
            thread2.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            c, in_video_interface = 0, False
            while thread2.is_alive():
                print(str(thread2.is_alive()) + ' th2 - ' + str(c))
                video_form = len(driver.find_elements_by_css_selector(ele_playing))
                if video_form > 0:
                    in_video_interface = True
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual2 = [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]
            list_expected2 = [return_true]*3

            check2 = assert_list(list_actual2, list_expected2)
            key = 'NON_FUNCTION_07'
            name = 'test_07_Wireless_5GHz_Streaming_Aging'
            duration = '0'
            if check2['result']:
                test_steps_pass = [f'[Pass] 1. On Stream {YOUTUBE_URL}; '
                                   f'{str(count_interrupt)} interrupt times;'
                                   f'{str(live_time)} live times', '[END TC]']
                write_ggsheet(key, test_steps_pass, name, duration, self.start_time)
            else:
                test_steps_fail = [f'[Fail] 1. On Stream {YOUTUBE_URL}; '
                                   f'{str(count_interrupt)} interrupt times;'
                                   f'{str(live_time)} live times', '[END TC]']
                write_ggsheet(key, test_steps_fail, name, duration, self.start_time)

            actual_check_ping = ping_result <= 1.0
            list_actual1 = [actual_check_ping]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_08_NON_FUNC_Static_Wired_Ping_Aging(self):
        self.key = 'NON_FUNCTION_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)

        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if check_login:
                wait_visible(driver, welcome_language)
                time.sleep(1)
                # Click start btn
                driver.find_element_by_css_selector(welcome_start_btn).click()
                time.sleep(3)
                wait_visible(driver, welcome_change_pw_fields)
                change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

                # A list contain values: Current Password, New Password, Retype new pw
                ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
                for p, v in zip(change_pw_fields, ls_change_pw_value):
                    ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                    time.sleep(0.5)

                # Next Change pw
                time.sleep(3)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)

                # Next Operation Mode
                time.sleep(3)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                    time.sleep(0.5)

                # Click arrow down
                time.sleep(3)
                driver.find_element_by_css_selector(option_select).click()
                time.sleep(2)
                ls_connection_type = driver.find_elements_by_css_selector(
                    welcome_internet_setup1_ls_option_connection_type)

                # Click Static IP
                for i in ls_connection_type:
                    if i.text == 'Static IP':
                        i.click()
                time.sleep(1)

                dns_2_input = driver.find_elements_by_css_selector('.wrap-form:last-child .wrap-input input')
                for i in dns_2_input:
                    ActionChains(driver).move_to_element(i).click().send_keys('0').perform()
                    time.sleep(0.5)

                len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))
                while len_let_go == 0:
                    # Next Internet Setup 1
                    time.sleep(2)
                    wait_visible(driver, welcome_next_btn)
                    next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                    if not next_btn.get_property('disabled'):
                        next_btn.click()
                        time.sleep(3)
                    len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))

                # Click Let's Go
                time.sleep(3)
                driver.find_element_by_css_selector(welcome_let_go_btn).click()
                # Write config
                save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(2)
                wait_visible(driver, home_view_wrap)
                time.sleep(5)

                wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            check_ota_auto_update(driver)
            time.sleep(1)
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            os.system(f'netsh wlan disconnect interface="Wi-Fi"')
            time.sleep(5)
        except:
            self.list_steps.append('[Fail] Precondition connect 5G Wifi Fail')

        try:
            ping_result = 0.0

            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']
            thread1 = threading.Thread(target=thread_ping)
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual1 = [ping_result <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_09_NON_FUNC_Static_Wireless_24GHz_Ping_Aging(self):
        self.key = 'NON_FUNCTION_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if check_login:
                wait_visible(driver, welcome_language)
                time.sleep(1)
                # Click start btn
                driver.find_element_by_css_selector(welcome_start_btn).click()
                time.sleep(3)
                wait_visible(driver, welcome_change_pw_fields)
                change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

                # A list contain values: Current Password, New Password, Retype new pw
                ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
                for p, v in zip(change_pw_fields, ls_change_pw_value):
                    ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                    time.sleep(0.5)

                # Next Change pw
                time.sleep(3)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)

                # Next Operation Mode
                time.sleep(3)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                    time.sleep(0.5)

                # Click arrow down
                time.sleep(3)
                driver.find_element_by_css_selector(option_select).click()
                time.sleep(2)
                ls_connection_type = driver.find_elements_by_css_selector(
                    welcome_internet_setup1_ls_option_connection_type)

                # Click Static IP
                for i in ls_connection_type:
                    if i.text == 'Static IP':
                        i.click()
                time.sleep(1)

                dns_2_input = driver.find_elements_by_css_selector('.wrap-form:last-child .wrap-input input')
                for i in dns_2_input:
                    ActionChains(driver).move_to_element(i).click().send_keys('0').perform()
                    time.sleep(0.5)

                len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))
                while len_let_go == 0:
                    # Next Internet Setup 1
                    time.sleep(2)
                    wait_visible(driver, welcome_next_btn)
                    next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                    if not next_btn.get_property('disabled'):
                        next_btn.click()
                        time.sleep(3)
                    len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))

                # Click Let's Go
                time.sleep(3)
                driver.find_element_by_css_selector(welcome_let_go_btn).click()
                # Write config
                save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(2)
                wait_visible(driver, home_view_wrap)
                time.sleep(5)

                wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            check_ota_auto_update(driver)
            time.sleep(15)
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(5)
        except:
            self.list_steps.append('[Fail] Precondition connect 2G Wifi Fail')

        try:
            ping_result = 0.0

            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']
            thread1 = threading.Thread(target=thread_ping)
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual1 = [ping_result <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_10_NON_FUNC_Static_Wireless_5GHz_Ping_Aging(self):
        self.key = 'NON_FUNCTION_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        # ===========================================================
        factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        NEW_PASSWORD = get_config('COMMON', 'new_pw', input_data_path)
        try:
            login(driver)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            # Goto Homepage
            check_login = len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0
            if check_login:
                wait_visible(driver, welcome_language)
                time.sleep(1)
                # Click start btn
                driver.find_element_by_css_selector(welcome_start_btn).click()
                time.sleep(3)
                wait_visible(driver, welcome_change_pw_fields)
                change_pw_fields = driver.find_elements_by_css_selector(welcome_change_pw_fields)

                # A list contain values: Current Password, New Password, Retype new pw
                ls_change_pw_value = [get_config('ACCOUNT', 'password'), NEW_PASSWORD, NEW_PASSWORD]
                for p, v in zip(change_pw_fields, ls_change_pw_value):
                    ActionChains(driver).move_to_element(p).click().send_keys(v).perform()
                    time.sleep(0.5)

                # Next Change pw
                time.sleep(3)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                time.sleep(5)

                # Next Operation Mode
                time.sleep(3)
                wait_visible(driver, welcome_next_btn)
                next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                if not next_btn.get_property('disabled'):
                    next_btn.click()
                    time.sleep(0.5)

                # Click arrow down
                time.sleep(3)
                driver.find_element_by_css_selector(option_select).click()
                time.sleep(2)
                ls_connection_type = driver.find_elements_by_css_selector(
                    welcome_internet_setup1_ls_option_connection_type)

                # Click Static IP
                for i in ls_connection_type:
                    if i.text == 'Static IP':
                        i.click()
                time.sleep(1)

                dns_2_input = driver.find_elements_by_css_selector('.wrap-form:last-child .wrap-input input')
                for i in dns_2_input:
                    ActionChains(driver).move_to_element(i).click().send_keys('0').perform()
                    time.sleep(0.5)

                len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))
                while len_let_go == 0:
                    # Next Internet Setup 1
                    time.sleep(2)
                    wait_visible(driver, welcome_next_btn)
                    next_btn = driver.find_element_by_css_selector(welcome_next_btn)
                    if not next_btn.get_property('disabled'):
                        next_btn.click()
                        time.sleep(3)
                    len_let_go = len(driver.find_elements_by_css_selector(welcome_let_go_btn))

                # Click Let's Go
                time.sleep(3)
                driver.find_element_by_css_selector(welcome_let_go_btn).click()
                # Write config
                save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
                wait_popup_disappear(driver, dialog_loading)
                time.sleep(2)
                wait_visible(driver, home_view_wrap)
                time.sleep(5)

                wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            check_ota_auto_update(driver)

            time.sleep(15)
            new_5g_wf_name = api_change_wifi_setting(URL_5g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_5g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_5g_wf_name}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_5g_wf_name}" name="{new_5g_wf_name}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
        except:
            self.list_steps.append('[Fail] Precondition connect 5G Wifi Fail')

        try:
            ping_result = 0.0

            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']

            thread1 = threading.Thread(target=thread_ping)
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual1 = [ping_result <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; Loss rate: {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_14_NON_FUNC_Extender_Aging_Wireless_24GHz(self):
        self.key = 'NON_FUNCTION_14'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)

        upper_2g_name = get_config('REPEATER', 'repeater_name', input_data_path)
        upper_2g_pw = get_config('REPEATER', 'repeater_pw', input_data_path)
        connect_repeater_mode(driver, REPEATER_UPPER=upper_2g_name, PW=upper_2g_pw)
        # ===========================================================

        PING_ADDRESS = '192.168.1.1'
        # PING_YOUTUBE = get_config('NON_FUNCTION', 'nf_ping_youtube', input_data_path)
        YOUTUBE_URL = get_config('NON_FUNCTION', 'nf_youtube_url', input_data_path)
        try:
            ping_result = 0.0

            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']

            count_interrupt = 0

            def thread_youtube():
                global count_interrupt, live_time
                # ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                # if ping_result['packet_loss_rate'] != 100.0:
                time.sleep(2)
                driver.get(YOUTUBE_URL)
                time.sleep(5)

                video_form = len(driver.find_elements_by_css_selector(ele_playing))

                count_video = 0
                while video_form == 0:
                    time.sleep(1)
                    video_form = len(driver.find_elements_by_css_selector(ele_playing))
                    # print(count_video)
                    count_video += 1
                    if count_video >= 30:
                        live_time = 0
                        break
                time.sleep(3)
                live_time = 0
                while live_time <= PING_TIMES:
                    buff_time = len(driver.find_elements_by_css_selector(ele_buffering))
                    time.sleep(1)
                    live_time += 1
                    print('Live time ' + str(live_time))
                    if buff_time == 1:
                        count_interrupt += 1

            thread1 = threading.Thread(target=thread_ping)
            thread2 = threading.Thread(target=thread_youtube)
            thread1.start()
            thread2.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            c, in_video_interface = 0, False
            while thread2.is_alive():
                print(str(thread2.is_alive()) + ' th2 - ' + str(c))
                video_form = len(driver.find_elements_by_css_selector(ele_playing))
                if video_form > 0:
                    in_video_interface = True
                time.sleep(1)
                c += 1
            time.sleep(2)

            # list_actual2 = [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]
            # list_expected2 = [return_true] * 3

            list_actual1 = [[ping_result <= 1.0], [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]]
            list_expected1 = [[return_true],  [return_true] * 3]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {str(ping_result)} '
                f'on {str(PING_TIMES)} seconds. '
                f'Check Youtube live stream: interrupt times =0, run enough time and in playing video mode. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}'
                f'Loss rate {str(ping_result)}'
                f' on {str(PING_TIMES)} seconds. '
                f'Check Youtube live stream: interrupt times =0, run enough time and in playing video mode. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    # def test_15_NON_FUNC_Extender_Aging_Wireless_5GHz(self):
    #     self.key = 'NON_FUNCTION_15'
    #     driver = self.driver
    #     self.def_name = get_func_name()
    #     list_step_fail = []
    #     self.list_steps = []
    #     # ===========================================================
    #     grand_login(driver)
    #     time.sleep(2)
    #     goto_menu(driver, network_tab, network_operationmode_tab)
    #
    #     upper_5g_name = get_config('REPEATER', 'repeater_name_5g', input_data_path)
    #     upper_5g_pw = get_config('REPEATER', 'repeater_pw_5g', input_data_path)
    #     # connect_repeater_mode(driver, REPEATER_UPPER=upper_5g_name, PW=upper_5g_pw)
    #     scan_wifi_repeater_mode(driver, upper_5g_name, upper_5g_pw)
    #     # ===========================================================
    #
    #     PING_ADDRESS = '192.168.1.1'
    #     # PING_YOUTUBE = get_config('NON_FUNCTION', 'nf_ping_youtube', input_data_path)
    #     YOUTUBE_URL = get_config('NON_FUNCTION', 'nf_youtube_url', input_data_path)
    #     try:
    #         ping_result = 0.0
    #
    #         def thread_ping():
    #             global ping_result
    #             ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)['packet_loss_rate']
    #
    #         count_interrupt = 0
    #
    #         def thread_youtube():
    #             global count_interrupt, live_time
    #             # ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
    #             # if ping_result['packet_loss_rate'] != 100.0:
    #             time.sleep(2)
    #             driver.get(YOUTUBE_URL)
    #             time.sleep(5)
    #
    #             video_form = len(driver.find_elements_by_css_selector(ele_playing))
    #
    #             count_video = 0
    #             while video_form == 0:
    #                 time.sleep(1)
    #                 video_form = len(driver.find_elements_by_css_selector(ele_playing))
    #                 # print(count_video)
    #                 count_video += 1
    #                 if count_video >= 30:
    #                     live_time = 0
    #                     break
    #             time.sleep(3)
    #             live_time = 0
    #             while live_time <= PING_TIMES:
    #                 buff_time = len(driver.find_elements_by_css_selector(ele_buffering))
    #                 time.sleep(1)
    #                 live_time += 1
    #                 print('Live time ' + str(live_time))
    #                 if buff_time == 1:
    #                     count_interrupt += 1
    #
    #         thread1 = threading.Thread(target=thread_ping)
    #         thread2 = threading.Thread(target=thread_youtube)
    #         thread1.start()
    #         thread2.start()
    #
    #         c = 0
    #         while thread1.is_alive():
    #             print(str(thread1.is_alive()) + ' th1 - ' + str(c))
    #             time.sleep(1)
    #             c += 1
    #
    #         c, in_video_interface = 0, False
    #         while thread2.is_alive():
    #             print(str(thread2.is_alive()) + ' th2 - ' + str(c))
    #             video_form = len(driver.find_elements_by_css_selector(ele_playing))
    #             if video_form > 0:
    #                 in_video_interface = True
    #             time.sleep(1)
    #             c += 1
    #         time.sleep(2)
    #
    #         # list_actual2 = [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]
    #         # list_expected2 = [return_true] * 3
    #
    #         list_actual1 = [[ping_result <= 1.0], [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]]
    #         list_expected1 = [[return_true],  [return_true] * 3]
    #         check = assert_list(list_actual1, list_expected1)
    #         self.assertTrue(check["result"])
    #         self.list_steps.append(
    #             f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
    #             f'Loss rate {str(ping_result)} '
    #             f'on {str(PING_TIMES)} seconds. '
    #             f'Check Youtube live stream: interrupt times =0, run enough time and in playing video mode. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         self.list_steps.append('[END TC]')
    #     except:
    #         self.list_steps.append(
    #             f'[Fail] 1, 2. Check Ping {PING_ADDRESS}'
    #             f'Loss rate {str(ping_result)}'
    #             f' on {str(PING_TIMES)} seconds. '
    #             f'Check Youtube live stream: interrupt times =0, run enough time and in playing video mode. '
    #             f'Actual: {str(list_actual1)}. '
    #             f'Expected: {str(list_expected1)}')
    #         self.list_steps.append('[END TC]')
    #         list_step_fail.append('1, 2. Assertion wong')
    #
    #     self.assertListEqual(list_step_fail, [])

    def test_48_MAIN_System_Router_mode_Check_Manual_Firmware_Update_operation(self):
        self.key = 'MAIN_48'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        detect_firmware_version(driver)
        # try:
        #     grand_login(driver)
        #     time.sleep(1)
        #
        #     pre_firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
        #     if not pre_firmware_version.endswith(expected_firmware_30012):
        #
        #         driver.find_element_by_css_selector(system_btn).click()
        #         time.sleep(1)
        #         driver.find_element_by_css_selector(ele_sys_firmware_update).click()
        #         time.sleep(1)
        #
        #         os.chdir(files_path)
        #         firmware_40012_path = os.path.join(os.getcwd(), 't10x_fullimage_3.00.12_rev11.img')
        #         driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40012_path)
        #         os.chdir(test_t10x_path)
        #         driver.find_element_by_css_selector(apply).click()
        #         time.sleep(1)
        #         if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
        #             driver.find_element_by_css_selector(ele_choose_firmware_select).click()
        #         time.sleep(0.5)
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(0.5)
        #         if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
        #             driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(0.5)
        #         wait_popup_disappear(driver, dialog_loading)
        #         wait_visible(driver, content)
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(1)
        #
        #     self.list_steps.append(
        #         f'[Pass] 0. Precondition goto firm 3.00.12 success. ')
        # except:
        #     self.list_steps.append(
        #         f'[Fail] 0. Precondition goto firm 3.00.12 fail. ')
        #     list_step_fail.append('0. Assertion wong')

        try:
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(1)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)
            popup_title = driver.find_element_by_css_selector(ele_check_for_update_title).text
            popup_sub_title = driver.find_element_by_css_selector(sub_title_popup_cls).text

            list_actual1 = [popup_title, popup_sub_title]
            list_expected1 = ['Firmware Update', exp_sub_title_update_firmware]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Goto firmware update. Check title and subtitle of popup'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Goto firmware update. Check title and subtitle of popup. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_40012_path = os.path.join(os.getcwd(), 't10x_fullimage_4.00.12_rev11.img')
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40012_path)
            os.chdir(test_t10x_path)
            # Check firmware btn activated
            check_firmware_btn = driver.find_element_by_css_selector(apply).is_enabled()

            list_actual2 = [check_firmware_btn]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Choose firmware file. Check button Firmware Update activated'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Choose firmware file. Check button Firmware Update activated. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [check_login_page]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3, 4. Click Firmware Update button. After reboot. Check login popup displayed. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 3, 4. Click Firmware Update button. After reboot. Check login popup displayed. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('3, 4. Assertion wong')

        try:
            grand_login(driver)
            firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
            check_firmware = True if firmware_version.endswith(expected_firmware_40012) else False

            list_actual5 = [check_firmware]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Login again. Check firmware version end with {expected_firmware_40012}. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Login again. Check firmware version end with {expected_firmware_40012}. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_49_MAIN_System_Router_mode_Check_Manual_downgrade_firmware(self):
        self.key = 'MAIN_49'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        detect_firmware_version(self.driver)
        # try:
        #     grand_login(driver)
        #     time.sleep(1)
        #
        #     pre_firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
        #     if not pre_firmware_version.endswith(expected_firmware_30012):
        #         driver.find_element_by_css_selector(system_btn).click()
        #         time.sleep(1)
        #         driver.find_element_by_css_selector(ele_sys_firmware_update).click()
        #         time.sleep(1)
        #         os.chdir(files_path)
        #         firmware_30012_path = os.path.join(os.getcwd(), 't10x_fullimage_3.00.12_rev11.img')
        #         driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_30012_path)
        #         os.chdir(test_t10x_path)
        #         driver.find_element_by_css_selector(apply).click()
        #         time.sleep(1)
        #         if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
        #             driver.find_element_by_css_selector(ele_choose_firmware_select).click()
        #         time.sleep(0.5)
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(0.5)
        #         if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
        #             driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(0.5)
        #         wait_popup_disappear(driver, dialog_loading)
        #         wait_visible(driver, content)
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(1)
        #
        #     self.list_steps.append(
        #         f'[Pass] 0. Precondition goto firm 3.00.12 success. ')
        # except:
        #     self.list_steps.append(
        #         f'[Fail] 0. Precondition goto firm 3.00.12 fail. ')
        #     list_step_fail.append('0. Assertion wong')

        try:
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(1)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)
            popup = driver.find_element_by_css_selector(dialog_content)

            popup_title = popup.find_element_by_css_selector(ele_check_for_update_title).text
            popup_sub_title = popup.find_element_by_css_selector(sub_title_popup_cls).text

            list_label = [i.text for i in popup.find_elements_by_css_selector(label_name_in_2g)]

            btn_update_text = popup.find_element_by_css_selector(apply).text

            list_actual1 = [popup_title, popup_sub_title,
                            list_label,
                            btn_update_text]
            list_expected1 = ['Firmware Update', exp_sub_title_update_firmware,
                              ['Model name', 'Current Version', 'Build time', 'Manual Upgrade'],
                              'Update']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Goto firmware update. Check title, subtitle, list label and button update text of popup '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Goto firmware update. Check title, subtitle, list label and button update text of popup. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_30005_path = os.path.join(os.getcwd(), 't10x_fullimage_3.00.05_rev09.img')
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_30005_path)
            os.chdir(test_t10x_path)
            # Check firmware btn activated
            check_firmware_btn = driver.find_element_by_css_selector(apply).is_enabled()

            list_actual2 = [check_firmware_btn]
            list_expected2 = [return_true]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2, 3. Choose firmware file. Check button Firmware Update activated'
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2, 3. Choose firmware file. Check button Firmware Update activated. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [check_login_page]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Click Firmware Update button. After reboot. Check login popup displayed. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Click Firmware Update button. After reboot. Check login popup displayed. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong')

        try:
            url_login = get_config('URL', 'url')
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')

            call_api_login_old_firmware(user_request, pass_word)
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')
            time.sleep(1)
            driver.get(url_login)
            time.sleep(2)
            driver.find_element_by_css_selector(el_lg_user_down_firm).send_keys(user_request)
            time.sleep(1)
            driver.find_element_by_css_selector(el_lg_pw_down_firm).send_keys(pass_word)
            time.sleep(1)
            driver.find_element_by_css_selector(el_lg_button_down_firm).click()

            wait_visible(driver, el_home_wrap_down_firm)
            time.sleep(2)
            firmware_version = driver.find_element_by_css_selector(el_home_info_firm_version_down_firm).text
            check_firmware = True if firmware_version.endswith(expected_firmware_30005) else False

            list_actual5 = [check_firmware]
            list_expected5 = [return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5. Login again. Check firmware version end with {expected_firmware_40012}. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 5. Login again. Check firmware version end with {expected_firmware_40012}. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_51_MAIN_System_Router_mode_Check_the_exception_message_when_firmware_update(self):
        self.key = 'MAIN_51'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ======================================
        firmware_40011 = 't5_t7_t9_fullimage_4.00.11_rev25.img'
        firmware_30012 = 't10x_fullimage_3.00.12_rev11.img'
        file_no_format = 'wifi_default_file.xml'
        firmware_40012 = 't10x_fullimage_4.00.12_rev11.img'
        detect_firmware_version(self.driver)
        # try:
        #     grand_login(driver)
        #     time.sleep(1)
        #
        #     pre_firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
        #     if not pre_firmware_version.endswith(expected_firmware_30012):
        #         driver.find_element_by_css_selector(system_btn).click()
        #         time.sleep(1)
        #         driver.find_element_by_css_selector(ele_sys_firmware_update).click()
        #         time.sleep(1)
        #         os.chdir(files_path)
        #         firmware_30012_path = os.path.join(os.getcwd(), firmware_30012)
        #         driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_30012_path)
        #         driver.find_element_by_css_selector(apply).click()
        #         time.sleep(1)
        #         if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
        #             driver.find_element_by_css_selector(ele_choose_firmware_select).click()
        #         time.sleep(0.5)
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(0.5)
        #         if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
        #             driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(0.5)
        #         wait_popup_disappear(driver, dialog_loading)
        #         wait_visible(driver, content)
        #         driver.find_element_by_css_selector(btn_ok).click()
        #         time.sleep(1)
        #
        #     self.list_steps.append(
        #         f'[Pass] 0. Precondition goto firm 3.00.12 success. ')
        # except:
        #     self.list_steps.append(
        #         f'[Fail] 0. Precondition goto firm 3.00.12 fail. ')
        #     list_step_fail.append('0. Assertion wong')

        try:
            grand_login(driver)
            time.sleep(1)
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(1)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)
            popup = driver.find_element_by_css_selector(dialog_content)
            popup_title = popup.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual1 = [popup_title]
            list_expected1 = ['Firmware Update']
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Goto firmware update. Check title, subtitle, list label and button update text of popup '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Goto firmware update. Check title, subtitle, list label and button update text of popup. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        try:
            os.chdir(files_path)
            no_format_path = os.path.join(os.getcwd(), file_no_format)
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(no_format_path)
            # Check firmware btn activated

            error_warning = driver.find_element_by_css_selector(err_dialog_msg_cls).text
            driver.find_element_by_css_selector(btn_ok).click()

            list_actual2 = [error_warning]
            list_expected2 = [exp_msg_invalid_file_firmware]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Up wrong file. Check Error warning message. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 2. Up wrong file. Check Error warning message. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_40011_path = os.path.join(os.getcwd(), firmware_40011)
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40011_path)
            # Check firmware btn activated

            manual_update_value = driver.find_element_by_css_selector(el_firmware_manual_box_value).text

            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) >0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            wait_visible(driver, dialog_content)
            time.sleep(1)
            cpt_popup_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            popup = driver.find_element_by_css_selector(dialog_content)
            popup_title2 = popup.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual3 = [manual_update_value, cpt_popup_msg, popup_title2]
            list_expected3 = [firmware_40011, exp_msg_update_fail_file_firmware, 'Firmware Update']
            check = assert_list(list_actual3, list_expected3)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Manual update file: Check upload success,  popup msg, popup firmware udate display after click OK. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Manual update file: Check upload success,  popup msg, popup firmware udate display after click OK. '
                f'Actual: {str(list_actual3)}. '
                f'Expected: {str(list_expected3)}')
            list_step_fail.append('3. Assertion wong')

        try:
            os.chdir(files_path)
            firmware_40012_path = os.path.join(os.getcwd(), firmware_40012)
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40012_path)
            os.chdir(test_t10x_path)

            driver.find_element_by_css_selector(apply).click()
            time.sleep(1)
            if len(driver.find_elements_by_css_selector(ele_choose_firmware_select)) > 0:
                driver.find_element_by_css_selector(ele_choose_firmware_select).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            if len(driver.find_elements_by_css_selector(btn_ok)) > 0:
                driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(0.5)
            wait_popup_disappear(driver, dialog_loading)
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
            check_firmware = True if firmware_version.endswith(expected_firmware_40012) else False

            list_actual4 = [check_firmware]
            list_expected4 = [return_true]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Login again. Check firmware version end with {expected_firmware_40012}. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 4. Login again. Check firmware version end with {expected_firmware_40012}. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')
        detect_firmware_version(driver)
        self.assertListEqual(list_step_fail, [])

    def test_84_MAIN_Verification_of_Bridge_mode_Menu_Tree(self):
        self.key = 'MAIN_84'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        detect_firmware_version(self.driver)
        try:
            grand_login(driver)
            time.sleep(1)

            goto_menu(driver, network_tab, network_operationmode_tab)
            # Click to Bridge mode
            driver.find_element_by_css_selector(ele_select_bridge_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            # wait_ping('dearmyextender.net')
            time.sleep(3)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')

            check_login = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual1 = [check_login]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Change Operation mode to Bridge mode. Apply. Check login page displayed.'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Change Operation mode to Bridge mode. Apply. Check login page displayed. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1, 2. Assertion wong')

        try:
            grand_login(driver)
            check_wan_mode_text = driver.find_element_by_css_selector(home_connection_description).text

            USER = get_config('ACCOUNT', 'user')
            PW = get_config('ACCOUNT', 'password')
            METHOD = 'GET'
            _TOKEN = get_token(USER, PW)
            URL_API = get_config('URL', 'url') + '/api/v1/network/qmode'
            BODY = ''
            res = call_api(URL_API, METHOD, BODY, _TOKEN)

            expected_response = {"operation": "ap",
                                 "qmode": "extender"}

            list_actual2 = [check_wan_mode_text, res]
            list_expected2 = ['Bridge Mode', expected_response]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 3. Check Text in Wan connection icon; Check API network/qmode. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 3. Check Text in Wan connection icon; Check API network/qmode. '
                f'Actual: {str(list_actual2)}. '
                f'Expected: {str(list_expected2)}')
            list_step_fail.append('3. Assertion wong')

        try:
            ls_menu_enable = driver.find_elements_by_css_selector(ele_home_tree_menu_enable)
            ls_menu_enable_text = [i.text for i in ls_menu_enable]

            ls_menu_disable = driver.find_elements_by_css_selector(ele_home_tree_menu_disable)
            ls_menu_disable_text = [i.text for i in ls_menu_disable]

            list_actual4 = [ls_menu_enable_text, ls_menu_disable_text]
            list_expected4 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'ADVANCED'],
                              ['QOS', 'SECURITY']]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 4. Check list tree menu Enable, list tree menu disable. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check list tree menu Enable, list tree menu disable. '
                f'Actual: {str(list_actual4)}. '
                f'Expected: {str(list_expected4)}')
            list_step_fail.append('4. Assertion wong')

        try:
            # Click Network
            goto_menu(driver, network_tab, 0)
            network_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click WL
            goto_menu(driver, wireless_tab, 0)
            wireless_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click MS
            goto_menu(driver, media_share_tab, 0)
            media_share_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]
            time.sleep(1)
            # Click ADVANCED
            goto_menu(driver, advanced_tab, 0)
            advanced_submenu = [i.text for i in driver.find_elements_by_css_selector(ele_home_sub_menu)]


            list_actual5 = [network_submenu, wireless_submenu, media_share_submenu, advanced_submenu]
            list_expected5 = [['Operation Mode'], ['Primary Network', 'Guest Network', 'WPS'],
                              ['USB', 'Server Setting'], ['Wireless', 'Diagnostics']]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 5, 6, 7, 8. Check Sub menu of NETWORK, WIRELESS, MS, ADVANCED. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5, 6, 7, 8. Check Sub menu of NETWORK, WIRELESS, MS, ADVANCED. '
                f'Actual: {str(list_actual5)}. '
                f'Expected: {str(list_expected5)}')
            list_step_fail.append('5, 6, 7, 8. Assertion wong')

        try:
            # CLick system button
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()

            time.sleep(1)
            sys_button_text = [i.text for i in driver.find_elements_by_css_selector(ele_sys_list_button)]


            list_actual9 = sorted(sys_button_text)
            list_expected9 = sorted(['Language', 'Firmware Update', 'Change Password', 'Backup/Restore',
                               'Restart/Factory Reset', 'Power Saving Mode', 'LED Mode', 'Date/Time', 'Wizard'])
            check = assert_list(list_actual9, list_expected9)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 9. Check list button in System button. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 9. Check list button in System button. '
                f'Actual: {str(list_actual9)}. '
                f'Expected: {str(list_expected9)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('9. Assertion wong')
        self.assertListEqual(list_step_fail, [])

    def test_85_2_MAIN_Verification_of_Login_page_on_Bridge_mode(self):
        self.key = 'MAIN_85_2'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        url_login = get_config('URL', 'url')
        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'password')
        save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        detect_firmware_version(self.driver)
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # Get and write URL
            driver.get(url_login)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
            captcha_text = get_captcha_string(captcha_src)
            act = ActionChains(driver)
            act.send_keys(user_request)
            act.send_keys(Keys.TAB)
            act.send_keys(pass_word)
            act.send_keys(Keys.TAB)
            act.send_keys(captcha_text)
            act.perform()

            driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
            time.sleep(3)
            wait_visible(driver, home_view_wrap)
            # Check Privacy Policy
            policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) > 0
            welcome_popup = len(driver.find_elements_by_css_selector(lg_welcome_header)) > 0
            home_view = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            check_tab_true = False
            if any([policy_popup, welcome_popup, home_view]):
                check_tab_true = True

            list_actual1 = [check_tab_true]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 1,2,3. Check function TAB key in login: TAB step by step, Click login check. Check login ok'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1,2,3.Check function TAB key in login: TAB step by step, Click login check. Check login ok'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1,2,3. Assertion wong')

        try:
            time.sleep(5)
            driver.get(url_login)
            time.sleep(3)

            welcome_text = driver.find_element_by_css_selector(lg_welcome_text).text
            id_holder = driver.find_element_by_css_selector(lg_user).get_attribute('placeholder')
            password_holder = driver.find_element_by_css_selector(lg_password).get_attribute('placeholder')
            captcha_holder = driver.find_element_by_css_selector(lg_captcha_box).get_attribute('placeholder')
            extra_lg_info = driver.find_element_by_css_selector(lg_extra_info).text

            list_actual2 = [welcome_text,
                            id_holder,
                            password_holder,
                            captcha_holder,
                            extra_lg_info]
            list_expected2 = [expected_welcome_text_en,
                              exp_lg_id_holder,
                              exp_lg_password_holder,
                              exp_lg_captcha_holder,
                              exp_lg_extra_info]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 4. Check Login page component: Welcome, user holder, pw holder, captcha holer, extra info. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
        except:
            self.list_steps.append(
                f'[Fail] 4. Check Login page component: Welcome, user holder, pw holder, captcha holer, extra info. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append(
                '4. Assertion wong.')

        try:
            # Connect wifi
            URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(10)


            check_connected_2g_name = current_connected_wifi()
            driver.get(url_login)
            time.sleep(2)
            check_lg_page_2g = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual5 = [check_connected_2g_name, check_lg_page_2g]
            list_expected5 = [new_2g_wf_name, return_true]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 5. Check Connect wifi 2g. Check login page displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
        except:
            self.list_steps.append(
                f'[Fail] 5. Check Connect wifi 2g. Check login page displayed. '
                f'Actual: {str(list_actual5)}. Expected: {str(list_expected5)}')
            list_step_fail.append(
                '5. Assertion wong.')

        try:
            # Connect wifi
            URL_5g = get_config('URL', 'url') + '/api/v1/wifi/1/ssid/0'
            new_5g_wf_name = api_change_wifi_setting(URL_5g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_5g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_5g_wf_name}"')
            time.sleep(3)
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_5g_wf_name}" name="{new_5g_wf_name}"')
            time.sleep(10)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            check_connected_5g_name = current_connected_wifi()
            driver.get(url_login)
            time.sleep(2)
            check_lg_page_5g = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual6 = [check_connected_5g_name, check_lg_page_5g]
            list_expected6 = [new_5g_wf_name, return_true]
            check = assert_list(list_actual6, list_expected6)
            self.assertTrue(check["result"])
            self.list_steps.append(
                '[Pass] 6. Check Connect wifi 5g. Check login page displayed. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 6. Check Connect wifi 5g. Check login page displayed. '
                f'Actual: {str(list_actual6)}. Expected: {str(list_expected6)}')
            list_step_fail.append(
                '6. Assertion wong.')
            self.list_steps.append('[END TC]')
        # ================================================================
        factory_dut()
        save_config(config_path, 'URL', 'url', get_config('URL', 'sub_url'))
        # ================================================================
        detect_firmware_version(driver)

        self.assertListEqual(list_step_fail, [])

    def test_45_HOME_Verification_of_Network_Map_WAN_information(self):
        self.key = 'HOME_45'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        detect_firmware_version(self.driver)
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
            time.sleep(2)
            policy_popup = len(driver.find_elements_by_css_selector(lg_privacy_policy_pop)) > 0
            welcome_popup = len(driver.find_elements_by_css_selector(lg_welcome_header)) > 0
            home_view = len(driver.find_elements_by_css_selector(home_view_wrap)) > 0

            check_tab_true = False
            if any([policy_popup, welcome_popup, home_view]):
                check_tab_true = True

            list_actual1 = [check_tab_true]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1. Login Web UI successfully. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
        except:
            self.list_steps.append(
                f'[Fail] 1. Login Web UI successfully. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            list_step_fail.append('1. Assertion wong')

        try:
            driver.find_element_by_css_selector(home_img_connection).click()
            time.sleep(1)
            check_bridge_mode = driver.find_element_by_css_selector(home_connection_mode).text
            check_ip_assigned = driver.find_element_by_css_selector(home_conection_img_wan_ip).text != '0.0.0.0'

            wan_card = driver.find_elements_by_css_selector(ele_wan_block)[0]
            list_label = [i.text for i in wan_card.find_elements_by_css_selector(label_name_in_2g)]

            expected_label = ['Connection Status',
                              'Connection Type',
                              'IP Address',
                              'Subnet Mask',
                              'Gateway',
                              'DNS Server 1',
                              'DNS Server 2',
                              'MAC Address']

            list_actual2 = [check_bridge_mode, check_ip_assigned, list_label]
            list_expected2 = ['Bridge Mode', return_true, expected_label]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 2. Check Bridge Mode, IP address assigned different 0.0.0.0. '
                f'Check list label displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 2. Check Bridge Mode, IP address assigned different 0.0.0.0. '
                f'Check list label displayed. '
                f'Actual: {str(list_actual2)}. Expected: {str(list_expected2)}')
            list_step_fail.append('2. Assertion wong.')
            self.list_steps.append('[END TC]')

        self.assertListEqual(list_step_fail, [])

if __name__ == '__main__':
    unittest.main()
