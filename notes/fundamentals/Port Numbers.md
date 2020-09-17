# List Order
Port | Protocol | Description
--- | --- | ---
TCP: 1 | ARP | (Address Resolution Protocol) Used to discover MAC address via IP address.
TCP: 20/21 | FTP | (File Transfer Protocol) 20 – Establishes session; 21 – Authentication & file transfer
TCP: 22 | SSH | (Secure Shell) Secure connect to remote devices
TCP: 23 | TELNET | (Telnet) Unsecure connection to remote device
TCP: 25 | smtp | (Simple Mail Transfer Protocol) Used for sending e-mails
TCP: 49 | TACACS+ | Provides authentication/authorization/accounting
TCP/UDP: 53 | DNS | (Domain Name System) TCP – Zone Transfer (servers); UDP – Domain to IP queries
TCP: 69 | TFTP | (Trivial FTP) Transfers file to/from remote host, no authentication
UDP: 67/68 | DHCP | (Dynamic Host Configuration Protocol) Provides IP addresses to network devices for client
TCP: 80 | http | (Hypertext Transfer Protocol) Retrieves contents from web server
TCP: 110 | POP3 | (Post Office Protocol version 3) Downloads e-mail to client, deletes from server
UDP: 123 | NTP | (Network Time Protocol) Synchronizes network device clocks with NTP server
TCP: 143 | IMAP4 | (Internet Message Access protocol version 4) Retrieves (copy of) e-mail form server
TCP: 389 | LDAP | (Lightweight Directory Access Protocol) Access to directories, usernames, passwords, e-mail
TCP: 443 | HTTPS | (HTTP Secure) HTTP over SSL/TLS
TCP: 161 / UDP: 162 | SNMPv3 | (Simple Network Management Protocol) Used to monitor/manage switches/routers from SNMP server. TCP 161 for polling; UDP 162 for notifications.
TCP: 989 / 990 | FTPS | (FTP Secure) FTP over SSL/TLS
UDP: 1645/1812 | RADIUS | Provides authentication/authorization/accounting
TCP: 3389 | RDP | (Remote Desktop Protocol) Provides remote control over Win desktop

---

# Grouped by Category

Ports | Purpose
--- | ---
Web | HTTP, HTTPS
Mail | SMTP, POP3, IMAPv4
AAA | TACACS, RADIUS
Remote | SSH, TELNET
File Transfer | FTP, TFTP, SFTP, FTPS
Management | NTP, LDAP, SNMPv3
Connectivity | ARP, ICMP