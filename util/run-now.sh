#!/bin/bash

for file in ../approved/*france.py ; do
 echo doing $file
 python $file
 sleep 60
 echo done $file
done
