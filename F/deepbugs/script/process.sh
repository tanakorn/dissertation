#!/bin/bash

systemname=$(basename $1)
cat $1 | sort -k 2 -n | awk -v systemname=$systemname 'BEGIN {print "\"Bug Id\" \"Short Id\" \"#Crash\" \"#Reboot\""} {printf "%s-%d %d %d %d\n", systemname, $2, $2, $4, $5}' > ../dat/$systemname.dat

