#$language = "python"
#$interface = "1.0"
import os
import sys
import ConfigParser
sys.path.append('../')


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

cmd_ifconfig = "ifconfig br-lan"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    login_rg_console()

    save_config('IFCONFIG', 'ipv4', str(get_IPv4_addr()))
    save_config('IFCONFIG', 'ipv6', str(get_IPv6_Link_addr()))
    save_config('IFCONFIG', 'ipv6_global', str(get_IPv6_Global_addr()))
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
    data = data.split('inet6 addr: ')[1].split('Scope:Link')[0]
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
    data = data.split('inet6 addr: ')[1].split('Scope:Global')[0]
    data = data.strip().split('/')[0]

    return data


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def get_user_pw():
#     crt.Screen.Clear()
#     crt.Screen.Send('\r')
#     crt.Screen.Send(cmd_user_pw + '\r')
#
#     if (crt.Screen.WaitForString(User_Prompt, 1) == True):
#         cur_row = crt.Screen.CurrentRow
#     user = crt.Screen.Get(cur_row, MIN_ROW, cur_row, MAX_COLUMNS)
#     user = user.strip()
#     user = user.split('<SupportUserName>')[1].split('</SupportUserName>')[0]
#
#     if (crt.Screen.WaitForString(Pw_Prompt, 1) == True):
#         cur_row = crt.Screen.CurrentRow
#     password = crt.Screen.Get(cur_row , MIN_ROW, cur_row +1 , MAX_COLUMNS)
#     password = password.strip()
#     password = password.split('<SupportPassword>')[1].split('</SupportPassword>')[0]
#
#     return user, password


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def save_config(section, option, value):
    config_path = "../Config/ifconfig.txt"
    config = ConfigParser.RawConfigParser()
    config.read(config_path)

    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())

    config.set(str(section).upper(), str(option), str(value))

    with open(config_path, 'r+') as config_file:
        config.write(config_file)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end():
    os.system("taskkill /f /im SecureCRT.exe")

main()