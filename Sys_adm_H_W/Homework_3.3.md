#Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

#####1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`.

```bash       
# strace -d /bin/bash -c 'cd /tmp' 2>&1 | grep  tmp   
execve("/bin/bash", ["/bin/bash", "-c", "cd /tmp"], 0x7ffe8c66cbf8 /* 24 vars */strace: [wait(0x04057f) = 2969] WIFSTOPPED,sig=SIGTRAP,EVENT_EXEC (4)
stat("/tmp", strace: [wait(0x00857f) = 2969] WIFSTOPPED,sig=133
chdir("/tmp"strace: [wait(0x00857f) = 2969] WIFSTOPPED,sig=133

вызов chdir
```
    


#####2. Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:  

```bash   
vagrant@netology1:~$ file /dev/tty

/dev/tty: character special (5/0)
vagrant@netology1:~$ file /dev/sda
/dev/sda: block special (8/0)
vagrant@netology1:~$ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64
```
    
   Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.

```bash
    # strace -d file /dev/tty 2>&1 | grep  -i open | grep -v .so
    
    openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXECstrace: [wait(0x00857f) = 2996] WIFSTOPPED,sig=133
    openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLYstrace: [wait(0x00857f) = 2996] WIFSTOPPED,sig=133
    openat(AT_FDCWD, "/etc/magic", O_RDONLYstrace: [wait(0x00857f) = 2996] WIFSTOPPED,sig=133
    openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLYstrace: [wait(0x00857f) = 2996] WIFSTOPPED,sig=133
    openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLYstrace: [wait(0x00857f) = 2996] WIFSTOPPED,sig=133
    # strace -d file /dev/tty 2>&1 | grep  -i magic | grep -v .so
     Magic local data for file(1) c"..., 4096) = 111
    openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLYstrace: [wait(0x00857f) = 3043] WIFSTOPPED,sig=133
```

#####3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).
```bash
$ vi home/serz/.cmd_yes.sh1
$ lsof   | grep cmd_yes.sh1
vi      23618 serz    3u   REG   8,21    12288  4722033 /home/serz/.cmd_yes.sh1.swp
$ rm /home/serz/.cmd_yes.sh1.swp
$ lsof   | grep cmd_yes.sh1
vi      23618 serz    3u   REG   8,21    12288  4722033 /home/serz/.cmd_yes.sh1.swp (deleted)
echo '' > /proc/23618/fd/3
23618 - PID процесса vi
3 - дескриптор файла , который предварительно удалил. 

```

#####4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?
```text
    "Зомби" процессы, в отличии от "сирот" освобождают свои ресурсы, но не освобождают запись в таблице процессов. 
    запись освободиться при вызове wait() родительским процессом. 
```
#####5. В iovisor BCC есть утилита `opensnoop`:
```bash
 root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
 /usr/sbin/opensnoop-bpfcc
```
 На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).

```text
если я правильно понял задание то:
при запуске strace -t  -e trace=openat opensnoop-bpfcc 2>>  time
вывод в первую секунду работы будет очень большим, всего 108 вызовов , ниже  первие строки
13:42:10 openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libdl.so.2", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libutil.so.1", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libexpat.so.1", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
13:42:10 openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3



```
   
#####6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.
```text
системный вызов uname()


 Part of the utsname information is also accessible  via  /proc/sys/ker‐
   nel/{ostype, hostname, osqrelease, version, domainname}.

```
#####7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
```bash
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```
   Есть ли смысл использовать в bash `&&`, если применить `set -e`?
```text
&& -  условный оператор, 
а ;  - разделитель последовательных команд

test -d /tmp/some_dir && echo Hi - в данном случае echo  отработает только при успешном заверщении команды test

set -e - прерывает сессию при любом ненулевом значении исполняемых команд в конвеере кроме последней.
в случае &&  вместе с set -e- вероятно не имеет смысла, так как при ошибке , выполнение команд прекратиться.
```
#####8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?
```text
-e прерывает выполнение исполнения при ошибке любой команды кроме последней в последовательности 
-x вывод трейса простых команд 
-u неустановленные/не заданные параметры и переменные считаются как ошибки, с выводом в stderr текста ошибки и выполнит завершение неинтерактивного вызова
-o pipefail возвращает код возврата набора/последовательности команд, ненулевой при последней команды или 0 для успешного выполнения команд.

По сути, для сценария , повышает деталезацию вывода ошибок(логирования), 
и завершит сценарий при наличии ошибок, на любом этапе выполнения сценария, кроме последней завершающей команды
```



#####9 Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).


```bash
    $ ps -ax  -o stat > ps-stat && for i in $(cat ps-stat | sort -u) ; do echo -e  $(grep -c  $i ps-stat) >> ps-stat.out $i  ; done  && cat ps-stat.out |  sort  &&  rm -f ps-stat.out ps-stat
    10 Ssl
    1 R+
    1 SLsl
    1 S<s
    1 STAT
    28 Ss
    2 S+
    2 SN
    2 Ss+
    40 I<
    47 I
    85 S
    9 S<
```
```text

S*(S,S+,Ss,Ssl,Ss+) - Спящий: ожидает завершения события.
I*(I,I<) - Рождающийся: процесс создается. 

доп символы это доп характеристики, например приоритет.

```