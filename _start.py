import argparse
import imp
import os
import psutil
import shutil
import sys

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-cm','--cm_port', help='The COM port of CM console', required=False)
parser.add_argument('-ip','--pc_ip', help='The IP address of the PC', required=True)
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

RG_IP = "192.168.0.102"
BAUD_RATE = 115200
READY_SEC = 120

RG_COM_PORT = str(args.rg_port).upper()
if (RG_COM_PORT == "None"):
    RG_COM_PORT = "COM5"
    print("RG_COM_PORT not be input. Using the default RG_COM_PORT.")
RG_COM_PORT.upper()

CM_COM_PORT = str(args.cm_port).upper()
if (CM_COM_PORT == "None"):
    CM_COM_PORT = "COM6"
    print("CM_COM_PORT not be input. Using the default CM_COM_PORT.")
CM_COM_PORT.upper()

# PC_IP = "192.168.0.29"
PC_IP = str(args.pc_ip)
print("PC_IP: " + PC_IP)
print("RG_COM_PORT: " + RG_COM_PORT)
print("CM_COM_PORT: " + CM_COM_PORT)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_main():
    print("\n*****************************************************************")

    print("script_dir: " + script_dir)
    print("binaries_dir: " + binaries_dir)
    print("utils_dir: " + utils_dir)

    if check_precondition():
        if get_firmware():
            if extract_firmware():
                kill_processes()
                enable_cm_console()
                if configure_TFTP_server():
                    if start_TFTP():
                        flash_firmware()
                        kill_processes()
                        print("Ready to run Automation test after " + str(READY_SEC) + " seconds...")
                        print("Done.")

                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

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
def get_firmware():
    print("\n*****************************************************************")
    user = str(args.login)
    URL_images = str(args.image_url)

    if (URL_images == "None"):
        print("URL_images not be input. Using the default URL.")
        URL_images = "http://arti.humaxdigital.com:8081/artifactory/Vina_automation/Network/hga20r_fw_images.zip"
    print("URL_images: " + URL_images)

    if (user == "None"):
        print("Login information not be input. Using the default login information.")
        user = "admin:password"

    if os.path.exists(firmware_file):
        print("Found an existed firmwares: " + firmware_file)
        os.remove(firmware_file)
        print("Removed the existed firmwares before downloading.")

    print("Getting firmware images from server: " + URL_images)
    cmd = "curl --retry 3 -u " + user + " " + URL_images + " -o " + firmware_file
    if (os.system(cmd) != 0):
        print("Download firmware images FAIL. Exit!!!")
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
    flash_fw_script = utils_dir + "\\flash_fw_silent.py"
    cmd = str("\""+ SecureCRT_file + "\"" + " /ARG " + binaries_dir + "\\ /ARG " + RG_IP + " /ARG " + PC_IP
            + " /SCRIPT " + flash_fw_script + " /SERIAL " + CM_COM_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def kill_processes():
    print("\n*****************************************************************")
    ps = psutil.pids()

    print("Need to kill some processes...")
    for x in ps:
        if psutil.Process(x).name() == "SecureCRT.exe":
            psutil.Process(x).terminate()
        if psutil.Process(x).name() == "tftpd64.exe":
            psutil.Process(x).terminate()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def enable_cm_console():
    print("\n*****************************************************************")
    print("Enabling CM console if disabled...")
    enable_cm_script = utils_dir + "\\cm_console.py"
    cmd = str("\""+ SecureCRT_file + "\"" + " /SCRIPT " + enable_cm_script + " /SERIAL " + RG_COM_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_TFTP():
    print("\n*****************************************************************")
    print("Starting TFTP server...")
    cmd = str("start \"TFTP\" \"" + TFTPd64_file + "\"")
    if (os.system(cmd) != 0):
        print("Could not start: " + TFTPd64_file + ". Exit!!!")
        return False
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def configure_TFTP_server():
    tftp_util_script = utils_dir + "\\tftp_server.py"
    cmd = str(tftp_util_script + " --bin_dir " + binaries_dir + " --pc_ip " + PC_IP\
             + " --tftpd64_file \"" + TFTPd64_file + "\"")

    if (os.system(cmd) != 0):
        print("Could not configure TFTP server. Exit!!!")
        return False
    return True

start_main()
