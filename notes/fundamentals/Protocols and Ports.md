Protocols and Ports

**Protocol**
- Defines packet format
- Defines permissible requests and responses
- Format of header information and data
- Packet ordering and timing

**Protocol Standards**
- Documents that define protocols
- RFC (Request for Comments) – Internet protocol standards

**Port Numbers**
- Defines witch application a TCP or UDP segment belongs to
- Well-known ports: 0 – 1023 (RFC 1700) – by IANA
- Registered ports: 1024 - 49151
- Dynamic ports (also called private ports): 49152 – 65535

**Note:**
- The standard ping command does not use TCP or UDP. It uses ICMP. To be more precise ICMP type 8 (echo message) and type 0 (echo reply message) are used. ICMP has no ports!
- See RFC792 for further details.
- ICMP is a control protocol, meaning that it designed to not carry application data, but rather information about the status of the network itself
- Both Transmission Control Protocol (TCP) and User Datagram Protocol (UDP) are transportation protocols, they are used to pass the actual data
- The primary difference is that TCP and UDP are for transferring application data (i.e. whatever the app desires), whereas ICMP is a "control" protocol that transfers information about other protocols.

