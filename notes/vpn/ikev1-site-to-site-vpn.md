# Title: Site-to-Site VPN - IKEv1

Phase 1:
- Policy
- Authenticaiton

Phase 2
- Transform-set
- ACL
- Crypto Map

IKEv1 Phase 1 Policy (must match on both peers)
- Encryption : DES, 3DES, AES (128, 192, 256)
- Hash : MD5, SHA-1, SHA-2 (256, 384, 512)
- Diffie-Hellman Group : 1, 2, 5, 14, 15, 16 or ECDH* 19, 20 and 24
- Authentication Method : Pre-Shared Key, Digital Certificates (RSA or ECDSA*)
- Lifetime : does not have to be the same

```
crypto isakmp policy [#]
  authentication [if applicable]
  encryption [algorithm]
  hash [algorithm]
  group [DH-group-number]
  lifetime [seconds]
```
Authenticaiton Credentials
```
crypto isakmp key
crypto pki trustopint
```

Quick Negotiation elements
- PFS (Perfect Forward Secrecy) (optional)
	- Enables an additional DH exchange to dervie a fresh set of symmetric keys for phase 2 tunnel
	- Encryption an dHashing functions 
	- Proxy Identities (traffic to be protected (ACL)


```
! - Transform-set
crypto ipsec transform-set name [esp-3des|esp-md5-hmac ...]
mode [transport|tunnel]

! - ACL
access-list.....

Group Policy configuration
group-policy pname [internal|external]
group-policy pname attributes

Tunnel Group configuration
tunnel-group tname type [ipsec-l2l|remote-access]
tunnel-group tname general-attributes
default-group-policy pname
tunnel-group tname ipsec-attributes



! - Crypto Map
crypto map [crypto-map-name] [map-seq-nr] ipsec-isakmp
crypto map [crypto-map-name] set peer [peer-address]
crypto map [crypto-map-name] set ikev1 transform-set [name]
crypto map [crypto-map-name] mathc addresss [access-list]
crypto map [crypto-map-name] set trustpoint
crypto map [crypto-map-name] interface
crypto okev1 enable  


--------------------------------------

IKEv1 Site-to-Site VPN on IOS

ASA has two mandatory componnets
- Tunnel Group and Group Policy
-  Tunnel group can be thought of as "Connection Profile"


How ASA selects a Tunnel Group
Authentication with Digital Certificates
1. Certificate OU field
2. IKE identifier of the VPN (IKE_ID)
3. VPN peer's IP address
4. If no match found, a pre-configured "Default RAGroup" will be selected


**Authentication iwth Pre-Shared Keys**
5. Aggressive Mode: IKE_ID (if present) or VPN peer’s IP address
6.  Main Mode : VPN peer’s IP address
7. If nothing was matched and VPN is L2L, a pre-configured „DefaultL2LGroup” is a go

