import argparse
import ctypes
import subprocess
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
    subprocess.call('netsh interface set interface name="Ethernet" admin=enabled', shell=True)
    subprocess.call('netsh interface set interface name="Ethernet 2" admin=disabled', shell=True)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
