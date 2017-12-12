#!/bin/bash

cd "$(dirname "$0")"
NAME=$1
ITEM="-"${2}

./zabbix_libvirt.py domain -n $NAME $ITEM
