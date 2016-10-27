# Automated VMware ESX and ESXi Guest VM creation 
## about
When superceeding the 3-tier-localhost (Web/App/Database on same Linux) architecture, you suddently have quite a lot Hosts to manage, and it'd be nice to have automated creation possibilities at the Machine level like creating n-webservers. 

This scripts allowes very basic operations of Guest-VMs on a ESX(i) Host (5.5?) like creating or deleting Virtual Machine Guests. See --help for more information.

## requirements
Python(2.7isch) and PySphere (pip install pysphere) 

Note: Windows / Python 2.7.xxx.msi installations: pip.exe is in C:\Python27\Scripts

## examples
```
# list avalable datastores and networks and guests on physical host 192.168.1.2
pySimpleVmCtrl.py -H 192.168.1.2 -U root -P password -A list-host -A list-guest

# create a guest called test-01
pySimpleVmCtrl.py -H 192.168.1.2 -U root -P password -A create -g test-01 \
       --disk 40 --store "[SomeDataStore]" --cpu 2 --mem 4096 --net LAN	

# power on guest test-01
pySimpleVmCtrl.py -v -H 192.168.1.2 7 -U root -P password -g test-01 -A on 
```

## fun
```
host_cred="-H 192.168.122.232 -U root -P password"

for i in `seq 1 8`; do
    python pySimpleVmCtrl.py ${host_cred} -A del -g test-${i} 2> /dev/null
    python pySimpleVmCtrl.py -v ${host_cred} -A create -g test-${i} \
       --disk ${i}  --cpu ${i} --mem $((${i} * 16))
done
```

## serious
```
net1="VM Network"
ds1="[datastore1]"
hprefix=xyz
action="-A create"

python pySimpleVmCtrl.py -g ${hprefix}-stage 	--mem 4096 	--cpu 2 --disk 24 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred} 
python pySimpleVmCtrl.py -g ${hprefix}-file 	--mem 4096 	--cpu 2 --disk 96 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hprefix}-db 	--mem 8192 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}

python pySimpleVmCtrl.py -g ${hprefix}-web-01 	--mem 4096 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hprefix}-proxy-01 --mem 1024 	--cpu 1 --disk 4 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hprefix}-web-01 	--mem 4096 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hprefix}-cf-01 	--mem 4096 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
```
## dangerous
```
# BIG FAT WARNING: THIS WILL JUST DELETE/WIPE/EMPTY YOUR HOST!!! ALL GUESTS WILL BE GONE!!!
# any you probabely shouldn't do things this way anyway!

# create ListOfVirtualMachines (lovm) - get list of all Guests on the very host
lovm=`python pySimpleVmCtrl.py ${host_cred} -A list-guest | awk '{if(NR>1)print $1}'`

# print them out again
echo "@@@@@@@@@@@@@@ WILL REMOVE THE FOLLOWING GUESTS/VMS @@@@@@@@@@@@@@"
echo ${lovm}
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

# loop and remove
for vm in ${lovm}; do
	echo "---------------------- REMOVING GUEST '${vm}'  ----------------------"
	python pySimpleVmCtrl.py ${host_cred} -A del -g ${vm}
done
```
