#!/usr/bin/env python
# -*- coding: utf-8 -*-

# requires: pysphere    (pip install pysphere)
# todo: replace with pyVmMon instead of pyshpere ...

import argparse
import logging
logger = logging.getLogger()

from pySimpleVmCtrl.ESXiGuest import *

############################

program_description = '''  Simple script to create/delete/list VMware ESXi (5.5) guests

examples:
# list available datastores and networks and guests on ESXi host 192.168.1.2
python ./pySimpleVmCtrl.py -H 192.168.1.2 -U root -P password -A list-host -A list-guest

# create a guest called test-01
python ./pySimpleVmCtrl.py -H 192.168.1.2 -U root -P password -A create \
    --disk 40 --store "[MainDS]" --cpu 2 --mem 4096 --net LAN -g test-01

# power on guest test-01
python ./pySimpleVmCtrl.py -v -H 192.168.1.2 -U root -P password -A on -g test-01

Note:
    -A  can be specified multiple times to run several operations on the same VM
        (e.g.  -A off -A del -A create -A on)

Warn:
    MULTIPLE GVMs/Guests can be created using the SAME name!!!
    Use '-A create' carefully, if you specify a already existing guest, a new, same-named
    guest will be created despite the original one, and you'll eventually confuse yourself!

Arguments:
'''

parser = argparse.ArgumentParser(description=program_description, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-v', action='store_true', default=False,
                    dest='verbosity',
                    help='be verbose [%(default)s]')

parser.add_argument('-H', action='store', default='localhost',
                    dest='host',
                    help='hostname esxi server [%(default)s]')

parser.add_argument('-U', action='store', default='root',
                    dest='user',
                    help='username to connect to esx [%(default)s]')

parser.add_argument('-P', action='store',
                    dest='passwd',
                    help='password [read from stdin]')

parser.add_argument('-A', action='append', dest='action',
                    help="what to do [list-host|list-guest|off|on|reboot|del|create]",
                    )

parser.add_argument('-g', action='store',
                    dest='guest',
                    help='Guest virtual machine name')

parser.add_argument('--store', action='store', default=None,
                    dest='datastore',
                    help='(create) datastore to use')

parser.add_argument('--net', action='store', default=None,
                    dest='network',
                    help='(create) network to connect to')

parser.add_argument('--disk', action='store', default=8,
                    dest='disksize',
                    help='(create) disksize in GB')

parser.add_argument('--cpu', action='store', default="1",
                    dest='cpu',
                    help='(create) cpu count [%(default)s]')

parser.add_argument('--mem', action='store', default="1024",
                    dest='memory',
                    help='(create) memory in MB [%(default)s]')

parser.add_argument('--os', action='store', default="rhel6_64Guest",
                    dest='operatingsystem',
                    help='(create) Operating system [%(default)s]')

parser.add_help

def execute_arguments(esx_host, action, args ):
    logger.debug('%s:execute_arguments(%s, %s, %s)',__name__, 'ESXiHostClass', action, args.guest)
    if action == "list-host": ###############################################
        print "--- available datastores ---"
        for each in esx_host.get_datastores():
            print "[" + each + "]"
        print "--- available networks ---"
        for each in esx_host.get_networks():
            print "'" + each + "'"
        return True

    elif action == "list-guest": #####################################################
        print "--- available guests ---"
        for each in esx_host.get_guests():
            each_guest = ESXiGuestClass(esx_host, each)
            power, net = each_guest.get_status()
            print each, ' ', power, ' ', net     # todo: nice output
        return True

    if args.guest is None:
        logger.critical('%s:execute_arguments(): either illegal action or specify guest name', __name__)
        return False


    # check for guest
    guest = ESXiGuestClass(esx_host, args.guest)
    # if guest.vm is None:
    #     logger.critical("%s:execute_arguments(): skipping guest '%s'", __name__, guest_name)
    #     return False

    assert isinstance(guest, ESXiGuestClass)

    if action == "off": ###############################################
        return guest.power_off()
    if action == "on": ###############################################
        return guest.power_on()
    if action in [ "reset", "reboot" ]: #######################
        return guest.reboot()

    if action in [ "add", "create" ]:
        #return guest.create_me(cpu = argparser.cpu, mem = argparser.memory, os = argparser.operatingsystem,
        #                       datastore = '"' + argparser.datastore + '"', network = argparser.network, diskGB = argparser.disksize)
        return guest.create_me( cpu = int(argparser.cpu), mem = int(argparser.memory), os = argparser.operatingsystem,
                                 datastore = argparser.datastore, network = argparser.network, diskGB = int(argparser.disksize))


    if action in [ "rem", "del" ]:
        guest.power_off()
        return guest.remove_me()

    if action in [ "bios"]:
        return guest.set_enter_bios()

    # else:
    #     logger.error('%s:unknown action %s', __name__, action)



if __name__ == "__main__":      # here we actually go and run
    argparser = parser.parse_args()

    if argparser.action is None:
        parser.print_help()
        quit(2)

    if argparser.verbosity:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)

    logger.debug('%s:argparser.verbosity  =  %s', __name__, str(argparser.verbosity))
    logger.debug('%s:argparser.host       =  %s', __name__, str(argparser.host))
    logger.debug('%s:argparser.user       =  %s', __name__, str(argparser.user))
    passwd = argparser.passwd
    # if not passwd:
    #     import getpass
    #     passwd = getpass.getpass()
    # logger.debug('%s:argparser.passwd     =  %s', __name__, str(passwd))
    logger.debug('%s:argparser.action     =  %s', __name__, str(argparser.action))
    logger.debug('%s:argparser.guest      =  %s', __name__, str(argparser.guest))
    logger.debug('%s:argparser.datastore      =  %s', __name__, str(argparser.datastore))

    #### here we go
    esx_host = ESXiHostClass(argparser.host, argparser.user, passwd)

    def exec_n_report(action, args):  # nasty little function to std-out stuff
        ret = execute_arguments(esx_host, action, args)
        #print "run: '" + each_action + "' agains guest '" + str(args.guest) + "': " + str(ret)
        return ret

    for each_action in argparser.action:
        exec_n_report(each_action, argparser)
