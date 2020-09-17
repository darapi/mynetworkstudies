**Encryption Algorithms:**
- Symmetric: DES (56-bit), 3DES (168-bit), AES (128, 192, 256-bit)
- Assymetric: RSA (512, 768, 1024, 2048, 4096-bits), DSA (512, 768, 1024, 2048, 4096-bits), DH (Group 1, 2, 5, 14, 15) 
- Assymetric Elliptic-Curve (EC) : newest alternative to RSA, DSA and DH

**Hashing Algorithms:**
- MD5 (128-bit)
- HA-1 (160-bit)
- SHA-2 (256, 384, 512)
- HMAC (Hashed Message Authentication Code) HMAC-MD5 and HMAC-SHA1 Includes a shared key when calculating a hash

**HMAC** 
- Includes shared key when calculating hash for additional security
- HMAC-MD5 and HMAC-SHA1

ISAKMP
- Framework desciribng core IPsec functions
- specifies that keyind and authenticaiton should occur
- describes the precedures to establish, negotiate, modify and delte tunnel info

IKDE
- An implmentation of ISAKMP
- Available in two versions IKEv1 and IKEv2

PHase 1
- Performed in two modes Main Mode (6 packets) and Aggressive Mode (3 packets)
- Succesful negotiateion results in a ISAKMP/IKE Security Association (SA)
- IKE Policy
  - Encryption: DES, 3DES, AES
  - Hash: MD5, SHA-1, SHA-2
  - DH: 1, 2, 5, 14, 15, 16 or ECDH 18, 20, 24
  - Authenticaiton Method: PSK or Digital Certificate (RSA, ECDSA)
  - Lifetime (does not have to match, all parameters above need to match)

Phase 2
- Performed only in Quick Mode
- Results in IPSec SA (Security Association)

Both ISAKMP phases are negotiated over UPD port 500 by default






# Site-to-Site VPN (IKEv2)

## IKEv1 vs. IKEv2

## Prequisites
- Internal interface is on the inside zone
- External interface is on the outside zone
- Can ping the peer to which VPN will be established with
- Establish tunnel between two peers

ASA

```
ASA1(config)# crypto ikev2 policy [10]
ASA1(config-ikev2-policy)# encryption [aes]
ASA1(config-ikev2-policy)# group [2]
ASA1(config-ikev2-policy)# prf [sha]
ASA1(config-ikev2-policy)# lifetime seconds 86400

(config)# crypto ipsec ikev2 ipsec-proposal [MY_PROPOSAL]
(config-ipsec-proposal)# protocol esp encryption [aes]
(config-ipsec-proposal)# protocol esp integrity [sha-1]

ASA1(config)# crypto map [MY_CRYPTO_MAP] [1] match address [LAN1_LAN2]
ASA1(config)# crypto map [MY_CRYPTO_MAP] [1] set peer [10.10.10.2]
ASA1(config)# crypto map [MY_CRYPTO_MAP] [1] set ikev2 ipsec-proposal [MY_PROPOSAL]
ASA1(config)# crypto map [MY_CRYPTO_MAP] interface outside


ASA1(config)# tunnel-group [10.10.10.2] type ipsec-l2l
ASA1(config)# tunnel-group [10.10.10.2] ipsec-attributes 
ASA1(config-tunnel-ipsec)# ikev2 local-authentication pre-shared-key [password]
ASA1(config-tunnel-ipsec)# ikev2 remote-authentication pre-shared-key [password]

ASA1(config)# crypto ikev2 enable outside

ASA1(config)# access-list [LAN1_LAN2] extended permit ip host [192.168.1.1] host [192.168.2.2]

ASA1(config)# route OUTSIDE 192.168.2.0 255.255.255.0 10.10.10.2

ASA1# show crypto isakmp sa
ASA1# show crypto ipsec sa
```



ESP (Encapsulating  Security Payload) is protocol 50



IOS

```
crypto isakmp policy 10
 encr 3des
 authentication pre-share
 group 2
crypto isakmp key cisco123 address 192.168.11.2

crypto ipsec transform-set newset esp-3des esp-md5-hmac

crypto map map1 5 ipsec-isakmp
 set peer 192.168.11.2
 set transform-set newset
 match address VPN_BO1
 
 interface Serial2/0
 ip address 192.168.10.10 255.255.255.0
 ip nat outside
 ip virtual-reassembly
 clock rate 64000
 crypto map map1
 
 ip nat inside source route-map nonat interface Serial2/0 overload
!
ip access-list extended NAT_Exempt
 deny ip 10.10.10.0 0.0.0.255 172.16.1.0 0.0.0.255
 permit ip 10.10.10.0 0.0.0.255 any
ip access-list extended VPN_BO1
 permit ip 10.10.10.0 0.0.0.255 172.16.1.0 0.0.0.255
!
route-map nonat permit 10
 match ip address NAT_Exempt
 
 
 
 
 
 
 
 
 
 
crypto isakmp policy 10
  authentication pre-share
  encryption aes
  hash md5
  group 2
  exit

crypto isakmp key test123 address peer_address

access-list - interesting traffic

crypto ipsec transform-set NAME esp-aes esp-sha
  mode tunnel 
  exit
  
crypto map MAP SEQ ipsec-isakmp
  set peer PEER_ADDRESS
  set transform-set SET_NAME
  match address ACCESS-LIST
  exit
  

 
 
