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

config_path = './Config/t10x/config.txt'
testcase_data_path = './Image/testcase_data.txt'
icon_path = './Image/icon_2_VZm_icon.ico'


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


def save_config(config_path, section, option, value):
    config = configparser.RawConfigParser()
    config.read(config_path)
    if not config.has_section(str(section).upper()):
        config.add_section(str(section).upper())
    config.set(str(section).upper(), str(option), str(value))
    with open(config_path, 'w') as config_file:
        config.write(config_file)


root = Tk()
root.title(f"NETWORK AUTOMATION TOOL")
root.iconbitmap(icon_path)


titleLabel = Label(root, text=" FIRMWARE UPDATE", font="Verdana 13")
titleLabel.pack(anchor=CENTER)


old_firmware = get_config(config_path, 'GENERAL', 'firmware_version')


def thread_run():
    os.system('python Jenkins_simulator_v6.py')

def thread_destroy():
    root.destroy()


def create_file():
    support_install_path = os.path.join(download_path, 'auto_generate_support_install_version.txt')
    if os.path.exists(support_install_path):
        os.remove(support_install_path)
    with open(support_install_path, 'w+') as f:
        f.write(root_dir)


def buttonNO():
    thread_2 = threading.Thread(target=thread_destroy)
    thread_2.start()
    thread_1 = threading.Thread(target=thread_run)
    thread_1.start()


from Helper.t10x.common import download_artifact, get_newest_artifact_name


new_firmware = get_newest_artifact_name()


def buttonYES():
    create_file()

    check_downloaded = download_artifact(new_firmware, download_path)
    print(f"Download is {str(check_downloaded)}: {new_firmware}")

    # Wait until download success
    download_zip_path = os.path.join(download_path, new_firmware)
    print(f"Download path file is: {download_zip_path}")

    time.sleep(3)
    count = 0
    while not os.path.exists(download_zip_path):
        time.sleep(1)
        count += 1
        if count == 10:
            messagebox.showerror('Error', 'Download new firmware failure.')
            thread_2 = threading.Thread(target=thread_destroy)
            thread_2.start()
            thread_1 = threading.Thread(target=thread_run)
            thread_1.start()
            break

    # Download successfully
    print("Download successfully")
    time.sleep(1)

    # Unzip file
    extra_to_file = download_path + "\generate"
    import zipfile
    with zipfile.ZipFile(download_zip_path, "r") as zip_ref:
        zip_ref.extractall(extra_to_file)

    print('Unzip file successfully')
    time.sleep(1)

    if os.path.exists(extra_to_file):
        os.chdir(extra_to_file)
        os.system(f'python setup_ota.py')

    thread_2 = threading.Thread(target=thread_destroy)
    thread_2.start()
    thread_1 = threading.Thread(target=thread_run)
    thread_1.start()
    os.chdir(root_dir)

    # support_install_path = os.path.join(download_path, 'auto_tool_support_install_version.txt')
    if os.path.exists(extra_to_file):
        os.system(f"RD /S /Q {extra_to_file}")
    save_config(config_path, 'GENERAL', 'firmware_version', new_firmware)


labelNewFirm = Label(root, text=f"Your old firmware is {old_firmware}. "
                            f"\nNew firmware {new_firmware} available."
                            f"\n Do you want to update version? "
                            f"\n After download new firmware patch. Please extra file then Run setup file.")
labelNewFirm.place(x=10, y=60)

_yesBtn = Button(root, text="Yes", command=buttonYES, height=1, width=10, borderwidth=2, compound=LEFT)
_yesBtn.place(x=120, y=150)

_noBtn = Button(root, text="No", command=buttonNO, height=1, width=10, borderwidth=2, compound=LEFT)
_noBtn.place(x=220, y=150)


root.geometry(f"410x200+500+100")
root.resizable(0, 0)
root.mainloop()
