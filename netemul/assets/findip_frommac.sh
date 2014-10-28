#!/bin/bash
mac=$1
sudo arp -an | grep $mac | awk '{print $2}' > /home/sampath/gitrepos/django/netemul/assets/foundip_frommac.txt

