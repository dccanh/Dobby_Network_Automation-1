import ast
import configparser
import os
import sys

from utils.common.common import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_TFTP(TFTPd64_file):
    print("\n*****************************************************************")
    print("Starting TFTP server...")
    cmd = str("start \"TFTP\" \"" + TFTPd64_file + "\"")
    if (os.system(cmd) != 0):
        print("Could not start: " + TFTPd64_file + ". Exit!!!")
        return False
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_origin_TFTP_server_config(TFTPd64_file):
    tftp_config = {}
    TFTP_installed_dir  = os.path.dirname(TFTPd64_file)
    TFTP_config_file    = TFTP_installed_dir + "\\tftpd32.ini"

    print("TFTPd64_file: " + TFTPd64_file)
    print("TFTP_config_file: " + TFTP_config_file)

    base_dir_key        = "BaseDirectory="
    local_IP_key        = "LocalIP="

    if os.path.exists(TFTP_config_file):
        with open(TFTP_config_file, 'r') as file:
            config_data = file.readlines()
            for line in range(0,len(config_data)):
                if "[TFTPD32]" in config_data[line]:
                    for i in range(line,len(config_data)):
                        if base_dir_key in config_data[i]:
                            tmp = config_data[i]
                            id = tmp.find(base_dir_key)
                            tmp = tmp[id + len(base_dir_key):]
                            tmp = tmp.strip()
                            tftp_config.update({base_dir_key.strip('='):str(tmp)})

                        if local_IP_key in config_data[i]:
                            tmp = config_data[i]
                            id = tmp.find(local_IP_key)
                            tmp = tmp[id + len(local_IP_key):]
                            tmp = tmp.strip()
                            tftp_config.update({local_IP_key.strip('='):str(tmp)})
                            break
            file.close()

    return tftp_config

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def configure_TFTP_server(PC_IP, binaries_dir, TFTPd64_file):
    TFTP_installed_dir  = os.path.dirname(TFTPd64_file)
    TFTP_config_file    = TFTP_installed_dir + "\\tftpd32.ini"

    print("TFTPd64_file: " + TFTPd64_file)
    print("TFTP_config_file: " + TFTP_config_file)
    print("binaries_dir: " + binaries_dir)
    print("PC_IP: " + PC_IP)

    base_dir_key        = "BaseDirectory="
    base_dir_config     = str(base_dir_key + binaries_dir + "\n")

    local_IP_key        = "LocalIP="
    local_IP_config     = str(local_IP_key + PC_IP + "\n")

    if os.path.exists(TFTP_config_file):
        with open(TFTP_config_file, 'r') as file:
            config_data = file.readlines()
            for line in range(0,len(config_data)):
                if "[TFTPD32]" in config_data[line]:
                    for i in range(line,len(config_data)):
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def restore_TFTP_server_config(TFTPd64_file):
    origin_TFTP_config = str(get_config("TFTP", "origin_tftp_config"))

    # Convert <str> type to <dict> type
    origin_TFTP_config = ast.literal_eval(origin_TFTP_config)

    TFTP_installed_dir  = os.path.dirname(TFTPd64_file)
    TFTP_config_file    = TFTP_installed_dir + "\\tftpd32.ini"

    base_dir_key        = "BaseDirectory="
    base_dir_config     = str(base_dir_key) + origin_TFTP_config[str(base_dir_key.strip('='))] + "\n"

    local_IP_key        = "LocalIP="
    local_IP_config     = str(local_IP_key) + origin_TFTP_config[str(local_IP_key.strip('='))] + "\n"

    if os.path.exists(TFTP_config_file):
        with open(TFTP_config_file, 'r') as file:
            config_data = file.readlines()
            for line in range(0,len(config_data)):
                if "[TFTPD32]" in config_data[line]:
                    for i in range(line,len(config_data)):
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
