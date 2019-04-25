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
parser.add_argument('-cm','--cm_port', help='The COM port of CM console. Ex: COM5', required=False)
parser.add_argument('-ip','--gw_ip', help='The IP address of the DUT gateway. Ex: 192.168.0.1', required=False)
parser.add_argument('-rg','--rg_port', help='The COM port of RG console. Ex: COM6', required=False)
parser.add_argument('-url','--image_url', help='The direct URL link of firmware image. Ex: http://abc.xyz/fw_images.zip', required=False)
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

RG_PORT = str(args.rg_port).upper()
if (RG_PORT == "NONE"):
    print("RG_PORT not be input. Using the default RG_PORT from the config file.")
    RG_PORT = str(get_config("SERIAL", "RG_PORT"))
    if (RG_PORT == "") or (RG_PORT == "None"):
        print("RG_PORT not be configured in the config file. Please check again. Exit!!!\n")
        parser.print_help()
        sys.exit()

CM_PORT = str(args.cm_port).upper()
if (CM_PORT == "NONE"):
    print("CM_PORT not be input. Using the default CM_PORT from the config file.")
    CM_PORT = str(get_config("SERIAL", "CM_PORT"))
    if (CM_PORT == "") or (CM_PORT == "None"):
        print("CM_PORT not be configured in the config file. Please check again. Exit!!!\n")
        parser.print_help()
        sys.exit()

# GW_IP = "192.168.0.1"
GW_IP = str(args.gw_ip)
if (GW_IP == "None"):
    print("GW_IP not be input. Using the default GW_IP from the config file.")
    GW_IP = str(get_config("IP", "GW_IP"))
    if (GW_IP == "") or (GW_IP == "None"):
        print("GW_IP not be configured in the config file. Please check again. Exit!!!\n")
        parser.print_help()
        sys.exit()

user = str(args.login)
if (user == "None"):
    user = "admin:password"

URL_images = str(args.image_url)
if (URL_images == "None"):
    print("URL_images not be input. Using the default URL.")
    URL_images = "http://arti.humaxdigital.com:8081/artifactory/Vina_automation/Network/hga20r_fw_images.zip"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_main():
    global PC_IP

    write_confg()
    print("\n*****************************************************************")
    print("script_dir: " + script_dir)
    print("binaries_dir: " + binaries_dir)
    print("utils_dir: " + utils_dir)

    rg_inf = get_RG_interface(GW_IP)
    save_config("IP", 'rg_inf', rg_inf)

    origin_IP_config = get_IP_config(rg_inf)
    save_config("IP", 'origin_IP_config', origin_IP_config)
    print("origin_IP_config: " + str(origin_IP_config))

    origin_TFTP_config = get_origin_TFTP_server_config(TFTPd64_file)
    save_config("COMMON", 'origin_TFTP_config', origin_TFTP_config)
    print("origin_TFTP_config: " + str(origin_TFTP_config))

    PC_IP = set_static_IP(rg_inf, GW_IP)
    save_config("IP", 'PC_IP', PC_IP)

    print("GW_IP: " + GW_IP)
    print("PC_IP: " + PC_IP)
    print("RG_PORT: " + RG_PORT)
    print("CM_PORT: " + CM_PORT)

    if check_precondition():
        if configure_TFTP_server(PC_IP, binaries_dir, TFTPd64_file):
            if get_firmware(user, URL_images):
                if extract_firmware():
                    kill_processes()
                    enable_cm_console()
                    if start_TFTP(TFTPd64_file):
                        flash_firmware()
                        kill_processes()
                        restore_TFTP_server_config(TFTPd64_file)
                        print("Ready to run Automation test after " + str(READY_SEC) + " seconds...")
    restore_IP_config(rg_inf)
    print("... DONE ...")

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
            + " /SCRIPT " + flash_fw_script + " /SERIAL " + CM_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def enable_cm_console():
    print("\n*****************************************************************")
    print("Enabling CM console if disabled...")
    enable_cm_script = utils_dir + "/secure_crt/rg/common.py"
    cmd = str("\""+ SecureCRT_file + "\"" + " /SCRIPT " + enable_cm_script + " /SERIAL " + RG_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def write_confg():
    save_config("COMMON", 'script_dir', script_dir)
    save_config("COMMON", 'firmware_file', firmware_file)
    save_config("COMMON", 'binaries_dir', binaries_dir)
    save_config("COMMON", 'utils_dir', utils_dir)
    save_config("SERIAL", "CM_PORT", CM_PORT)
    save_config("SERIAL", "RG_PORT", RG_PORT)
    save_config("SERIAL", "BAUD_RATE", BAUD_RATE)
    save_config("IP", "GW_IP", GW_IP)
    save_config("AUTHENTICATION", "url_images", URL_images)
    save_config("AUTHENTICATION", "user", user)
    save_config("COMMON", "READY_SEC", READY_SEC)

start_main()
