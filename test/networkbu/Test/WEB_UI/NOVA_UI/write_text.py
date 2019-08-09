import tftpy
import os
import time

script_dir = os.path.dirname(os.path.realpath(__file__))
host = "192.168.0.1"
port = 69
output = os.path.join(script_dir, "url.txt")
client = tftpy.TftpClient(host, port)
client.download('url.txt', output)

output2 = os.path.join(script_dir, "account.txt")
client = tftpy.TftpClient(host, port)
client.download('account.txt', output2)