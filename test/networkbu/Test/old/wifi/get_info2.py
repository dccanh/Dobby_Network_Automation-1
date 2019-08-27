#$language = "python"
#$interface = "1.0"
import os
import sys
sys.path.append('../')
import ConfigParser

CM_Prompt   = "CM/NonVol> "
LG_Prompt   = "login:"
PW_Prompt   = "Password:"


MIN_COLUMNS         = 1
MAX_COLUMNS         = crt.Screen.Columns
MIN_ROW             = 1
MAX_ROW             = crt.Screen.Rows


cmd_user_pw = '/non-vol/userif/http_user'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    crt.Sleep(500)
    save_config("USER_INFO", "user", str(get_user()))
    save_config("USER_INFO", "pw", str(get_user_pw()))
    end()


def get_user():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_user_pw + '\r')

    if (crt.Screen.WaitForString('\'\n', 1) == True):
        cur_row = crt.Screen.CurrentRow

    user = crt.Screen.Get(4, MIN_ROW, 5, MAX_COLUMNS)
    user = str(user).strip().split('ID=')[1].split(',')[0].strip("\'")
    return user

def get_user_pw():
    crt.Screen.Clear()
    crt.Screen.Send('\r')
    crt.Screen.Send(cmd_user_pw + '\r')

    if (crt.Screen.WaitForString('\'\n', 1) == True):
        cur_row = crt.Screen.CurrentRow
    info = crt.Screen.Get(4, MIN_ROW, 5, MAX_COLUMNS)
    pw = str(info).strip().split('password=')[1].strip("\'")
    return pw
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