Things To Be Done
=================

Most Priority (The project is incomplete without them)
------------------------------------------------------
* Documentation of the code.
* Clear commenting and removal of useless code.
* Most important:
      Add try catch to show what are the exceptions.

      In some places I have given address of the files as "/home/sampath/gitrepos/django/netemul/assets/........". This has to be changed to relative addressing.

* Remove the error in the graphs page (graphs load after pressing F12)
* Display of the database results in table.
* Make a minor feature change to give same parameters while simulation to different PCs.
* Display of live data(numbers) using Ajax-polling.

Improvements in the GUI to be done
----------------------------------
* The main testing page surely needs improvement in GUI.
* If possible try to implement Django-SocketIO(but only after basics are completed).



Errors in the code or where the code will surely not work
=========================================================

* The following are the places where the password has to be entered in the terminal.
  * Whenever the NMAP command is used password has to be entered.
    * Scanning of PCS
      When we scan the PCs in a subnet, to get the MAC addresses we need to run the command in sudo. So one has to enter the password
    * Addition of PCs without scanning:
      When a PC is added without scanning, the nmap command is executed as root to get the MAC address. We need MAC address because at the time of Update PC we will need it. We are not having this problem when we add by scanning because we already know MAC address.(That scanning obviously needs nmap as root, as explained in previous point).
    * Update of IP:
      Again at the time of IP update, we have to run nmap as root.

  * Apart from Nmap command TC command needs root permissions.
    * While manipulating with tc qdisc commands one should be root user.
    * Actually for presentation and demo purposes I have commented the code:
        subprocess.call("assets/pre_test.sh")
      This bash scripts prepares for the simulation of multiple PCs. There were also issues with server stability, so I changed this bash script.
      Actually this script includes the code:
        sudo sysctl net.ipv4.ip_forward=1   //to make ip forward = 1  
        sudo tc qdisc del dev eth0 root     // to delete the qdiscs of the previous simulation 
      There were other commands which were not required(I guess), but these were used in TCSWanem. Our code works without using them also, but I will figure out why the other commands are used in TCSWanem
      These extra commands were(not fully sure):
        sudo sysctl net.ipv4.send_redirects.all = 0
        sudo sysctl net.ipv4.send_redirects.eth0 = 0
* Solution:
    * I think once the changes are made to pre_test.sh and the tc command and nmap command are made to run without password everything will be fine


Proposed order of Bug Fixing:
=============================
* Documentation of the code.
* Clear commenting and removal of useless code.
* Most important:
  * Add try catch to show what are the exceptions.
  * In some places I have given address of the files as "/home/sampath/gitrepos/django/netemul/assets/........". This has to be changed to relative addressing.


PS: I will keep updating this file as I find more errors and bugs. :D And I will keep updating which bugs are solved and pushed to gitblit
------------------------------------------------------------------------------------------------------------------------------------------
