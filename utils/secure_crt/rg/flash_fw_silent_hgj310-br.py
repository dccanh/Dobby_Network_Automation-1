#$language = "python"
#$interface = "1.0"

import os
import sys

binaries_dir = crt.Arguments.GetArg(0)

#=============================================================================
# RGIP    = "192.168.0.11"
RGIP    = crt.Arguments.GetArg(1)
Netmask = "255.255.255.0"
PCIP    = crt.Arguments.GetArg(2)
# PCIP    = "192.168.0.29"

#=============================================================================
#  Mandatory items : Can edit the values but do not comment out
# =============================================================================
username = "root"
password = "Broadcom"

# device_tree = "rg.3390b0-smwvg.dtb"
initrd = "vmlinuz-initrd-3390b0-lattice-4.9"
initrd_file	= binaries_dir + initrd

factorydefault = True # True for doing factory default, False for skipping it

#=============================================================================
#  Optional items : Can comment out if you want to skip downloading
# =============================================================================
# bolt = "bolt-v4.00_B1-3390b0-xx-bfw-x.x.x.bin"

kernel = "vmlinuz-3390b0"
kernel_file	= binaries_dir + kernel

cm_img = "ubifs-128k-2048-3390b0-CM.img"
cm_img_file	= binaries_dir + cm_img

rg_img = "ubifs-128k-2048-3390b0-RG.img"
rg_img_file	= binaries_dir + rg_img

# device_tree_tgz = "rg.3390b0.dtb.tgz"

Bolt_Prompt = "BOLT>"
Initrd_Prompt = "# "

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
	crt.Screen.IgnoreEscape = True
	crt.Screen.Synchronous = True

	if not os.path.exists(initrd_file):
		return

	if not os.path.exists(kernel_file):
		return

	if not os.path.exists(cm_img_file):
		return

	if not os.path.exists(rg_img_file):
		return

	if not login_rg_console():
		return

	crt.Screen.Send('\r')
	crt.Screen.Send('reboot\r')
	crt.Screen.WaitForString('AVS init OK')
	count = 1
	while True and (count < 30):
		crt.Screen.Send(chr(0x03))
		count+=count
	crt.Screen.Send('\r')

	wait_enter_bolt()
	bolt_send_cmd_wait_resp('wd -disable')
	bolt_send_cmd_wait_resp('ifconfig eth0 -addr=' + RGIP)

	# flash bolt
	if 'bolt' in globals():
		bolt_send_cmd_wait_resp('flash ' + PCIP + ':' + bolt + ' flash0.bolt')
		crt.Screen.Send('reboot\r')

		wait_enter_bolt()
		bolt_send_cmd_wait_resp('ifconfig eth0 -addr=' + RGIP)

	if (not 'kernel' in globals() and
		not 'cm_img' in globals() and
		not 'rg_img' in globals() and
		not 'device_tree_tgz' in globals() and
		not factorydefault ):
		end_download()
		return

	#load device tree onto ram
	#bolt_send_cmd_wait_resp('load -nz -raw -addr=$DT_ADDRESS -max=0x10000 '
	#				   + PCIP + ':' + device_tree)
	bolt_send_cmd_wait_resp('load -nz -raw -addr=$DT_ADDRESS -max=0x10000 flash0.devtree0')

	#boot with initrd image
	send_cmd_wait_resp('boot ' + PCIP + ':' + initrd, "==============================")

	#wait to enter initrd shell
	result = crt.Screen.WaitForStrings(['(none) login:', "# "])
	if (result == 1):
		crt.Screen.Send(username + '\r')
		crt.Screen.WaitForString('Password:')
		crt.Screen.Send(password + '\r')

	crt.Sleep(1000)

	cmds = [
			"modprobe -q ethsw.ko",
			"modprobe -q mdio-bcm-unimac.ko",
			"mknod /dev/bdmf_shell c 215 0",
			"modprobe -q bdmf.ko bdmf_chrdev_major=215",
			"modprobe -q rdpa_gpl.ko",
			"modprobe -q rdpa_cm.ko",
			"modprobe -q rdpa.ko",
			"modprobe -q dqnet_rfap.ko",
			"modprobe -q dqnet_gfap.ko",
			"modprobe dqnet.ko",
			"brctl addbr br0",
			"brctl addif br0 eth0",
			"brctl addif br0 eth1",
			"brctl addif br0 eth2",
			"brctl addif br0 eth3",
			"brctl addif br0 cm0",
			"ifconfig eth0 up",
			"ifconfig eth1 up",
			"ifconfig eth2 up",
			"ifconfig eth3 up",
			"ifconfig cm0 up",
			"ifconfig br0 up",
			"modprobe nf_conntrack",
			"modprobe nf_defrag_ipv4",
			"modprobe nf_conntrack_ipv4",
			"modprobe flowmgr",
			"echo 1 > /proc/sys/net/netfilter/nf_conntrack_acct",
			"echo 1 > /proc/sys/net/ipv4/netfilter/ip_conntrack_tcp_be_liberal",
			"echo fap_enable 1 > /proc/driver/flowmgr/cmd",
			"echo 1 > /proc/sys/net/flowmgr/enable",
			"source /etc/init.d/rcS.util",
			"mount_by_name flash0.cmnonvol0 jffs2 /mnt/cmnonvol",
			"mount_by_name flash0.rgnonvol0 jffs2 /data",
			"ethtool --set-eee eth0 eee off"
			]
	for cmd in cmds:
		send_cmd_wait_resp(cmd, Initrd_Prompt)

	#assign ip address to RG
	send_cmd_wait_resp('ifconfig br0 ' + RGIP, Initrd_Prompt)

	# bootarg
	cmd = "boltenv -s STARTUP" + \
		" '" + \
		"load -nz -raw -addr=$DT_ADDRESS -max=0x10000 flash0.devtree$DT_IDX;boot flash1.kernel$KL_IDX" + \
		' "' + \
		"ubi.mtd=flash1.rg$RG_IDX rootfstype=ubifs root=ubi0:rootfs platformboot ubifs_apps jffs2_data coherent_pool=1M" + \
		'"' + "'"
	crt.Screen.Send(cmd + '\r')
	crt.Screen.WaitForString('successfully' + '\r')
	crt.Screen.WaitForString(Initrd_Prompt)

	crt.Sleep(3000)

	# flash kernel
	if 'kernel' in globals():
		tftp_send_cmd_wait_resp('tftp -g '
								+ PCIP
								+ ' -r '
								+ kernel
								+ ' -l /tmp/vmlinuz',
								Initrd_Prompt)
		send_cmd_wait_resp('flash_erase /dev/mtd0 0 0', Initrd_Prompt)
		send_cmd_wait_resp('nandwrite -p /dev/mtd0 /tmp/vmlinuz', Initrd_Prompt)
		send_cmd_wait_resp('rm /tmp/vmlinuz', Initrd_Prompt)

		cmds = ["boltenv -s KL_IDX 0",
				"set_springevent_var SPRINGEVENT KL 1",
				"set_springevent_var SPRINGEVENT STBUTIL 1"]
		for cmd in cmds:
			send_cmd_wait_resp(cmd, Initrd_Prompt)

	# flash cm image
	if 'cm_img' in globals():
		tftp_send_cmd_wait_resp('tftp -g '
								+ PCIP
								+ ' -r '
								+ cm_img
								+ ' -l /tmp/cm',
								Initrd_Prompt)
		send_cmd_wait_resp('ubiformat /dev/mtd2 --yes --flash-image=/tmp/cm',
						   Initrd_Prompt)
		send_cmd_wait_resp('rm /tmp/cm', Initrd_Prompt)
		send_cmd_wait_resp('boltenv -s CM_IDX 0', Initrd_Prompt)

	# flash rg image
	if 'rg_img' in globals():
		tftp_send_cmd_wait_resp('tftp -g '
								+ PCIP
								+ ' -r '
								+ rg_img
								+ ' -l /tmp/rg',
								Initrd_Prompt)
		send_cmd_wait_resp('ubiformat /dev/mtd4 --yes --flash-image=/tmp/rg',
						   Initrd_Prompt)
		send_cmd_wait_resp('rm /tmp/rg', Initrd_Prompt)

		cmds = ["boltenv -s RG_IDX 0",
				"set_springevent_var SPRINGEVENT RG 1",
				"set_springevent_var SPRINGEVENT STBUTIL 1"]
		for cmd in cmds:
			send_cmd_wait_resp(cmd, Initrd_Prompt)

	# flash device_tree_tgz
	if 'device_tree_tgz' in globals():
		tftp_send_cmd_wait_resp('tftp -g '
								+ PCIP
								+ ' -r '
								+ device_tree_tgz
								+ ' -l /tmp/dt',
								Initrd_Prompt)
		send_cmd_wait_resp('flash_erase /dev/mtd11 0 0', Initrd_Prompt)
		send_cmd_wait_resp('dd if=/tmp/dt of=/dev/mtd11', Initrd_Prompt)
		send_cmd_wait_resp('rm /tmp/dt', Initrd_Prompt)

		cmds = ["boltenv -s DT_IDX 0",
				"set_springevent_var SPRINGEVENT DT 1",
				"set_springevent_var SPRINGEVENT STBUTIL 1"]
		for cmd in cmds:
			send_cmd_wait_resp(cmd, Initrd_Prompt)

	if factorydefault:
		# Display a messagebox with Yes/No buttons.
		# Make the 'No' button the default.
		crt.Sleep(1000)
		send_cmd_wait_resp('rm -f /data/mdm-backup.config', Initrd_Prompt)
		send_cmd_wait_resp('rm -f /data/mdm.config', Initrd_Prompt)
		send_cmd_wait_resp('rm -f /mnt/cmnonvol/cm_dyn.bin', Initrd_Prompt)

	end_download()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end_download():
	crt.Screen.Send('\r')
	crt.Screen.Send('reboot\r')
	# crt.Dialog.MessageBox('Download Completed!')
	os.system("taskkill /f /im SecureCRT.exe")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# initrd console echo back by spliting a long line into multiple 80-col lines
def smart_wait_string(string):
	# 첫번째 line 처리: 현재 cursor의 위치를 감안한다.
	# 현재의 column number (1-based)
	c = crt.Screen.CurrentColumn
	if ((c + len(string)) > 80):
	   str1 = string[:(80-c)]
	   crt.Screen.WaitForString(str1 + '\r')
	   string = string[(80-c+1):]
	# 중간 lines 처리
	while (len(string) > 80):
		str1 = string[:79]
		crt.Dialog.MessageBox(str(c))
		crt.Dialog.MessageBox(str1)
		crt.Screen.WaitForString(str1 + '\r')
		string = string[80:]
	# 마지막 line 처리
	if (len(string) > 0):
	   crt.Screen.WaitForString(string)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def wait_enter_bolt():
	# crt.Screen.WaitForString('AVS init OK')
	crt.Screen.WaitForString('Automatic startup canceled via Ctrl-C')
	while True:
		crt.Screen.Send(chr(0x03))
		if True == crt.Screen.WaitForString(Bolt_Prompt, 1):
			break
	crt.Sleep(1000)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def send_cmd_wait_resp(cmd, resp):
	crt.Screen.Send(cmd + '\r')
	#crt.Screen.WaitForString(cmd + '\r')
	smart_wait_string(cmd + '\r')
	crt.Screen.WaitForString(resp)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def bolt_send_cmd_wait_resp(cmd):
	crt.Screen.Send(cmd + '\r')
	crt.Screen.WaitForString(cmd + '\r')
	crt.Screen.WaitForString('*** command status = ')
	result = crt.Screen.ReadString(Bolt_Prompt)
	if int(result) < 0:
		crt.Dialog.MessageBox('Command failed: result=' + str(result), 'Error')
		# sys.exit(-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tftp_send_cmd_wait_resp(cmd, promptString):
	crt.Screen.Send(cmd + '\r')
	#crt.Screen.WaitForString(cmd + '\r')
	smart_wait_string(cmd + '\r')
	result = crt.Screen.ReadString(promptString)
	if 'tftp: server error' in result:
		crt.Dialog.MessageBox('Command failed:' + result, 'Error')
		# sys.exit(-1)
	if 'tftp: timeout' in result:
		crt.Dialog.MessageBox('Command failed:' + result, 'Error')
		# sys.exit(-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def login_rg_console():
    US      = "root"
    PW      = "humax@!0416"

    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString("OpenWrt login:", 1) == True):
        crt.Screen.Send(US + '\r')
    if (crt.Screen.WaitForString("Password:", 1) == True):
        crt.Screen.Send(PW + '\r')

    if not in_RG_console():
        return False
    else:
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def in_RG_console():
    crt.Screen.Send('\r')
    if (crt.Screen.WaitForString("RG]#", 1) == True):
        return True
    else:
        return False

main()
