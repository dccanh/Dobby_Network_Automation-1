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

t10x_crt_path = os.path.join(root_dir, "Helper", "t10x", "secure_crt")
crt_common = os.path.join(t10x_crt_path, "common.py")
crt_run_command = os.path.join(t10x_crt_path, "run_command.py")

t10x_config_path = os.path.join(root_dir, "Helper", "t10x", "config")
captcha_path = os.path.join(t10x_config_path, "captcha.py")
expected_path = os.path.join(t10x_config_path, "data_expected.py")
elements_path = os.path.join(t10x_config_path, "elements.py")
read_config_path = os.path.join(t10x_config_path, "read_config.py")
write_config_path = os.path.join(t10x_config_path, "write_config.py")
gg_credential_path = os.path.join(t10x_config_path, "dn8c_cred.json")

test_t10x_path = os.path.join(root_dir, "Test", "t10x")
after_test_path = os.path.join(test_t10x_path, "After_test.py")
before_test_path = os.path.join(test_t10x_path, "Before_test.py")
pilot_path = os.path.join(test_t10x_path, "Pilot.py")




