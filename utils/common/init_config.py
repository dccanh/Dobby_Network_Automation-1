import argparse
import configparser
import os
import shutil
import subprocess
import sys

from common import *

# Parse the input arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-cm','--cm_port', help='The COM port of CM console. Ex: COM5', required=True)
parser.add_argument('-ip','--gw_ip', help='The IP address of the DUT gateway. Ex: 192.168.0.1', required=True)
parser.add_argument('-rg','--rg_port', help='The COM port of RG console. Ex: COM6', required=True)
parser.add_argument('-m','--mode', help='The operation mode: auto or manual', required=False)
args = parser.parse_args()

RG_PORT = str(args.rg_port).upper()
print("RG_PORT: " + RG_PORT)
save_config("SERIAL", "RG_PORT", RG_PORT)

CM_PORT = str(args.cm_port).upper()
print("CM_PORT: " + CM_PORT)
save_config("SERIAL", "CM_PORT", CM_PORT)

# GW_IP = "192.168.0.1"
GW_IP = str(args.gw_ip)
print("GW_IP: " + GW_IP)
save_config("IP", "GW_IP", GW_IP)

mode = str(args.mode)
if (mode.lower() == "manual"):
    save_config("COMMON", "manual_mode", "True")
    print("Flash mode: Manual")
else:
    save_config("COMMON", "manual_mode", "False")
    print("Flash mode: Auto")

