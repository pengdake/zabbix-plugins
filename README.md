# zabbix-templates

## 介绍
* zabbix-templates是基于zabbix userparameters的方式对zabbix监控项进行扩展的项目

### 环境
* centos 7
* zabbix 3.2
* libvirt 1.1.1
* libvirt-python 1.1.1
* python 2.7

### Template App Libvirt
#### 监控指标
##### domain
###### 虚拟机状态
###### 虚拟机进程所占宿主机内存
###### 虚拟机最大内存
###### 虚拟机cpu使用率
###### 虚拟机cpu数量
###### 虚拟机网卡IO总流量（字节）
###### 虚拟机磁盘读写的总字节数量

##### hypervisor
###### 总共内存大小
###### 总共cpu核心数
###### 总共cpu线程数
###### 是否支持超线程
###### cpu内存频率

### 怎么用
#### 配置文件
* 将config下面的文件拷贝到被监控主机的/etc/zabbix/zabbix_agentd.d/下
#### 模板
* 将template下的模板使用zabbix的导入功能导入
#### 脚本
* 将scripts下的子目录拷贝到被监控主机的/etc/zabbix/scripts/下
