# client

1. **Pre-condition:**
    - Tftpd64: https://bitbucket.org/phjounin/tftpd64/downloads/tftpd64.464.zip
    - SecureCRT 7.3
    - 7-zip
    - Python2.7.5 with installed libraries: psutil, shutil, argparse, imp

2. **Need to configure:**
    - **_start.bat:**
        + **Input URL_images as command parameter**

            Ex:

                _start.bat "http://test.com/file.zip"

        + **Setup IP address:** RG_IP, PC_IP, COM_PORT, BAUD_RATE

            Ex:

                RG_IP       = "192.168.0.11"    // IP address of DUT

                PC_IP       = "192.168.0.29"    // IP address of TPTP server

                COM_PORT    = COM6             // COM port connect to serial on board

                BAUD_RATE   = 115200           // Baud rate | Default: 115200

    - **_start.py:**
        + **Input cm_port, pc_ip, rg_port, image_url, login as command parameters**
            - *_start.py -h* to show help for more details

    - **TFTPd64:**
        + **tftpd32.ini:**
            - LocalIP=*<TFTP_server_IP>*

            Ex:

                LocalIP=192.168.0.29        // PC_IP

            - BaseDirectory=*<Saved_images_directory>*

            Ex:

                BaseDirectory=Z:\_Share\TFTP

3. **How to run:**
    - **Step 01:** Kill all applications/processes using COM ports related to device.
    - **Step 02:**
        + **Method 1:**
            - Run directly by double-click _start.bat from its directory.
        + **Method 2:**
            - Open Command Prompt (cmd)
            - Run command:
                    <Path_to_file>\_start.bat
                    <Path_to_file>\_start.py

            Ex:

                Z:\_Share\TFTP\_start.bat
                Z:\_Share\source_code\automation\client\_start.py -ip 192.168.0.29
                Z:\_Share\source_code\automation\client\_start.py -ip 192.168.0.29 -cm COM6 -rg COM5
                Z:\_Share\source_code\automation\client\_start.py -ip 192.168.0.29 -cm COM6 -rg COM5 --image_url http://arti.humaxdigital.com:8081/artifactory/Vina_automation/Network/hga20r_fw_images.zip"
                Z:\_Share\source_code\automation\client\_start.py -ip 192.168.0.29 -cm COM6 -rg COM5 --image_url http://arti.humaxdigital.com:8081/artifactory/Vina_automation/Network/hga20r_fw_images.zip" -user "user:password"
