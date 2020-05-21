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
welcome_change_pw_label = '.password-wrap .wrap-label'
welcome_msg_up = 'li.text-wrap'
welcome_msg_down = 'div.text-bold-decoration'
welcome_first_pic = '.step-summary>.first'
welcome_second_pic = '.step-summary>.second'
welcome_third_pic = '.step-summary>.third'
welcome_language_wz = '.language-dialog-select'
welcome_timezone_wz = '.datetime-dialog-select'
change_pw_msg = '.guide-msg'
change_pw_default_login_id = '.text-info'
welcome_current_pw_error_msg = '.origin-password .error-message'
welcome_internet_setup1_guide = '.align-text>p:not([style="display: none;"])'
welcome_internet_setup1_ls_option_connection_type = 'li[option-value] span.text'
ele_welcome_router_box ='#operationMode'
ele_welcome_connection_box = '#connectionType'
ele_internet_setup_error_msg = '.error'
ele_internet_setup_title = '.width-step'
ele_wizard_wl_block = '.card-wizard'
ele_wizard_wl_2g_pw = '[id="24-input-value-lable"]'
ele_wizard_wl_5g_pw = '[id="5-input-value-lable"]'
ele_wizard_step = '.wizard-step'
ele_wizard_check_same_pw = '.checkbox-text'
ele_wizard_checkbox_status = 'input.custom-checkbox'
ele_wizard_template = '.wizard-step .wizard-template'
ele_wizard_check_same_pw_input = 'input[name="square-check-box-template"]'
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
wireless_repeater_setting_tab = 'a[href="/wireless/repeater"]'

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

advanced_tab = 'a[href="/advanced"]'
advanced_network_tab = 'a[href="/advanced/network"]'
advanced_wireless_tab = 'a[href="/advanced/wireless"]'
advanced_iptv_tab = 'a[href="/advanced/iptv"]'
advanced_ddnswol_tab = 'a[href="/advanced/ddnswol"]'
advanced_portforwarding_tab = 'a[href="/advanced/portforwarding"]'
advanced_porttriggering_tab = 'a[href="/advanced/porttriggering"]'
advanced_diagnostics_tab = 'a[href="/advanced/diagnostics"]'
advanced_upnp_tab = 'a[href="/advanced/upnp"]'

qos_tab = 'a[href="/advanced/qos"]'
# ~~~~~~~~~~~~~~~~~ NETWORK
ip_address_input_filed = 'div.ip-address [name="input-field"]'
start_end_ip_address = '.ip-class-c .input-field input'
dual_wan_block_ele = '.dual-wan-card'
dual_wan_input = '.dual-wan-card .wrap-input input'
dual_wan_button = '.dual-wan-card .wrap-input .toggle-button'
dual_wan_ls_fields = '.dual-wan-card .wrap-input'
active_drop_down_values = '.custom-select-list.active>ul>li>button>span'
dual_wan_apply_btn = '.dual-wan-card button.active-button'
internet_setting_block = '.internet-dual-setting-card'
internet_setting_block_single = '.internet-setting-card'
text_field_required = '//*[text()="This field is required"]'
page_network = '.view-wrap.network'
network_lan_card = '.network-lan-card'
network_reserved_ip_card = '.ip-reserved-card'
ele_wan_block = '.wan-card'
ele_reserve_ip_addr_input = '.ip-address input'
ele_router_mode_input = '#router-mode-radio'
ele_select_router_mode = '#router-mode-radio+label'
ele_select_bridge_mode = '.access-point-mode [for]'
ele_bridge_mode_input = '#access-point-mode-radio'
ele_select_repeater_mode = '.repeater-mode [for]'
ele_select_ap_mode = '#mesh-ap-mode-radio +label'
ele_repeater_mode_input = '.repeater-mode input'
ele_lan_ip_input_not_disabled = '[name="input-field"]:not([disabled])'
ele_lan_ip_first_start_end_ip = '.octet-wrap'
ele_ip_address_range_input = '.dot-span+.form-group input'
ele_repeater_mode_card = '.repeater-step-one'
ele_card_title = '.card-title>h3'
# ~~~~~~~~~~~~~~~~~ WIRELESS
fields_in_2g = '.left .wrap-form'
label_name_in_2g = '.wrap-label>.input-label'
label_value_in_2g = '.wrap-input input'
secure_value_field = '[name=security]'
encryption_value_field = '[name=encryption]'
key_type_value_field = '#firstOctet'
secure_value_in_drop_down = 'ul>li'
password_eye = '.password-eye'
password_error_msg = '.password .error-message'

guest_network_block = '.guestnetwork'
wl_primary_card = '.primary-card'
ele_wl_ssid_value_field = '[name="input-field"]'
ele_wl_nw_name_ssid = '.network-name-col'
ele_wl_security_guest_nw = '.security-col'
ele_wl_wps_inform = '.inform'
ele_wps_button = 'button.active-wps-button'
ele_btn_select_disable = '.toggle-disable'
ele_block_card = '.access-content'
ele_access_control_card = '.access-control-card'
ele_wps_status = '.wps-status-message'
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

account_setting_card = '.account-setting-card'

permission_write_check_box_first_row = '.read-write #custom-checkbox-write-0'
permission_write_check_box_radio_first_row = '.read-write [for=custom-checkbox-write-0]'
permission_read_check_box_first_row = '.read-write #custom-checkbox-read-0'
permission_read_check_box_radio_first_row = '.read-write [for=custom-checkbox-read-0]'
account_link_cls = '.account-link'
ftp_server = '.left .ftp-card'
media_item = '.media-item'
samba_server_card = '.window-network-card'
dlna_server_card = '.dlna-card'
dev_dav_server_card = '.dev-dav-card'
torrent_server_card = '.torrent-card'
time_machine_server_card = '.time-machine-card'
ele_usb_title = '.usb-title-page'
ele_sub_title = '.sub-title-page'
ele_usb_mediashare_block_title = '.mediashare h3'
ele_usb_space_available = '.space-available'
ele_usb_space_total = '.space-total'
# ~~~~~~~~~~~~~~~~~ SECURITY
parental_code_card = '.parenatal-code-card'
parental_popup_label = '.content-wrap .pin-item>.title'
parental_popup_input = '.content-wrap .pin-item input'
parental_popup_title = '.dialog-content .description-wrap'
parental_wrap_input = '.content-wrap .pin-wrap input'
security_page = '.security'
parental_pop_init_pw = '.parental-create-password-dialog'

parental_rule_card = '.parental-rule-card'
service_filter_items = '.service-filter .filter-item'
block_schedule = 'td.schedule>span'

ele_firewall_medium = '.medium'
ele_firewall_lv_medium = '.circle-icon.medium'
ele_security_check_parental = '.toggle-right'

ele_ip_port_filtering = '.ip-port-filtering-card'
ele_port = '.port'
ele_protocol = '.protocol '

ele_mac_filtering = '.mac-filtering-card'
ele_mac_device_name = '.device-name'

ele_security_check_block = '.security-check-dialogue'
# ~~~~~~~~~~~~~~~~ ADVANCED
advanced_extra_info = '.server-guide>div'
wol_mac_addr = '.mac-address'
delete_wol = '.last-child'
input_mac_addr = '.right .mac-address input'
port_forwarding_card = '.portforwarding-card'
port_triggering_card = '.triggering-card'
dmz_card = '.dmz-card'
diagnostic_card = '.diagnostic-card'

ip_address_col_cls = '.ip-address-col'
service_type_cls = '.service-type-col'
local_port_cls = '.local-port-col'
external_port_cls = '.external-port-col'
protocol_col_cls = '.protocol-col'
description_col_cls = '.description-col'
triggered_col_cls = '.triggered-col'
forwarded_col_cls = '.forwarded-col'
diagnostic_result = '.result-diagnostics textarea'
clear_btn = '.result-diagnostics button'
adv_wl_radio_row = '.form-container>.wrap-form'
ele_title_page = '.title-page'
ele_title_sub_page = '.sub-title-lines-page'
ele_channel_field = '#channel'
ele_wireless_mode_filed = '#wireless-mode'
ele_output_power_filed = '#output-power'
ele_bandwidth_field = '#bandwidth'
ele_sideband_field = '#sideband'
ele_beacon_cls = '.beacon'
ele_dtim_textbox_cls = '.text-box'
ele_button_restore = 'button.btn-restore'
ele_button_scan = 'button.btn-scan'
ele_scan_title = '.text-title'
ele_wifi_chart = '.wifi-chart'
ele_wifi_chart_5g = '.wifi-chart-5ghz'
ele_button_chart = '.btn-chart-mode'
ele_button_list = '.btn-list-mode'
ele_wifi_table = '.table-content'
ele_btn_close = 'button.md-primary'
ele_table_nw_ssid_name = '.col-network-name'
ele_table_channel = '.col-ch'
ele_table_rssi = '.col-rssi'
ele_table_security = '.col-security'
ele_adv_wireless_card = '.wireless-card'
ele_upnp_card = '.upnp-card'
ele_options_card = '.option-card'
# ~~~~~~~~~~~~~~~~ SYSTEM
system_btn = '[name="system-menu-system"]'
sys_language = '[name="system-menu-system"]+ul>li:nth-child(1)>button'
sys_reset = '[name="system-menu-system"]+ul>li:nth-child(6)>button'
sys_pop_factory_reset = '#factory-popup .bottom-button>button'
language_selected_text = '#language-popup .option-selected-text>span'
list_language_option = '#language-popup ul>li>button>span'
pop_up_btn_apply = '#language-popup button.active-button'
ele_sys_change_pw = '[title=System]+ul>li:nth-child(3)>button'
ele_sys_winzard = '[title=System]+ul>li:nth-child(9)>button'
ele_sys_date_time = '[title=System]+ul>li:nth-child(8)>button'
ele_sys_change_pw_current_pw = '#change-password-input-value-lable'
ele_winzard_step_id = '#wizard-step-id'
ele_system_2g = '._2-4G'
ele_system_5g = '._5G'
ele_sys_backup_restore = '[name="system-menu-system"]+ul>li:nth-child(5)>button'
ele_sys_firmware_update = '[name="system-menu-system"]+ul>li:nth-child(2)>button'
ele_system_connected_status = '[name="connected-status"]'
ele_popup_language = '.system-language-content'
ele_firm_update_msg = '.upgrable-msg'
ele_choose_firmware_file = '.inputfile'
ele_choose_firmware_select = '.select-item:nth-child(2) [for="selected-firmware"]'
ele_wireless_description = '.wireless-description-text'
# ~~~~~~~~~~~~~~.internet-dual-setting-card~~ DIALOG
btn_ok = 'button.confirm'
dialog_loading = '.dialog-body>.loading'
btn_cancel = 'button.cancel'
icon_loading = '.loading'
# ~~~~~~~~~~~~~~~~ HOME
logout_btn = 'a.system-menu-logout'
home_view_wrap = 'div.view-wrap.home'
home_img_connection = 'div.wan-connection>a.img-connection'
home_img_lan_connection = 'div.lan-connection>a.img-connection'
home_connection_description = 'div.wan-connection>.text-description'
home_img_usb_connection = 'div.usb-connection>a.img-connection'
home_img_device_connection = 'div.device-connection>a.img-connection'
home_img_device = 'div.device-connection'

home_wan_ls_fields = '.wrap-form'
home_wan_ls_label = 'label.input-label'
home_wan_ls_value = 'span.text-label'
home_icon_fab = '.icon-fab'
home_icon_more_fab = 'button.more-fab'
home_conection_img_wan_ip = '.wan-connection .more-info'
home_connection_mode = '.wan-connection .qmode'
left = '.left'
right = '.right'
wrap_input = '.wrap-input'
input = 'input'
apply = 'button.active-button'
select = '.toggle-button'
label = '.input-label'
input_pw = 'input[type=password]'
confirm_dialog_msg = '.confirm-dialog-message'
google_img = '.content#main>#body'
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
name_cls = '.name'
content = '.content'
rows = 'tbody>tr'
row_table = 'table>tr'
option_select = '.option-selected-text'
input_filed = '.input-field'
input_not_disabled = 'input:not([disabled="disabled"])'
submit_btn = '.submit>button'
mac_addr_text_cls = '.mac-address-text'
mac_desc_cls = '.mac-description'
ip_address_cls = '.ip-address'
id_cls = '.id'
password_cls = '.password'
edit_cls = '.edit'
delete_cls = '.delete'
err_dialog_msg_cls = '.error-dialog-message'
custom_error_cls = '.custom-error'
wireless_block = '.tabs-wireless'
ls_tab = '.parent-menu>a'
arrow_down_cls = '.down-arrow'
card_cls = '.card'
title_tabs_cls = '.title-tabs'
card_tabs_cls = '.md-ink-ripple'
internet_cls = '.internet'
title_cls = '.title'
wireless_cls = '.wireless'
password_input_cls = '.password-input>.form-group'
sub_title_popup_cls = '.sub-title-dialog'
menu_main_cls = '.main-menu'
popup_header_cls = '.custom-header'
confirm_dialog_cls = '.confirm-dialog'
btn_active_not_disabled = 'button.active-button:not([disabled])'
ele_active_connected_device = '.device-connectivity .active'
ele_active_cls = '.active'
ele_count_cls = '.count'
ele_edit_device_img = '.thumb>span'
ele_info_cls = '.info'
ele_advanced_button = '.advanced-btn'
ele_icon_cls = '.icon'
ele_table_row = 'table>tr.body'
ele_ssid_cls = '.ssid'
ele_second_tab = '.second-tab'
ele_device_tab_titles = '.tabs-device-connectivity'
ele_button_type = '[type=button]'
ele_device_row_connected = 'table>tr.connected'
ele_device_row_disconnected = 'table>tr.disconnected'
ele_btn_refresh = 'button.btn-refresh'
ele_device_network_title = '.network-item-title>.title'
ele_device_connect_col_title = 'td.theader>span'
ele_skip_btn = 'button.skip'
ele_back_btn = 'button.back'
ele_time_content = '.text-content-large'
ele_timezone_cls = '.time-zone'
ele_dst_cls = '.dst'
ele_ntp_cls = '.npt'
ele_npt_server_cls = '.table-device'
ele_index_cls = '.index'
ele_home_info_firm_version = '.information .wrap-form:nth-child(3) >.wrap-input'
ele_home_info_old_firm_version = '.tabs-information .wrap-form:nth-child(3) >.wrap-input'
ele_wrap_input_label = '.wrap-input .text-label'
ele_data_placeholder = '[data-placeholder]'
ele_more_info_cls = '.more-info'
ele_disconnect_device_tab = 'div.second-tab>button.md-button'
ele_disconnect_table = '.disconnected-table'
ele_disconnect_header = 'tr.header>td.theader'
ele_block_button_cls = 'tr.body>td.block'
ele_network_name = '.network-name'
ele_input_pw = '.password-input input'
ele_apply_highlight = '.active-button.hight-light'
ele_host_network = '.host-network'
ele_connected_table = '.connected-table'
ele_icon_dot = '.slave-img'
ele_version = '.version'
ele_upgrade_btn = '.upg_btn'
ele_lan_card = '.tabs-lan'
ele_wireless_card = '.tabs-wireless'
ele_information_card = '.information'
ele_ethernet_port_status = '.ethernet-status'
ele_cpu_card = '.cpu-card'
ele_memory_card = '.memory-card'
ele_operation_mode_card = '.operation-modes>.card'
ele_mesh_mode_icon = '.meshmode-img'
ele_description_text = '.description-text'
ele_manual_scan_btn = '.manual-action button'
ele_guideline = '.guideline'
ele_btn_next = 'button.next'
ele_toggle_input = '.toggle-button input'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USB
ele_usb_card = '.simple-usb'
ele_space_use = '.space-used'
ele_space_available = '.space-available'
ele_space_bar = '.space-bar'
ele_server_card = '.simple-server'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ OTHERS
ele_home_tab = 'a[href="/home"]'
ele_humax_about = '[title="Link to About HUMAX Wi-Fi"]'
ele_humax_help_guide = '[title="Go to Support page"][name=help]'
ele_humax_support = '[title="Go to Support page"]:not([name=help])'
ele_humax_contact_us = '[title="Go to Contact Us page"]'
ele_humax_search_box = '.footer-input-inner>input'
ele_humax_search_value_menu_2 = '.footer-list-group ul>li>a'
ele_humax_search_value_menu_1 = '.footer-list-group>li>a'
ele_humax_show = '.index-toggle-icon:not(.show)'
ele_check_for_update_title = '.custom-dialog-header>h2'
ele_close_button = '.dialog-close-button'
ele_device_more_info = '.device-connection .more-info'
ele_upgrade_server_popup = '.upgrade-save'
ele_button_scan_ap = 'button.scan'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ YOUTUBE
ele_playing = '.playing-mode'
ele_buffering = '.buffering-mode'
ele_skip_ad = '.ytp-ad-skip-button-text'
ele_video = '.video-stream'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FACEBOOK
ele_verify_facebook = '#facebook .fb_logo'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BRIDGE MODE
ele_home_tree_menu_enable = '#parent-menu:not(.disabled)>a'
ele_home_tree_menu_disable = '#parent-menu.disabled>a'
ele_home_sub_menu = '#sub-menu>a'
ele_sys_list_button = '#system-menu-dropdown-wrap>li>button'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DOWN FIRMWARE
el_lg_user_down_firm = '.id-form input'
el_lg_pw_down_firm = '.pwd-form input'
el_lg_button_down_firm = 'button[type=submit]'
el_home_wrap_down_firm = '[ng-controller=MainController]'
el_home_info_firm_version_down_firm = '.gateway-information .wrap-form:nth-child(3) >.wrap-input'
el_firmware_manual_box_value = '.dialog-content .box span'
ele_privacy_agree = '[ng-click="saveAgreements()"]'