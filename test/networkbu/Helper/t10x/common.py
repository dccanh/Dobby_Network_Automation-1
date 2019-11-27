#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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
from pywinauto.application import Application
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


def save_config(config_path, section, option, value):
    config = configparser.RawConfigParser()
    config.read(config_path)
    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())
    config.set(str(section).upper(), str(option), str(value))
    with open(config_path, 'w', encoding='utf-8') as config_file:
        config.write(config_file)


# save_config(config_path, 'PATH', 'crt_common_path', crt_common)
# save_config(config_path, 'PATH', 'crt_run_cmd_path', crt_run_command)


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


def next_available_row(sheet):
    str_list = list(filter(None, sheet.col_values(1)))  # fastest
    return str(len(str_list) + 1)


def write_ggsheet(key, list_steps, func_name, duration):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(gg_credential_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open("[DOB] Report Automation").get_worksheet(1)
    next_row = next_available_row(sheet)
    sheet.update_acell("A{}".format(next_row), key)
    sheet.update_acell("B{}".format(next_row), func_name)
    if '[Fail]' in str(list_steps):
        sheet.update_acell("C{}".format(next_row), 'FAIL')
    else:
        if '[END TC]' not in str(list_steps):
            sheet.update_acell("C{}".format(next_row), 'ERROR')
        else:
            sheet.update_acell("C{}".format(next_row), 'PASS')
    sheet.update_acell("D{}".format(next_row), duration)
    sheet.update_acell("E{}".format(next_row), str(list_steps))


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
    # time.sleep(5)

    # If login Fail. Get USER and PW again
    msg_error = driver.find_element_by_css_selector(lg_msg_error).text
    if msg_error != '':
        filename_2 = 'account.txt'
        command_2 = 'capitest get Device.Users.User.2. leaf'
        run_cmd(command_2, filename_2)
        time.sleep(3)
        get_result_command_from_server(url_ip=url_login, filename=filename_2)

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
        time.sleep(5)

    # Check Privacy Policy
    policy_popup = driver.find_elements_by_css_selector(lg_privacy_policy_pop)
    if len(policy_popup):
        ActionChains(driver).move_to_element(policy_popup[0]).click().send_keys(Keys.ARROW_DOWN).perform()
        driver.find_element_by_css_selector(btn_ok).click()
        time.sleep(3)


def get_url_ipconfig(ipconfig_field='Default Gateway'):
    cmd = 'ipconfig'
    write_cmd = subprocess.check_output(cmd, encoding='oem')
    split_result = [i.strip() for i in write_cmd.splitlines()]
    default_gw = [i for i in split_result if i.startswith(ipconfig_field)]
    url_ = 'http://'+[i.split(':')[1].strip() for i in default_gw if i.split(':')[1].strip().startswith('192.168.1')][0]
    save_config(config_path, 'URL', 'url', url_)


def goto_menu(driver, parent_tab, child_tab):
    ActionChains(driver).move_to_element(driver.find_element_by_css_selector(parent_tab)).perform()
    # driver.find_element_by_css_selector(parent_tab).click()
    time.sleep(0.5)
    driver.find_element_by_css_selector(child_tab).click()
    time.sleep(0.5)


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