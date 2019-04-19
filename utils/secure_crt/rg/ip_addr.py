#$language = "python"
#$interface = "1.0"

import os
import sys

RG_Prompt           = "RG]#"
LG_Prompt           = "login:"
PW_Prompt           = "Password:"
IPv4_Prompt         = "inet addr:"
IPv6_Prompt         = "inet6 addr:"

MIN_COLUMNS         = 1
MAX_COLUMNS         = crt.Screen.Columns
MIN_ROW             = 1
MAX_ROW             = crt.Screen.Rows

cmd_ifconfig = "ifconfig br0"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def utils_ifconfig_main():
    if not in_RG_console():
        login_rg_console()
    ip_addr = "IPv4_addr: " + get_IPv4_addr() \
            + " | IPv6_Link_addr: " + get_IPv6_Link_addr() \
            + " | IPv6_Global_addr: " + get_IPv6_Global_addr()

    crt.Screen.Send(str(ip_addr))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def login_rg_console():
    US      = "root"
    PW      = "humax@!0416"

    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(LG_Prompt) == True):
        crt.Screen.Send(US + '\r')
    if (crt.Screen.WaitForString(PW_Prompt) == True):
        crt.Screen.Send(PW + '\r')

    if not in_RG_console():
        return False
    else:
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv4_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv4_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    IPv4_addr = crt.Screen.Get(cur_row, MIN_ROW, cur_row, MAX_COLUMNS)
    id = IPv4_addr.find("Bcast:")
    IPv4_addr = IPv4_addr[:id]
    id = IPv4_addr.find("inet addr:")
    IPv4_addr = IPv4_addr[id + 10:]
    IPv4_addr = IPv4_addr.strip()

    return IPv4_addr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv6_Link_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv6_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    IPv6_Link_addr = crt.Screen.Get(cur_row, MIN_ROW, cur_row + 1, MAX_COLUMNS)
    id = IPv6_Link_addr.find("Scope:Global")

    if (id == -1):
        id = IPv6_Link_addr.find("Scope:Link")
    else:
        IPv6_Link_addr = IPv6_Link_addr[id + 12:]
        id = IPv6_Link_addr.find("Scope:Link")

    IPv6_Link_addr = IPv6_Link_addr[:id - 4]
    id = IPv6_Link_addr.find("inet6 addr:")
    IPv6_Link_addr = IPv6_Link_addr[id + 11:]
    IPv6_Link_addr = IPv6_Link_addr.strip()

    return IPv6_Link_addr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv6_Global_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv6_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    IPv6_Global_addr = crt.Screen.Get(cur_row, MIN_ROW, cur_row + 1, MAX_COLUMNS)
    id = IPv6_Global_addr.find("Scope:Global")

    if (id != -1):
        IPv6_Global_addr = IPv6_Global_addr[:id - 4]
        id = IPv6_Global_addr.find("inet6 addr:")
        IPv6_Global_addr = IPv6_Global_addr[id + 11:]
        IPv6_Global_addr = IPv6_Global_addr.strip()
    else:
        IPv6_Global_addr = str()

    return IPv6_Global_addr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def in_RG_console():
    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(RG_Prompt, 1) == True):
        return True
    else:
        return False

utils_ifconfig_main()
