from tkinter import Tk, Frame, BOTH, Label, filedialog, constants, messagebox
from tkinter import *
import configparser, os, datetime
import webbrowser
from PIL import ImageTk, Image
from Helper.t10x.ls_path import *
import threading
import signal
import glob, subprocess
from winreg import *
from Helper.t10x.common import get_newest_artifact_name, download_artifact
def download_destination_path():
    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    return Downloads
download_path = download_destination_path()

def get_config(config_path, section, option):
    if not os.path.exists(config_path):
        print("The config file not exist. Exit!!!")
        return
    config = configparser.RawConfigParser()
    config.read(config_path)
    if config.has_option(str(section).upper(), option):
        return config.get(str(section).upper(), option)
    else:
        return

new_firmware = get_newest_artifact_name()
print(new_firmware)
# a = download_artifact(new_firmware, download_path)
# print(a)
if get_config(config_path, 'GENERAL', 'firmware_version') != new_firmware:
    os.system('python OTA.py')
else:
    os.system('python Jenkins_simulator_v6.py')

