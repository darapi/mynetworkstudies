# CEF

Switching used to be done in hardware speed
Routing was done in softwasre speed
Now both are done in hardware speed



CAM Table
- Source MAC address
- interface where MAC address was learned on
- To which VLAN the MAC address belongs

TCAM Table
- Access-lists
- QoS information
- routing table

TCAM values:
- 0 = must be 0
- 1 = must be 1
- x = 0 or 1 both acceptable
- Longest match will return a hit
- Useful for a lookup where we dont need an exact match (routing table or ACLs for exmaple)


CAM requires an exact match. e.g. MAC must match exactly to forward frame out interface.
TCAM does not require exact match (routing table, ACL). e.g. A /32 destination address matches a /24 prefix.

ASIC what is?


Types of switching:
- Process switching
  - all packed are examed by CPU and forwarding decisions are made in software, very slow.
  - l3 switch/router will remove header of frame, look up dest IP in routing table for each packet, then forward frame with rewritten MAC addresss and CRC. all done in software.
- Fast switching (route caching)
  - First packet flow is examined by CPU. The forward decisions is cached so the next packets of the same flow get forwarded quicker. Faster.
  - Looks up first IP packet but will store forwarding decision in the fast switching cahce. future packets of the same flow will use info from the cache to mak tthe decision. 
- CEF (Cisco Express Forwarding) 
  - aka "topology based switching"
  - Forwarding table created in hardware beforehand. All packets will be swithced using hardware. Fastest, but has lmitations.  Multilayer switches and routers use CEF.
  - Default config for routers.
  - Builds two hardware tables: FIB and Adjacency table
  - FIB (Forward Information Base) - built from routing table
  - Adjacenecy Table - built based off the ARP table
  
  "Lower end" routers dont have dedicated hardware for forwarding. They store these tables in software.
  
  
  `show ip cef` - sho wfib table
  
 Types of different adjacencies
 - Null adjacency
   - used to send packets to the null0 interface
 - Drop adjacency
   - you'll see 
 - Discard Adjacency
 - Punt adjacency
 - Glean adjacency
  
  
