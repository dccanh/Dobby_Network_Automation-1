import os
import sys
import configparser
import time
import subprocess
''' 
********** HOW TO RUN ***********
Command: python run_start.py rg_port cm_port

Example: python run_start.py COM5 COM6

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


def run_start(rg, cm):
    config_path = '../Config/ifconfig.txt'
    f = open(config_path, 'w+')
    f.write('')
    f.close()
    try:
        subprocess.check_output('TASKLIST | FINDSTR /I "SecureCRT.exe"', shell=True)
        os.system("taskkill /f /im SecureCRT.exe")
    except subprocess.CalledProcessError:
        print("SecureCRT was off. Run now.")

    save_config(config_path, 'PORT', 'RG_Port', rg.upper())
    save_config(config_path, 'PORT', 'CM_Port', cm.upper())

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


if __name__ == '__main__':
    run_start(sys.argv[1], sys.argv[2])