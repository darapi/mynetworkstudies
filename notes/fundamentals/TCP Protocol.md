
**TCP (Transmission Control Protocol)**
- Connection oriented, reliable protocol
- Retransmits segments that are dropped, not received or containing errors
- Provides sequencing of segments, so that they are put in order when received
- Features: Three-Way Handshake, Sliding Window, PAR, and Buffering

**TCP Three-Way Handshake**
- Process of initiated a connection between a client and server
- Device_1 sends SYN to Device_2
  - SYN – A number associated with a segment
- Device_2 replies with SYN + ACK
  - ACK – One number greater than SYN, serves as confirmation
- Device_1 responds with ACK

**PAR (Positive Acknowledge with Retransmission)**
- Each segment has a sequence number + timer starts
- For each segment, recipient replies with ACK (ACK = SYN + 1)
- If ACK is not received, segment is retransmitted once timeout occurs

**TCP Sliding Window**
- Controls rate/speed of segment transfer
- Exponentially increases number of segments sent at a time
- Groups of segments can be confirmed by a single ACK
- If ACK not received, window size is decreased
