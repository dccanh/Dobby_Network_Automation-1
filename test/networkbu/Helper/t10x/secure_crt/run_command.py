#$language = "python"
#$interface = "1.0"
import os
import sys
sys.path.append('../../../')
import time
import re


T10x_Prompt = "HUMAX_T10X:~#"
web_dir = "/opt/humax/rego/www/"

command = crt.Arguments.GetArg(0)
file_name = crt.Arguments.GetArg(1)
file_path = web_dir + file_name

cmd_str = str(command + " > " + file_path)


def send_command(cmd):
    if not in_RG_console():
        login_console()
    crt.Screen.Clear()
    crt.Screen.Send(cmd + '\r')
    crt.Sleep(1000)
    end()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def login_console():
    US      = "root"
    PW      = "pw!0001"

    crt.Screen.Send('\r')
    crt.Sleep(1000)
    crt.Screen.Send(US + '\r')
    crt.Sleep(1000)
    crt.Screen.Send(PW + '\r')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end():
    os.system("taskkill /f /im SecureCRT.exe")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def in_RG_console():
    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(T10x_Prompt, 1) == True):
        return True
    else:
        return False



send_command(cmd_str)

