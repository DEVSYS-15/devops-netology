# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

    * поместите его в автозагрузку,
    * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
    * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.
   ```text
    node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2022-01-29 18:28:43 UTC; 6s ago
    Main PID: 2895 (node_exporter)
      Tasks: 6 (limit: 4496)
     Memory: 2.9M
     CGroup: /system.slice/node_exporter.service
             └─2895 /opt/node_exporter/node_exporter --collector.arp
    # cat /etc/default/node_exporter 
        EXTRA_PARAMS='--collector.arp'
   ```
   ```text
   # /etc/systemd/system/node_exporter.service
   [Unit]
   Description=Node Exporter
   After=network.target
   
   [Service]
   Type=simple
   User=node
   Group=node
   EnvironmentFile=/etc/default/node_exporter
   ExecStart=/opt/node_exporter/node_exporter $EXTRA_PARAMS
   Restart=always
   SyslogIdentifier=node_exporter
   [Install]
   WantedBy=default.target

   ```
2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.
   ```text
   CPU:
       node_cpu_seconds_total{cpu="0",mode="idle"} 2238.49
       node_cpu_seconds_total{cpu="0",mode="system"} 16.72
       node_cpu_seconds_total{cpu="0",mode="user"} 6.86
       process_cpu_seconds_total
       
   Memory:
       node_memory_MemAvailable_bytes 
       node_memory_MemFree_bytes
       
   Disk(если несколько дисков то для каждого):
       node_disk_io_time_seconds_total{device="sda"} 
       node_disk_read_bytes_total{device="sda"} 
       node_disk_read_time_seconds_total{device="sda"} 
       node_disk_write_time_seconds_total{device="sda"}
       
   Network(так же для каждого активного адаптера):
       node_network_receive_errs_total{device="eth0"} 
       node_network_receive_bytes_total{device="eth0"} 
       node_network_transmit_bytes_total{device="eth0"}
       node_network_transmit_errs_total{device="eth0"}
   ```

3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    ```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
    ```

    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.
      
    [Netdata image](https://drive.google.com/drive/folders/1lQCpVA-AhWbcdyBbY6gQt4f6JEugbReg?ths=true)
    
   
   
   
4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?
```shell
      $ dmesg | grep vir
      [    0.039696] Booting paravirtualized kernel on KVM
      [    1.182850] virtio_blk virtio0: [vda] 268435456 512-byte logical blocks (137 GB/128 GiB)
    * [    2.331104] systemd[1]: Detected virtualization kvm.
      [    2.700992] systemd[1]: Unnecessary job for /sys/devices/virtual/misc/vmbus!hv_vss was removed.
      [    2.701003] systemd[1]: Unnecessary job for /sys/devices/virtual/misc/vmbus!hv_fcopy was removed.
```
5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?
```text
   $ /sbin/sysctl -n fs.nr_open
    1048576

   
   Это максимальное число открытых дескрипторов для ядра (системы), для пользователя задать больше этого числа нельзя (если не менять). 
   Число задается кратное 1024, в данном случае =1024*1024. 
   Но макс.предел ОС можно посмотреть так :
    $  cat /proc/sys/fs/file-max
    9223372036854775807
   
   $ ulimit -Sn
    1024
    мягкий лимит (так же ulimit -n)на пользователя 


```
6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.
```bash
   # ps aux
   USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
   root           1  0.0  0.1  10860  5124 pts/0    S    21:00   0:00 /bin/bash
   root          10  0.0  0.0   8080   588 pts/0    S    21:02   0:00 unshare --fork --pid --mount-proc sleep 1h
 * root          11  0.0  0.0   8076   592 pts/0    S    21:02   0:00 sleep 1h
   root          12  0.0  0.0   8996   632 pts/0    S    21:02   0:00 nsenter --target 10 --pid --mount
   root          13  0.0  0.1  10860  5248 pts/0    S    21:02   0:00 -bash
   root          34  0.0  0.0   8996   684 pts/0    S    21:04   0:00 nsenter --target 11 --pid --mount
   root          35  0.0  0.1  10860  5200 pts/0    S    21:04   0:00 -bash
   root          92  0.0  0.0  11492  3384 pts/0    R+   21:15   0:00 ps aux
  cat /proc/11/status | grep -i nspid
  NSpid:	11	1



```
7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?
```text
cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-2.scope
Если установить ulimit -u && - число процессов будет ограниченно && для пользоователя. 

Этот Bash код создаёт функцию, которая запускает ещё два своих экземпляра, которые, в свою очередь снова запускают эту функцию и так до тех пор, пока этот процесс не займёт всю физическую память

```

