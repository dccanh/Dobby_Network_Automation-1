#$language = "python"
#$interface = "1.0"

import os
import sys

RG_Prompt           = "RG]#"
IPv4_Prompt         = "inet addr:"
IPv6_Prompt         = "inet6 addr:"

MIN_COLUMNS         = 1
MAX_COLUMNS         = crt.Screen.Columns
MIN_ROW             = 1
MAX_ROW             = crt.Screen.Rows

cmd_ifconfig = "ifconfig br0"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    if (is_RG_console() == True):
        data = "IPv4_addr: " + get_IPv4_addr() \
                + " | IPv6_Link_addr: " + get_IPv6_Link_addr() \
                + " | IPv6_Global_addr: " + get_IPv6_Global_addr()

        crt.Screen.Send(str(data))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv4_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv4_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    data = crt.Screen.Get(cur_row, MIN_ROW, cur_row, MAX_COLUMNS)
    id = data.find("Bcast:")
    data = data[:id]
    id = data.find("inet addr:")
    data = data[id + 10:]
    data = data.strip()

    return data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_IPv6_Link_addr():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_ifconfig + '\r')

    if (crt.Screen.WaitForString(IPv6_Prompt, 1) == True):
        cur_row = crt.Screen.CurrentRow
        cur_col = crt.Screen.CurrentColumn

    crt.Sleep(500)
    data = crt.Screen.Get(cur_row, MIN_ROW, cur_row + 1, MAX_COLUMNS)
    id = data.find("Scope:Global")

    if (id == -1):
        id = data.find("Scope:Link")
    else:
        data = data[id + 12:]
        id = data.find("Scope:Link")

    data = data[:id - 4]
    id = data.find("inet6 addr:")
    data = data[id + 11:]
    data = data.strip()

    return data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def is_RG_console():
    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(RG_Prompt, 1) == True):
        return True
    else:
        return False

main()
