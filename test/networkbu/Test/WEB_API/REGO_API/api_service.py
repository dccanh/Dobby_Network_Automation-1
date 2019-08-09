import os
import sys

sys.path.append('../../../')
import json
import unittest
import datetime
import configparser
import Helper.Helper_common
from path import root_dir
from Helper.Helper_common import tag
from requests.exceptions import ReadTimeout
from Helper.Helper_common import read_input, assert_value, call_api, assert_completely, call_api_extend
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

with open('data_input', encoding='utf8') as i:
    data_input = json.load(i)
with open('data_expected', encoding='utf8') as e:
    data_expected = json.load(e)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

final_api_report = 'final_api_report_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '-') + '.xlsx'
final_api_report = os.path.join(root_dir, "Report", "WEB_API", final_api_report)
Helper.Helper_common.reset_report_api_result(final_api_report)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Service(unittest.TestCase):
    def setUp(self):
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'skip_setup' in tags:
            return
        else:
            self.token = Helper.Helper_common.call_api_login(user, pw)[0]["accessToken"]

    def tearDown(self):
        Helper.Helper_common.report_excel_api(self.list_step, self.def_name, final_api_report)

    def test_BE_SV_01(self):
        """Implemented service APIs"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/service/accessADM'
        res_accessADM = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/ddns'
        res_ddns = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/dmz'
        res_dmz = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/ipFiltering'
        res_ipFiltering = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/log'
        res_log = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/macFiltering'
        res_macFiltering = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/networkOption'
        res_networkOption = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/portFiltering'
        res_portFiltering = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/portForwarding'
        res_portForwarding = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/portIpFiltering'
        res_portIpFiltering = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/portTriggering'
        res_portTriggering = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/service/upnp'
        res_upnp = Helper.Helper_common.call_get_api_token(url, self.token)

        actual = [res_accessADM[1],
                  res_ddns[1],
                  res_dmz[1],
                  res_ipFiltering[1],
                  res_log[1],
                  res_macFiltering[1],
                  res_networkOption[1],
                  res_portFiltering[1],
                  res_portForwarding[1],
                  res_portIpFiltering[1],
                  res_portTriggering[1],
                  res_upnp[1]]
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

        self.assertListEqual(list_step_fail, [], '[BE_SV_01] Assertion fail')

    def test_BE_SV_02(self):
        """Get DDNS information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_02] Assertion wrong')

    def test_BE_SV_03(self):
        """Get DDNS information with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_03] Assertion wrong')

    def test_BE_SV_04(self):
        """Get DMZ information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_04] Assertion wrong')

    def test_BE_SV_05(self):
        """Get DMZ information with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_05] Assertion wrong')

    def test_BE_SV_06(self):
        """Get IP filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_06] Assertion wrong')

    def test_BE_SV_07(self):
        """Get IP filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_07] Assertion wrong')

    def test_BE_SV_08(self):
        """Get DDNS information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_08] Assertion wrong')

    def test_BE_SV_09(self):
        """Get log configuration and information with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_09] Assertion wrong')

    def test_BE_SV_10(self):
        """Get MAC Filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_10] Assertion wrong')

    def test_BE_SV_11(self):
        """Get MAC Filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_11] Assertion wrong')

    def test_BE_SV_12(self):
        """Get network options"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_12] Assertion wrong')

    def test_BE_SV_13(self):
        """Get network options with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_13] Assertion wrong')

    def test_BE_SV_14(self):
        """Get PORT filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_14] Assertion wrong')

    def test_BE_SV_15(self):
        """Get PORT filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_15] Assertion wrong')

    def test_BE_SV_16(self):
        """Get PORT forwarding information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_16] Assertion wrong')

    def test_BE_SV_17(self):
        """Get PORT forwarding information with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_17] Assertion wrong')

    def test_BE_SV_18(self):
        """Get port and (or) IP filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_18] Assertion wrong')

    def test_BE_SV_19(self):
        """Get port and (or) IP filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_19] Assertion wrong')

    def test_BE_SV_20(self):
        """Get PORT triggering information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_20] Assertion wrong')

    def test_BE_SV_21(self):
        """Get PORT triggering information with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_21] Assertion wrong')

    def test_BE_SV_22(self):
        """Get UPnP information"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_22] Assertion wrong')

    def test_BE_SV_23(self):
        """Get UPnP information with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_23] Assertion wrong')

    def test_BE_SV_24(self):
        """Execute ping command"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_24] Assertion wrong')

    def test_BE_SV_25(self):
        """Execute ping command invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_25] Assertion wrong')

    def test_BE_SV_26(self):
        """Execute ping command invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_26] Assertion wrong')

    def test_BE_SV_27(self):
        """Get traceroute routehops"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_27] Assertion wrong')

    def test_BE_SV_28(self):
        """Get traceroute route hops with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_28] Assertion wrong')

    def test_BE_SV_29(self):
        """Execute traceroute command"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_29] Assertion wrong')

    def test_BE_SV_30(self):
        """Execute traceroute command with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_30] Assertion wrong')

    def test_BE_SV_31(self):
        """Execute traceroute command with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_31] Assertion wrong')

    def test_BE_SV_32(self):
        """Create IP filtering rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_32] Assertion wrong')

    def test_BE_SV_33(self):
        """Create IP filtering rule with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_33] Assertion wrong')

    def test_BE_SV_34(self):
        """Create IP filtering rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_34] Assertion wrong')

    def test_BE_SV_35(self):
        """Delete all IP filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 6
        input_ = read_input(self.def_name, 'step6')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 7
        input_ = read_input(self.def_name, 'step7')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step7', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        self.assertListEqual(list_step_fail, [], '[BE_SV_35] Assertion wrong')

    def test_BE_SV_36(self):
        """Delete all IP filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_36] Assertion wrong')

    def test_BE_SV_37(self):
        """Clear log files"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_37] Assertion wrong')

    def test_BE_SV_38(self):
        """Clear log files with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_38] Assertion wrong')

    def test_BE_SV_39(self):
        """Create MAC filtering rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_39] Assertion wrong')

    def test_BE_SV_40(self):
        """Create MAC filtering rule with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_40] Assertion wrong')

    def test_BE_SV_41(self):
        """Create MAC filtering rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_41] Assertion wrong')

    def test_BE_SV_42(self):
        """Delete all MAC filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 6
        input_ = read_input(self.def_name, 'step6')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 7
        input_ = read_input(self.def_name, 'step7')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step7', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        self.assertListEqual(list_step_fail, [], '[BE_SV_42] Assertion wrong')

    def test_BE_SV_43(self):
        """Delete all MAC filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_43] Assertion wrong')

    def test_BE_SV_44(self):
        """Create PORT filtering rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 6
        input_ = read_input(self.def_name, 'step6')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 7
        input_ = read_input(self.def_name, 'step7')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step7', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        self.assertListEqual(list_step_fail, [], '[BE_SV_44] Assertion wrong')

    def test_BE_SV_45(self):
        """Create PORT filtering rule with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_45] Assertion wrong')

    def test_BE_SV_46(self):
        """Create PORT filtering rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_46] Assertion wrong')

    def test_BE_SV_47(self):
        """Delete all Port filtering rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 6
        input_ = read_input(self.def_name, 'step6')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 7
        input_ = read_input(self.def_name, 'step7')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step7', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '7.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        self.assertListEqual(list_step_fail, [], '[BE_SV_47] Assertion wrong')

    def test_BE_SV_48(self):
        """Delete all Port filtering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_48] Assertion wrong')

    def test_BE_SV_49(self):
        """Create PORT forwarding rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                'Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 6
        input_ = read_input(self.def_name, 'step6')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                    str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_49] Assertion wrong')

    def test_BE_SV_50(self):
        """Create PORT forwarding rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_50] Assertion wrong')

    def test_BE_SV_51(self):
        """Delete PORT forwarding rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_step2 = read_input(self.def_name, 'step2')
        url = ipv4 + input_step2['url']
        body_step2 = input_step2['body']
        res = call_api(url, input_step2['method'], self.token, body_step2)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)
        last_rule_id_step3 = res[0]['rules'][len(res[0]['rules'])-1]['id']
        update_times_to_expected = len(res[0]['rules'])
        for i in range(update_times_to_expected-1):
            res[0]['rules'].pop(0)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url'] + str(last_rule_id_step3)
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)
        last_rule_id_step5 = res[0]['rules'][len(res[0]['rules'] )- 1]['id']

        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (
                str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertEqual(last_rule_id_step5 , last_rule_id_step3 -1 )
            self.list_step.append(
                '[Pass] 5.2 The rules delete success. \nActual last RuleID: %d. \nExpected last RuleID: %d' % (last_rule_id_step5, last_rule_id_step3 -1))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 The rules delete fail. \nActual last RuleID: %d. \nExpected last RuleID: %d' % (last_rule_id_step5, last_rule_id_step3 -1))
            list_step_fail.append(
                '5.2 The rules delete fail. \nActual last RuleID: %d. \nExpected last RuleID: %d' % (last_rule_id_step5, last_rule_id_step3 -1))

        self.assertListEqual(list_step_fail, [], '[BE_SV_51] Assertion wrong')

    def test_BE_SV_52(self):
        """Delete PORT forwarding rule with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_step2 = read_input(self.def_name, 'step2')
        url = ipv4 + input_step2['url']
        res = call_api(url, input_step2['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 500)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_52] Assertion wrong')

    def test_BE_SV_53(self):
        """Delete PORT forwarding rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        input_step2 = read_input(self.def_name, 'step2')
        url = ipv4 + input_step2['url']
        body_step2 = input_step2['body']
        res = call_api(url, input_step2['method'], self.token, body_step2)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step4', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("4. [Fail] Timeout with empty token")

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 7
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step7', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 7.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '7.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '7.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_53] Assertion wrong')

    def test_BE_SV_54(self):
        """Change status of PORT forwarding"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_54] Assertion wrong')

    def test_BE_SV_55(self):
        """Change status of PORT forwarding"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)
        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_55] Assertion wrong')

    def test_BE_SV_56(self):
        """Change status of PORT forwarding with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_56] Assertion wrong')

    # 4 steps
    def test_BE_SV_57(self):
        """Delete all PORT Forwarding rules"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_57] Assertion wrong')

    # Wrong token
    def test_BE_SV_58(self):
        """Delete all PORT Forwarding rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_58] Assertion wrong')

    # 6 steps
    def test_BE_SV_59(self):
        """Create Port/IP filtering rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '5.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 6
        input_ = read_input(self.def_name, 'step6')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '6.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_59] Assertion wrong')

    def test_BE_SV_60(self):
        """Create Port/IP filtering rule with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_value(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_60] Assertion wrong')

    def test_BE_SV_61(self):
        """Create Port/IP filtering rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_61] Assertion wrong')

    # 3 steps
    def test_BE_SV_62(self):
        """Create PORT triggering rule"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()
        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_62] Assertion wrong')

    def test_BE_SV_63(self):
        """Create PORT triggering rule with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_63] Assertion wrong')

    def test_BE_SV_64(self):
        """Create PORT triggering rule with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_64] Assertion wrong')

    def test_BE_SV_65(self):
        """Change status PORT triggering"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token, body)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_65] Assertion wrong')

    def test_BE_SV_66(self):
        """Change status of PORT triggering with invalid input"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']
        body = input_['body']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_66] Assertion wrong')

    def test_BE_SV_67(self):
        """Change status of PORT triggering with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_67] Assertion wrong')

    def test_BE_SV_68(self):
        """Delete all PORT triggering rules"""

        # Precondition
        Service.test_BE_SV_62(self)

        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '2.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 3
        input_ = read_input(self.def_name, 'step3')
        url = ipv4 + input_['url']

        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step3', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '3.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 4
        input_ = read_input(self.def_name, 'step4')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 200)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
            list_step_fail.append(
                '4.1 Assert status code is 200: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(200)))
        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append('4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_68] Assertion wrong')

    def test_BE_SV_69(self):
        """Delete all PORT triggering rules with invalid token"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "wrong-access-token": 'c507a70e9c343c919f10559ef3a1c46c51a4fdfabecb2be61b0b552751993af'
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '2.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '2.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 3
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": ''
        }
        try:

            res = call_api_extend(url, input_['method'], headers)

            check = assert_completely(self.def_name, 'step3', res[0])
            try:
                self.assertEqual(res[1], 401)
                self.list_step.append(
                    '[Pass] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
                list_step_fail.append(
                    '3.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

            try:
                self.assertTrue(check[0])
                self.list_step.append(
                    '[Pass] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            except AssertionError:
                self.list_step.append(
                    '[Fail] 3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
                list_step_fail.append(
                    '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except ReadTimeout:
            list_step_fail.append("3. [Fail] Timeout with empty token")

        # Step 4
        headers = {
            "content-type": "application/json",
            "content-language": "en"
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step4', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '4.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """123! @ # 456:789 ^ & * ( ) + _ - = { } [ ] | . ? ` $ % \ ; '" < > , /"""
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step5', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '5.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '5.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 6
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": """NHÀO ZÔ ĐI... 2G ĐÓ ©§¼@µ¤£»²âîü""".encode('utf-8')
        }
        res = call_api_extend(url, input_['method'], headers)

        check = assert_completely(self.def_name, 'step6', res[0])
        try:
            self.assertEqual(res[1], 401)
            self.list_step.append(
                '[Pass] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))
            list_step_fail.append(
                '6.1 Assert status code is 401: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(401)))

        try:
            self.assertTrue(check[0])
            self.list_step.append(
                '[Pass] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        except AssertionError:
            self.list_step.append(
                '[Fail] 6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
            list_step_fail.append(
                '6.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SV_69] Assertion wrong')










if __name__ == '__main__':
    unittest.main()
