
# All BGP Configuration Commands
---

BGP Global Commands | Explanation
--- | ---
`router bgp [ASN]` | The BGP process 
`no synchronization` | ---
`bgp log-neighbor-changes` | ---
`network [ip_address]` | Advertise a (summarized) network into BGP. Summarization must be enabled for this to work.
`network [ip_address] mask [mask]` | Advertise a (not summarized) network into BGP. Must exactly match as found in the RIB, unless summarization is enabled.
`aggregate-address [ip_address] [mask]` | Enables summarization only for prefixes within configured range. Prefix must exists in RIB, and also advertised in BGP with the `network [ip_address] mask [mask]` command.
`aggregate-address summary-only` | ---
`no auto-summary` | Default setting, disables auto-summarization globally.
`clear ip bgp *` | Resets BGP process
`clear ip bgp ?` | ---

</br>

BGP Neighbor Commands | Explanation
--- | ---
`neighbor [ip_address] remote-as [ASN]` | Configure a neighbor. The router will also use the ASN to determine if to run iBGP or eBGP
`neighbor [ip_address] shutdown` | Admin shutdown BGP neighbor
`neighbor [ip_address] update-source Loopback[#]` | ---
`neighbor [ip_address] route-reflector-client` | ---
`neighbor [ip_address] next-hop-self` | Informs iBGP router that to get to an eBGP prefix go through "self" (local router)
`neighbor [ip_address] weight [weight_value]` | Configures weight value for all prefixes from neighbor
`neighbor [ip_address] route-map [route_map_name] in` | Configures weight for specific prefixes from neighbor. Route-map will specify which prefixes, weight value, and ACL.

</br>

Insert prefix in RIB | Explanation
--- | ---
`ip route [ip_address] [mask] null 0` | Inserts a prefix into the RIB so that BGP can advertise a network, if the prefix isn't already in RIB
`interface loopback [#]` | Can be used to isnert a perfix into the RIB so that BGP can advertise the network, if the prefix isn't already in RIB

</br>

Route-Map for BGP Weight | Explanation
--- | ---
`access-list [acl_id] permit [ip_address] [wildcard]` | Create an ACL to match traffic. If ACL is removed, or not added to the route-map configs, the route-map will match everything. Be careful.
`route-map [route_map_name] permit [seq]` | Create a route-map at sequence number [seq]
`match ip address [acl_id]` | Use ACL to match traffic. If this command, or ACL, is not configured, it will match everything. Be careful.
`set weight [weight_value]` | Set weight for prefixes that are matched by the ACL.
`route-map [route_map_name] permit [seq]` | Create a new entry in route-map by using same route_map_name and difference seq number.
`set weight 0` | Set weight to 0 for all other prefixes. Because no ACL is configured for this route-map entry, it will match everythig (except for what is matched by the previous route-map entry).
