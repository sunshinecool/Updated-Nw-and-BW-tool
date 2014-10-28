#!/bin/bash
sudo echo 1 > /proc/sys/net/ipv4/ip_forward

sudo tc qdisc del dev eth0 root

sudo tc qdisc add dev eth0 handle 1: root htb

sudo tc class add dev eth0 parent 1: classid 1:1 htb rate 100Mbps
