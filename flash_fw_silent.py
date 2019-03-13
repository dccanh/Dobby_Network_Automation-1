#$language = "python"
#$interface = "1.0"
import os
import sys


script_dir = crt.Arguments.GetArg(0)

#=============================================================================
#  IP Address
# =============================================================================
# RGIP    = "192.168.0.11"
RGIP    = crt.Arguments.GetArg(1)
Netmask = "255.255.255.0"
PCIP    = crt.Arguments.GetArg(2)
# PCIP    = "192.168.0.29"

#=============================================================================
#  Optional items : Can comment out if you want to skip downloading
# =============================================================================
# images are stored in primary bank and system boots from there
rg_kernel 		= "rg_kernel.bin"
rg_kernel_file 	= script_dir + rg_kernel
cm_img 			= "cm_image.bin"
cm_img_file 	= script_dir + cm_img
rg_apps 		= "rg_app.bin"
rg_apps_file 	= script_dir + rg_apps

#=============================================================================
#  Mandatory items : Can edit the values but do not comment out
# =============================================================================
CM_Prompt	= "CM> "
BL_Enter	= "Enter \'a\' (primary), \'b\' (secondary), \'o\' (old-school boot), or \'p\' (prompt)"
BL_Prompt	= "Main Menu:"
Prompt 		= "z) Reset"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
	global rg_kernel
	global cm_img
	global rg_apps

	rg_kernel_found = False
	cm_img_found = False
	rg_apps_found = False

	crt.Screen.IgnoreEscape = True
	crt.Screen.Synchronous = True

	crt.Screen.Send('\r')
	if (crt.Screen.WaitForString(CM_Prompt) == True):
		crt.Screen.Send('reset\r')
	if (crt.Screen.WaitForString(BL_Enter) == True):
		crt.Screen.Send('p')

	if 'rg_kernel' in globals():
		rg_kernel_found = os.path.isfile(rg_kernel_file)
		if not rg_kernel_found:
			return

	if 'rg_apps' in globals():
		rg_apps_found = os.path.isfile(rg_apps_file)
		if not rg_apps_found:
			return

	if 'cm_img' in globals():
		cm_img_found = os.path.isfile(cm_img_file)
		if not cm_img_found:
			return

	if (not rg_kernel_found and
		not rg_apps_found and
		not cm_img_found):
		return

	wait_enter_bootloader()
	setup_network_parameters()

	# flash rg_kernel
	if rg_kernel_found: upgrade_one_image(rg_kernel, "3")

	# flash rg_apps image
	if rg_apps_found: upgrade_one_image(rg_apps, "4")

	# flash cm image
	if cm_img_found: upgrade_one_image(cm_img, "1")

	# Back to Default
	send_receive_string("c", Prompt)
	end_download()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def end_download():
	# Send key to reset
	crt.Screen.Send('z')
	# crt.Quit()
	os.system("taskkill /f /im SecureCRT.exe")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def wait_enter_bootloader():
	crt.Screen.WaitForString(BL_Prompt)
	while True:
		result = crt.Screen.WaitForStrings([Prompt, 'Board IP Address'], 1)
		if (result == 1): break;
		elif (result == 2):
			send_cmd_wait_resp(RGIP, "]: ")
			send_cmd_wait_resp(Netmask, "]: ")
			send_cmd_wait_resp(RGIP, "]: ")
			send_cmd_wait_resp("", "(e/i/a)[a]")
			send_cmd_wait_resp("", Prompt)
			break;
		else: crt.Screen.Send('p')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setup_network_parameters():
	send_receive_string("i", "]: ")
	send_cmd_wait_resp(RGIP, "]: ")
	send_cmd_wait_resp(Netmask, "]: ")
	send_cmd_wait_resp(RGIP, "]: ")
	send_cmd_wait_resp("", "(e/i/a)[a]")
	send_cmd_wait_resp("", Prompt)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def upgrade_one_image(filepath, part_num):
	send_receive_string("d", "]: ")
	send_cmd_wait_resp(PCIP, "]: ")

	crt.Screen.Send(filepath + '\r')
	ok = ')[2]:'
	err1 = 'Sending "Retry limit exceeded" error packet'
	err2 = 'Received Error Code 1: File not found'
	result = crt.Screen.WaitForStrings([ok, err1, err2])
	if (result == 1):
		send_cmd_wait_resp(part_num, "Store parameters to flash? [n]")
		send_cmd_wait_resp("n", Prompt)
	elif (result == 2):
		crt.Quit()
	elif (result == 3):
		crt.Quit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def send_receive_string(cmd, resp):
	crt.Screen.Send(cmd)
	crt.Screen.WaitForString(resp)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def send_cmd_wait_resp(cmd, resp):
	crt.Screen.Send(cmd + '\r')
	crt.Screen.WaitForString(cmd + '\r')
	crt.Screen.WaitForString(resp)

main()


