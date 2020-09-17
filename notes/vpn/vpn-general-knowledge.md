# Title: VPN (Virtual Private Network)

What is a VPN?
- A secure encrypted tunnel established between two endpoints
- Secure tunnel is established across the public Internet (unsecured)
- Remote devices is provided access to the internal network through this tunnel

Types of VPN:
- Remote Access VPN
- Site-to-Site VPN 

Remote Access VPN
- A VPN connecting an end device (PC or laptop) to the company's network
- e.g. User laptop needs access to company's network when working remotely
- Requires software to be installed, e.g. Cisco AnyConnect

Site-to-Site VPN
- Also known as: L2L or LAN-to-LAN

IPsec
- Consists of multiple protocols and standards
- ISAKMP - framework describing core IPsec functions to 
	- Describes procedures to establish, negotiation and modified and delete tunnel info
	- Specify that keying and authentication should occur 
- IKE - implmenetion of ISAKMP
	- Performs main Control Plane functions like keying exchange, authenticaiton, etc.
	- Two versions: IKEv1 and IKEv2
- 
- Authentication
- Data Confidentiality
- Data Integrity 
- Replay Protection

Other IPsec framework components
- Control Plane
-Key Management : DH, ECDH
- Authentication : PSK, RSA, ECDSA
- Data Plane
- Security Protocols : ESP, AH
- Confidentiality : DES, 3DES, AES, SEAL
- Data Integrity and Origin Authentication : MD5, SHA-1, SHA-2     


"ISAKMP makes the rules, IKE plays the game"
UDP Port: 500

VPN Phases
- Phase 1
	- Main Mode (MM)
	- Aggressive Mode (AM)
- Phase 2
	- Quick Mode (QM)


Phase 1 SA, ISAKMP SA, IKE SA
- used to protect the second negotiation (phase 2)

Phase 2 SA / Tunnels
- One for inboud
- second for outbound

