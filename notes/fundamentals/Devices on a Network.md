# Clients and Servers

**Client**
- Devices on a network (PC, laptop, phone) accessing a resource provided by a server
- E.g. computer obtains IP address from DHCP server

**Server**
- Device on a network providing a resource accessible by clients
- E.g. DHCP server provides IP addresses for connected computers
- Server Types: DHCP, DNS, NTP, FTP, HTTP
- OS: Linux (Red Hat, Suse, Ubuntu) or Windows (2008/2012)
- Hardware Type: Tower, Rack, Blade
- HD &rarr; VMWARE ESX 5/5.5/6 &rarr; Hyper-V &rarr; VM &rarr; OS &rarr; Role

---

# End Devices

**What is an end device**
- Devices that utilize the network
- PC
- Laptops
- Printer
- Tablet
- Smartphone
- Printer
- Fax
- IP Phone
- Medical devices

---

# Network Devices

**Hub**
- OSI Model | Layer 1 – Physical
- Forwards received frames out of every port, does not inspect the frames
- Half-Duplex
- All devices in one collision domain and one broadcast domain

**Repeater (Wireless Range Extender)**
- OSI Model | Layer 1 – Physical
- Regenerates signals to increase distance; helps against attenuation

**Ethernet Switch**
- OSI Model | Layer 2 – Data Link
- Connects devices in a LAN, forwards frames based on MAC addresses
- Each port is a separate collision domain – full-duplex
  - Unless port is configured to operate in half-duplex
- All ports, by default, are in one broadcast domain
  - Unless VLANs are used to separate the broadcast domains

**Router**
- OSI Model | Layer 3 – Network
- Connects LAN networks and/or subnets within a LAN
- Forwards frames based on source/destination IP addresses
- Separates broadcast domains
  - Unless configured to allow specific broadcast packets

**Firewalls**
- OSI Model | Layer 3, 4, 7 – Network, Transport, Application
- Mitigate threats by monitoring all traffic entering or leaving a network.
- Layer 3 | Network – Filter based on IP Address
- Layer 4 | Transport – Filter based on Ports
- Layer 7 | Application – Inspects protocol states or data
- Stateful Inspection
  - Remembers source of outbound traffic, then accepts related traffic going in

**Autonomous Access Points**
- Each AP device is managed individually


**LWAP (Lightweight WAP)**
- Wireless AP that are managed by a wireless LAN controller
- The point where the wireless network connects with the wired network

**Wireless Controllers**
- Used to manage multiple LWAP
- Used to use the LWAPP protocol
  - Now replaced by CAPWAP
