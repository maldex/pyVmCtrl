# Automated VMware ESX and ESXi Guest VM creation 
## about

This scripts allowes very basic operations of Guest-VMs on a ESXi like creating or deleting Virtual Machine Guests thorugh a simple shell-command. It exposes a simplfied interface to python's [pysphere](https://pypi.python.org/pypi/pysphere) module. 

So far tested and working against ESXi 5.1, 5.5 and 6.5. With vCenter, you still need to target the actual host, not the vcenter.

## requirements
Python(2.7isch) and PySphere (```pip install pysphere```) 

Note: Windows / Python 2.7.xxx.msi installations: pip.exe is in C:\Python27\Scripts

## --help
[some more samples](SAMPLE.md)
```$ python ./pySimpleVmCtrl.py --help
usage: pySimpleVmCtrl.py [-h] [-v] [-H HOST] [-U USER] [-P PASSWD] [-A ACTION]
                         [-g GUEST] [--store DATASTORE] [--net NETWORK]
                         [--disk DISKSIZE] [--cpu CPU] [--mem MEMORY]
                         [--os OPERATINGSYSTEM]

  Simple script to create/delete/list VMware ESXi guests

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
        (e.g.  -A off -A del -A create -A on :)

Warn:
    Use '-A create' carefully, if you specify a already existing guest, a new, same-named
    guest will be created despite the original one, and you'll eventually confuse yourself!
    # todo: test which vm will be deleted if two same-named vm exist?

Arguments:

optional arguments:
  -h, --help            show this help message and exit
  -v                    be verbose [False]
  -H HOST               hostname esxi server [localhost]
  -U USER               username to connect to esx [root]
  -P PASSWD             password [read from stdin]
  -A ACTION             what to do [list-host|list-guest|off|on|reboot|del|create]
  -g GUEST              Guest virtual machine name
  --store DATASTORE     (create) datastore to use
  --net NETWORK         (create) network to connect to
  --disk DISKSIZE       (create) disksize in GB [8]
  --cpu CPU             (create) cpu count [1]
  --mem MEMORY          (create) memory in MB [1024]
  --os OPERATINGSYSTEM  (create) Operating system [rhel6_64Guest]
```
