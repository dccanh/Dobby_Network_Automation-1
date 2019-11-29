import sys
sys.path.append('../')
"""
$language: python
$version: 3.7

Elements file:
    variable = value

All variables is global variable and all of them imported in Test file to get "value".
Value is a web element of 2 type: xpath and css selector
We define type of them in Test file as find_element_by_xpath and find_element_by_css_selector

"""

# ~~~~~~~~~~~~~~~~ LOGIN
lg_welcome_text = '.login-block>form>h1'
lg_page = '.login-page'
lg_user = '#login'
lg_password = '#password'
lg_captcha_src = '.captcha-img>img'
lg_captcha_box = 'input#uword'
lg_btn_login = 'button.button-login'
lg_extra_info = '.extra-info>span'
lg_privacy_policy_pop = '#privacy-dialog-id'
lg_company_img = '.login-page>.company>a'
lg_msg_error = '.login-page .msg-error'
# ~~~~~~~~~~~~~~~~~ WELCOME
lg_welcome_header = 'span.header-text'
welcome_language = '.selected'
welcome_list_language = '.selected .custom-select-list>ul>li span'
welcome_time_zone = '.selected+.selected'
welcome_list_time_zone = '.selected+.selected .custom-select-list>ul>li span'
welcome_start_btn = '#wizard-step-id button.start'
welcome_next_btn = '#wizard-step-id button.next'
welcome_let_go_btn = '#wizard-step-id button.summary'
welcome_change_pw_fields = '.text-wrap .password-input input'
# ~~~~~~~~~~~~~~~~~ REDIRECT
network_tab = 'a[href="/network"]'
network_internet_tab = 'a[href="/network/internet"]'
network_lan_tab = 'a[href="/network/lan"]'
network_operationmode_tab = 'a[href="/network/operationmode"]'
home_tab = 'a[href="/home"]'
wireless_tab = 'a[href="/wireless"]'
wireless_primarynetwork_tab = 'a[href="/wireless/primarynetwork"]'
wireless_guestnetwork_tab = 'a[href="/wireless/guestnetwork"]'
wireless_wps_tab = 'a[href="/wireless/wps"]'
media_share_tab = 'a[href="/mediashare"]'
media_share_usb_tab = 'a[href="/mediashare/usb"]'
media_share_server_settings_tab = 'a[href="/mediashare/serversetting"]'
current_tab_chosen = '#parent-menu:not(.hide)>#sub-menu>a.active'

security_tab = 'a[href="/security"]'
security_parentalcontrol_tab = 'a[href="/security/parentalcontrol"]'
security_firewall_tab = 'a[href="/security/firewall"]'
security_vpn_tab = 'a[href="/security/vpn"]'
security_filtering_tab = 'a[href="/security/filtering"]'
security_selfcheck_tab = 'a[href="/security/selfcheck"]'
# ~~~~~~~~~~~~~~~~~ NETWORK
ip_address_input_filed = 'div.ip-address [name="input-field"]'
start_end_ip_address = '.ip-class-c .input-field input'

dual_wan_input = '.dual-wan-card .wrap-input input'
dual_wan_button = '.dual-wan-card .wrap-input .toggle-button'
dual_wan_ls_fields = '.dual-wan-card .wrap-input'
active_drop_down_values = '.custom-select-list.active>ul>li>button>span'
dual_wan_apply_btn = '.dual-wan-card button.active-button'
internet_setting_block = '.internet-dual-setting-card'
internet_setting_block_single = '.internet-setting-card'
text_field_required = '//*[text()="This field is required"]'
page_network = '.view-wrap.network'
# ~~~~~~~~~~~~~~~~~ WIRELESS
fields_in_2g = '.left .wrap-form'
label_name_in_2g = '.wrap-label>.input-label'
label_value_in_2g = '.wrap-input input'
secure_value_field = '[name=security]'
secure_value_in_drop_down = 'ul>li'
password_eye = '.password-eye'
password_error_msg = '.password .error-message'
encryption_value_field = '[name=encryption]'

# ~~~~~~~~~~~~~~~~ MEDIA SHARE
usb_class = '.usb'
usb_network = '.usb .network-folder'
select_folder_item = '.select-folder-content .item'
permission_write_check_box = '.read-write #custom-checkbox-write-add'
permission_write_check_box_radio = '.read-write [for=custom-checkbox-write-add]'
permission_read_check_box = '.read-write #custom-checkbox-read-add'
permission_read_check_box_radio = '.read-write [for=custom-checkbox-read-add]'
tree_icon = '.tree-icon'
path_name_lv1 = '.item-level-1>li .path-name>span'
action_edit = '.action .edit'
action_delete = '.action .delete'

permission_write_check_box_first_row = '.read-write #custom-checkbox-write-0'
permission_write_check_box_radio_first_row = '.read-write [for=custom-checkbox-write-0]'
permission_read_check_box_first_row = '.read-write #custom-checkbox-read-0'
permission_read_check_box_radio_first_row = '.read-write [for=custom-checkbox-read-0]'

ftp_server = '.left .ftp-card'
media_item = '.media-item'

# ~~~~~~~~~~~~~~~~~ SECURITY
parental_code_card = '.parenatal-code-card'
parental_popup_label = '.content-wrap .pin-item>.title'
parental_popup_input = '.content-wrap .pin-item input'
parental_popup_title = '.dialog-content .description-wrap'
parental_wrap_input = '.content-wrap .pin-wrap input'
security_page = '.security'
parental_pop_init_pw = '.parental-create-password-dialog'
# ~~~~~~~~~~~~~~~~ SYSTEM
system_btn = '[title=System]'
sys_language = '[title=System]+ul>li:nth-child(1)>button'
sys_reset = '[title=System]+ul>li:nth-child(6)>button'
sys_pop_factory_reset = '#factory-popup .bottom-button>button'
language_selected_text = '#language-popup .option-selected-text>span'
list_language_option = '#language-popup ul>li>button>span'
pop_up_btn_apply = '#language-popup button.active-button'


# ~~~~~~~~~~~~~~.internet-dual-setting-card~~ DIALOG
btn_ok = 'button.confirm'
dialog_loading = '.dialog-body>.loading'
btn_cancel = 'button.cancel'

# ~~~~~~~~~~~~~~~~ HOME
home_view_wrap = 'div.view-wrap.home'
home_img_connection = 'div.wan-connection>a.img-connection'
home_connection_description = 'div.wan-connection>.text-description'
home_wan_ls_fields = '.wrap-form'
home_wan_ls_label = 'label.input-label'
home_wan_ls_value = 'span.text-label'
home_icon_fab = '.icon-fab'
home_icon_more_fab = 'button.more-fab'
home_conection_img_wan_ip = '.wan-connection .more-info'
left = '.left'
right = '.right'
wrap_input = '.wrap-input'
input = 'input'
apply = 'button.active-button'
select = '.toggle-button'
label = '.input-label'
input_pw = 'input[type=password]'
confirm_dialog_msg = '.confirm-dialog-message'
google_img = 'img[alt=Google]'
add_class = '.add'
edit_mode = '.edit-mode'
description = '.description'
path = '.path'
btn_save = 'button.save'
tbody = 'tbody'
table_row = 'tr'
error_message = '.error-message'
status = '.status'
complete_dialog_msg = '.complete-dialog-message'
error_text = '.error-text'
dialog_content = '.dialog-content'