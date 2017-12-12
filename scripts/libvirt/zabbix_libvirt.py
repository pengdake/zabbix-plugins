#!/usr/bin/env /usr/bin/python

import libvirt
import argparse
import time
import json
from xml.etree import ElementTree

DOMAIN_STATES = ["nostate",
                 "running",
                 "blocked",
                 "paused",
                 "shutdown",
                 "shutoff",
                 "crashed",
                 "pmsuspended"]


def get_node_info(conn, tag):
    node_info_list = conn.getInfo()
    if tag == "memory":
        return node_info_list[1]
    elif tag == "frequency":
        return node_info_list[3]
    elif tag == "cpus":
        return node_info_list[2]
    elif tag == "cores":
        return node_info_list[6]
    elif tag == "threads":
        return node_info_list[7]


def get_domain_list(conn):
    domain_list = []
    domains = conn.listAllDomains()
    for domain in domains:
        domain_list.append({"{#DOMAIN_NAME}": domain.name()})
    return json.dumps({"data": domain_list}, indent=4)


def get_domain_info(conn, name, tag):
    domain_obj = conn.lookupByName(name)
    domain_info = domain_obj.info()
    if tag == "state":
        domain_state = domain_info[0]
        return DOMAIN_STATES[domain_state]
    elif tag == "max_mem":
        return domain_info[1]
    elif tag == "mem_used":
        return domain_info[2]
    elif tag == "cpu_num":
        return domain_info[3]
    elif tag == "cpu_used":
        time_1 = domain_info[4]
        sleep_time = 1
        time.sleep(sleep_time)
        time_2 = domain_obj.info()[4]
        cpu_cores = get_node_info(conn, "cores")
        return round(100 * (time_2 - time_1)/(sleep_time * cpu_cores * 1e9), 2)


def get_domain_xml(domain_obj):
    return ElementTree.fromstring(domain_obj.XMLDesc())


def get_domain_iface_info(conn, name, tag):
    domain_obj = conn.lookupByName(name)
    domain_tree = get_domain_xml(domain_obj)
    ifaces = domain_tree.findall('devices/interface/target')
    total = 0
    for iface in ifaces:
        iface_str = iface.get('dev')
        iface_info = domain_obj.interfaceStats(iface_str)
        if tag == "incoming_byte":
            total += iface_info[0]
        elif tag == "outgoing_byte":
            total += iface_info[4]
    return total


def domain_info(args):
    conn = libvirt.openReadOnly("qemu+ssh://root@10.10.10.111/system")
    if args.list:
        domains = get_domain_list(conn)
        print domains
    elif args.name:
        if args.state:
            tag = "state"
            domain_state = get_domain_info(conn, args.name, tag)
            print domain_state
        elif args.memory_used:
            tag = "mem_used"
            domain_mem_used = get_domain_info(conn, args.name, tag)
            print domain_mem_used
        elif args.max_memory:
            tag = "max_mem"
            domain_max_mem = get_domain_info(conn, args.name, tag)
            print domain_max_mem
        elif args.cpu_num:
            tag = "cpu_num"
            domain_cpu_num = get_domain_info(conn, args.name, tag)
            print domain_cpu_num
        elif args.cpu_used:
            tag = "cpu_used"
            domain_cpu = get_domain_info(conn, args.name, tag)
            print domain_cpu
        elif args.incoming_byte:
            tag = "incoming_byte"
            domain_incoming = get_domain_iface_info(conn, args.name, tag)
            print domain_incoming
        elif args.outgoing_byte:
            tag = "outgoing_byte"
            domain_outgoing = get_domain_iface_info(conn, args.name, tag)
            print domain_outgoing


def hypervisor_info(args):
    conn = libvirt.openReadOnly("qemu+ssh://root@10.10.10.111/system")
    if args.memory:
        tag = "memory"
        hypervisor_mem = get_node_info(conn, tag)
        print hypervisor_mem
    elif args.cores:
        tag = "cores"
        hypervisor_cores = get_node_info(conn, tag)
        print hypervisor_cores
    elif args.cpus:
        tag = "cpus"
        hypervisor_cpus = get_node_info(conn, tag)
        print hypervisor_cpus
    elif args.threads:
        tag = "threads"
        hypervisor_threads = get_node_info(conn, tag)
        print hypervisor_threads
    elif args.frequency:
        tag = "frequency"
        hypervisor_frequency = get_node_info(conn, tag)
        print hypervisor_frequency


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # add domain subcmd
    parser_domain = subparsers.add_parser('domain',
                                          help="info about domain")
    parser_domain.add_argument("-l", "--list",
                               action="store_true",
                               help="list all domains")
    parser_domain.add_argument("-n",
                               "--name",
                               help="domain name")
    parser_domain.add_argument("-s", "--state",
                               action="store_true",
                               help="the domain state")
    parser_domain.add_argument("-mu",
                               "--memory_used",
                               action="store_true",
                               help="the domain memory used")
    parser_domain.add_argument("-mm",
                               "--max_memory",
                               action="store_true",
                               help="the domain used memory")
    parser_domain.add_argument("-cu",
                               "--cpu_used",
                               action="store_true",
                               help="the domain cpu used")
    parser_domain.add_argument("-cn",
                               "--cpu_num",
                               action="store_true",
                               help="cpu number of the domain used")
    parser_domain.add_argument("-rb",
                               "--incoming_byte",
                               action="store_true",
                               help="the network incoming bytes")
    parser_domain.add_argument("-tb",
                               "--outgoing_byte",
                               action="store_true",
                               help="the network outgoing bytes")
    parser_domain.set_defaults(func=domain_info)
    # add hypervisor subcomd
    parser_hypervisor = subparsers.add_parser('hypervisor',
                                              help="info about hypervisor")
    parser_hypervisor.add_argument("-m",
                                   "--memory",
                                   action="store_true",
                                   help="total memory")
    parser_hypervisor.add_argument("-c",
                                   "--cores",
                                   action="store_true",
                                   help="total cpu cores")
    parser_hypervisor.add_argument("-t",
                                   "--threads",
                                   action="store_true",
                                   help="threads of one cpu core")
    parser_hypervisor.add_argument("-s",
                                   "--cpus",
                                   action="store_true",
                                   help="sum of cpu threads")
    parser_hypervisor.add_argument("-hz",
                                   "--frequency",
                                   action="store_true",
                                   help="cpu frequency")
    parser_hypervisor.set_defaults(func=hypervisor_info)
    args = parser.parse_args()
    args.func(args)
