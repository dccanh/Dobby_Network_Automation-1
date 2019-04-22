import configparser
import os
import psutil

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def save_config(section, option, value):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = script_dir + "/../../config.ini"

    config = configparser.RawConfigParser()
    config.read(config_path)

    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())

    config.set(str(section).upper(), str(option), str(value))

    with open(config_path, 'w') as config_file:
        config.write(config_file)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_config(section, option):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = script_dir + "/../../config.ini"

    config = configparser.RawConfigParser()
    config.read(config_path)

    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_firmware(user, URL_images):
    if (user == "None"):
        user = str(get_config("AUTHENTICATION", "user"))

    if (URL_images == "None"):
        URL_images = str(get_config("AUTHENTICATION", "url_images"))

    print("URL_images: " + URL_images)
    firmware_file = str(get_config("common", "firmware_file"))
    if os.path.exists(firmware_file):
        print("Found an existed firmwares: " + firmware_file)
        os.remove(firmware_file)
        print("Removed the existed firmwares before downloading.")

    print("Getting firmware images from server: " + URL_images)
    cmd = "curl --retry 3 -u " + user + " " + URL_images + " -o " + firmware_file
    if (os.system(cmd) != 0):
        print("Download firmware images FAIL. Exit!!!")
        return False

    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def kill_processes():
    ps = psutil.pids()

    print("Need to kill some processes...")
    for x in ps:
        if psutil.Process(x).name() == "SecureCRT.exe":
            psutil.Process(x).terminate()
        if psutil.Process(x).name() == "tftpd64.exe":
            psutil.Process(x).terminate()
