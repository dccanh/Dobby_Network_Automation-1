import sys
from Helper.t10x.common import save_config
from Helper.t10x.ls_path import *


def write_config(stage, version, serial_number, serial_port):
    save_config(config_path, 'GENERAL', 'stage', stage)
    save_config(config_path, 'GENERAL', 'version', version)
    save_config(config_path, 'GENERAL', 'serial_number', serial_number)
    save_config(config_path, 'CONSOLE', 'serial_port', serial_port)


if __name__ == '__main__':
    write_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

