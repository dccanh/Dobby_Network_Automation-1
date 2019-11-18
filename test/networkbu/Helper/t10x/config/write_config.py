import sys
from Helper.t10x.common import save_config
from Helper.t10x.ls_path import *


def write_config(stage, version):
    save_config(config_path, 'GENERAL', 'stage', stage)
    save_config(config_path, 'GENERAL', 'version', version)


if __name__ == '__main__':
    write_config(sys.argv[1], sys.argv[2])

