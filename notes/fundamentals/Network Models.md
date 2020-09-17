# Network Models

**Objective**
- Know and understand how network communication is divided into layers based on the services that each layer provides
- Conceptually categorize and group different aspects of network communication

**Solution**
- The OSI Model and TCP/IP Stack Model both provide standardized frameworks for understanding how data is communicated over a network

**How it Works**
- Each layer of the network reference model explains what services are offered, which protocols are implemented, and how data is sent

**Troubleshooting**
- Understanding how data is sent over a network helps narrowing down the probable cause of an issue to a specific layer. You can then begin troubleshooting from there.

**Network Model**
- A framework designed to help understand the process of network communication
- Also helps with troubleshooting
	- TCP/IP Model
	- OSI Model

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