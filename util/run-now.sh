#!/bin/bash

for file in ../git/approved/*france.py ; do
 clear
 echo doing $file
 python $file
 echo done $file
 echo ------------------------------------------------------
 sleep 60
done
