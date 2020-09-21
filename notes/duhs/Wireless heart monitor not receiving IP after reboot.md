# Symptoms:
A wireless medical device (heart monitor called  EKG/ECG) would sometimes fail to get on the network after a reboot. 
When the device is rebooted, there was a 50% chance that it would receive an IP address.

# Analysis:
In Cisco Prime, there were some alerts generated for that device's MAC address.

**Alerts:**
```
IDS 'Broadcast Probe flood' Signature attack detected on AP 'dpc-leesville-1-prep-145b' protocol '802.11a' on Controller '10.98.2.22'. The Signature description is 'Broadcast Probe Request flood', with precedence '7'. The attacker's mac address is '84:25:3f:69:7e:40', channel number is '116', and the number of detections is '500'. - Device Name: nc1-41p-wlc-8540-1 - Reporting Address: 10.98.2.22
WLAN Controller nc1-41p-wlc-8540-1/10.98.2.22
10.98.2.22
 IDS 'Broadcast Probe flood' Signature attack detected on AP 'dpc-leesville-1-prep-145b' protocol '802.11a' on Controller '10.98.2.22'. The Signature description is 'Broadcast Probe Request flood', with precedence '7'. The attacker's mac address is '84:25:3f:69:7e:40', channel number is '165', and the number of detections is '500'. - Device Name: nc1-41p-wlc-8540-1 - Reporting Address: 10.98.2.22
WLAN Controller nc1-41p-wlc-8540-1/10.98.2.22
10.98.2.22
 IDS 'Broadcast Probe flood' Signature attack detected on AP 'dpc-leesville-1-breakroom' protocol '802.11a' on Controller '10.98.2.22'. The Signature description is 'Broadcast Probe Request flood', with precedence '7'. The attacker's mac address is '84:25:3f:69:7e:40', channel number is '36', and the number of detections is '500'. - Device Name: nc1-41p-wlc-8540-1 - Reporting Address: 10.98.2.22
WLAN Controller nc1-41p-wlc-8540-1/10.98.2.22
10.98.2.22
 IDS 'Broadcast Probe flood' Signature attack detected on AP 'dpc-leesville-1-lab-107' protocol '802.11a' on Controller '10.98.2.22'. The Signature description is 'Broadcast Probe Request flood', with precedence '7'. The attacker's mac address is '84:25:3f:69:7e:40', channel number is '161', and the number of detections is '500'. - Device Name: nc1-41p-wlc-8540-1 - Reporting Address: 10.98.2.22
WLAN Controller nc1-41p-wlc-8540-1/10.98.2.22
10.98.2.22
```

# Troubleshooting
- Created case with Cisco
- Did debug on controller while the client was rebooting `debug client [mac-address]`
- Stop debug with `debug disable-all` and sent output to Cisco
