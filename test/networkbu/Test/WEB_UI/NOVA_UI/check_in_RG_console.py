#$language = "python"
#$interface = "1.0"
import os
import sys
import ConfigParser
sys.path.append('../../../')
import time
import re
from path import root_dir
config_path = os.path.join(root_dir, "Config", "ifconfig.txt")
# config.read_file(open(r'../'))


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


def main():
    in_RG_console()
    end()


def in_RG_console():
   crt.Screen.Send('\r')
   if (crt.Screen.WaitForString(RG_Prompt, 1) == True):
       save_config('COMMON', 'RG_is_enable', 'true')
   else:
       crt.Screen.Clear()
       crt.Screen.Send('\r')
       if (crt.Screen.WaitForString(LG_Prompt, 1) == True):
           save_config('COMMON', 'RG_is_enable', 'true')
       else:
           save_config('COMMON', 'RG_is_enable', 'false')


def save_config(section, option, value):

    config = ConfigParser.RawConfigParser()
    config.read(config_path)

    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())

    config.set(str(section).upper(), str(option), str(value))

    with open(config_path, 'r+') as config_file:
        config.write(config_file)


def end():
    os.system("taskkill /f /im SecureCRT.exe")


main()
