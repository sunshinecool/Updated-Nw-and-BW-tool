#!/bin/bash
LATENCY=$1
LOSS=$2
BW=$3
sudo /sbin/tc qdisc del dev eth0 root
echo "1"
sudo /sbin/tc qdisc add dev eth0 root handle 1: netem delay $LATENCY 
echo "2"
sudo /sbin/tc qdisc add dev eth0 parent 1:1 handle 10: netem loss $LOSS
echo "3"
sudo /sbin/tc qdisc add dev eth0 parent 10:1 handle 20: htb default 1
echo "4"
sudo /sbin/tc class add dev eth0 parent 20: classid 20:1 htb rate $BW ceil $BW
echo "Simulation success"
echo
echo "check by pinging from the host computers"


#tc qdisc add dev eth0 parent 1:12 handle 20: netem loss 20% delay 100ms