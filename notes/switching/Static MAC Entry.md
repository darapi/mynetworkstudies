

- CAM table is populated with the source MAC address of incoming frames
- If destination MAC address is found in CAM table, frame is forwarded out of the associated interfaces
- If destination MAC address does not exist in CAM table, the frame is "flooded" out all ports except where it came from
- "Aging Time" is how long an entry remains in the CAM table (unless it is renewed by an incoming frame). Default time is 300 seconds
- Static entries will overrule dynamic MAC entries

## Clearing the CAM table

You can clear:
- Entire CAM table: `clear mac address-table dynamic`
- A specific address: `clear mac address-table dynamic address [address]`
- All entries on an interface: `clear mac address-table dynamic interface [interface]`
- All entries for a VLAN: `clear mac address-table dynamic vlan [vlan]`

## Static MAC entry

- Configure Static MAC address entry:
  - `mac address-table static [mac-address] vlan [vlan-id] interface [interface#/#]`
- Verify
  - `show mac address-table static | include fa#/#`
- Drop frames 
  - `mac address-table static [mac-address] vlan [vlan-id] drop
  
  `


```
! Show MAC addresses dynamically learned on the switch
show mac address-table dynamic
show mac address-table 
```
Verification Command | Explanation 
--- | ---
`show mac address-table ` | Show all contents of CAM table. Use "dynamic" keyword for dynamic entries only
`show mac address-table [mac-address]` | show entry for speciic MAC address
`show mac address interface [interface]` | show all MAC entries for a specific interface
`show mac address-table aging-time` | Show the aging time of MAC addresses

! - Statically configure MAC on specific interface. This MAC cannot be learned on any other interface, and no other MAC can be learned on this interface.
mac address-table static [mac-address] vlan [vlan-id] interface [interface-id]
! - Drop frames that are destined to specified MAC address
mac address-table static [mac-address] vlan [vlan-id] drop

