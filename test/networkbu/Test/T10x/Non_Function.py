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
token = get_token(USER, PW)
URL_2g = get_config('URL', 'url') + '/api/v1/wifi/0/ssid/0'

URL_5g = 'http://192.168.1.1/api/v1/wifi/1/ssid/0'


PING_TIMES = 60


class NON_FUNCTION(unittest.TestCase):
    def setUp(self):
        try:
            os.system('echo. &echo ' + self._testMethodName)
            self.start_time = datetime.now()
            os.system(f'python {nw_interface_path} -i Ethernet -a enable')
            time.sleep(15)
            self.driver = webdriver.Chrome(driver_path)
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

    def test_02_Dynamic_Wired_Ping_Aging_INTERGRATION_WITH_05(self):
        self.key = 'NON_FUNCTION_02'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        NEW_PASSWORD = 'abc123'
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

        PING_ADDRESS = '8.8.8.8'
        # PING_TIMES = 43200
        PING_YOUTUBE = 'youtube.com'
        YOUTUBE_URL = 'https://www.youtube.com/watch?v=e6iGJIYUroo'
        try:
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)

            def thread_youtube():
                global count_interrupt, live_time
                count_interrupt = 0
                ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                if ping_result['packet_loss_rate'] != 100.0:
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

            list_actual1 = [ping_result['packet_loss_rate'] <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {ping_result["packet_loss_rate"]} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}'
                f'Loss rate {ping_result["packet_loss_rate"]}'
                f' on {str(PING_TIMES)} seconds.'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_03_Wireless_24GHz_Ping_Aging_INTERGRATION_WITH_06(self):
        self.key = 'NON_FUNCTION_03'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        PING_ADDRESS = '8.8.8.8'
        # PING_TIMES = 43200
        PING_YOUTUBE = 'youtube.com'
        YOUTUBE_URL = 'https://www.youtube.com/watch?v=e6iGJIYUroo'
        NEW_PASSWORD = 'abc123'
        filename = '1'
        commmand = 'factorycfg.sh -a'
        run_cmd(commmand, filename=filename)
        # Wait 5 mins for factory
        time.sleep(150)
        wait_DUT_activated(URL_LOGIN)
        wait_ping('192.168.1.1')

        filename_2 = 'account1.txt'
        commmand_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(commmand_2, filename_2)
        time.sleep(3)
        # Get account information from web server and write to config.txt
        user_pw = get_result_command_from_server(url_ip=URL_LOGIN, filename=filename_2)

        try:
            new_2g_wf_name = api_change_wifi_setting(URL_2g)
            time.sleep(10)
            write_data_to_xml(wifi_default_file_path, new_name=new_2g_wf_name)
            time.sleep(3)
            os.system(f'netsh wlan delete profile name="{new_2g_wf_name}"')
            # Connect Default 2GHz
            os.system(f'netsh wlan add profile filename="{wifi_default_file_path}"')
            time.sleep(5)

            os.system(f'netsh wlan connect ssid="{new_2g_wf_name}" name="{new_2g_wf_name}"')
            time.sleep(5)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
        except:
            self.list_steps.append('[FAIL] Precondition connect 2G Wifi Fail')

        try:
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)

            def thread_youtube():
                global count_interrupt, live_time
                count_interrupt = 0
                ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                if ping_result['packet_loss_rate'] != 100.0:
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

            list_actual1 = [ping_result['packet_loss_rate'] <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {str(ping_result["packet_loss_rate"])} on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate {str(ping_result["packet_loss_rate"])} on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_04_Wireless_5GHz_Ping_Aging_INTERGRATION_WITH_07(self):
        self.key = 'NON_FUNCTION_04'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        PING_ADDRESS = '8.8.8.8'
        # PING_TIMES = 43200
        PING_YOUTUBE = 'youtube.com'
        YOUTUBE_URL = 'https://www.youtube.com/watch?v=e6iGJIYUroo'
        NEW_PASSWORD = 'abc123'
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

        try:
            time.sleep(5)
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
            time.sleep(6)

            os.system(f'python {nw_interface_path} -i Ethernet -a disable')
            time.sleep(4)
        except:
            self.list_steps.append('[FAIL] Precondition connect 5G Wifi Fail')

        try:
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)

            def thread_youtube():
                global count_interrupt, live_time
                count_interrupt = 0
                ping_result = ping_to_address(PING_YOUTUBE, PING_TIMES=1)
                if ping_result['packet_loss_rate'] != 100.0:
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

            list_actual1 = [ping_result['packet_loss_rate'] <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_08_Static_Wired_Ping_Aging(self):
        self.key = 'NON_FUNCTION_08'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        PING_ADDRESS = '8.8.8.8'
        # PING_TIMES = 43200
        PING_YOUTUBE = 'youtube.com'
        YOUTUBE_URL = 'https://www.youtube.com/watch?v=e6iGJIYUroo'
        NEW_PASSWORD = 'abc123'
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
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)
            thread1 = threading.Thread(target=thread_ping)
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual1 = [ping_result['packet_loss_rate'] <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_09_Static_Wireless_24GHz_Ping_Aging(self):
        self.key = 'NON_FUNCTION_09'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        PING_ADDRESS = '8.8.8.8'
        # PING_TIMES = 43200
        PING_YOUTUBE = 'youtube.com'
        YOUTUBE_URL = 'https://www.youtube.com/watch?v=e6iGJIYUroo'
        NEW_PASSWORD = 'abc123'
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
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)
            thread1 = threading.Thread(target=thread_ping)
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual1 = [ping_result['packet_loss_rate'] <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])

    def test_10_Static_Wireless_5GHz_Ping_Aging(self):
        self.key = 'NON_FUNCTION_10'
        driver = self.driver
        self.def_name = get_func_name()
        list_step_fail = []
        self.list_steps = []

        URL_LOGIN = get_config('URL', 'url')
        PING_ADDRESS = '8.8.8.8'
        # PING_TIMES = 43200
        PING_YOUTUBE = 'youtube.com'
        YOUTUBE_URL = 'https://www.youtube.com/watch?v=e6iGJIYUroo'
        NEW_PASSWORD = 'abc123'
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
            def thread_ping():
                global ping_result
                ping_result = ping_to_address(PING_ADDRESS, PING_TIMES)

            thread1 = threading.Thread(target=thread_ping)
            thread1.start()

            c = 0
            while thread1.is_alive():
                print(str(thread1.is_alive()) + ' th1 - ' + str(c))
                time.sleep(1)
                c += 1

            time.sleep(2)

            list_actual1 = [ping_result['packet_loss_rate'] <= 1.0]
            list_expected1 = [return_true]
            check = assert_list(list_actual1, list_expected1)
            self.assertTrue(check["result"])
            self.list_steps.append(
                f'[Pass] 1, 2. Check Ping {PING_ADDRESS}; '
                f'Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds. '
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
        except:
            self.list_steps.append(
                f'[Fail] 1, 2. Check Ping {PING_ADDRESS}; Loss rate: {str(ping_result["packet_loss_rate"])} '
                f'on {str(PING_TIMES)} seconds'
                f'Actual: {str(list_actual1)}. '
                f'Expected: {str(list_expected1)}')
            self.list_steps.append('[END TC]')
            list_step_fail.append('1, 2. Assertion wong')

        self.assertListEqual(list_step_fail, [])


if __name__ == '__main__':
    unittest.main()
