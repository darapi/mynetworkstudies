
# Encapsulation


**Encapsulation**
- Outgoing traffic starts as data & moves down network reference model
- Encapsulation: Data &rarr; Segments &rarr; Packets &rarr; Frames &rarr; Bits
- At each layer, a header is added during the encapsulation process

**Decapsulation**
- Incoming traffic is received as bits, and moves up network reference model
- Decapsulation: Bits &rarr; Frames &rarr; Packets &rarr; Segments &rarr; Data
- At each layer, a header is removed during the decapsulation process

**PDU (Protocol Data Unit)**
- The information at which a specified layer in the OSI model communicates with
- The top three layers of the OSI only deal with data
- The bottom for layers deal with different PDU types
  - Each layer encapsulates or decapsulates the previous PDU

**Encapsulation / Decapsulation**
- Encapsulation – when data is sent
  - Data &rarr; segment &rarr; packet &rarr; frame &rarr; bits &rarr; sent over physical medium
  - Every time a PDU is encapsulated, a new header is added to it
- Decapsulation – when data is received
  - Received over physical medium &rarr; Bits &rarr; frame &rarr; segment &rarr; data
  - Every time a PDU is decapsulated, the previous header is removed