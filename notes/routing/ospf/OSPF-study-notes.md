<a id="topofpage"></a>
# OSPF Theory

## Table of Contents

- [General Info](#general-info)
- [OSPF Packet Types](#ospf-packet-types)
- [Neighbor Discovery and Adjacency](#neighbor-discovery-and-adjacency)
- [DR/BDR Election](#drbdr-election)
- [OSPF Cost and Load Balancing](#ospf-cost-and-load-balancing)
- [Path Selection](#path-selection)
- [Route Summarization](#route-summarization)
- [LSA Types](#lsa-types)
- [LSA Filtering](#lsa-filtering)
- [LSDB Update](#lsdb-update)
- [OSPF Network Types](#ospf-network-types)
- [Hardening](#ospf-hardening)
- [OSPFv3](#ospfv3)
- [Glossary](#glossary)
- [Random](#random)

---

## General Info

Category | Info 
---|---
Administrative Distance | 110
IGP type | Link-State
Algorithm | Dijkstra's SPF
IP Port | 89 (not TCP/UDP)
Multicast | 224.0.0.5 (DR/BDR: 224.0.0.6)

---

## OSPF Packet Types

- **HELLO**: Neighbor discovery, build and maintain neighbor adjacencies. Multicast IP `224.0.0.5`.
  - Router-ID
  - Hello/Dead interval
  - Neighbors
  - Area ID
  - Authentication
  - Router priority - determines DR/BDR
  - DR IP address
  - BDR IP address
  - Stub Area flag - area type

- **LSA**: Link advertisements used to build the LSDB. There are 7 [LSA types](#lsa-types).
- **DBD**: Summary of the LSDB. Used to compare two router LSDB to check for differences.
- **LSR**: Requests specific link-state record from an OSPF neighbor
- **LSU**: Sends specif.ic link-state records that were requested. Multiple LSA encapsulated inside of an LSU
- **LSAck**: Acknolwedgement packet.

---

## Neighbor Discovery and Adjacency

### Overview

OSPF routers on the same link are *neighbors*. They must establish an *adjacency* in order to exchange OSPF info. There are also ways to speed up the discovery process, or delcare a neighbor dead. In a multiple-access network, a router is elected as a DR and every other router forms an adjacency with the DR, instead of each-other.

### Requirements to establish adjacency

OSPF routers will exchange HELLO packets before forming an adjacency.
The following parameters must be matching on both neighbors
- [x] Unique Router-ID `#show ip protocols`
- [x] Interface Area-ID `#show ip protocols`
- [x] Hello / Dead Interval `#show ip ospf interface f[#/#] | include intervals`
- [x] Interface network address
- [x] Interface MTU `#show interface f[#/#]`
- [x] Network Type
- [x] Authentication `#show run interface f[#/#]`
- [x] Stub Area Flags
- [x] Other optional capabilities

### Adjacency process

Uses `debug ip ospf adj` to see each step in real-time.
1. **Down**: 
Neighbor has not been detected or considered down due to no HELLO packet received within specified dead interval.

2. **Init**: 
Neighbor detected. *HELLO* packet received from neighbor (multicast 224.0.0.5) containing *neighbor RID*. Does not contain local RID.

2.5 **Attempt**: 
Only valid for NBMA networks.  HELLO packet has not been received from the neighbor and the local router is going to send a unicast hello packet to that neighbor within the specified hello interval period.

3. **Two-way**: 
Local router received unicast HELLO packet containing own RID in the Neighbor field. Elects *DR/BDR*. Bidirectional communication and neighborship is established. Databaes exchanged in upcomign states.

4. **Exstart**: 
Determines *Master/Slave* to lead the DB synchronization process. Master has the highest RID.

5. **Exchange**: 
*DBD* packets (summarizing LSDB) are exchanged. IP MTU of used interface is included in the DBD packet.

6. **Loading**:
*LSAck* packet sent upon DBD receipt. DBD is compared to current LSDB and *LSR/LSU* are exhcanged if more info is needed.

7. **Full**: LSDB synchronization complete. Full adjacency established. This adjacency is added to the LSDB and advertised via LSU to other neighbors.

**Note**:
If adjacency get stuck in ExStart state, check the MTU of the interfaces.

<img src="https://github.com/darapi/StudyNotes/blob/master/images/ospf_states.png" alt="OSPF States" width="50%" height="50%">
<img src="https://github.com/darapi/StudyNotes/blob/master/images/OSPF_Adjacency_Wireshark.png" alt="Adjacency wireshark capture">


### Neighbor Down
The Hello/Dead intervals can be reduced to identify a neighbor or declare a neighbor dead, more quickly. The interface commands to adjust the intervals are `ip ospf hello-interval [#]` and `ip ospf dead-interval [#]`. It is recommended that the Dead Interval is always x4 the Hello interval. 
Neighbor discovery/down can be made even quicker with the command `ip ospf dead-interval minimal hello-multiplier [#]`. This will configure the number of HELLO packets sent *per second*. 
Note: check out **Bidirectional Forwarding Detection (BFD)** for reducing failover time

## DR/BDR Election

### Overview
The purpose in selecting DR/BDR is to *limit LSA flooding* in a multi-access network.
Instead forming a full-mesh of adjecencies, each router will establish an adjacency only with the DR.
The DR will serve as a hub to which all LSA packets will be sent to/from.
This election happens in the **Two-way** stage of the OSPF adjacency process.

**Note**: DR/BDR election occurs per multi-access network, **not** per area

### Election Process

1. Router with the highest OSPF Priority becomes DR
2. Router with 2nd highest priority becomed BDR
3. All other routers become DROTHER
4. If priority is a tie, router with highest IP address becomes DR
5. Router with 2nd highest IP address becomes BDR
6. All other routers become DROTHER

- Default priority value is 1
- Routers with priority value of 0 do not participate in DR/BDR election
- Priority can be configured with interface command `ip ospf priority [#]`
- Use `clear ip ospf process` for change to take effect

---

## OSPF Cost and Load Balancing

### Overview

The metric that OSPF uses to determine 'the best path' to a destination is *cost*. 
OSPF will add the cost of each link per path from source to destination.
It will then select the path with the lowest cost value.
If there is more than one path with equal cost, OSPF will load-balance between them

### Metric = Cost

- Cost = *Reference Bandwidth / Interface Bandwidth*
- Default Reference Bandwidth value = 100 Mbps (100000 Kbps)
- Recommended Reference Bandwidth value = 1000 Mbps (1000000 Kbps)
- Manually adjust cost on OSPF interface with `ip ospf cost [value]`
- Look up reference bandwidth with command `show interfaces FastEthernet 0/0 | include BW`
- Look up OSF cost of interface with command `show ip ospf interface FastEthernet 0/0 | include Cost`

### Load Balancing

- Occurs when there are two paths of equal cost
- By default, 4 equal-cost paths can be inserted into routing table for load balancing
  - Can be configured up to 16 paths max
- Interface BW or cost can be changed to configure for load balancing
- Change interface cost with command `ip ospf cost [value]`
- Change interface bandwidth with command `bandwidth [Kbps]
  - This will change the "bandwidth" to manipulate OSPF, does not change the real BW

---

## Path Selection

1. Use **path type** to select the best path (see below)
2. Uses **lowest cost** to determine best path
3. If equal cost, performs **load-balancing**
4. If load-balancing is disabled, selects path with most **stable LSA entry** in LSDB (or lowest RID, not sure)
5. If multiple paths from different OSPF processes, selects **lowest OSPF PID**

**Path Types - Before Cisco IOS release 15.1(2)S:**
1. Intra-Area (O)
2. Inter-Area (O IA)
3. External Type 1 (E1)
4. NSSA Type 1 (N1)
5. External Type 2 (E2)
6. NSSA Type 2 (N2)

**Path Types - After Cisco IOS release 15.1(2)S:**
1. Intra-Area (O)
2. Inter-Area (O IA)
3. NSSA Type 1 (N1)
4. External Type 1 (E1)
5. NSSA Type 2 (N2)
6. External Type 2 (E2)

---

## Route Summarization

OSPF route summarization can only be configured on the ABR (Type 3 LSA) or ASBR (Type 5 LSA). 

**Type 3 Interarea Route Summarization**
- A summary route will only be advertised if you have at least one subnet that falls within the summary range.
- A summary route will have the cost of the subnet with the lowest cost that falls within the summary range.
- Your ABR that creates the summary route will create a **null0** interface to prevent loops.
- OSPF is a classless routing protocol so you can pick any subnet mask you like for prefixes.
- OSPF config is `area [AID] range [prefix] [mask]`

**Type 5 External Route Summarization**
- You can create the summary only on the ASBR.
- A **null0** entry will be created in the routing table for the summary route.
- OSPF config is `summary-address [prefix] [mask]`

---

## LSA Types

### Overview

OSPF LSA packets are used to build the LSDB. Reliable delivery of LSA packets is ensured via implicit and explicit acknowledgements.
An implicit acknowledgement is when a duplicate of the same packet is sent back to the originating router.
Different LSA types are used for the following:
- Area types (backbone, non-backbone, stub)
- Routers (regular, DR, ABR, ASBR)
- Default routes
- External routes

Type     | Name                                                        | Description
-------- | ----------------------------------------------------------- | --------------------------------
Type 1   |  [Router LSA](#lsa-type-1---router-lsa)                     | Represents a router
Type 2   |  [Network LSA](#lsa-type-2---network-lsa)                   | Reperesents the DR
Type 3   |  [Network Summary LSA](#lsa-type-3---network-summary-lsa)   | Inter-area routes
Type 4   |  [ASBR Summary LSA](#lsa-type-4---asbr-summary-lsa)         | Represents an ASBR
Type 5   |  [External LSA](#lsa-type-5---external-lsa)                 | A non-OSPF route
Type 6   |  [Group Membership LSA](#lsa-type-6---group-membership-lsa) | n/a
Type 7   |  [NSSA LSA](#lsa-type-7---nssa-lsa)                         | Used in stub areas in place of Type 5

The LSA type can be viewed with the command `show ip ospf database`

### Detailed Explanations                             

#### LSA Type 1 - Router LSA

All OSPF routers create a single Type 1 LSA, with *info about all OSPF links*.
It is then advertises to the entire local area.
A Type 1 LSA contains the following:
- RID
- The prefix and type ([LSID](#lsid)) of OSPF links

Link Type	| Description	                                  | LSID
----------|-----------------------------------------------|--------------------
1	        | Point-to-point connection to another router	  | Neighbor router ID
2	        | Connection to transit network (multi-access)	| IP address of DR
3	        | Connection to stub network.                 	| IP Network
4	        | Virtual Link	                                | Neighbor router ID

#### LSA Type 2 - Network LSA

A DR will create a Type 2 LSA for each *multi-access network* it connects to.
It is then advertised to the entire local area.
A Type 2 LSA contains the following:
- The Router-ID
- The prefix and mask of OSPF interface on multi-access network
- List of routers that connect to the multi-access network

#### LSA Type 3 - Network Summary LSA

An ABR creates a Type 3 LSA per area, and advertise it to all other areas.
Thus *each area will have information about each-other*. 
Routing table entries with **O IA** are learned through Type 3 LSA. 
A Type 3 LSA includes the following:
- List of subnets in an area

#### LSA Type 4 - ASBR Summary LSA

An ABR creates a Type 4 LSA containing ASBR info.
This is advertised to all OSPF areas, so that they know *how to reach the ASBR*.

#### LSA Type 5 - External LSA

An ASBR creates a Type 5 LSA for *non-OSPF routes*. 
It is then advertised to all areas. These route entries apprear in the routing table with **E1** (cummulitive cost) or **E2** (static cost)

#### LSA Type 6 - Group Membership LSA

Used for [MOSPF](#whatismospf). 
No longer supported by Cisco.
Cisco instead uses [PIM](#whatispim).

#### LSA Type 7 - NSSA LSA

ABR creates Type 7 with exact same content as Type 5 LSA.
Since Type 5 is blocked in a NSSA, a Type 7 is used instead. 
A Type 7 LSA only lives with a NSSA.
These route entries will appear in the routing table with **N1** or **N2**
The Type 7 is eventually converted to Type 5 by other ABRs.

#### Type 8 - External attribute LSA for BGP

Not used on Cisco routers

#### Type 9-11 - Opaque

Reserved for future use. 
Type 10 is used in MPLS traffic engineering

---

## LSA Filtering

### Overview

OSPF can only filter LSA packets because it advertises LSAs instead of routes.
LSA packets are used to build the LSDB, which must be identical across all OSPF routers within an area.
Therefore, LSA filtering cannot be applied within an area as that would create an inconsistency across router LSDBs.

Options for route filtering:
- Filtering the routing table 
- Interarea Type 3 LSA on the ABR
- External Type 5 LSA on the ASBR.

### Filtering - Routing Table

The only option to "filter" within an area is to filter which routes appear in the routing table. However these prefixes will still appear in the LSDB and LSA packets are still being advertised to neighbors.
**Note**: A filtered route may cause a black hole. The route may be filtered from one router's routing table yet still exists on all other router routing tables. Neigihbors will then forward packets to the router on which filtering is configured on, causing packets to be dropped or misrouted.

- **ACL + Distribute-List** - filter which prefixes appear in the routing table; use **in** keyword

### Filtering - LSA Type 3

Interarea Type 3 LSA filtering is configured on the ABR.
A Type 3 LSA can be filtered using a **filter-list** combined with a **prefix-list**. 
This is configured on an **ABR** to prevent filter prefixes **between areas**. 

- **Prefix-List + Filter-List** - filter Type 3 LSA packets (inbound or outbound)
- LSA Type 3 **IN**bound filter-list - filters prefixes of any area **from entering IN a specific area**
- LSA Type 3 **OUT**bound filter-list - filters prefixes of a specific area **from getting OUT of that area**

### Filtering - LSA Type 5

External Type 5 LSA filtering is configured on the ASBR. 
There are three possible methods for filtering:
- **ACL + Distribute-List** - filter certain networks from entering the area, use *out* keyword
- **ACL + Route-Map + Redistribution** - filter what is being redistributed into OSPF
- **Summary Address No-Advertise** - do not advertise specified prefix in OSPF

---

## LSDB Update

![LSDB Flowchart](https://github.com/darapi/StudyNotes/blob/master/images/lsa_lsdb_flooding.png)

LSA components that determine how ***recent*** it is:
- A higher sequence number.
- A higher checksum number.
- An age equal to the maximum age.
- If the link-state age is much younger.

LSA Sequence Number:
- There are 4 bytes or 32-bits.
- Begins with 0x80000001 and ends at 0x7FFFFFFF.
- Every 30 minutes each LSA will age out and will be flooded:
  - The sequence number will increment by one
  - The last sequence number 0x7FFFFFFF it will wrap around and start again at 0x80000001

---

## OSPF Network Types

### Overview 

Network Type | Subnet | Hello/Dead | DR/BDR | Proprietary | Hello Packet | Neighborship | Network | Next Hop
--- | --- | --- | --- | --- | --- | --- | --- | ---
PtP | Different | 10/40 | No | Cisco | Multicast | Auto | PPP, HDLC, FR P2P | neighbor
PtMP | Same | 30/120 | No | RFC | Multicast | Auto | FR Multipoint | neighbor
PtMP-NB | Same | 30/120 | No | Cisco | Unicast | Configured | FR Multipoint | neighbor
BMA | Same | 10/40 | Yes; Auto-elected | Cisco | Multicast | Auto | Eth, Token, FDDI | source
NBMA | Same | 30/120 | Yes; Configured | RFC | Unicast | Configured | FR Multipoint, X.25, ATM | source

**Notes:**
- DR/BDR election is required on multi-access networks (BMA, NBMA). Not requried on "Point" networks.
- Neighbors must be configured on Non-Broadcast networks because auto-discovery wont' work since multicast is not supported.
- Only PtP requires a different subnet per PVC. All other types share the same subnet.
- Next-Hop on BMA and NBMA is the source where the network is being advertised from. FR map tells router how to go through Hub to reach spoke.

### PtP (Point-to-Point network)
A serial connection between two routers.

### Point-to-Multipoint
The Hub has a point-to-pont connection to each spoke over a Non-Broadcast Multi-Access network.
A DR/BDR is not necessary in this topology.

### Point-to-Multipoint Non-Broadcast
test

### Broadcast Multi-Access network
Two or more routers on the same subnet (***multi-access***) connected to an Ethernet switch. OSPF will automatically elect a DR/BDR.
The next two types of network are used to accommodate Multi-Access technologies that don’t support broadcast.<br/>
These technologies include Frame Relay and ATM.

### NBMA (Non-Broadcast Multi-Access network)
Two or more routers on the same subnet connected over a ***non-broadcast*** technology (e.g. Frame-Relay).
To emulate a broadcast, OSPF sends unicast packets to all destinations.
In this case, the Hub router must become the DR by configuring the Spokes as DROTHER (command: `ip ospf priority 0`).
Configure `ip ospf network non-broadcast` on the Hub and the Spoke routers.

---

## OSPF Hardening

### Overview

There are two options to making OSPF more secure
- Authenticating neighbor adjacencies
- TTL security checks, to prevent spoofing
- Disable unecessary HELLO advertisements on interfaces

#### OSPF Neighbor Authentication

There are four options for authentication
- Aut:0 - Null authentication
  - No configs need to be made for this
- Aut:1 - Plain text authentication
  - Configured at interface level
- Aut:2 - MD5 authentication
  - Configured at interface level, or entire area (via key chain)
- HMAC-SHA authentication
  - Configured at interface level or entire area (via key chain)

#### TTL Security Check

- Router discards OSPF packets bellow TTL treshold (default is 255)
- OSPF packets with TTL of 255 is only possible from adjacent neighbors (266 - 1 = 255)
- Not applied to virtual links or sham links by default
- If you want to use this, then you can use the `area virtual-link ttl-security` or `area sham-link ttl-security` commands

### Passive Interfaces

It is sometimes undesirable to send HELLO packets out of certain interfaces. For example, those that connect to L2 switches.

---

## Area Types

### Overview
All areas must connect to Area 0, also called the Backbone area. Routers located in Area 0 are referred to as Backbone routers. An ABR is a router between two areas. An ASBR is a router running a routing protocol in addition to OSPF.

**Advantages of using areas:**
- Reduce memory consumption
- Lower cpu intensitiy
- Smaller LSDB
- Reduces complexiity
- Improve convertence speed

---

## OSPFv3

### Overview

- **Link-local addresses** : Packets are sourced from link-local IPv6 addresses
- **Links, not networks**: Uses the term "links" instead of "networks"
- **New LSA types**: Two new LSA types, and LSA type 1 and 2 have changed
- **Interface commands**: OSPFv3 is enabled on interfaces, instead of `network` command
- **Router ID**: Must be manually configured, auto self-assign feature not available
- **Multiple prefixes per interface**: Will advertise all configured IPv6 prefixes on a single interface 
- **Flooding scope**: Has a flood scope for different LSA
- **Multiple instances per link**: Capable of running multiple OSPFv3 instances per link
- **Authentication**: IPv6 IPSec authentication only
- **Prefixes in LSAs**: Shows prefixes in LSAs as prefix + prefix length.


### OSPFv3 LSA Types

v3 Type | v3 Name | v2 Type | v2 Name
--- | --- | --- | --- 
0x2001 | Router LSA | 1 | Router LSA
0x2002 | Network LSA | 2 | Network LSA
0x2003 | Inter-Area Prefix LSA | 3 | Network Summary LSA
0x2004 | Inter-Area Router LSA | 4 | ASBR Summary LSA
0x4005 | AS-External LSA | 5 | AS-External LSA
0x2006 | Group Membership LSA | 6 | Group Membership LSA
0x2007 | Type-7 LSA | 7 | NSSA External LSA
0x0008 | Link LSA | --- | ---
0x2009 | Intra-Area Prefix LSA | --- | ---

v3 Hex | v3 Scope 
--- | --- 
0x0 | Link-local
0x2 | Single area
0x4 | Entire OSPFv3 routing domain

**Separation of Addressing from the SPF Tree**

LSA Type 1 and Type 2 include topology ***and*** network information in OSPFv2. In OSPFv3, they contain ***only*** topology information (not network). Prefixes are instead advertised through OSPFv3 LSA Type 9.

**Packet Header**

OSPFv6 also has a new field in the packet header called **Instance ID**. This allows multiple OSPFv3 instances to run on a single link. Instance ID must match in order to become neighbors. Value is 0 by default.

**Configuration**
Almost all commands for OSPFv2 are the same, except it will have `ipv6` before the command.
IPv6 must be enabled on interface with the `ipv6 enable` command.
IPv6 routing must be enabled on the router with `R1(config)#ipv6 unicast-routing`

### OSPFv3 Authentication and Encryption

OSPFv3 does not have an authentication field in the packet header. It instead relies on IPsec to do the authentication.
IPsec two encapsulation types: AH (Authenticaiton Header) and ESP (Encapsulating Security Payload).
AH only encrypts the header whereas ESP encrypts the entire packet. With ESP, you can achieve authentication and encryption for OSPFv3.
The following interface command is used for authentication: `ipv6 ospf authentication ipsec spi [#] sha1/md5 [key]`
To configure the same authentication key for the entire area, use `area [AID] authentication` under the OSPFv3 proccess.

ESP Authentication/Encryption
```
R1(config-if)#ipv6 ospf encryption ipsec spi 256 esp aes-cbc 256 [key]
```

Verification Commands:
```
R1#show ipv6 ospf interface Fa #/# | include auth
R1#show crypto ipsec sa
R1#show crypto ipsec policy
```

**Configuring IPv4 on OSPFv3**
```
R1(config)#router ospfv3 1
R1(config)#ipv6 unicast-routing
R1(config)#interface GigabitEthernet 3
R1(config-if)#ospfv3 1 ipv4 area 0
R1(config-if)#ip address [ip_address]
```

---

## Glossary:

**DR (Designated Router)**
: In a *multi-access network*, router with highest priority value becomes the DR. All routers form adjacencies *only* with the DR. LSA packets are sent to and from the DR. This prevents a full-mesh of OSPF adjacencies from occurring, which can flood the network with OSPF hello and LSA packets.

**BDR (Backup Designated Router)**
: If the DR goes down, this router becomes the new DR.

**DROTHER**
: An OSPF router that is not a DR or a BDR in a multiple-access network

**ABR (Area Border Router)**
: A router bridging two OSPF areas. One interface belongs to Area 0 and another interface belongs to Area X.

**ASBR (Autonomous System Border Router)**
: A router bridging the OSPF network to a non-OSPF network. Example: one interface connects to OSPF network, and another interface connects to EIGRP network.

**LSDB (Link State Database)**
: Database mapping the full network topology using info gathered from LSA packets.

**SPF (Shortest Path First algorithm)**
: Algorithm used to determine the shortest path from A to B.

**Metric**
: OSPF uses "cost" as a metric; the formula is: Cost = Reference Bandwidth / Interface Bandwidth

**Hello Interval**
: How often (in seconds) a HELLO packet is sent out. Default is 10 seconds.

**Dead Interval**
: Waiting time (in seconds) to receive a HELLO packet before considering the adjacent neighbor down

<a name="lsid"></a>
**LSID (Link-State Identifier)**
: A 32-bit marking that identifies the LSA type

**NSSA (Not So Stuby Area)**
: test123

<a name="whatismospf"></a>
**MOSPF (Multicast OSPF)**
: Feature no longer used on Cisco devices.

<a name="whatispim"></a>
**PIM (Protocol Independent Multicast)**
: Used for multicast on Cisco devices

**BW (Bandwidth)**
: Typically measured in bits, kilobits, or megabits per second, is the rate at which data flows over the network. This is a measure of throughput (amount per second) rather than speed (distance traveled per second). The "bandwidth" configured on a Cisco interface only affects layer 3 routing protocols such as OSPF cost calculation. It *does not* change the actual bandwidth of the interface.

**HELLO packet**
: Neighbor discovery, neighbor adjacency, maintain adjacency. Sent to multicast 224.0.0.5.

**LSA (Link-State Advertisement)**
: Packet advertising OSPF links. Used to build the LSDB.

**DBD (Database Descrpition)**
: Summary of the LSDB. Used to compare two router LSDB to check for differences.

**LSR (Link-State Request)**
: Requests specific link-state record from an OSPF neighbor

**LSU (Link-State Update)**
: Packent containing specific likn-state records that were requested. Contains multiple LSAs in it.

**LSAck (Acknowledgement)**
: Acknolwedgement packet

**RID (Router-ID)**
: Used to identify OSPF router in LSDB topology. Order of preference: 1. manually configured, 2. highest loopback IP 3. highest active intrface IP.

**AID (Area-ID)**
: Area ID can be expressed with a single number (Area 0) or decimal notation (Area 0.0.0.0)

**Default Route**
: Advertised to all areas via Type 5 LSA. Entry will appear in routing tables as **O*E2**

**OSPF Multi-Access netwwork**
: Two or more routers that are on the same subnet.

**Dijkstra's Algorithm**
: OSPF algorithm that selects path with lowest cost. 

**Cost**
: The metric that OSPF uses to calculated the shortest path to a destination.

---

## Random

##### Default Route

- Advertise default route into OSPF
- Other routers will go through this router to exit the network
- Configure in OSPF process: `default-information originate always`
- The default route will appear on other routers as such: `O*E2 0.0.0.0/0 [110/1] via 192.168.13.3, 00:00:50, FastEthernet1/0`
- configured on ASBR, sends out Type 5 LSA

##### OSPF Authentication Options

- Configured on OSPF interface or OSPF process
- Aut:0 - Null
- Aut:1 - Plain text
- Aut:2 - MD5
  - key-id and password must match on both ends
  
  ## Show Commands

```
R1#show ip route ospf
O    192.168.13.0/24 [110/2] via 192.168.23.3, 00:09:45, FastEthernet1/0
```
- Format: `[protocol]    [destination_ip/[CIDR] [AD/metric] via [next-hop], [timestamp], [egress interface]`
- Timestamp - elapsed time since network was discovered

```
R1#show ip ospf interface fa1/0
FastEthernet1/0 is up, line protocol is up 
  Internet Address 192.168.23.2/24, Area 0 
  Process ID 1, Router ID 2.2.2.2, Network Type BROADCAST, Cost: 1
```
- Cost of interface

---

##Troubleshooting

### Adjacency issues

```
R2#debug ip ospf packet 
OSPF packet debugging is on
OSPF: rcv. v:2 t:1 l:48 rid:1.1.1.1
      aid:0.0.0.0 chk:4D40 aut:0 auk: from FastEthernet0/0
```

- V:2 - stands for OSPF version 2 (IPv6 is version 3)
- T:1 - stands for OSPF packet number 1 (Hello packekt). 
- L:48 is the packet length in bytes. 
- RID 1.1.1.1 - is the Router ID.
- AID:0.0.0.0 - Area ID in decimal notation
- CHK 4D40 - checksum of OSPF packet
- AUT:0 - authenticaiton type (0 = null, 1 = clear-text, 2 = MD5)
- AUK: - Authentication info

  
###### [↑ Go to Top of Page ↑](#topofpage)
