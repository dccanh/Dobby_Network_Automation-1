import argparse
import ctypes
import subprocess
import sys

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-a','--action', help='Action: enabled/disabled', required=False)
parser.add_argument('-i','--interface', help='The network interface', required=False)
args = parser.parse_args()

interface = str(args.interface)
action = str(args.action).lower()

print("interface: " + interface + " | action: " + action)

cmd = "netsh interface set interface name=\"" + interface + "\" admin=" + action

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
    subprocess.call(cmd, shell=True)
else:
    # Re-run the program with admin rights
    parameters = ""
    for i in range(1, len(sys.argv)):
        parameters = parameters + " \"" + str(sys.argv[i]) + "\""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__ + parameters, None, 1)
