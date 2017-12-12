#!/bin/bash

cd "$(dirname "$0")"
ITEM="-"${1}

./zabbix_libvirt.py hypervisor $ITEM
