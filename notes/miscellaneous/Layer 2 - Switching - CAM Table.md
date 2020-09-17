<a id="topofpage"></a>

# CAM Table

- [Overview](#overview)
- [CAM Table](#cam-table)
- [Static and Dynamic Entries](#static-and-dynamic-entries)
- [MAC Learning](#mac-learning)
- [Frame Forwarding](#frame-forwarding)
- [Configuration Commands](#configuration-commands)
- [Verification Commands](#verification-commands)
- [Glossary](#glossary)
- [Useful Links](#useful-links)

---

# Overview

- Switches forward frames
- Frames are forwarded by destination MAC address
- CAM table contains entries of learned MAC addresses

You will need the CAM table for:
- Finding which switch and/or interface a device is connected to
- Finding out where a frame is being forwarded out 

---

# CAM Table

**CAM Table**
- aka "MAC Address Table" or "MAC Forwarding Table"
- Contains information:
	- Learned MAC addresses
	- Interface the MAC was learned on
	- VLAN that the device belongs to
- Switch looks up MAC address in CAM to know which interface to forward the frame out of
- Show table with `show mac address-table` 
- Clear table with `clear mac-address-table`

**Aging**
- Each dynamic entry remains for a specific time called "aging time"
- The aging time is renewed when a new frame with that source MAC is received
- After the aging time expires, the entry is removed
- Prevents CAM table from overflowing with too many entries
- The default aging time varies per platform
  - IOS: 800 seconds
  - NX-OS: 300 seconds

 **Configuring Aging Time**
 - Age value may be rounded off to the nearest multiple of 5 seconds
 - Aging value set to 0 will disable MAC address aging
 - Configuring aging for a specific VLAN will only affect entries belonging to that VLAN
 - Configured with `mac address-table aging-time [seconds] [vlan-id]`
 - Removing the configured aging time
	 - Use the `no mac address-table aging time [vlan-id]` command
	 - Only removes entries for that VLAN
	 - Will not affect entries for other VLANs
	 - Aging time returns to default value


###### [↑ Go to Top of Page ↑](#topofpage)

---

# Static and Dynamic Entries

**Dynamic Entries**
- Switch learns and adds MAC addresses automatically to the CAM table
- Saved in RAM - lost after reboot

**Static Entries**
- MAC address is manually configured
- Saved in NVRAM - restored to CAM table after reboot
- You will rarely have to configure a MAC address statically
- There are some static entries that are there by default


###### [↑ Go to Top of Page ↑](#topofpage)

---

# MAC Learning

**Learning New MAC Addresses**
- Switch looks at source MAC address of incoming frames
- If no entry already exists in CAM, new entry is created
- If entry already exists, it will be updated
	- Timestamp wil be updated as well
- The entry will include the following:
	- MAC address
	- Interface it was learned on
	- VLAN ID
	- Time it was learned
- If device is relocated, the switch wil remove old entry and add new entry	

**Forwarding Frames**
- Looks up destination MAC address in CAM table
- If entry is found, it forwards frame out designated interface
- If entry is not found, the frame is **flooded** out all ports except where it came from
	- "Flooding" is just sending copies of the frame out each port

**Step By Step Process**
*PC-A is sending a frame to PC-B*
- Switch receives frame on an interface, from PC-A
- Source MAC address is added to CAM table
	- If entry already exists, it is only updated
- Switch looks up destination MAC in CAM table
	- If found - frame forward out designated interface
	- If not found - frame is **flooded**
		- Forwards the frame out all interface except where it came from
    - When PC-B replies to PC-A the switch will learn the MAC address
    - Since PC-A MAC is already in CAM table, frame is forwarded directly to PC-A


###### [↑ Go to Top of Page ↑](#topofpage)

---

# Frame Forwarding

**Step By Step Process**
*PC-A is sending a frame to PC-B*
- Switch receives frame on an interface, from PC-A
- Source MAC address is added to CAM table
	- If entry already exists, it is only updated
- Switch looks up destination MAC in CAM table
	- If found - frame forward out designated interface
	- If not found - frame is **flooded**
		- Forwards the frame out all interface except where it came from
    - When PC-B replies to PC-A the switch will learn the MAC address
    - Since PC-A MAC is already in CAM table, frame is forwarded directly to PC-A

---

# Configuration Commands

## List of All Commands
```
! - Configure static MAC address
S1(config)#mac address-table static [mac-address] vlan [vlan-id] interface [#/#]

! - Auto update the entry if device is switched to a different port
S1(config)#mac address-table static [mac-address] vlan [vlan-id] interface [#/#] auto-learn

! - Configure aging time for all MAC addresses in particular VLAN
! - Value of 0 disables MAC address aging
! - If VLAN ID is not specified, it is applied to all MAC addresses (I think)
S1(config)#mac address-table aging-time [seconds] [vlan-id]

! - Clear all dynamic entries 
clear mac-address-table dynamic

! - Clear a single entry
clear mac-address-table dynamic [mac-address] interface [#/#] vlan [vlan-id]

! - Remove configured aging time 
no mac address-table aging time [vlan-id]
```

## What Each Command Does

Command | Explanation 
--- | ---
`mac address-table static [mac-address] vlan [vlan-id] interface [#/#]` | Configure static MAC address
`#mac address-table static [mac-address] vlan [vlan-id] interface [#/#] auto-learn` | Auto update the entry if device is switched to a different port
`mac address-table aging-time [seconds] [vlan-id]` | Configure aging time for all MAC addresses in particular VLAN. Value of 0 disables MAC address aging. If VLAN ID is not specified, it is applied to all MAC addresses (I think).
`clear mac-address-table dynamic` | Clear all dynamic entries 
`clear mac-address-table dynamic [mac-address] interface [#/#] vlan [vlan-id]` | Clear a single entry
`no mac address-table aging time [vlan-id]` | Remove configured aging time 


###### [↑ Go to Top of Page ↑](#topofpage)

---

# Verification Commands

## List of All Verification Commands
```
! - Show commands:
show mac-address-table
show mac address-table dynamic
show mac address-table interface [interface-id]
show mac address | include [mac-address]
show mac-address-table aging-time
```

## What Each Command Does

Verification Command | Output
--- | ---
`show mac address-table` | Shows entire CAM table
`show mac address-table dynamic` | Shows only dynamic entries in CAM table
`show mac address-table interface [interface-id]` | Show learned MAC addresses on specific interface
`show mac address | include [mac-address]` | Show if there is an entry for the specified MAC address
`show mac-address-table aging-time` | Displays the MAC address aging time for all VLANS defined in the switch.


###### [↑ Go to Top of Page ↑](#topofpage)

---

# Glossary

**CAM Table** :
A table containing mac ADD

**MAC Aging**:
The amount of time an entry will remain in the CAM table before its removed (unless renewed)

**MAC Learning** :
The ability to automatically learn source MAC addresses from incoming frames, and enter them into the CAM table as dynamic entries.

**Flooding**:
When a switch receives a frame with an unknown destination MAC address, it will forward it out all interfaces except for the interface that it was received on


###### [↑ Go to Top of Page ↑](#topofpage)

---

# Useful Links

-  [ComputerNetworkingNotes: How Switch learns the MAC addresses Explained](https://www.computernetworkingnotes.com/ccna-study-guide/how-switch-learns-the-mac-addresses-explained.html)
- [Cisco Documentation: Cisco Nexus 5000 Series NX-OS Software Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus5000/sw/configuration/guide/cli/CLIConfigurationGuide/MACAddress.html)
- [Cisco Documentation: MAC Address Table Aging Time](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus3000/sw/layer2/503_U2_1/b_Cisco_n3k_layer2_config_guide_503_U2_1/b_Cisco_n3k_layer2_config_gd_503_U2_1_chapter_01101.html)

###### [↑ Go to Top of Page ↑](#topofpage)
