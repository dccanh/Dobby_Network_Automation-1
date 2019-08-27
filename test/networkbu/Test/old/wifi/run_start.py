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

def run_start(rg, cm):
    try:
        subprocess.check_output('TASKLIST | FINDSTR /I "SecureCRT.exe"', shell=True)
        os.system("taskkill /f /im SecureCRT.exe")
    except subprocess.CalledProcessError:
        print("SecureCRT was off. Run now.")

    config = configparser.ConfigParser()
    config['PORT'] = {}
    config['PORT']['RG_Port'] = rg.upper()
    config['PORT']['CM_Port'] = cm.upper()

    with open('../Config/ifconfig.txt', 'w') as configfile:
        config.write(configfile)
    time.sleep(1)

    os.system(
            '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./get_info.py /SERIAL ' + str(rg.upper()) + ' /BAUD 115200')
    time.sleep(1)
    os.system(
            '"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe" /SCRIPT ./get_info2.py /SERIAL ' + str(cm.upper()) + ' /BAUD 115200')


if __name__ == '__main__':
    run_start(sys.argv[1], sys.argv[2])