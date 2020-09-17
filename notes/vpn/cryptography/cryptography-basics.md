
  
# Title: Cryptography Basics

## Table of Contents

- Encryption (Confidentiality)
- Hashing (Integrity)
- Digital Signatures (Authentication)

---

# Encryption (Confidentiality)

## Overview

- Encryption keeps data confidential.
- Prevents any device other than the receiver from reading the data
- Encrypted data is "unreadable" by those who can decrypt it

**Comparison Table**
--- | Symmetric encryption | Asymmetric encryption
--- | --- | ---
Keys | Shared key | Public/private keys
Speed | Faster | Slower
Number of Keys | Grows exponentially as users grow | Grows linearly as users grow
Use | Bulk encryption, files and data transfer | Used smaller transactions; e.g. authenticating and establishing a secure communication channel prior to the actual data transfer
Security Services Provided | Confidentiality | Confidentiality, authentication, non-repudiation| 
Protocols | RC4, DES, 3DES, AES | RSA, DH, ECC

## Symmetric encryption
- The same shared key is used for data encryption and decryption.
- The sender and the receiver both have a copy of the same shared key.
- Easy to compromise.
- Symmetric encryption provides low security but is processed quickly, good for encrypting a lot of data.
- It’s mostly used when large chunks of data need to be transferred.
- Algorithms:
  - DES - 56 bit key
  - 3DES - 168 bit key
  - AES - 128, 192 and 256 bit keys

## Asymmetric encryption
- Uses a "private key" and a "public key".
- The public key can be shared with anyone, the private key is kept a secret.
- Either key can be used for encryption or decryption.
- Whichever key was used for encryption, only the other key is capable of decryption.
- It’s used in smaller transactions, primarily to authenticate and establish a secure communication channel prior to the actual data transfer.
- Often used for authentication purposes
- Algorithms:
  - RSA - 512, 768, 1024, 2048, 4096 bits
  - DSA (similar to RSA)
  - DH – group 1, 2, 5, 14, 15
  - EC (newest alternative to RSA, DSA and DH)
  
----

# Hashing (Integrity)

## Overview
- Used to verify that received data is intact in its original form.
- One-way only, cannot be reversed

## Algorithms
 
**Standard algorithms:**
- MD5 - produces 128-bit hashes
- SHA-1 - produces 160-bit hashes
- SHA-2 produces 256, 384, 512-bit hashes

**HMAC**
- Includes a shared key when calculating hash
- Provides data integrity and authentication
- Algorithms: 
  - HMAC-MD5
  - HMAC-SHA1
 
----

# Digital Signatures (Authentication)

- When asymmetric cryptography is used for authentication, Digital Signatures provides additional authentication and integrity of a message
- Used to secure Digital Certificates
- Relies on Asymmetric Key Pair and Hashing

1. Sender calculates hash of the original packet
2. The calculated hash gets encrypted with the Private Key
3. Original packet is sent to recipient with encrypted hash attached with it
4. Receiver uses Public Key to decrypt the encrypted hash value
5. Receiver now has:
   - a) The original packet
   - b) The decrypted hash value
6. Receiver calculates its own hash value on the original data
7. Receiver compares its own calculated hash to the received decrypted hash value
8. If the two hashes match, it is confiremd that the packet maintains integrity

- **Note**: One flaw with asymmetric encryption is that the recipient must know which Public Key (if it has multiple keys stored) corresponds to the sender's Private Key.

