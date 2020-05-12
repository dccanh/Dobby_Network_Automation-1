from tkinter import Tk, Frame, BOTH, Label, filedialog, constants, messagebox
from tkinter import *
import configparser, os, datetime
import webbrowser
from PIL import ImageTk, Image
from Test.T10x.Main import *
from Test.T10x.Home import *
from Test.T10x.Network import *
from Test.T10x.Wireless import *
from Test.T10x.Security import *
from Test.T10x.Advanced import *
from Test.T10x.MediaShare import *
from Test.T10x.Non_Function import *
import threading
import signal
import glob, subprocess
from Helper.t10x.common import factory_dut
os.chdir(root_dir)
try:
    import keyboard
except ModuleNotFoundError:
    os.system('pip install keyboard')
    import keyboard
try:
    import serial
except ModuleNotFoundError:
    os.system('pip install pyserial')
    import keyboard

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left', relief='solid', borderwidth=1)
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


config_path = './Config/t10x/config.txt'
testcase_data_path = './Image/testcase_data.txt'
icon_path = './Image/icon_2_VZm_icon.ico'


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


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


def delete_report_offline():
    """
    Delete content of Excel report file.
    Delete before run a section.
    """
    import openpyxl
    ls = subprocess.check_output('tasklist')
    if b'EXCEL.EXE' in ls:
        os.system("taskkill /f /im EXCEL.EXE")
    excel_file = report_offline_path
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    ws.delete_rows(6, ws.max_row)
    wb.save(excel_file)


def exit_Btn():
    exit()


def callback(url):
    webbrowser.open_new(url)


def load_database_tc(module_name):
    main_cls = module_name
    tc_name = [i[0] for i in [(name, t) for name, t in main_cls.__dict__.items() if
                              type(t).__name__ == 'function' and not name.startswith('__')]]
    test_class1_name = main_cls.__name__
    for i in range(len(tc_name)):
        if tc_name[i].startswith('test_'):
            save_config(testcase_data_path, test_class1_name, test_class1_name + str(i), tc_name[i])


load_database_tc(MAIN)
load_database_tc(HOME)
load_database_tc(NETWORK)
load_database_tc(WIRELESS)
load_database_tc(SECURITY)
load_database_tc(ADVANCED)
load_database_tc(MEDIASHARE)
load_database_tc(NON_FUNCTION)


def get_num_test_case_module():
    config = configparser.RawConfigParser()
    config.read(testcase_data_path)
    return {"Main": len(list(config.items('MAIN'))),
            "Home": len(list(config.items('HOME'))),
            "Network": len(list(config.items('NETWORK'))),
            "Wireless": len(list(config.items('WIRELESS'))),
            "Security": len(list(config.items('SECURITY'))),
            "MediaShare": len(list(config.items('MEDIASHARE'))),
            "Advanced": len(list(config.items('ADVANCED'))),
            "Non_Function": len(list(config.items('NON_FUNCTION'))),
            "All": len(list(config.items('NON_FUNCTION')))
                   + len(list(config.items('MAIN')))
                   + len(list(config.items('HOME')))
                   + len(list(config.items('NETWORK')))
                   + len(list(config.items('WIRELESS')))
                   + len(list(config.items('SECURITY')))
                   + len(list(config.items('MEDIASHARE')))
                   + len(list(config.items('ADVANCED')))
            }

def get_runtime_test_module():
    import math
    config = configparser.RawConfigParser()
    config.read(testcase_runtime_data_path)
    dict_time = dict()
    for s in config.sections():
        module_time = 0
        for i in config.items(s):
            module_time += int(i[1])
        dict_time.update({s: math.ceil(module_time/60)})
    dict_time.update({'ALL': sum(list(dict_time.values()))})
    return dict_time


def get_runtime_test_case(list_individual_tc):
    config = configparser.RawConfigParser()
    config.read(testcase_runtime_data_path)
    _indiv_total_time = 0
    print(list_individual_tc)
    if len(list_individual_tc)>0:

        for _indiv in list_individual_tc:

            for s in config.sections():
                if isinstance(_indiv, list):
                    check_tc = get_config(testcase_runtime_data_path, s, _indiv[1])
                else:
                    check_tc = get_config(testcase_runtime_data_path, s, _indiv)
                if check_tc is not None:
                    _indiv_total_time += int(check_tc)
        return round(_indiv_total_time / 60, 1)
    return 0


convert_module = {
    'MAIN': 'Main.py',
    'HOME': 'Home.py',
    'WIRELESS': 'Wireless.py',
    'NETWORK': 'Network.py',

    'MEDIASHARE': 'MediaShare.py',
    'SECURITY': 'Security.py',
    'ADVANCED': 'Advanced.py',
    'NON_FUNCTION': 'Non_Function.py',
    'ALL': ['Main.py', 'Home.py', 'Wireless.py', 'Network.py', 'MediaShare.py', 'Security.py', 'Advanced.py',
            'Non_Function.py']
}

# def new_version():
#     return 'Automation ver 2.0'
# def api_download_new_version():
#     print('Download successfully')


# if get_config(config_path, 'GENERAL', 'firmware_version') != new_version():
#     root_install = Tk()
#     root_install.geometry(f"300x200+500+100")
#     root_install.title = 'Firmware Update'
#     labelSerialNumber = Label(root_install, text="New firmware is available. \n Do you want to update version?")
#     labelSerialNumber.place(x=50, y=20)

# class Tools:
#     def __init__(self):
#         if get_config(config_path, 'GENERAL', 'firmware_version') != new_version():
#             root_install = Tk()
#             root_install.geometry(f"300x200+500+100")
#             root_install.title = 'Firmware Update'
#             labelSerialNumber = Label(root_install, text="New firmware is available. \n Do you want to update version?")
#             labelSerialNumber.place(x=50, y=20)
#             basicSettingBtn = Button(root_install, text="Yes", height=1, width=10, borderwidth=2, compound=LEFT,
#                                      command=self._ok)
#             basicSettingBtn.place(x=50, y=70)
#
#             repeaterSettingBtn = Button(root_install, text="No", height=1, width=10, borderwidth=2, compound=LEFT,
#                                         command=self._cancel)
#             repeaterSettingBtn.place(x=150, y=70)
#             root_install.mainloop()
#
#     def _ok(self):
#         # api_download_new_version()
#         download_path = download_destination_path()
#         support_install_path = os.path.join(download_path, 'auto_tool_support_install_version.txt')
#         # Create a .txt file support install new version
#         with open(support_install_path, 'w+') as f:
#             # Write network BU path
#             print(root_dir)
#             f.write(root_dir)
#     def _cancel(self):
#         test()
#
#
#
#
# def test():
root = Tk()
root.title(f"NETWORK AUTOMATION TOOL")
root.iconbitmap(icon_path)

img = Image.open('./Image/humax-vector-logo_2.png')
photo = ImageTk.PhotoImage(img)
label = Label(root, image=photo)
label.image = photo
label.place(x=2, y=0)

titleLabel = Label(root, text="    NETWORK AUTOMATION TOOL", font="Verdana 13")
titleLabel.place(x=150, y=0)

img_down = Image.open('./Image/down-icon.png')
photo_down = ImageTk.PhotoImage(img_down)
img_up = Image.open('./Image/up-icon.png')
photo_up = ImageTk.PhotoImage(img_up)
img_run = Image.open('./Image/run2.png')
photo_run = ImageTk.PhotoImage(img_run)
img_manual = Image.open('./Image/hand-click2.png')
photo_manual = ImageTk.PhotoImage(img_manual)
img_abort = Image.open('./Image/abort2.png')
photo_abort = ImageTk.PhotoImage(img_abort)
img_playing = Image.open('./Image/playing.png')
photo_playing = ImageTk.PhotoImage(img_playing)
img_setting = Image.open('./Image/setting_5.png')
photo_setting = ImageTk.PhotoImage(img_setting)
img_setting_2 = Image.open('./Image/settings_3.png')
photo_setting_2 = ImageTk.PhotoImage(img_setting_2)

img_loading = Image.open('./Image/sync.png')
photo_loading = ImageTk.PhotoImage(img_loading)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
labelFile1 = Label(root, text="Tester:")
labelFile1.place(x=30, y=40)
labelFile2 = Label(root, text="Model:")
labelFile2.place(x=30, y=90)
labelFile3 = Label(root, text="Settings:")
labelFile3.place(x=30, y=190)
labelFile4 = Label(root, text="Serial Port:")
labelFile4.place(x=30, y=140)
labelFile5 = Label(root, text="Test Suite:")
labelFile5.place(x=30, y=240)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cusStage1 = StringVar()
stage1 = Entry(root, textvariable=cusStage1)
stage1.pack()
stage1.place(x=140, y=40, height=25, width=330)


cusModel = StringVar()
choices = ['T10X']
cusModel.set(choices[0])
model = OptionMenu(root, cusModel, *choices)
model.place(x=140, y=90, height=30, width=330)
model['background'] = 'white'

FACTORY_TIME = 200

def flow_off_field(value):
    port4['state'] = value
    stage1['state'] = value
    model['state'] = value
    loopBox['state'] = value
    report_val['state'] = value

    basicSettingBtn['state'] = value
    repeaterSettingBtn['state'] = value
    runButton['state'] = value
    manualButton['state'] = value
    # abortButton['state'] = value
    basicSettingBtn['state'] = value
    repeaterSettingBtn['state'] = value
    factoryButton['state'] = value

def _basicSetting():
    flow_off_field(DISABLED)


    config = configparser.RawConfigParser()
    config.read(testcase_data_path)
    now_x = root.winfo_x()
    now_y = root.winfo_y()
    window = Toplevel(root)

    window.geometry(f"400x200+{str(now_x+50)}+{now_y+50}")
    window.resizable(0, 0)
    window.title("Basic Setting")
    window.iconbitmap(icon_path)

    frame = Frame(window, relief=RAISED)
    frame.pack(fill=BOTH, expand=True)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    labelSerialNumber = Label(window, text="Serial Number:")
    labelSerialNumber.place(x=15, y=30)

    ModuleNumber = StringVar()
    previous_number = get_config(config_path, 'GENERAL', 'serial_number')
    ModuleNumber.set(previous_number)
    number = Entry(window, textvariable=ModuleNumber)
    number.pack()
    number.place(x=115, y=30, height=25, width=265)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    labelAgging = Label(window, text="Aging Time(sec):")
    labelAgging.place(x=15, y=70)

    ModuleAging = StringVar()
    previous_AgingTime = get_config(input_data_path, 'NON_FUNCTION', 'nf_ping_time')
    ModuleAging.set(previous_AgingTime)
    _aging = Entry(window, textvariable=ModuleAging)
    _aging.pack()
    _aging.place(x=115, y=70, height=25, width=265)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    labelReportPath = Label(window, text="Local Report:")
    labelReportPath.place(x=15, y=110)

    ModulePath = StringVar()
    previous_path = get_config(config_path, 'REPORT', 'report_path')
    ModulePath.set(previous_path)
    _path = Entry(window, textvariable=ModulePath)
    _path.pack()
    _path.place(x=115, y=110, height=25, width=265)

    def _saveFolder():
        folder_path = filedialog.askdirectory()
        window.lift()
        ModulePath.set(folder_path)

    BrowBtn = Button(window, text="...", width=15, command=_saveFolder, background='white')
    BrowBtn.pack()
    BrowBtn.place(x=360, y=110, height=25, width=20)

    def _saveBtn():
        save_config(config_path, 'GENERAL', 'serial_number', number.get())
        save_config(config_path, 'REPORT', 'report_path', _path.get())
        save_config(input_data_path, 'NON_FUNCTION', 'nf_ping_time', _aging.get())
        window.destroy()

        flow_off_field(NORMAL)

    SaveBtn = Button(window, text="Save", width=15, command=_saveBtn)
    SaveBtn.pack(anchor='center', padx=5, pady=10)

    def on_closing():

        flow_off_field(NORMAL)
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()


def _repeaterSetting():
    flow_off_field(DISABLED)
    config = configparser.RawConfigParser()
    config.read(testcase_data_path)
    now_x = root.winfo_x()
    now_y = root.winfo_y()
    window = Toplevel(root)
    window.geometry(f"500x550+{str(now_x+50)}+{now_y+50}")
    window.resizable(0, 0)
    window.title("Upper Router Settings")
    window.iconbitmap(icon_path)

    frame = Frame(window, relief=RAISED)
    frame.pack(fill=BOTH, expand=True)
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = 65, 95, 125, 155, 185, 215, 300, 330, 360, 390, 420, 450

    label_MeshTitle = Label(window, text="\t\tMesh - Upper Router", font="Verdana 9")
    label_MeshTitle.place(x=15, y=10)

    label_MeshLogin = Label(window, text="WEB UI Login:")
    label_MeshLogin.place(x=15, y=40)

    label_MeshLgID = Label(window, text="\tID:")
    label_MeshLgID.place(x=15, y=c0)

    label_MeshLgPassword = Label(window, text="\tPassword:")
    label_MeshLgPassword.place(x=15, y=c1)

    label_MeshName_2g = Label(window, text="2G\tSSID:")
    label_MeshName_2g.place(x=15, y=c2)
    label_MeshPW_2g = Label(window, text="\tPassword:")
    label_MeshPW_2g.place(x=15, y=c3)

    label_MeshName_5g = Label(window, text="5G\tSSID:")
    label_MeshName_5g.place(x=15, y=c4)
    label_MeshPW_5g = Label(window, text="\tPassword:")
    label_MeshPW_5g.place(x=15, y=c5)

    label= Label(window, text="---------------------------------------------" * 2)
    label.place(x=15, y=230)

    label_PartyTitle = Label(window, text="\t\tThird Party - Upper Router", font="Verdana 9")
    label_PartyTitle.place(x=15, y=250)

    label_PartyLogin = Label(window, text="WEB UI Login:")
    label_PartyLogin.place(x=15, y=275)

    label_PartyLgID = Label(window, text="\tID:")
    label_PartyLgID.place(x=15, y=c6)

    label_PartyLgPassword = Label(window, text="\tPassword:")
    label_PartyLgPassword.place(x=15, y=c7)

    label_PartyName_2g = Label(window, text="2G\tSSID:")
    label_PartyName_2g.place(x=15, y=c8)
    label_PartyPW_2g = Label(window, text="\tPassword:")
    label_PartyPW_2g.place(x=15, y=c9)

    label_PartyName_5g = Label(window, text="5G\tSSID:")
    label_PartyName_5g.place(x=15, y=c10)
    label_PartyPW_5g = Label(window, text="\tPassword:")
    label_PartyPW_5g.place(x=15, y=c11)



    previous_meshLogin_name = get_config(input_data_path, 'REPEATER', 'user')
    previous_meshLogin_pw = get_config(input_data_path, 'REPEATER', 'pw')
    previous_mesh2g_name = get_config(input_data_path, 'REPEATER', 'repeater_name')
    previous_mesh2g_pw = get_config(input_data_path, 'REPEATER', 'repeater_pw')
    previous_mesh5g_name = get_config(input_data_path, 'REPEATER', 'repeater_name_5g')
    previous_mesh5g_pw = get_config(input_data_path, 'REPEATER', 'repeater_pw_5g')

    previous_thPartyLogin_name = get_config(input_data_path, 'REPEATER', 'third_party_login_user')
    previous_thPartyLogin_pw = get_config(input_data_path, 'REPEATER', 'third_party_login_pw')
    previous_thParty2g_name = get_config(input_data_path, 'REPEATER', 'third_party_name')
    previous_thParty2g_pw = get_config(input_data_path, 'REPEATER', 'third_party_pw')
    previous_thParty5g_name = get_config(input_data_path, 'REPEATER', 'third_party_name_5g')
    previous_thParty5g_pw = get_config(input_data_path, 'REPEATER', 'third_party_pw_5g')

    #
    Module0 = StringVar()
    Module1 = StringVar()
    Module2 = StringVar()
    Module3 = StringVar()
    Module4 = StringVar()
    Module5 = StringVar()
    Module6 = StringVar()
    Module7 = StringVar()
    Module8 = StringVar()
    Module9 = StringVar()
    Module10 = StringVar()
    Module11 = StringVar()


    cus0 = Entry(window, textvariable=Module0)
    cus1 = Entry(window, textvariable=Module1)
    cus2 = Entry(window, textvariable=Module2)
    cus3 = Entry(window, textvariable=Module3)
    cus4 = Entry(window, textvariable=Module4)
    cus5 = Entry(window, textvariable=Module5)
    cus6 = Entry(window, textvariable=Module6)
    cus7 = Entry(window, textvariable=Module7)
    cus8 = Entry(window, textvariable=Module8)
    cus9 = Entry(window, textvariable=Module9)
    cus10 = Entry(window, textvariable=Module10)
    cus11 = Entry(window, textvariable=Module11)

    for m, l, c, p in zip([Module0, Module1, Module2, Module3, Module4, Module5, Module6, Module7, Module8, Module9, Module10, Module11],
                    [cus0, cus1, cus2, cus3, cus4, cus5, cus6, cus7, cus8, cus9, cus10, cus11],
                    [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11],
                    [previous_meshLogin_name, previous_meshLogin_pw,
                     previous_mesh2g_name, previous_mesh2g_pw,
                     previous_mesh5g_name, previous_mesh5g_pw,
                     previous_thPartyLogin_name, previous_thPartyLogin_pw,
                     previous_thParty2g_name, previous_thParty2g_pw,
                     previous_thParty5g_name, previous_thParty5g_pw]):
        m.set(p)
        l.pack()
        l.place(x=135, y=c, height=25, width=330)

    def _saveBtn():
        save_config(input_data_path, 'REPEATER', 'user', cus0.get())
        save_config(input_data_path, 'REPEATER', 'pw', cus1.get())
        save_config(input_data_path, 'REPEATER', 'repeater_name', cus2.get())
        save_config(input_data_path, 'REPEATER', 'repeater_pw', cus3.get())
        save_config(input_data_path, 'REPEATER', 'repeater_name_5g', cus4.get())
        save_config(input_data_path, 'REPEATER', 'repeater_pw_5g', cus5.get())

        save_config(input_data_path, 'REPEATER', 'third_party_login_user', cus6.get())
        save_config(input_data_path, 'REPEATER', 'third_party_login_pw', cus7.get())
        save_config(input_data_path, 'REPEATER', 'third_party_name', cus8.get())
        save_config(input_data_path, 'REPEATER', 'third_party_pw', cus9.get())
        save_config(input_data_path, 'REPEATER', 'third_party_name_5g', cus10.get())
        save_config(input_data_path, 'REPEATER', 'third_party_pw_5g', cus11.get())
        window.destroy()

        flow_off_field(NORMAL)
    OKBtn = Button(window, text="Save", width=15, command=_saveBtn)
    OKBtn.pack(anchor='center', padx=5, pady=10)

    def on_closing():

        flow_off_field(NORMAL)
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()


basicSettingBtn = Button(root, text="   Basic", height=20, width=150, borderwidth=4, image=photo_setting,
                       compound=LEFT, command=lambda: _basicSetting())
basicSettingBtn.place(x=140, y=190)

repeaterSettingBtn = Button(root, text="   Upper Router", height=20, width=150, borderwidth=4, image=photo_setting_2,
                       compound=LEFT, command=lambda: _repeaterSetting())
repeaterSettingBtn.place(x=310, y=190)


cusPort4 = StringVar(None)
choices = serial_ports()
cusPort4.set(choices[0])
port4 = OptionMenu(root, cusPort4, *choices)
port4.place(x=140, y=140, height=30, width=330)
port4['background'] = 'white'

moduleChoices = ['MAIN', 'HOME', 'WIRELESS', 'NETWORK', 'MEDIASHARE', 'SECURITY', 'ADVANCED', 'NON_FUNCTION']
cusModuleAll = BooleanVar()
checkA = Checkbutton(root, text='ALL', variable=cusModuleAll, command=lambda: check_all_module())
checkA.place(x=140, y=240)

Module0 = BooleanVar()
Module1 = BooleanVar()
Module2 = BooleanVar()
Module3 = BooleanVar()
Module5 = BooleanVar()
Module6 = BooleanVar()
Module7 = BooleanVar()
Module8 = BooleanVar()
check0 = Checkbutton(root, text=moduleChoices[0], variable=Module0, command=lambda: all_module_checked())
check0.place(x=140 + 0 * 100, y=270)
check1 = Checkbutton(root, text=moduleChoices[1], variable=Module1, command=lambda: all_module_checked())
check1.place(x=140 + 1 * 100, y=270)
check2 = Checkbutton(root, text=moduleChoices[2], variable=Module2, command=lambda: all_module_checked())
check2.place(x=140 + 2 * 100, y=270)
check3 = Checkbutton(root, text=moduleChoices[3], variable=Module3, command=lambda: all_module_checked())
check3.place(x=140 + 0 * 100, y=270 + 30)
check5 = Checkbutton(root, text=moduleChoices[4], variable=Module5, command=lambda: all_module_checked())
check5.place(x=140 + 2 * 100, y=270 + 30)
check6 = Checkbutton(root, text=moduleChoices[5], variable=Module6, command=lambda: all_module_checked())
check6.place(x=140 + 0 * 100, y=270 + 60)
check7 = Checkbutton(root, text=moduleChoices[6], variable=Module7, command=lambda: all_module_checked())
check7.place(x=140 + 1 * 100, y=270 + 60)
check8 = Checkbutton(root, text=moduleChoices[7], variable=Module8, command=lambda: all_module_checked())
check8.place(x=140 + 2 * 100, y=270 + 60)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CreateToolTip(checkA, f" {str(get_num_test_case_module()['All'])} TCs ~ {str(get_runtime_test_module()['ALL'])} minutes")
CreateToolTip(check0, f" {str(get_num_test_case_module()['Main'])} TCs ~ {str(get_runtime_test_module()['MAIN'])} minutes")
CreateToolTip(check1, f" {str(get_num_test_case_module()['Home'])} TCs ~ {str(get_runtime_test_module()['HOME'])} minutes")
CreateToolTip(check2, f" {str(get_num_test_case_module()['Wireless'])} TCs ~ {str(get_runtime_test_module()['WIRELESS'])} minutes")
CreateToolTip(check3, f" {str(get_num_test_case_module()['Network'])} TCs ~ {str(get_runtime_test_module()['NETWORK'])} minutes")
CreateToolTip(check5, f" {str(get_num_test_case_module()['MediaShare'])} TCs ~ {str(get_runtime_test_module()['MEDIASHARE'])} minutes")
CreateToolTip(check6, f" {str(get_num_test_case_module()['Security'])} TCs ~ {str(get_runtime_test_module()['SECURITY'])} minutes")
CreateToolTip(check7, f" {str(get_num_test_case_module()['Advanced'])} TCs ~ {str(get_runtime_test_module()['ADVANCED'])} minutes")
CreateToolTip(check8, f" {str(get_num_test_case_module()['Non_Function'])} TCs ~ {str(get_runtime_test_module()['NON_FUNCTION'])} minutes")
scrollbar = Scrollbar(root, orient=HORIZONTAL)

linkLabel = Label(root, text="")

labelFile6 = Label(root, text="Individual TC:")
labelFile6.place(x=30, y=440)
ls_tc = StringVar()
lstc_box = Entry(root, textvariable=ls_tc, state=DISABLED, xscrollcommand=scrollbar.set)
lstc_box.pack()
lstc_box.place(x=140, y=440, height=25, width=330)


def cls():
    lstc_box.configure(state=NORMAL)
    lstc_box.delete(0, END)
    lstc_box.configure(state=DISABLED)

img_clear = Image.open('./Image/clear_btn.png')
photo_cls = ImageTk.PhotoImage(img_clear)
label = Label(root, image=photo_cls)
label.image = photo_cls
label.place(x=446, y=442)
label.bind("<Button-1>", lambda e: cls())


# ~~~~~~~~~~~~~~~
loopLabel = Label(root, text="Loop times:")
loopLabel.pack()
loopLabel.place(x=30, y=480)

loopBox = Spinbox(root, from_=1, to_=10)
loopBox.pack()
loopBox.place(x=140, y=480, width=50)

MakeReport = BooleanVar()
report_val = Checkbutton(root, text='Report to new sheet', variable=MakeReport)
report_val.select()
report_val.place(x=80, y=520)

progress = Label(root, text='Progress:')
progress.place(x=250, y=510)

from tkinter.ttk import Progressbar
from tkinter import ttk

style = ttk.Style(root)
style.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])

style.configure("black.Horizontal.TProgressbar", background="#00FF00")

total_percent = 170  # ~100%
bar = Progressbar(root, length=total_percent, style="text.Horizontal.TProgressbar")
bar['value'] = 0
bar.place(x=300, y=535)
style.configure("text.Horizontal.TProgressbar", text=f' {str(bar["value"])} %')

progress_bar = Label(root)
progress_bar.place(x=318, y=510)



scrollbar.place(x=140, y=463, height=10, width=330)
scrollbar.config(command=lstc_box.xview)

def check_all_module():
    if cusModuleAll.get():
        for m in [Module0, Module1, Module2, Module3, Module5, Module6, Module7, Module8]:
            m.set(True)
        for c in [check0, check1, check2, check3, check5, check6, check7, check8]:
            c.config(state=DISABLED)
        lstc_box.delete(0, END)
        manualButton.configure(state=DISABLED)

    else:
        for m in [Module0, Module1, Module2, Module3, Module5, Module6, Module7, Module8]:
            m.set(False)
        for c in [check0, check1, check2, check3, check5, check6, check7, check8]:
            c.config(state=NORMAL)
        manualButton.configure(state=NORMAL)


def all_module_checked():
    list_module = [Module0, Module1, Module2, Module3, Module5, Module6, Module7, Module8]
    check = all([m.get() for m in list_module])
    if check:
        cusModuleAll.set(True)
    else:
        cusModuleAll.set(False)


def find_chosen_module():
    list_modules = [cusModuleAll, Module0, Module1, Module2, Module3, Module5, Module6, Module7, Module8]
    list_choiced = list()
    for tx, va in zip(['ALL'] + moduleChoices, list_modules):
        if va.get():
            list_choiced.append(tx)
    return list_choiced


def detect_run_testcase(progress_bar):


    modules_name = get_config(config_path, 'GENERAL', 'module').split(';')
    if len(modules_name) >= 1 and modules_name[0] != '':

        if MakeReport.get():
            print('cd Test/T10x && python Before_test.py')
            os.system('cd Test/T10x && python Before_test.py')

        config_data = configparser.RawConfigParser()
        config_data.read(testcase_data_path)

        list_run = list()
        if 'ALL' not in modules_name:
            for module in modules_name:
                if module.startswith('test_'):
                    for s in config_data.sections():
                        for i in config_data.items(s):
                            if i[1] == module:
                                list_run.append([s, i[1]])
                else:
                    for sec in config_data.sections():
                        if module == sec:
                            for i in config_data.items(sec):
                                list_run.append([module, i[1]])

        else:
            for sec in config_data.sections():
                for i in config_data.items(sec):
                    list_run.append([sec, i[1]])

        total_time_run = get_runtime_test_case(list_run)
        print(total_time_run)
        bar['value'] = 0
        progress_bar.configure(text=f' {str(total_time_run)} minutes left')
        style.configure("text.Horizontal.TProgressbar", text=f' 0 %')
        for r in list_run:
            check_abort = get_config(config_path, 'GENERAL', 'abort')
            if check_abort == '0':
                break
            print(f'cd Test/T10x &&  python {convert_module[r[0]]} {r[0]}.{r[1]}')
            # time.sleep(1.5)
            os.system(f'cd Test/T10x &&  python {convert_module[r[0]]} {r[0]}.{r[1]}')

            progress_percent = int(((list_run.index(r) + 1) / len(list_run)) * 100)

            calculate_remain_time = round(((100 - progress_percent) * total_time_run)/100, 1)
            progress_bar.configure(text=f' {str(calculate_remain_time)} minutes left')

            bar['value'] = progress_percent
            style.configure("text.Horizontal.TProgressbar", text=f' {str(progress_percent)} %')

        if get_config(config_path, 'GENERAL', 'abort') == '0':
            progress_bar.configure(text=f' ABORTED')
        else:
            bar['value'] = 100
            style.configure("text.Horizontal.TProgressbar", text=f' 100 %')
            progress_bar.configure(text=f' DONE')



        print('cd Test/T10x && python After_test.py')
        os.system('cd Test/T10x && python After_test.py')
    else:
        messagebox.showinfo('Notice', 'Please choose your modules to run first.')


def _runBtn():
    flow_off_field(DISABLED)
    if stage1.get() == '':
        messagebox.showerror('Warning', ' Please fill in the Tester filed first.')
        flow_off_field(NORMAL)
        return



    save_config(config_path, 'GENERAL', 'stage', stage1.get())
    save_config(config_path, 'GENERAL', 'version', cusModel.get())

    save_config(config_path, 'CONSOLE', 'serial_port', cusPort4.get())

    list_choiced = find_chosen_module()

    if 'ALL' in list_choiced or moduleChoices == list_choiced:
        list_choiced = ['ALL']
    # global list_chosen_inform
    list_choiced_inform = ';'.join(list_choiced)

    if lstc_box.get() != '':
        save_config(config_path, 'GENERAL', 'module', lstc_box.get())
    else:
        save_config(config_path, 'GENERAL', 'module', list_choiced_inform)

    if warning():
        delete_report_offline()



        linkLabel.configure(text='< << Click here to go to report page >> >', fg='blue', anchor="center")
        linkLabel.pack()
        linkLabel.place(x=180, y=410)
        linkLabel.bind("<Button-1>", lambda e: callback("https://docs.google.com/spreadsheets/d/1kliw4-QTK4g3iz8fpbiyo-62L1dZZa5mCRTTMkBaLu4/edit?pli=1#gid=0"))

        runButton.configure(text=' Playing', image=photo_playing, state=DISABLED)

        for i in range(int(loopBox.get())):
            print(f'\n**************\n_- Run times {str(i + 1)} -_\n')
            # progress_bar.configure(text='     ')
            # progress_bar.configure(text=f' 0\t%')
            bar['value'] = 1
            detect_run_testcase(progress_bar)
        runButton.configure(text=' Run', image=photo_run, state=NORMAL)

        flow_off_field(NORMAL)
        # After Run. Set all module is uncheck
        # list_module = [cusModuleAll, Module0, Module1, Module2, Module3, Module5, Module6, Module7, Module8]
        # for m in list_module:
        #     m.set(False)
        cls()
    else:
        flow_off_field(NORMAL)
        if cusModuleAll.get():
            manualButton.configure(state=DISABLED)
        else:
            manualButton.configure(state=NORMAL)




def warning():
    return messagebox.askyesno('Confirm', f'Are you sure to run the test suit?')


def _manualBtn():
    manualButton.configure(state='disable')


    list_module_chosen = find_chosen_module()
    if not len(list_module_chosen):
        messagebox.showwarning('Warning', 'Please choose the test suit first!')
        manualButton.configure(state=NORMAL)
    else:

        config = configparser.RawConfigParser()
        config.read(testcase_data_path)
        now_x = root.winfo_x()
        now_y = root.winfo_y()
        window = Toplevel(root)
        window.geometry(f"1000x580+{str(now_x)}+{now_y}")
        window.resizable(0, 0)
        window.title("Pick testcases")
        window.iconbitmap(icon_path)

        # Search box
        ModuleSearch = StringVar()
        search_box = Entry(window, textvariable=ModuleSearch)
        search_box.pack()
        search_box.place(x=15, y=5, height=22, width=450)

        frame = Frame(window, relief=RAISED, borderwidth=12)
        frame.place(x=0, y=30, height=515, width=1000)



        def _addColor():
            selected = listBox.curselection()
            origin_list = listBox.get(0, listBox.size())
            list_append = [origin_list[i] for i in selected]
            for item in list_append:
                receipBox.insert(END, [item])
            while len(selected) > 0:
                listBox.delete(selected[0])
                selected = listBox.curselection()

        def _deleteColor():
            selected = receipBox.curselection()
            origin_list2 = receipBox.get(0, receipBox.size())
            list_append = [origin_list2[i] for i in selected]
            for item in list_append:
                listBox.insert(END, [item])
            while len(selected) > 0:
                receipBox.delete(selected[0])
                selected = receipBox.curselection()

        def warning2(number_chosen_tc):
            OKBtn.configure(state='disable')

            return messagebox.showinfo('Notice', f'Save {str(number_chosen_tc)} choices successfully')

        def _okBtn():
            individual_tc = list()
            for i in receipBox.get(0, receipBox.size()):
                if isinstance(i, tuple):
                    individual_tc.append(i[0])
                else:
                    individual_tc.append(i)

            individual_tc_string = ';'.join(individual_tc)

            if warning2(len(individual_tc)):


                indiv_tooltip = f'Estimate run time {str(get_runtime_test_case(list_individual_tc=individual_tc))} minutes.'
                CreateToolTip(lstc_box, indiv_tooltip)
                ls_tc.set(individual_tc_string)
                window.destroy()
                manualButton.configure(state='normal')

        def _cancelBtn():
            window.destroy()
            manualButton.configure(state='normal')

        list_value = list()
        if list_module_chosen != ['ALL']:
            for m in list_module_chosen:
                list_value += ([i[1] for i in config.items(m)])
        else:
            print(moduleChoices)
            for m in moduleChoices:
                list_value += ([i[1] for i in config.items(m)])

        source_in_individual_data = lstc_box.get()

        if source_in_individual_data != '':
            # Up old tc to receive box
            source_in_receive_data = source_in_individual_data.split(';')
            # Remove old tc to Send box
            for i in source_in_receive_data:
                if i in list_value:
                    list_value.remove(i)
        else:
            source_in_receive_data = []

        list_value = ' '.join(list_value)
        source_tc_send = StringVar()
        source_tc_send.set(list_value)

        listBox = Listbox(frame, listvariable=source_tc_send, selectmode=MULTIPLE)
        listBox.place(x=0, y=0, width=450, height=490)

        source_tc_receive = StringVar()
        source_tc_receive.set(source_in_receive_data)

        receipBox = Listbox(frame, listvariable=source_tc_receive, selectmode=MULTIPLE, width=73, height=20)
        receipBox.pack(fill=BOTH, side=RIGHT, padx=0)

        def update_source_data():
            current_source_data = list_value.split()
            current_source_data = [i for i in current_source_data]
            # print(current_source_data)
            current_receipt_data = receipBox.get(0, receipBox.size())
            current_receipt_data = [i[0] for i in current_receipt_data]
            # print(current_receipt_data)

            for i in current_receipt_data:
                if i in current_source_data:
                    current_source_data.remove(i)

            return current_source_data



        def _search_result():
            key = search_box.get()
            list_value_before_search = update_source_data()
            print(list_value_before_search)
            list_value_after_search = list()

            if key == '':
                list_value_after_search = list_value_before_search
            else:
                for v in list_value_before_search:
                    if key in v:
                        list_value_after_search.append(v)
            list_value_after_search = ' '.join(list_value_after_search)
            # print(list_value_before_search)
            source_tc_send.set(list_value_after_search)
            return list_value_after_search



        searchBtn = Button(window, text="Search", command=lambda: _search_result())
        searchBtn.place(x=480, y=3, height=25, width=50)


        copyButton = Button(frame, text=">>>", command=_addColor)
        copyButton.place(x=470, y=130)

        deleteButton = Button(frame, text="<<<", command=_deleteColor)
        deleteButton.place(x=470, y=170)



        cancelBtn = Button(window, text="Cancel", width=15, command=_cancelBtn)
        # cancelBtn.pack(side=BOTTOM, anchor='center', padx=5, pady=5)
        cancelBtn.place(x=530, y=550)
        OKBtn = Button(window, text="Save", width=15, command=_okBtn)
        # OKBtn.pack(side=RIGHT, anchor='center', padx=5, pady=5)
        OKBtn.place(x=370, y=550)
        def on_closing():
            # Destroy window and enable Manual button
            manualButton.configure(state='normal')
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_closing)

        window.mainloop()


def _abortBtn():
    print('Abort')
    warning = messagebox.askokcancel('Warning!', 'Are you sure to Abort this process? \n\n You should wait for current test case finish running..')

    if warning:
        save_config(config_path, 'GENERAL', 'abort', '0')


def run():
    save_config(config_path, 'GENERAL', 'abort', '1')
    threadRun = threading.Thread(target=_runBtn)
    threadRun.start()


def abort():
    threadAbort = threading.Thread(target=_abortBtn)
    threadAbort.start()






def _realcallback2():
    progress.configure(text='Progress:')
    abortButton['state'] = NORMAL
    flow_off_field(NORMAL)
    for c in [checkA, check0, check1, check2, check3, check5, check6, check7, check8]:
        c.config(state=NORMAL)
    progress_bar.configure(text=f' ')
    bar['value'] = 1

def _Factory():
    confirm_msg = messagebox.askyesno('Confirm factory', 'Do you want to factory set DUT?')
    if confirm_msg:
        root.after(500, _realcallback1)
        root.after(1_000, lambda: factory())
        root.after(FACTORY_TIME*1_000+3_000, _realcallback2)

def _realcallback1():
    progress.configure(text='Factoring ...')
    flow_off_field(DISABLED)
    abortButton['state'] = DISABLED
    for c in [checkA, check0, check1, check2, check3, check5, check6, check7, check8]:
        c.config(state=DISABLED)

def factory_bar(factory_time=FACTORY_TIME):
    bar['value'] = 1
    count = 1
    while count < factory_time:
        count += 1
        time.sleep(1)
        factory_percent = int(count * 100 / factory_time)
        print('Percent ' + str(factory_percent))
        bar['value'] = factory_percent
        style.configure("text.Horizontal.TProgressbar", text=f' {str(factory_percent)} %')
        progress_bar.configure(text=f' {str(factory_time-count)} seconds left.')
    progress_bar.configure(text=f' Finish factory.')
    style.configure("text.Horizontal.TProgressbar", text=f' 100 %')

def factory():
    save_config(config_path, 'CONSOLE', 'serial_port', cusPort4.get())
    os.system('netsh wlan disconnect')
    interface_connect_disconnect('Ethernet', 'Enable')
    theadFactoryCommand = threading.Thread(target=lambda: factory_dut())
    theadFactoryCommand.start()
    theadFactoryBar = threading.Thread(target=lambda: factory_bar())
    theadFactoryBar.start()


factoryButton = Button(root, text=" Factory", command=lambda: _Factory(), height=20, width=80, borderwidth=4, image=photo_loading,
                       compound=LEFT)
factoryButton.place(x=140, y=370)
CreateToolTip(factoryButton, f" Estimate {str(FACTORY_TIME)} seconds. ")

runButton = Button(root, text=" Run", command=run, height=20, width=80, borderwidth=4, image=photo_run, compound=LEFT)
runButton.place(x=250, y=370)


manualButton = Button(root, text=" Manual", command=_manualBtn, height=20, width=80, borderwidth=4, image=photo_manual,
                      compound=LEFT)
manualButton.place(x=360, y=475)

abortButton = Button(root, text=" Abort", command=abort, height=20, width=80, borderwidth=4, image=photo_abort,
                     compound=LEFT)
abortButton.place(x=360, y=370)


# __VERSION_ENVIRONMENT__ = 'T10.2.3'
#
# statusbar = Label(root, text=' '.join(['ver', __VERSION_ENVIRONMENT__]), bd=1, anchor=W, font="Verdana 6")
# statusbar.pack(side=BOTTOM, fill=X)
# =======================================================================================
def show_guideline():
    guide_text = '''
    This is the User manual of HUMAX T10X AUTOMATION desktop application.

    <Content of guide line>
    '''
    messagebox.showinfo(title='Application Manual', message=guide_text)


def guide_ver_0_1_1():
    guide_text = '''
        Release date: 01/01/2020.
        Content:
            + Build first class of Application
            + Link testcases created to app store file
            + Create basic functions
        '''
    messagebox.showinfo(title='Release ver T10.1.1', message=guide_text)


def guide_ver_0_1_2():
    guide_text = '''
        Release date: 01/02/2020.
        Content:
            + Update functions of Application
            + Add more testcases
        '''
    messagebox.showinfo(title='Release ver T10.1.2', message=guide_text)


def guide_ver_0_1_3():
    guide_text = '''
        Release date: 03/03/2020.
        Content:
            + Update Menu of Application.
            + Fixed bugs move app.
            + Add feature report to new sheet or not.
            + Improve code of test cases.
            + Prepare show demo in 13/03/2020.
        '''
    messagebox.showinfo(title='Release ver T10.1.3', message=guide_text)


def guide_ver_0_2_1():
    guide_text = '''
        Release date: Mar 11,2020.

        Content App:
           + Change app's icon.
           + Add HUMAX logo.
           + Disabled QoS module.
           + Change label: Tester, Module, Test Suite, More >>, Less <<, Goto report.
           + Remove Edit button.
           + Change type of Serial port.

        Content Scripts:
            + Add module name in testcase name.
            + Integration test and fixed bugs.
        '''
    messagebox.showinfo(title='Release ver T10.2.1', message=guide_text)


def guide_ver_0_2_2():
    guide_text = '''
        Release date: Mar 12,2020.

        Content App:
           + Resize to small icon.
           + Ignore feature ABORT.
           + Fixed missing run Non_function when Test suite is ALL.

        Content Scripts:
            + Add feature report to excel file.

        '''
    messagebox.showinfo(title='Release ver T10.2.2', message=guide_text)


def guide_ver_0_2_3():
    guide_text = '''
        Release date: Mar 13,2020.

        Content App:
           + Delete old value in Excel file.
           + Change ALL module logic: Disable all others  module, Clear Individual TC, Disabled Manual button.

        Content Scripts:
            + Optimize run time.

        '''
    messagebox.showinfo(title='Release ver T10.2.3', message=guide_text)


menu = Menu(root)
root.config(menu=menu)

about = Menu(menu)
about.add_command(label='Guideline', command=show_guideline)
menu.add_cascade(label='About', menu=about)

release = Menu(menu)
release.add_command(label='T10.1.1', command=guide_ver_0_1_1)
release.add_command(label='T10.1.2', command=guide_ver_0_1_2)
release.add_command(label='T10.1.3', command=guide_ver_0_1_3)
release.add_command(label='T10.2.1', command=guide_ver_0_2_1)
release.add_command(label='T10.2.2', command=guide_ver_0_2_2)
release.add_command(label='T10.2.3', command=guide_ver_0_2_3)
menu.add_cascade(label='Release notes', menu=release)

# =======================================================================================

root.geometry("520x560+500+100")
root.resizable(0, 0)
root.mainloop()
