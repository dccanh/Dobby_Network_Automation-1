from tkinter import Tk, Frame, BOTH, Label, filedialog, constants, messagebox
from tkinter import *
import configparser, os, datetime
import webbrowser
from PIL import ImageTk, Image
from Test.T10x.Non_Function import *
import threading
import signal
import glob, subprocess
from winreg import *



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

def new_version():
    return 'Automation ver 2.0'

new_firmware = new_version()


if get_config(config_path, 'GENERAL', 'firmware_version') != new_firmware:
    os.system('python OTA.py')
else:
    os.system('python Jenkins_simulator_v6.py')

