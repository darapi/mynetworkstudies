Verify MAC address is learned on the access switch
`show mac addresss-table address [mac_address]

See what interfaces the VLAN is trunked out of on the access switch
show interfaces trunk

If it is a port channel find the memberts of that port channel
show interface Po[#} | include Member

Find the IP address of the device on the other end of that port channel 
show cdp neighbors Gig [#/#] detail

Remote into the next device and repeat the steps until you make it to the SVI


Verify the VLAN exists and that STP is forwardng the traffic
`show blan brief | include active`
`show spanning-tree vlan [vlan_id]`

