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
cmd_kill_process = 'killall udpsvd'
cmd_precondition = 'udpsvd -c 2 -E 192.168.0.1 69 /sbin/tftpd -c /var/tftpboot &'
cmd_ifconfig = "ifconfig br0  > /var/tftpboot/url.txt"
cmd_user_pw = 'dumpmdm | grep -i -e "SupportUserName" -e "<SupportPassword>"  > /var/tftpboot/account.txt'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    login_rg_console()
    # Kill Process
    crt.Screen.Clear()
    crt.Screen.Send(cmd_kill_process + '\r')
    crt.Sleep(1000)
    #Precondition
    crt.Screen.Clear()
    crt.Screen.Send(cmd_precondition + '\r')
    crt.Sleep(1000)
    # Get URL
    crt.Screen.Clear()
    crt.Screen.Send(cmd_ifconfig + '\r')
    crt.Sleep(1000)
    # Get account information
    crt.Screen.Clear()
    crt.Screen.Send(cmd_user_pw + '\r')
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