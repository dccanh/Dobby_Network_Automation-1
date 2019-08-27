#$language = "python"
#$interface = "1.0"

import os
import sys
import ConfigParser
sys.path.append('../../../')
import time
import re
# config.read_file(open(r'../'))

from path import root_dir
config_path = os.path.join(root_dir, "Config", "ifconfig.txt")

mode = str(crt.Arguments.GetArg(0))

def get_config(config_path, section, option):
    if not os.path.exists(config_path):
        print("The config file not exist. Exit!!!")
        return

    config = ConfigParser.RawConfigParser()
    config.read(config_path)

    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

RG_Prompt   = "RG]#"
LG_Prompt   = "login:"
PW_Prompt   = "Password:"

RG_Prompt           = "RG]#"
# IPv4_Prompt         = "inet addr:"
IPv4_Prompt="Bcast:"
# IPv6_Prompt         = "inet6 addr:"
IPv6_Prompt= "Scope:"
User_Prompt         = "</SupportUserName>"
Pw_Prompt           = "</SupportPassword>"

MIN_COLUMNS         = 1
MAX_COLUMNS         = crt.Screen.Columns
MIN_ROW             = 1
MAX_ROW             = crt.Screen.Rows
gw_ip = get_config(config_path, "IFCONFIG", "ipv4")
cmd_kill_process = "killall udpsvd"
cmd_precondition = "udpsvd -c 2 -E " + str(gw_ip) + " 69 /sbin/tftpd -c /var/tftpboot &"
cmd_ifconfig = "ifconfig br0  > /var/tftpboot/url.txt"
cmd_user_pw = "dumpmdm | grep -i -e \"SupportUserName\" -e \"<SupportPassword>\"  > /var/tftpboot/account.txt"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_login_info():
    login_rg_console()
    # Kill Process
    crt.Screen.Clear()
    crt.Screen.Send(cmd_kill_process + '\r')
    crt.Sleep(1000)
    #Precondition
    crt.Screen.Clear()
    crt.Screen.Send(cmd_precondition + '\r')
    crt.Sleep(1000)
    # Get URL
    crt.Screen.Clear()
    crt.Screen.Send(cmd_ifconfig + '\r')
    crt.Sleep(1000)
    # Get account information
    crt.Screen.Clear()
    crt.Screen.Send(cmd_user_pw + '\r')
    end()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def reboot_DUT():
    login_rg_console()
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send('reboot')
    crt.Screen.Send('\r')
    end()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def restore_defaults():
    login_rg_console()
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send('restoredefault')
    crt.Screen.Send('\r')
    end()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def login_rg_console():
    US      = "root"
    PW      = "humax@!0416"

    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(LG_Prompt, 1) == True):
        crt.Screen.Send(US + '\r')
    if (crt.Screen.WaitForString(PW_Prompt, 1) == True):
        crt.Screen.Send(PW + '\r')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end():
    os.system("taskkill /f /im SecureCRT.exe")

if (mode == "login_info"):
    get_login_info()
elif (mode == "reboot"):
    reboot_DUT()
elif (mode == "restore_defaults"):
    restore_defaults()
