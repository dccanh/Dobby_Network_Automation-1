#$language = "python"
#$interface = "1.0"

import os
import sys

RG_Prompt   = "RG]#"
LG_Prompt   = "login:"
PW_Prompt   = "Password:"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cm_console_main():
    enable_cm_console()
    end()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def login_rg_console():
    US      = "root"
    PW      = "humax@!0416"

    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(LG_Prompt, 1) == True):
        crt.Screen.Send(US + '\r')
    if (crt.Screen.WaitForString(PW_Prompt, 1) == True):
        crt.Screen.Send(PW + '\r')

    if not in_RG_console():
        return False
    else:
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def enable_cm_console():
    CM_CMD      = "snmpset -v2c -c private 172.31.255.45 .1.3.6.1.4.1.4413.2.2.2.1.9.1.2.1.0 int 2"

    if not in_RG_console():
        if not login_rg_console():
            return False

    crt.Screen.Send('\r')
    crt.Screen.Send(CM_CMD + '\r')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def in_RG_console():
    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString(RG_Prompt, 1) == True):
        return True
    else:
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end():
    os.system("taskkill /f /im SecureCRT.exe")

cm_console_main()
