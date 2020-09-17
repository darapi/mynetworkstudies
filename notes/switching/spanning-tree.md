
Bridge ID
- Bridge Priority - 0 - 61440 in increments of 4096
- System+

MAC address reduction
- If you have 10 VLANs



Designatedd Port
- Downstream Port forwarding traffic away from the root bridge

Root Port
- Upstream port forwarding data twoards the root bridge


All switches should agree on the root bridge ID is
If multiple switches are claming themselves as root, there may be a layer 2 problem (port or trunk down, allowed list misconfigured)


Port STates
- Root - upworard
- Designated - downarard
- Blocking

Verify interface cost
``


`show spanning-tree detail`
- Hello time, max age, and forward delay, are determined by the root bridge
- sayhs cost of entire path to get to root bridge
Root Bridge sets the timers in STP

Total path cost = local port cost + designated path cost

Designated path cost 0 - only when port is directly connected to root bridge, meaning that it is a root port


a switchport in blocking state isn't actually "blocking" traffic.
The switch simply no longer learns MAC addresses on that interfaces.
A staticall oncigured MAC entry would bypass the blocking state.


Layer 2 forwarding alway shas to be symmetrical
- the path a received frame came from, is the same path the reply will go out of
In layer 3 paths can be different 



In traditionaol STP, BPDU are only originated by the root bridge
in other versions of STP BPDUs are used as a keepalive


if more than one switch claims to be root bridge for a vlan, check that trunk interfaces are allowing vlan on both ends of link
