#!/bin/bash
ip=$1
echo "hi all"
sudo nmap -sP -n $ip | awk '/MAC Address:/ {print $3}' > /home/sampath/gitrepos/django/netemul/assets/found_mac.txt

