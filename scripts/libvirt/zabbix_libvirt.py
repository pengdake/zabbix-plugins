#!/usr/bin/env python

import libvirt
import argparse

def get_domain_list(conn):
    return [domain.name() for domain in conn.listAllDomains()]

def get_domain(conn, name):
    return conn.lookupByName(name)

def get_domain_state(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    import pdb;pdb.set_trace()
    return domain_obj.info()[0]

def get_domain_memory_used(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    return domain_obj.info()[2]

def get_domain_cpu_num(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    return domain_obj.info()[3]
    
def get_domain_cpu_used(conn, domain_name):
    domain_obj = get_domain(conn, domain_name)
    return domain_obj.info()[4]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # add domain subcmd
    parser_domain = subparsers.add_parser('domain',  help="info about domain")
    parser_domain.add_argument("-l", "--list", action="store_true", help="list all domains")
    parser_domain.add_argument("-n", "--name", help="domain name")
    parser_domain.add_argument("-s", "--state", action="store_true", help="the domain state")
    parser_domain.add_argument("-um", "--usememory", action="store_true", help="the domain used memory")
    parser_domain.add_argument("-uc", "--usecpu", action="store_true", help="the domain cpu used")
    parser_domain.add_argument("-cn", "--cpunum", action="store_true", help="cpu number of the domain used")
    # add hypervisor subcomd
    parser_hypervisor = subparsers.add_parser('hypervisor', help="info about hypervisor")
    parser_hypervisor.add_argument("-l", "--list")
    
    conn = libvirt.openReadOnly(None)
    args = parser.parse_args()
    if args.list:
        domains = get_domain_list(conn)
    elif args.name:
        if args.state:
            domain_state = get_domain_state(conn, args.name)
        elif args.usememory:
            domain_memory = get_domain_memory_used(conn, args.name)
        elif args.cpunum:
            domain_cpu_num = get_domain_cpu_num(conn, args.name)
        elif args.usecpu:
            domain_cpu = get_domain_cpu_used(conn, args.name)
                



