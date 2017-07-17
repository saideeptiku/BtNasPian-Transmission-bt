# BtNasPian: Transmission-bt

This is a program that automates Transmission daemon setup. 
The daemon is stopped if VPN is not working.
Will add option for setup without VPN as well. Only works with PPTP based VPN.

This program is intended to be one out of a three part solution that combines:
* NAS
* Transmission Bit Torrent (Web-Interface Daemon)
* VPN

## Instructions:

Transmission settings can be modified in the transmission-autorun-setup.py file.
Make sure your IP is whitelisted. After this , execute the following command to install:

```
sudo chmod +X bt_util.sh
sudo sh bt_util.sh install_and_setup_transmission_daemon
```

To remove:
```
sudo sh bt_util.sh remove_transmission
```
