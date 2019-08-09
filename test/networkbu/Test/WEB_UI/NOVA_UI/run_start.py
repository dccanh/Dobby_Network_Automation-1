import os
import sys
sys.path.append('../../../')
import configparser
import time
import subprocess
from path import root_dir
config_path = os.path.join(root_dir, "Config", "ifconfig.txt")

'''
********** HOW TO RUN ***********
Command: python run_start.py model rg_port cm_port

Example: python run_start.py HGA COM5 COM6

Write act port to file ifconfig.txt
'''


def save_config(config_path, section, option, value):

    config = configparser.RawConfigParser()
    config.read(config_path)

    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())

    config.set(str(section).upper(), str(option), str(value))

    with open(config_path, 'r+') as config_file:
        config.write(config_file)

def get_config(config_path, section, option):
    if not os.path.exists(config_path):
        print("The config file not exist. Exit!!!")
        return

    config = configparser.RawConfigParser()
    config.read(config_path)

    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

def run_start(model, rg, cm, mode):
    if model.upper() in ["HGA20R", "HGA"]:
        os.system("taskkill /f /im SecureCRT.exe")
        os.system(
            '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./check_in_RG_console.py /SERIAL ' + str(
                rg.upper()) + ' /BAUD 115200')
        config = configparser.ConfigParser()
        config.read_file(open(config_path, 'r'))
        RG_is_enable = config.get("COMMON", 'RG_is_enable')
        print(RG_is_enable)
        count = 0
        while RG_is_enable == "false":
            enable_RG_console()
            os.system(
                '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./check_in_RG_console.py /SERIAL ' + str(
                    rg.upper()) + ' /BAUD 115200')
            config = configparser.ConfigParser()
            config.read_file(open(config_path, 'r'))
            RG_is_enable = config.get("COMMON", 'RG_is_enable')
            print(RG_is_enable)
            if ((count == 2) and (str(RG_is_enable).lower() == "false")):
                os.system('echo "Can not enable RG console"')
                exit(0)
                break
            count += 1
        # f = open(config_path, 'w+')
        # f.write('')
        # f.close()
        try:
            subprocess.check_output('TASKLIST | FINDSTR /I "SecureCRT.exe"', shell=True)
            os.system("taskkill /f /im SecureCRT.exe")
        except subprocess.CalledProcessError:
            # print("SecureCRT was off. Run now.")
            pass
        save_config(config_path, 'PORT', 'Model', model.upper())
        save_config(config_path, 'PORT', 'RG_Port', rg.upper())
        save_config(config_path, 'PORT', 'CM_Port', cm.upper())

        if (str(mode) == "login_info"):
            os.system(
                    '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./get_info_hga20r.py /SERIAL ' + str(rg.upper()) + ' /BAUD 115200')
            time.sleep(1)
            os.system('python write_text.py')
            f = open('account.txt', 'r')
            t = f.read()
            save_config(config_path, 'USER_INFO', 'user', t.split('<SupportUserName>')[1].split('</SupportUserName>')[0])
            save_config(config_path, 'USER_INFO', 'pw', t.split('<SupportPassword>')[1].split('</SupportPassword>')[0])
            f.close()
            # #
            f = open('url.txt', 'r')
            t = f.read()
            save_config(config_path, 'IFCONFIG', 'ipv4', t.split('inet addr:')[1].split('Bcast:')[0])
            save_config(config_path, 'IFCONFIG', 'ipv6', t.split('inet6 addr: ')[1].split('Scope:Link')[0].split('/')[0])
            if 'Scope:Global' in t:
                save_config(config_path, 'IFCONFIG', 'ipv6_global', t.split('inet6 addr: ')[1].split('Scope:Global')[0].split('/')[0])
            else:
                save_config(config_path, 'IFCONFIG', 'ipv6_global', 'unknown')
            f.close()
            time.sleep(1)
            os.system('del url.txt')
            os.system('del account.txt')
        elif ((str(mode) == "reboot") or (str(mode) == "restore_defaults")):
            os.system('"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe"' + ' /ARG ' + str(mode) + ' /SCRIPT ./get_info_hga20r.py /SERIAL ' + str(rg.upper()) + ' /BAUD 115200')
            time.sleep(3)
            # print("reboot")
    elif model.upper() in ["HGJ310", "HGJ", "HGJ310-BR", "HGJ310BR"]:
        if (str(mode) == "login_info"):
            f = open(config_path, 'w+')
            f.write('')
            f.close()
            try:
                subprocess.check_output('TASKLIST | FINDSTR /I "SecureCRT.exe"', shell=True)
                os.system("taskkill /f /im SecureCRT.exe")
            except subprocess.CalledProcessError:
                print("SecureCRT was off. Run now.")

            config = configparser.ConfigParser()
            # config['PORT'] = {}
            config['PORT']['Model'] = model.upper()
            config['PORT']['RG_Port'] = rg.upper()
            config['PORT']['CM_Port'] = cm.upper()

            with open(config_path, 'w') as configfile:
                config.write(configfile)
            time.sleep(1)

            os.system(
                '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./get_info_hgj310_1.py /SERIAL ' + str(
                    rg.upper()) + ' /BAUD 115200')
            time.sleep(1)
            os.system(
                '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./get_info_hgj310_2.py /SERIAL ' + str(
                    cm.upper()) + ' /BAUD 115200')
        elif ((str(mode) == "reboot") or (str(mode) == "restore_defaults")):
            pass
            # print("reboot")

def enable_RG_console():
    SecureCRT_file = "C:\\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.exe"
    test_script = os.path.join(os.path.dirname(os.path.realpath(__file__)), "serial_console.py")
    server_ip = "172.16.0.15"
    config_path = os.path.join(root_dir, "Config", "config.txt")
    cpe_ip = get_config(config_path, "COMMON", "cpe_ip")
    user = "nltuan"
    pw = "nltuan_humax@!"

    cmd = str("\""+ SecureCRT_file + "\"" + " /ARG " + server_ip + " /ARG " + cpe_ip + " /ARG " + user + " /ARG " + pw + " /SCRIPT " + test_script)
    os.system(cmd)

if __name__ == '__main__':
    run_start(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
