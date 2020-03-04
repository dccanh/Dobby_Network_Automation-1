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

try:
    import keyboard
except ModuleNotFoundError:
    os.system('pip install keyboard')
    import keyboard
config_path = './Config/t10x/config.txt'
testcase_data_path = './Image/testcase_data.txt'
icon_path = './Image/sun.ico'
VERSION_ENVIRONMENT = 'v0.1.3'


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
    'ALL': ['Main.py', 'Home.py', 'Wireless.py', 'Network.py', 'MediaShare.py', 'Security.py', 'Advanced.py', ]
}

root = Tk()
root.title(f"Canh______Ciel______{VERSION_ENVIRONMENT}")
root.iconbitmap(icon_path)
titleLabel = Label(root, text="HUMAX T10X AUTOMATION", anchor='center', font=40)
titleLabel.pack()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
labelFile1 = Label(root, text="Stage:")
labelFile1.place(x=30, y=40)
labelFile2 = Label(root, text="Version:")
labelFile2.place(x=30, y=90)
labelFile3 = Label(root, text="Serial Number:")
labelFile3.place(x=30, y=140)
labelFile4 = Label(root, text="Serial Port:")
labelFile4.place(x=30, y=190)
labelFile5 = Label(root, text="Module:")
labelFile5.place(x=30, y=240)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cusStage1 = StringVar()
stage1 = Entry(root, textvariable=cusStage1)
stage1.pack()
cusStage1.set(get_config(config_path, 'GENERAL', 'stage'))
stage1.place(x=140, y=40, height=25, width=330)

cusVersion2 = StringVar(None)
version2 = Entry(root, textvariable=cusVersion2)
version2.pack()
cusVersion2.set(get_config(config_path, 'GENERAL', 'version'))
version2.place(x=140, y=90, height=25, width=330)

cusNumber3 = StringVar()
number3 = Entry(root, textvariable=cusNumber3)
number3.pack()
cusNumber3.set(get_config(config_path, 'GENERAL', 'serial_number'))
number3.place(x=140, y=140, height=25, width=330)

cusPort4 = StringVar(None)
port4 = Entry(root, textvariable=cusPort4)
port4.pack()
cusPort4.set(get_config(config_path, 'CONSOLE', 'serial_port'))
port4.place(x=140, y=190, height=25, width=330)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
moduleChoices = ['MAIN', 'HOME', 'WIRELESS', 'NETWORK', 'QOS', 'MEDIASHARE', 'SECURITY', 'ADVANCED', 'NON_FUNCTION']
cusModuleAll = BooleanVar()
check2 = Checkbutton(root, text='ALL', variable=cusModuleAll)
check2.place(x=140, y=240)

Module0 = BooleanVar()
Module1 = BooleanVar()
Module2 = BooleanVar()
Module3 = BooleanVar()
Module4 = BooleanVar()
Module5 = BooleanVar()
Module6 = BooleanVar()
Module7 = BooleanVar()
Module8 = BooleanVar()
check0 = Checkbutton(root, text=moduleChoices[0], variable=Module0).place(x=140 + 0 * 100, y=270)
check1 = Checkbutton(root, text=moduleChoices[1], variable=Module1).place(x=140 + 1 * 100, y=270)
check2 = Checkbutton(root, text=moduleChoices[2], variable=Module2).place(x=140 + 2 * 100, y=270)
check3 = Checkbutton(root, text=moduleChoices[3], variable=Module3).place(x=140 + 0 * 100, y=270 + 30)
check4 = Checkbutton(root, text=moduleChoices[4], variable=Module4).place(x=140 + 1 * 100, y=270 + 30)
check5 = Checkbutton(root, text=moduleChoices[5], variable=Module5).place(x=140 + 2 * 100, y=270 + 30)
check6 = Checkbutton(root, text=moduleChoices[6], variable=Module6).place(x=140 + 0 * 100, y=270 + 60)
check7 = Checkbutton(root, text=moduleChoices[7], variable=Module7).place(x=140 + 1 * 100, y=270 + 60)
check8 = Checkbutton(root, text=moduleChoices[8], variable=Module8).place(x=140 + 2 * 100, y=270 + 60)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# notiLabel = Label(root, text="")
# notiLabel.place(x=170, y=400)
linkLabel = Label(root, text="")

labelFile6 = Label(root, text="Individual TC:")
labelFile6.place(x=30, y=440)
ls_tc = StringVar()
lstc_box = Entry(root, textvariable=ls_tc)
lstc_box.pack()
lstc_box.place(x=140, y=440, height=25, width=330)

# ~~~~~~~~~~~~~~~
loopLabel = Label(root, text="Loop times:")
loopLabel.pack()
loopLabel.place(x=30, y=480)

loopBox = Spinbox(root, from_=1, to_=10)
loopBox.pack()
loopBox.place(x=140, y=480, width=50)


def _advanceBtn():
    global now_x, now_y
    now_x = root.winfo_x()
    now_y = root.winfo_y()
    if root.winfo_height() == 440:
        root.geometry(f"520x560+{str(now_x)}+{str(now_y)}")
    else:
        root.geometry(f"520x440+{str(now_x)}+{str(now_y)}")


    global MakeReport
    MakeReport = BooleanVar()
    report_val = Checkbutton(root, text='Report to new sheet', variable=MakeReport).place(x=80, y=520)

    progressLabel = StringVar()
    progress = Label(root, text='Progress:')
    progress.place(x=250, y=520)


def find_chosen_module():
    list_modules = [cusModuleAll, Module0, Module1, Module2, Module3, Module4, Module5, Module6, Module7, Module8]
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
        messagebox.showinfo('Ciel Says', 'Please choose your modules to run first.')


def _runBtn():
    save_config(config_path, 'GENERAL', 'stage', stage1.get())
    save_config(config_path, 'GENERAL', 'version', version2.get())
    save_config(config_path, 'GENERAL', 'serial_number', number3.get())
    save_config(config_path, 'CONSOLE', 'serial_port', port4.get())

    list_choiced = find_chosen_module()

    if 'ALL' in list_choiced or moduleChoices == list_choiced:
        list_choiced = ['ALL']
    # global list_choiced_inform
    list_choiced_inform = ';'.join(list_choiced)

    if lstc_box.get() != '':
        save_config(config_path, 'GENERAL', 'module', lstc_box.get())
    else:
        save_config(config_path, 'GENERAL', 'module', list_choiced_inform)

    if warning():
        # notiLabel.configure(text=f'__- Ready to execute module -__', anchor="center")
        linkLabel.configure(text='< << <<< <<<< <<<<<Go to report page>>>>> >>>> >>> >> >', fg='blue', anchor="center")
        linkLabel.pack()
        linkLabel.place(x=140, y=410)
        linkLabel.bind("<Button-1>", lambda e: callback("https://sum.vn/Rx5Zy"))

        for i in range(int(loopBox.get())):
            print(f'\n**************\n_- Run times {str(i + 1)} -_\n')

            detect_run_testcase()

        progress = Label(root, text=f'DONE at {str(datetime.now())}')
        progress.place(x=318, y=520)


def warning():
    return messagebox.askyesno('Confirm', f'Are you sure to run?')


# def _manualBtn():
#     # root.disable()
#     load_database_tc(MAIN)
#     load_database_tc(HOME)
#     load_database_tc(NETWORK)
#     load_database_tc(WIRELESS)
#     load_database_tc(SECURITY)
#     load_database_tc(ADVANCED)
#     load_database_tc(MEDIASHARE)
#
#     list_module_chosen = find_chosen_module()
#
#     config = configparser.RawConfigParser()
#     config.read(testcase_data_path)
#
#     window = Toplevel(root)
#     window.geometry("985x550+300+300")
#     window.title("Ciel pick test case")
#     def _addColor():
#         selected = listBox.curselection()
#         origin_list = listBox.get(0, listBox.size())
#         list_append = [origin_list[i] for i in selected]
#         for item in list_append:
#             receipBox.insert(END, [item])
#         while len(selected) > 0:
#             listBox.delete(selected[0])
#             selected = listBox.curselection()
#
#     def _deleteColor():
#         selected = receipBox.curselection()
#         origin_list2 = receipBox.get(0, receipBox.size())
#         list_append = [origin_list2[i] for i in selected]
#         for item in list_append:
#             listBox.insert(END, [item])
#         while len(selected) > 0:
#             receipBox.delete(selected[0])
#             selected = receipBox.curselection()
#
#     def warning2():
#         return messagebox.showinfo('Ciel Says', 'Your choices save successfully')
#
#     def _okBtn():
#         individual_tc = list()
#         for i in receipBox.get(0, receipBox.size()):
#             if isinstance(i, tuple):
#                 individual_tc.append(i[0])
#             else:
#                 individual_tc.append(i)
#
#         individual_tc_string = ';'.join(individual_tc)
#         # window.grab_set()
#         if warning2():
#
#             ls_tc.set(individual_tc_string)
#             window.destroy()
#         # window.grab_release()
#
#     list_value = list()
#     if list_module_chosen != ['ALL']:
#         for m in list_module_chosen:
#             list_value += ([i[1] for i in config.items(m)])
#     else:
#         for m in moduleChoices:
#             list_value += ([i[1] for i in config.items(m)])
#
#     source_in_individual_data = lstc_box.get()
#     print(source_in_individual_data)
#     # # Remove data in Individual box
#     if source_in_individual_data != '':
#         # Up old tc to receive box
#         source_in_receive_data = source_in_individual_data.split(';')
#         # Remove old tc to Send box
#         for i in source_in_receive_data:
#             if i in list_value:
#                 list_value.remove(i)
#     else:
#         source_in_receive_data = []
#
#     list_value = ' '.join(list_value)
#     source_tc_send = StringVar()
#     source_tc_send.set(list_value)
#
#     listBox = Listbox(window, listvariable=source_tc_send, selectmode=MULTIPLE)
#     listBox.place(x=0, y=0, width=450, height=490)
#
#     copyButton = Button(window, text=">>>", command=_addColor)
#     copyButton.place(x=465, y=130)
#
#     deleteButton = Button(window, text="<<<", command=_deleteColor)
#     deleteButton.place(x=465, y=170)
#
#     source_tc_receive = StringVar()
#     source_tc_receive.set(source_in_receive_data)
#
#     receipBox = Listbox(window, listvariable=source_tc_receive, selectmode=MULTIPLE, width=20, height=10)
#     receipBox.place(x=530, y=0, width=450, height=490)
#
#     OKBtn = Button(window, text="Save", width=15, command=_okBtn)
#     OKBtn.pack(side=BOTTOM, anchor='center', padx=10, pady=5)
#     # OKBtn = Button(window, text="Cancel")
#     # OKBtn.pack(side=RIGHT, anchor='center', padx=15, pady=5)
#
#     window.mainloop()

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

    config = configparser.RawConfigParser()
    config.read(testcase_data_path)

    window = Toplevel(root)
    window.geometry(f"985x550+{str(now_x)}+{now_y}")
    window.resizable(0, 0)
    window.title("Ciel pick test case")





    frame = Frame(window, relief=RAISED, borderwidth=12)
    frame.pack(fill=BOTH, expand=True)

    # window.pack(fill=BOTH, expand=True)

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

    def warning2():
        OKBtn.configure(state='disable')
        return messagebox.showinfo('Ciel Says', 'Your choices save successfully')

    def _okBtn():
        individual_tc = list()
        for i in receipBox.get(0, receipBox.size()):
            if isinstance(i, tuple):
                individual_tc.append(i[0])
            else:
                individual_tc.append(i)

        individual_tc_string = ';'.join(individual_tc)

        if warning2():
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
        for m in moduleChoices:
            list_value += ([i[1] for i in config.items(m)])

    source_in_individual_data = lstc_box.get()
    print(source_in_individual_data)
    # # Remove data in Individual box
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
    listBox.place(x=0, y=0, width=450, height=480)

    copyButton = Button(frame, text=">>>", command=_addColor)
    copyButton.place(x=465, y=130)

    deleteButton = Button(frame, text="<<<", command=_deleteColor)
    deleteButton.place(x=465, y=170)

    source_tc_receive = StringVar()
    source_tc_receive.set(source_in_receive_data)

    receipBox = Listbox(frame, listvariable=source_tc_receive, selectmode=MULTIPLE, width=54, height=20)
    # receipBox.place(x=530, y=0, width=450, height=490)
    receipBox.pack(fill=BOTH, side=RIGHT, padx=0)
    # receipBox.grid(sticky=W+E)

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
    keyboard.press('ctrl+c')
    warning = messagebox.askokcancel('Warning!', 'System must to reload after abort.')
    if warning:
        root.destroy()
        os.system('_run_app.bat')


def run():
    threadRun = threading.Thread(target=_runBtn)
    threadRun.start()


def abort():
    threadAbort = threading.Thread(target=_abortBtn)
    threadAbort.start()
    # exit_Btn()


exitButton = Button(root, text="Exit", command=exit_Btn, height=1, width=10, borderwidth=4)
exitButton.place(x=170, y=370)
mergeButton = Button(root, text="Run", command=run, height=1, width=10, borderwidth=4)
mergeButton.place(x=280, y=370)
advanceButton = Button(root, text="Advance", command=_advanceBtn, height=1, width=10, borderwidth=4)
advanceButton.place(x=390, y=370)
manualButton = Button(root, text="Manual", command=_manualBtn, height=1, width=10, borderwidth=4)
manualButton.place(x=250, y=470)
abortButton = Button(root, text="Abort", command=abort, height=1, width=10, borderwidth=4)
abortButton.place(x=360, y=470)


# =======================================================================================
def show_guideline():
    guide_text = '''
    This is the User manual of HUMAX T10X AUTOMATION desktop application.
    After each official release ver will be plus +1
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
    messagebox.showinfo(title='Release ver 0.1.1', message=guide_text)


def guide_ver_0_1_2():
    guide_text = '''
        Release date: 01/02/2020.
        Content:
            + Update functions of Application
            + Add more testcases
        '''
    messagebox.showinfo(title='Release ver 0.1.2', message=guide_text)


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
    messagebox.showinfo(title='Release ver 0.1.3', message=guide_text)


menu = Menu(root)
root.config(menu=menu)

about = Menu(menu)
about.add_command(label='Guideline', command=show_guideline)
menu.add_cascade(label='About', menu=about)

release = Menu(menu)
release.add_command(label='v0.1.1', command=guide_ver_0_1_1)
release.add_command(label='v0.1.2', command=guide_ver_0_1_2)
release.add_command(label='v0.1.3', command=guide_ver_0_1_3)
menu.add_cascade(label='Release', menu=release)

# =======================================================================================

root.geometry("520x440+500+100")
root.resizable(0, 0)
root.mainloop()
