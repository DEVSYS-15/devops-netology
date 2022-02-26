# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```
2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.

```bash
modprobe -v dummy numdummies=2
ifconfig -a | grep dummy
dummy0: flags=130<BROADCAST,NOARP>  mtu 1500
dummy1: flags=130<BROADCAST,NOARP>  mtu 1500
ip addr add 192.168.0.2/255.255.255.0 dev dummy0
ip addr add 192.168.0.3/255.255.255.0 dev dummy1
ip link set dev dummy0 up
ip link set dev dummy1 up
ip -br  a
lo               UNKNOWN        127.0.0.1/8 
eth0             UP             192.168.121.44/24 fe80::5054:ff:fed2:3e45/64 
eth1             UP             172.17.2.19/24 fe80::5054:ff:fe4a:5361/64 
dummy0           UNKNOWN           192.168.0.2/24 
dummy1           UNKNOWN           192.168.0.3/24 


ip route add 192.168.3.1/32 via 192.168.0.2
ip route add 192.168.3.2/32 via 192.168.0.3
ip route show
default via 192.168.121.1 dev eth0 proto dhcp src 192.168.121.44 metric 100 
default via 172.17.2.1 dev eth1 proto dhcp src 172.17.2.19 metric 100 
172.17.2.0/24 dev eth1 proto kernel scope link src 172.17.2.19 
172.17.2.1 dev eth1 proto dhcp scope link src 172.17.2.19 metric 100 
192.168.0.0/24 dev dummy0 proto kernel scope link src 192.168.0.2 
192.168.0.0/24 dev dummy1 proto kernel scope link src 192.168.0.3 
192.168.3.1 via 192.168.0.2 dev dummy0 
192.168.3.2 via 192.168.0.3 dev dummy1 
192.168.121.0/24 dev eth0 proto kernel scope link src 192.168.121.44 
192.168.121.1 dev eth0 proto dhcp scope link src 192.168.121.44 metric 100 


```

3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.
```bash

 netstat -tnlp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      614/systemd-resolve 
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      857/sshd: /usr/sbin 
tcp        0      0 127.0.0.1:8125          0.0.0.0:*               LISTEN      1693/netdata        
tcp        0      0 127.0.0.1:19999         0.0.0.0:*               LISTEN      1693/netdata  
ss -t -a
State                       Recv-Q                      Send-Q                                            Local Address:Port                                              Peer Address:Port                      Process                     
LISTEN                      0                           4096                                              127.0.0.53%lo:domain                                                 0.0.0.0:*                                                     
LISTEN                      0                           128                                                     0.0.0.0:ssh                                                    0.0.0.0:*                                                     
LISTEN                      0                           4096                                                  127.0.0.1:8125                                                   0.0.0.0:*                                                     
LISTEN                      0                           4096                                                  127.0.0.1:19999                                                  0.0.0.0:*                                                     
ESTAB                       0                           0                                                192.168.121.44:ssh                                              192.168.121.1:54470                                                 
LISTEN                      0                           128                                                        [::]:ssh                                                       [::]:*      


 
```
4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?
```bash
netstat -unlp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
udp        0      0 127.0.0.1:8125          0.0.0.0:*                           1693/netdata        
udp        0      0 127.0.0.53:53           0.0.0.0:*                           614/systemd-resolve 
udp        0      0 172.17.2.19:68          0.0.0.0:*                           424/systemd-network 
udp        0      0 192.168.121.44:68       0.0.0.0:*                           424/systemd-network 


```
5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали. 
[ip plan](https://drive.google.com/drive/folders/1L8qDKrHzsj7bi6EWvVZEvEUoXIWTe7OX)
 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

6*. Установите Nginx, настройте в режиме балансировщика TCP или UDP.

7*. Установите bird2, настройте динамический протокол маршрутизации RIP.

8*. Установите Netbox, создайте несколько IP префиксов, используя curl проверьте работу API.



