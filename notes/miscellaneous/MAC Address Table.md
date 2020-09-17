A layer 2 switch forwards a frame based on its destination MAC address. In other words, the destination MAC address is used to determine which interface the frame will be forwarded out of. So how does the switch determine the correct interface? This is where the MAC address table comes into play.

The MAC address table contains a list of MAC addresses along with their associated interface. When the switch receives a frame it will look up the destination MAC address in this table and then find the associated interface. That will be the interface the frame will be forwarded out of.

Lets look into an example to understand this better. Consider the network diagram below:

```
S1#show mac-address-table 
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----

   1    0005.5e8e.b275    DYNAMIC     Fa0/1
   1    000a.f323.2793    DYNAMIC     Fa0/3
```
