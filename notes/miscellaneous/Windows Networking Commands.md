Command  | Description
--- | ---
`systeminfo` | Computer info
`ipconfig /all` | Display all network configs
`ipconfig /release` | Release current IP address
`ipconfig / renew` | Renew IP address
`ipconfig /flushdns` | Flush DNS cache
`ipconfig /all \| find /I "address"` | Filter ipconfig output to show only IP and MAC addresses
`hostname` | Hostname of PC
`getmac` | Lists MAC addresses
`arp -a` | Address resolution cache
`netstat` | Active TCP/UDP ports
`command /?` | help menu
`tracert [destination]` | Traceroute to destination
`pathping [destination]` | Network latency and network loss at intermediate hops between a source and destination
`netsh wlan show all` |  Shows complete wireless device and networks information
`netsh wlan show drivers` | Shows properties of the wireless LAN drivers on the system.
`netsh wlan show interfaces` | Shows a list of the wireless LAN interfaces on system
`netsh wlan show networks` | Shows a list of networks visible on the system.
`netsh wlan show profiles` | Shows a list of profiles configured on the system.
`netsh wlan show wirelesscapabilities` | Shows the wireless capabilities of the system
`netsh wlan show wlanreport` | Generate a report showing recent wireless session information
`netsh interface show interface` | Show connected interfaces
`F11` | Toggle Full-Screen mode
`ping.exe -t HOSTNAME\|Foreach{"{0} - {1}" -f (Get-Date),$_}` | Ping with timestamp via powershell
`Test-Connection -Count 9999 -ComputerName HOSTNAME \| Format-Table @{Name='TimeStamp';Expression={Get-Date}},Address,ProtocolAddress,ResponseTime` | ping with timestamp via powershell
`psping [ip_address]:22` | test if a port is open on a remote device, must be installed
`Test-NetConnection -Port [port-number] -ComputerName [hostname]` | Powershell, test open port on remote device.



Check out this link later

https://docs.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection?view=win10-ps
