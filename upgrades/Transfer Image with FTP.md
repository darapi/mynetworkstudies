# Transfer Image with FTP

## Overview

1. Setup FTP server
2. Copy image to root directory
3. Configure FTP credentials on network device
4. Transfer the image file
5. Verify MD5 hash value

---

### 1. Setup FTP server

Download FileZilla Server for Windows ([click here](https://filezilla-project.org/download.php?type=server))

Setup username, password and directory:

```
Edit --> User
Add new user
Checkmark "Enable account" and "Password"
Enter a password
Go to "Shared folders" tab and select root directory
Make path to root directory: C:\FTP-Root
```

---

### 2. Copy the image file to the root directory.

Download the cisco image from the Cisco Software Download page ([click here](https://software.cisco.com/download/home))

Copy the image to the FTP root directory, at C:\FTP-Root

---

### 3. Configure FTP credentials on network device

```
configure terminal
ip ftp username [uname]
ip ftp password [passwd]
end
```

---

### 4. Transfer the image file

```
copy ftp: flash:
[ip_address]
[file_name]
```

---

### 5. Verify MD5 hash value


The expected MD5 hash value can be found on the Cisco Software Download page

```
end
#verify /md5 flash:[file_name] [expected_md5_hash_value]
```

---

- Author: Daniel Arapi
- Last Update: 07/13/21
