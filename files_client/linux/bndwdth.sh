#!/bin/bash
mydate=$(date +%Y-%m-%d' '%H:%M:%S)
echo ","$mydate >date.csv
#hostname>source.csv
 src=$(hostname)
 echo $src>source.csv
ServerIp=10.129.200.200
HostIp=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*)
echo $HostIp>Hostip.csv
tshark -i eth0 -a duration:1 host $ServerIp -w CapFileTest.pcap
tshark -r CapFileTest.pcap -T fields -e ip.src -e frame.len -E separator=, -E occurrence=f > CapFileTestSrc.csv
tshark -r CapFileTest.pcap -T fields -e frame.len -E separator=, -E occurrence=f > length.csv
sed -n "/$ServerIp/!p" CapFileTestSrc.csv> CapFileTestClient.csv

echo `cat CapFileTestClient.csv | cut -d ','  -f 2 | paste -sd+| bc`/`cat CapFileTestClient.csv|wc -l` | bc > AvgPacketSize.csv

awk 'END {print NR}' CapFileTestClient.csv > TotalClientPacket.csv
awk '{avgPckt=$1/1} {print avgPckt}' TotalClientPacket.csv > AvgPacketSec.csv


cat AvgPacketSize.csv|awk '{n=$1;getline<"AvgPacketSec.csv";print (n*$1/1024)*8}'>BwdthKbps.csv
# Merging the Upload files 
 paste -d ',' TotalClientPacket.csv AvgPacketSec.csv AvgPacketSize.csv BwdthKbps.csv >ClientUp.csv
# For Download Bandwidth    

    #mkdir ../ClientDownLoadTest
    cp CapFileTestSrc.csv CapFileTestDwn.csv
    #cd ../ClientDownLoadTest
    sed -n "/$HostIp/!p" CapFileTestDwn.csv>CapFileTestClientDwn.csv 
    echo `cat CapFileTestClientDwn.csv | cut -d ','  -f 2 | paste -sd+| bc`/`cat CapFileTestClientDwn.csv|wc -l` | bc>AvgPacketSizeDwn.csv

    awk 'END {print NR}' CapFileTestClientDwn.csv >TotalClientPacketDwn.csv
    awk '{avgPckt=$1/1} {print avgPckt}' TotalClientPacketDwn.csv>AvgPacketSecDwn.csv
    cat AvgPacketSizeDwn.csv|awk '{n=$1;getline<"AvgPacketSecDwn.csv";print (n*$1/1024)*8}'>BwdthKbpsDwn.csv
#merging different csv files

        paste -d ',' TotalClientPacketDwn.csv AvgPacketSecDwn.csv AvgPacketSizeDwn.csv BwdthKbpsDwn.csv >ClientDwn.csv
# Merging csv to obtain the final result
    paste -d ',' date.csv source.csv Hostip.csv ClientUp.csv ClientDwn.csv >TestAnalysis.csv
# upload the data on mysql using python script

#TotalCapPacket=`cat TotalClientPacket.csv`
TotalCapPacket=$(wc -l<length.csv)


## To start the hostname with , 
echo ","$src >source.csv
paste -d ',' source.csv>Percentage.csv
#echo ","$Hostip>Hostip.csv
paste -d ',' Hostip.csv>>Percentage.csv
#
##### Client Packet Percentage
#
#### Copy the second column entry from CapFileTestClient which contain the packet size of upload
awk -F ',' '{print $2 }' CapFileTestClient.csv >length.csv
#
awk '{ if ($1 >= 40 && $1 <= 79) print $1 }' length.csv>40-79.csv
total=$(wc -l<40-79.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
#
awk '{ if ($1 >= 80 && $1 <= 159) print $1 }' length.csv>80-159.csv
total=$(wc -l<80-159.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
#
awk '{ if ($1 >= 160 && $1 <= 319) print $1 }' length.csv>160-319.csv
total=$(wc -l<160-319.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
#
awk '{ if ($1 >= 320 && $1 <= 639) print $1 }' length.csv>320-639.csv
total=$(wc -l<320-639.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
#
awk '{ if ($1 >= 640 && $1 <= 1279) print $1 }' length.csv>640-1279.csv
total=$(wc -l<640-1279.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
#
awk '{ if ($1 >= 1280 && $1 <= 2559) print $1 }' length.csv>1280-2559.csv
total=$(wc -l<1280-2559.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
#
awk '{ if ($1 >= 2560 && $1 <= 5119) print $1 }' length.csv>2560-5119.csv
total=$(wc -l<2560-5119.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>Percentage.csv
### Convert the column entries if the Percentage.csv in row entries pecentage.csv
paste -s -d ',' Percentage.csv>Pecentage.csv
#
#
#### Server Packet Percentage
#
echo ","$src >source.csv
paste -d ',' source.csv>PercentageDwn.csv
#echo ","$Hostip>Hostip.csv
paste -d ',' Hostip.csv>>PercentageDwn.csv


awk -F ',' '{print $2 }' CapFileTestClientDwn.csv >lengthDwn.csv

awk '{ if ($1 >= 40 && $1 <= 79) print $1 }' lengthDwn.csv>40-79Dwn.csv
total=$(wc -l<40-79Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
#
awk '{ if ($1 >= 80 && $1 <= 159) print $1 }' lengthDwn.csv>80-159Dwn.csv
total=$(wc -l<80-159Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
#
awk '{ if ($1 >= 160 && $1 <= 319) print $1 }' lengthDwn.csv>160-319Dwn.csv
total=$(wc -l<160-319Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
#
awk '{ if ($1 >= 320 && $1 <= 639) print $1 }' lengthDwn.csv>320-639Dwn.csv
total=$(wc -l<320-639Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
#
awk '{ if ($1 >= 640 && $1 <= 1279) print $1 }' lengthDwn.csv>640-1279Dwn.csv
total=$(wc -l<640-1279Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
#
awk '{ if ($1 >= 1280 && $1 <= 2559) print $1 }' lengthDwn.csv>1280-2559Dwn.csv
total=$(wc -l<1280-2559Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
#
awk '{ if ($1 >= 2560 && $1 <= 5119) print $1 }' lengthDwn.csv>2560-5119Dwn.csv
total=$(wc -l<2560-5119Dwn.csv)
echo "scale=4;($total / $TotalCapPacket) * 100"|bc -l>>PercentageDwn.csv
### Convert the column entries if the Percentage.csv in row entries pecentage.csv
paste -s -d ',' PercentageDwn.csv>PecentageDwn.csv
#
