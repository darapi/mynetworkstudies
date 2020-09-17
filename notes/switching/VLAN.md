VLAN


VLAN | Range | Usage | Propegated by VTP
--- | --- | --- | ---
0, 4095 | Reserved | For system use only. You cannot see or use these VLANs. | ---
1 | Normal | Cisco default. You can use this VLAN but you cannot delete it. | Yes
2-1001 | Normal | For Ethernet VLANs; you can create, use, and delete these VLANs. | Yes
1002-1005 | Normal | Cisco defaults for FDDI and Token Ring. You cannot delete VLANs 1002-1005. | Yes
1006-4094 | Extended | For Ethernet VLANs only. | No





- Standard VLAN
  - Range: 1 - 1005
  - VLAN 1
    - Access ports belong to VLAN 1 by default unless configured otherwise
    - Is the default Native VLAN for 802.1q trunking
    - Cannot be pruned by VTP
    - Best practice: do not assigned access ports to this VLAN
  - Range 1002 - 1005 [legacy]
    - Cannot be deleted, but can be manually pruned from trunks
    - Cannot be pruend by VTP
    - Best practice: do not use for actual port assignments
- Extended VLAN
  - Range: 1006 - 6094
  -  Can be used in VTPv3 and/or locally on switch in VTP Transparent mode
  - Some of these VLANs can be used, some cannot. Depending on the platform. Not standardized. Would need to look up platform documentation.
  - Some are reserved as "Internal VLANs"
    - reserved for internal applications (e.g. native layer 3 switchports)
    - `show vlan internal usage`
    - `show run all | include internal|allocation`
    - Some allocate ascending, or decending
- VLAN Database

Creating VLANs
- config mode
- VLAN database [legacy]
  - Command `vlan database`
- at time of assignment [not recommended]
  - If switch is in VTP Client mode, it will assign port to VLAN but the VLAN wont actually be created. Therefore this method is not recommended.
- Creating a VLAN
  - automatically creates an STP instance once the VLAN is in use (access prot assigned to VLAN or trunk port allowing that VLAN)
  - MAC address table
- Verify VLAN was created
  - `show vlan brief | include active`
  - `show spanning-tree vlan [vlan_number]`
  
```
! Configuring a VLAN
vlan [vlan_id]
  name [vlan_name]
  exit
```  

Switchport Types
- Access Ports
  - interface is assigned to a specific VLAN
- Trunk Port
  - Carries traffic for multiple VLAN
  - Negotiation order: ISL --> dot1q --> access port
  - 802.1q
    - Open standard
    -  Native VLAN is untagged (by default it is VLAN 1)
    - switchport encapsulation dot1qm switchport mode trunk, switchport nonegotiate (disables DTP)
    - switchport mode trunk does not disable negotiaten, it just statically selects the mode
- Dynamic Port
  - DTP negotiated
- Tunnel Switchports
  - Transparent Layer 2 VPN
- interface type verification commands
  - `show interface trunk`
  - `show interface switchport [interface]`
  - `show spanning-tree [vlan|interface]`

```
Name: Ethernet1/1
  Switchport: Enabled <--- Interface is up at L2
  Switchport Monitor: Not enabled
  Operational Mode: trunk <--- switchport type (access or trunk)
  Access Mode VLAN: 1 (default) <--- default VLAN
  Trunking Native Mode VLAN: 1 (default) <--- Native VLAN
  Trunking VLANs Allowed: 102-103,105,110,200-234,236-243,245-247,250,301-335,900-901,1000
  FabricPath Topology List Allowed: 0
  Administrative private-vlan primary host-association: none
  Administrative private-vlan secondary host-association: none
  Administrative private-vlan primary mapping: none
  Administrative private-vlan secondary mapping: none
  Administrative private-vlan trunk native VLAN: none
  Administrative private-vlan trunk encapsulation: dot1q
  Administrative private-vlan trunk normal VLANs: none
  Administrative private-vlan trunk private VLANs: none
  Operational private-vlan: none

```

Trunking
- DTP
- 802.1Q Native VLAN
- Trunking Allowed List



```
S1# show vlan internal usage

VLANs                   DESCRIPTION
-------------------     -----------------
3968-4031               Multicast
4032-4035,4048-4059     Online Diagnostic
4036-4039,4060-4087     ERSPAN
4042                    Satellite
4044                    Native VLAN to enable/disable tagging
4040                    Fabric scale
4041                    Fabric Multicast vpc (FP)
4045                    Fabric Multicast vpc (CE)
4043                    FCF vlans
3968-4095               Current
dhn-t000-n7k-core#
```





