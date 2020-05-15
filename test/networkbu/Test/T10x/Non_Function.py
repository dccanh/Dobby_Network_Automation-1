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
            os.system('netsh wlan delete profile name=*')
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
            step_1_2_name = f"1, 2. Check Ping {PING_ADDRESS}; "
            list_check_in_step_1_2 = ["Condition 'ping result less than 1.0' is correct"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
        # factory_dut()
        # ===========================================================
        PING_ADDRESS = get_config('NON_FUNCTION', 'nf_ping_address', input_data_path)
        PING_YOUTUBE = get_config('NON_FUNCTION', 'nf_ping_youtube', input_data_path)
        YOUTUBE_URL = get_config('NON_FUNCTION', 'nf_youtube_url', input_data_path)

        try:
            grand_login(driver)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            block2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
            ssid_2g = wireless_get_default_ssid(block2g, 'Network Name(SSID)')
            pw_2g = wireless_check_pw_eye(driver, block2g, change_pw=False)
            # new_2g_wf_name = api_change_wifi_setting(URL_2g)
            # time.sleep(10)
            # write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            # time.sleep(3)
            # os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            # time.sleep(3)
            # # Connect Default 2GHz
            # os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            # time.sleep(5)
            #
            # os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            # time.sleep(10)
            current_connect = connect_wifi_by_command(ssid_2g, pw_2g)
            print(current_connect)
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
                driver.get(YOUTUBE_URL)
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
            step_1_name = f"1. Check Ping {PING_ADDRESS}; "
            list_check_in_step_1 = [
                f"Condition 'count interrupt == 0' is correct",
                f"Condition 'live time >= {PING_TIMES}' is correct",
                f"Condition 'in video interface' is correct"
            ]

            check2 = assert_list(list_actual2, list_expected2)
            self.assertTrue(check2["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_name,
                    list_check_in_step=list_check_in_step_1,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
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
            step_2_name = "2.Check Ping loss rate"
            list_check_in_step_2 = ["Condition 'Ping loss rate less than 1%' is correct"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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
            step_1_2_name = f"1, 2. Check Ping {PING_ADDRESS}; "
            list_check_in_step_1_2 = ["Condition 'Ping loss rate less than 1%' is correct"]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])

            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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

            step_1_2_name = f"1, 2. Check Ping {PING_ADDRESS}; "
            list_check_in_step_1_2 = ["Condition 'Ping loss rate less than 1%' is correct"]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
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

            step_1_2_name = f'1, 2. Check Ping {PING_ADDRESS}; '
            list_check_in_step_1_2 = ["Condition 'Ping loss rate less than 1%' is correct"]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_14_NON_FUNC_Extender_Aging_Wireless_24GHz(self):
        self.key = 'NON_FUNCTION_14'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)

        upper_2g_name = get_config('REPEATER', 'repeater_name', input_data_path)
        upper_2g_pw = get_config('REPEATER', 'repeater_pw', input_data_path)
        connect_repeater_mode(driver, REPEATER_UPPER=upper_2g_name, PW=upper_2g_pw, force=True)
        wait_ethernet_available()
        interface_connect_disconnect('Wi-Fi', 'enable')
        # ===========================================================
        try:
            wait_ethernet_available()
            URL_wifi_2g = 'http://dearmyextender.net/api/v1/wifi/0/ssid/0'
            extender_MAC = api_change_wifi_setting(URL_wifi_2g, get_only_mac=True)
            print(extender_MAC)
            wifi = connect_wifi_by_command(upper_2g_name, upper_2g_pw)
            interface_connect_disconnect('Ethernet', 'disable')
            connected_mac = get_current_wifi_MAC()
            print(connected_mac)
            if extender_MAC != connected_mac:
                os.system('netsh wlan delete profile name=*')
                wifi = connect_wifi_by_command(upper_2g_name, upper_2g_pw)
            connected_mac = get_current_wifi_MAC()
            print(connected_mac)
            print(wifi)
            list_actual0 = [connected_mac]
            list_expected0 = [extender_MAC]
            step_0_name = "0. Precondition. Connect wifi of Extender router 2G. "
            list_check_in_step_0 = [f"mac address of extender router is: {extender_MAC}"]

            check = assert_list(list_actual0, list_expected0)
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
                time.sleep(5)
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

            list_actual1 = [[ping_result <= 1.0], [count_interrupt == 0, live_time >= PING_TIMES, in_video_interface]]
            list_expected1 = [[return_true],  [return_true] * 3]
            step_1_2_name = f'1, 2. Check Ping {PING_ADDRESS}; '
            list_check_in_step_1_2 = [
                "Condition 'Ping loss rate less than 1%' is correct",
                "Condition 'Streaming should be played without interruption' is correct"
            ]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_15_NON_FUNC_Extender_Aging_Wireless_5GHz(self):
        self.key = 'NON_FUNCTION_15'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        # ===========================================================
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        wait_popup_disappear(driver, dialog_loading)
        upper_5g_name = get_config('REPEATER', 'repeater_name_5g', input_data_path)
        upper_5g_pw = get_config('REPEATER', 'repeater_pw_5g', input_data_path)
        connect_repeater_mode(driver, REPEATER_UPPER=upper_5g_name, PW=upper_5g_pw)
        wait_ethernet_available()

        wifi = connect_wifi_by_command(upper_5g_name, upper_5g_pw)
        interface_connect_disconnect('Ethernet', 'disable')

        print(wifi)

        try:
            wait_ethernet_available()
            URL_wifi_5g = 'http://dearmyextender.net/api/v1/wifi/1/ssid/0'
            extender_MAC = api_change_wifi_setting(URL_wifi_5g, get_only_mac=True)
            print(extender_MAC)
            wifi = connect_wifi_by_command(upper_5g_name, upper_5g_pw)
            interface_connect_disconnect('Ethernet', 'disable')
            connected_mac = get_current_wifi_MAC()
            print(connected_mac)
            if extender_MAC != connected_mac:
                os.system('netsh wlan delete profile name=*')
                wifi = connect_wifi_by_command(upper_5g_name, upper_5g_pw)
            connected_mac = get_current_wifi_MAC()
            print(wifi)
            list_actual0 = [connected_mac]
            list_expected0 = [extender_MAC]
            step_0_name = "0. Precondition. Connect wifi of Extender router 5G. "
            list_check_in_step_0 = [f"Mac address of extender router is: {extender_MAC}"]

            check = assert_list(list_actual0, list_expected0)
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
                time.sleep(5)
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

            list_actual1 = [ping_result <= 1.0, (count_interrupt == 0) and
                            (live_time >= PING_TIMES) and in_video_interface]
            list_expected1 = [return_true,  return_true]
            step_1_2_name = f'1, 2. Check Ping {PING_ADDRESS}; '
            list_check_in_step_1_2 = [
                "Condition 'Ping loss rate less than 1%' is correct",
                "Condition 'Streaming should be played without interruption' is correct"
            ]

            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_1_2_name,
                    list_check_in_step=list_check_in_step_1_2,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])


    def test_45_HOME_Verification_of_Network_Map_WAN_information(self):
        self.key = 'HOME_45'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        detect_firmware_version(driver)

        grand_login(driver)
        time.sleep(1)
        goto_menu(driver, network_tab, network_operationmode_tab)
        # Click to Bridge mode
        if not driver.find_element_by_css_selector(ele_bridge_mode_input).is_selected():
            driver.find_element_by_css_selector(ele_select_bridge_mode).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(apply).click()
            time.sleep(0.5)
            driver.find_element_by_css_selector(btn_ok).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(3)
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        wait_ethernet_available()
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            # time.sleep(20)
            wait_ethernet_available()
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
            step_1_name = "1. Login Web UI successfully. "
            list_check_in_step_1 = ["Login success"]
            check = assert_list(list_actual1, list_expected1)
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
            step_2_name = "2. Check Bridge Mode, IP address assigned different 0.0.0.0. Check list label displayed."
            list_check_in_step_2 = [
                f"Operation mode is: Bridge Mode",
                "Condition 'Assigned IP is different 0.0.0.0' is correct",
                f"List label is: {';'.join(expected_label)}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong.')
            self.list_steps.append('[END TC]')

        self.assertListEqual(list_step_fail, [])

    def test_48_MAIN_System_Router_mode_Check_Manual_Firmware_Update_operation(self):
        self.key = 'MAIN_48'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        detect_firmware_version(driver)
        wait_ethernet_available()
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
            list_expected1 = ['Update', exp_sub_title_update_firmware]
            step_1_name = "1. Goto firmware update. Check title and subtitle of popup. "
            list_check_in_step_1 = [
                "Popup title is: Update",
                f"Popup sub title is: {exp_sub_title_update_firmware}"
            ]

            check = assert_list(list_actual1, list_expected1)
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
            step_2_name = "2. Choose firmware file. Check button Firmware Update activated"
            list_check_in_step_2 = ["Button firmware update is enabled"]
            check = assert_list(list_actual2, list_expected2)
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
            wait_ethernet_available()
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [check_login_page]
            list_expected4 = [return_true]
            step_3_4_name = "3, 4. Click Firmware Update button. After reboot. Check login popup displayed. "
            list_check_in_step_3_4 = ["Login popup is appear"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_4_name,
                    list_check_in_step=list_check_in_step_3_4,
                    list_actual=list_actual4,
                    list_expected=list_expected4
                )
            )
            list_step_fail.append('3, 4. Assertion wong')

        try:
            grand_login(driver)
            firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
            check_firmware = True if firmware_version.endswith(expected_firmware_40012) else False

            list_actual5 = [check_firmware]
            list_expected5 = [return_true]
            step_5_name = f"5. Login again. Check firmware version end with {expected_firmware_40012}. "
            list_check_in_step_5 = ["Firmware version is update correct"]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        list_step_fail.append('5. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_49_MAIN_System_Router_mode_Check_Manual_downgrade_firmware(self):
        self.key = 'MAIN_49'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        detect_firmware_version(driver)
        wait_ethernet_available()
        try:
            time.sleep(20)
            wait_ethernet_available()
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
            step_1_name = "1. Goto firmware update. Check title, subtitle, list label and button update text of popup "
            list_check_in_step_1 = [
                f"Popup title is: {list_expected1[0]}",
                f"Popup sub title is: {list_expected1[1]}",
                f"List label is: {';'.join(list_expected1[2])}",
                f"Text of button update is: {list_expected1[3]}"
            ]
            check = assert_list(list_actual1, list_expected1)
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
            step_2_3_name = "2, 3. Choose firmware file. Check button Firmware Update activated"
            list_check_in_step_2_3 = ["Button Firmware Update is enabled"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_3_name,
                    list_check_in_step=list_check_in_step_2_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('2. Assertion wong')

        try:
            os.system('netsh wlan delete profile name=*')
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
            wait_ethernet_available()
            wait_visible(driver, content)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            wait_ethernet_available()
            check_login_page = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [check_login_page]
            list_expected4 = [return_true]
            step_4_name = "4. Click Firmware Update button. After reboot. Check login popup displayed. "
            list_check_in_step_4 = ["Login popup is appear"]
            check = assert_list(list_actual4, list_expected4)
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
            list_step_fail.append('4. Assertion wong')

        try:
            url_login = get_config('URL', 'url')
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')

            call_api_login_old_firmware(user_request, pass_word)
            user_request = get_config('ACCOUNT', 'user')
            pass_word = get_config('ACCOUNT', 'password')
            time.sleep(20)

            wait_ethernet_available()
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
            step_5_name = f"5. Login again. Check firmware version end with {expected_firmware_30005}. "
            list_check_in_step_5 = ["Firmware version is updated success"]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step_5,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('5. Assertion wong')
        detect_firmware_version(driver)
        self.assertListEqual(list_step_fail, [])

    def test_51_MAIN_System_Router_mode_Check_the_exception_message_when_firmware_update(self):
        self.key = 'MAIN_51'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # factory_dut()
        # ======================================
        firmware_40011 = 't5_t7_t9_fullimage_4.00.11_rev25.img'
        firmware_30012 = 't10x_fullimage_3.00.12_rev11.img'
        file_no_format = 'wifi_default_file.xml'
        firmware_40012 = 't10x_fullimage_4.00.12_rev11.img'
        detect_firmware_version(driver)
        wait_ethernet_available()
        try:
            time.sleep(20)
            wait_ethernet_available()
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
            step_1_name = "1. Goto firmware update. Check title, subtitle, list label and button update text of popup "
            list_check_in_step_1 = [f"Popup title is: {list_expected1[0]}"]
            check = assert_list(list_actual1, list_expected1)
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
            list_step_fail.append('1. Assertion wong')

        try:
            time.sleep(5)
            os.chdir(files_path)
            no_format_path = os.path.join(os.getcwd(), file_no_format)
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(no_format_path)
            # Check firmware btn activated
            time.sleep(1)
            error_warning = driver.find_element_by_css_selector(err_dialog_msg_cls).text
            driver.find_element_by_css_selector(btn_ok).click()

            list_actual2 = [error_warning]
            list_expected2 = [exp_msg_invalid_file_firmware]
            step_2_name = "2. Up wrong file. Check Error warning message. "
            list_check_in_step_2 = [f"Error message is: {exp_msg_invalid_file_firmware}"]
            check = assert_list(list_actual2, list_expected2)
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
            list_step_fail.append('2. Assertion wong')

        try:
            time.sleep(2)
            os.chdir(files_path)
            firmware_40011_path = os.path.join(os.getcwd(), firmware_40011)
            driver.find_element_by_css_selector(ele_choose_firmware_file).send_keys(firmware_40011_path)
            # Check firmware btn activated
            time.sleep(0.5)
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
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(5)
            wait_popup_disappear(driver, icon_loading)

            cpt_popup_msg = driver.find_element_by_css_selector(complete_dialog_msg).text
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(2)

            popup = driver.find_element_by_css_selector(dialog_content)
            popup_title2 = popup.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual3 = [manual_update_value, cpt_popup_msg, popup_title2]
            list_expected3 = [firmware_40011, exp_msg_update_fail_file_firmware, 'Firmware Update']
            step_3_name = "3. Manual update file: Check upload success,  popup msg, " \
                          "popup firmware udate display after click OK."
            list_check_in_step_3 = [
                f"Firmware value is: {list_expected3[0]}",
                f"Warning message is: {list_expected3[1]}",
                f"Popup title is: {list_expected3[2]}"
            ]
            check = assert_list(list_actual3, list_expected3)
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
            list_step_fail.append('3. Assertion wong')

        try:
            time.sleep(2)
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
            time.sleep(30)
            wait_popup_disappear(driver, dialog_loading)
            wait_popup_disappear(driver, icon_loading)
            wait_visible(driver, content)
            wait_popup_disappear(driver, icon_loading)
            wait_ethernet_available()
            time.sleep(5)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)
            wait_ethernet_available()
            grand_login(driver)
            firmware_version = driver.find_element_by_css_selector(ele_home_info_firm_version).text
            check_firmware = True if firmware_version.endswith(expected_firmware_40012) else False

            list_actual4 = [check_firmware]
            list_expected4 = [return_true]
            step_4_name = f"4. Login again. Check firmware version end with {expected_firmware_40012}. "
            list_check_in_step_4 = ["Firmware version is updated success"]
            check = assert_list(list_actual4, list_expected4)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_4_name,
                    list_check_in_step=list_check_in_step_4,
                    list_actual=list_actual1,
                    list_expected=list_expected1
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('4. Assertion wong')
        change_firmware_version(driver)
        self.assertListEqual(list_step_fail, [])

    def test_84_MAIN_Verification_of_Bridge_mode_Menu_Tree(self):
        self.key = 'MAIN_84'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        factory_dut()
        detect_firmware_version(driver)
        wait_ethernet_available()
        try:
            time.sleep(20)
            wait_ethernet_available()
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
            step_1_2_name = "1, 2. Change Operation mode to Bridge mode. Apply. Check login page displayed."
            list_check_in_step_1_2 = ["Login page is appear"]

            check = assert_list(list_actual1, list_expected1)
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
            step_3_name = "3. Check Text in Wan connection icon; Check API network/qmode. "
            list_check_in_step_3 = [
                f"Wan connection icon is: {list_expected2[0]}",
                f"Expected response is: {list_expected2[1]}",
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            ls_menu_enable = driver.find_elements_by_css_selector(ele_home_tree_menu_enable)
            ls_menu_enable_text = [i.text for i in ls_menu_enable]

            ls_menu_disable = driver.find_elements_by_css_selector(ele_home_tree_menu_disable)
            ls_menu_disable_text = [i.text for i in ls_menu_disable]

            list_actual4 = [ls_menu_enable_text, ls_menu_disable_text]
            list_expected4 = [['HOME', 'NETWORK', 'WIRELESS', 'MEDIA SHARE', 'ADVANCED'],
                              ['QOS', 'SECURITY']]
            step_4_name = "4. Check list tree menu Enable, list tree menu disable. "
            list_check_in_step_4 = [
                f"List tree menu Enable is: {list_expected4[0]}",
                f"List tree menu Disable is: {list_expected4[1]}"
            ]
            check = assert_list(list_actual4, list_expected4)
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
            step_5_6_7_8_name = "5, 6, 7, 8. Check Sub menu of NETWORK, WIRELESS, MS, ADVANCED. "
            list_check_in_step_5_6_7_8 = [
                f"Network submenu is: {list_expected5[0]}",
                f"Wireless submenu is: {list_expected5[0]}",
                f"Media share submenu is: {list_expected5[0]}",
                f"Advanced submenu is: {list_expected5[0]}",
            ]

            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_7_8_name,
                    list_check_in_step=list_check_in_step_5_6_7_8,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_6_7_8_name,
                    list_check_in_step=list_check_in_step_5_6_7_8,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5, 6, 7, 8. Assertion wong')

        try:
            # CLick system button
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()

            time.sleep(1)
            sys_button_text = [i.text for i in driver.find_elements_by_css_selector(ele_sys_list_button)]

            list_actual9 = [";".join(sorted(sys_button_text))]
            list_expected9 = [";".join(sorted(['Language', 'Firmware Update', 'Change Password', 'Backup/Restore',
                                               'Restart/Factory Reset', 'Power Saving Mode', 'LED Mode', 'Date/Time',
                                               'Wizard']))]
            step_9_name = "9. Check list button in System button. "
            list_check_in_step_9 = [f"List buttons in system is: {list_expected9[0]}"]
            check = assert_list(list_actual9, list_expected9)
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
        factory_dut()
        detect_firmware_version(driver)
        wait_ethernet_available()

        grand_login(driver)
        time.sleep(1)
        goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)

        block_2g = driver.find_elements_by_css_selector(wl_primary_card)[0]
        wifi_name_2g = wireless_get_default_ssid(block_2g, 'Network Name(SSID)')
        wifi_pw_2g = wireless_check_pw_eye(driver, block_2g, change_pw=False)

        block_5g = driver.find_elements_by_css_selector(wl_primary_card)[1]
        wifi_name_5g = wireless_get_default_ssid(block_5g, 'Network Name(SSID)')
        wifi_pw_5g = wireless_check_pw_eye(driver, block_5g, change_pw=False)


        goto_menu(driver, network_tab, network_operationmode_tab)
        # Click to Bridge mode
        if not driver.find_element_by_css_selector(ele_bridge_mode_input).is_selected():
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
            wait_ethernet_available()
            save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        # ~~~~~~~~~~~~~~~~~~~~~~ Check login ~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            time.sleep(20)
            wait_ethernet_available()
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
            step_1_2_3_name = "1,2,3. Check function TAB key in login: " \
                              "TAB step by step, Click login check. Check login ok"
            list_check_in_step_1_2_3 = ["Login success"]
            check = assert_list(list_actual1, list_expected1)
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
            step_4_name = "4. Check Login page component: " \
                          "Welcome, user holder, pw holder, captcha holer, extra info. "
            list_check_in_step_4 = [
                f"Wellcome message is {expected_welcome_text_en}",
                f"Placeholder of ID input box is {exp_lg_id_holder}",
                f"Placeholder of Password input box is {exp_lg_password_holder}",
                f"Placeholder of Security code is {exp_lg_captcha_holder}",
                f"Guide message is {exp_lg_extra_info}"
            ]
            check = assert_list(list_actual2, list_expected2)
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
            list_step_fail.append(
                '4. Assertion wong.')

        try:
            connect_wifi_by_command(wifi_name_2g, wifi_pw_2g)
            time.sleep(10)
            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)

            check_connected_2g_name = current_connected_wifi()

            check_lg_page_2g = check_connect_to_web_admin_page()

            list_actual5 = [check_connected_2g_name, check_lg_page_2g]
            list_expected5 = [wifi_name_2g, return_true]
            step_5_name = "5. Check Connect wifi 2g. Check login page displayed. "
            list_check_in_step_5 = [
                f"Connected wifi name is: {list_expected5[0]}",
                "Login page is appear"
            ]
            check = assert_list(list_actual5, list_expected5)
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
            list_step_fail.append(
                '5. Assertion wong.')

        try:
            # Connect wifi
            connect_wifi_by_command(wifi_name_5g, wifi_pw_5g)
            time.sleep(10)

            # os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(3)
            check_connected_5g_name = current_connected_wifi()
            check_lg_page_5g = check_connect_to_web_admin_page()

            list_actual6 = [check_connected_5g_name, check_lg_page_5g]
            list_expected6 = [wifi_name_5g, return_true]
            step_6_name = "6. Check Connect wifi 5g. Check login page displayed. "
            list_check_in_step_6 = [
                f"Connected wifi name is: {list_expected6[0]}",
                "Login page is appear"
            ]
            check = assert_list(list_actual6, list_expected6)
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(10)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_6_name,
                    list_check_in_step=list_check_in_step_6,
                    list_actual=list_actual6,
                    list_expected=list_expected6
                )
            )
            list_step_fail.append(
                '6. Assertion wong.')
            self.list_steps.append('[END TC]')
        # ================================================================
        # factory_dut()
        # save_config(config_path, 'URL', 'url', get_config('URL', 'sub_url'))
        # # ================================================================
        # detect_firmware_version(driver)

        self.assertListEqual(list_step_fail, [])



    def test_65_MAIN_System_Verification_of_Restart_Factory_Reset_operation(self):
        self.key = 'MAIN_65'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # ===========================================================
        factory_dut()
        # ===========================================================
        NEW_PASSWORD_2 = get_config('MAIN', 'main65_new_pw', input_data_path)
        SSID_2G_NEW = get_config('MAIN', 'main65_ssid_2g_new', input_data_path)
        WL_PW_2G = get_config('MAIN', 'main65_wl_pw_2g', input_data_path)
        try:
            time.sleep(20)
            wait_ethernet_available()
            grand_login(driver)
            # Change login password
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_change_pw).click()
            time.sleep(0.2)

            change_pw(driver, NEW_PASSWORD_2)
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD_2)
            # Click ok
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(3)

            grand_login(driver)

            #  Change wireless SSID and PW of 2.4GHz
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            left_2g = driver.find_element_by_css_selector(left)
            ssid_2g = left_2g.find_element_by_css_selector('input[placeholder="Enter the network name (SSID)"]')
            ActionChains(driver).click(ssid_2g).key_down(Keys.CONTROL).send_keys('a') \
                .send_keys(Keys.DELETE).key_up(Keys.CONTROL).send_keys(SSID_2G_NEW).perform()

            pw_2g = left_2g.find_element_by_css_selector('input[placeholder="Enter the Password"]')
            ActionChains(driver).click(pw_2g).key_down(Keys.CONTROL).send_keys('a') \
                .send_keys(Keys.DELETE).key_up(Keys.CONTROL).send_keys(WL_PW_2G).perform()

            left_2g.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            # Enable QOS
            goto_menu(driver, qos_tab, 0)
            time.sleep(1)
            select_btn = driver.find_element_by_css_selector(select)
            if not select_btn.find_element_by_css_selector(input).is_selected():
                select_btn.click()
            wait_popup_disappear(driver, dialog_loading)
            time.sleep(1)

            # Change Firewall to Medium
            goto_menu(driver, security_tab, security_firewall_tab)
            time.sleep(1)
            driver.find_element_by_css_selector(ele_firewall_medium).click()
            time.sleep(1)
            driver.find_element_by_css_selector(apply).click()
            wait_popup_disappear(driver, dialog_loading)
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(1)

            self.list_steps.append(
                '[Pass] Precondition Pass. Change PW, Change Wireless SSID, PW, Enable QoS, Set Firewall is Medium')
        except:
            self.list_steps.append(
                '[Fail] Precondition Fail. Change PW, Change Wireless SSID, PW, Enable QoS, Set Firewall is Medium')
            list_step_fail.append('Assertion wong')

        try:
            # Reset/ Factory Reset
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(sys_reset).click()
            time.sleep(0.5)
            # Check Pop up title
            popup = driver.find_element_by_css_selector(dialog_content)
            popup_title = popup.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual1 = [popup_title]
            list_expected1 = ['Restart/Factory Reset']
            step_1_2_name = "1, 2. System> Reset/ Factory Reset. Check title popup appear. "
            list_check_in_step_1_2 = [f"Popup title is: {list_expected1[0]}"]
            check = assert_list(list_actual1, list_expected1)
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
            list_step_fail.append('1, 2. Assertion wong')

        try:
            # Popup button
            buttons = popup.find_elements_by_css_selector(apply)
            # Click restart
            buttons[0].click()
            time.sleep(1)
            confirm_dialog_title = driver.find_element_by_css_selector(confirm_dialog_msg).text
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            popup_2 = driver.find_element_by_css_selector(dialog_content)
            popup_title_2 = popup_2.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual2 = [confirm_dialog_title, popup_title_2]
            list_expected2 = [exp_restart_confirm_msg, 'Restart/Factory Reset']
            step_3_name = "3. Click Restart. Check confirm message. Click Cancel. Return to previous state."
            list_check_in_step_3 = [
                f"Confirm message is: {exp_restart_confirm_msg}",
                f"Popup title is: {list_expected2[1]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_3_name,
                    list_check_in_step=list_check_in_step_3,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            list_step_fail.append('3. Assertion wong')

        try:
            popup = driver.find_element_by_css_selector(dialog_content)
            # Popup button
            buttons = popup.find_elements_by_css_selector(apply)
            # Click restart
            buttons[0].click()
            time.sleep(1)
            confirm_dialog_title = driver.find_element_by_css_selector(confirm_dialog_msg).text
            # Click Cancel
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(150)
            wait_popup_disappear(driver, dialog_loading)
            wait_visible(driver, lg_page)
            check_login_displayed = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual4 = [confirm_dialog_title, check_login_displayed]
            list_expected4 = [exp_restart_confirm_msg, return_true]
            step_4_name = "4. Click Restart. Check confirm message. Click OK. Check Login page displayed."
            list_check_in_step_4 = [
                f"Confirm message is: {exp_restart_confirm_msg}",
                "Login page is appear"
            ]
            check = assert_list(list_actual4, list_expected4)
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
            list_step_fail.append('4. Assertion wong')

        try:
            grand_login(driver)
            # Wireless > Primary Network
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            left_2g = driver.find_element_by_css_selector(left)
            check_wireless_ssid = wireless_get_default_ssid(left_2g, 'Network Name(SSID)')
            check_wireless_pw = wireless_check_pw_eye(driver, left_2g, change_pw=False)
            # QOS
            goto_menu(driver, qos_tab, 0)
            time.sleep(1)
            select_btn = driver.find_element_by_css_selector(select)
            check_enable_qos = select_btn.find_element_by_css_selector(input).is_selected()
            # Firewall
            goto_menu(driver, security_tab, security_firewall_tab)
            time.sleep(1)
            check_medium_firewall = len(driver.find_elements_by_css_selector(ele_firewall_lv_medium)) > 0
            time.sleep(1)

            list_actual5 = [[check_wireless_ssid, check_wireless_pw],
                            check_enable_qos,
                            check_medium_firewall]
            list_expected5 = [[SSID_2G_NEW, WL_PW_2G],
                              return_true,
                              return_true]
            step_5_name = "5. Verify state after restart: "
            list_check_in_step = [
                "Wireless ssid and password is correct",
                "QOS is enable",
                "Condition 'firewall is medium' is correct"
            ]
            check = assert_list(list_actual5, list_expected5)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_5_name,
                    list_check_in_step=list_check_in_step,
                    list_actual=list_actual5,
                    list_expected=list_expected5
                )
            )
            list_step_fail.append('5. Assertion wong')

        try:
            # Reset/ Factory Reset
            system_button = driver.find_element_by_css_selector(system_btn)
            ActionChains(driver).move_to_element(system_button).click().perform()
            time.sleep(0.5)
            driver.find_element_by_css_selector(sys_reset).click()
            time.sleep(0.5)
            # Check Pop up title
            popup = driver.find_element_by_css_selector(dialog_content)
            popup_title = popup.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual6 = [popup_title]
            list_expected6 = ['Restart/Factory Reset']
            step_6_name = "6. System> Reset/ Factory Reset. Check title popup appear. "
            list_check_in_step_6 = [f"Popup title is: {list_expected6[0]}"]
            check = assert_list(list_actual6, list_expected6)
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
            list_step_fail.append('6. Assertion wong')

        try:
            # Popup button
            buttons = popup.find_elements_by_css_selector(apply)
            # Click restart
            buttons[1].click()
            time.sleep(1)
            confirm_dialog_title = driver.find_element_by_css_selector(confirm_dialog_msg).text
            # Click Cancel
            driver.find_element_by_css_selector(btn_cancel).click()
            time.sleep(1)
            popup_2 = driver.find_element_by_css_selector(dialog_content)
            popup_title_2 = popup_2.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual7 = [confirm_dialog_title, popup_title_2]
            list_expected7 = [exp_factory_restart_confirm_msg, 'Restart/Factory Reset']
            step_7_name = "7. Click Factory Restart. Check confirm message. Click Cancel. Return to previous state."
            list_check_in_step_7 = [
                f"Confirm message is: {exp_factory_restart_confirm_msg}",
                f"Popup title is: {list_expected7[1]}"
            ]
            check = assert_list(list_actual7, list_expected7)
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
            list_step_fail.append('7. Assertion wong')

        try:
            popup = driver.find_element_by_css_selector(dialog_content)
            # Popup button
            buttons = popup.find_elements_by_css_selector(apply)
            # Click restart
            buttons[1].click()
            time.sleep(1)
            confirm_dialog_title = driver.find_element_by_css_selector(confirm_dialog_msg).text
            # Click Cancel
            driver.find_element_by_css_selector(btn_ok).click()
            time.sleep(150)
            wait_popup_disappear(driver, dialog_loading)
            wait_visible(driver, lg_page)
            check_login_displayed = len(driver.find_elements_by_css_selector(lg_page)) > 0

            list_actual8 = [confirm_dialog_title, check_login_displayed]
            list_expected8 = [exp_factory_restart_confirm_msg, return_true]
            step_8_name = "8. Click Factory Restart. Check confirm message. Click OK. Check Login page displayed."
            list_check_in_step_8 = [
                f"Confirm message is: {exp_factory_restart_confirm_msg}",
                "Login page appear"
            ]
            check = assert_list(list_actual8, list_expected8)
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
            list_step_fail.append('8. Assertion wong')

        try:
            wait_ethernet_available()

            filename_2 = 'account2.txt'
            command_2 = 'capitest get Device.Users.User.2. leaf'
            run_cmd(command_2, filename_2)
            time.sleep(10)
            url_login = get_config('URL', 'url')
            get_result_command_from_server_api(url_login, filename_2)
            wait_ethernet_available()
            grand_login(driver)
            # Wireless > Primary Network
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            time.sleep(1)
            left_2g = driver.find_element_by_css_selector(left)
            check_wireless_ssid = wireless_get_default_ssid(left_2g, 'Network Name(SSID)')
            check_wireless_pw = wireless_check_pw_eye(driver, left_2g, change_pw=False)
            # QOS
            goto_menu(driver, qos_tab, 0)
            time.sleep(1)
            select_btn = driver.find_element_by_css_selector(select)
            check_enable_qos = select_btn.find_element_by_css_selector(input).is_selected() is False
            # Firewall
            goto_menu(driver, security_tab, security_firewall_tab)
            time.sleep(1)
            check_medium_firewall = len(driver.find_elements_by_css_selector(ele_firewall_lv_medium)) == 0
            time.sleep(1)

            list_actual9 = [[check_wireless_ssid, check_wireless_pw],
                            check_enable_qos,
                            check_medium_firewall]
            list_expected9 = [[exp_ssid_2g_default_val, 'humax_'+get_config('GENERAL', 'serial_number')],
                              return_true,
                              return_true]
            step_9_name = "9. Verify state after restart: "
            list_check_in_step_9 = [
                "Wireless ssid and password is correct",
                "QOS is enable",
                "Condition 'Firewall is medium' is correct"
            ]
            check = assert_list(list_actual9, list_expected9)
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
            list_step_fail.append('9. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_R_59_MAIN_System_Extender_mode_Check_firmware_upgrade_when_disconnected_internet(self):
        self.key = 'MAIN_59'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        # save_config(config_path, 'URL', 'url', 'http://dearmyextender.net')
        # ===========================================================
        detect_firmware_version(driver)
        time.sleep(10)
        wait_ethernet_available()
        grand_login(driver)
        time.sleep(2)
        goto_menu(driver, network_tab, network_operationmode_tab)
        time.sleep(2)
        connect_repeater_mode(driver, force=True)
        # ===========================================================

        try:
            # URL_LOGIN = get_config('URL', 'url')
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            # Call API disconnect WAN
            URL_DISCONNECT_WAN = 'http://192.168.1.1' + '/api/v1/network/wan/0/disconnect'
            _METHOD = 'POST'
            _TOKEN = call_api_login(_USER, _PW, url='http://dearmyrouter.net')["accessToken"]
            _BODY = ''

            # res_data = call_api(URL_DISCONNECT_WAN, _METHOD, _BODY, _TOKEN)
            headers = {
                "content-type": "application/json",
                "content-language": "en",
                "access-token": _TOKEN
            }
            res_data = send_request(URL_DISCONNECT_WAN, _METHOD, headers, _BODY)
            time.sleep(300)
            list_actual0 = [res_data.status_code]
            list_expected0 = [200]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] Pre-condition: API Disconnect WAN Success. Check Status code. ')
        except:
            self.list_steps.append(
                f'[Fail] Pre-condition: Disconnect WAN Fail. Check Status code. ')
            list_step_fail.append('0. Assertion wong')

        try:
            time.sleep(20)
            wait_ethernet_available()
            grand_login(driver)
            time.sleep(1)

            # System > Firmware
            driver.find_element_by_css_selector(system_btn).click()
            time.sleep(0.2)
            driver.find_element_by_css_selector(ele_sys_firmware_update).click()
            time.sleep(1)

            # Check pop up firmware update display
            check_pop_firmware_display = driver.find_element_by_css_selector(ele_check_for_update_title).text

            list_actual1 = [check_pop_firmware_display]
            list_expected1 = ['Firmware Update']
            check = assert_list(list_actual1, list_expected1)
            step_1_name = "1. Login > System > Firmware. Check name of popup displayed. "
            list_check_in_step_1 = ["Popup name is: Firmware Update"]
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
            list_step_fail.append('1. Assertion wong')

        try:
            message = driver.find_element_by_css_selector(ele_firm_update_msg).text

            list_actual2 = [message]
            list_expected2 = ['Internet disconnected']
            step_2_name = "2. Check Message shown in pop up firmware update. "
            list_check_in_step_2 = [
                f"Message is: {list_expected2[0]}"
            ]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append(f'[Fail] 2. Check Message shown in pop up firmware update '
                                  f'Actual: {str(list_actual2)}. '
                                  f'Expected: {str(list_expected2)}')

        try:
            _USER = get_config('ACCOUNT', 'user')
            _PW = get_config('ACCOUNT', 'password')
            # Call API disconnect WAN
            URL_DISCONNECT_WAN = 'http://192.168.1.1' + '/api/v1/network/wan/0/disconnect'
            _METHOD = 'POST'
            _TOKEN = call_api_login(_USER, _PW, url='http://dearmyrouter.net')["accessToken"]
            _BODY = ''
            headers = {
                "content-type": "application/json",
                "content-language": "en",
                "access-token": _TOKEN
            }
            res_data = send_request(URL_DISCONNECT_WAN, _METHOD, headers, _BODY)
            time.sleep(300)
            list_actual0 = [res_data.status_code]
            list_expected0 = [200]
            check = assert_list(list_actual0, list_expected0)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'API Connect WAN Success After test. Check Status code. ')
        except:
            self.list_steps.append(
                f'Connect WAN Fail After test. Check Status code. ')

        self.assertListEqual(list_step_fail, [])

    def test_14_MAIN_Verify_the_time_out_operation(self):
        self.key = 'MAIN_14'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []
        try:
            grand_login(driver)
            self.list_steps.append('[Pass] Login successfully')
        except:
            self.list_steps.append('[Fail] Login fail')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            goto_menu(driver, network_tab, network_internet_tab)
            # Wait 20 mins
            sleep_time = 20 * 60
            time.sleep(sleep_time)
            time.sleep(1)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            wait_popup_disappear(driver, dialog_loading)
            msg_time_out = driver.find_elements_by_css_selector(content)
            if len(msg_time_out) > 0:
                msg_time_out_text = msg_time_out[0].text
                driver.find_element_by_css_selector(btn_ok).click()
                time.sleep(3)
            else:
                msg_time_out_text = 'No popup appear'
            # Click ok
            # Lg is display
            check_lg_page = len(driver.find_elements_by_css_selector(lg_page)) > 0
            list_actual1 = [msg_time_out_text, check_lg_page]
            list_expected1 = [exp_time_out_msg, return_true]
            step_1_name = "1. Time out: Check msg time out, Login page is displayed"
            list_check_in_step_1 = ["Login page is appear"]
            check = assert_list(list_actual1, list_expected1)
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
            list_step_fail.append('1. Assertion wong')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try:
            grand_login(driver)
            sleep_time = 20 * 60
            time.sleep(sleep_time)
            goto_menu(driver, wireless_tab, wireless_primarynetwork_tab)
            # Click cancel
            time.sleep(2)
            msg_time_out_pop = len(driver.find_elements_by_css_selector(content)) == 0
            list_actual2 = [msg_time_out_pop]
            list_expected2 = [return_true]
            step_2_name = "2. Wait in Home page: After 20 mins. Check popup time out do not appear. "
            list_check_in_step_2 = ["Popup time out not appear"]
            check = assert_list(list_actual2, list_expected2)
            self.assertTrue(check["result"])
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                generate_step_information(
                    step_name=step_2_name,
                    list_check_in_step=list_check_in_step_2,
                    list_actual=list_actual2,
                    list_expected=list_expected2
                )
            )
            self.list_steps.append('[END TC]')
            list_step_fail.append('2. Assertion wong')
        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
