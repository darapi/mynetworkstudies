

```
! - Statically configure MAC on specific interface. This MAC cannot be learned on any other interface, and no other MAC can be learned on this interface.
mac address-table static [mac-address] vlan [vlan-id] interface [interface-id]
! - Drop frames that are destined to specified MAC address
mac address-table static [mac-address] vlan [vlan-id] drop
```
