import configparser
from Helper.t10x.ls_path import *

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
serial = get_config("CONSOLE", "serial_port")
baud_rate = get_config("CONSOLE", "baud_rate")
SecureCRT_file = "C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe"
script_path = crt_run_command

# Kill if SecureCRT ran
import subprocess
ls = subprocess.check_output('tasklist')
if b'SecureCRT.exe' in ls:
    os.system("taskkill /f /im SecureCRT.exe")

def run_cmd(cmd, filename):
    cmd = str("\""+ SecureCRT_file + "\"" + " /ARG \"" + cmd + "\" /ARG \"" + filename + "\" /SCRIPT \"" + script_path + "\" /SERIAL "+serial+" /BAUD "+baud_rate)
    os.popen(cmd)
# cmd = "capitest get Device.Users.User.2. leaf"
# run_cmd(cmd, "user.txt")




