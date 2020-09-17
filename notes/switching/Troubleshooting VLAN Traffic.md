# Troubleshooting VLAN Traffic

- Verify STP is forwarding traffic
  - `show spanning-tree vlan [vlan_id]`
  - `show spanning-tree interface [interface] detail`
- Does VLAN exist? Is it properly assigned?
  - `show vlan brief | include active`
- Is the VLAN trunking? Was it manually pruned?
  - `show interface trunk`
- Is  VTP purning the VLAN?
  - `show interface [interface] pruning`
- Is the port errdisabled?
  - `show interface status`
  - `show interface switchport`
- Data plane filters?
  - `show access-list`
  - `show vlan filter`
  

