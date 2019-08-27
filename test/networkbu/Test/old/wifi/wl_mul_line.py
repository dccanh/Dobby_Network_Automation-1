#$language = "python"
#$interface = "1.0"
import os
import sys
sys.path.append('../')
import re
import ConfigParser


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

result = []
config = ConfigParser.RawConfigParser()
config.read('../Config/config.txt')
cm_list = []
for i in range(len(config.items('COMMAND'))):
    cm_list.append(config.get('COMMAND', 'cmd'+str(i)))
config_path = "../Config/cmd_value.txt"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    login_rg_console()

    for i in range(len(cm_list)):
        crt.Screen.Clear()
        crt.Screen.Send('\r')
        crt.Screen.Send(cm_list[i] + '\r')

        if (crt.Screen.WaitForString('anything', 1) == True):
            cur_row = crt.Screen.CurrentRow
            cur_col = crt.Screen.CurrentColumn
        crt.Sleep(500)
        data = crt.Screen.Get(3, MIN_ROW, MAX_ROW, MAX_COLUMNS)
        data = data.strip()
        crt.Sleep(3000)
        result.append(data)

    f = open(config_path, 'w')
    f.write('')
    f.close()

    for j in range(len(result)):
        a = str(result[j].split('[')[0].strip())
        while '  ' in a:
            a = a.replace('  ', ' ')
        save_config('COMMAND', str(option_key(cm_list)[j]), a)

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
def save_config(section, option, value):

    config = ConfigParser.RawConfigParser()
    config.read(config_path)

    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())

    config.set(str(section).upper(), str(option), str(value))

    with open(config_path, 'r+') as config_file:
        config.write(config_file)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def option_key(cm_list):
    key = []
    for a in cm_list:
        x = ''
        for i in a:
            if not i.isalnum():
                if i in '[]-\\':
                    x += '\\' + i
                else:
                    x += i
        import re
        line = re.sub('[' + x + ']', '_', a)
        key.append(line)
    option = []
    for i in key:
        option.append('cm_' + i)
    return option


def end():
    os.system("taskkill /f /im SecureCRT.exe")

main()