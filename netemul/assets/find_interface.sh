#!/bin/bash
ifconfig -s -a|grep -v Iface|grep -v lo|cut -d " " -f1 > assets/interfaces.txt
echo 3
