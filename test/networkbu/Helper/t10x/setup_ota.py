import configparser, os
from winreg import *
def download_destination_path():
    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    return Downloads
download_path = download_destination_path()
# print(download_path)

support_install_path = os.path.join(download_path, 'auto_generate_support_install_version.txt')
# print(support_install_path)
if os.path.exists(support_install_path):
    with open(support_install_path, 'r') as f:
        client_repo_path = f.read()
        print(client_repo_path)
current_path = os.getcwd()
# print(current_path)

config = configparser.RawConfigParser()
change_log_path = os.path.join(current_path, "changed_info.txt")
config.read(change_log_path)
list_change = [i[1] for i in list(config.items('CHANGE_INFO'))]
# print(list_change)


for f in list_change:
    source_path = os.path.join(current_path, f.replace("/", "\\"))
    # print(source_path)
    target_path = os.path.join(client_repo_path, "../..", f)
    dest_copy = os.path.abspath(target_path+"/..")
    print(dest_copy)
    if os.path.exists(target_path):
        os.remove(target_path)

    cmd = f'copy "{source_path}" "{dest_copy}"'
    print(cmd)
    os.system(cmd)


