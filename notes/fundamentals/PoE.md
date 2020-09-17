# PoE

PSE & PD

IEE Standards for PoE
- IEEE 802.3af
- IEEE 802.3at
- IEEE 802.3bt

PoE device categories:
- PSE (Power Sourcing Equipment) - provide power (e.g. PoE switch)
- PD (Power Devices) - devices that uses power (e.g. access point, telephone)



IEEE Standard | Type | Power Budget per Device
IEEE 802.3af | Type 1 | 15.4W
IEEE 802.3at / PoE+ | Type 2 | 30.8W
802.3bt / Cisco UPoE | Type 3 | 60W
IEE 802.3bt / UPoE+ | Type 4 | 90-95W

- Note: Power budge is how much power leaes the switch, but not that exact amount will reach the device, some is loss while transmitted
"Power Budget" - maximum power the switch (or switchport) can deliver out the port


PoE Detection & Negotiation
- How does switch know if end device needs power or not? And how much power?
- PSE outputs a small amount of power to detect if there is any resistance
- PD has a special resistor in the NIC that will respond, and limit this incoming voltage and relflect back a certain amount of PSE
- PSE now knows it is connected to a PD
- If power received back is less than transmitted (but within a ratio), the switch detects it as a PD
- If power received back is the same, it is not a pD
- Switch will do this process a few more times to determine how much power the device needs and other info, etc.
- If device is powered on from the switch and it has CDP/LLDP enabled, that is another way for the switch to communicate with it and get info about it

````
Show command:
show cdp neighbor detail | include Power
show power inline
````
