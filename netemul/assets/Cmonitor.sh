#!/bin/bash

##  Tests directory to create file related to that test
cd assets/Tests
#cd Tests
## Server IP
echo $(pwd)
server=192.168.121.7

## To enter IP in file which is readed by tshark to conduct the monitoring

#echo " Enter number of machine to conduct the test"
#read n
#
#for ((i=0; i<n; i++))
#do
#	read -p "Enter IP " ip
#    echo $ip
#	echo $ip >> 1.txt
#done
#
## Array to genrate the IP string which is pass to the tshark 

 iptxt='1.txt'
 i=0
 hosts='host '
 ors='or '





	for each in $@; do
		ips[i]=$hosts
		ips[i+1]=$each
		ips[i+2]=$ors
		i=$(($i+3))
        echo ${ips[0]}
	done
				
	wordcount=$(echo ${ips[@]} | wc -c)
						
	wordcountless2=$(($wordcount-3))
					
	para=$(echo ${ips[@]} | cut -c -$wordcountless2)
	echo $para
	#return 


#echo "Duration of Test in Seconds"
#read dur
dur=1

#mkdir testof-$(date +%d%H%M)

#cd testof-$(date +%d%H%M)

tshark -i eth0 -a duration:$dur $para -w PacketCap.pcap

i=0
	for each in $@; do
		ip[i]=$each
		tshark -Y "ip.src == ${ip[i]} && ip.dst == $server" -r PacketCap.pcap >ClientUp$i-.csv
		sed -i '/TCP Dup/d' ClientUp$i-.csv
		sed -i '/TCP Retransmission/d' ClientUp$i-.csv


		tshark -Y "ip.dst == ${ip[i]} && ip.src == $server" -r PacketCap.pcap >ClientDown$i-.csv
		sed -i '/TCP Dup/d' ClientDown$i-.csv
		sed -i '/TCP Retransmission/d' ClientDown$i-.csv

## Total Packet Calculation for Upload and Download

		awk 'END {print NR}' ClientUp$i-.csv>TotalClientUpPacket$i-.csv 
		awk 'END {print NR}' ClientDown$i-.csv>TotalClientDownPacket$i-.csv 
		echo `cat TotalClientUpPacket$i-.csv`
		echo `cat TotalClientDownPacket$i-.csv`

## Average packet per second transmited

		awk '{avgPckt=$1/'$dur'} {print avgPckt}' TotalClientUpPacket$i-.csv>AvrgUpPacket$i-.csv
		awk '{avgPckt=$1/'$dur'} {print avgPckt}' TotalClientDownPacket$i-.csv>AvrgDownPacket$i-.csv

## Average packet size Upload and Download 

		awk '{sum+=$7}  END { print "" sum/NR} ' ClientUp$i-.csv>AvrgUpSize$i-.csv 
		sed -i '/^$/d' AvrgUpSize$i-.csv
		awk '{sum+=$7}  END { print "" sum/NR} ' ClientDown$i-.csv>AvrgDownSize$i-.csv 
		sed -i '/^$/d' AvrgDownSize$i-.csv

## Upload Bandwidth Calculation 
		paste AvrgUpPacket$i-.csv AvrgUpSize$i-.csv| awk '{print ($1 * $1)}'> BandwdthUp$i-.csv

		paste -d ',' AvrgUpPacket$i-.csv AvrgUpSize$i-.csv TotalClientUpPacket$i-.csv BandwdthUp$i-.csv>CaptureUp$i-Data.csv


## Download Bandwidth Calculation 
		paste AvrgDownPacket$i-.csv AvrgDownSize$i-.csv| awk '{print ($1 * $1)}'> BandwdthDown$i-.csv

		paste -d ',' AvrgDownPacket$i-.csv AvrgDownSize$i-.csv TotalClientDownPacket$i-.csv BandwdthDown$i-.csv>CaptureDown$i-Data.csv
		
		i=$(expr $i + 1)
		
	done
 
rm -rf Avrg* Total*
cd ..

