#$language = "python"
#$interface = "1.0"

import os
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def serial_consoles_main():
    COM_PORT_5 = "serial-com5"
    COM_PORT_6 = "serial-com6"

    # crt.Dialog.MessageBox("/s " + COM_PORT_5)
    # crt.Session.Connect("/s " + COM_PORT_5)
    crt.Session.Connect("/s " + COM_PORT_5 + " /s " + COM_PORT_6)

serial_consoles_main()
