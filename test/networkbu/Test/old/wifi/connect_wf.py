import argparse
import os
import subprocess
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def connect_wifi_profile(wifi_profile):
    print("Connecting...")

    cmd = "netsh wlan connect name=\"" + wifi_profile + "\""
    log = subprocess.check_output(cmd)

    if (str(log).find("Connection request was completed successfully") != -1):
        print("Connected the wifi: \"" + wifi_profile + "\"")

        return True
    else:
        print("Connect the wifi:" + wifi_profile + " FAIL! Please check again!!!")

        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def connect_HVNWifi():
    profile = "HVNWifi"
    connect_wifi_profile(profile)

connect_HVNWifi()
