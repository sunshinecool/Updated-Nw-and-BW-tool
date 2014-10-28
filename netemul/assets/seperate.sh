
tc qdisc del dev eth0 root
tc qdisc add dev eth0 handle 1: root htb

tc class add dev eth0 parent 1: classid 1:1 htb rate 1000Mbps
tc class add dev eth0 parent 1:1 classid 1:11 htb rate 100Mbps
tc class add dev eth0 parent 1:1 classid 1:12 htb rate 100Mbps
tc class add dev eth0 parent 1:1 classid 1:13 htb rate 100Mbps

tc qdisc add dev eth0 parent 1:11 handle 10: netem delay 500ms
tc qdisc add dev eth0 parent 1:12 handle 20: netem delay 200ms
tc qdisc add dev eth0 parent 1:13 handle 30: netem delay 300ms

tc filter add dev eth0 protocol ip prio 1 u32 match ip src 10.105.15.34 flowid 1:11
tc filter add dev eth0 protocol ip prio 1 u32 match ip dst 192.168.1.2 flowid 1:12
tc filter add dev eth0 protocol ip prio 1 u32 match ip dst 192.168.1.2 flowid 1:13

echo 1