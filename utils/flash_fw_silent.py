#$language = "python"
#$interface = "1.0"

import os
import sys

script_dir = crt.Arguments.GetArg(0)

#=============================================================================
# RGIP    = "192.168.0.11"
RGIP    = crt.Arguments.GetArg(1)
Netmask = "255.255.255.0"
PCIP    = crt.Arguments.GetArg(2)
# PCIP    = "192.168.0.29"

# =============================================================================
cm_img 			= "cm_image.bin"
cm_img_file 	= script_dir + cm_img
rg_apps 		= "rg_app.bin"
rg_apps_file 	= script_dir + rg_apps
rg_kernel 		= "rg_kernel.bin"
rg_kernel_file 	= script_dir + rg_kernel

# =============================================================================
CM_Prompt	= "CM> "
BL_Enter	= "Enter \'a\' (primary), \'b\' (secondary), \'o\' (old-school boot), or \'p\' (prompt)"
BL_Prompt	= "Main Menu:"
Part_Prompt = "Flash Partition information:"
Prompt 		= "z) Reset"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def flash_fw_silent_main():
	cm_img_found = False
	rg_apps_found = False
	rg_kernel_found = False

	crt.Screen.IgnoreEscape = True
	crt.Screen.Synchronous = True

	cm_img_found = os.path.exists(cm_img_file)
	if not cm_img_found:
		return

	rg_apps_found = os.path.exists(rg_apps_file)
	if not rg_apps_found:
		return

	rg_kernel_found = os.path.exists(rg_kernel_file)
	if not rg_kernel_found:
		return

	crt.Screen.Send('\r')
	if (crt.Screen.WaitForString(CM_Prompt, 1) == True):
		crt.Screen.Send('reset\r')
		if (crt.Screen.WaitForString(BL_Enter) == True):
			crt.Screen.Send('p')
		setup_network_parameters()
	else:
		crt.Screen.Send('p')
		if (crt.Screen.WaitForString(Part_Prompt) == True):
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
	os.system("taskkill /f /im SecureCRT.exe")

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

flash_fw_silent_main()
