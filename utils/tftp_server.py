import argparse
import os
import sys

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-b','--bin_dir', help='The directory contains firmware binaries', required=True)
parser.add_argument('-ip','--pc_ip', help='The IP address of the PC', required=True)
parser.add_argument('-u','--tftpd64_file', help='The installed directory of TFTP server', required=True)
args = parser.parse_args()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tftp_server_main():
    configure_TFTP_server()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def configure_TFTP_server():
    TFTPD64_file = str(args.tftpd64_file)
    binaries_dir = str(args.bin_dir)
    PC_IP = str(args.pc_ip)

    print("TFTPD64_file: " + TFTPD64_file)
    print("binaries_dir: " + binaries_dir)
    print("PC_IP: " + TFTPD64_file)

    TFTP_installed_dir  = os.path.dirname(TFTPD64_file)
    TFTP_config_file    = TFTP_installed_dir + "\\tftpd32.ini"

    base_dir_key        = "BaseDirectory="
    base_dir_config     = str(base_dir_key + binaries_dir + "\n")

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

tftp_server_main()
