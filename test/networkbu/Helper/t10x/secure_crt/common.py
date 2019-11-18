from Helper.t10x.common import get_config
from Helper.t10x.ls_path import *


serial = get_config("CONSOLE", "serial_port")
baud_rate = get_config("CONSOLE", "baud_rate")
SecureCRT_file = "C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe"
script_path = crt_run_command


def run_cmd(cmd, filename):
    cmd = str("\""+ SecureCRT_file + "\"" + " /ARG \"" + cmd + "\" /ARG \"" + filename + "\" /SCRIPT \"" + script_path + "\" /SERIAL "+serial+" /BAUD "+baud_rate)
    os.popen(cmd)
# cmd = "capitest get Device.Users.User.2. leaf"
# run_cmd(cmd, "user.txt")




