import argparse
import os
import shutil
import subprocess
import sys

from utils.common.common import *
from utils.common.ip_addr import *
from utils.common.tftp_server import *

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-cm','--cm_port', help='The COM port of CM console', required=False)
parser.add_argument('-ip','--gw_ip', help='The IP address of the DUT gateway', required=True)
parser.add_argument('-rg','--rg_port', help='The COM port of RG console', required=False)
parser.add_argument('-url','--image_url', help='The URL of firmware image', required=False)
parser.add_argument('-user','--login', help='(Optional) The login information to download the firmware image with format: \"user:password\"', required=False)
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))
firmware_file = script_dir + "\\fw_images.zip"
binaries_dir = script_dir + "\\binaries"
utils_dir = script_dir + "\\utils"

SecureCRT_file = "C:\\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.exe"
TFTPd64_file = "C:\\Program Files\\Tftpd64\\tftpd64.exe"
Seven_Zip_file = "C:\\Program Files\\7-Zip\\7z.exe"

BAUD_RATE = 115200
READY_SEC = 120
PC_IP = ""

RG_COM_PORT = str(args.rg_port)
if (RG_COM_PORT == "None"):
    RG_COM_PORT = "COM5"
    print("RG_COM_PORT not be input. Using the default RG_COM_PORT.")
RG_COM_PORT = RG_COM_PORT.upper()

CM_COM_PORT = str(args.cm_port)
if (CM_COM_PORT == "None"):
    CM_COM_PORT = "COM6"
    print("CM_COM_PORT not be input. Using the default CM_COM_PORT.")
CM_COM_PORT = CM_COM_PORT.upper()

# GW_IP = "192.168.0.1"
GW_IP = str(args.gw_ip)

user = str(args.login)
URL_images = str(args.image_url)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_main():
    global PC_IP

    write_confg()
    print("\n*****************************************************************")
    print("script_dir: " + script_dir)
    print("binaries_dir: " + binaries_dir)
    print("utils_dir: " + utils_dir)

    rg_inf = get_RG_interface(GW_IP)

    print("GW_IP: " + GW_IP)
    print("RG_COM_PORT: " + RG_COM_PORT)
    print("CM_COM_PORT: " + CM_COM_PORT)

    if check_precondition():
        if get_firmware(user, URL_images):
            if extract_firmware():
                kill_processes()
                enable_cm_console()
                PC_IP = set_static_IP(rg_inf, GW_IP)
                print("PC_IP: " + PC_IP)
                save_config("COMMON", 'PC_IP', PC_IP)
                if configure_TFTP_server(PC_IP, binaries_dir, TFTPd64_file):
                    if start_TFTP(TFTPd64_file):
                        flash_firmware()
                        kill_processes()
                        print("Ready to run Automation test after " + str(READY_SEC) + " seconds...")
                        print("Done.")
                    restore_TFTP_server_config(TFTPd64_file)
                set_DHCP_IP(rg_inf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def check_precondition():
    print("\n*****************************************************************")
    print("Checking some applications need to install...")
    if not os.path.exists(SecureCRT_file):
        print(SecureCRT_file + " not exist. Exit!!!")
        return False

    if not os.path.exists(TFTPd64_file):
        print(TFTPd64_file + " not exist. Exit!!!")
        return False

    if not os.path.exists(Seven_Zip_file):
        print(Seven_Zip_file + " not exist. Exit!!!")
        return False

    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extract_firmware():
    print("\n*****************************************************************")
    print("Checking the downloaded firmware images: " + firmware_file)
    if not os.path.exists(firmware_file):
        print("The firmwares not exist. Exit!!!")
        return False

    if os.path.exists(binaries_dir):
        shutil.rmtree(binaries_dir)
    os.mkdir(binaries_dir)

    print("Extracting the downloaded firmware images to: "+ binaries_dir)
    cmd = str("\""+ Seven_Zip_file + "\"" + " x " + firmware_file + " -o" + binaries_dir + " -aoa")
    if (os.system(cmd) != 0):
        print("Something wrong when extract the downloaded firmware images. Exit!!!")
        return False

    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def flash_firmware():
    print("\n*****************************************************************")
    print("Flashing firmware images...")
    flash_fw_script = utils_dir + "/secure_crt/cm/flash_fw_silent.py"
    cmd = str("\""+ SecureCRT_file + "\"" + " /ARG " + binaries_dir + "/ /ARG " + GW_IP + " /ARG " + PC_IP
            + " /SCRIPT " + flash_fw_script + " /SERIAL " + CM_COM_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def enable_cm_console():
    print("\n*****************************************************************")
    print("Enabling CM console if disabled...")
    enable_cm_script = utils_dir + "/secure_crt/rg/common.py"
    cmd = str("\""+ SecureCRT_file + "\"" + " /SCRIPT " + enable_cm_script + " /SERIAL " + RG_COM_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def write_confg():
    save_config("COMMON", 'script_dir', script_dir)
    save_config("COMMON", 'firmware_file', firmware_file)
    save_config("COMMON", 'binaries_dir', binaries_dir)
    save_config("COMMON", 'utils_dir', utils_dir)
    save_config("COMMON", "CM_COM_PORT", CM_COM_PORT)
    save_config("COMMON", "RG_COM_PORT", RG_COM_PORT)
    save_config("COMMON", "GW_IP", GW_IP)
    save_config("COMMON", "user", user)
    save_config("COMMON", "URL_images", URL_images)
    save_config("COMMON", "BAUD_RATE", BAUD_RATE)
    save_config("COMMON", "READY_SEC", READY_SEC)

start_main()
