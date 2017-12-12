#!/bin/bash

cd "$(dirname "$0")"

./zabbix_libvirt.py domain -l
