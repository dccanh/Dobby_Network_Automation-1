#$language = "python"
#$interface = "1.0"

import ConfigParser
import os
import sys

config = ConfigParser.RawConfigParser()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serial_consoles_main():
    BAUD_RATE = get_config("SERIAL", "BAUD_RATE")
    RG_PORT = get_config("SERIAL", "RG_PORT").upper()
    CM_PORT = get_config("SERIAL", "CM_PORT").upper()
    # crt.Dialog.MessageBox(CM_PORT + " | " + RG_PORT)

    if (RG_PORT == "") or (CM_PORT == ""):
        crt.Dialog.MessageBox("Not found RG/CM port in the config file.\n\nPLEASE CHECK AGAIN!!!")
        return
    else:
        RG_SESSION = "/SERIAL " + RG_PORT +  " /BAUD " + BAUD_RATE
        CM_SESSION = "/SERIAL " + CM_PORT +  " /BAUD " + BAUD_RATE
        # crt.Session.Connect("/s " + COM_PORT)
        # crt.Session.Connect("/s " + CM_PORT + " /s " + RG_PORT)
        # crt.Session.Disconnect()
        crt.Session.ConnectInTab(RG_SESSION)
        crt.Session.ConnectInTab(CM_SESSION)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_config(section, option):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = str(os.path.join(script_dir, "..", "..", "config", "config.ini"))

    if not os.path.exists(config_path):
        return

    config.read(config_path)

    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

serial_consoles_main()
