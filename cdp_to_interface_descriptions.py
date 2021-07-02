import re

cdp = """

PASTE OUTPUT HERE

-------------------------
Device ID: SOM-PARK-BLD3-4007OIT-9300.ens
Entry address(es):
  IP address: 10.28.220.5
Platform: cisco C9300-48UXM,  Capabilities: Switch IGMP
Interface: TwentyFiveGigE1/0/5,  Port ID (outgoing port): TenGigabitEthernet1/1/1
Holdtime : 134 sec

Version :
Cisco IOS Software [Gibraltar], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.12.5, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2021 by Cisco Systems, Inc.
Compiled Fri 29-Jan-21 12:11 by mcpre

advertisement version: 2
VTP Management Domain: ''
Native VLAN: 1
Duplex: full
Management address(es):
  IP address: 10.28.220.5

"""


def cleanUp(text):

    output = list()
    text = text.strip() 
    text = text.splitlines()

    for line in text:
        if line.find("Device ID:") != -1 or line.find("Interface:") != -1:
            output.append(line) 
            
    return output


def main():
    
    parsed_data = cleanUp(cdp)
    items = len(parsed_data)-2
    counter = 0
    
    while counter <= items:
        
            hostname = parsed_data[counter]
            hostname = hostname[11:]
            hostname = hostname.strip('\n')
            hostname = hostname.strip(".ens")
            hostname = hostname.upper()
            
            interface_line = parsed_data[counter + 1]
            
            remote_interface = interface_line.split()[-1].upper()
            remote_interface_type = remote_interface[:3]
            port_ID_regex = "(\s?(\d{1,4}(?:\/\d{0,4}){0,2}))"
            remote_interface_id = (re.search(port_ID_regex, remote_interface).group(0))
            
            comma_index = interface_line.find(',')
            colon_index = interface_line.find(':')
            
            local_interface = interface_line[0:comma_index].rstrip(',')
            local_interface = local_interface.replace(':','')
            
            print(local_interface)
            print("  description {} {} {}".format(hostname, remote_interface_type, remote_interface_id))
            print("  exit \n")
            
            counter = counter + 2
            
main()

# Created by: Daniel Arapi (da202)
# Last Updated: 07/02/21
    


