import argparse
import os
import subprocess
import sys

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-p','--profile', help='The name of wifi profile', required=True)
parser.add_argument('-u','--path', help='The path of the wifi profile', required=False)
args = parser.parse_args()

script_dir = os.path.dirname(os.path.realpath(__file__))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _tmp_main():
    # WIFI_PROFILE = "HVN_NW_Test_2G"
    WIFI_PROFILE = args.profile

    print("Wifi profile: \"" + WIFI_PROFILE + "\"")

    if find_wifi_profile_in_list(WIFI_PROFILE, get_wifi_profiles()):
        remove_wifi_profile(WIFI_PROFILE)

    if add_wifi_profile(WIFI_PROFILE):
        disconnect_wifi()
        connect_wifi_profile(WIFI_PROFILE)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def connect_wifi_profile(wifi_profile):
    cmd = "netsh wlan connect name=\"" + wifi_profile + "\""
    log = subprocess.check_output(cmd)
    # print(log)

    if (log.find("Connection request was completed successfully") != -1):
        print("Connected the wifi: " + wifi_profile)

        return True
    else:
        print("Connect the wifi:" + wifi_profile + " FAIL! Please check again!!!")

        return False

    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def remove_wifi_profile(wifi_profile):
    existed_profiles = get_wifi_profiles()
    # print(existed_profiles)

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
    wifi_profile_file = args.path

    if wifi_profile_file == None:
        wifi_profile_file = script_dir + "\\" +  wifi_profile + ".xml"

        if not os.path.exists(wifi_profile_file):
            print(wifi_profile_file + " not exist. Please check again!!!")
            return False

    print("Wifi profile: \"" + wifi_profile_file + "\"")

    cmd = "netsh wlan add profile filename=\"" + wifi_profile_file + "\""
    os.system(cmd)

    if find_wifi_profile_in_list(wifi_profile, get_wifi_profiles()):
        print("The profile added successfully!")

        return True
    else:
        print("Something's wrong when adding the profile!!!")

        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def disconnect_wifi():
    cmd = "netsh wlan disconnect"
    log = subprocess.check_output(cmd)
    # print(log)

    if (log.find("Disconnection request was completed successfully for interface") != -1):
        print("Disconnect wifi successfully!")

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
    # print(profiles)

    return profiles

_tmp_main()
