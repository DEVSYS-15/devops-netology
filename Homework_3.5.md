# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.
      ```bash
        lvm_experiments_disk0_path = "lvm_experiments_disk0.img"
        lvm_experiments_disk1_path = "lvm_experiments_disk1.img"
        vb.storage :file,\
                :device => 'sda',\
                :size => '2560M',\
                :path => lvm_experiments_disk1_path,\
                :bus => 'sata',\
                :discard => 'unmap'
        vb.storage :file,\
                :device => 'sdb',\
                :size => '2560M',\
                :path => lvm_experiments_disk0_path,\
                :bus => 'sata',\
                :discard => 'unmap'

   
   
   ```

   ```bash
      NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
      sda      8:0    0   2.5G  0 disk 
      sdb      8:16   0   2.5G  0 disk 
      vda    252:0    0   128G  0 disk 
      ├─vda1 252:1    0   487M  0 part /boot
      ├─vda2 252:2    0   1.9G  0 part [SWAP]
      └─vda3 252:3    0 125.6G  0 part /

   ```
4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
   ```bash    
      sda      8:0    0   2.5G  0 disk 
      ├─sda1   8:1    0     2G  0 part 
      └─sda2   8:2    0   511M  0 part 
   ```
5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.
   ```bash
   sfdisk -d /dev/sda | sfdisk  /dev/sdb   
   # lsblk
   NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
   sda      8:0    0   2.5G  0 disk 
   ├─sda1   8:1    0     2G  0 part 
   └─sda2   8:2    0   511M  0 part 
   sdb      8:16   0   2.5G  0 disk 
   ├─sdb1   8:17   0     2G  0 part 
   └─sdb2   8:18   0   511M  0 part 

   ```
6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.
   ```bash
   # lsblk
   NAME    MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
   sda       8:0    0   2.5G  0 disk  
   ├─sda1    8:1    0     2G  0 part  
   │ └─md0   9:0    0     2G  0 raid1 
   └─sda2    8:2    0   511M  0 part  
   sdb       8:16   0   2.5G  0 disk  
   ├─sdb1    8:17   0     2G  0 part  
   │ └─md0   9:0    0     2G  0 raid1 
   └─sdb2    8:18   0   511M  0 part  
   
   ```
7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.
   ```bash
   # lsblk
   NAME    MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
   sda       8:0    0   2.5G  0 disk  
   ├─sda1    8:1    0     2G  0 part  
   │ └─md0   9:0    0     2G  0 raid1 
   └─sda2    8:2    0   511M  0 part  
     └─md1   9:1    0  1017M  0 raid0 
   sdb       8:16   0   2.5G  0 disk  
   ├─sdb1    8:17   0     2G  0 part  
   │ └─md0   9:0    0     2G  0 raid1 
   └─sdb2    8:18   0   511M  0 part  
   └─md1   9:1    0  1017M  0 raid0 

   ```
8. Создайте 2 независимых PV на получившихся md-устройствах.
   ```bash
   # pvcreate /dev/md1 /dev/md0
   Physical volume "/dev/md1" successfully created.
   Physical volume "/dev/md0" successfully created.

    ```
9. Создайте общую volume-group на этих двух PV.
   ```bash
   # vgcreate vg1 /dev/md1 /dev/md0
   Volume group "vg1" successfully created
   # vgdisplay 
    --- Volume group ---
    VG Name               vg1
    System ID             
    Format                lvm2
    Metadata Areas        2
    Metadata Sequence No  1
    VG Access             read/write
    VG Status             resizable
    MAX LV                0
    Cur LV                0
    Open LV               0
    Max PV                0
    Cur PV                2
    Act PV                2
    VG Size               <2.99 GiB
    PE Size               4.00 MiB
    Total PE              765
    Alloc PE / Size       0 / 0   
    Free  PE / Size       765 / <2.99 GiB
    VG UUID               c56Io6-WRB1-f1qv-SZFd-QA34-jooq-v3x9TR

   ```
10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.
    ```bash
    # lvcreate -L 100M vg1 /dev/md1
    Logical volume "lvol0" created.

    ```
11. Создайте `mkfs.ext4` ФС на получившемся LV.
    ```bash
    mkfs.ext4 /dev/vg1/lvol0 
    mke2fs 1.45.5 (07-Jan-2020)
    Discarding device blocks: done                            
    Creating filesystem with 25600 4k blocks and 25600 inodes
   
    Allocating group tables: done                            
    Writing inode tables: done                            
    Creating journal (1024 blocks): done
    Writing superblocks and filesystem accounting information: done

    ```
12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.
    ```bash
      # mount /dev/vg1/lvol0 /mnt/
      # df -h
      Filesystem             Size  Used Avail Use% Mounted on
      udev                   1.9G     0  1.9G   0% /dev
      tmpfs                  384M  748K  383M   1% /run
      /dev/vda3              124G  3.0G  114G   3% /
      tmpfs                  1.9G     0  1.9G   0% /dev/shm
      tmpfs                  5.0M     0  5.0M   0% /run/lock
      tmpfs                  1.9G     0  1.9G   0% /sys/fs/cgroup
      /dev/vda1              456M  202M  221M  48% /boot
      tmpfs                  384M     0  384M   0% /run/user/1000
    * /dev/mapper/vg1-lvol0   93M   72K   86M   1% /mnt

    ```
13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.
    ```bash
      # la -la /mnt/
      total 21632
      drwxr-xr-x  3 root root     4096 Feb  5 08:56 .
      drwxr-xr-x 19 root root     4096 Jan 18 22:26 ..
      drwx------  2 root root    16384 Feb  5 08:52 lost+found
      -rw-r--r--  1 root root 22125941 Feb  5 05:42 test.gz

   
    ```
14. Прикрепите вывод `lsblk`.
    ```bash
      # lsblk 
      NAME            MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
      sda               8:0    0   2.5G  0 disk  
      ├─sda1            8:1    0     2G  0 part  
      │ └─md0           9:0    0     2G  0 raid1 
      └─sda2            8:2    0   511M  0 part  
        └─md1           9:1    0  1017M  0 raid0 
          └─vg1-lvol0 253:0    0   100M  0 lvm   /mnt
      sdb               8:16   0   2.5G  0 disk  
      ├─sdb1            8:17   0     2G  0 part  
      │ └─md0           9:0    0     2G  0 raid1 
      └─sdb2            8:18   0   511M  0 part  
        └─md1           9:1    0  1017M  0 raid0 
          └─vg1-lvol0 253:0    0   100M  0 lvm   /mnt
      vda             252:0    0   128G  0 disk  
      ├─vda1          252:1    0   487M  0 part  /boot
      ├─vda2          252:2    0   1.9G  0 part  [SWAP]
      └─vda3          252:3    0 125.6G  0 part  /

   
    ```
15. Протестируйте целостность файла:

     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# 
     0
     ```
    ```bash
      # gzip -t /mnt/test.gz
      # echo $?
      0

    ```

16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.
    ```bash
    # pvmove /dev/md1 /dev/md0
     /dev/md1: Moved: 20.00%
     /dev/md1: Moved: 100.00%
    # lsblk 
      NAME            MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
      sda               8:0    0   2.5G  0 disk  
      ├─sda1            8:1    0     2G  0 part  
      │ └─md0           9:0    0     2G  0 raid1 
      │   └─vg1-lvol0 253:0    0   100M  0 lvm   /mnt
      └─sda2            8:2    0   511M  0 part  
        └─md1           9:1    0  1017M  0 raid0 
      sdb               8:16   0   2.5G  0 disk  
      ├─sdb1            8:17   0     2G  0 part  
      │ └─md0           9:0    0     2G  0 raid1 
      │   └─vg1-lvol0 253:0    0   100M  0 lvm   /mnt
      └─sdb2            8:18   0   511M  0 part  
        └─md1           9:1    0  1017M  0 raid0 
      vda             252:0    0   128G  0 disk  
      ├─vda1          252:1    0   487M  0 part  /boot
      ├─vda2          252:2    0   1.9G  0 part  [SWAP]
      └─vda3          252:3    0 125.6G  0 part  /

    ```
17. Сделайте `--fail` на устройство в вашем RAID1 md.
    ```bash
     # mdadm /dev/md0 --fail /dev/sdb1
      mdadm: set /dev/sdb1 faulty in /dev/md0

    ```
18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.
    ```bash
      # dmesg | grep md0
      [  610.715766] md/raid1:md0: not clean -- starting background reconstruction
      [  610.715769] md/raid1:md0: active with 2 out of 2 mirrors
      [  610.715836] md0: detected capacity change from 0 to 2144337920
      [  610.716240] md: resync of RAID array md0
      [  633.258633] md: md0: resync done.
      [ 2437.526820] md/raid1:md0: Disk failure on sdb1, disabling device.
                     md/raid1:md0: Operation continuing on 1 devices.

    ```
19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# echo $?
     0
     ```
     ```bash
      # gzip -t /mnt/test.gz
      # echo $?
      0

    ```

20. Погасите тестовый хост, `vagrant destroy`.
    ```bash
     poweroff
   
    ```
