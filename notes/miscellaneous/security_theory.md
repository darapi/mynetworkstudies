

## AAA

- Authentication - verifies user identity
- Authorization - determines user privileges
- Accounting - audit user behavior

### RADIUS
- Open standard
- Any AAA vendor for ACS/client
- UDP 1812 (authentication) and 1813 (accounting)
- Authentication and Authorization is combined in RADIUS
- Encrypts only password
- Preferrably used with ISE
- Best for network access (who joined the network, how did they authenticate, how long were they on, did they on-board, what types of endpoints are on the network)


### TACACS+
- Cisco proprietary
- Used for communication between Cisco ACS and client
- TCP: 49
- Authentication, Authorization and Accounting is separated
- Encrypts entire packet
- Preferrably used with ACS
- Used for device administration (who entered which command and when)


### ISE
- Combines NAC and ACS
- Profiling and posture services
- Policy Definition
- Control
- Reporting
- Appliance
  - Hardware: 3315, 3355, 3395
  - VMware

## Port Security

### 802.1X
- Used to block or unblock an interface
- Uses EAPoL between Authenticator and client
- Uses EAP between RADIUS and Authenticator


