import argparse
import os
import subprocess
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def connect_wifi_profile(wifi_profile):
    print("Connecting...")

    cmd = "netsh wlan connect name=\"" + wifi_profile + "\""
    log = subprocess.check_output(cmd)

    if (log.find("Connection request was completed successfully") != -1):
        print("Connected the wifi: \"" + wifi_profile + "\"")

        return True
    else:
        print("Connect the wifi:" + wifi_profile + " FAIL! Please check again!!!")

        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def remove_wifi_profile(wifi_profile):
    print("Removing the profile...")

    existed_profiles = get_wifi_profiles()

    cmd = "netsh wlan delete profile name=\"" + wifi_profile + "\""
    os.system(cmd)

    if not find_wifi_profile_in_list(wifi_profile, get_wifi_profiles()):
        print("Remove the existed profile successfully!")

        return True
    else:
        print("Something's wrong when removing the existed profile. Exit!!!")

        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_wifi_profile(wifi_profile):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print("Adding the profile...")

    wifi_profile_file = wifi_profile
    wifi_profile = str(os.path.splitext(os.path.basename(wifi_profile))[0])

    if os.path.exists(wifi_profile_file):
        print("Found the wifi profile file here.")
    else:
        print("Finding the wifi profile file in current directory: \"" + script_dir + "\"")
        wifi_profile_file = script_dir + "\\" +  wifi_profile + ".xml"

        if not os.path.exists(wifi_profile_file):
            print(wifi_profile_file + " not exist. Please check again!!!")

            return False

    print("Found a wifi profile: \"" + wifi_profile_file + "\"")

    cmd = "netsh wlan add profile filename=\"" + wifi_profile_file + "\""
    os.system(cmd)

    if find_wifi_profile_in_list(str(wifi_profile), str(get_wifi_profiles())):
        print("The profile added successfully!")

        return True
    else:
        print("Something's wrong when adding the profile!!!")

        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def disconnect_wifi():
    print("Disconnecting...")

    cmd = "netsh wlan disconnect"
    log = subprocess.check_output(cmd)

    if (log.find("Disconnection request was completed successfully for interface") != -1):
        print("Disconnected wifi successfully!")

        return True
    else:
        # print("Something's wrong when disconnecting wifi! Please check again!!!")

        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_wifi_profile_in_list(wifi_profile, list):
    if list.find(wifi_profile) > 0:

        return True
    else:

        return  False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_wifi_profiles():
    cmd = "netsh wlan show profile"
    profiles = subprocess.check_output(cmd)

    return profiles

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def connect_HVNWifi():
    profile = "HVNWifi"
    disconnect_wifi()
    remove_wifi_profile(profile)
    add_wifi_profile(profile)
    connect_wifi_profile(profile)
