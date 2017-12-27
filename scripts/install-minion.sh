#!/bin/sh -
#######################################################################################################################
#
#          FILE: minion-setup.sh
#
#   DESCRIPTION:  Salt minion installation for redhat&centos system
# -*- coding: utf-8 -*-
#
# @author: alex.tang <feng.tang@jinmuinfo.com>
# Created on 2017/07/20
#
#######################################################################################################################


salt_repo_server="192.168.3.169"
salt_master_ip="192.168.3.169"
salt_conf_dir="/etc/salt"
repo_rev="2016.11"

#######################################################################################################################
#
#   install salt minion
#

install_saltstack_rhel_repository() {
  rv=$(lsb_release >/dev/null 2>&1)
  if [ $? -eq 0 ]; then
    DISTRO_MAJOR_VERSION=$(lsb_release -sr |awk -F. '{print $1}')
  else
    DISTRO_VERSION=$(cat /etc/redhat-release)
    if [ "$(echo $DISTRO_VERSION | egrep '5\.')" != "" ]; then
      DISTRO_MAJOR_VERSION=5
    elif [ "$(echo $DISTRO_VERSION  | egrep '6\.')" != "" ]; then
      DISTRO_MAJOR_VERSION=6
    elif [ "$(echo $DISTRO_VERSION  | egrep '7\.')" != "" ]; then
      DISTRO_MAJOR_VERSION=7
    fi
  fi
  echo $DISTRO_MAJOR_VERSION


    base_url="http://${salt_repo_server}/yum/redhat/${DISTRO_MAJOR_VERSION}/\$basearch/${repo_rev}/"
    repo_file="/etc/yum.repos.d/saltstack.repo"

    if [ ! -s "$repo_file" ]; then
        cat <<_eof > "$repo_file"
[saltstack]
name=SaltStack ${repo_rev} Release Channel for RHEL/CentOS \$releasever
baseurl=${base_url}
gpgcheck=0
enabled=1
_eof
    fi
    yum clean all
}

yum_install_noinput() {
    yum -y install salt-minion
}

#######################################################################################################################
#
#   enable salt minion service
#

install_centos_stable_post() {
        if [ -f /bin/systemctl ]; then
                /bin/systemctl start salt-minion.service
                /bin/systemctl enable salt-minion.service

        elif [ -f "/etc/init.d/salt-minion" ]; then
            /sbin/chkconfig salt-minion on
            /sbin/service salt-minion start
        fi
    return 0
}


#######################################################################################################################
#
#   config salt minion
#
config_salt_minion() {
    if [ -f "$salt_conf_dir/minion" ]; then
        /bin/cp "$salt_conf_dir/minion" "$salt_conf_dir/minion.`date +%Y%m%d%H%M%S`"
    fi
    if [ "$(egrep '^master' $salt_conf_dir/minion)" = ""  ]; then
      echo "master: $salt_master_ip" >> $salt_conf_dir/minion
    else
      echo "master already setup for this minion, please check!"
    fi
}


salt_minion_setup(){
  install_saltstack_rhel_repository
  yum_install_noinput
  config_salt_minion
  install_centos_stable_post
}

salt_minion_setup