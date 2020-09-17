# Network Components and Terminology

# Wired 
NIC (Network Interface Card)
- The port on a PC to where the Ethernet cable connects to 
- Has a MAC addressed embedded to it

Ethernet Cable
- Has an RJ-45 connector
- Connects the PC to the switch (or patch panel)

Ethernet Jack
- The port on the wall where the PC connects to
- This cable then connects to a patch panel 
- Usually labeled to identify the patch panel

Patch Panel
- All Ethernet cables in the office connect to the patch panel
- The patch panel then connects to the switch
- The patch panel does not provide any function
- Its purpose is so that the cables to the switch are short and easy to move
- It will be labeled according to the ethernet jack

Switch
- Creates a LAN
- Forwards frames by MAC address

Router
- Connects LANs
- Forwards packets by IP address

Traditional Firewall
- permits or denies traffic by source/destination IP address or port number
- 
Next-Generation Firewall
- Includes the features of a traditional firewall
- Deep-packet inspection
- IPS capabilities

IPS (Intrusion Prevention System)
- Placed behind a firewall
- Detects malicious packets

----
# Wireless
Wireless NIC
- Contains an antenna to connect to the WiFi

Access Points
- Provides wireless connectivity
- Connects back to the switch
- Autonomous AP
	- Just a regular independent AP that provoides wireless connectivity
- LWAP (Lightweight Access Point)
	- Managed by a Wireless Controller
	- All configurations are made on the controller and pushed to the LWAP 

Wireless Controller
- Controls multiple access piont
- A central point to manage group of LWAPs
- Appliance or cloud-based

- 
Cisco DNA Center
- Centralized management dashbaord for completete control of a network
- Central automation  
- Central opnt of GUI-based nework control
	- Design your network
	- Create topology maps and diagrams
	- Identify/list "golden images" for software deployment
