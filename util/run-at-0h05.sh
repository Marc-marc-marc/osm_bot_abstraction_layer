#!/bin/bash

while [ $(date +%H) -ge 1 ] ; do echo waiting for midnight ; sleep 300 || break ; done
while [ $(date +%M) -lt 5 ] ; do echo waiting for the 5th minutte or more ; sleep 60 || break ; done
./run.sh
