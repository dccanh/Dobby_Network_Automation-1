# _version_: 1.1
# Language: python 3.7
# Author: Ciel Dinh <dccanh@humaxdigital.com>
"""
This module is automation generate a simple test case of Page Wifi Radio by command line.

Test URL: http://192.168.0.1/#page-wifi-radio
With 6 params as:
    - op: Output Power >> Potência de saída
    - wm: Wireless Mode >> Modo 802.11.n
    - bw: Band Width >> Largura de banda
    - sb: Side Band >> Banda lateral para canal de controle (somente 40Mhz)
    - cn: Channel >> Canal de controle
    - bf: Beamforming >> Beamforming

*** How to use ***
1. Open command line in folder contain this file and chromedriver.exe
2. Just type: python customize_tc.py prefix_chars value
3. Example: python customize_tc.py -op Alto -wm Auto -bf Disabled. Values of prefix_chars is values in WebUI
4. If you need help: python customize_tc.py -h

"""


import argparse, time, os, sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# Arguments
parser = argparse.ArgumentParser(description='str(sys.argv[0]')
parser.add_argument('-op', '--outputPower', default='ALTO', help='outputPower Value. Ex: high, medium, low', required=False)
parser.add_argument('-wm', '--wirelessMode', default="AUTO",  help='wirelessMode Value. Ex: auto, off', required=False)
parser.add_argument('-bw', '--bandwidth', default="40MHZ", help='Bandwidth Value. Ex: 40, 20', required=False)
parser.add_argument('-sb', '--sideband', default="BAIXO", help='sideband Value. Ex: lower, upper', required=False)
parser.add_argument('-cn', '--channel', default="AUTO", help='Channel Value. Ex: auto, 1->9(40MHz), 1->13(20MHz)', required=False)
parser.add_argument('-bf', '--beamforming', default="DISABLED", help='beamforming Value. Ex: false, true', required=False)

args = parser.parse_args()
# 1 Handle data of Output Power
op_dict = {
    "ALTO": "high",
    "MEDIO": "medium",
    "BAIXO": "low"
}
outputPower = ['outputPower', op_dict[str(args.outputPower).upper()]]

# 2 Handle data of Wireless Mode
wm_dict = {
    "AUTO": "auto",
    "OFF": "off"
}
wirelessMode = ['wirelessMode', wm_dict[str(args.wirelessMode).upper()]]

# 3 Handle data of BandWidth
bw_dict = {
    "20MHZ": "20",
    "40MHZ": "40"
}
bandwidth = ['bandwidth', bw_dict[str(args.bandwidth).upper()]]

# 4 Handle data of Side band
sb_dict = {
    "BAIXO": "lower",
    "ALTO": "upper"
}

sideband = ['sideband', sb_dict[str(args.sideband).upper()]]

# 5 Handle data of Channel
cn_dict = {
    "AUTO": 'auto'
}
for i in range(1, 14):
    cn_dict.update({str(i): str(i)})

channel = ['channel', cn_dict[str(args.channel).upper()]]

# 6 Handle data of Beamforming
bf_dict = {
    "DISABLED": "false",
    "ENABLED": "true"
}
beamforming = ['beamforming', bf_dict[str(args.beamforming).upper()]]

user = 'NET_4F9761'
pass_word = '942CB34F9761'
url_root = 'http://192.168.0.1/#'
url_target = 'http://192.168.0.1/#page-wifi-radio'


# Functions
def login(driver, url_root):
    time.sleep(1)
    driver.get(url_root)
    time.sleep(2)
    driver.find_element_by_id('login').send_keys(user)
    driver.find_element_by_id('senha').send_keys(pass_word)
    driver.find_element_by_xpath('//button[@value="Entrar"]').click()
    time.sleep(1)


def goto_url_target(driver, url_):
    driver.get(url_)
    time.sleep(3)


def setUp():
    driver = webdriver.Chrome('../Driver/chromedriver.exe')
    login(driver, url_root)
    time.sleep(2)
    goto_url_target(driver, url_target)
    time.sleep(5)
    return driver


def apply(driver):
    driver.find_element_by_css_selector('button[value="Aplicar Ajustes"').click()
    # Apply  the change and Wait until pop up wait disappear. If the pop-up were not, Quit (time = 300s).
    pop_up_wait = driver.find_elements_by_css_selector('.msgText')
    count_time = 0
    while len(pop_up_wait) == 1:
        pop_up_wait = driver.find_elements_by_css_selector('.msgText')
        time.sleep(1)
        count_time += 1
        if count_time >= 300:
            break


def check_logic():
    reason = "Condition was satisfied"
    # Handle Logic of Page Wifi
    op = op_dict[str(args.outputPower).upper()]
    wm = wm_dict[str(args.wirelessMode).upper()]
    bw = bw_dict[str(args.bandwidth).upper()]
    sb = sb_dict[str(args.sideband).upper()]
    cn = cn_dict[str(args.channel).upper()]
    bf = bf_dict[str(args.beamforming).upper()]
    # Case 1
    if wm == 'off':
        if bw == '40':
            reason = "Bandwidth Invalid"
        elif bw == '20':
            if cn not in [str(i) for i in range(1, 14)]+['auto']:
                reason = "Channel Invalid 1"
        else:
            reason = "Bandwidth Invalid"
    elif wm == 'auto':
        if bw == '40':
            if sb == 'lower':
                if cn not in [str(i) for i in range(1, 10)]+['auto']:
                    reason = "Channel Invalid 2"
            elif sb == 'upper':
                if cn not in [str(i) for i in range(5, 14)]+['auto']:
                    reason = "Channel Invalid 3"
            else:
                reason = "SideBand Invalid"
        elif bw == '20':
            if cn not in [str(i) for i in range(1, 14)]+['auto']:
                reason = "Channel Invalid 4"
        else:
            reason = "Bandwidth Invalid"
    else:
        reason = "Wireless Mode Invalid"

    # Case 2
    if op not in ['high', 'medium', 'low']:
        reason = "Output Power Invalid"

    # Case 3
    if bf not in ['true', 'false']:
        reason = "Beamforming Invalid"

    return reason


class Customize:
    """ This is Class of customize a test case. Click to element and chose a value."""

    def __init__(self, id_element, value):
        self.id_element = id_element
        self.value = value

    def step(self, driver):
        # Check condition of Params
        if "Invalid" not in check_logic():
            os.system('echo ' + check_logic())
            element = driver.find_element_by_css_selector('#' + str(self.id_element))
            ActionChains(driver).move_to_element(element).perform()
            driver.find_element_by_css_selector(
                '#' + str(self.id_element) + '>option[value="' + str(self.value) + '"]').click()
        else:
            os.system('echo ' + check_logic())


sys_argv = sys.argv
argvs = [i for i in sys_argv if '-' in i]
dict_argv = {
    '-op': outputPower,
    '-wm': wirelessMode,
    '-bw': bandwidth,
    '-sb': sideband,
    '-cn': channel,
    '-bf': beamforming
}
driver = setUp()
assert_fields = []
for argv in argvs:
    Customize(dict_argv[argv][0], dict_argv[argv][1]).step(driver)
    assert_fields.append(dict_argv[argv][0])
apply(driver)
time.sleep(1)
driver.refresh()
time.sleep(1)
actual = []
expected = []
for argv in argvs:
    actual.append(driver.find_element_by_css_selector('#'+dict_argv[argv][0]).get_attribute('value'))
    expected.append(dict_argv[argv][1])
try:
    assert expected == actual
    message = "[Pass] Values of %s. Expected: %s. Actual: %s." %(str(assert_fields), str(expected), str(actual))
except AssertionError:
    message = "[Fail] Values of %s. Expected: %s. Actual: %s." %(str(assert_fields), str(expected), str(actual))

os.system('echo ' + message)
driver.quit()


