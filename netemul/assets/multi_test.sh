
#!/bin/bash
x=$1
delay=$2
ipsrc=$3
BW=$4
loss=$5
z=10
y=$(($x*$z))
f=$(($y+2))
g=$(($f+2))
echo $y
echo $f 
echo $g
sudo tc class add dev eth0 parent 1:1 classid 1:$x htb rate 100mbps
sudo tc qdisc add dev eth0 parent 1:$x handle $y: netem delay $delay 
sudo tc qdisc add dev eth0 parent $y:1 handle $g: netem loss $loss
echo 3
sudo tc qdisc add dev eth0 parent $g:1 handle $f: htb default 1
sudo tc class add dev eth0 parent $f: classid $f:1 htb rate $BW ceil $BW
sudo tc filter add dev eth0 protocol ip prio 1 u32 match ip src $ipsrc flowid 1:$x
