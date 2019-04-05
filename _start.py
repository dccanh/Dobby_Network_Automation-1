import argparse
import imp
import os
import psutil
import shutil
import sys

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-cm','--cm_port', help='The URL of firmware image', required=False)
parser.add_argument('-ip','--pc_ip', help='The IP address of the PC', required=True)
parser.add_argument('-rg','--rg_port', help='The URL of firmware image', required=False)
parser.add_argument('-url','--image_url', help='The URL of firmware image', required=False)
parser.add_argument('-user','--login', help='(Optional) The login information to download the firmware image with format: \"user:password\"', required=False)
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))
firmware_file = script_dir + "\\fw_images.zip"
firmware_dir = script_dir + "\\fw_binaries"

SecureCRT = "C:\\Program Files\\VanDyke Software\\SecureCRT\\SecureCRT.exe"
TFTPd64 = "C:\\Program Files\\Tftpd64\\tftpd64.exe"
Seven_Zip = "C:\\Program Files\\7-Zip\\7z.exe"

RG_IP = "192.168.0.102"
BAUD_RATE = 115200
READY_SEC = 120

RG_COM_PORT = str(args.rg_port).upper()
if RG_COM_PORT:
    RG_COM_PORT = "COM5"
    print("RG_COM_PORT not be input. Using the default RG_COM_PORT: " + RG_COM_PORT)

CM_COM_PORT = str(args.cm_port).upper()
if CM_COM_PORT:
    CM_COM_PORT = "COM6"
    print("CM_COM_PORT not be input. Using the default CM_COM_PORT: " + CM_COM_PORT)

# PC_IP = "192.168.0.29"
PC_IP = str(args.pc_ip)
print("PC_IP: " + PC_IP)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_main():
    print("\n*****************************************************************")

    print("script_dir: " + script_dir)

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
    if not os.path.exists(SecureCRT):
        print(SecureCRT + " not exist. Exit!!!")
        return False

    if not os.path.exists(TFTPd64):
        print(TFTPd64 + " not exist. Exit!!!")
        return False

    if not os.path.exists(Seven_Zip):
        print(Seven_Zip + " not exist. Exit!!!")
        return False

    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_firmware():
    print("\n*****************************************************************")
    user = str(args.login)
    URL_images = str(args.image_url)

    if URL_images:
        print("URL_images not be input. Using the default URL.")
        URL_images = "http://arti.humaxdigital.com:8081/artifactory/Vina_automation/Network/hga20r_fw_images.zip"
    print("URL_images: " + URL_images)

    if user:
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

    if os.path.exists(firmware_dir):
        shutil.rmtree(firmware_dir)
    os.mkdir(firmware_dir)

    print("Extracting the downloaded firmware images to: "+ firmware_dir)
    cmd = str("\""+ Seven_Zip + "\"" + " x " + firmware_file + " -o" + firmware_dir + " -aoa")
    if (os.system(cmd) != 0):
        print("Something wrong when extract the downloaded firmware images. Exit!!!")
        return False

    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def flash_firmware():
    print("\n*****************************************************************")
    print("Flashing firmware images...")
    flash_fw_script = script_dir + "\\flash_fw_silent.py"
    cmd = str("\""+ SecureCRT + "\"" + " /ARG " + firmware_dir + "\\ /ARG " + RG_IP + " /ARG " + PC_IP
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
    enable_cm_script = script_dir + "\\enable_cm_console.py"
    cmd = str("\""+ SecureCRT + "\"" + " /SCRIPT " + enable_cm_script + " /SERIAL " + RG_COM_PORT + " /BAUD " + str(BAUD_RATE))
    os.system(cmd)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_TFTP():
    print("\n*****************************************************************")
    print("Starting TFTP server...")
    cmd = str("start \"TFTP\" \"" + TFTPd64 + "\"")
    if (os.system(cmd) != 0):
        print("Could not start: " + TFTPd64 + ". Exit!!!")
        return False
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def configure_TFTP_server():
    TFTP_installed_dir  = os.path.dirname(TFTPd64)
    TFTP_config_file    = TFTP_installed_dir + "\\tftpd32.ini"

    base_dir_key        = "BaseDirectory="
    base_dir_config     = str(base_dir_key + firmware_dir + "\n")

    local_IP_key        = "LocalIP="
    local_IP_config     = str(local_IP_key + PC_IP + "\n")

    if os.path.exists(TFTP_config_file):
        with open(TFTP_config_file, 'r') as file:
            config_data = file.readlines()
            for line in xrange(0,len(config_data)):
                if "[TFTPD32]" in config_data[line]:
                    for i in xrange(line,len(config_data)):
                        if base_dir_key in config_data[i]:
                            base_dir_id = i
                        if local_IP_key in config_data[i]:
                            local_IP_id = i
                            break

            config_data[base_dir_id] = base_dir_config
            config_data[local_IP_id] = local_IP_config
            file.close()

        with open(TFTP_config_file, 'w') as file:
            file.writelines(config_data)
            file.close()

        return True
    else:
        print(TFTP_config_file + " not exist. Exit!!!")
        return False

start_main()
