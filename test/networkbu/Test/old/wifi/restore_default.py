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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv4_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')
	
    if (crt.Screen.WaitForString(IPv4_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    data = crt.Screen.Get(cur_row, MIN_ROW, cur_row+1, MAX_COLUMNS)


    # id = data.find("Bcast:")
    # data = data[:id]
    # id = data.find("inet addr:")
    # data = data[id + 10:]

    data = data.split('inet addr:')[1].split('Bcast:')[0]
    data = data.strip()
    return data


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv6_Link_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv6_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    data = crt.Screen.Get(cur_row, MIN_ROW, cur_row +1, MAX_COLUMNS)
    # id = data.find("Scope:Global")
    #
    # if (id == -1):
    #     id = data.find("Scope:Link")
    # else:
    #     data = data[id + 12:]
    #     id = data.find("Scope:Link")
    #
    # data = data[:id - 4]
    # id = data.find("inet6 addr:")
    # data = data[id + 11:]
    data = data.split('inet6 addr:')[1].split('Scope:')[0]
    data = data.strip().split('/')[0]

    return data


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv6_Global_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv6_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    data = crt.Screen.Get(cur_row, MIN_ROW, cur_row + 1, MAX_COLUMNS)
    id = data.find("Scope:Global")

    if (id != -1):
        data = data[:id - 4]
        id = data.find("inet6 addr:")
        data = data[id + 11:]
        data = data.strip()
    else:
        data = str()

    return data


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_user_pw():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_user_pw + '\r')

    if (crt.Screen.WaitForString(User_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
    user = crt.Screen.Get(cur_row, MIN_ROW, cur_row, MAX_COLUMNS)
    user = user.strip()
    user = user.split('<SupportUserName>')[1].split('</SupportUserName>')[0]

    if (crt.Screen.WaitForString(Pw_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
    password = crt.Screen.Get(cur_row , MIN_ROW, cur_row +1 , MAX_COLUMNS)
    password = password.strip()
    password = password.split('<SupportPassword>')[1].split('</SupportPassword>')[0]

    return user, password


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end():
    os.system("taskkill /f /im SecureCRT.exe")

main()