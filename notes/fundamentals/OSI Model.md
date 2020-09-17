# The OSI Model

- A framework designed to help understand the process of network communication
- Also helps with troubleshooting
- TCP/IP Model
  - Model designed around the protocols which the Internet has developed (TCP/IP)
  - Only has 4 layers, it groups some of the OSI 7 layers
- OSI Model (Open System Interconnection)
  - Developed by ISO (International Organization for Standardization) in the 1970’s
  - Based off the TCP/IP model, except it’s more generic to accommodates all protocols


**OSI (Open Systems Interconnection)**
- Created by ISO (International Organization for Standardization), in 1983
- Designed to suit many types of protocols: OSI, IPX, SPS and AppleTalk
- Top 3 Layers define data communication
- Bottom 4 Layers define how data is transmitted through which devices


---

# Table

Layer | Description | Services | Protocols | Devices | PDU
--- | --- | --- | --- | --- | --- | ---
7 - Application | Network services | n/a | HTTP, DNS, DHCP, FTP | n/a | Data
6 - Presentation | Performs translation, encryption, compression, and conversion of data. | n/a | TLS, MPEG, MIDI, XDIR, TIFF, PICT | n/a | Data
5 - Session | Initiate, maintian, and terminate sessions. | Sync and dialog control (half or full duplex) | SIP, NetBIOS, SCP, SQL, NFS, ZIP | n/a | Data
4 - Transport | Provides process to process message delivery | Flow control, error control, segmentation, congestion control | TCP, UDP | n/a | Segments (TCP), Datagrams (UDP)
3 - Network | Packet switching and routing, routes packets across a network | n/a | Routed: IP (version 4 and outing: RIPv2, OSPF, EIGRP, IS-IS, BGP | Routers, Layer 3 switches | Packets
2 - Data Link | Adds header that includes source and destination MAC | Flow Control, error control, QoS, link management | ARP, CDP, LDP, HDLC, PPP, Frame Relay, MPLS | Switches, Bridges | Frames
1 - Physical | Transmission of raw bits over a physical medium (e.g. copper/fiber cables) | Transmission rate, bit/block encoding, multiplexing | Ethernet, DSL, ISDN, 802.11 | Hubs, Repeaters | Bits

---

# Encapsulation

**PDU (Protocol Data Unit)**
- The information at which a specified layer in the OSI model communicates with
- The top three layers of the OSI only deal with data
- The bottom for layers deal with different PDU types
  - Each layer encapsulates or decapsulates the previous PDU

**Encapsulation / Decapsulation**
- Encapsulation – when data is sent
  - Data --> segment --> packet --> frame --> bits --> sent over physical medium
  - Every time a PDU is encapsulated, a new header is added to it
- Decapsulation – when data is received
  - Received over physical medium --> Bits --> frame --> segment --> data
  - Every time a PDU is decapsulated, the previous header is removed


