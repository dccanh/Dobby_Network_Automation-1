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
lg_welcome_header = 'span.header-text'
lg_privacy_policy_pop = '#privacy-dialog-id'
lg_company_img = '.login-page>.company>a'
# ~~~~~~~~~~~~~~~~~ REDIRECT
network_tab = 'a[href="/network"]'
network_internet_tab = 'a[href="/network/internet"]'
network_lan_tab = 'a[href="/network/lan"]'
network_operationmode_tab = 'a[href="/network/operationmode"]'

wireless_tab = 'a[href="/wireless"]'
wireless_primarynetwork_tab = 'a[href="/wireless/primarynetwork"]'
wireless_guestnetwork_tab = 'a[href="/wireless/guestnetwork"]'
wireless_wps_tab = 'a[href="/wireless/wps"]'


# ~~~~~~~~~~~~~~~~~ NETWORK
ip_address_input_filed = 'div.ip-address [name="input-field"]'
start_end_ip_address = '.ip-class-c .input-field input'


# ~~~~~~~~~~~~~~~~~ WIRELESS
fields_in_2g = '.left .wrap-form'
label_name_in_2g = '.wrap-label>.input-label'
label_value_in_2g = '.wrap-input input'
secure_value_field = '[name=security]'
secure_value_in_drop_down = 'ul>li'


# ~~~~~~~~~~~~~~~~ SYSTEM
system_btn = '[title=System]'
sys_language = '[title=System]+ul>li:nth-child(1)>button'
sys_reset = '[title=System]+ul>li:nth-child(6)>button'
sys_pop_factory_reset = '#factory-popup .bottom-button>button'
language_selected_text = '#language-popup .option-selected-text>span'
list_language_option = '#language-popup ul>li>button>span'
pop_up_btn_apply = '#language-popup button.active-button'


# ~~~~~~~~~~~~~~~~ DIALOG
btn_ok = 'button.confirm'
dialog_loading = '.dialog-body>.loading'