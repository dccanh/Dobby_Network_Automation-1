#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(os.path.dirname(script_dir), "..")

config_dir = os.path.join(root_dir, "Config", "t10x")
config_path = os.path.join(config_dir, "config.txt")
captcha_dict_path = os.path.join(config_dir, "captcha.dict")
wifi_2g_path = os.path.join(config_dir, "wifi2g.xml")
wifi_5g_path = os.path.join(config_dir, "wifi5g.xml")

driver_path = os.path.join(root_dir, "Driver", "chromedriver.exe")
driver_firefox_path = os.path.join(root_dir, "Driver", "geckodriver.exe")
driver_edge_path = os.path.join(root_dir, "Driver", "MicrosoftWebDriver.exe")
driver_safari_path = os.path.join(root_dir, "Driver", "SafariDriver.safariextz")

t10x_crt_path = os.path.join(root_dir, "Helper", "t10x", "secure_crt")
crt_common = os.path.join(t10x_crt_path, "common.py")
crt_run_command = os.path.join(t10x_crt_path, "run_command.py")
nw_interface_path = os.path.join(root_dir, "Helper", "t10x", "nw_interface.py")

t10x_config_path = os.path.join(root_dir, "Helper", "t10x", "config")
captcha_path = os.path.join(t10x_config_path, "captcha.py")
expected_path = os.path.join(t10x_config_path, "data_expected.py")
elements_path = os.path.join(t10x_config_path, "elements.py")
read_config_path = os.path.join(t10x_config_path, "read_config.py")
write_config_path = os.path.join(t10x_config_path, "write_config.py")
gg_credential_path = os.path.join(t10x_config_path, "dn8c_cred.json")
input_data_path = os.path.join(t10x_config_path, "input_data.txt")

test_t10x_path = os.path.join(root_dir, "Test", "T10X")
after_test_path = os.path.join(test_t10x_path, "After_test.py")
before_test_path = os.path.join(test_t10x_path, "Before_test.py")
pilot_path = os.path.join(test_t10x_path, "Pilot.py")

files_path = os.path.join(root_dir, "Config", "Files")
default_wifi_2g_path = os.path.join(files_path, "Wi-Fi-We Love You So Much_2G!.xml")
wifi_default_file_path = os.path.join(files_path, "wifi_default_file.xml")
wifi_none_secure_path = os.path.join(files_path, "wifi_none_secure.xml")
firmware_4_path = os.path.join(files_path, "t10x_fullimage_4.00.12_rev11.img")
firmware_3_path = os.path.join(files_path, "t10x_fullimage_3.00.05_rev09.img")

report_offline_path = os.path.join(root_dir, "Report", "T10X", "T10x_report_automation.xlsx")
