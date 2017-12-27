#!/bin/bash
# -*- coding: utf-8 -*-
#
# @author: alex.tang <feng.tang@gmail.com>
# Created on 2017/06/28
# only for HP server
function get_install_ip(){
#get master ip address
        preip=$(/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|grep -v "0.0.0.0"|awk '{print $2}'|tr -d "addr:"|head -1)
        echo $preip
}

function ipmiinfo(){
#ipmitool get ipmiip and other info

        #if [ ! -f "/usr/bin/ipmitool" ]
        #then
                #yum install ipmitool -y > /dev/null 2>&1
        #fi
        #sleep 10
        #if [ -f "/usr/bin/ipmitool" ]
        #then
            modprobe ipmi_watchdog
            modprobe ipmi_poweroff
            modprobe ipmi_devintf
            modprobe ipmi_si
            modprobe ipmi_msghandler
      ipmiip=$(/usr/bin/ipmitool -I open lan print | grep "IP Address" |grep -v "IP Address Source"|awk -F : {'print $NF'})
        #else
        #        ipmiip="noipmi"
        #fi
  echo $ipmiip
}

function get_mac_addr(){
# get mac for eth0
        eth0_mac=$(/sbin/ifconfig -a | grep eth0 | awk '{print $5}')
        echo $eth0_mac
}

function get_server_id(){
# get the sn of the server
        server_id=$(/usr/sbin/dmidecode |grep "Serial Number"|sed -n '1p' |awk -F: '{print $NF}'|sed 's/[][ ]*//g')
        eth0_mac=$(/sbin/ifconfig -a | grep eth0 | awk '{print $5}')
        if [ -z "$serialno" ]
        then
            server_id=$(echo "$eth0_mac" |md5sum )
        fi
        echo $server_id
}


function get_serial_no(){
# get the sn of the server
        serialno=$(/usr/sbin/dmidecode |grep "Serial Number"|sed -n '1p' |awk -F: '{print $NF}'|sed 's/[][ ]*//g')
        echo $serialno
}

function get_manufacturer(){
#get the vendor info
        manufacturer=$(/usr/sbin/dmidecode |grep "Manufacturer"|sed -n "1p" |awk -F: '{print $NF}' | sed 's/[][ ]*//g')
        echo $manufacturer
}

function get_product_name(){
#get the production model
        product_name=$(/usr/sbin/dmidecode |grep "Product Name"|sed -n "1p" |awk -F: '{print $NF}')
        echo $product_name
}

function get_cpu_info(){
#get cpu model and number
        cpu_model=$(/usr/bin/lscpu |grep "Model name"|awk -F: '{print $NF}')
        echo $cpu_model
}

function get_cpu_sockets(){
#get physical cpu numbers and cores
        sockets=$(/usr/bin/lscpu |grep "Socket(s)" |awk -F: '{print $NF}' |sed 's/[][ ]*//g')
        echo $sockets
}

function get_cpu_cores(){
#get physical cpu numbers and cores
        cores=$(/usr/bin/lscpu |grep "Core(s) per socket" |awk -F: '{print $NF}' |sed 's/[][ ]*//g')
        echo $cores
}


function get_cpu_threads(){
#get physical cpu numbers and cores
        threads=$(/usr/bin/lscpu |grep "Thread(s) per core" |awk -F: '{print $NF}' |sed 's/[][ ]*//g')
        echo $threads
}

function get_mem_size(){
        mem_size=$(/usr/sbin/lshw -C memory |grep "*-bank" -A 6 |grep "size: [0-9]" |awk -F: '{print $NF}' |grep -oP "\d+"| sed 's/[][ ]*//g'|awk '{sum += $1};END{print sum}')
        echo $mem_size

}

function get_mem_slots(){
        total_mem_slots=$(/usr/sbin/lshw -C memory |grep "*-bank" |wc -l)
        echo $total_mem_slots

}

function get_empty_mem_slots(){
        total_mem_slots=$(/usr/sbin/lshw -C memory |grep "*-bank" |wc -l)
        used_mem_slots=$(/usr/sbin/lshw -C memory |grep "*-bank" -A 6 |grep "size: [0-9]" |wc -l)
        empty_mem_slots=$(expr $total_mem_slots - $used_mem_slots)
        echo $empty_mem_slots

}

function get_raid_controller_type(){
        manufacturer=$(/usr/sbin/dmidecode |grep "Manufacturer"|sed -n "1p" |awk -F: '{print $NF}' | sed 's/[][ ]*//g')
        if [[ $manufacturer == "HP" || $manufacturer == "Hewlett-Packard" ]]
        then
            raid_controller_type=$(/opt/ssacli/bin/ssacli ctrl all show status|sed -n '2p')
        fi
        echo $raid_controller_type
}

function get_raid_controller_slot(){
        manufacturer=$(/usr/sbin/dmidecode |grep "Manufacturer"|sed -n "1p" |awk -F: '{print $NF}' | sed 's/[][ ]*//g')
        if [[ $manufacturer == "HP" || $manufacturer == "Hewlett-Packard" ]]
        then
            raid_controller_type=`/opt/ssacli/bin/ssacli ctrl all show status|sed -n '2p'`
            #raid_controller_slot=$({raid_controller_type#*in} | awk '{print $2}')
            raid_controller_slot=`echo ${raid_controller_type#*in} | awk '{print $2}'`

        fi
        #echo $raid_controller_slot
}


# function get_raid_info(){
#         manufacturer=$(/usr/sbin/dmidecode |grep "Manufacturer"|sed -n "1p" |awk -F: '{print $NF}' | sed 's/[][ ]*//g')
#         if [ $manufacturer == "HP" ]
#         then
#         echo"" >/tmp/raid_info_list
#         get_raid_controller_slot
#         raidlist=`ssacli ctrl slot=$raid_controller_slot ld all show |grep -v "Smart Array"|grep "Array" |sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'|awk '{print $2}'`
#         for raid in `echo $raidlist`;do
#           raid_type=`ssacli ctrl slot=$raid_controller_slot array $raid ld all show |grep logicaldrive |awk -F, '{print $2}'|sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'`
#           echo $raid"&#"$raid_type >> /tmp/raid_info_list
#         done
#         fi
# }

function get_disk_info(){
        manufacturer=$(/usr/sbin/dmidecode |grep "Manufacturer"|sed -n "1p" |awk -F: '{print $NF}' | sed 's/[][ ]*//g')
        if [[ $manufacturer == "HP" || $manufacturer == "Hewlett-Packard" ]]
        then
        echo"" >/tmp/disk_info_list
        get_raid_controller_slot
        disklist=`/opt/ssacli/bin/ssacli ctrl slot=$raid_controller_slot pd all show status  |grep -E "physicaldrive|ssdphysicaldrive"|awk '{print $2}'`
        for disk in `echo $disklist`;do
          disk_type=`/opt/ssacli/bin/ssacli ctrl slot=$raid_controller_slot physicaldrive $disk show |grep "Drive Type"|awk -F: '{print $2}'|sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'`
          if [ "$disk_type" == "Data Drive" ]
          then
            disk_raid=`/opt/ssacli/bin/ssacli ctrl slot=$raid_controller_slot physicaldrive $disk show |grep -v "Smart Array"|grep "Array"|sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'|awk '{print $2}'`
            raid_type=`/opt/ssacli/bin/ssacli ctrl slot=$raid_controller_slot array $disk_raid ld all show |grep logicaldrive |awk -F, '{print $2}'|sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'`
          else
            disk_raid="Unassigned"
            raid_type=""
          fi
          disk_type=`/opt/ssacli/bin/ssacli ctrl slot=$raid_controller_slot physicaldrive $disk show |grep "Interface Type"|sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'|awk -F: '{print $2}'`
          disk_size=`/opt/ssacli/bin/ssacli ctrl slot=$raid_controller_slot physicaldrive $disk show |grep -v "Logical/Physical Block Size"|grep "Size"|sed 's/^[ \t]*//g'|sed 's/[ \t]*$//g'|awk -F: '{print
$2}'`
          echo $disk"&#"$disk_type"&#"$disk_size"&#"$disk_raid"&#"$raid_type >> /tmp/disk_info_list
        done
        fi

}


function get_nics_info(){
        echo "" >/tmp/tmp_net_list
        netlist=`cat /proc/net/dev|grep -Ev "Inter|face|lo"|awk -F ":" '{print $1}'|sed 's/[][ ]*//g'|sed 's/\"//g'`
        for net in `echo $netlist`;do
          nic_model=$(lshw -short |grep $net |awk '{for(i=4;i<=NF;i++)printf $i" ";printf "\n"}')
          mac=$(ip addr show $net|grep "link/ether"|awk '{print $2}'|sed 's/[][ ]*//g'|sed 's/\"//g')
          echo $net"&#"$mac"&#"$nic_model >> /tmp/tmp_net_list
        done
}






function post_server_info(){
        server_id=`get_server_id`
        sn=`get_serial_no`
        cpu_model=`get_cpu_info`
        cpu_sockets=`get_cpu_sockets`
        cpu_cores=`get_cpu_cores`
        cpu_threads=`get_cpu_threads`
        mem_size=`get_mem_size`
        mem_total_slots=`get_mem_slots`
        mem_free_slots=`get_empty_mem_slots`
        raid_adapter=`get_raid_controller_type`
        raid_adapter_slot=`get_raid_controller_slot && echo $raid_controller_slot`
        ipmi_ip=`ipmiinfo`
        tag="L"
        pxe_mac=`get_mac_addr`
        pxe_ip=`get_install_ip`
        vendor=`get_manufacturer`
        model=`get_product_name`
        get_nics_info
        get_disk_info

        printf "{" > /tmp/json.json
        printf  "\"server_id\":\"$server_id\"," >> /tmp/json.json
        printf  "\"power\":\"1\"," >> /tmp/json.json
        printf  "\"sn\":\"$sn\"," >> /tmp/json.json
        printf  "\"cpu_model\":\"$cpu_model\"," >> /tmp/json.json
        printf  "\"cpu_sockets\":\"$cpu_sockets\"," >> /tmp/json.json
        printf  "\"cpu_cores\":\"$cpu_cores\"," >> /tmp/json.json
        printf  "\"cpu_threads\":\"$cpu_threads\"," >> /tmp/json.json
        printf  "\"mem_size\":\"$mem_size\"," >> /tmp/json.json
        printf  "\"mem_total_slots\":\"$mem_total_slots\"," >> /tmp/json.json
        printf  "\"mem_free_slots\":\"$mem_free_slots\"," >> /tmp/json.json
        printf  "\"raid_adapter\":\"$raid_adapter\"," >> /tmp/json.json
        printf  "\"raid_adapter_slot\":\"$raid_adapter_slot\"," >> /tmp/json.json
        printf  "\"ipmi_ip\":\"$ipmi_ip\"," >> /tmp/json.json
        printf  "\"tag\":\"$tag\"," >> /tmp/json.json
        printf  "\"pxe_mac\":\"$pxe_mac\"," >> /tmp/json.json
        printf  "\"pxe_ip\":\"$pxe_ip\"," >> /tmp/json.json
        printf  "\"vendor\":\"$vendor\"," >> /tmp/json.json
        printf  "\"model\":\"$model\"," >> /tmp/json.json
        #add nics info
        printf  "\"nics\":[\n" >> /tmp/json.json
        FIRST_ELEMENT=1
        SAVEIFS=$IFS
        IFS=$(echo -en "\n\b")
        for nic in `cat /tmp/tmp_net_list`
        do
                nic_name=$(echo $nic|awk -F "&#" '{print $1}')
          mac=$(echo $nic|awk -F "&#" '{print $2}')
                nic_model=$(echo $nic|awk -F "&#" '{print $3}')
        if [[ $FIRST_ELEMENT -ne 1 ]]; then
                printf ",\n">>/tmp/json.json
        fi
        FIRST_ELEMENT=0
        printf  "{\n" >> /tmp/json.json
        printf  "\"nic_name\":\"$nic_name\"," >> /tmp/json.json
        printf  "\"mac\":\"$mac\"," >> /tmp/json.json
        printf  "\"nic_model\":\"$nic_model\"" >> /tmp/json.json
                printf  "}" >> /tmp/json.json
        done
        IFS=$SAVEIFS
        printf  "\n],\n" >> /tmp/json.json
        #add disk&raid info
        printf  "\"disk\":[\n" >> /tmp/json.json
        FIRST_ELEMENT=1
        SAVEIFS=$IFS
        IFS=$(echo -en "\n\b")
        for disk in `cat /tmp/disk_info_list`
        do
          raid_name=$(echo $disk|awk -F "&#" '{print $4}')
          raid_type=$(echo $disk|awk -F "&#" '{print $5}')
          disk_path=$(echo $disk|awk -F "&#" '{print $1}')
          disk_type=$(echo $disk|awk -F "&#" '{print $2}')
          disk_size=$(echo $disk|awk -F "&#" '{print $3}')
        if [[ $FIRST_ELEMENT -ne 1 ]]; then
          printf ",\n">>/tmp/json.json
        fi
        FIRST_ELEMENT=0
        printf  "{\n" >> /tmp/json.json
        printf  "\"raid_name\":\"$raid_name\"," >> /tmp/json.json
        printf  "\"raid_type\":\"$raid_type\"," >> /tmp/json.json
        printf  "\"disk_path\":\"$disk_path\"," >> /tmp/json.json
        printf  "\"disk_type\":\"$disk_type\"," >> /tmp/json.json
        printf  "\"disk_size\":\"$disk_size\"" >> /tmp/json.json
        printf  "}" >> /tmp/json.json
        done
        IFS=$SAVEIFS
        printf  "\n]\n" >> /tmp/json.json
        printf "}\n" >> /tmp/json.json
        /usr/bin/curl -H "Content-type: application/json" -X POST -d "@/tmp/json.json" http://192.168.3.168:80/installation/post_server_info/
}

post_server_info
