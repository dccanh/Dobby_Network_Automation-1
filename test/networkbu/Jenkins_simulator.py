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

config_path = './Config/t10x/config.txt'
testcase_data_path = './Image/testcase_data.txt'
icon_path = './Image/logo.ico'


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


convert_module = {
    'MAIN': 'Main.py',
    'HOME': 'Home.py',
    'WIRELESS': 'Wireless.py',
    'NETWORK': 'Network.py',
    'QOS': 'QOS.py',
    'MEDIASHARE': 'MediaShare.py',
    'SECURITY': 'Security.py',
    'ADVANCED': 'Advanced.py',
    'NON_FUNCTION': 'Non_Function.py',
    'ALL': ['Main.py', 'Home.py', 'Wireless.py', 'Network.py', 'MediaShare.py', 'Security.py', 'Advanced.py',
            'Non_Function.py']
}

root = Tk()
root.title(f"NETWORK AUTOMATION TOOL")
root.iconbitmap(icon_path)

img = Image.open('./Image/humax-logo-01.png')
photo = ImageTk.PhotoImage(img)
label = Label(root, image=photo)
label.image = photo
label.place(x=2, y=0)

titleLabel = Label(root, text="NETWORK AUTOMATION TOOL", font="Verdana 13")
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
labelFile1 = Label(root, text="Tester:")
labelFile1.place(x=30, y=40)
labelFile2 = Label(root, text="Model:")
labelFile2.place(x=30, y=90)
labelFile3 = Label(root, text="Serial Number:")
labelFile3.place(x=30, y=140)
labelFile4 = Label(root, text="Serial Port:")
labelFile4.place(x=30, y=190)
labelFile5 = Label(root, text="Test Suite:")
labelFile5.place(x=30, y=240)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cusStage1 = StringVar()
stage1 = Entry(root, textvariable=cusStage1)
stage1.pack()
stage1.place(x=140, y=40, height=25, width=330)

# cusVersion2 = StringVar(None)
# version2 = Entry(root, textvariable=cusVersion2)
# version2.pack()
# version2.place(x=140, y=90, height=25, width=330)
cusModel = StringVar()
choices = ['T9X', 'T10X', 'T11X']
cusModel.set(choices[1])
model = OptionMenu(root, cusModel, *choices)
model.place(x=140, y=90, height=30, width=330)
model['background'] = 'white'


# cusNumber3 = StringVar()
# number3 = Entry(root, textvariable=cusNumber3)
# number3.pack()
# number3.place(x=140, y=140, height=25, width=330)
cusNumber = StringVar()
choices = ['0001', '0016', '0028', '0049']
cusNumber.set(choices[1])
numberl = OptionMenu(root, cusNumber, *choices)
numberl.place(x=140, y=140, height=30, width=330)
numberl['background'] = 'white'


cusPort4 = StringVar(None)
choices = serial_ports()
cusPort4.set(choices[0])
port4 = OptionMenu(root, cusPort4, *choices)
port4.place(x=140, y=190, height=30, width=330)
port4['background'] = 'white'

moduleChoices = ['MAIN', 'HOME', 'WIRELESS', 'NETWORK', 'MEDIASHARE', 'SECURITY', 'ADVANCED', 'NON_FUNCTION']
cusModuleAll = BooleanVar()
check2 = Checkbutton(root, text='ALL', variable=cusModuleAll, command=lambda: check_all_module())
check2.place(x=140, y=240)

Module0 = BooleanVar()
Module1 = BooleanVar()
Module2 = BooleanVar()
Module3 = BooleanVar()
# Module4 = BooleanVar()
Module5 = BooleanVar()
Module6 = BooleanVar()
Module7 = BooleanVar()
Module8 = BooleanVar()
check0 = Checkbutton(root, text=moduleChoices[0], variable=Module0)
check0.place(x=140 + 0 * 100, y=270)
check1 = Checkbutton(root, text=moduleChoices[1], variable=Module1)
check1.place(x=140 + 1 * 100, y=270)
check2 = Checkbutton(root, text=moduleChoices[2], variable=Module2)
check2.place(x=140 + 2 * 100, y=270)
check3 = Checkbutton(root, text=moduleChoices[3], variable=Module3)
check3.place(x=140 + 0 * 100, y=270 + 30)
check5 = Checkbutton(root, text=moduleChoices[4], variable=Module5)
check5.place(x=140 + 2 * 100, y=270 + 30)
check6 = Checkbutton(root, text=moduleChoices[5], variable=Module6)
check6.place(x=140 + 0 * 100, y=270 + 60)
check7 = Checkbutton(root, text=moduleChoices[6], variable=Module7)
check7.place(x=140 + 1 * 100, y=270 + 60)
check8 = Checkbutton(root, text=moduleChoices[7], variable=Module8)
check8.place(x=140 + 2 * 100, y=270 + 60)
check4 = Checkbutton(root, text='QoS', state='disabled').place(x=140 + 1 * 100, y=270 + 30)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


linkLabel = Label(root, text="")

labelFile6 = Label(root, text="Individual TC:")
labelFile6.place(x=30, y=440)
ls_tc = StringVar()
lstc_box = Entry(root, textvariable=ls_tc, state=DISABLED)
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
progress.place(x=250, y=520)


def _advanceBtn():
    global MakeReport

    global now_x, now_y
    now_x = root.winfo_x()
    now_y = root.winfo_y()
    if root.winfo_height() == 440:
        root.geometry(f"520x560+{str(now_x)}+{str(now_y)}")
        advanceButton.configure(text=' Less', image=photo_up)
    else:
        root.geometry(f"520x440+{str(now_x)}+{str(now_y)}")
        advanceButton.configure(text=' More', image=photo_down)


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


def find_chosen_module():
    list_modules = [cusModuleAll, Module0, Module1, Module2, Module3, Module5, Module6, Module7, Module8]  # , Module4
    list_choiced = list()
    for tx, va in zip(['ALL'] + moduleChoices, list_modules):
        if va.get():
            list_choiced.append(tx)
    return list_choiced


def detect_run_testcase():
    # os.system('cd Test/T10x && python Before_test.py')

    modules_name = get_config(config_path, 'GENERAL', 'module').split(';')
    if len(modules_name) >= 1 and modules_name[0] != '':

        if MakeReport.get():
            print('cd Test/T10x && python Before_test.py')
            # os.system('TIMEOUT /T 20')
            os.system('cd Test/T10x && python Before_test.py')

        config_data = configparser.RawConfigParser()
        config_data.read(testcase_data_path)

        for module in modules_name:
            if module.startswith('test_'):
                for s in config_data.sections():
                    for i in config_data.items(s):
                        if i[1] == module:
                            print(f'cd Test/T10x &&  python {convert_module[s]} {s}.{i[1]}')
                            os.system(f'cd Test/T10x &&  python {convert_module[s]} {s}.{i[1]}')
            else:
                if module == 'ALL':
                    for m in convert_module[module]:
                        print(f'cd Test/T10x &&  python {m}')
                        os.system(f'cd Test/T10x &&  python {m}')
                    break
                else:
                    print(f'cd Test/T10x &&  python {convert_module[module]}')
                    os.system(f'cd Test/T10x &&  python {convert_module[module]}')

        print('cd Test/T10x && python After_test.py')
        os.system('cd Test/T10x && python After_test.py')
    else:
        messagebox.showinfo('Notice', 'Please choose your modules to run first.')


def _runBtn():
    stage1.configure(state=DISABLED)
    model.configure(state=DISABLED)
    numberl.configure(state=DISABLED)



    save_config(config_path, 'GENERAL', 'stage', stage1.get())
    save_config(config_path, 'GENERAL', 'version', cusModel.get())
    save_config(config_path, 'GENERAL', 'serial_number', cusNumber.get())
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

        progress = Label(root)
        progress.place(x=318, y=520)

        linkLabel.configure(text='< << Click here to go to report page >> >', fg='blue', anchor="center")
        linkLabel.pack()
        linkLabel.place(x=180, y=410)
        linkLabel.bind("<Button-1>", lambda e: callback("https://docs.google.com/spreadsheets/d/1kliw4-QTK4g3iz8fpbiyo-62L1dZZa5mCRTTMkBaLu4/edit?pli=1#gid=0"))

        mergeButton.configure(text=' Playing', image=photo_playing, state=DISABLED)

        for i in range(int(loopBox.get())):
            print(f'\n**************\n_- Run times {str(i + 1)} -_\n')

            detect_run_testcase()
        time = datetime.now()
        time_str = time.strftime('%d %b, %Y %H:%M:%S')
        progress.configure(text=f' DONE: {time_str}')
        manualButton.configure(state=NORMAL)
        mergeButton.configure(text=' Run', image=photo_run, state=NORMAL)

        stage1.configure(state=NORMAL)
        model.configure(state=NORMAL)
        numberl.configure(state=NORMAL)



def warning():
    return messagebox.askyesno('Confirm', f'Are you sure to run?')


def _manualBtn():
    manualButton.configure(state='disable')
    load_database_tc(MAIN)
    load_database_tc(HOME)
    load_database_tc(NETWORK)
    load_database_tc(WIRELESS)
    load_database_tc(SECURITY)
    load_database_tc(ADVANCED)
    load_database_tc(MEDIASHARE)
    load_database_tc(NON_FUNCTION)

    list_module_chosen = find_chosen_module()
    if not len(list_module_chosen):
        messagebox.showwarning('Warning', 'You have to choose test suite first!')
        manualButton.configure(state=NORMAL)
    else:

        config = configparser.RawConfigParser()
        config.read(testcase_data_path)
        now_x = root.winfo_x()
        now_y = root.winfo_y()
        window = Toplevel(root)
        window.geometry(f"985x550+{str(now_x)}+{now_y}")
        window.resizable(0, 0)
        window.title("Pick testcases")
        window.iconbitmap(icon_path)

        frame = Frame(window, relief=RAISED, borderwidth=12)
        frame.pack(fill=BOTH, expand=True)

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
        print(source_in_individual_data)
        # Remove data in Individual box
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

        copyButton = Button(frame, text=">>>", command=_addColor)
        copyButton.place(x=465, y=130)

        deleteButton = Button(frame, text="<<<", command=_deleteColor)
        deleteButton.place(x=465, y=170)

        source_tc_receive = StringVar()
        source_tc_receive.set(source_in_receive_data)

        receipBox = Listbox(frame, listvariable=source_tc_receive, selectmode=MULTIPLE, width=73, height=20)
        receipBox.pack(fill=BOTH, side=RIGHT, padx=0)

        cancelBtn = Button(window, text="Cancel", width=15, command=_cancelBtn)
        cancelBtn.pack(side=RIGHT, anchor='center', padx=5, pady=5)
        OKBtn = Button(window, text="Save", width=15, command=_okBtn)
        OKBtn.pack(side=RIGHT, anchor='center', padx=5, pady=5)

        def on_closing():
            # Destroy window and enable Manual button
            manualButton.configure(state='normal')
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_closing)

        window.mainloop()


def _abortBtn():
    print('Aboart')
    warning = messagebox.askokcancel('Warning!', 'This Abort function has not been implemented.')
    # warning = messagebox.askokcancel('Warning!', 'System must to reload after abort.')
    # if warning:
    #     root.destroy()
    #     os.system('taskkill /IM "pythonw.exe" /F')
    #     os.system('taskkill /IM "cmd.exe" /F')
    #     os.system('_run_app.bat')
    # os.system('taskkill /IM "python.exe" /F')
    # root.destroy()


def run():
    threadRun = threading.Thread(target=_runBtn)
    threadRun.start()


def abort():
    threadAbort = threading.Thread(target=_abortBtn)
    threadAbort.start()
    # exit_Btn()


def factory():
    print(cusPort4.get())
    save_config(config_path, 'GENERAL', 'serial_number', cusNumber.get())
    save_config(config_path, 'CONSOLE', 'serial_port', cusPort4.get())
    time.sleep(3)
    factory_dut()


factoryButton = Button(root, text=" Factory", command=factory, height=20, width=80, borderwidth=4, image=photo_run, compound=LEFT)
factoryButton.place(x=140, y=370)


mergeButton = Button(root, text=" Run", command=run, height=20, width=80, borderwidth=4, image=photo_run, compound=LEFT)
mergeButton.place(x=250, y=370)
advanceButton = Button(root, text=" More", command=_advanceBtn, height=20, width=80, borderwidth=4, image=photo_down,
                       compound=LEFT)
advanceButton.place(x=360, y=370)
manualButton = Button(root, text=" Manual", command=_manualBtn, height=20, width=80, borderwidth=4, image=photo_manual,
                      compound=LEFT)
manualButton.place(x=250, y=470)
abortButton = Button(root, text=" Abort", command=abort, height=20, width=80, borderwidth=4, image=photo_abort,
                     compound=LEFT)
abortButton.place(x=360, y=470)


__VERSION_ENVIRONMENT__ = 'T10.2.3'

statusbar = Label(root, text=' '.join(['ver', __VERSION_ENVIRONMENT__]), bd=1, anchor=W, font="Verdana 6")
statusbar.pack(side=BOTTOM, fill=X)
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

root.geometry("520x440+500+100")
root.resizable(0, 0)
root.mainloop()
