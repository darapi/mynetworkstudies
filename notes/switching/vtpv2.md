<a id="topofpage"></a>
# VTPv2 (Virtual Trunking Protocol Version 2)

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
**Tracking Mechanism** | CRN (Configuration Number)
**Standard** | Cisco proprietary
**OSI Model** | Layer 2 - Data Link
**Compatibility** | Compatible with VTPv1

---
###### [↑ Go to Top of Page ↑](#topofpage)


# New Features

- **Token Ring** - TrBRF and TrCRF
- **Uncategorized TLV support**
- **Version dependent transparent-mode** - VTPv2 transparent swtichs no longer require version to match
- **Consistency checks** - Check VLAN names/values

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

# VTP Advertisements

- VTP advertisements distribute this global domain information:
  - VTP domain name
  - VTP CRN
  - Update identity and update timestamp
  - MD5 digest VLAN configuration, including maximum transmission unit (MTU) size for each VLAN.
  - Frame format

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


# VTP Caveats

**VTP server**
- If a failure occurs while writing configs to NVRAM, VTP server changes to VTP client mode.
  - Switch cannot be returned to VTP server mode until the NVRAM is functioning again.

**VTP client**
- If new VTPv2 client with higher CRN db is added to the network, will overwrite all other databases
- VTP client will move to transparent mode if there is any failure during updating VLAN database received from server.
  - User need to change back the VTP mode to client to get latest database from server

**VTP transparent**
- Unlike VTPv 2 or VTPv3, VTPv1 transparent switches **do not** forward VTP advertisements that they receive from other switches through their trunk interfaces. 
- In VTPv1 and VTPv2, the switch must be in VTP transparent mode when you create extended-range VLANs.
- In VTPv1 and VTPv2, the switch must be in VTP transparent mode when you create private VLANs and when they are configured.

**VTPv2 Pruning**
- A transparent will undo VTP pruning
- Either change the switch from transparent mode to client or disable pruning

---
###### [↑ Go to Top of Page ↑](#topofpage)


# Useful Links

- [Cisco documentation: Catalyst 3560 Software Configuration Guide, Release 12.2(52)SE](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3560/software/release/12-2_52_se/configuration/guide/3560scg/swvtp.html)
- [Cisco documentation: Configuring VTP V3](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus6000/sw/layer2/7x/b_6k_Layer2_Config_7x/config_vtp_v3.pdf)
- [YouTube: VLAN Trunking Protocol (VTP) Explained | Version 1 & 2 by CertBros](https://www.youtube.com/watch?v=Nlyx5lFQR34)

---
###### [↑ Go to Top of Page ↑](#topofpage)


# Glossary:

**VTP (Virtual Trunking Protocol)**
: Used to sync VLAN database across switches within VTP domain. Layer 2 Cisco proprietary protocol. Show command `show vtp status`.

**CRN (Configuration Revision Number**
: Counter used to track most updated VLAN database. Switches sync with database of highest CRN value. 

**VTP server**
: Switch within VTP domain that permits VLAN changes. These changes are then advertised to clients within the domain. 

**VTP client**
: Switch within VTP domain on which VLAN changes cannot be made. VTP client syncs its VLAN database with that of the server. 

**VTP transparent**
: Switch within VTP domain that forwards VTP advertisements. It does not sync itself with the VTP server. 

**vlan.dat**
: File containing local VLAN database. Show command `dir`.

**db**
: Short for "database"

---
###### [↑ Go to Top of Page ↑](#topofpage)

