#!/bin/bash

# add -f to run ssh in background, parallellize
SSH="ssh -o StrictHostKeyChecking=no"

# update these entries to match your username and allocated resources!
RTR1="jaikumar@pc1.instageni.iu.edu -p 26612"
NODE11="jaikumar@pc1.instageni.iu.edu -p 26610"
NODE12="jaikumar@pc1.instageni.iu.edu -p 26611"

RTR2="jaikumar@pc2.instageni.nps.edu -p 26012"
NODE21="jaikumar@pc2.instageni.nps.edu -p 26010"
NODE22="jaikumar@pc2.instageni.nps.edu -p 26011"

RTR3="jaikumar@pc603.emulab.net -p 29644"
NODE31="jaikumar@pc603.emulab.net -p 29642"
NODE32="jaikumar@pc603.emulab.net -p 29643"

ALL_NODES=("$RTR1" "$RTR2" "$RTR3"
	   "$NODE11" "$NODE12"
	   "$NODE21" "$NODE22"
	   "$NODE31" "$NODE32")

RTRS=("$RTR1" "$RTR2" "$RTR3")

HOSTS=("$NODE11" "$NODE12"
       "$NODE21" "$NODE22"
       "$NODE31" "$NODE32")

# Run commands below
# For example, this clears all IPs from dataplane interfaces
# and resets /etc/hosts

# NOTE: build a map of which ethX interfaces connect to each other
# before flushing!

# e.g.
# rtr1:eth3 < 10.10.100.1 - 10.10.100.3 > rtr3:eth4
# rtr1:eth4 < 10.10.101.1 - 10.10.101.2 > rtr2:eth3
# rtr2:eth4 < 10.10.102.2 - 10.10.102.3 > rtr3:eth3
for h in "${RTRS[@]}"; do
    $SSH $h "hostname; sudo ip addr flush dev eth1; \
    	    	       sudo ip addr flush dev eth2; \
		       sudo ip addr flush dev eth3; \
		       sudo ip addr flush dev eth4; \
		       head -n 1 /etc/hosts | sudo tee /etc/hosts ;\
		       echo "10.10.0.1 router1" | sudo  tee -a /etc/hosts ;\
		       echo "10.10.101.2 router2" | sudo  tee -a /etc/hosts ;\
		       echo "10.10.100.3 router3" | sudo tee -a /etc/hosts ;\
		       echo "10.10.0.11 node11" | sudo tee -a /etc/hosts ;\
		       echo "10.10.0.12 node12" | sudo tee -a /etc/hosts ;\
		       echo "10.10.1.21 node21" | sudo tee -a /etc/hosts ;\
		       echo "10.10.1.22 node22" | sudo tee -a /etc/hosts ;\
		       echo "192.168.0.31 node31" | sudo tee -a /etc/hosts ;\
		       echo "192.168.0.32 node32" | sudo tee -a /etc/hosts ;"
done

for h in "${HOSTS[@]}"; do
    $SSH $h "hostname; sudo ip addr flush dev eth1; \
    	     head -n 1 /etc/hosts | sudo tee /etc/hosts ;\
	     echo "10.10.0.1 router1" | sudo  tee -a /etc/hosts ;\
	     echo "10.10.101.2 router2" | sudo  tee -a /etc/hosts ;\
	     echo "10.10.100.3 router3" | sudo tee -a /etc/hosts ;\
	echo "10.10.0.11 node11" | sudo tee -a /etc/hosts ;\
	echo "10.10.0.12 node12" | sudo tee -a /etc/hosts ;\
	echo "10.10.1.21 node21" | sudo tee -a /etc/hosts ;\
	echo "10.10.1.22 node22" | sudo tee -a /etc/hosts ;\
	echo "192.168.0.31 node31" | sudo tee -a /etc/hosts ;\
	echo "192.168.0.32 node32" | sudo tee -a /etc/hosts ;"
done

# Next step: assign desired IPs to each site hosts and routers
# Update /etc/hosts if desired

$SSH $NODE11 "hostname; sudo ip addr add 10.10.0.11/24 dev eth1"
$SSH $NODE12 "hostname; sudo ip addr add 10.10.0.12/24 dev eth1"

$SSH $NODE21 "hostname; sudo ip addr add 10.10.1.21/24 dev eth1"
$SSH $NODE22 "hostname; sudo ip addr add 10.10.1.22/24 dev eth1"

$SSH $NODE31 "hostname; sudo ip addr add 192.168.0.31/24 dev eth1"
$SSH $NODE32 "hostname; sudo ip addr add 192.168.0.32/24 dev eth1"

$SSH $RTR1 "hostname; sudo ip addr add 10.10.0.1/24 dev eth1; \
		      sudo ip addr add 10.10.100.1/24 dev eth3; \
		      sudo ip addr add 10.10.101.1/24 dev eth4;"

$SSH $RTR2 "hostname; sudo ip addr add 10.10.1.1/24 dev eth1; \
		      sudo ip addr add 10.10.101.2/24 dev eth3; \
		      sudo ip addr add 10.10.102.2/24 dev eth4;"

$SSH $RTR3 "hostname; sudo ip addr add 192.168.0.1/24 dev eth1; \
		      sudo ip addr add 10.10.102.3/24 dev eth3; \
		      sudo ip addr add 10.10.100.3/24 dev eth4;"

# Adding static routes on the routers router1, router2, router3 and hosts 

echo "Static IP addition"
echo "r1"
$SSH $RTR1 "hostname; sudo ip route add 10.10.102.2 via 10.10.101.2; \
		      sudo ip route add 10.10.102.3 via 10.10.100.3; \
                      sudo ip route add 10.10.1.0/24 via 10.10.100.3; \
		      sudo ip route delete 10.10.101.0/24 ; \
		      sudo ip route add 10.10.101.0/24 via 10.10.100.3;"
echo "r2"
$SSH $RTR2 "hostname; sudo ip route add 10.10.0.0/16 via 10.10.101.1;"

echo "r3"
$SSH $RTR3 "hostname; sudo ip route add 10.10.0.0/24 via 10.10.100.1; \
                      sudo ip route add 10.10.1.0/24 via 10.10.102.2; \
                      sudo ip route add 10.10.101.0/24 via 10.10.102.2;"

echo "node11"
$SSH $NODE11 "hostname; sudo ip route add 10.10.0.0/16 via 10.10.0.1; \
                        sudo ip route add 10.10.1.0/24 via 10.10.0.1;"

echo "node21"
$SSH $NODE21 "hostname; sudo ip route add 10.10.0.0/16 via 10.10.1.1;"

echo "node31"
$SSH $NODE31 "hostname; sudo ip route add 10.10.0.0/24 via 192.168.0.1; \
                        sudo ip route add 10.10.1.0/24 via 192.168.0.1;"

# END #

