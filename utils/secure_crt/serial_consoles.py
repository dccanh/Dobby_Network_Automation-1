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
    if (crt.Arguments.Count < 1):
        BAUD_RATE = get_config("SERIAL", "BAUD_RATE")
        RG_PORT = get_config("SERIAL", "RG_PORT").upper()
        CM_PORT = get_config("SERIAL", "CM_PORT").upper()

        COM_PORT = [RG_PORT, CM_PORT]
        # crt.Dialog.MessageBox(CM_PORT + " | " + RG_PORT)

        if (RG_PORT == "") or (CM_PORT == ""):
            crt.Dialog.MessageBox("Not found RG/CM port in the config file.\n\nPLEASE CHECK AGAIN!!!")
            return
        else:
            for i in range(0,len(COM_PORT)):
                # crt.Dialog.MessageBox(str(COM_PORT[port]))
                crt.Session.ConnectInTab("/SERIAL " + str(COM_PORT[i]) +  " /BAUD " + BAUD_RATE)
            # crt.Session.Connect("/s " + COM_PORT)
            # crt.Session.Connect("/s " + CM_PORT + " /s " + RG_PORT)
            # crt.Session.Disconnect()
    else:
        # server_ip = "172.16.0.14"
        server_ip = str(crt.Arguments.GetArg(0))
        # cpe_ip = "10.10.10.241"
        cpe_ip = str(crt.Arguments.GetArg(1))
        username = str(crt.Arguments.GetArg(2))
        password = str(crt.Arguments.GetArg(3))

        if connect_server(server_ip, username, password):
            time.sleep(1)
            enable_serial_consoles(cpe_ip)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_config(section, option):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = str(os.path.join(script_dir, "..", "..", "config", "config.ini"))

    if not os.path.exists(config_path):
        return

    config = ConfigParser.RawConfigParser()
    config.read(config_path)

    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

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

serial_consoles_main()
