<a id="topofpage"></a>
# VTPv3 (Virtual Trunking Protocol Version 3)

# Table of Contents
- [General Overview](#general-overview)
- [New Features](#new-features)
- [VTP Version Comparison](#vtp-version-comparison)
- [VTP Requirements](#vtp-requirements)
- [VTP Modes](vtp-modes)
- [VTP Advertisements](#vtp-advertisement)
- [VTP Pruning](#vtp-pruning)

---

# General Overview

Category | Information
--- | ---
**Purpose** | Sync VLAN database on all switches within VTP domain
**Tracking Mechanism** | VTP primary server
**Standard** | Cisco proprietary
**OSI Model** | Layer 2 - Data Link
**Compatibility** | Backwards compatible with VTPv2, but not VTPv1

---
###### [↑ Go to Top of Page ↑](#topofpage)


# New Features

**New features in VTPv3:**
- **Primary and backup servers:**
  - By default, all VTPv3 switches operate as backup servers
  - Only the primary server can make VLAN changes in VTP domain
  - Backup servers save a copy of the primary's VLAN db in NVRAM
  - If Primary server reboots, or if VTP domain paramaters change, it is downgraded to backup server.
  - ***Best practice:***
    - Set all switces within domain as backup servers
    - Promote switch to primary server (command `vtp primary`) when making VLAN changes, then revert to backup server when done.
- **Extended VLAN support**
  - VTP servers and clients supports advertisements of extended VLAN range 1006 to 4094 (but not for pruning)
- **Supports other database types**
  - Can also propegate other databases such as MST db info. A seperate instance of VTP runs for each application that uses VTP.
  - Global config
  - Interface-config
    - Cannot have MST on and VTP off, any other combination works.
- **Private VLAN support**
- **Enhanced authentication**
  - VTP athentication password can be configured "hidden" or "secret".
  - "Hidden" - Password is saved in VLAN db file, but appears as a secret key in the running configs.
  - "Secret" - Configure the password by entering the secret key (copy from one switch and paste into others)
- **Interface-level configs** 
  - Use command `no vtp` on trunking interface to turn VTP on/off.
  - Interface-config options:
    - VTP on, MST off
    - VTP off, MST off
    
---  
###### [↑ Go to Top of Page ↑](#topofpage)


# VTP Version Comparison 

Parameter | v1 | v2 | v3
--- | --- | --- | ---
Available Modes | Server, Client, Transparent | Server, Client, Transparent | Server, Client, Transparent, Off
Token Ring Support | No | Yes | Yes
Unrecognized TLV Support | No | Yes | Yes
Version dependent transparent-mode | Yes | No | No
Consistency Checks Supported | No | Yes | Yes
Extended VLAN Support | No | No | Yes
Private VLAN supported? | no | no | yes
MST support | No | No | Yes
Password encrypted? | No | No | Yes
VLAN Update mechanism | CRN | CRN | Primary Server

---
###### [↑ Go to Top of Page ↑](#topofpage)


# VTP Requirements
- [x] Links must be trunking - `show interfaces trunk`
- [x] VTP domain name must match - `show vtp status`
- [x] VTP password must match - `show vtp password`

---
###### [↑ Go to Top of Page ↑](#topofpage)


# VTP Modes

## Comparing Modes

Mode | Modify VLAN db | Source advertisements | Forward advertisements | Sync self | Save in NVRAM
--- | --- | --- | --- | --- | ---
**Server** | Yes | Yes | Yes | Yes | *Yes*
**Client** | No | *Yes* | Yes | Yes | No
**Transparent** | *Locally* | No | Yes | No | Yes
**Off** | No | No | No | No | No

## Configuring VTP Mode

```
S1(config)#vtp mode [server, client, transparent, off]
```

## Verifying VTP Mode:

```
S1#show vtp status
S1#show run | include vtp
```

--- 
###### [↑ Go to Top of Page ↑](#topofpage)


# VTP Advertisements

- VTP advertisements distribute this global domain information:
  - VTP domain name
  - VTP CRN
  - Update identity and update timestamp
  - MD5 digest VLAN configuration, including maximum transmission unit (MTU) size for each VLAN.
  - Frame format
  - Primary servert ID (**new in VTPv3**)
  - Instance number (**new in VTPv3**)
  - Start index (**new in VTPv3**)

- VTP advertisements distribute this VLAN information for each configured VLAN:
  - VLAN IDs (ISL and IEEE 802.1Q)
  - VLAN name
  - VLAN type
  - VLAN state
  - Additional VLAN configuration information specific to the VLAN type

---
###### [↑ Go to Top of Page ↑](#topofpage)


# VTP Pruning

## Overview

- VTP pruning reduces unnecessary replication of: broadacsts, unknown unicasts, unknown multicasts
- On VTPv2, it is only supported in server and client mode, not transparent mode.
- Pruning will not work if there is a transparent switch on the network.
- VTP server/client will only forward out advertisements for VLANs that are being "asked for" by the client. Client will "ask for" VLANs that are currently in use.
- Filter which VLANs are advertised outboun

**Prune Eligible**
- In VTPv2 it is VLAN 2 - 1001

**Not Prune Eligible**
- VLAN 1 and Extended VLANs

**Conencting to non-Cisco switches**
- The Cisco switch will ask what VLANs are needed
- The non-Cisco switch will not reply because it does not run Cisco proprietary VTP protocol
- The Cisco switch does not know what to prune for that interface, therefore it assumes it needs all VLANs
- The Cisco switch sends requests to other Cisco switches that it needs all VLANs - defeats the prupose of purning
- This is fixed by limiting what VLANs are allowd on the trunk port with the command `switchport trunk allowed vlan xyz`

## Configuring VTP Pruning

```
vtp pruning
switchport trunk pruning vlan [vlan_id]
```

## Verifying VTP Pruning

```
show interface trunk
show interface pruning
show interface switchport
```

---
###### [↑ Go to Top of Page ↑](#topofpage)


