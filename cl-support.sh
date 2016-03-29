#!/bin/bash

LOCATION=/tmp/cl-support.log
SERVER=192.168.207.254

echo "sudo cl-support > $LOCATION"

FILENAME=`cat /tmp/cl-support.log | awk '{print $3}'`

scp $FILENAME $SERVER: