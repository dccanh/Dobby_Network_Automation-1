import sys
sys.path.append('../')
import os
# from Config.Gateway_Expected_data import *
import HTMLTestRunner
import requests
import unittest
import json
import time
import configparser
import Helper.Helper_common
config = configparser.ConfigParser()
config.read_file(open(r'../Config/config.txt'))
# url = config.get('URL', 'url')
# user = config.get('USER_INFO', 'user')
# pass_word = config.get('USER_INFO', 'password_base64')




# class TestLogin(unittest.TestCase):
#     def test_login(self):
#         password_base64 = Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055")
#
#         # login and get token
#         url_login = "http://192.168.0.1/api/v1/gateway/users/login"
#         data = {
#             "userName": "NET_3F8055+)*&^%",
#             "password": password_base64
#         }
#
#         res_login = requests.post(url=url_login, json=data)
#         # verity status code
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         # verify return format
#         self.assertListEqual(sorted(res_login_expected.keys()), sorted(json.loads(res_login.text).keys()),
#                              "List of return Key is different")


# class TestLogout(unittest.TestCase):
#     def setUp(self):
#         password_base64 = Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055")
#         # login and get token
#         url_login = "http://192.168.0.1/api/v1/gateway/users/login"
#         data = {
#             "userName": "NET_3F8055",
#             "password": password_base64
#         }
#
#         res_login = requests.post(url=url_login, json=data)
#         # verity status code
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_logout_valid(self):
#         url_logout = "http://192.168.0.1/api/v1/gateway/users/logout"
#         headers = {"content-type": "application/json",
#                    "content-language": "application/json",
#                    "access-Token": self.token}
#         res_logout = requests.post(url=url_logout, headers=headers)
#         self.assertEqual(res_logout.status_code, 200)
#
#     def test_logout_token_invalid(self):
#         url_logout = "http://192.168.0.1/api/v1/gateway/users/logout"
#         headers = {"content-type": "application/json",
#                    "content-language": "application/json",
#                    "access-Token": "123"}
#         res_logout = requests.post(url=url_logout, headers=headers)
#         self.assertEqual(res_logout.status_code, 401)
#
#     def test_logout_token_null(self):
#         url_logout = "http://192.168.0.1/api/v1/gateway/users/logout"
#         headers = {"content-type": "application/json",
#                    "content-language": "application/json",
#                    "access-Token": ""}
#         timeout = False
#         try:
#             # set timeout = 10s
#             res_logout = requests.post(url=url_logout, headers=headers, timeout=10.0)
#             self.assertEqual(res_logout.status_code, 401)
#         except requests.exceptions.Timeout:
#             timeout = True
#         self.assertEqual(timeout, False, "Timeout while calling API with token = null")
#
#
# # 2.1.3
# class GatewayUserAccount(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_list(self):
#         url_request = self.url + "/api/v1/gateway/users/vpn"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.4
# class GatewaySecurityLevelPasswordGet(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_security_level_passoword_get(self):
#         url_request = self.url + "/api/v1/gateway/users/web/securityLevel?userName=NET_3F8055"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.6
# class GatewayChangePassword(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_change_password_web(self):
#         url_request = self.url + "/api/v1/gateway/users/web/change"
#         headers = {"content-type": "application/json",
#                    "content-language": "en",
#                    "access-token": self.token}
#         body = {
#             "userName": "NET_3F8055",
#             "oldPassword": Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055"),
#             "newPassword": Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055"),
#             "level": "strong"
#         }
#         res = requests.post(url=url_request, headers=headers, json=body)
#         self.assertEqual(res.status_code, 200, '[] Changed password fail')
#
#     def test_gateway_change_password_vpn(self):
#         url_request = self.url + "/api/v1/gateway/users/vpn/change"
#         headers = {"content-type": "application/json",
#                    "content-language": "en",
#                    "access-token": self.token}
#         body = {
#             "userName": "NET_3F8055",
#             "oldPassword": Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055"),
#             "newPassword": Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055"),
#             "level": "strong"
#         }
#         res = requests.post(url=url_request, headers=headers, json=body)
#         self.assertEqual(res.status_code, 200, '[] Changed password fail')
#
#     def test_gateway_change_password_mediashare(self):
#         url_request = self.url + "/api/v1/gateway/users/mediashare/change"
#         headers = {"content-type": "application/json",
#                    "content-language": "en",
#                    "access-token": self.token}
#         body = {
#             "userName": "NET_3F8055",
#             "oldPassword": Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055"),
#             "newPassword": Helper.Helper_common.base64encode("HS:NET_3F8055:942CB33F8055"),
#             "level": "strong"
#         }
#         res = requests.post(url=url_request, headers=headers, json=body)
#         self.assertEqual(res.status_code, 200, '[] Changed password fail')
#
#
# # 2.1.7
# class CreateUserAccount(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_create_vpn(self):
#         url_request = self.url + "/api/v1/gateway/users/vpn"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         body = {
#             "userName": "vpn_acc_test",
#             "password": Helper.Helper_common.base64encode("HS:vpn_acc_test:00000000")
#         }
#         res = requests.post(url=url_request, headers=headers, json=body)
#         self.assertEqual(res.status_code, 200, '[] Changed password fail')
#
#     def test_gateway_user_create_mediashare(self):
#         url_request = self.url + "/api/v1/gateway/users/mediashare"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         body = {
#             "userName": "vpn_acc_test",
#             "password": Helper.Helper_common.base64encode("HS:vpn_acc_test:00000000")
#         }
#         res = requests.post(url=url_request, headers=headers, json=body)
#         self.assertEqual(res.status_code, 200, '[] Changed password fail')
#
#
# # 2.1.8
# class DeleteUserAccount(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_delete_vpn(self):
#         url_request = self.url + "/api/v1/gateway/users/ vpn / id"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.delete(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_gateway_user_delete_mediashare(self):
#         url_request = self.url + "/api/v1/gateway/users/ mediashare / id"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.delete(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.9
# class DeleteAllUserAccount(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_delete_vpn(self):
#         url_request = self.url + "/api/v1/gateway/users/ vpn / deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_gateway_user_delete_mediashare(self):
#         url_request = self.url + "/api/v1/gateway/users/ mediashare / deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.10
# class ValidateUserAccount(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         self.password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_validate_vpn(self):
#         url_request = self.url + "/api/v1/gateway/users/ vpn / validate"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_gateway_user_validate_mediashare(self):
#         url_request = self.url + "/api/v1/gateway/users/ mediashare / validate"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_gateway_user_validate_web(self):
#         url_request = self.url + "/api/v1/gateway/users/ web / validate"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.11
# class RefreshUserSession(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         self.password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_refresh_web(self):
#         url_request = self.url + "/api/v1/gateway/users/ web / refresh"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "userName": user,
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.12
# class CheckWhetherDefaultPasswordChange(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         self.password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_check_default_web(self):
#         url_request = self.url + "/api/v1/gateway/users/ web / checkDefault"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "userName": user,
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.13
# class DoNotShowWizard(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         self.password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_user_hide_wizard_web(self):
#         url_request = self.url + "/api/v1/gateway/users/ web / hideWizard "
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "userName": user,
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.1.14
# class ChangeVPNUserID(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         self.password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": self.password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_change_user_id_vpn(self):
#         url_request = self.url + "/api/v1/gateway/users/vpn/idChange"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "id": 100,
#             "oldID": "myvpn",
#             "newID": "yourvpn"
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.2.1
# class GetConnectivityInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_connectivity(self):
#         url_request = self.url + "/api/v1/gateway/connectivity"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.3.1
# class GetGatewayInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_about(self):
#         url_request = self.url + "/api/v1/gateway/about"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data_about = json.loads(res.text)
#
#
#
#
# # 2.3.2
# class GetRegistrationCode(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_registration_code(self):
#         url_request = self.url + "/api/v1/gateway/regCode"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.3.3
# class GetPrivacyPolicy(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_privacy_policy_get(self):
#         url_request = self.url + "/api/v1/gateway/privacyPolicy"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.3.4
# class SetPrivacyPolicy(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_privacy_policy_set(self):
#         url_request = self.url + "/api/v1/gateway/privacyPolicy"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "mandatory": True,
#             "optional": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.4.1
# class CPU(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     # 2.4.1.1
#     def test_gateway_cpu_usage(self):
#         url_request = self.url + "/api/v1/gateway/statuses/cpuUsage"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 2.4.1.2
#     def test_gateway_cpu_temperature(self):
#         url_request = self.url + "/api/v1/gateway/statuses/cpuTemp"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.4.2
# class Memory(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     # 2.4.2.1
#     def test_gateway_memory_usage(self):
#         url_request = self.url + "/api/v1/gateway/statuses/memoryUsage "
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#         # 2.4.2.2
#
#     def test_gateway_temperature_current(self):
#         url_request = self.url + "/api/v1/gateway/statuses/temperature"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.5.1
# class GetInformationOfDevice(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     # 2.5.1.1
#     def test_gateway_devices_list_connected(self):
#         url_request = self.url + "/api/v1/gateway/devices?connected=true "
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 2.5.1.2
#     def test_gateway_devices_list_interface(self):
#         url_request = self.url + "/api/v1/gateway/devices?interface=lan "
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 2.5.1.3
#     def test_gateway_devices_list_interface_5g(self):
#         url_request = self.url + "/api/v1/gateway/devices?connected=true&interface=lan,2.4g "
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 2.5.1.4
#     def test_gateway_devices_list_interface_ssid(self):
#         url_request = self.url + "/api/v1/gateway/devices?connected=true&interface=5g&ssid=0"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 2.5.1.5
#     def test_gateway_devices_list_networkType(self):
#         url_request = self.url + "/api/v1/gateway/devices?connected=true&interface=2.4g&networkType=guest"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.5.2
# class GetSpecificDeviceInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_devices_getOne(self):
#         url_request = self.url + "/api/v1/gateway/devices/0C:54:15:F6:20:02"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.5.3
# class UpdateSpecificDeviceInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_devices_update(self):
#         url_request = self.url + "/api/v1/gateway/devices/0C:54:15:F6:20:02"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "deviceName": "dccanh",
#             "type": "PC"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.6.1
# class CurrentLEDStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_led_get(self):
#         url_request = self.url + "/api/v1/gateway/led"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.6.2
# class UpdateLEDStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_led_update(self):
#         url_request = self.url + "/api/v1/gateway/led"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "power": True,
#             "mode": "always"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.7.1
# class GetDateTimeInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_datetime_get(self):
#         url_request = self.url + "/api/v1/gateway/datetime"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.7.2
# class UpdateDateTimeInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_datetime_get(self):
#         url_request = self.url + "/api/v1/gateway/datetime"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "timeZone": 0,
#             "daylightSavingTime": {
#                 "active": True,
#                 "startDate": "...",
#                 "endDate": "..."
#             },
#             "ntp": {
#                 "active": True,
#                 "server": [
#                     "0.pool.ntp.org",
#                     "1.pool.ntp.org"
#                 ]
#             }
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.7.3
# class DeleteNTPServer(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_datetime_delete(self):
#         url_request = self.url + "/api/v1/gateway/datetime/   id "
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#
#         res = requests.delete(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.8.1
# class GetCurrentLanguage(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_language_get(self):
#         url_request = self.url + "/api/v1/gateway/language/0C:54:15:F6:20:02"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.8.2
# class ChangeLangeguage(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_language_change(self):
#         url_request = self.url + "/api/v1/gateway/language"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "id": "0C:54:15:F6:20:02",  # ?????
#             "code": "ko",
#             "name": "Korean"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.9.1
# class GetBatteryStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_batery_get(self):
#         url_request = self.url + "/api/v1/gateway/battery"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.10.1
# class GetPowerSavingMode(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_powersave_mode_get(self):
#         url_request = self.url + "/api/v1/gateway/powersave"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.10.2
# class UpdatePowerSavingMode(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_powersaving_mode_change(self):
#         url_request = self.url + "/api/v1/gateway/powersave"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True,
#             "powerTimer": 10
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.11.1
# class CheckWhetherThereIsNewFirmwareUpdate(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_check_new_update(self):
#         url_request = self.url + "/api/v1/gateway/firmware/checkNew"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.11.2
# class GetStatusOfKeepingFirmwareUptodate(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_firmware_get(self):
#         url_request = self.url + "/api/v1/gateway/firmware"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.11.3
# class UpdateStatusOfKeepingFirmwareUptodate(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_firmware_get(self):
#         url_request = self.url + "/api/v1/gateway/firmware"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "autoUpdate": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.12.1
# class SWUpgrade(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_upgrade(self):
#         url_request = self.url + "/api/v1/gateway/upgrade"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "type": "manual"
#             # "filename": "hg700_v1.0.0.img"
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.12.2
# class CheckSWUpgradeStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_upgrade_status(self):
#         url_request = self.url + "/api/v1/gateway/upgrade/status"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.12.3
# class FactoryReset(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_factory_reset(self):
#         url_request = self.url + "/api/v1/gateway/factoryReset"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 202, 'Watting factory reset ~ 100s')
#         time.sleep(100)
#
#
# # 2.12.4
# class Reboot(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_reboot(self):
#         url_request = self.url + "/api/v1/gateway/reboot"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 202, 'Waitting for reboot ~ 100s')
#         time.sleep(100)


# 2.12.5
class Backup(unittest.TestCase):
    def setUp(self):
        url = 'http://12.168.0.1'
        password_base64 = Helper.Helper_common.base64encode("HS:NET_4F9761:942CB34F9761")
        url_login = url + "/api/v1/gateway/users/login"
        data = {
            "userName": 'NET_4F9761',
            "password": '942CB34F9761'
        }
        res_login = requests.post(url=url_login, json=data)
        self.assertEqual(res_login.status_code, 200,
                         "API login doesn't return status code 200 when calling API with valid username/password")
        self.token = json.loads(res_login.text)["accessToken"]

    def test_gateway_backup(self):
        url_request = "http://12.168.0.1/api/v1/gateway/backup"
        headers = {
            "content-type": "application/json",
            "content-language": "en",
            "access-token": self.token
        }
        res = requests.post(url=url_request, headers=headers)
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.text)
        backup = json_data['path']
        res_backup = requests.get('http://192.168.0.1' + backup, headers=headers)
        backup_text = res_backup.text
        file = open('backupsettings.conf', 'w', encoding='utf-8')
        file.write(backup_text)
        file.close()


# 2.12.6
# class Restore(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_backup(self):
#         url_request = self.url + "/api/v1/gateway/restore"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         file_name = os.getcwd() + "backupsettings.conf"
#         data = {
#             "filename": file_name
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 202)
#
#
# # 2.13.1
# class GetDeviceManagement(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_device_management_get(self):
#         url_request = self.url + "/api/v1/gateway/tr069"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 2.13.2
# class UpdateDeviceManagement(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_gateway_device_management_change(self):
#         url_request = self.url + "/api/v1/gateway/tr069"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True,
#             "periodicInform": {
#                 "active": True,
#                 "interval": 86400
#             },
#             "acs": {
#                 "url": "http://acs.co.kr",
#                 "username": "root",
#                 "password": "1234"
#             },
#             "connectionRequest": {
#                 "username": "admin",
#                 "password": "password",
#                 "port": 7547
#             },
#             "certificate": {
#                 "active": False
#             }
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)


#
##
#
# WIFI
# 3.1.1
# class GetInterfacesInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_interface_get(self):
#         url_request = self.url + "/api/v1/wifi"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         actual = json_data['interfaces']
#         expected = wifi_interface_get_expected['interfaces']
#         self.assertListEqual(actual, expected, 'List of interfaces wrong.')


# 3.2.1
# class GetRadioInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_get_2g_active(self):
#         url_request = self.url + "/api/v1/wifi/0/radio?filter=channelList"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(get_radio_information_expected.keys()),
#                              'List main keys wrong')
#
#     def test_wifi_radio_get_5g_channelList(self):
#         url_request = self.url + "/api/v1/wifi/1/radio"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(get_radio_information_expected.keys()),
#                              'List main keys wrong')


# 3.2.2
# class ChangeParameterRadio(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_change_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/radio"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "true",
#             "basic": {
#                 "channel": {
#                     "set": "auto",
#                     "used": 1
#                 },
#                 "wirelessMode": "802.11bgn",
#                 "bandwidth": {
#                     "set": "auto",
#                     "used": "40"
#                 },
#                 "sideband": "upper",
#                 "outputPower": "high"
#             },
#             "advanced": {
#                 "obssCoexistence": "false",
#                 "802dot11Protection": "true",
#                 "regulatoryMode": "true",
#                 "beamforming": "true",
#                 "shortGuardInterval": "auto",
#                 "beaconInterval": "10",
#                 "dtimInteval": "30",
#                 "fragmentationThreshold": "1",
#                 "rstThreshold": "1",
#                 "dfs": True,
#                 "countryCode": "US",
#                 "mumimo": True
#             },
#             "wmm": {
#                 "active": True,
#                 "option": "Normal",
#                 "noAck": True,
#                 "powerSave": True
#             }
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_radio_change_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/radio"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "true",
#             "basic": {
#                 "channel": {
#                     "set": "auto",
#                     "used": 1
#                 },
#                 "wirelessMode": "802.11bgn",
#                 "bandwidth": {
#                     "set": "auto",
#                     "used": "40"
#                 },
#                 "sideband": "upper",
#                 "outputPower": "high"
#             },
#             "advanced": {
#                 "obssCoexistence": "false",
#                 "802dot11Protection": "true",
#                 "regulatoryMode": "true",
#                 "beamforming": "true",
#                 "shortGuardInterval": "auto",
#                 "beaconInterval": "10",
#                 "dtimInteval": "30",
#                 "fragmentationThreshold": "1",
#                 "rstThreshold": "1",
#                 "dfs": True,
#                 "countryCode": "US",
#                 "mumimo": True
#             },
#             "wmm": {
#                 "active": True,
#                 "option": "Normal",
#                 "noAck": True,
#                 "powerSave": True
#             }
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.2.3
# class ChangeStatusOfRadio(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_inactive_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/radio/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": False
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertFalse(json_data['active'], 'API must be return value of Acitve is False')
#
#     def test_wifi_radio_active_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/radio/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertTrue(json_data['active'], 'API must be return value of Acitve is True')
#
#     def test_wifi_radio_active_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/radio/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertTrue(json_data['active'], 'API must be return value of Acitve is True')
#
#     def test_wifi_radio_inactive_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/radio/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": False
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertFalse(json_data['active'], 'API must be return value of Acitve is False')
#
#
# # 3.2.4
# class RestoreWifiRadioConfigByDefault(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_restore_default(self):
#         url_request = self.url + "/api/v1/wifi/0/radio/restoreDefault"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.2.5
# class GetCountryCodeListOfEachRadio(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_country_code_get_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/radio/countryCode"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_radio_country_code_get_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/radio/countryCode"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.2.6
# class GetAntennaInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_antenna_get_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/radio/antenna"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_radio_antenna_get_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/radio/antenna"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.2.7
# class SetAntenna(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_radio_antenna_set_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/radio/antenna/0"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)


# 3.3.1
# class GetWorkType(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_network_type_get_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(json_data, get_work_type_expected)
#
#     def test_wifi_network_type_get_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/networkType"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(json_data, get_work_type_expected)


# 3.3.2
# class ChangeStatusOfWifiNetwork(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_network_type_change_2g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType/guest"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_network_type_change_2g_primary(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType/primary"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_network_type_change_2g_mso(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType/mso"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_network_type_change_5g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType/guest"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_network_type_change_5g_primary(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType/primary"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_network_type_change_5g_mso(self):
#         url_request = self.url + "/api/v1/wifi/0/networkType/mso"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.4.1
# class GetBriefSSIDInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_list_all_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         actual_primary = []
#         actual_guest = []
#         for j in range(len(json_data)):
#             if json_data[j]['type'] == 'primary':
#                 actual_primary.append(json_data[j]['index'])
#             elif json_data[j]['type'] == 'guest':
#                 actual_guest.append(json_data[j]['index'])
#
#         url_expected = "http://192.168.0.1/api/v1/wifi/0/networkType"
#         res_expected = requests.get(url=url_expected, headers=headers)
#         json_expected = json.loads(res_expected.text)
#         expected_primary = []
#         expected_guest = []
#         for i in range(len(json_expected)):
#             if json_expected[i]['key'] == 'primary':
#                 expected_primary += json_expected[i]['ssid']
#             elif json_expected[i]['key'] == 'guest':
#                 expected_guest += json_expected[i]['ssid']
#
#         self.assertListEqual(actual_primary, expected_primary)
#         self.assertListEqual(actual_guest, expected_guest)
#
#     def test_wifi_ssid_list_all_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/ssid"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         actual_primary = []
#         actual_guest = []
#         for j in range(len(json_data)):
#             if json_data[j]['type'] == 'primary':
#                 actual_primary.append(json_data[j]['index'])
#             elif json_data[j]['type'] == 'guest':
#                 actual_guest.append(json_data[j]['index'])
#
#         url_expected = "http://192.168.0.1/api/v1/wifi/1/networkType"
#         res_expected = requests.get(url=url_expected, headers=headers)
#         json_expected = json.loads(res_expected.text)
#         expected_primary = []
#         expected_guest = []
#         for i in range(len(json_expected)):
#             if json_expected[i]['key'] == 'primary':
#                 expected_primary += json_expected[i]['ssid']
#             elif json_expected[i]['key'] == 'guest':
#                 expected_guest += json_expected[i]['ssid']
#
#         self.assertListEqual(actual_primary, expected_primary)
#         self.assertListEqual(actual_guest, expected_guest)
#
#
# # 3.4.2
# class GetSpecificSSIDInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_get_2g(self):
#         ssid_id = 0
#         url_request = self.url + "/api/v1/wifi/0/ssid/" + str(ssid_id)
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         actual_type = json_data['type']
#         actual_index = json_data['index']
#         self.assertEqual(actual_index, ssid_id, 'Index ID is not match with ssid ID')
#         # API get list all
#         url_expected = "http://192.168.0.1/api/v1/wifi/0/ssid"
#         res_expected = requests.get(url=url_expected, headers=headers)
#         json_expected = json.loads(res_expected.text)
#         expected_type = ''
#         for i in range(len(json_expected)):
#             if json_expected[i]['index'] == ssid_id:
#                 expected_type = json_expected[i]['type']
#                 break
#         self.assertEqual(actual_type, expected_type, 'Actual Type is not match with expected Type')
#
#     def test_wifi_ssid_get_5g(self):
#         ssid_id = 5
#         url_request = self.url + "/api/v1/wifi/1/ssid/" + str(ssid_id)
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         actual_type = json_data['type']
#         actual_index = json_data['index']
#         self.assertEqual(actual_index, ssid_id, 'Index ID is not match with ssid ID')
#         # API get list all
#         url_expected = "http://192.168.0.1/api/v1/wifi/1/ssid"
#         res_expected = requests.get(url=url_expected, headers=headers)
#         json_expected = json.loads(res_expected.text)
#         expected_type = ''
#         for i in range(len(json_expected)):
#             if json_expected[i]['index'] == ssid_id:
#                 expected_type = json_expected[i]['type']
#                 break
#         self.assertEqual(actual_type, expected_type, 'Actual Type is not match with expected Type')
#
#
# # 3.4.3
# class UpdateSpecificSSIDParameter(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_update_2g(self):
#         ssid_id = 0
#         url_request = self.url + "/api/v1/wifi/0/ssid/" + str(ssid_id)
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         expected_name = "myPrimary1"
#         pw = "12345678"
#         pw_base64 = Helper.Helper_common.base64encode(pw)
#         data = {
#             "active": "true",
#             "name": expected_name,
#             "security": {
#                 "type": "WPA-PSK",
#                 "personal": {
#                     "encryption": "AES",
#                     "password": pw_base64,
#                     "groupKey": 120
#                 },
#                 "enterprise": None,
#                 "wep": None
#             },
#             "webUIAccess": True,
#             "hiddenSSID": True,
#             "APIsolate": True,
#             "internetOnly": False
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#         GetSpecificSSIDInformation.test_wifi_ssid_get_2g(self)
#         json_actual = json.loads(res.text)
#         self.assertEqual(json_actual['name'], expected_name, 'Update Name fail')
#
#
# # 3.4.4
# class CreateGuestSSID(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_create_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         expected_name = "Ciel_Primary"
#         pw = "12345678"
#         # pw_base64 = Helper.Helper_common.base64encode(pw)
#         data = {
#             "active": "true",
#             "name": expected_name,
#             "security": {
#                 "type": "WPA-PSK",
#                 "personal": {
#                     "encryption": "AES",
#                     "password": pw,
#                     "groupKey": 120
#                 },
#                 "enterprise": None,
#                 "wep": None
#             },
#             "webUIAccess": True,
#             "hiddenSSID": True,
#             "APIsolate": True,
#             "internetOnly": False
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.4.5
# class DeleteAGuestSSID(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_delete_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.delete(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 204)
#
#
# # 3.4.6
# # class DeleteAllGuestSSID(unittest.TestCase):
# #     def setUp(self):
# #         self.url = url
# #         password_base64 = Helper.Helper_common.base64encode(pass_word)
# #         url_login = url + "/api/v1/gateway/users/login"
# #         data = {
# #             "userName": user,
# #             "password": password_base64
# #         }
# #         res_login = requests.post(url=url_login, json=data)
# #         self.assertEqual(res_login.status_code, 200,
# #                          "API login doesn't return status code 200 when calling API with valid username/password")
# #         self.token = json.loads(res_login.text)["accessToken"]
# #
# #     def test_wifi_ssid_delete_2g(self):
# #         url_request = self.url + "/api/v1/wifi/0/ssid/deletes"
# #         headers = {
# #             "content-type": "application/json",
# #             "content-language": "en",
# #             "access-token": self.token
# #         }
# #         res = requests.delete(url=url_request, headers=headers)
# #         self.assertEqual(res.status_code, 200)
#
#
# # 3.4.6
# class ChangeStatusOfSSID(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_active_5g_guest(self):
#         url_request = self.url + "/api/v1/wifi/1/ssid/1/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         status = False
#         data = {
#             "active": status
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#         url_ = "http://192.168.0.1/api/v1/wifi/1/ssid/1"
#         res_ = requests.get(url=url_, headers=headers)
#         json_data = json.loads(res_.text)
#         self.assertEqual(json_data['active'], status, 'Status of active is not change')
#         # Return to the original status
#         data_revert = {
#             "active": True
#         }
#         requests.post(url=url_request, headers=headers, json=data_revert)
#
#     def test_wifi_ssid_active_5g_primary(self):
#         url_request = self.url + "/api/v1/wifi/1/ssid/0/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         status = False
#         data = {
#             "active": status
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#         url_ = "http://192.168.0.1/api/v1/wifi/1/ssid/0"
#         res_ = requests.get(url=url_, headers=headers)
#         json_data = json.loads(res_.text)
#         self.assertEqual(json_data['active'], status, 'Status of active is not change')
#         # Return to the original status
#         data_revert = {
#             "active": True
#         }
#         requests.post(url=url_request, headers=headers, json=data_revert)
#
#     def test_wifi_ssid_active_2g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         status = False
#         data = {
#             "active": status
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#         url_ = "http://192.168.0.1/api/v1/wifi/0/ssid/1"
#         res_ = requests.get(url=url_, headers=headers)
#         json_data = json.loads(res_.text)
#         self.assertEqual(json_data['active'], status, 'Status of active is not change')
#         # Return to the original status
#         data_revert = {
#             "active": True
#         }
#         requests.post(url=url_request, headers=headers, json=data_revert)
#
#     def test_wifi_ssid_active_2g_primary(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/0/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         status = False
#         data = {
#             "active": status
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#         url_ = "http://192.168.0.1/api/v1/wifi/0/ssid/0"
#         res_ = requests.get(url=url_, headers=headers)
#         json_data = json.loads(res_.text)
#         self.assertEqual(json_data['active'], status, 'Status of active is not change')
#         # Return to the original status
#         data_revert = {
#             "active": True
#         }
#         requests.post(url=url_request, headers=headers, json=data_revert)
#
#
# # 3.5.1
# class GetWifiAccessControl(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_get_2g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/0/accessControl"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.5.2
# class UpdateWifiAccessControl(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_update_2g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/accessControl"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True,
#             "allow": True,
#             "maxRules": 12,
#             "rules": [
#                 {
#                     "id": 1,
#                     "name": "HVN PC",
#                     "macAddress": "94:2C:B3:3F:80:5A"
#                 }
#             ],
#             "probeResponse": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.5.3
# class UpdateSpecificWifiAccessControlRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_path_2g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/accessControl/ruleID"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True,
#             "allow": True,
#             "maxRules": 12,
#             "rules": [
#                 {
#                     "id": 1,
#                     "name": "HVN PC",
#                     "macAddress": "94:2C:B3:3F:80:5A"
#                 }
#             ],
#             "probeResponse": True
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.5.4
# class CreateWifiAccessControlRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_path(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/accessControl"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "name": "mypc",
#             "macAddress": "F8:CA:B8:52:27:24"
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.5.5
# class DeleteWifiAccessControlRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_delete_one(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/accessControl/1"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.delete(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 204)
#
#
# # 3.5.6
# class DeleteAllWifiAccessControlRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_delete_all(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/accessControl/deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.delete(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 204)
#
#
# # 3.5.7
# class ChangeStatusOfWifiAccessControl(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_ssid_accesscontrol_active_2g_guest(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/1/accessControl/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_ssid_accesscontrol_active_5g_guest(self):
#         url_request = self.url + "/api/v1/wifi/1/ssid/1/accessControl/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_ssid_accesscontrol_active_2g_primary(self):
#         url_request = self.url + "/api/v1/wifi/0/ssid/0/accessControl/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_ssid_accesscontrol_active_5g_primary(self):
#         url_request = self.url + "/api/v1/wifi/1/ssid/0/accessControl/active"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": True
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)


# 3.6.1
# class GetWPSStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wps_get(self):
#         url_request = self.url + "/api/v1/wifi/wps"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_wps_get_expected.keys()), 'No match keys. '
#                              + 'Expected: ' + str(sorted(wifi_wps_get_expected.keys()))
#                              + 'Actual: ' + str(sorted(json_data.keys())))
#
#
# # 3.6.2
# class GetWPSConnectionStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wps_get_connection(self):
#         url_request = self.url + "/api/v1/wifi/wps/connection"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_wps_get_connection_expected.keys()),
#                              'No match keys. '
#                              + 'Expected: ' + str(sorted(wifi_wps_get_connection_expected.keys()))
#                              + 'Actual: ' + str(sorted(json_data.keys())))


# 3.6.3
# class UpdateWPSStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wps_update(self):
#         url_request = self.url + "/api/v1/wifi/wps"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "false"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)


# 3.6.4
# class Commands(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     # 3.6.4.1
#     def test_wifi_wps_activate(self):
#         url_request = self.url + "/api/v1/wifi/wps/activate"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 3.6.4.2
#     def test_wifi_wps_activate_pin(self):
#         url_request = self.url + "/api/v1/wifi/wps/devicePin"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "pin": "B33F8055",
#             "macAddress": "F8:CA:B8:52:27:24"
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     # 3.6.4.3
#     def test_wifi_wps_router_pin(self):
#         url_request = self.url + "/api/v1/wifi/wps/routerPin"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertEqual(json_data.keys(), wifi_wps_activate_routerpin_expected.keys(), 'No match keys'
#                          + 'Expected: ' + str(json_data.keys())
#                          + 'Actual: ' + str(wifi_wps_activate_routerpin_expected.keys()))
#
#     # 3.6.4.4
#     def test_wifi_wps_cancel(self):
#         url_request = self.url + "/api/v1/wifi/wps/cancel"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     # 3.6.4.5
#     def test_wifi_wps_restore_default(self):
#         url_request = self.url + "/api/v1/wifi/wps/restoreDefault"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.7.1
# class GetWMMInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wmm_get_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wmm"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_wmm_get_expected.keys()), 'No match keys API 2.4G'
#                              + 'Expected: ' + str(sorted(wifi_wmm_get_expected.keys()))
#                              + 'Actual: ' + str(sorted(json_data.keys())))
#
#     def test_wifi_wmm_get_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/wmm"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_wmm_get_expected.keys()), 'No match keys API 5G'
#                              + 'Expected: ' + str(sorted(wifi_wmm_get_expected.keys()))
#                              + 'Actual: ' + str(sorted(json_data.keys())))


# 3.7.2
# class UpdateWMMSetting(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wmm_update_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wmm"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "true",
#             "option": "normal",
#             "noAck": "true",
#             "powersave": "false"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_wmm_update_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/wmm"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "true",
#             "option": "normal",
#             "noAck": "true",
#             "powersave": "false"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)


# 3.8.1
# class GetWDSListAndStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wds_get_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wds"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_wds_get_expected.keys()), 'No match keys.'
#                              + 'Expected: ' + str(sorted(wifi_wds_get_expected.keys()))
#                              + 'Actual: ' + str(sorted(json_data.keys())))
#
#     def test_wifi_wds_get_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/wds"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_wds_get_expected.keys()), 'No match keys.'
#                              + 'Expected: ' + str(sorted(wifi_wds_get_expected.keys()))
#                              + 'Actual: ' + str(sorted(json_data.keys())))


# # 3.8.2
# class ChangeStatusOfWDS(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wds_update_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wds"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "false"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_wds_update_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/wds"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "active": "false"
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.8.3
# class AddWDSRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wds_create_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wds"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "type": "slave",
#             "ssid": "mySSID",
#             "mac": "12:23:35:aa:bb:cc:",
#             "ext": {
#                 "channel": 10,
#                 "security": {
#                     "type": "WPA-PSK",
#                     "personal": {
#                         "encryption": "AES",
#                         "password": "abcde"
#                     },
#                     "wep": None
#                 },
#                 "ipAdddress": "192.168.1.1"
#             }
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 201)
#
#     def test_wifi_wds_create_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/wds"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "type": "slave",
#             "ssid": "mySSID",
#             "mac": "12:23:35:aa:bb:cc:",
#             "ext": {
#                 "channel": 10,
#                 "security": {
#                     "type": "WPA-PSK",
#                     "personal": {
#                         "encryption": "AES",
#                         "password": "abcde"
#                     },
#                     "wep": None
#                 },
#                 "ipAdddress": "192.168.1.1"
#             }
#         }
#         res = requests.post(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 201)
#
#
# # 3.8.4
# class DeleteWDSRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wds_delete_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wds/ ruleid"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.delelte(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 204)
#
#
# # 3.8.5
# class DeleteAllWDSRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_wds_delete_all_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/wds/ deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_wds_delete_all_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/wds/ deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.9.1
# class RestoreWifiDefault(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_restore_default_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/restore"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_restore_default_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/restore"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 3.9.2
# class RestartWifiInterface(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_restart_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/restart"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#     def test_wifi_restore_default_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/restart"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)


# 3.9.3
# class ScanAP(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_scan_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/scan"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 202)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_scan_expected.keys()),
#                              'No match keys'
#                              + 'Expected: ' + str(sorted(json_data.keys()))
#                              + 'Actual: ' + str(sorted(wifi_scan_expected.keys())))
#
#     def test_wifi_scan_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/scan"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 202)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(wifi_scan_expected.keys()),
#                              'No match keys'
#                              + 'Expected: ' + str(sorted(json_data.keys()))
#                              + 'Actual: ' + str(sorted(wifi_scan_expected.keys())))
#
#
# # 3.9.4
# class GetResultOfScanningAP(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_wifi_scan_result_2g(self):
#         url_request = self.url + "/api/v1/wifi/0/scanResult"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(list(json_data[0].keys())), sorted(wifi_scan_result_expected[0].keys()),
#                              'No match keys'
#                              + 'Expected: ' + str(sorted(list(json_data[0].keys())))
#                              + 'Actual: ' + str(sorted(wifi_scan_result_expected[0].keys())))
#
#     def test_wifi_scan_result_5g(self):
#         url_request = self.url + "/api/v1/wifi/1/scanResult"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(list(json_data[0].keys())), sorted(wifi_scan_result_expected[0].keys()),
#                              'No match keys'
#                              + 'Expected: ' + str(sorted(list(json_data[0].keys())))
#                              + 'Actual: ' + str(sorted(wifi_scan_result_expected[0].keys())))
#
#
# ##
# ##
# ##
# #           NETWORK API             #
# # 4.1.1
# class GetLANInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_lan_get(self):
#         url_request = self.url + "/api/v1/network/lan"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#         json_data = json.loads(res.text)
#         self.assertListEqual(sorted(json_data.keys()), sorted(network_lan_get_expected.keys()),
#                              'No match keys'
#                              + 'Expected: ' + str(sorted(json_data.keys()))
#                              + 'Actual: ' + str(sorted(network_lan_get_expected.keys())))


# # 4.1.2  =================>> ERROR
# class UpdateLANConfiguration(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_lan_update(self):
#         url_request = self.url + "/api/v1/network/lan"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "ipv4": {
#                 "ipAddress": "192.168.0.1",
#                 "subnet": "255.255.255.0",
#                 "dhcp": {
#                     "active": True,
#                     "startIP": "192.168.0.2",
#                     "endIP": "192.168.0.200",
#                     "leaseTime": 60,
#                     "primaryDNS": "8.8.8.8",
#                     "secondaryDNS": "8.8.8.9",
#                     "dnsProxy": False
#                 }
#             },
#             "ipv6": {
#                 "mode": "stateful",
#                 "ipAddress": "2001:DB8:0101:1::1",
#                 "linkLocal": "fe00::1",
#                 "dhcpv6": {
#                     "startIP": "1",
#                     "endIP": "100",
#                     "numberOfAddresses": 256,
#                     "leaseTime": 86400,
#                     "rapidCommit": False,
#                     "unicast": True
#                 },
#                 "prefix": "2001:DB8::1",
#                 "prefixLength": 64
#             }
#         }
#
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.1.3
# class UpdateLANIPv6Configuration(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_lan_ipv6_update(self):
#         url_request = self.url + "/api/v1/network/lan/ipv6"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         data = {
#             "mode": "stateful",
#             "ipAddress": "2001:DB8:0101:1::1",
#             "linkLocal": "fe00::1",
#             "dhcpv6": {
#                 "startIP": "1",
#                 "endIP": "100",
#                 "numberOfAddresses": 256,
#                 "leaseTime": 86400,
#                 "rapidCommit": False,
#                 "unicast": True
#             },
#             "prefix": "2001:DB8::1",
#             "prefixLength": 64
#         }
#         res = requests.put(url=url_request, headers=headers, json=data)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.1.4
# class RestoreLANDHCpv6ConfigurationDefault(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_lan_ipv6_restoreDefault(self):
#         url_request = self.url + "/api/v1/network/lan/ipv6/restoreDefault"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.2.1
# class GetWANInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_wan_information(self):
#         url_request = self.url + "/api/v1/network/wan"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.7.2
# class GetChannelInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_docsis_channel_get(self):
#         url_request = self.url + "/api/v1/network/docsis/channel"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.7.3
# class GetInitializationProcedure(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_docsis_initial_procedure_get(self):
#         url_request = self.url + "/api/v1/network/docsis/procedure"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.7.6
# class GetMTALineStatus(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_docsis_mta_procedure_get(self):
#         url_request = self.url + "/api/v1/network/docsis/mta/line"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.7.6
# class GetMTAStartUPProcedure(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_docsis_mta_procedure_get(self):
#         url_request = self.url + "/api/v1/network/docsis/mta/procedure"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 4.7.7
# class GetInitialFrequency(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_network_docsis_initial_frequency_get(self):
#         url_request = self.url + "/api/v1/network/docsis/initialFrequency"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.1.1
# class GetMACFilteringRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_mac_filtering_list(self):
#         url_request = self.url + "/api/v1/service/macFiltering"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.1.6
# class DeleteAllPortIPFilteringRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_macfiltering_delete_all(self):
#         url_request = self.url + "/api/v1/service/macFiltering/deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.8.1
# class GetDMZInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_dmz_get(self):
#         url_request = self.url + "/api/v1/service/dmz"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# class GetDDNSInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_ddns_get(self):
#         url_request = self.url + "/api/v1/service/ddns"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
# # 5.11.1
# class GetUPnPInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_networkOption_get(self):
#         url_request = self.url + "/api/v1/service/upnp"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.12.1
# class GetLog(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_log_get(self):
#         url_request = self.url + "/api/v1/service/log"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.17.1
# class GetNetworkOption(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_networkOption_get(self):
#         url_request = self.url + "/api/v1/service/networkOption"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.18.1
# class GetPortIPFilteringRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_port_ipfiltering_list(self):
#         url_request = self.url + "/api/v1/service/portIpFiltering"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 5.18.5
# class DeleteallPortIPFilteringRule(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_service_port_ipfiltering_delete_all(self):
#         url_request = self.url + "/api/v1/service/portIpFiltering/deletes"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.post(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 6.1.1
# class GetFirewallInformation(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_security_firewall_get(self):
#         url_request = self.url + "/api/v1/security/firewall"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 6.1.3
# class GetIPv4Firewall(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_security_firewall_ipv4_get(self):
#         url_request = self.url + "/api/v1/security/firewall/ipv4"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)
#
#
# # 6.1.7
# class GetAlertSetting(unittest.TestCase):
#     def setUp(self):
#         self.url = url
#         password_base64 = Helper.Helper_common.base64encode(pass_word)
#         url_login = url + "/api/v1/gateway/users/login"
#         data = {
#             "userName": user,
#             "password": password_base64
#         }
#         res_login = requests.post(url=url_login, json=data)
#         self.assertEqual(res_login.status_code, 200,
#                          "API login doesn't return status code 200 when calling API with valid username/password")
#         self.token = json.loads(res_login.text)["accessToken"]
#
#     def test_security_firewall_alert_get(self):
#         url_request = self.url + "/api/v1/security/firewall/alert"
#         headers = {
#             "content-type": "application/json",
#             "content-language": "en",
#             "access-token": self.token
#         }
#         res = requests.get(url=url_request, headers=headers)
#         self.assertEqual(res.status_code, 200)









# main function
if __name__ == '__main__':
    print("wait 2 mintues for DUT after Flashing image")
    time.sleep(120)
    HTMLTestRunner.main()
