#!/usr/bin/env python

import libvirt
import argparse
import time


def get_node_memory(conn):
    return conn.getInfo()[1]


def get_node_frequency(conn):
    return conn.getInfo()[3]


def get_node_cpus(conn):
    return conn.getInfo()[2]


def get_node_cores(conn):
    return conn.getInfo()[6]


def get_node_threads(conn):
    return conn.getInfo()[7]


def get_domain_list(conn):
    return [domain.name() for domain in conn.listAllDomains()]


def get_domain(conn, name):
    return conn.lookupByName(name)


def get_domain_state(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    domain_state = domain_obj.info()[0]
    domain_state_list = ["nostate",
                         "running",
                         "blocked",
                         "paused",
                         "shutdown",
                         "shutoff",
                         "crashed",
                         "pmsuspended"]
    return domain_state_list[domain_state]


def get_domain_memory_used(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    return domain_obj.info()[2]


def get_domain_cpu_num(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    return domain_obj.info()[3]


def get_domain_cpu_used(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    sleep_time = 1
    time_1 = domain_obj.info()[4]
    time.sleep(sleep_time)
    time_2 = domain_obj.info()[4]
    cpu_cores = get_node_cores(conn)
    return round(100 * (time_2 - time_1)/(sleep_time * cpu_cores * 1e9), 2)

def domain_info(args):
    conn = libvirt.openReadOnly(None)
    if args.list:
        domains = get_domain_list(conn)
        print domains
    elif args.name:
        if args.state:
            domain_state = get_domain_state(conn, args.name)
            print domain_state
        elif args.usememory:
            domain_memory = get_domain_memory_used(conn, args.name)
            print domain_memory
        elif args.cpunum:
            domain_cpu_num = get_domain_cpu_num(conn, args.name)
            print domain_cpu_num
        elif args.usecpu:
            domain_cpu = get_domain_cpu_used(conn, args.name)
            print domain_cpu


def hypervisor_info(args):
    conn = libvirt.openReadOnly(None)
    if args.memory:
        hypervisor_mem = get_node_memory(conn)
        print hypervisor_mem
    elif args.cores:
        hypervisor_cores = get_node_cores(conn)
        print hypervisor_cores
    elif args.cpus:
        hypervisor_cpus = get_node_cpus(conn)
        print hypervisor_cpus
    elif args.threads:
        hypervisor_threads = get_node_threads(conn)
        print hypervisor_threads
    elif args.frequency:
        hypervisor_frequency = get_node_frequency(conn)
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
    parser_domain.add_argument("-um",
                               "--usememory",
                               action="store_true",
                               help="the domain used memory")
    parser_domain.add_argument("-uc",
                               "--usecpu",
                               action="store_true",
                               help="the domain cpu used")
    parser_domain.add_argument("-cn",
                               "--cpunum",
                               action="store_true",
                               help="cpu number of the domain used")
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
