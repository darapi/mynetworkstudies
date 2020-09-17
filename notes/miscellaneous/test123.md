**VRF Commands**
- `show ip route vrf all [ip_address]`
- `show ip arp vrf all | include [mac|ip]`
- `show ip interface brief vrf all`

**Cisco WLC Commands**
- `debug client [mac]`

**Traceroute**
- cdp neighbors must be enabled:
- `traceroute mac [source_mac] [destination_mac]`
- `traceroute mac ip [source_ip] [destination_ip]`

