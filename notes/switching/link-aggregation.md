<a id="topofpage"></a>
# LAG (Link Aggregation)

# Table of Contents
- [General Overview](#general-overview)
- [LAG Components](#lag-components)
- [LAG Design](#lag-design)
- [LAG Protocols](#lag-protocols)
- [Port-channel Interfaces](#port-channel-interfaces)
- [Order of Operations](#order-of-operations)
- [Guidelines](#guidelines)
- [Forwarding Methods](#forward-methods)
- [MultiChassis EtherChannel](#multichassis-etherchannel)
- [All Configuration Commands](#all-configuration-commands)
- [All Verification Commands](#all-verification-commands)
- [Useful Links](#useful-links)

---
###### [↑ Go to Top of Page ↑](#topofpage)

# General Overview

Category | Information
--- | ---
Purpose | Redundancy; Increase bandwidth/redundancy minimizing bottlenecks
Protocols | LACP (Cisco proprietary) / PAgP (IEE 802.3ad)
Pro | Cheaper to aggregate than upgrade switch; link redundancy
Con | Flows get polarized to one member of the port-channel
Limitation | Port-channel bandwidth cannot exceed the bandwidth of the individual liinks

---
###### [↑ Go to Top of Page ↑](#topofpage)

# LAG Components

Component | Description
--- | ---
Port-channel interface | The logical interface representing the underlying physical interfaces being aggregated.
Member interfaces | The physical interfaces that are aggregated to form a logical port-channel interface.
Protocol | PAgP or LACP; Used to hide member interfaces, behind a logical Port Channel, from Spanning-Tree and the CAM table

---
###### [↑ Go to Top of Page ↑](#topofpage)

# LAG Design

Design | Explanation
--- | ---
Standalone switch | ---
Single switch in a stack | ---
Multiple switches in a stack | ---

---
###### [↑ Go to Top of Page ↑](#topofpage)

# LAG Protocols

**Benefits of Using a LAG Protocol**
- Hides the physical member interfaces, behind a logcal port-channel, from Spanning-Tree and the CAM table
  - Spanning-Tree will not block redundant links
  - CAM table will not have duplicate entries
  
Protocol | Standard
--- | ---
PAgP | IEEE 802.3ad
LACP | Cisco proprietary
Static | No protocol used

Protocol | Mode | Description
--- | --- | ---
LACP | `active` | Initiates negotiation by sending LACP packets.
LACP | `passive` | Responds if LACP packet is received, but does not initate the negotiation.
PAgP | `desirable` | Initiates and negotiation by sending PAgP packets.
PAgP | `auto` | Responds if PAgP packet is received, but does not initate the negotiation.
EtherChannel | `on` | Forces LAG without using a protocol

LACP Mode | Active | Passive | On
--- | --- | --- | ---
Active | Yes | Yes | No
Passive | Yes | No | No
On | No | No | Yes

PAgP Mode | Desirable | Auto | On
--- | --- | --- | ---
Desirable | Yes | Yes | No
Auto | Yes | No | No
On | No | No | Yes

**PAgP Non-Silent Mode**
- Command `non-silent`
- Switch is in silent mode by default
- Use silent mode when connecting to a device that is not PAgP capable and rarely sends packets (e.g. file server, packet analyzer that doesn't generate traffic)

**On Mode**
- Useful when remote device does not support LACP or PAgP
- May create a switching loop, the physical interfaces are not hidden from Spanning-Tree

---
###### [↑ Go to Top of Page ↑](#topofpage)

# Port-channel Interfaces

Interface | Explanation
--- | ---
Layer 2 port-channel | Aggregation of Layer 2 switching interfaces. Cannot be converted to a Layer 3 port-channel.
Layer 3 port-channel | Aggregation of Layer 3 routing interfaces. Cannot be created by converting a prexisting Layer 2 port-channel. 

---
###### [↑ Go to Top of Page ↑](#topofpage)

# Order of Operations

**Creating a new Layer 2 port-channel with LACP or PAgP**
1. Create the new port-channel `interface port-channel [po_id]
2. Add physical interfaces to the port-channel `channel-group [po_id]`

**Creating a new Layer 3 port-channel**
1. Create the new Port-Channel `interface port-channel [po_id]
2. Convert the newly created port-channel into a layer 3 routing interface `no switchport`
3. Add *Layer 3 routing interfaces* to the port-channel `channel-group [po_id]`

**Creating new static port-channel**
1. Shutdown member interfaces first
2. Add physical interfaces to the port-channel

**Configuring changes to member interfaces**
- Apply config changes to the port-channel, and it will be automatically applied to its member interfaces

---
###### [↑ Go to Top of Page ↑](#topofpage)

# Guidelines

- Configure a PAgP EtherChannel with up to eight Ethernet ports of the same type.
- Configure a LACP EtherChannel with up to16 Ethernet ports of the same type. Up to eight ports can be active, and up to eight ports can be in standby mode.
- Configure all ports in an EtherChannel to operate at the same speeds and duplex modes.
- When a group is first created, all ports follow the parameters set for the first port to be added to the group.
- Do not configure a private-VLAN port as part of an EtherChannel.
- Ports must have the same native VLAN. Ports with different native VLANs cannot form an EtherChannel.
- For Layer 3 EtherChannels, assign the Layer 3 address to the port-channel logical interface, not to the physical ports in the channel.

---
###### [↑ Go to Top of Page ↑](#topofpage)

# Forwarding Methods

Method | Explanation 
---  | ---
**Source MAC** | Those from different hosts use different ports; those from same host use same port.
**Destination MAC** |Those to different destinations use different ports, those to same destination use same port.
**Source & destination MAC** | Can be used if it is not clear whether source-MAC or destination-MAC address forwarding is better suited on a particular switch
**Source IP** | Those from different hosts use different ports; those from same host use same port.
**Destination IP** | Those to different destinations use different ports, those to same destination use same port.
**Source & destination IP** | Can be used if it is not clear whether source-IP or destination-IP address-based forwarding is better suited on a particular switch.

- **Note:** Use command `port-channel load-balance`.

---
###### [↑ Go to Top of Page ↑](#topofpage)

# MultiChassis EtherChannel

**Server to Single Chassis port channel**
- Multiple ports on a single chasses are aggregated
- SPOF (Single Point of Failure) - if chassis goes down, the port channel does with it

**Server to Multiple Access Layer Switches**
- 50% bandwidth lost - Most server NICs support only active/standby outside of aggregation on single chassis

**MCEC**
- Two physical chassis appear as one logical chassis to the server
- To the server it appears as a port channel to a single switch
- 100% bandwidth is used, and more redundancy
- MCEC/MLAG synchronizes control plane between switches
  - Sync is proprietary, both chassis need to be of the same vendor/model/version/OS
  
**StackWise Cross-Stack EtherChannel**
- Access platforms - e.g. Catalyst 3750/3850
- Control plane sync over dedicated stacking cables
- One control plane is shared among stack members
- One managment plane is shared among stack members
- Must be using switches of the same vendor/model/parts

**VSS (Virtual Switching Systems)**
- Aggregated platforms (core switches) e.g. Catalyst 4500/6500/6800
- Control plane syncs over VSL (Virtual Switch Link)
- One control plane is shared among VSS
- One management plane is shared among VSS
- Usually 1 active supervisor and 3 standby supervisors

**vPC (Virtual Port Channel)**
- Data Center platforms e.g. Nexus 5K/7K/9K
- Control plane sync over a vPC Peer Link
- Two independent control planes in the vPC
- Two independent management planes in the vPC
- Usually 2 active supervisors and 2 standby supervisors

**StackWise vs VSS vs vPC**
- Stackwise can havemore than 2 members, up to the stack limit
- VSS and vPC are always a pair of switches
- Logical result of all three is the same

---
###### [↑ Go to Top of Page ↑](#topofpage)

# All Configuration Commands

```

Switch# configure terminal
Switch(config)# interface port-channel 5
Switch(config-if)# no switchport
Switch(config-if)# ip address 172.10.20.10 255.255.255.0
Switch(config-if)# end


Switch# configure terminal
Switch(config)# interface range gigabitethernet2/0/1 -2
Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport access vlan 10
Switch(config-if-range)# channel-protocol lacp 
Switch(config-if-range)# channel-group 5 mode active
Switch(config-if-range)# end


interface portchannel [portchannel_id]  
  switchport trunk encapsulation dot1q
  channel-protocol lacp 
  switchoprt mode trunk
  exit
interface range FastEthernet0/23-24
  no shutdown 
``` 
---
###### [↑ Go to Top of Page ↑](#topofpage)

# All Verification Commands

Command | Output
--- | ---
`show etherchannel summary` | Group ID, Negotiation Protocol, Member ports, Layer2/3, In use
`show spanning tree` | Port channel should appear, and not the individual member interfaces
`show lacp neighbor` | LACP details
`show pagp neighbor` | PAgP details


###### [↑ Go to Top of Page ↑](#topofpage)

# Useful Links

[Cisco Documentation - Catalyst 3750-X and 3560-X Switch Software Configuration Guide, Release 12.2(55)SE
](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3750x_3560x/software/release/12-2_55_se/configuration/guide/3750xscg/swethchl.html)
[PacketLife - EtherChannel considerations
](https://packetlife.net/blog/2010/jan/18/etherchannel-considerations/)

---
###### [↑ Go to Top of Page ↑](#topofpage)

