# client

1. **Pre-condition:**
    - Tftpd64: https://bitbucket.org/phjounin/tftpd64/downloads/tftpd64.464.zip
    - SecureCRT 7.3

2. **Need to configure:**
    - **_start.bat:**
        + **Setup IP address:** RG_IP, PC_IP, COM_PORT, BAUD_RATE

            Ex:

                RG_IP       = "192.168.0.11"    // IP address of DUT

                PC_IP       = "192.168.0.29"    // IP address of TPTP server

                COM_PORT    = COM6             // COM port connect to serial on board

                BAUD_RATE   = 115200           // Baud rate | Default: 115200

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

            Ex:

                Z:\_Share\TFTP\_start.bat
