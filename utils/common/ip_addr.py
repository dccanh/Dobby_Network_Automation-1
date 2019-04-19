import argparse
import os
import subprocess

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def set_static_IP(interface, GW_IP):
    gw = GW_IP.split(".")
    gw_str = gw[0] + "." + gw[1] + "." + gw[2] + "."

    PC_IP = gw_str + "102"
    NET_MASK = "255.255.255.0"
    cmd = "netsh interface ipv4 set address name="\
            + interface + " static " + PC_IP + " mask="\
            + NET_MASK + " gateway=" + GW_IP
    os.system(cmd)
    print("Set the static IP: " + PC_IP)

    return str(PC_IP)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_INF_config(interface):
    inf_config = {}
    dhcp_str = "DHCP enabled:"
    ip_str = "IP Address:"
    mask_str = "(mask"
    gw_str = "Default Gateway:"

    cmd = "netsh interface ipv4 show config " + interface
    inf_data = str(subprocess.check_output(cmd))
    inf_data = inf_data.split("\\r\\n")

    for line in range(1, len(inf_data)):
        if dhcp_str in inf_data[line]:
            tmp = inf_data[line]
            id = tmp.find(dhcp_str)
            tmp = tmp[id + len(dhcp_str):]
            tmp = tmp.strip()
            inf_config.update({"dhcp":str(tmp)})

        if ip_str in inf_data[line]:
            tmp = inf_data[line]
            id = tmp.find(ip_str)
            tmp = tmp[id + len(ip_str):]
            tmp = tmp.strip()
            inf_config.update({"ip":str(tmp)})

        if mask_str in inf_data[line]:
            tmp = inf_data[line]
            id = tmp.find(mask_str)
            tmp = tmp[id + len(mask_str):]
            tmp = tmp.strip(')')
            inf_config.update({"mask":str(tmp)})

        if gw_str in inf_data[line]:
            tmp = inf_data[line]
            id = tmp.find(gw_str)
            tmp = tmp[id + len(gw_str):]
            tmp = tmp.strip()
            inf_config.update({"gateway":str(tmp)})

    return inf_config

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_RG_interface(GW_IP):
    interfaces = []
    cmd = "netsh interface ipv4 show config"
    ipconfig_data = str(subprocess.check_output(cmd))
    ipconfig_data = ipconfig_data.split("\\r\\n")

    for line in range(1, len(ipconfig_data)):
        inf_str = "Configuration for interface"
        if inf_str in ipconfig_data[line]:
            inf_data = ipconfig_data[line]
            id = inf_data.find("\"")
            interfaces.append(inf_data[id:])

    for i in range(1, len(interfaces)):
        gw = GW_IP.split(".")
        gw_str = gw[0] + "." + gw[1] + "." + gw[2] + "."
        cmd = "netsh interface ipv4 show config " + interfaces[i]
        inf_data = str(subprocess.check_output(cmd))
        inf_data = inf_data.split("\\r\\n")

        for line in range(1, len(inf_data)):
            if gw_str in inf_data[line]:
                rg_inf = str(interfaces[i])

                return rg_inf

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def set_DHCP_IP(interface):
    cmd_ip = "netsh interface ipv4 set address name=" + interface + " dhcp"
    cmd_dns = "netsh interface ipv4 set dns name=" + interface + " dhcp"
    os.system(cmd_ip)
    os.system(cmd_dns)
    if (str(get_INF_config(interface)["dhcp"]) == "Yes"):
        print("Configure the DHCP IP successfully.")

        return True
    else:
        print("Could not configure the DHCP IP !!!")

        return False
