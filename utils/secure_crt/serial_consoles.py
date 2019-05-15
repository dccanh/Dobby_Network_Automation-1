#$language = "python"
#$interface = "1.0"

import ConfigParser
import os
import sys

config = ConfigParser.RawConfigParser()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serial_consoles_main():
    CM_PORT = "serial-" + str(get_config("SERIAL", "CM_PORT")).lower()
    RG_PORT = "serial-" + str(get_config("SERIAL", "RG_PORT")).lower()
    # crt.Dialog.MessageBox(CM_PORT + " | " + RG_PORT)

    # crt.Session.Connect("/s " + COM_PORT)
    crt.Session.Connect("/s " + CM_PORT + " /s " + RG_PORT)

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
