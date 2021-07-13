

### Show Commands
```
show module
show switch detail
show version
```
---

### Examples

#### show module

```
Switch#show module 
Switch  Ports    Model                Serial No.   MAC address     Hw Ver.       Sw Ver. 
------  -----   ---------             -----------  --------------  -------       --------
 1       56     WS-C3850-48F-L        FOC1734U09T  5017.ff81.9a00  V02           16.3.7        
 2       56     WS-C3850-48F-L        FOC1734U011  e8ed.f300.1f00  V02           16.3.7        
 3       56     WS-C3850-48F-L        FOC1734X04R  5017.ffd8.3800  V02           16.3.7        
 4       56     WS-C3850-48F-L        FOC1733X05V  5017.ff71.c680  V02           16.3.7        
```

#### show switch detail

```
Switch#show switch detail
Switch/Stack Mac Address : 5017.ff81.9a00 - Local Mac Address
Mac persistency wait time: Indefinite
                                             H/W   Current
Switch#   Role    Mac Address     Priority Version  State 
------------------------------------------------------------
*1       Active   5017.ff81.9a00     15     V02     Ready               
 2       Member   e8ed.f300.1f00     1      V02     Ready               
 3       Member   5017.ffd8.3800     1      V02     Ready               
 4       Standby  5017.ff71.c680     1      V02     Ready               



         Stack Port Status             Neighbors     
Switch#  Port 1     Port 2           Port 1   Port 2 
--------------------------------------------------------
  1         OK         OK               2        4 
  2         OK         OK               3        1 
  3         OK         OK               4        2 
  4         OK         OK               1        3 
```

#### show version
```
Switch#show version
Cisco IOS Software [Denali], Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 16.3.7, RELEASE SOFTWARE (fc4)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2018 by Cisco Systems, Inc.
Compiled Fri 03-Aug-18 23:49 by mcpre


[Excluded output]


ROM: IOS-XE ROMMON
BOOTLDR: CAT3K_CAA Boot Loader (CAT3K_CAA-HBOOT-M) Version 4.68, RELEASE SOFTWARE (P)

[Excluded output]


Switch Ports Model              SW Version        SW Image              Mode   
------ ----- -----              ----------        ----------            ----   
*    1 56    WS-C3850-48P       16.3.7            CAT3K_CAA-UNIVERSALK9 INSTALL
     2 56    WS-C3850-48P       16.3.7            CAT3K_CAA-UNIVERSALK9 INSTALL
     3 56    WS-C3850-48P       16.3.7            CAT3K_CAA-UNIVERSALK9 INSTALL
     4 56    WS-C3850-48P       16.3.7            CAT3K_CAA-UNIVERSALK9 INSTALL

[Excluded output]
```

