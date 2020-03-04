#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
sys.path.append('../../')
import openpyxl
import time
import random
import subprocess
import datetime
import json
import requests
import gspread
import configparser
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from datetime import date
from faker import Faker
from Helper.t10x.config.read_config import *
from Helper.t10x.config.elements import *
from Helper.t10x.config.captcha import *
import base64
from oauth2client.service_account import ServiceAccountCredentials
from Helper.t10x.ls_path import *
from Helper.t10x.secure_crt.common import *
import re
import xml.etree.ElementTree as ET
from winreg import *
def save_config(config_path, section, option, value):
    config = configparser.RawConfigParser()
    config.read(config_path)
    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())
    config.set(str(section).upper(), str(option), str(value))
    with open(config_path, 'w', encoding='utf-8') as config_file:
        config.write(config_file)



def get_config(section, option):
    if not os.path.exists(config_path):
        print("The config file not exist. Exit!!!")
        return

    config = configparser.RawConfigParser()
    config.read(config_path)

    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

serial_num = get_config('GENERAL', 'serial_number')
save_config(config_path, 'ACCOUNT', 'default_pw', serial_num)


def next_available_row(sheet):
    str_list = list(filter(None, sheet.col_values(1)))  # fastest
    return str(len(str_list) + 1)


def write_ggsheet(key, list_steps, func_name, duration, time_stamp=0):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(gg_credential_path, scope)
    client = gspread.authorize(creds)
    # sheet = client.open("[DOB] Report Automation").get_worksheet(1)
    get_gg_sheet_name = get_config('REPORT', 'sheet_name')
    sheet = client.open("[DOB] Report Automation").worksheet(get_gg_sheet_name)
    next_row = next_available_row(sheet)
    sheet.update_acell("A{}".format(next_row), key)
    sheet.update_acell("B{}".format(next_row), func_name)
    if '[Fail]' in str(list_steps):
        sheet.update_acell("C{}".format(next_row), 'FAIL')
    else:
        # if '[END TC]' not in str(list_steps):
        if '[END TC]' not in list_steps:
            sheet.update_acell("C{}".format(next_row), 'ERROR')
        else:
            sheet.update_acell("C{}".format(next_row), 'PASS')
    sheet.update_acell("D{}".format(next_row), duration)
    sheet.update_acell("E{}".format(next_row), str(list_steps))
    sheet.update_acell("H{}".format(next_row), str(time_stamp))


def assert_list(list_actual_result, list_expected_result):
    actual_fail = []
    expected_fail = []
    for a, e in zip(list_actual_result, list_expected_result):
        if str(a) != str(e):
            actual_fail.append(str(a))
            expected_fail.append(str(e))
    if len(actual_fail) == 0 and len(expected_fail) == 0 and len(list_actual_result) == len(list_expected_result):
        return {"result": True, "actual": [], "expected": []}
    return {"result": False, "actual": list_actual_result, "expected": list_expected_result}


def get_func_name():
    import inspect
    return inspect.stack()[1][3]


def convert_type_number(num):
    if '.0' in str(num):
        return str(num).split('.0')[0]
    return str(num)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~REQUEST GENERAL  BLOCK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def wait_visible(driver, css_element):
    visible = driver.find_elements_by_css_selector(css_element)
    count = 0
    while len(visible) == 0:
        time.sleep(1)
        visible = driver.find_elements_by_css_selector(css_element)
        count += 1
        if count == 300:
            driver.quit()
            os.system("[Fail] Loaded time out.")
            return False
    else:
        return True


def wait_popup_disappear(driver, pop_up_element):
   visible = driver.find_elements_by_css_selector(pop_up_element)
   count =0
   while len(visible) != 0:
       time.sleep(1)
       visible = driver.find_elements_by_css_selector(pop_up_element)
       count += 1
       if count == 300:
           driver.quit()
           os.system("[Fail] Loaded time out.")
           return False
   else:
       return True


def random_list_drop_down_with_condition(driver, css_option_condition):
    project_options = driver.find_elements_by_css_selector(css_option_condition)
    choice = random.choice(project_options)
    ActionChains(driver).move_to_element(choice).perform()
    option_value = choice.text
    choice.click()
    return {"chosenValue": option_value}


def random_list_drop_down_regis_emp(driver, css_option_condition):
    project_options = driver.find_elements_by_css_selector(css_option_condition)
    if len(project_options):
        choice = random.choice(project_options)
        ActionChains(driver).move_to_element(choice).perform()
        option_value = choice.text
        choice.click()
        return {"chosenValue": option_value}
    else:
        return False


def read_column(driver, col):
    # col = name
    elem1 = driver.find_element_by_xpath("//span[contains(text(),'" + col + "')]/../../..")
    lst = driver.find_elements_by_xpath("//div[@class='ant-table-scroll']/div[1]/table/thead/tr/th")
    a = lst.index(elem1) + 1

    time.sleep(2)
    list_pages = driver.find_elements_by_xpath('//ul//li//a')
    data = []
    info_each_row = []
    if len(list_pages) != 0:
        num_pages = int(list_pages[-2].text)
        for num in range(1, num_pages + 1):
            num_rows = driver.find_elements_by_css_selector('.ant-table-scroll tr.ant-table-row-level-0')
            for row in range(0, len(num_rows)):
                if a > 2:
                    num_cells = driver.find_elements_by_css_selector(
                        "div.ant-table-scroll> * tr>td:nth-child(" + str(a) + ")")
                    time.sleep(0.01)
                    data.append(num_cells[row].text)
                else:
                    num_cells = driver.find_elements_by_css_selector(
                        ".ant-table-fixed-left tr>td:nth-child(" + str(a) + ")")
                    time.sleep(0.01)
                    data.append(num_cells[row].text)
            list_pages[-1].click()
            time.sleep(2)
    else:
        total_result = int(driver.find_element_by_css_selector('h3.text-primary.mb-0.mr-2').text.split(': ')[1])
        if total_result != 0:
            num_rows = driver.find_elements_by_css_selector('.ant-table-scroll tr.ant-table-row-level-0')
            for row in range(0, len(num_rows)):
                if a > 2:
                    num_cells = driver.find_elements_by_css_selector(
                        ".ant-table-scroll tr>td:nth-child(" + str(a) + ")")
                    ActionChains(driver).move_to_element(num_cells[row]).perform()
                    data.append(num_cells[row].text)
                else:
                    num_cells = driver.find_elements_by_css_selector(
                        ".ant-table-fixed-left tr>td:nth-child(" + str(a) + ")")
                    ActionChains(driver).move_to_element(num_cells[row]).perform()
                    data.append(num_cells[row].text)
        else:
            data = 'No data'
    return data


def scroll_to(driver, element):
    coordinates = element.location_once_scrolled_into_view  # returns dict of X, Y coordinates
    driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))


def get_result_command_from_server(url_ip, filename='1'):
    driver2 = webdriver.Chrome(driver_path)
    url_result = url_ip + '/' + filename
    time.sleep(1)
    driver2.get(url_result)
    time.sleep(2)
    get_all_text = driver2.find_element_by_css_selector('html>body>pre').text
    command_result = '{' + get_all_text.split('@@@ PRINT OBJLIST START @@@')[1].split(' @@@@@@ PRINT OBJLIST END @@@@@@')[0]
    fit_result = command_result.split('''   },\n  },\n }''')[0]+'}}}'

    info = json.loads(fit_result)
    username = info['Device.Users.User.2']['Username']['paramValue']
    password = info['Device.Users.User.2']['Password']['paramValue']

    save_config(config_path, 'ACCOUNT', 'user', username)
    save_config(config_path, 'ACCOUNT', 'password', password)
    driver2.quit()
    return {'userName': username, 'passWord': password}


def login(driver):
    url_login = get_config('URL', 'url')
    user_request = get_config('ACCOUNT', 'user')
    pass_word = get_config('ACCOUNT', 'password')

    time.sleep(1)
    driver.get(url_login)
    time.sleep(2)
    driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
    time.sleep(1)
    driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
    time.sleep(1)
    # Captcha
    captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
    captcha_text = get_captcha_string(captcha_src)
    driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
    time.sleep(1)
    driver.find_elements_by_css_selector(lg_btn_login)[-1].click()

    # If login Fail. Get USER and PW again
    msg_error = driver.find_element_by_css_selector(lg_msg_error).text
    if msg_error != '':
        filename_2 = 'account.txt'
        command_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(command_2, filename_2)
        time.sleep(3)
        get_result_command_from_server(url_ip=url_login, filename=filename_2)

        user_request = get_config('ACCOUNT', 'user')
        pass_word = get_config('ACCOUNT', 'default_pw')

        time.sleep(1)
        driver.get(url_login)
        time.sleep(2)
        driver.find_elements_by_css_selector(lg_user)[-1].send_keys(user_request)
        time.sleep(1)
        driver.find_elements_by_css_selector(lg_password)[-1].send_keys(pass_word)
        time.sleep(1)
        # Captcha
        captcha_src = driver.find_element_by_css_selector(lg_captcha_src).get_attribute('src')
        captcha_text = get_captcha_string(captcha_src)
        driver.find_element_by_css_selector(lg_captcha_box).send_keys(captcha_text)
        time.sleep(1)
        driver.find_elements_by_css_selector(lg_btn_login)[-1].click()
        time.sleep(5)
    wait_popup_disappear(driver, dialog_loading)
    time.sleep(1)
    # Check Privacy Policy
    time.sleep(2)
    policy_popup = driver.find_elements_by_css_selector(lg_privacy_policy_pop)
    if len(policy_popup):
        ActionChains(driver).move_to_element(policy_popup[0]).click().send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1)
        driver.find_element_by_css_selector(btn_ok).click()
        time.sleep(3)


def grand_login(driver):
    login(driver)
    wait_popup_disappear(driver, dialog_loading)
    time.sleep(1)
    # Goto Homepage
    if len(driver.find_elements_by_css_selector(lg_welcome_header)) != 0:
        handle_winzard_welcome(driver)
        wait_popup_disappear(driver, dialog_loading)
    time.sleep(3)
    check_ota_auto_update(driver)
    time.sleep(1)


def get_url_ipconfig(ipconfig_field='Default Gateway'):
    cmd = 'ipconfig'
    write_cmd = subprocess.check_output(cmd, encoding='oem')
    split_result = [i.strip() for i in write_cmd.splitlines()]
    default_gw = [i for i in split_result if i.startswith(ipconfig_field)]
    url_ = 'http://'+[i.split(':')[1].strip() for i in default_gw if i.split(':')[1].strip().startswith('192.168.1')][0]
    save_config(config_path, 'URL', 'url', url_)


def goto_menu(driver, parent_tab, child_tab):
    ActionChains(driver).move_to_element(driver.find_element_by_css_selector(parent_tab)).click().perform()
    time.sleep(1)
    if child_tab != 0:
        driver.find_element_by_css_selector(child_tab).click()
        time.sleep(0.5)


def detect_current_menu(driver):
    # Detect current active tab in T10x
    main_tab = driver.find_element_by_css_selector('#parent-menu>a.active.open').text

    child_tab = driver.find_elements_by_css_selector('#sub-menu>.active')
    if not len(child_tab):
        child_tab = 0
    else:
        child_tab = child_tab[0].text
    return main_tab, child_tab


def base64encode(user, pw):
    import hashlib, binascii, base64
    salt = base64.b64encode(('hmx#cpe@pbkdf2*SALT!' + user).encode('utf-8'))

    # salt = binascii.hexlify(hash0_pw)
    if salt is not None:
        mode = 'sha512'
        iterations = 1000
        dklen = 64

        hash0_pw = hashlib.pbkdf2_hmac(mode, pw.encode('utf-8'), salt, iterations, dklen)
        # hash1_pw = binascii.hexlify(hash0_pw)
        hash1_pw = base64.b64encode(hash0_pw)

        hash2_pw = hash1_pw.decode('utf-8')
        initial_data = 'HS:' + user + ':' + hash2_pw
        byte_string = initial_data.encode('utf-8')
        encoded_data = base64.b64encode(byte_string)
        return encoded_data.decode('ascii')
    else:
        initial_data = 'HS:' + user + ':' + pw
        byte_string = initial_data.encode('utf-8')
        encoded_data = base64.b64encode(byte_string)

        return encoded_data.decode('ascii')

def base64encodev2(user, pw):
    import hashlib, binascii, base64

    initial_data = 'HS:' + user + ':' + pw
    byte_string = initial_data.encode('utf-8')
    encoded_data = base64.b64encode(byte_string)

    return encoded_data.decode('ascii')

def send_request(url, method, headers, body, timeout=120):
    result = requests.models.Response()
    try:
        if method.upper() == 'GET':
            result = requests.get(url=url, headers=headers, json=body, timeout=timeout)
        elif method.upper() == 'POST':
            result = requests.post(url=url, headers=headers, json=body, timeout=timeout)
        elif method.upper() == 'PUT':
            result = requests.put(url=url, headers=headers, json=body, timeout=timeout)
        elif method.upper() == 'DELETE':
            result = requests.put(url=url, headers=headers, json=body, timeout=timeout)
    except Exception:
        result.status_code = 404
    return result


def call_api_login(user, pw):
    """Method: POST; Require: user, pw; Return: JSON data"""
    url = get_config('URL', 'url')
    url_login = url + "/api/v1/gateway/users/login"
    data = {
        "userName": user,
        "password": base64encode(user, pw)
    }
    res = requests.post(url=url_login, json=data)

    if res.status_code != 200:

        user = get_config('ACCOUNT', 'user')
        pw = get_config('ACCOUNT', 'default_pw')
        data = {
            "userName": user,
            "password": base64encode(user, pw)
        }
        res = requests.post(url=url_login, json=data)
        if res.status_code == 200:
            save_config(config_path, 'ACCOUNT', 'password', pw)

    json_data = json.loads(res.text)
    return json_data


def get_token(user, pw):
    token = call_api_login(user, pw)["accessToken"]
    return token


def call_api(url, method, body, token):

    headers = {
        "content-type": "application/json",
        "content-language": "en",
        "access-token": token
    }
    res_data = send_request(url, method, headers, body)
    if res_data.status_code != 404:
        data = json.loads(res_data.text)
    else:
        data = {"body": "404", "statusCode": 404}
    return data


def check_page_exist(url):
    # api_url = ipv4 + "/index.html"
    try:
        res = requests.get(url=url, timeout=1)
        if (res.status_code == 200):
            return True
    except Exception:
        return False


def wait_DUT_activated(url):
    count = 0
    url = url + "/index.html"
    while True:
        count += 1

        print(url)
        if check_page_exist(url):
            return True
        else:
            print("          WAITING FOR THE DEVICE ACTIVED... | RE-TRY TIMES: " + str(count))
            time.sleep(1)
            if (count % 180 == 0):
                return False


def ping_to_url(url):
    TIME_OUT = 'time out'
    result = subprocess.check_output('ping ' + url)
    if TIME_OUT not in result.decode('utf8'):
        # Check there is no time out in pinged result > Successfully
        return True
    return False


def wait_ping(url):
    TIME_OUT = 'Request time out'
    count = 0
    while True:
        result = subprocess.check_output('ping ' + url)
        time.sleep(1)
        count += 1
        if TIME_OUT not in result.decode('utf8'):
            break
        else:
            if count == 300:
                print('Wait more than 300s')
                break


def scan_wifi(wifi_name=None):
    cmd = 'netsh wlan show networks'
    write_cmd = subprocess.check_output(cmd, encoding='oem')
    ls_header = [i for i in write_cmd.splitlines() if i.startswith('SSID')]
    ls_wifi_name = [i.split(': ')[1] for i in ls_header]
    if wifi_name is not None:
        while True:
            write_cmd = subprocess.check_output(cmd, encoding='oem')
            ls_header = [i for i in write_cmd.splitlines() if i.startswith('SSID')]
            ls_wifi_name = [i.split(': ')[1] for i in ls_header]
            if wifi_name in ls_wifi_name:
                return True
            else:
                time.sleep(1)

    return ls_wifi_name


def change_nw_profile(wifi_xml_path, field, value):
    """
    :param wifi_xml_path: wifi_2g_path or wifi_5g_path
    :param field: Fields name: SSID, Security or Password
    :param value: Value of field
    :return: overwrite wifi_xml_path new value
    """
    value = value.replace('&', '&amp;')
    value = value.replace('>', '&gt;')
    value = value.replace('<', '&lt;')
    trans_dict = {"Ssid": "name",
                  "Security": "authentication",
                  "Encryption": "encryption",
                  "Password": "keyMaterial"}
    temp_path = config_dir + '\\temp.txt'

    os.rename(wifi_xml_path, temp_path)
    time.sleep(1)
    with open(temp_path) as f:
        data = f.read()
        rows = [i.strip() for i in data.splitlines() if i.strip().startswith('<' + trans_dict[field] + '>')]
        # old = a[0].split('<' + trans_dict[field] + '>')[1].split('</' + trans_dict[field] + '>')[0]
        for r in rows:
            old = r.split('<' + trans_dict[field] + '>')[1].split('</' + trans_dict[field] + '>')[0]
            data = data.replace(old, value)
        # b = data.replace(old, value)
        f.close()
    with open(temp_path, 'w') as f:
        f.write(data)
        f.close()
    os.rename(temp_path, wifi_xml_path)


def connect_wifi_from_xml(wifi_xml_path):
    temp_path = config_dir + '\\temp.txt'
    os.rename(wifi_xml_path, temp_path)
    with open(temp_path) as f:
        data = f.read()
        name = [i.strip() for i in data.splitlines() if i.strip().startswith('<name>')]
        _name = name[0].split('<name>')[1].split('</name>')[0]
        f.close()
    os.rename(temp_path, wifi_xml_path)

    # Add network profile
    cmd_add_profile = 'netsh wlan add profile filename="'+wifi_xml_path+'"'
    print(cmd_add_profile)
    os.system(cmd_add_profile)
    time.sleep(2)
    # Connect that name
    cmd_connect = 'netsh wlan connect ssid="'+_name+'" name="'+_name+'"'
    print(cmd_connect)
    os.system(cmd_connect)


def setting_wireless_security(block_left_right, secur_type=None, encryption=None, key_type=None):
    # block_ = driver.find_element_by_css_selector(block_element)

    security_ = block_left_right.find_element_by_css_selector(secure_value_field)
    security_.click()
    ls_security_ = security_.find_elements_by_css_selector(secure_value_in_drop_down)
    time.sleep(0.5)
    for o in ls_security_:
        if o.get_attribute('option-value') == secur_type:
            o.click()
            break

    if encryption is not None:
        encryption_ = block_left_right.find_element_by_css_selector(encryption_value_field)
        encryption_.click()
        ls_encryption_ = encryption_.find_elements_by_css_selector(secure_value_in_drop_down)
        time.sleep(0.5)
        for o in ls_encryption_:
            if o.get_attribute('option-value') == encryption:
                o.click()
                break

    if key_type is not None:
        key_type_ = block_left_right.find_element_by_css_selector(encryption_value_field)
        key_type_.click()
        ls_key_type_ = key_type_.find_elements_by_css_selector(secure_value_in_drop_down)
        time.sleep(0.5)
        for o in ls_key_type_:
            if o.get_attribute('option-value') == key_type:
                o.click()
                break


def apply_process(driver, block_left_right):
    time.sleep(0.2)
    block_left_right.find_element_by_css_selector(apply).click()
    time.sleep(1)
    wait_popup_disappear(driver, dialog_loading)
    driver.find_element_by_css_selector(btn_ok).click()
    wait_popup_disappear(driver, dialog_loading)
    time.sleep(2)


def checkMACAddress(x):
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", x.lower()):
        return True
    return False


def checkIPAddress(x):
    if re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", x):
        return True
    return False


def handle_winzard_welcome(driver, NEW_PASSWORD='abc123', exp_language='English'):
    exp_time_zone = '(GMT+07:00) Bangkok, Ho Chi Minh, Phnom Penh, Vientiane'
    # Click to Language
    driver.find_element_by_css_selector(welcome_language).click()
    time.sleep(3)

    # Choose Language
    ls_time_zone = driver.find_elements_by_css_selector(welcome_list_language)
    for t in ls_time_zone:
        ActionChains(driver).move_to_element(t).perform()
        if t.text == exp_language:
            t.click()
            break
    time.sleep(3)
    # Click to time zone
    driver.find_element_by_css_selector(welcome_time_zone).click()
    time.sleep(3)

    # Choose time zone in drop down: Vn zone GMT +7
    ls_time_zone = driver.find_elements_by_css_selector(welcome_list_time_zone)
    for t in ls_time_zone:
        ActionChains(driver).move_to_element(t).perform()
        if t.text == exp_time_zone:
            t.click()
            break

    time.sleep(3)
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

    while True:
        time.sleep(2)
        wait_visible(driver, welcome_next_btn)
        next_btn = driver.find_element_by_css_selector(welcome_next_btn)
        if not next_btn.get_property('disabled'):
            next_btn.click()
        time.sleep(5)

        if len(driver.find_elements_by_css_selector(welcome_let_go_btn)) > 0:
            break


    # # Next Operation Mode
    # time.sleep(3)
    # wait_visible(driver, welcome_next_btn)
    # next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    # if not next_btn.get_property('disabled'):
    #     next_btn.click()
    #     time.sleep(0.5)
    # time.sleep(3)
    #
    # # Next Internet Setup 1
    # time.sleep(2)
    # wait_visible(driver, welcome_next_btn)
    # next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    # if not next_btn.get_property('disabled'):
    #     next_btn.click()
    #
    # # Next Internet setup 2
    # time.sleep(3)
    # wait_visible(driver, welcome_next_btn)
    # next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    # if not next_btn.get_property('disabled'):
    #     next_btn.click()
    #
    # # Next Wireless Setup
    # time.sleep(3)
    # wait_visible(driver, welcome_next_btn)
    # next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    # if not next_btn.get_property('disabled'):
    #     next_btn.click()
    #
    # # Next Humax Wifi App
    # time.sleep(3)
    # wait_visible(driver, welcome_next_btn)
    # next_btn = driver.find_element_by_css_selector(welcome_next_btn)
    # if not next_btn.get_property('disabled'):
    #     next_btn.click()
    # time.sleep(3)

    # Click Let's Go
    time.sleep(3)
    driver.find_element_by_css_selector(welcome_let_go_btn).click()
    # Write config
    save_config(config_path, 'ACCOUNT', 'password', NEW_PASSWORD)
    wait_popup_disappear(driver, dialog_loading)
    time.sleep(2)
    wait_visible(driver, home_view_wrap)
    time.sleep(5)


def ping_to_address(PING_ADDRESS, PING_TIMES=4):
    import pingparsing
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = PING_ADDRESS
    transmitter.count = PING_TIMES
    result = transmitter.ping()
    json_str = json.dumps(ping_parser.parse(result).as_dict(), indent=4)
    str_to_json = json.loads(json_str)
    return str_to_json


def network_interface_action(interface='Ethernet', action='enable'):
    # Interface option Wi-Fi / Ethernet
    # Action: enabled/disabled
    import ctypes

    print("interface: " + interface + " | action: " + action)

    cmd = f'netsh interface set interface name="{interface}" admin={action}'

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        # Code of your program here
        subprocess.call(cmd, shell=True)
    else:
        # Re-run the program with admin rights
        parameters = ""
        for i in range(1, len(sys.argv)):
            parameters = parameters + " \"" + str(sys.argv[i]) + "\""
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__ + parameters, None, 1)


def api_change_wifi_setting(url_change, new_wifi_name='', get_only_mac=False, ):

    user = get_config('ACCOUNT', 'user')
    pw = get_config('ACCOUNT', 'password')
    token = get_token(user, pw)

    get_mac = call_api(url_change, 'GET', body='', token=token)['macAddress']
    if get_only_mac:
        return get_mac
    else:
        if new_wifi_name == '':
            new_wifi_name = '_'.join(['wifi', get_mac.replace(':', '_')])
        data = {
            "active": True,
            "name": new_wifi_name,
            "macAddress": get_mac,
            "hiddenSSID": False,
            "APIsolate": False,
            "webUIAccess": True,
            "internetOnly": False,
            "accessControl": False,
            "security": {
                "type": "WPA2/WPA-PSK",
                "personal": {
                    "password": "SFM6YWRtaW46aHVtYXhfMDAwMQ==",
                    "encryption": "AES/TKIP",
                    "groupKey": 3600
                },
                "enterprise": None,
                "wep": None
            },
            "index": 0
        }
        call_api(url_change, 'PUT', body=data, token=token)
        return new_wifi_name


def write_data_to_xml(xml_path, new_name='',
                      new_pw='humax_'+get_config('GENERAL', 'serial_number'),
                      new_secure='',
                      new_encryption='',
                      new_key_type=''):
    with open(xml_path) as wf:
        data = wf.read()
        if new_name != '':
            rows_name = [i.strip() for i in data.splitlines() if i.strip().startswith('<name>')]
            for r in rows_name:
                old = r.split('<name>')[1].split('</name>')[0]
                data = data.replace(old, new_name)

            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<hex>')][0]
            old = rows_hex.split('<hex>')[1].split('</hex>')[0]
            data = data.replace(old, new_name.encode('utf-8').hex())

        if new_pw != '':
            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<keyMaterial>')][0]
            old = rows_hex.split('<keyMaterial>')[1].split('</keyMaterial>')[0]
            data = data.replace(old, new_pw)

        if new_secure != '':
            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<authentication>')][0]
            old = rows_hex.split('<authentication>')[1].split('</authentication>')[0]
            data = data.replace(old, new_secure)

        if new_encryption != '':
            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<encryption>')][0]
            old = rows_hex.split('<encryption>')[1].split('</encryption>')[0]
            data = data.replace(old, new_encryption)

        if new_key_type != '':
            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<keyType>')][0]
            old = rows_hex.split('<keyType>')[1].split('</keyType>')[0]
            data = data.replace(old, new_key_type)

        wf.close()

    with open(xml_path, 'w') as f:
        f.write(data)
        f.close()


def write_data_to_none_secure_xml(xml_path, new_name='',
                      new_secure='',
                      new_encryption=''):
    with open(xml_path) as wf:
        data = wf.read()
        if new_name != '':
            rows_name = [i.strip() for i in data.splitlines() if i.strip().startswith('<name>')]
            for r in rows_name:
                old = r.split('<name>')[1].split('</name>')[0]
                data = data.replace(old, new_name)

            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<hex>')][0]
            old = rows_hex.split('<hex>')[1].split('</hex>')[0]
            data = data.replace(old, new_name.encode('utf-8').hex())

        if new_secure != '':
            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<authentication>')][0]
            old = rows_hex.split('<authentication>')[1].split('</authentication>')[0]
            data = data.replace(old, new_secure)

        if new_encryption != '':
            rows_hex = [i.strip() for i in data.splitlines() if i.strip().startswith('<encryption>')][0]
            old = rows_hex.split('<encryption>')[1].split('</encryption>')[0]
            data = data.replace(old, new_encryption)
        wf.close()

    with open(xml_path, 'w') as f:
        f.write(data)
        f.close()


def download_destination_path():
    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

    return Downloads


def change_pw(driver, pw):
    current_pw = get_config('ACCOUNT', 'password')
    ls_pw_box = driver.find_elements_by_css_selector(' '.join([dialog_content, password_input_cls]))
    # Current pw
    ActionChains(driver).move_to_element(ls_pw_box[0]).click().send_keys(current_pw).perform()
    time.sleep(0.2)
    # New pw
    ActionChains(driver).move_to_element(ls_pw_box[1]).click().send_keys(pw).perform()
    time.sleep(0.2)
    # Retype new pw
    ActionChains(driver).move_to_element(ls_pw_box[2]).click().send_keys(pw).perform()
    time.sleep(0.2)
    # CLick to other place
    driver.find_element_by_css_selector(apply).click()
    time.sleep(0.2)
    wait_popup_disappear(driver, dialog_loading)
    time.sleep(1)


def check_ota_auto_update(driver):
    if len(driver.find_elements_by_css_selector(ele_upgrade_server_popup)) > 0:
        driver.find_element_by_css_selector(btn_cancel).click()
        time.sleep(1)
        # turn Off OTA
        # Actions Systems > Backup
        system_button = driver.find_element_by_css_selector(system_btn)
        ActionChains(driver).move_to_element(system_button).click().perform()
        time.sleep(0.5)
        driver.find_element_by_css_selector(ele_sys_firmware_update).click()
        time.sleep(0.5)
        # Click disable auto update
        driver.find_element_by_css_selector('.dialog-content .toggle-button').click()
        wait_popup_disappear(driver, dialog_loading)
        driver.find_element_by_css_selector(ele_close_button).click()
        time.sleep(1)


def wireless_get_default_ssid(driver, label_name):
    edit_2g_label = driver.find_elements_by_css_selector(label_name_in_2g)
    edit_2g_fields = driver.find_elements_by_css_selector(wrap_input)
    for l, f in zip(edit_2g_label, edit_2g_fields):
        # Connection type
        if l.text == label_name:
            default_ssid_2g_value = f.find_element_by_css_selector(input).get_attribute('value')
            return default_ssid_2g_value


def wireless_check_pw_eye(driver, block, change_pw=False, new_pw='00000000'):
    if not change_pw:
        pw_eye = block.find_element_by_css_selector(password_eye)
        act = ActionChains(driver)
        act.click_and_hold(pw_eye)
        pw_default = block.find_element_by_css_selector(input_pw).get_attribute('value')
        act.release(pw_eye)
        act.perform()
        return pw_default
    else:
        # Change password
        pw_place = block.find_element_by_css_selector(input_pw)
        ActionChains(driver).move_to_element(pw_place).click().key_down(Keys.CONTROL).send_keys('a').key_up(
            Keys.CONTROL).send_keys(new_pw).perform()
        return new_pw


def wireless_change_choose_option(driver, element_option, VALUE_OPTION):
    # Ap dung cho:
    # Security
    # Encryption
    # Key Type
    action_wl = driver.find_element_by_css_selector(element_option)
    action_wl.click()
    ls_options = action_wl.find_elements_by_css_selector(secure_value_in_drop_down)
    time.sleep(0.5)
    for o in ls_options:
        if o.get_attribute('option-value') == VALUE_OPTION:
            o.click()
            break