import os
import sys

sys.path.append('../../../')
import json
import time
import unittest
import datetime
import requests
import configparser
import Helper.Helper_common
from path import root_dir
from Helper.Helper_common import tag
from requests.exceptions import ReadTimeout

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ifconfig_path = os.path.join(root_dir, "Config", 'ifconfig.txt')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config = configparser.ConfigParser()
config.read_file(open(ifconfig_path, 'r'))
ipv4 = 'http://' + config.get("IFCONFIG", 'ipv4')
user = config.get("USER_INFO", 'user')
pw = config.get("USER_INFO", 'pw')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pw_hash_encode = Helper.Helper_common.base64encode(user, pw)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

with open('expected_api') as f:
    exp_data = json.load(f)
final_api_report = 'final_api_report_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '-') + '.xlsx'
final_api_report = os.path.join(root_dir, "Report", "WEB_API", final_api_report)
Helper.Helper_common.reset_report_api_result(final_api_report)


class Gateway(unittest.TestCase):
    def setUp(self):
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'skip_setup' in tags:
            return
        else:
            self.token = Helper.Helper_common.call_api_login(user, pw)[0]["accessToken"]

    def tearDown(self):
        Helper.Helper_common.report_excel_api(self.list_step, self.def_name, final_api_report)

    def test_BE_GW_01(self):
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/gateway/users/login'
        data = {
            'userName': user,
            'password': pw_hash_encode
        }
        res = requests.post(url, json=data)
        self.assertEqual(200, res.status_code)
        api = json.loads(res.text)
        actual = [api['role'],
                  api['expireIn'],
                  api['system']['timer']['session']]
        expected = ['technician', 3600, 10]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append('[Pass] Values return wrong. \nActual: %s. \nExpected: %s.' % (
                str(actual), str(expected)))
        except AssertionError:
            self.list_step.append('[Fail] Values return wrong. \nActual: %s. \nExpected: %s.' % (
                str(actual), str(expected)))
            list_step_fail.append('Values return wrong. \nActual: %s. \nExpected: %s.' % (
                str(actual), str(expected)))
        self.token = api['accessToken']
        try:
            self.assertIsNotNone(self.token)
            self.list_step.append('[Pass] Value of Access Token is None. \nActual: %s' % (str(self.token)))
        except AssertionError:
            self.list_step.append('[Fail] Value of Access Token is None. \nActual: %s' % (str(self.token)))
            list_step_fail.append('Value of Access Token is None. \nActual: %s.' % (str(actual)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_01] Assertion fail')

    def test_BE_GW_02(self):
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login

        url_about = ipv4 + '/api/v1/gateway/about'
        res_about = Helper.Helper_common.call_get_api_token(url_about, self.token)

        url_connectivity = ipv4 + '/api/v1/gateway/connectivity'
        res_connectivity = Helper.Helper_common.call_get_api_token(url_connectivity, self.token)

        url_devices = ipv4 + '/api/v1/gateway/devices'
        res_devices = Helper.Helper_common.call_get_api_token(url_devices, self.token)

        actual = [res_about[1], res_connectivity[1], res_devices[1]]
        expected = [200, 200, 200]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '[Pass] Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '[Fail] Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append('Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_02] Assertion fail')

    def test_BE_GW_03(self):
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/gateway/about'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0].keys(), res[0]['software'].keys(), res[0]['hardware'].keys()]
        dict_about = exp_data['gateway/about']
        expected = [dict_about.keys(), dict_about['software'].keys(), dict_about['hardware'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        actual = list(res[0].values()) + list(res[0]['software'].values()) + list(res[0]['hardware'].values())
        check_actual = True
        for i in actual:
            if i is None:
                check_actual = False
        try:
            self.assertTrue(check_actual)
            self.list_step.append(
                '\n[Pass] 2.3 Assert values of API is not None: \nActual: %s.' % (str(actual)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.3 Assert values of API is not None: \nActual: %s.' % (str(actual)))
            list_step_fail.append(
                '2.3 Assert values of API is not None: \nActual: %s.' % (str(actual)))
        self.assertListEqual(list_step_fail, [], '[BE_GW_03] Assertion fail')

    def test_BE_GW_04(self):
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/gateway/connectivity'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0].keys(),
                  res[0]['wan'].keys(),
                  res[0]['lan'].keys(),
                  res[0]['wifi'][0].keys(),
                  res[0]['wifi'][1].keys(),
                  res[0]['usb'].keys()]
        dict_connectivity = exp_data['gateway/connectivity']
        expected = [dict_connectivity.keys(),
                    dict_connectivity['wan'].keys(),
                    dict_connectivity['lan'].keys(),
                    dict_connectivity['wifi'][0].keys(),
                    dict_connectivity['wifi'][1].keys(),
                    dict_connectivity['usb'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_04] Assertion fail')

    def test_BE_GW_05(self):
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/gateway/devices'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0][0].keys()]
        dict_devices = exp_data['gateway/devices']
        expected = [dict_devices.keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_05] Assertion fail')

    def test_BE_GW_06(self):
        """Login API using POST method with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # About
        url_about = ipv4 + '/api/v1/gateway/about'
        res = Helper.Helper_common.call_get_api_token(url_about, self.token)

        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0].keys(), res[0]['software'].keys(), res[0]['hardware'].keys()]
        dict_about = exp_data['gateway/about']
        expected = [dict_about.keys(), dict_about['software'].keys(), dict_about['hardware'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Logout
        res = Helper.Helper_common.call_api_logout(self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200 of API Logout: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        try:
            self.assertDictEqual(res[0], {})
            self.list_step.append(
                '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api About again using old token
        res = Helper.Helper_common.call_get_api_token(url_about, self.token)

        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code of About after Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code of About after Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code of About after Logout: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0].keys(), res[0]['error'].keys()]
        dict_about = exp_data['invalid_token']
        expected = [dict_about.keys(), dict_about['error'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert keys error of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert keys error of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert keys error of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        actual = [res[0]['error']['code'], res[0]['error']['type'], res[0]['error']['message']]
        expected = [dict_about['error']['code'], dict_about['error']['type'], dict_about['error']['message']]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.3 Assert value error of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.3 Assert value error of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '4.3 Assert value error of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_06] Assertion fail')

    @tag('skip_setup')
    def test_BE_GW_07(self):
        """Login API using POST method with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + "/api/v1/gateway/users/login"
        # Login 1: User/Password are null
        data1 = {
            "userName": "",
            "password": ""
        }
        login1 = Helper.Helper_common.call_api_login_extend(url, data1)
        try:
            self.assertEqual(login1[1], 401)
            self.list_step.append(
                '[Pass] 1.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (
                    str(login1[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 1.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (
                    str(login1[1]), str(401)))
            list_step_fail.append(
                '1.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (str(login1[1]), str(401)))
        actual = login1[0]
        expected = exp_data['invalid_user_password']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 1.2 Assert dict error of Invalid User Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 1.2 Assert dict error of Invalid User Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '1.2 Assert dict error of Invalid User Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))

        # Login 2: Password null
        data2 = {
            "userName": user,
            "password": ""
        }
        login1 = Helper.Helper_common.call_api_login_extend(url, data2)
        try:
            self.assertEqual(login1[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (
                    str(login1[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (
                    str(login1[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (str(login1[1]), str(401)))
        actual = login1[0]
        expected = exp_data['invalid_password']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict error of Invalid Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict error of Invalid Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict error of Invalid Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))

        # Login 3: User null
        pw3 = Helper.Helper_common.base64encode("", pw)
        data3 = {
            "userName": "",
            "password": pw3
        }
        login1 = Helper.Helper_common.call_api_login_extend(url, data3)
        try:
            self.assertEqual(login1[1], 401)
            self.list_step.append(
                '[Pass] 3.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (
                    str(login1[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (
                    str(login1[1]), str(401)))
            list_step_fail.append(
                '3.1 Assert status code Unauthorized: \nActual: %s. \nExpected: %s.' % (str(login1[1]), str(401)))
        actual = login1[0]
        expected = exp_data['invalid_password']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 3.2 Assert dict error of Invalid Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 3.2 Assert dict error of Invalid Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '3.2 Assert dict error of Invalid Password: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        self.assertListEqual(list_step_fail, [], '[BE_GW_07] Assertion fail')

    def test_BE_GW_08(self):
        """Login API using POST method with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # About
        url_about = ipv4 + '/api/v1/gateway/about'
        res = Helper.Helper_common.call_get_api_token(url_about, self.token)

        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0].keys(), res[0]['software'].keys(), res[0]['hardware'].keys()]
        dict_about = exp_data['gateway/about']
        expected = [dict_about.keys(), dict_about['software'].keys(), dict_about['hardware'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 3. Logout with wrong token
        res = Helper.Helper_common.call_api_logout('c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af')
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '3.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 4 Call api About again using valid token
        res = Helper.Helper_common.call_get_api_token(url_about, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code of About: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code of About: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code of About: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        actual = [res[0].keys(), res[0]['software'].keys(), res[0]['hardware'].keys()]
        dict_about = exp_data['gateway/about']
        expected = [dict_about.keys(), dict_about['software'].keys(), dict_about['hardware'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 242 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5 Logout with empty token

        header = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        url_logout = ipv4 + "/api/v1/gateway/users/logout"
        try:
            res = Helper.Helper_common.call_post_api_extend(url_req=url_logout, headers=header)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 5.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 5.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '5.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("5. [Fail] Timeout with empty token")

        # 6. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.call_post_api_extend(url_req=url_logout, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 7. Logout with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_api_logout(token=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '7.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 7.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 7.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '7.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 8. Logout with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_api_logout(token=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 8.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 8.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '8.1 Assert status code is 401 of API Logout: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 8.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 8.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '8.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_08] Assertion fail')

    def test_BE_GW_09(self):
        """Backup API using Post method"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Backup
        url_backup = ipv4 + '/api/v1/gateway/backup'
        res = Helper.Helper_common.call_post_api(url_backup, self.token)

        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = res[0]
        expected = exp_data['backup']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        url = ipv4 + res[0]['path']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": self.token
        }
        res = requests.get(url, headers=headers)
        actual = res.status_code
        try:
            self.assertEqual(actual, 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(actual), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(actual), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(actual), str(200)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_09] Assertion fail')

    def test_BE_GW_10(self):
        """Backup API using POST method with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Backup with wrong token
        url = ipv4 + '/api/v1/gateway/backup'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_post_api(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Logout with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_api_logout(token=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Logout with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_api_logout(token=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_10] Assertion fail')

    def test_BE_GW_11(self):
        """Factory reset API using POST method"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Backup with wrong token
        url = ipv4 + '/api/v1/gateway/factoryReset'
        try:
            res = Helper.Helper_common.call_post_api(url, self.token)
            try:
                self.assertEqual(res[1], 200)
                self.list_step.append(
                    '[Pass] 2.1 Assert status code is 200 of API FactoryReset: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(200)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 2.1 Assert status code is 200 of API FactoryReset: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(200)))
                list_step_fail.append(
                    '2.1 Assert status code is 200 of API FactoryReset: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            actual = res[0]
            expected = exp_data['factoryReset']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
                list_step_fail.append(
                    '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append('[Fail] Call FactoryReset timeout')
        self.assertListEqual(list_step_fail, [], '[BE_GW_11] Assertion fail')

    def test_BE_GW_12(self):
        """Factory reset API using POST method with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # FactoryReset with wrong token
        url = ipv4 + '/api/v1/gateway/factoryReset'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_post_api(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Call API with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_post_api(url, token=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Call API with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_post_api(url, token=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_12] Assertion fail')

    def test_BE_GW_13(self):
        """Change password API using POST method"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + "/api/v1/gateway/users/web/change"
        new_pw = "12345678"
        # new_pw = "942CB34F9761"
        body = {
            "userName": user,
            "oldPassword": Helper.Helper_common.base64encode(user, pw),
            "newPassword": Helper.Helper_common.base64encode(user, new_pw),
            "level": "strong"
        }

        res = Helper.Helper_common.call_post_api(url_req=url, token=self.token, body=body)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        actual = res[0]
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        url_login = ipv4 + "/api/v1/gateway/users/login"
        pw_new = Helper.Helper_common.base64encode(user, new_pw)
        data = {
            "userName": user,
            "password": pw_new
        }
        res = Helper.Helper_common.call_api_login_extend(url_login, data)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        actual = [res[0]['role'], res[0]['expireIn']]
        expected = [exp_data['user/login']['role'], exp_data['user/login']['expireIn']]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # body = {
        #     "userName": user,
        #     "oldPassword": Helper.Helper_common.base64encode("HS:" + user + ":" + new_pw),
        #     "newPassword": Helper.Helper_common.base64encode("HS:" + user + ":" + pw),
        #     "level": "strong"
        # }
        # Helper.Helper_common.call_post_api(url_req=url, token=self.token, body=body)
        self.assertListEqual(list_step_fail, [], '[BE_GW_13] Asserttion fail')

    def test_BE_GW_14(self):
        """"Change password API using POST method with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # FactoryReset with wrong token
        url = ipv4 + '/api/v1/gateway/users/web/change'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_post_api(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Call API with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_post_api(url, token=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Call API with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_post_api(url, token=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_14] Assertion fail')

    # NG (Implement again)
    def test_BE_GW_15(self):
        """Restore configuration of gateway API"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url_backup = ipv4 + '/api/v1/gateway/backup'
        res = Helper.Helper_common.call_post_api(url_backup, self.token)

        # Save file
        url = ipv4 + res[0]['path']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": self.token
        }
        res = requests.get(url, headers=headers)
        data = res.content
        # Delete old-version
        if os.path.exists('backupsettings.conf'):
            os.system('del backupsettings.conf')

        with open('backupsettings.conf', 'wb') as f:
            f.write(data)

        while os.path.exists('backupsettings.conf'):
            # url_restore = ipv4 + '/api/v1/gateway/restore'
            url_restore = ipv4 + '/restore'
            file_name = os.getcwd() + "\\backupsettings.conf"
            body = {
                "filename": file_name
            }
            res = Helper.Helper_common.call_post_api_extend(url_req=url_restore, headers=headers, body=body)

            try:
                self.assertEqual(res[1], 202)
                self.list_step.append(
                    '[Pass] 2.1 Assert status code is 202: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(202)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 2.1 Assert status code is 202: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(202)))
                list_step_fail.append(
                    '2.1 Assert status code is 202: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(202)))

            actual = res[0].keys()
            expected = exp_data['restore'].keys()
            try:
                self.assertListEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 2.2 Assert list Keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 2.2 Assert list Keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
                list_step_fail.append(
                    '2.2 Assert list Keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            break

        self.assertListEqual(list_step_fail, [], '[BE_GW_15] Assertion fail')
        os.system('del backupsettings.conf')

    # NG (Implement again)
    def test_BE_GW_16(self):
        """Restore configuration of gateway API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/gateway/restore'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_post_api(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_post_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Logout with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_api_logout(token=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Logout with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_api_logout(token=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_16] Assertion fail')

    def test_BE_GW_17(self):
        """API access token expire"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/gateway/about'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0].keys(), res[0]['software'].keys(), res[0]['hardware'].keys()]
        dict_about = exp_data['gateway/about']
        expected = [dict_about.keys(), dict_about['software'].keys(), dict_about['hardware'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        sension = Helper.Helper_common.call_api_login(user, pw)[0]['system']['timer']['session']

        time.sleep((sension + 1) * 60)

        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['expired_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_17] Assertion fail')

    def test_BE_GW_18(self):
        """Get gateway information API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # API about with wrong access token
        url = ipv4 + '/api/v1/gateway/about'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_get_api_token(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Logout with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_get_api_token(url_req=url, accesstoken=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Logout with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_get_api_token(url_req=url, accesstoken=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_18] Assertion fail')

    def test_BE_GW_19(self):
        """Get connectivity information API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # API connectivity with wrong access token
        url = ipv4 + '/api/v1/gateway/connectivity'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_get_api_token(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Logout with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_get_api_token(url_req=url, accesstoken=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Logout with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_get_api_token(url_req=url, accesstoken=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_19] Assertion fail')

    def test_BE_GW_20(self):
        """Get information of devices that have ever been connected to gateway API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # API devices with wrong access token
        url = ipv4 + '/api/v1/gateway/devices'
        wrong_token = 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        res = Helper.Helper_common.call_get_api_token(url, wrong_token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                        str(res[1]), str(401)))
            actual = res[0]
            expected = exp_data['invalid_token']
            try:
                self.assertDictEqual(actual, expected)
                self.list_step.append(
                    '\n[Pass] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
            except AssertionError:
                self.list_step.append(
                    '\n[Fail] 3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                        str(actual), str(expected)))
                list_step_fail.append(
                    '3.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # 4. Logout with empty access token field of header
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '4.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 5. Logout with empty access token with special keys
        token = """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        res = Helper.Helper_common.call_get_api_token(url_req=url, accesstoken=token)
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # 6. Logout with empty access token with special keys
        token = """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü"""
        res = Helper.Helper_common.call_get_api_token(url_req=url, accesstoken=token.encode('utf-8'))
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401 of API Backup: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(401)))
        actual = res[0]
        expected = exp_data['invalid_token']
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual), str(expected)))
            list_step_fail.append(
                '6.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_GW_20] Assertion fail')


if __name__ == '__main__':
    unittest.main()
