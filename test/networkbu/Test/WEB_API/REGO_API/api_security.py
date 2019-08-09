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


class Security(unittest.TestCase):
    def setUp(self):
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'skip_setup' in tags:
            return
        else:
            self.token = Helper.Helper_common.call_api_login(user, pw)[0]["accessToken"]

    def tearDown(self):
        Helper.Helper_common.report_excel_api(self.list_step, self.def_name, final_api_report)

    def test_BE_SR_01(self):
        """Implemented security APIs"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        url = ipv4 + '/api/v1/security/firewall'
        res_firewall = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/security/firewall/alert'
        res_firewall_alert = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/security/firewall/ipv4'
        res_firewall_ipv4 = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/security/firewall/log'
        res_firewall_log = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/security/managedServices'
        res_managed_services = Helper.Helper_common.call_get_api_token(url, self.token)

        url = ipv4 + '/api/v1/security/managedSite'
        res_managed_site = Helper.Helper_common.call_get_api_token(url, self.token)

        actual = [res_firewall[1],
                  res_firewall_alert[1],
                  res_firewall_ipv4[1],
                  res_firewall_log[1],
                  res_managed_services[1],
                  res_managed_site[1]]
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_01] Assertion fail')

    def test_BE_SR_02(self):
        """Get firewall information"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_02] Assertion wrong')

    def test_BE_SR_03(self):
        """Get firewall alert information"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_03] Assertion wrong')

    def test_BE_SR_04(self):
        """Get firewall ipv4 information"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_04] Assertion wrong')

    def test_BE_SR_05(self):
        """Get firewall ipv6 information"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_05] Assertion wrong')

    def test_BE_SR_06(self):
        """Get get managed devices"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_06] Assertion wrong')

    def test_BE_SR_07(self):
        """Get managed site"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_07] Assertion wrong')

    def test_BE_SR_08(self):
        """Get firewall information with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_08] Assertion wrong')

    def test_BE_SR_09(self):
        """Get firewall alert information with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_09] Assertion wrong')

    def test_BE_SR_10(self):
        """Get IPv4 firewall information with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_10] Assertion wrong')

    def test_BE_SR_11(self):
        """Get IPv6 firewall information with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_11] Assertion wrong')

    def test_BE_SR_12(self):
        """Get managed devices with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_12] Assertion wrong')

    def test_BE_SR_13(self):
        """Get managed site with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_13] Assertion wrong')

    def test_BE_SR_14(self):
        """Add blocked/allowed devices"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step2
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        # Step3
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_14] Assertion wrong')

    def test_BE_SR_15(self):
        """Add blocked/allowed devices with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_15] Assertion wrong')

    def test_BE_SR_16(self):
        """Add trust computer in managed services"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_16] Assertion wrong')

    def test_BE_SR_17(self):
        """Add trusted computer in managed services with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_17] Assertion wrong')

    def test_BE_SR_18(self):
        """Add blocked site/keyword"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_18] Assertion wrong')

    def test_BE_SR_19(self):
        """Add blocked site/keyword with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_19] Assertion wrong')

    def test_BE_SR_20(self):
        """Add blocked site/keyword with invalid keyword"""
        self.list_step = []
        list_step_fail = []
        self.def_name = Helper.Helper_common.get_func_name()

        # Step 2
        input_ = read_input(self.def_name, 'step2')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

        check = assert_completely(self.def_name, 'step2', res[0])
        try:
            self.assertEqual(res[1], 400)
            self.list_step.append(
                '[Pass] 2.1 Assert status code is 400: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(400)))
        except AssertionError:
            self.list_step.append(
                '[Fail] 2.1 Assert status code is 400: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(400)))
            list_step_fail.append(
                '2.1 Assert status code is 400: \nActual: %s. \nExpected: %s.' % (str(res[1]), str(400)))

        try:
            self.assertTrue(check[0])
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_20] Assertion wrong')

    def test_BE_SR_21(self):
        """Add trust computer in managed site"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_21] Assertion wrong')

    def test_BE_SR_22(self):
        """Add trusted computer in managed site with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_22] Assertion wrong')

    def test_BE_SR_23(self):
        """Update firewall configuration"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

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
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

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

        self.assertListEqual(list_step_fail, [], '[BE_SR_23] Assertion wrong')

    # 501
    def test_BE_SR_24(self):
        """Update firewall configuration invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_24] Assertion wrong')

    def test_BE_SR_25(self):
        """Update firewall configuration invalid input"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

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
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_25] Assertion wrong')

    def test_BE_SR_26(self):
        """Update firewall alert configuration"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

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
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

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

        self.assertListEqual(list_step_fail, [], '[BE_SR_26] Assertion wrong')

    # 501
    def test_BE_SR_27(self):
        """Update firewall alert configuration with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_27] Assertion wrong')

    def test_BE_SR_28(self):
        """Update IPv4 firewall configuration"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

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
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

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

        self.assertListEqual(list_step_fail, [], '[BE_SR_28] Assertion wrong')

    def test_BE_SR_29(self):
        """Update IPv4 firewall configuration with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_29] Assertion wrong')

    def test_BE_SR_30(self):
        """Update IPv4 firewall configuration"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

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
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

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

        self.assertListEqual(list_step_fail, [], '[BE_SR_30] Assertion wrong')

    # 501
    def test_BE_SR_31(self):
        """Update IPv6 firewall configuration with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_31] Assertion wrong')

    def test_BE_SR_32(self):
        """Set managed devices in parental control"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

        self.assertListEqual(list_step_fail, [], '[BE_SR_32] Assertion wrong')

    def test_BE_SR_33(self):
        """Set managed devices in parental control with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_33] Assertion wrong')

    def test_BE_SR_34(self):
        """Set managed sites in parental control"""
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
            self.list_step.append('[Pass] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
        except AssertionError:
            self.list_step.append('[Fail] 2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))
            list_step_fail.append('2.2 Assert dict of API return. \nActual: %s. \nExpected: %s'%(check[1], check[2]))

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
            list_step_fail.append(
                '3.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))

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
            list_step_fail.append(
                '4.2 Assert dict of API return. \nActual: %s. \nExpected: %s' % (check[1], check[2]))
        # Step 5
        input_ = read_input(self.def_name, 'step5')
        url = ipv4 + input_['url']
        res = call_api(url, input_['method'], self.token, input_['body'])

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

        self.assertListEqual(list_step_fail, [], '[BE_SR_34] Assertion wrong')

    def test_BE_SR_35(self):
        """Set managed devices in parental control with invalid token"""
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

        self.assertListEqual(list_step_fail, [], '[BE_SR_35] Assertion wrong')


if __name__ == '__main__':
    unittest.main()
