#!/usr/bin/env python

import subprocess
import optparse
import re

def change_mac (interface,new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", dest="interface", help="interface")
    parser.add_option("--mac", dest="new_mac", help="mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac address")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return(mac_address_search_result.group(0))
    else:
        print("Couldn't find the mac address.")

def check_mac(current_macc):
    if current_mac == options.new_mac:
        print(f"The MAC address has been changed to {current_macc}")
    else:
        print(f"The mac address has not been changed")

options = get_arguments()
old_mac = get_current_mac(options.interface)
print(f"Old MAC address: {old_mac}")
change_mac(options.interface,options.new_mac)
current_mac = get_current_mac(options.interface)
check_mac(current_mac)



