#$language = "python"
#$interface = "1.0"
import os
import sys
sys.path.append('../')
import time
import re
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

cmd_ifconfig = "ifconfig br0"
cmd_user_pw = 'dumpmdm | grep -i -e "SupportUserName" -e "<SupportPassword>"'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    login_rg_console()
    crt.Screen.Clear()
    # crt.Screen.Send('\r')
    crt.Screen.Send('restoredefault' + '\r')
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

main()