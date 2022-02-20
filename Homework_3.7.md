# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?
 ```shell
# Windows
Get-NetAdapter
ipconfig
netsh interface ipv4 show interfaces
#Linux
  ip link
  ifconfig
  lshw -C network   
 ```
2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?
```bash
lldpd
ldpctl |grep Interface
Interface:    eth0, via: LLDP, RID: 2, Time: 5 days, 07:18:27
Interface:    eth1, via: LLDP, RID: 2, Time: 5 days, 07:18:2

```

3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.

   Это VLAN. Для её использования в Ubuntu есть пакет vlan. Приведу пример временной настройки (до перезагрузки):
```bash
      $apt install vlan
      $vconfig add eth2 9
      $ip a
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 52:54:00:15:a2:d8 brd ff:ff:ff:ff:ff:ff
        inet 192.168.121.202/24 brd 192.168.121.255 scope global dynamic eth0
           valid_lft 3468sec preferred_lft 3468sec
        inet6 fe80::5054:ff:fe15:a2d8/64 scope link 
           valid_lft forever preferred_lft forever
        3: eth0.9@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
        link/ether 52:54:00:15:a2:d8 brd ff:ff:ff:ff:ff:ff
      $ip addr add 10.0.0.9/24 dev eth0.9
      $ip link set eth0.9 up
      $ip a
         1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
             link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
             inet 127.0.0.1/8 scope host lo
                valid_lft forever preferred_lft forever
         2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
             link/ether 52:54:00:15:a2:d8 brd ff:ff:ff:ff:ff:ff
             inet 192.168.121.202/24 brd 192.168.121.255 scope global dynamic eth0
                valid_lft 2958sec preferred_lft 2958sec
             inet6 fe80::5054:ff:fe15:a2d8/64 scope link 
                valid_lft forever preferred_lft forever
         3: eth0.9@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
             link/ether 52:54:00:15:a2:d8 brd ff:ff:ff:ff:ff:ff
             inet 10.0.0.9/24 scope global eth0.9
                valid_lft forever preferred_lft forever

   
      
 ```
4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

```text
mode=0 (balance-rr)

Этот режим используется по-умолчанию, если в настройках не указано другое. balance-rr обеспечивает балансировку нагрузки и отказоустойчивость. В данном режиме пакеты отправляются "по кругу" от первого интерфейса к последнему и сначала. Если выходит из строя один из интерфейсов, пакеты отправляются на остальные оставшиеся.При подключении портов к разным коммутаторам, требует их настройки.
mode=1 (active-backup)

При active-backup один интерфейс работает в активном режиме, остальные в ожидающем. Если активный падает, управление передается одному из ожидающих. Не требует поддержки данной функциональности от коммутатора.
mode=2 (balance-xor)

Передача пакетов распределяется между объединенными интерфейсами по формуле ((MAC-адрес источника) XOR (MAC-адрес получателя)) % число интерфейсов. Один и тот же интерфейс работает с определённым получателем. Режим даёт балансировку нагрузки и отказоустойчивость.
mode=3 (broadcast)

Происходит передача во все объединенные интерфейсы, обеспечивая отказоустойчивость.
mode=4 (802.3ad)

Это динамическое объединение портов. В данном режиме можно получить значительное увеличение пропускной способности как входящего так и исходящего трафика, используя все объединенные интерфейсы. Требует поддержки режима от коммутатора, а так же (иногда) дополнительную настройку коммутатора.
mode=5 (balance-tlb)

Адаптивная балансировка нагрузки. При balance-tlb входящий трафик получается только активным интерфейсом, исходящий - распределяется в зависимости от текущей загрузки каждого интерфейса. Обеспечивается отказоустойчивость и распределение нагрузки исходящего трафика. Не требует специальной поддержки коммутатора.
mode=6 (balance-alb)

Адаптивная балансировка нагрузки (более совершенная). Обеспечивает балансировку нагрузки как исходящего (TLB, transmit load balancing), так и входящего трафика (для IPv4 через ARP). Не требует специальной поддержки коммутатором, но требует возможности изменять MAC-адрес устройства.
```
```bash
ip -br a
lo               UNKNOWN        127.0.0.1/8 
eth0             UP             192.168.121.100/24 fe80::5054:ff:feb2:7d66/64 
eth1             UP             192.168.33.10/24 fe80::5054:ff:fe9d:7652/64 
eth2             UP             192.168.33.11/24 fe80::5054:ff:fed1:2f3b/64 
vi /etc/netplan/50-vagrant.yaml
---
network:
  version: 2
  renderer: networkd
  ethernets:
    eth1: {}
    eth2: {}
  bonds:
    bond0:
      dhcp4: no
      interfaces:
      - eth1
      - eth2
      parameters:
         mode: active-backup
      addresses:
        - 192.168.33.11/24
        
netplan apply
       
ip -br a
lo               UNKNOWN        127.0.0.1/8 
eth0             UP             192.168.121.100/24 fe80::5054:ff:feb2:7d66/64 
eth1             UP             
eth2             UP             
bond0            UP             192.168.33.11/24 fe80::942e:5bff:fe9c:4bd8/64
```

5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
```bash
ipcalc 10.10.10.0/29
Address:   10.10.10.0           00001010.00001010.00001010.00000 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
HostMin:   10.10.10.1           00001010.00001010.00001010.00000 001
HostMax:   10.10.10.6           00001010.00001010.00001010.00000 110
Broadcast: 10.10.10.7           00001010.00001010.00001010.00000 111
Hosts/Net: 6                     Class A, Private Internet

ipcalc 10.10.10.0/24
Address:   10.10.10.0           00001010.00001010.00001010. 00000000
Netmask:   255.255.255.0 = 24   11111111.11111111.11111111. 00000000
Wildcard:  0.0.0.255            00000000.00000000.00000000. 11111111
=>
Network:   10.10.10.0/24        00001010.00001010.00001010. 00000000
HostMin:   10.10.10.1           00001010.00001010.00001010. 00000001
HostMax:   10.10.10.254         00001010.00001010.00001010. 11111110
Broadcast: 10.10.10.255         00001010.00001010.00001010. 11111111
Hosts/Net: 254                   Class A, Private Internet
 ```
В /24 подсети 256 адресов, значит, подсеть 10.10.10.0/24 можно разделить на 32 подсети 10.10.10.0/29 Подсети будут такими: Network: 10.10.10.0/29 Network: 10.10.10.8/29
Network: 10.10.10.16/29 и т.д. до Network: 10.10.10.248/29
6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.
```bash
ipcalc 100.64.0.0/10 -s 50
Address:   100.64.0.0           01100100.01 000000.00000000.00000000
Netmask:   255.192.0.0 = 10     11111111.11 000000.00000000.00000000
Wildcard:  0.63.255.255         00000000.00 111111.11111111.11111111
=>
Network:   100.64.0.0/10        01100100.01 000000.00000000.00000000
HostMin:   100.64.0.1           01100100.01 000000.00000000.00000001
HostMax:   100.127.255.254      01100100.01 111111.11111111.11111110
Broadcast: 100.127.255.255      01100100.01 111111.11111111.11111111
Hosts/Net: 4194302               Class A

1. Requested size: 50 hosts
Netmask:   255.255.255.192 = 26 11111111.11111111.11111111.11 000000
Network:   100.64.0.0/26        01100100.01000000.00000000.00 000000
HostMin:   100.64.0.1           01100100.01000000.00000000.00 000001
HostMax:   100.64.0.62          01100100.01000000.00000000.00 111110
Broadcast: 100.64.0.63          01100100.01000000.00000000.00 111111
Hosts/Net: 62                    Class A

Needed size:  64 addresses.
Used network: 100.64.0.0/26
Unused:
100.64.0.64/26
100.64.0.128/25
100.64.1.0/24
100.64.2.0/23
100.64.4.0/22
100.64.8.0/21
100.64.16.0/20
100.64.32.0/19
100.64.64.0/18
100.64.128.0/17
100.65.0.0/16
100.66.0.0/15
100.68.0.0/14
100.72.0.0/13
100.80.0.0/12
100.96.0.0/11
 
 ```

7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?
```shell
Windows 
  arp -arp
  Interface: 172.17.2.25 --- 0x4
  Internet Address      Physical Address      Type
  172.17.2.1            b8-69-f4-be-9d-12     dynamic
  172.17.2.11           dc-a9-04-93-5a-70     dynamic
  172.17.2.32           00-11-32-0e-3f-1a     dynamic
  172.17.2.240          78-e7-d1-c5-c7-e9     dynamic
  172.17.2.255          ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  224.0.1.60            01-00-5e-00-01-3c     static
  239.242.6.7           01-00-5e-72-06-07     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  239.255.255.255       01-00-5e-7f-ff-ff     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

  arp -d 172.17.2.240
  Interface: 172.17.2.25 --- 0x4
  Internet Address      Physical Address      Type
  172.17.2.1            b8-69-f4-be-9d-12     dynamic
  172.17.2.11           dc-a9-04-93-5a-70     dynamic
  172.17.2.32           00-11-32-0e-3f-1a     dynamic
  172.17.2.255          ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  224.0.1.60            01-00-5e-00-01-3c     static
  239.242.6.7           01-00-5e-72-06-07     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  239.255.255.255       01-00-5e-7f-ff-ff     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
Linux
  arp
  Address                  HWtype  HWaddress           Flags Mask            Iface
  172.17.2.240             ether   78:e7:d1:c5:c7:e9   C                     eth1
  192.168.121.1            ether   52:54:00:b3:28:f7   C                     eth0
  172.17.2.10              ether   00:10:18:73:bc:74   C                     eth1
  172.17.2.1               ether   b8:69:f4:be:9d:12   C                     eth1
  arp -d 172.17.2.240 
  Address                  HWtype  HWaddress           Flags Mask            Iface
  192.168.121.1            ether   52:54:00:b3:28:f7   C                     eth0
  172.17.2.10              ether   00:10:18:73:bc:74   C                     eth1
  172.17.2.1               ether   b8:69:f4:be:9d:12   C                     eth1

```


 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

 8*. Установите эмулятор EVE-ng.
 
 Инструкция по установке - https://github.com/svmyasnik240ov/eve-ng

 Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng. 
 