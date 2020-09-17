What happens if the native vlan does not match on both ends?
- Received BPDU with inconsidetnt peer - detected by CDP

What if VLAN is pruned only in one direction and not on both ends?
- You will get a one-way trunk. VLAN traffic will be forwarded from the switched that is not purning to the switch that is pruning. But it will not return from switch that is pruning to the switch that is not pruning.


What happens if VLAN 1 is pruned?
- VLAN 1 mimimzation - vlan 1 is sitll used by protocols that require it. Control plane protocls that use it will still work.

What if allowed list is not used with pruning?
- it will break VTP pruning. The two must be combined. 

What happens if nonegotiate is configured on access port?
- DTP is already disabled when a switchport is put into access mode (`switchport mode access`). nonegotiate has no affect. It only has an affect on trunk ports.

what happens if both sides of switch is in dynamic auto?
what happens if both sides of link are using different trunking protocols?
What happens if VTP domains do not match?
What happens if VTP password does not match?
