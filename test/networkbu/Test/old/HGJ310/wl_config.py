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
    a = wl_bss()

    b = wl_radio()

    c = nvram_radio()

    d = mdm_getpv()

    crt.Screen.Clear()

    f = open('../Config/config.txt', 'r+')
    for line in open('../Config/config.txt'):
        if line.startswith('value ='):
            line_new = line.replace(line, 'value = '
                                    + str(a) + ' '
                                    + str(b) + ' '
                                    + str(c) + ' '
                                    + str(d))
            f.write(line_new)
        else:
            f.write(line)
    f.close()


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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def wl_bss():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send('wl -i wl0 bss' + '\r')

    if (crt.Screen.WaitForString('anything', 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn


    crt.Sleep(500)
    data = crt.Screen.Get(3, MIN_ROW, 3, MAX_COLUMNS)
    data = data.strip()
    return data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def wl_radio():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send('wl -i wl0 radio' + '\r')

    # if (crt.Screen.WaitForString(IPv4_Prompt, 1) == True):
    #     cur_row = crt.Screen.CurrentRow
    #     cur_col = crt.Screen.CurrentColumn
    if (crt.Screen.WaitForString('anything', 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn
    crt.Sleep(500)
    data = crt.Screen.Get(3, MIN_ROW, 3, MAX_COLUMNS)

    data = data.strip()
    return data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def nvram_radio():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send('nvram get wl0_radio' + '\r')

    # if (crt.Screen.WaitForString(IPv4_Prompt, 1) == True):
    #     cur_row = crt.Screen.CurrentRow
    #     cur_col = crt.Screen.CurrentColumn
    if (crt.Screen.WaitForString('anything', 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn
    crt.Sleep(500)
    data = crt.Screen.Get(3, MIN_ROW, 3, MAX_COLUMNS)

    data = data.strip()
    return data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def mdm_getpv():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send('mdm getpv Device.WiFi.Radio.1.Enable' + '\r')
    if (crt.Screen.WaitForString('anything', 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn
    # if (crt.Screen.WaitForString(IPv4_Prompt, 1) == True):
    #     cur_row = crt.Screen.CurrentRow
    #     cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    data = crt.Screen.Get(3, MIN_ROW, 3, MAX_COLUMNS)
    data = data.strip().split()[1]

    return data

def end():
    os.system("taskkill /f /im SecureCRT.exe")

main()