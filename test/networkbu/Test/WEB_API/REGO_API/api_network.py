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
# pw_hash_encode = Helper.Helper_common.base64encode(user , pw)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

with open('expected_api') as f:
    exp_data = json.load(f)
final_api_report = 'final_api_report_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '-') + '.xlsx'
final_api_report = os.path.join(root_dir, "Report", "WEB_API", final_api_report)
Helper.Helper_common.reset_report_api_result(final_api_report)


class Network(unittest.TestCase):
    def setUp(self):
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'skip_setup' in tags:
            return
        else:
            self.token = Helper.Helper_common.call_api_login(user, pw)[0]["accessToken"]

    def tearDown(self):
        Helper.Helper_common.report_excel_api(self.list_step, self.def_name, final_api_report)

    def test_BE_NW_01(self):
        """Implemented network APIs"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis/'
        res_docsis = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/docsis/channel'
        res_docsis_channel = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/docsis/initialFrequency'
        res_docsis_initialFrequency = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/docsis/mta/line'
        res_docsis_mta_line = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/docsis/mta/procedure'
        res_docsis_mta_procedure = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/docsis/procedure'
        res_docsis_procedure = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/lan'
        res_lan = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/operation'
        res_operation = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/network/wan'
        res_wan = Helper.Helper_common.call_get_api_token(url, self.token)

        actual = [res_docsis[1],
                  res_docsis_channel[1],
                  res_docsis_initialFrequency[1],
                  res_docsis_mta_line[1],
                  res_docsis_mta_procedure[1],
                  res_docsis_procedure[1],
                  res_lan[1],
                  res_operation[1],
                  res_wan[1]]
        check = False
        check = True if 501 in actual else check

        try:
            self.assertFalse(check)
            self.list_step.append(
                '[Pass] Status code APIs are not 501: \nActual: %s.' % (str(actual)))
        except AssertionError:
            self.list_step.append(
                '[Fail] Status code of some APIs are 501: \nActual: %s.' % (str(actual)))
            list_step_fail.append('Status code APIs are not 501: \nActual: %s.' % (str(actual)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_01] Assertion fail')

    def test_BE_NW_02(self):
        """Get general information of cable modem API"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/docsis'
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

        actual = [res[0].keys(), res[0]['cm'].keys()]
        _dict = exp_data['network/docsis']
        expected = [_dict.keys(), _dict['cm'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_02] Assertion fail')

    def test_BE_NW_03(self):
        """Get channel information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/docsis/channel'
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

        actual = [res[0].keys()]
        _dict = exp_data["network/docsis/channel"]
        expected = [_dict.keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_03] Assertion fail')

    def test_BE_NW_04(self):
        """Get initial frequency API"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/docsis/initialFrequency'
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

        actual = [res[0].keys()]
        _dict = exp_data["network/docsis/initialFrequency"]
        expected = [_dict.keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_04] Assertion fail')

    def test_BE_NW_05(self):
        """Get MTA line status API"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/docsis/mta/line'
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

        actual = [res[0][0].keys(), res[0][1].keys()]
        _dict = exp_data["network/docsis/mta/line"]
        expected = [_dict[0].keys(), _dict[1].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_05] Assertion fail')

    def test_BE_NW_06(self):
        """Get MTA startup procedure API"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/docsis/mta/procedure'
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

        actual = [res[0].keys()]
        _dict = exp_data["network/docsis/mta/procedure"]
        expected = [_dict.keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_06] Assertion fail')

    def test_BE_NW_07(self):
        """Get initialization procedure API"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/docsis/procedure'
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

        actual = [res[0].keys()]
        _dict = exp_data["network/docsis/procedure"]
        expected = [_dict.keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_07] Assertion fail')

    def test_BE_NW_08(self):
        """Get LAN information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/lan'
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

        actual = [res[0].keys(), res[0]['ipv4'].keys(), res[0]['ipv6'].keys()]
        _dict = exp_data["network/lan"]
        expected = [_dict.keys(), _dict['ipv4'].keys(), _dict['ipv6'].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_08] Assertion fail')

    def test_BE_NW_09(self):
        """Get WAN information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Login
        url = ipv4 + '/api/v1/network/wan'
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

        actual = [res[0].keys(), res[0]['interfaces'][0].keys()]
        _dict = exp_data["network/wan"]
        expected = [_dict.keys(), _dict['interfaces'][0].keys()]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_09] Assertion fail')

    def test_BE_NW_10(self):
        """Restore LAN DHCPv6 configuration default"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/network/lan/ipv6/restoreDefault'
        res = Helper.Helper_common.call_post_api(url, self.token)
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
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_10] Assertion fail')

    def test_BE_NW_11(self):
        """Restore LAN DHCPv6 configuration default with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/lan/ipv6/restoreDefault'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_post_api_extend(url, headers)
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_11] Assertion fail')

    def test_BE_NW_12(self):
        """Change switch mode bridged"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/network/wan/0/bridge'
        res = Helper.Helper_common.call_post_api(url, self.token)
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
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_12] Assertion fail')

    def test_BE_NW_13(self):
        """Change switch mode bridged with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan/0/bridge'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_post_api_extend(url, headers)
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_13] Assertion fail')

    def test_BE_NW_14(self):
        """Connect specific WAN interface"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/network/wan/0/connect'
        res = Helper.Helper_common.call_post_api(url, self.token)
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
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_14] Assertion fail')

    def test_BE_NW_15(self):
        """Connect specific WAN interface with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan/0/connect'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_post_api_extend(url, headers)
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_15] Assertion fail')

    def test_BE_NW_16(self):
        """DisConnect specific WAN interface"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/network/wan/0/disconnect'
        res = Helper.Helper_common.call_post_api(url, self.token)
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
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_16] Assertion fail')

    def test_BE_NW_17(self):
        """DisConnect specific WAN interface with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan/0/disconnect'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_post_api_extend(url, headers)
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_17] Assertion fail')

    # NG
    def test_BE_NW_18(self):
        """Update LAN settings"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + '/api/v1/network/lan'
        # Step 2
        body = {
            "ipv4":
                {
                    "ipAddress": "192.168.0.1",
                    "subnet": "255.255.255.0"
                }
        }
        res = Helper.Helper_common.call_put_api(url, self.token, body=body)
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
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        time.sleep(5)
        # Step 3
        ipv4_change = 'http://' + body['ipv4']['ipAddress'] + '/api/v1/gateway/users/login'
        pw_hash = Helper.Helper_common.base64encode('HS:' + user + ':' + pw)
        data = {
            "userName": user,
            "password": pw_hash
        }
        res = Helper.Helper_common.call_api_login_extend(url=ipv4_change, data=data)
        token3 = res[0]['accessToken']
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        # Step 4
        body4 = {
            "ipv4":
                {
                    "ipAddress": "192.168.0.1",
                    "subnet": "255.255.255.0",
                    "dhcp":
                        {
                            "active": True,
                            "startIP": "192.168.0.7",
                            "endIP": "192.168.0.209"
                        }
                }
        }

        res = Helper.Helper_common.call_put_api(url, token3, body=body4)
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
        expected = {}
        try:
            self.assertDictEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        self.assertListEqual(list_step_fail, [], '[BE_NW_18] Assertion fail')

    def test_BE_NW_19(self):
        """Update LAN settings with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/lan'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_put_api_extend(url, headers)
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
            res = Helper.Helper_common.call_put_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_put_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.call_put_api(url, token=token)
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
        res = Helper.Helper_common.call_put_api(url, token=token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_19] Assertion fail')

    # NG
    def test_BE_NW_20(self):
        """Update LAN settings with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        url = ipv4 + "/api/v1/network/lan"
        body = {
            "ipv4": {
                "ipAddress": "",
                "subnet": "",
                "dhcp": {
                    "active": True,
                    "startIP": "",
                    "endIP": "",
                    "leaseTime": 300
                }
            }
        }

        res = Helper.Helper_common.call_put_api(url_req=url, token=self.token, body=body)
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_20] Assertion fail')

    def test_BE_NW_21(self):
        """Get general information of cable modem API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url, headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_21] Assertion fail')

    def test_BE_NW_22(self):
        """Get channel information API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis/channel'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_22] Assertion fail')

    def test_BE_NW_23(self):
        """Get initial frequency API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis/initialFrequency'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_23] Assertion fail')

    def test_BE_NW_24(self):
        """Get MTA line API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis/mta/line'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_24] Assertion fail')

    def test_BE_NW_25(self):
        """Get MTA startup procedure API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis/mta/procedure'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_25] Assertion fail')

    def test_BE_NW_26(self):
        """Get initialization procedure API with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/docsis/procedure'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_26] Assertion fail')

    def test_BE_NW_27(self):
        """Get LAN information with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/lan'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_27] Assertion fail')

    def test_BE_NW_28(self):
        """Get WAN information with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
            res = Helper.Helper_common.call_get_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_get_api_extend(url, headers)
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
        res = Helper.Helper_common.call_get_api_token(url, token)
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
        res = Helper.Helper_common.call_get_api_token(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_28] Assertion fail')

    def test_BE_NW_29(self):
        """Update LAN ipv6 configuration"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Step 2
        url = ipv4 + '/api/v1/network/lan/ipv6'
        body = {
            "mode": "stateless",
            "dhcpv6":
                {
                    "startIP": "3",
                    "endIP": "102",
                    "numberOfAddresses": 256,
                    "leaseTime": 86400,
                    "rapidCommit": False,
                    "unicast": True
                }
        }
        res = Helper.Helper_common.call_put_api(url, self.token, body)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        # Step 3
        url = ipv4 + '/api/v1/network/lan'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0]['ipv6']['mode'],
                  res[0]['ipv6']['dhcpv6']['rapidCommit'],
                  res[0]['ipv6']['dhcpv6']['unicast']]

        expected = ['stateless', True, False]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 3.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 3.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '3.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Step 4
        url = ipv4 + '/api/v1/network/lan/ipv6'
        body = {
            "mode": "slaac",
            "dhcpv6":
                {
                    "startIP": "3",
                    "endIP": "102",
                    "numberOfAddresses": 256,
                    "leaseTime": 86400,
                    "rapidCommit": False,
                    "unicast": True
                }
        }
        res = Helper.Helper_common.call_put_api(url, self.token, body)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        # Step 5
        url = ipv4 + '/api/v1/network/lan'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0]['ipv6']['mode'],
                  res[0]['ipv6']['dhcpv6']['rapidCommit'],
                  res[0]['ipv6']['dhcpv6']['unicast']]

        expected = ['slaac', True, False]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 5.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 5.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '5.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Step 6
        url = ipv4 + '/api/v1/network/lan/ipv6'
        body = {
            "mode": "stateful",
            "dhcpv6":
                {
                    "startIP": "3",
                    "endIP": "102",
                    "numberOfAddresses": 256,
                    "leaseTime": 86400,
                    "rapidCommit": False,
                    "unicast": True
                }
        }
        res = Helper.Helper_common.call_put_api(url, self.token, body)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        # Step 7
        url = ipv4 + '/api/v1/network/lan'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        actual = [res[0]['ipv6']['mode'],
                  res[0]['ipv6']['dhcpv6']['rapidCommit'],
                  res[0]['ipv6']['dhcpv6']['unicast']]

        expected = ['stateful', False, True]
        try:
            self.assertListEqual(actual, expected)
            self.list_step.append(
                '\n[Pass] 7.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 7.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
            list_step_fail.append(
                '7.2 Assert values of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))
        self.assertListEqual(list_step_fail, [], '[BE_NW_29] Assertion fail')

    def test_BE_NW_30(self):
        """Update LAN IPv6 configuration with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/lan/ipv6'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_put_api_extend(url, headers)
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

        # Call api with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_put_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_put_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.call_put_api(url, token=token)
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
        res = Helper.Helper_common.call_put_api(url, token=token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_30] Assertion fail')

    def test_BE_NW_31(self):
        """Update LAN ipv6 configuration with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/lan'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        flatten = Helper.Helper_common.flatten_json(res[0]['ipv6'])
        actual = '' not in flatten.values()
        try:
            self.assertTrue(actual)
            self.list_step.append(
                '\n[Pass] 2.2 Some values require are null: \nActual: %s.' % (str(flatten)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Some values require are null: \nActual: %s.' % (str(flatten)))
            list_step_fail.append(
                '2.2 Some values require are null: \nActual: %s.' % (str(flatten)))

        # Step 3
        url = ipv4 + '/api/v1/network/lan/ipv6'
        body = {
            "mode": "",
            "dhcpv6":
                {
                    "startIP": "",
                    "endIP": "",
                    "numberOfAddresses": "",
                    "leaseTime": "",
                    "rapidCommit": "",
                    "unicast": ""
                },
            "prefix": "",
            "prefixLength": ""
        }
        res = Helper.Helper_common.call_put_api(url, self.token, body)
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

        url = ipv4 + '/api/v1/network/lan'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
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

        flatten = Helper.Helper_common.flatten_json(res[0]['ipv6'])
        actual = '' not in flatten.values()
        try:
            self.assertTrue(actual)
            self.list_step.append(
                '\n[Pass] 4.2 Some values require are null: \nActual: %s.' % (str(flatten)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 4.2 Some values require are null: \nActual: %s.' % (str(flatten)))
            list_step_fail.append(
                '4.2 Some values require are null: \nActual: %s.' % (str(flatten)))
        self.assertListEqual(list_step_fail, [], '[BE_NW_31] Assertion fail')

    # 501 PUT to /wan/0
    def test_BE_NW_32(self):
        """Update specific WAN interface configuration"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan/0'
        body = {
            "name": "default",
            "active": True,
            "linkType": "docsis",
            "connectivity": "Connected",
            "switchMode": "router",
            "connectionType": "dynamic",
            "macAddress": "94:2C:B3:3F:80:42",
            "ipv4": {
                "active": True,
                "mode": "static",
                "address": "10.0.0.102",
                "subnet": "255.255.255.0",
                "gateway": "10.0.0.1",
                "dnsAuto": False,
                "dnsServer1": "172.16.0.12",
                "dnsServer2": "8.8.4.4",
                "leaseTime": 10800,
                "expireTime": "Mon Jul 15 07:51:52 2019\n"
            }
        }
        res = Helper.Helper_common.call_post_api(url_req=url, token=self.token, body=body)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))

        # Step 3
        res = Helper.Helper_common.call_get_api_token(url, self.token)

    def test_BE_NW_33(self):
        """Update specific WAN interface configuration with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan/0'
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "Wrong_Access_Token": "c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af"
        }
        res = Helper.Helper_common.call_put_api_extend(url_req=url, headers=headers)
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
                '\n[Pass] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                str(actual), str(expected)))
        except AssertionError:
            self.list_step.append(
                '\n[Fail] 2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (
                str(actual), str(expected)))
            list_step_fail.append(
                '2.2 Assert dict return of API: \nActual: %s. \nExpected: %s.' % (str(actual), str(expected)))

        # Call api Backup with empty token
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ""
        }
        try:
            res = Helper.Helper_common.call_put_api_extend(url_req=url, headers=headers)
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
        res = Helper.Helper_common.res = Helper.Helper_common.call_put_api_extend(url, headers)
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
        res = Helper.Helper_common.call_put_api(url, token)
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
        res = Helper.Helper_common.call_put_api(url, token.encode('utf-8'))
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

        self.assertListEqual(list_step_fail, [], '[BE_NW_33] Assertion fail')

    # 501 PUT to /wan/0
    def test_BE_NW_34(self):
        """Update specific WAN interface configuration with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/network/wan/0'
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        _dict = exp_data["network/wan/0"]

        expected_key = [_dict.keys(), _dict['ipv4'].keys(), _dict['ipv6'].keys()]
        actual_key = [res[0].keys(), res[0]['ipv4'].keys(), res[0]['ipv6'].keys()]
        try:
            self.assertListEqual(actual_key, expected_key)
            self.list_step.append(
                '[Pass] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual_key), str(expected_key)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual_key), str(expected_key)))
            list_step_fail.append(
                '2.2 Assert keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual_key), str(expected_key)))

        # Step 3:
        body = {
            "name" : "",
            "active" : "",
            "linkType" : "",
            "connectivity" : "",
            "switchMode" : "",
            "connectionType" : "",
            "macAddress" : "",
            "ipv4" : {
                "active" : "",
                "mode" : "",
                "address" : "",
                "subnet" : "",
                "gateway" : "",
                "dnsAuto" : "",
                "dnsServer1" : "",
                "dnsServer2" : "",
                "leaseTime" : "",
                "expireTime" : ""
            },
            "ipv6" : {
                "active" : "",
                "mode" : "",
                "prefixLength" : "",
                "address" : "",
                "linkLocalAddress" : "",
                "gateway" : "",
                "dnsAuto" : "",
                "dnsServer1" : "",
                "dnsServer2" : "",
                "leaseTime" : "",
                "expireTime" : ""
            }
        }
        res = Helper.Helper_common.call_put_api(url, self.token, body)
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

        # Step 4:
        res = Helper.Helper_common.call_get_api_token(url, self.token)
        try :
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError :
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200 of API: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        _dict = exp_data["network/wan/0"]

        expected_key = [_dict.keys(), _dict['ipv4'].keys(), _dict['ipv6'].keys()]
        actual_key = [res[0].keys(), res[0]['ipv4'].keys(), res[0]['ipv6'].keys()]
        try :
            self.assertListEqual(actual_key, expected_key)
            self.list_step.append(
                '[Pass] 4.1 Assert keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual_key), str(expected_key)))
        except AssertionError :
            self.list_step.append(
                '[Fail] 4.1 Assert keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual_key), str(expected_key)))
            list_step_fail.append(
                '4.1 Assert keys of API: \nActual: %s. \nExpected: %s.' % (
                    str(actual_key), str(expected_key)))
        self.assertListEqual(list_step_fail, [], '[BE_NW_34] Assertion wrong')


if __name__ == '__main__':
    unittest.main()
