# 安装kubernetes #

## 安装要求 ##

```
 One or more machines running Ubuntu 16.04+, CentOS 7 or HypriotOS v1.0.1+
1GB or more of RAM per machine (any less will leave little room for your apps)
Full network connectivity between all machines in the cluster (public or private network is fine)
Unique MAC address and product_uuid for every node
Certain ports are open on your machines. See the section below for more details
```

## 安装docker ##
> [preflight] WARNING: docker version is greater than the most recently validated version. Docker version: 17.06.0-ce. Max validated version: 1.12

```
#yum install -y yum-utils device-mapper-persistent-data lvm
#yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
#yum makecache fast
#yum install docker-ce
#systemctl start docker    
```

## 安装kubectl ##
```
#curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
#chmod +x ./kubectl
#mv ./kubectl /usr/local/bin/kubectl
```
> 可以只在master安装


## 安装kubelet & kubeadm ##
```
#cat <<EOF > /etc/yum.repos.d/k8s.repo
[kubelet]
name=kubelet
baseurl=file:///root/release/rpm/output/x86_64
enabled=1
gpgcheck=0
EOF
#setenforce 0
#yum install -y kubelet kubeadm
#systemctl enable kubelet && systemctl start kubelet
```


## 准备docker镜像 ##
```
1.MAC挂在VPN，在docker里面设置http代理
2.docker login --username=feng.tang@jinmuinfo.com registry.cn-hangzhou.aliyuncs.com
3.运行脚本 k8s.sh
#!/usr/bin/env bash

images=(
    kube-proxy-amd64:v1.7.1
    kube-controller-manager-amd64:v1.7.1
    kube-apiserver-amd64:v1.7.1
    kube-scheduler-amd64:v1.7.1
    kubernetes-dashboard-amd64:v1.6.0
    k8s-dns-sidecar-amd64:1.14.1
    k8s-dns-kube-dns-amd64:1.14.1
    k8s-dns-dnsmasq-nanny-amd64:1.14.1
    etcd-amd64:3.0.17
    pause-amd64:3.0
)

for imageName in ${images[@]} ; do
    docker pull gcr.io/google_containers/$imageName
    docker tag gcr.io/google_containers/$imageName registry.cn-hangzhou.aliyuncs.com/collapsar/$imageName
    docker push registry.cn-hangzhou.aliyuncs.com/collapsar/$imageName
done

docker pull quay.io/coreos/flannel:v0.7.0-amd64
docker tag quay.io/coreos/flannel:v0.7.0-amd64 registry.cn-hangzhou.aliyuncs.com/collapsar/flannel:v0.7.0-amd64
docker push registry.cn-hangzhou.aliyuncs.com/collapsar/flannel:v0.7.0-amd64
```

export KUBE_REPO_PREFIX="registry.cn-hangzhou.aliyuncs.com/collapsar"
export KUBE_ETCD_IMAGE="registry.cn-hangzhou.aliyuncs.com/collapsar/etcd-amd64:3.0.17"

kubeadm init --kubernetes-version=v1.7.1

  kubeadm join --token d2316d.2c59563673c66b38 192.168.101.200:6443

```
> 如果卡住，可以将阿里云上的image pull下来，tag到gcr.io/google_containers

```
kubectl执行后可能会有报错"The connection to the server localhost:8080 was refused - did you specify the right host or port?"

执行以下命令：
sudo cp /etc/kubernetes/admin.conf $HOME/
sudo chown $(id -u):$(id -g) $HOME/admin.conf
export KUBECONFIG=$HOME/admin.conf
```
