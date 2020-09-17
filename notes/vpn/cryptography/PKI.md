# PKI (Public Key Infrastructure)

- CA (Certificate Authority)
- Digital Certificates
- Certificate Revocation Server

# Digital Certificates
- Electronic files used to prove an identity
- Can be used to authenticate HTTPS, IPsec VPN, SSL VPN, 802.1x session, etc.

## X.509 Certificate Structure
- Serial Number
- Issuer Name
- Subject Name and Subject Name's Public Key
- Digital Signature
- Expiration Dates and CRL

# CA (Certificate Authority)
- Issues, maintains and revokes Digital Certificates
- Commercial CA - have an established reputation, paid, salable
- Internal CA - limited scope, free, requires maintenance

**Certificate Enrollment**
- The proccess of joining to a PKI
- Pre-requisistes: NTP synced, Key Pair generation
  - `crypto key generate rsa`

**Cerificate Revocation**
- Process of checking if a certificate is sitll in a PKI
- Optional or can be disabled
- CRL (Certificate Revocation List) or OSCP (Oline Certificate Status Protocol)
- CRL in file contains serial numbers of revoked certificates
- This file is downloaded periodicaly and cached

**Digital Certificate Authentication Process**
- Certificate validation
  - Siganture check
  - Expiration Check
  - Revocation Check (Optional)
- Assymetric encryption/decryption (after certifcate is validated)


PKI relis on a single trust relationship with a CA
- Trusted the CA implies trusting to all certificates issued by the CIA


