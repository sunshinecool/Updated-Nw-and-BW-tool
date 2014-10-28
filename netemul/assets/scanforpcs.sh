#!/bin/bash
startip=$1
endip=$2
sudo nmap -sn -n $1-$2| awk '{if(FNR>2){ if(FNR%3==0) {if($1=="Nmap" && $2=="done:") {} else print $5;} else if(FNR%3==2) print $3;}}'> assets/ip_mac.txt
echo 0
echo "scanforpcs running"
