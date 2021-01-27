```
! - Show if interface is connected, an duplex/speed
show interface status

! - Show layer 1 and 2 status of interface
show ip interface brief


show power inline module [#]
show power inline [interface]


show interfaces Gig#/# tranciever detail


! - Last time interface was in use:
show interfaces | include line|Last input

! - Test cable signals
test cable-diagnostics tdr interface Gig#/#/#
show cable-diagnostics tdr interface Gig#/#/#


show run | include Chevron
! to find the pod 

```
