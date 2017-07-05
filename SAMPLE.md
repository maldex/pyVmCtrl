## fun
```
host_cred="-H 192.168.122.21 -U root -P password"

for i in `seq 1 8`; do
    python pySimpleVmCtrl.py ${host_cred} -A del -g test-${i} 2> /dev/null
    python pySimpleVmCtrl.py -v ${host_cred} -A create -g test-${i} \
       --disk ${i}  --cpu ${i} --mem $((${i} * 16))
done
```

## serious
```
net1="LAN"
ds1="[1GbSlowStore]"
hpre=dev
action="-A create"

python pySimpleVmCtrl.py -g ${hpre}-stage 	--mem 4096 	--cpu 2 --disk 24 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred} 
python pySimpleVmCtrl.py -g ${hpre}-file 	--mem 4096 	--cpu 2 --disk 96 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hpre}-db   	--mem 8192 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}

hpst=01
python pySimpleVmCtrl.py -g ${hpre}-proxy-${hpst} 	--mem 1024 	--cpu 1 --disk 4 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hpre}-php-${hpst} 	--mem 4096 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
python pySimpleVmCtrl.py -g ${hpre}-cf-${hpst} 		--mem 4096 	--cpu 2 --disk 8 	--store "${ds1}" --net "${net1}"  ${action}  ${host_cred}
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
