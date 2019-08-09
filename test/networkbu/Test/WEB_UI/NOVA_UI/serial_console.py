#$language = "python"
#$interface = "1.0"

import ConfigParser
import os
import sys
import time

# ========== EXAMPLE TO USE THIS ==========
#   1. Use to open with SecureCRT
#        SecureCRT_file = "C:\\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.exe"
#        test_script = "Z:\\_Temp\\serial_consoles.py"
#
#        server_ip = "172.16.0.15"
#        cpe_ip = "10.10.10.126"
#        user = "nltuan"
#        pw = "nltuan_humax@!"
#
#        cmd = str("\""+ SecureCRT_file + "\"" + " /ARG " + server_ip + " /ARG " + cpe_ip + " /ARG " + user + " /ARG " + pw + " /SCRIPT " + test_script)
#        os.system(cmd)
#
#   2. Use to open in SecureCRT
#        Run this script with format argument: <server_ip> <cpe_ip> <username> <password>
#        Example: 172.16.0.15 10.10.10.126  nltuan nltuan_humax@!
#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serial_consoles_main():
    # server_ip = "172.16.0.14"
    server_ip = str(crt.Arguments.GetArg(0))
    # cpe_ip = "10.10.10.241"
    cpe_ip = str(crt.Arguments.GetArg(1))
    username = str(crt.Arguments.GetArg(2))
    password = str(crt.Arguments.GetArg(3))

    if connect_server(server_ip, username, password):
        time.sleep(1)
        enable_serial_consoles(cpe_ip)

    end()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def enable_serial_consoles(cpe_ip):
    # cmd_disable_RG_CM = "snmpset -v2c -c private 10.10.10.126 1.3.6.1.4.1.4413.2.2.2.1.9.1.2.1.0 int 0"
    cmd_enable_RG = "snmpset -v2c -c private " + str(cpe_ip) + " 1.3.6.1.4.1.4413.2.2.2.1.9.1.2.1.0 int 1"
    cmd_enable_CM = "snmpset -v2c -c private " + str(cpe_ip) + " 1.3.6.1.4.1.4413.2.2.2.1.9.1.2.1.0 int 2"

    CMD = [cmd_enable_RG, cmd_enable_CM]

    for i in range(0,len(CMD)):
            crt.Screen.Send('\r')
            crt.Screen.Send(CMD[i] + '\r')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def connect_server(server_ip, username, password):
    # crt.Session.ConnectInTab("/SSH1 " + server_ip + " /L " + username + " /PASSWORD " + password)
    errcode = 0
    try:
        crt.Session.Connect("/SSH2 /ACCEPTHOSTKEYS " + server_ip + " /L " + username + " /PASSWORD " + password, True)
    except ScriptError:
        errcode = crt.GetLastError()
    if (errcode != 0):
        return False
    else:
        return True


def end():
    os.system("taskkill /f /im SecureCRT.exe")


serial_consoles_main()
