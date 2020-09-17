<a id="topofpage"></a>

# BGP (Border Gateway Protocol)

---

# Table of Contents

- [BGP Overview](#bgp-overview)
- [BGP Neighborship](#bgp-neighborship)
- [BGP Neighbor Adjacency States](#bgp-neighbor-adjacency-states)
- [BGP Messages](#bgp-messages)
- [The BGP Table](#the-bgp-table)
- [Advertising Networks into BGP](#advertising-networks-into-bgp)
- [Route Summarization](#route-summarization)
- [iBGP](#ibgp)
- [BGP Path Selection](#bgp-path-selection)
- [BGP Configuration Commands](#bgp-configuration-commands)
- [BGP Verification Commands](#bgp-verification-commands)
- [Useful Links](#useful-links)
- [Glossary](#glossary)

---

# BGP Overview

**Note:**
- BGP is an application used to exchange Network Layer Reachability Information (NLRI) – not a routing protocol
- Advertises prefix details but not the path details
  - IPv4 NLRI contains:
  - Prefix/Length
  - Attributes
  - Next-Hop
 
## General Info

Category | Info 
---|---
eBGP Administrative Distance | 20
iBGP Administrative Distance | 200
EGP type | Path-Vector
Protocol Typ | Path Vector
RFC / Proprietary | RFC4271
Algorithm | BGP Best Path Selection Process
Transport protocol | TCP/179
Metric | AS Path Hop / Policy
Best path selection | BGP Best Path Selection Process
Hello interval | N/A
Update destination | Unicast neighbors
eBGP Update Interval | 30 seconds
iBGP Update Interval | 5 seconds
Full of partial updates | Partial updates
Triggered updates | No
Authentication | MD5
Route-tags | On redistribution into and out of BGP

---

# BGP Neighborship

## Overview:

The same commands are used for configuring iBGP and eBGP neighbors
The only thing that distinguishes iBGP from eBGP is the ASN.

**Note:**
- iBGP requires a **full-mesh** between all iBGP routers, due to **Split-Horizon**
- Loopback IP addresses must be **advertised into an IGP** (e.g. OSPF, EIGRP)

### Configuration

```
R1(config)#router bgp [ASN]
R1(config-router)#bgp log-neighbor-changes
R1(config-router)#neighbor [ip_address] remote-as [ASN]
R1(config-router)#neighbor [ip_address] ebgp-multihop 2
R1(config-router)#neighbor [ip_address] update-source loopback [#]
R1(config-router)#no auto-summary
R1(config-router)#exit
```

**Note**
- `neighbor [ip_address] update-source loopback [#]` - It's best practice to use loopback interfaces as the source for iBGP sessions. Physical interfaces may go down, but the loopback remains up unless the router is offline.
- `neighbor [ip_address] ebgp-multihop 2` - TTL must be +1 since BGP is being sourced from the loopback instead of directly connected interfaces

## eBGP Multihop

eBGP routers are not required to be directly connected for them to form a neighbor adjacency, as long as the TTL value is configured correctly.
By default, the TTL value is set to 0, which only allows for directly connecteed neighbors to form an adjacency. 
The TTL value must be adjusted based on the number of hops between the two neighbors.
Use the `ebgp-multihop` command instead of `remote-as` command.

```
R1(config)#router bgp [ASN]
R1(config-router)#bgp log-neighbor-changes
R1(config-router)#neighbor [ip_address] remote-as [ASN]
R1(config-router)#neighbor [ip_address] ebgp-multihop 2
R1(config-router)#neighbor [ip_address] update-source loopback [#]
R1(config-router)#no auto-summary
R1(config-router)#exit
```

### Configuration

```
R1(config)#router bgp [ASN]
R1(config-router)#neighbor [ip_address] ebgp-multihop [TTL]
R1(config-router)#exit
```

###### [↑ Go to Top of Page ↑](#topofpage)

---

# BGP Neighbor Adjacency States

Unlike OSPF and EIGRP, BGP neighbors must be configured manually.
BGP IP port: TCP 179

<img src="https://github.com/darapi/StudyNotes/blob/master/images/BGP-Neighbor-States.jpg" alt="BGP Neighbor States 1" width="50%" height="50%">

<img src="https://github.com/darapi/StudyNotes/blob/master/images/BGP%20nghbr%20states.jpg" alt="BGP Neighbor States 2" width="50%" height="50%">

**1. Idle** - (Verifies route to neighbor)

- Waits for the `Start Event`
  - When a new BGP neighbor is configured
  - When a BGP peer session is reset
- Resets `ConnectRetry` timer
- Looks in RIB for route to reach neighbor
- Starts TCP 3-Way Handshake
- Continues to listen for a connection from neighbor

**2. Connect** - (Completes TCP 3-Handshake)

- Waits for completion of TCP 3-Way Handshake
  - If fails, goes into ***Active*** state. 
- If `ConnectRetry` timer expires:
  - Remains in ***Connect*** state
  - Attempts TCP 3-Way Handshake again
  - Resets the `ConnectRetry` timer
- Any other issues that may occur puts it back to ***Idle*** state
- Sends `Open` message with BGP parameters

**3. Active** - (Skipped if Connect state passes)

- Completes another TCP 3-Way Handshake
- If `ConnectRetry` timer expires, it will go back to ***Connect*** state
- Listens for incoming connections
 
**4. OpenSent** - (Open message sent to neighbor)

- Expects to receive an `Open` message
  - Contains parameters: BGP version number, ASN, etc.
  - If mismatch, replies with `Notification` message and goes back to ***Idle*** state
- Decides to use eBGP or iBGP depending on ASN in the `Open` message
- If successful, sends `Keepalive` message
- Negotiates `Hold Timer` (lowest value selected)
  - If expires, sends `Notification` message + error code & goes back to ***Idle*** state
- If TCP session fails, goes back to ***Active*** state

**5. OpenConfirm** - (Neighbor replied with Open message)

- Waits to recveive `Keepalive` messages, and keep sending them
- Resets `Hold` timer
- If `Notification` message received, goes back to ***Idle*** state

**6. Established** - (Adjacency established)

- Adjacency complete
- Sends update packets, exchanging routing info
- `Hold` timer reset everytime `Keepalive` is received
- If `Notification` message is received, goes back to ***Idle*** state

### Verification

Command | Expected Output
--- | ---
`debug ip bgp` | Step-by-step process of BGP neighborship

<img src="https://github.com/darapi/StudyNotes/blob/master/images/bgp_debug.jpg" alt="BGP Debug output">

###### [↑ Go to Top of Page ↑](#topofpage)

---

# BGP Messages

## Overview

BGP uses different messages type to establish and exchange info with neighbor:

- [Open Message](#open-message)
- [Update Message](#update-message)
- [Keepalive Message](#keepalive-message)
- [Notification Message](#notification-message)

All BGP messages have a fixed-size header and a "type" field to identify the message type.

### Open Message

Open messages contains info about the router and is used to establish a BGP session. This is done after the TCP 3-Way Handshake. Parameters must be accepted by both routers.

Field | Description 
--- | ---
`Marker` | MD5 Authentication; All 1's = active; All f's = disabled.
`Version` | Current BGP version is 4 (RFC 4271)
`My AS` | ASN of the router. Determines iBGP or eBGP
`Keepalive` | Sent every X seconds, notifying neighbor that router is still "up". Cisco IOS default value is 60 seconds.
`Hold Time` | If `keepalive` message not received before `Hold Time` expires, session is removed. Default value for Cisco IOS is 180 seconds. BGP uses lowest configured hold down timer. Typically 3 times the value of the Keepalive timer.
`BGP Identifier` | Local BGP RID, elected same way as OSPF. 1. RID configured via `bgp router-id` command, 2. highest IP on loopback, 3. highest IP on physical interface.
`Optimal Parameters` | For future upgrades to BGP protocol, so that they won't have to create a new BGP version. Includes MP-BGP, Route Refres, 4-octet AS numbers.

<img src="https://github.com/darapi/StudyNotes/blob/master/images/xwireshark-capture-bgp-open-message.png" alt="BGP Open Message Packet Capture">

### Update Message

Used to exchange routing info, after neighborship has been established.
- Info about **NLRI (Network Layer Reachability Information)** - BGP version of a prefix

Info | Descripton
--- | ---
`Withdrawn Route Length` | Shows length of the `Withdrawn Routes` field in bytes. When set to 0, there are no routes withdrawn and the Withdrawn Routes field will not show up.
`Withdrawn Routes` | Shows all the prefixes that should be removed from BGP table
`Total Path Attribute Length` | Total length of the `Path Attributes` field
`Path Attributes` | e.g. origin, as_path, next_hop, med, local preference, etc Stored in TLV-format (Type, Length, Value).

BGP Attirbute Flag | Descripton
--- | ---
`Optional` | when the attribute is well-known this bit is set to 0, when its optional it is set to 1
`Transitive` | when an optional attribute is non-transitive this bit is set to 0, when it is transitive it is set to 1
`Partial` | when an optional attribute is complete this bit is set to 0, when it’s partial it is set to 1
`Extended Length` | when the attribute length is 1 octet it is set to 0, for 2 octets it is set to 1. This extended length flag may only be used if the length of the attribute value is greater than 255 octets

<img src="https://github.com/darapi/StudyNotes/blob/master/images/xwireshark-capture-bgp-update-route-message.png" alt="BGP Update Message Packet Capture">

<img src="https://github.com/darapi/StudyNotes/blob/master/images/xwireshark-capture-bgp-update-withdrawn-message.png" alt="BGP Update Message Withdrawn Route Packet Capture">

### Keepalive Message

Sent every 60 seconds to notify neighbor that local router is still "up". If Keepalive Message is not received before the Hold Timer expires (3 x 60 = default 180 seconds), will remove routes from that BGP neighbor.

<img src="https://github.com/darapi/StudyNotes/blob/master/images/xwireshark-capture-bgp-keepalive-message.png" alt="BGP Keepalive Message Packet Capture">

### Notification Message

Sent when an error occurs, resulting in termination of BGP adjacency.
- TCP session will be cleared
- All entries from this BGP neighbor will be removed from BGP table 
- Update messages with route withdrawals will be sent to other BGP neighbors

**BGP Eror codes**
- Message header error
- Open message error
- Update message error

**BGP Subtype Error Codes**
- Unsupported version number
- Bad peer AS
- Bad BGP identifier
- Unsupported optional parameter
- Unacceptable hold time

List of BGP Error codes can be found on <a href="https://www.iana.org/assignments/bgp-parameters/bgp-parameters.xhtml#bgp-parameters-3">IANA - BGP Error (Notification) Codes</a>

<img src="https://github.com/darapi/StudyNotes/blob/master/images/xwireshark-capture-bgp-notification-message.png" alt="BGP Notification Message Packet Capture">

###### [↑ Go to Top of Page ↑](#topofpage)

---

# The BGP Table

The command `show ip bgp` will display the paths that BGP has learned.
Each path will have a status code.

Status Code | Description
--- | ---
`*` | This is a valid route and that BGP is able to use it
`>` | This entry has been selected as the best path
`*>` | This is a valid route and the best path. It will appear in the routing table `show ip route bgp`
`s` | ***Surpressed*** - BGP knows the network but won’t advertise it, this can occur when the network is part of a summary.
`d` | ***Damped*** -  BGP doesn’t advertise this network because it was flapping too often (network appears, disapears, appears, etc.) so it got a penalty.
`h` | ***History*** - BGP learned this network but doesn’t have a valid route at the moment.
`r` | ***RIB-failure*** - BGP learned this network but didn’t install it in the routing table. This occurs when another routing protocol with a lower administrative distance also learned it.
`s` | ***Suppressed*** - this is used for non-stop forwarding, this entry has to be refreshed when the remote BGP neighbor has returned.
`i` | ***Internal*** - Advertised into BGP using the `network` command
`?` | ***Redistributed*** into BGP
`e` | EGP (Legacy status code)

###### [↑ Go to Top of Page ↑](#topofpage)

---

# Advertising Networks into BGP

## Overview

There are two ways to advertise networks into BGP:
- [Method 1: Network Command](#method-1network-command)
- [Method 2: Redistribution](#method-2redistribution)

## Method 1: Network Command

### Overview:

The `network` command in BGP functions similar to OSPF, except a few differences:
- Auto-Summary is disabled by default. The exact network and subnet mask must be entered. See [Route Summarization](#route-summarization)
- Uses subnet mask instead of wildcard mask

### Configuration

```
! - Advertise a network that is directly connected:
R1(config)#router bgp [ASN]
R1(config-router)#network [ip_address] mask [subnet-mask]
R1(config-router)#exit

! ---

! - Advertise a discarded route:
! - Done by configuring a static route
R1(config)#ip route [ip_address] [subnet-mask] null 0
```

**Note**
- `network [ip_address] mask [subnet-mask]` must have the exact network and subnet mask because auto-summarization is disabled by default (unless it is enabled)

### Verification

Command | Expected Output
--- | ---
`show running-config bgp` | The `network` commands you just entered.
`show ip bgp [ip_address]` | ---
`show ip route [ip_address]` | Advertised routes appear in the RIB


## Method 2: Redistribution

Routes can be redistributed from another protocol (e.g. OSPF, EIGRP) into BGP.

### Configuration

```
R1(config)#router bgp [ASN]
R1(config-router)#redistribute [ospf/eigrp] [PID/ASN]
```

**Note**:
- `redistribute [ospf/eigrp] [PID/ASN]` - will redistribute ***all*** OSPF/EIGRP routes into BGP.

### Verification

Command | Expected Output
--- | ---
`show ip route [ip_address]` | Route appears as "directly connected" on local router
`show ip bgp` | Network has next-hop `0.0.0.0` on local router's BGP table
`show ip bgp [ip_address]` | Network is learned by other routers

###### [↑ Go to Top of Page ↑](#topofpage)

---

# Route Summarization

## Overview

By default, route summarization is *disabled* and a network will not be advetised into BGP unless an *exact match* already exists in the routing table.

Benefits of route summarization:
- Conserves router resources
- Reduces size of routing table, accelerating best-path calculation
- Hides route flaps from downstream routers, enhancing stability

There are three methods to BGP route summarization:
- [Method 1: Aggregate Address](#method-1-aggregate-address)
- [Method 2: Manual](#method-2-manual)
- [Method 3: Auto-Summary](#method-3-auto-summary)

## Method 1: Aggregate Address

### Overview

The `network` command is used to enter each individual network (with exact prefix and mask).
Those networks can then be summarized using the `aggregate-address` command. This will only summarize the configured subnets that fall within range of the summarized prefix.

### Configuration

```
R1(config)#router bgp [ASN]
R1(config-router)#network [address_1] mask [subnet_mask]
R1(config-router)#network [address_2] mask [subnet_mask]
R1(config-router)#network [address_3] mask [subnet_mask]
R1(config-router)#aggregate-address [summarized_prefix] [summarized_mask] summary-only
R1(config-router)#exit
```

### Verification

Command | Expected Output
--- | ---
`show ip bgp  ` | Status code for summarized route is `*>`, and for individual routes `s>`


## Method 2: Manual

### Overview

With route-summarization being disabled (by default), a route will not be advertised into BGP unless an exact match is already existing in the RIB. 

The summarized prefix can be manually added to the RIB by configuring a **discarded route**. This will then allow for a summarized prefix to be advertised into BGP via the `network` command.

The purpose of the discarded route:
- For the summarized prefix to appear in the RIB
  - A requirement for the `network` command to advertise the summarized prefix into BGP
- Prevent routing loops
  - Discards packets that don't match more specific entries in the RIB
  - Note: Think of this as the RIB version of an ACL; permits specific subnets and discards all else within the summarized range

### Configuration

```
R1(config)#ip route [summarized_prefix] [summarized_mask] null0

R1(config)#router bgp [ASN]
R1(config-router)#network [summarized_prefix] mask [summarized_mask]
R1(config-router)#exit
```

### Verification

Command | Expected Output
--- | ---
`show ip route [ip_address]` | The discarded route appears in the routing table
`show ip bgp [ip_address]` | The advertised summarized route appears in the BGP table


## Method 3: Auto-Summary

### Overview

This is disabled by default. If it is enabled, BGP will automatically advertise the classful network, if the classful network or a subnet of this network exists in the routing table.

### Configuration

```
R1(config)#router bgp [ASN]
R1(config-router)#auto-summary
R1(config-router)#exit
```

### Verification

Command | Expected Output
--- | ---
`show running-config bgp` | The `no auto-summary` command is configured under BGP.
`show ip bgp` | The classful network will apear.

###### [↑ Go to Top of Page ↑](#topofpage)

---

# iBGP

## Overview:

- Used in a transit AS to advertise internet prefixes between other autonomous systems
- Is capable of handling the internet routing table, unlike an IGP (e.g. OSPF, EIGRP)
- iBGP does not require routers to be directly connected to form a neighborship
  - An IGP stil needs to be configured for routers to be able to communicate with eachother


Why use iBGP instead of an IGBP
- Scalability
  - IGBP utilize too many resources

- Has more ways to filter peers than IGPs (for controllng what you advertise adn receive)
- Slower convergence than IGPs

### Configuration

```
! - 1. Configure an IGP so that routers within the AS can communicate
! - 2. Configure iBGP neighborship
R1(config)#router bgp [ASN]
R1(config-router)#neighbor [ip_address] remote-as [ASN]
R1(config-router)#neighbor [ip_address] update-source loopback [#]
R1(config-router)#neighbor [ip_address] next-hop-self
R1(config-router)#exit
```
**Note**:
- `#neighbor [ip_address] update-source loopback [#]` - It's best practice to use loopback interfaces with iBGP. Physical interfaces may go down, but a loopback will not go down unless the router is down. The loopback IP will be source for the iBGP session.
- `neighbor [ip_address] next-hop-self` - The iBGP router that learns a prefix from an eBGP router, will advertise it to other iBGP routers with a next-hop address of the eBGP router. The other iBGP routers will not know how to reach the eBGP router so the prefix will not be installed in their routing table. This command tells other iBGP routers that to reach the eBGP router (that's advertising the prefix), to go through the local iBGP router. Other iBGP routers  will know how to reach the local iBGP router because it's loopback will be advertised via an IGP.

###### [↑ Go to Top of Page ↑](#topofpage)

---


# BGP Path Selection

Preference | Notes
--- | --- 
If next-hop is inaccessible - ignore route | ---
Highest `weight` | Cisco proprietarry; local to router; default value is 0 for routes not originated by local router.
Highest `LOCAL_PREF` | Used within AS; default value is 100. If a route in BGP table has no `LOCAL_PREF` value, that means it's a 100.
Routes originated by self | Has next-hop of 0.0.0.0 in BGP table.
Shortest `AS_Path` | ---
Lowest Origin | IGP < EGP < Incomplete
Lowest `MED` | MED is exchanged between AS's; MED comparisode made if neighboring AS is same for all routes considered, unless `bgp always-compare-med` command is enabled.
eBGP over Confederation eBGP over iBGP path | ---
Lowest IGP metric to BGP `NEXT_HOP` | Prefers shortest internal path within the AS to reach destination
Oldest path  | The path that was received first; to minimize flapping.
Lowest RID source  | ---
Lowest neighbor IP address | The tie breaker

---

Attribute | Category | Type
--- | --- | ---
1 | `Origin` | WK-M
2 | `AS_PATH` | WK-M
3 | `NEXT_HOP` | WK-M
4 | `MULTI_EXIT_DISC` | O-NT
5 | `LOCAL_PREF` | WK-M
6 | `ATOMIC-AGGREGATE` | WK-M
7 | `AGGRATOR` | O-T
8 | `COMMUNITY` | O-T
9 | `ORIGINATOR_ID` | O-NT
10 | `CLUSTER_LIST` | O-NT

---

# BGP Configuration Commands

BGP Global Commands | Explanation
--- | ---
`router bgp [ASN]` | The BGP process 
`no synchronization` | ---
`bgp log-neighbor-changes` | ---
`network [ip_address]` | Advertise a (summarized) network into BGP. Summarization must be enabled for this to work.
`network [ip_address] mask [mask]` | Advertise a (not summarized) network into BGP. Must exactly match as found in the RIB, unless summarization is enabled.
`aggregate-address [ip_address] [mask]` | Enables summarization only for prefixes within configured range. Prefix must exists in RIB, and also advertised in BGP with the `network` command.
`aggregate-address summary-only` | ---
`no auto-summary` | Default setting, disables auto-summarization globally.

</br>

BGP Neighbor Commands | Explanation
--- | ---
`neighbor [ip_address] remote-as [ASN]` | Configure a neighbor. The router will also use the ASN to determine if to run iBGP or eBGP
`neighbor [ip_address] shutdown` | Admin shutdown BGP neighbor
`neighbor [ip_address] update-source Loopback[#]` | ---
`neighbor [ip_address] route-reflector-client` | ---
`neighbor [ip_address] next-hop-self` | Informs iBGP router that to get to an eBGP prefix go through "self" (local router)

</br>

Insert prefix in RIB | Explanation
--- | ---
`ip route [ip_address] [mask] null 0` | Inserts a prefix into the RIB so that BGP can advertise a network, if the prefix isn't already in RIB
`interface loopback [#]` | Can be used to isnert a perfix into the RIB so that BGP can advertise the network, if the prefix isn't already in RIB

###### [↑ Go to Top of Page ↑](#topofpage)

---

# BGP Verification Commands

## BGP Neighbor Adjacency
- [x] Verify interfaces are up
- [x] Make sure the BGP routers can reach each other (preferrably loopback)
- [x] BGP packets are sourced from the correct interface (preferrably loopback)
- [x] Multihop is configured for eBGP (if necessary)
- [x] TCP port 179 is not blocked

## BGP Route Advertisements
- [x] Prefix is advertised with `network` command has exact subnet mask as found in RIB
- [x] Prefix being advertised with `network` command exists in the RIB
- [x] If prefix range does not exist in RIB, create a discarded route or loopback interface that falls within range
- [x] If classful networks appear in BGP table, auto-summary might be enabled
- [x] Verify route-maps are not blocking the advertisement of prefixes
- [x] iBGP neighbor adjacencies must be a full-mesh, or use a route-reflector or confederation
- [x] Verify next-hop IP address is reachable, for routes to be installed in RIB

Command | Output
--- | ---
`show run \| section router bgp` | Show all BGP configs on router's running configs
`show ip protocols` | Shows running protocols, filters, and summarization
`show ip bgp summary` | ---
`show ip bgp` | Shows destination, next-hop, weight, path, status code
`show ip bgp \| exclude *` | Show learned routes that have issues; excludes valid routes
`show ip bgp [ip_address]` | Shows possible paths to destination & the *best* path
`show ip bgp neighbors` | ---
`show ip route [ip_address]` | Show a route that is in the routing table
`debug ip packet` | ---
`telnet [ip_address] 179` | Test to see if TCP port 179 is being blocked

###### [↑ Go to Top of Page ↑](#topofpage)

---

# Useful Links:

- <a href="https://www.iana.org/">IANA</a>
- <a href="https://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.xml">IANA IPv4 Address Space Registry</a>
- <a href="https://www.ultratools.com/tools/asnInfo">ASN  Lookup Tool</a>
- <a href="https://www.cidr-report.org/as2.0/">CIDR Report</a>
- <a href="https://www.bgp4.as/looking-glasses">Looking Glass Servers</a>
- <a href="https://www.ciscopress.com/articles/article.asp?p=2756480&seqNum=13">Cisco Press BGP Route Summarization</a>
- <a href="https://www.packetflow.co.uk/cisco-ios-bgp-summarization/#:~:text=In%20short%2C%20when%20auto%2Dsummary,no%20auto%2Dsummary%20enabled)">Packetflow BGP Route Summarization</a>
- <a href="http://thebitbucket.co.uk/ccie/topic-notes/routing/dynamic-routing-protocols/bgp-topic-notes/">The Bit Bucket CCIE Notes</a>
- <a href="https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/22166-bgp-trouble-main.html">Cisco - BGP Troubleshooting</a>
- <a href="https://www.iana.org/assignments/bgp-parameters/bgp-parameters.xhtml#bgp-parameters-3">IANA - BGP Error (Notification) Codes</a>

###### [↑ Go to Top of Page ↑](#topofpage)

---

# Glossary:

**BGP (Border Gateway Protocol)**
: EGP used for routing between autonomous systems

**AS (Autonomous System)**
: A collection of networks managed by a single entity or organization

**ASN (Autonomous System Number)**
: Number identifying an AS. Global: 1 - 64511, Private: 64512 – 65535

**ISP (Internet Service Provider)**
: test

**IANA (Internet Assigned Numbers Authority)**
: Organization that assignes public IP addresses. Website: http://www.iana.org/

**RIB (Routing Information Base)**
: The "routing table" that is displayed via `show ip route` command; control plane

**Discarded route**
: A static route that points to a null interface, e.g. ip route `192.168.10.0 255.255.255.0 null0`. Often used to do route summarization in BGP.

**Transit AS**
: An AS that is in between two other autonomous systems

**MED**
: Multi Exit Discriminator

---
  
###### [↑ Go to Top of Page ↑](#topofpage)
