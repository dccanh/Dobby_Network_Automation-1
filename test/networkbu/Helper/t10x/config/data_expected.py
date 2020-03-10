import sys
sys.path.append('../')
from Helper.t10x.common import get_config
"""
$language: python
$version: 3.7

Expected file:
    variable = value(s)

All variables is global variable and all of them imported in Test file to get "value" as Expected result

"""

return_true = True
return_false = False

# ~~~~~~~~~~~~~~~~~~~~~~~~`
exp_time_out_msg = 'Automatically logs out after 20 minutes of inactivity.'
exp_tooltip_logout = 'Logout'
exp_logout_msg = 'Do you want to log out?'
# ~~~~~~~~~~~~~~~~~~~~~~~ URL redirect
homepage = '/homepage'
network_internet = '/network/internet'
network_lan = '/network/lan'
wireless_primary = '/wireless/primarynetwork'
# ~~~~~~~~~~~~~~~~~~~~~~~ Console
connect_wifi_msg = 'Connection request was completed successfully.'
disconnect_wifi_msg = 'Disconnection request was completed successfully for interface "Wi-Fi".'

expected_welcome_text_en = 'WELCOME!'
expected_welcome_text_vi = 'CHÀO MỪNG!'

exp_lg_id_holder = 'Enter the router login ID'
exp_lg_password_holder = 'Enter the Password'
exp_lg_captcha_holder = 'Enter the text below'
exp_lg_extra_info = 'For the default Router Login ID and Password \nsee the label of the product.'
exp_tooltip_img = 'http://quantum.humaxdigital.com/'
exp_quantum_url = 'quantum.humaxdigital.com'
exp_wrong_captcha = 'Incorrect security code'
exp_wrong_id_pw = 'Router login ID or password is not correct.'
# ~~~~~~~~~~~~~~~~~~~~~~~ Welcome
exp_time_zone = '(GMT+07:00) Bangkok, Ho Chi Minh, Phnom Penh, Vientiane'
exp_language = 'English'
# header_login_text = 'Welcome to HUMAX T10X'
header_login_text = 'Welcome to ' + get_config('GENERAL', 'model')
exp_welcome_msg_up = 'Edit your settings simply and easily to optimize your network environment and configure various functions.'
exp_internet = 'Internet Setup'
exp_wireless = 'Wireless Setup'
exp_changepw = 'Change Password'
exp_welcome_msg_down = 'Please select your language and time zone.'

exp_change_pw_title = 'Change Login Password'
exp_change_pw_msg = 'Change the login password for security.\nFor the default router login password see the label of the product.\nThe new login password will take effect the next login.'
exp_current_pw_error_msg = 'Password is not correct'
exp_retype_new_pw_error_msg = 'Password does not match'
exp_internet_setup_guide = 'You can manually configure your internet settings.\nIf you do not know the Internet connection type, please contact your ISP'
exp_internet_setup_error_msg = 'Internet cable is unplugged. Please check your internet cable first.'

# ~~~~~~~~~~~~~~~~~~~~~~~ Wireless
exp_ssid_2g_default_val = 'We Love You So Much_2G!'
exp_ssid_5g_default_val = 'We Love You So Much_5G!'
exp_ssid_placeHolder = 'Enter the network name (SSID)'
exp_password_error_msg = 'More than 8 characters.'
exp_dialog_hide_ssid_title = 'If the Hide SSID is enabled, WPS function is inactivated.'
exp_dialog_add_same_ssid = 'The Network Name(SSID) already exists. Enter another Network Name(SSID).'
exp_wl_default_pw = '00000000'
exp_short_pw_error_msg = "That's too short."
exp_wps_red_message = "If both Hide SSIDs on both wireless networks are set to on, WPS is disabled."

# ~~~~~~~~~~~~~~~~~~~~~~ Media share
exp_nw_folder_exist = 'The same network folder exists.'
exp_max_row_usb_nw = 8
exp_confirm_msg_edit = 'Cannot edit while server is running.\nTurn off the server and try again.'
exp_confirm_msg_delete = 'Do you want to stop sharing FTP and media server?'
exp_account_id_exist = 'The same ID exists'
exp_account_null_id = 'This field is required.'
exp_account_not_available = 'This ID is not available.'
exp_delete_account_when_server_running = 'The server is running under the account. If you delete this item, the related server will no longer work. Continue?'
exp_server_account_warning = 'Create an account first. Go to Account Setting.'
exp_server_folder_warning = 'Create a network folder first. Go to Network Folder Setting.'
# ~~~~~~~~~~~~~~~~~~~~~ Security
exp_ls_parental_label = ['New Parental Code', 'Retype New Parental Code']
exp_parental_pop_up_title = 'Enter the Parental Code.'
exp_parental_error_msg = 'Incorrect Parental Code.'
exp_ls_service_filter_items_value = ['Social Network[1]', 'User Define[1]']
exp_block_schedule_value = 'Only Specific Time'


# ~~~~~~~~~~~~~~~~~~~~~ Network
exp_nw_subnet_type_c = ['255.255.255.0']
exp_nw_subnet_type_b = ['255.255.255.0', '255.255.0.0']
exp_nw_subnet_type_a = ['255.255.255.0', '255.255.0.0', '255.0.0.0']
exp_error_msg_start_less_end = 'Start IP address should be smaller than End IP address.'
exp_error_msg_start_end_small = 'The DHCP range is too small. The minimum range is at least 32.'
exp_error_msg_start_end_same_lan_ip = 'Enter another IP address. Can not same as the LAN IP address.'
exp_error_msg_start_end_include_lan_ip = 'LAN IP address must be outside DHCP range. Change the LAN IP Address or DHCP Start/End Address.\nOK'
exp_reserved_device_placeholder = 'Select the device'
exp_reserved_maximum_rules = '32'
exp_mac_address_exists = 'This MAC Address already exists.'
exp_ip_address_exists = 'This IP Address already exists.'
exp_out_of_start_end_ip = 'Enter a number between Start IP Address and End IP Address.'

# ~~~~~~~~~~~~~~~~~~~~~ Advanced
exp_destination_same_lan_ip_error_msg = 'Enter another IP address. Cannot same as the LAN IP address.'
exp_warning_local_port_same_external = 'The number of Local Ports must be the same as that of External Ports.'
exp_add_local_external_port_exist = 'This Local Port/External Port already exists.'
exp_none_text = ''
exp_error_msg_ip_same_lan_ip = 'Enter another IP address. Cannot same as the LAN IP address.'

# ~~~~~~~~~~~~~~~~~~~~ System
# exp_backup_file_name = 'Setting_HUMAX T10X.bin'
exp_backup_file_name = f'Setting_{get_config("GENERAL", "model")}.bin'
exp_backup_confirm_msg = 'Do you want to back up the current setting file?'
exp_restore_confirm_msg = 'Do you want to restore to the selected file? Restart the system to apply the changes.'



# ~~~~~~~~~~~~~~~~~~~~ HOME
exp_confirm_msg_add_resserve_ip = 'Do you want to reserve IP Address?'
exp_confirm_msg_delete_resserve_ip = 'Do you want to delete this item?'

exp_confirm_msg_add_mac_filtering = 'Do you want to add this MAC Address to MAC Filtering List?'