# arp-spoofer

A python script that performs an ARP spoof attack.<br>
 In an ARP spoofing attack, the attacker sends forged ARP messages to other devices on the network, essentially tricking them into thinking that the attacker’s device has the same IP address as another device on the network.

<p align="center">
  <img src="https://raw.githubusercontent.com/Ahmed-Z/the-blog/gh-pages/assets/arp-spoofing.PNG" style="width:600px;"><br>
</p>

# Installation
`git clone https://github.com/Ahmed-Z/arp-spoofer`<br>
`cd arp-spoofer` <br><br>
After downloading you have to install dependencies:<br>
`pip install -r requirements.txt`

# How to use
`python arp-spoof.py -t <target_ip_address> -g <gateway_ip_address>`
