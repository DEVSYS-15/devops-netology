# Домашнее задание к занятию "6.3. MySQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.
```text
docker run --name mysql -e MYSQL_ROOT_PASSWORD=123 -it -v ~/db-data2:/var/lib/mysql/ -v ~/db-backup:/backup -p 3306:3306   mysql:8
```

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.
```text
mysql -u root -p
CREATE SCHEMA `test_db` ;
\q
mysql -u root -p test_db < /backup/test_dump.sql 
```
Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.
```text
Note that all text commands must be first on line and end with ';'
?         (\?) Synonym for `help'.
clear     (\c) Clear the current input statement.
connect   (\r) Reconnect to the server. Optional arguments are db and host.
delimiter (\d) Set statement delimiter.
edit      (\e) Edit command with $EDITOR.
ego       (\G) Send command to mysql server, display result vertically.
exit      (\q) Exit mysql. Same as quit.
go        (\g) Send command to mysql server.
help      (\h) Display this help.
nopager   (\n) Disable pager, print to stdout.
notee     (\t) Don't write into outfile.
pager     (\P) Set PAGER [to_pager]. Print the query results via PAGER.
print     (\p) Print current command.
prompt    (\R) Change your mysql prompt.
quit      (\q) Quit mysql.
rehash    (\#) Rebuild completion hash.
source    (\.) Execute an SQL script file. Takes a file name as an argument.
status    (\s) Get status information from the server.
system    (\!) Execute a system shell command.
tee       (\T) Set outfile [to_outfile]. Append everything into given outfile.
use       (\u) Use another database. Takes database name as argument.
charset   (\C) Switch to another charset. Might be needed for processing binlog with multi-byte charsets.
warnings  (\W) Show warnings after every statement.
nowarning (\w) Don't show warnings after every statement.
resetconnection(\x) Clean session context.
query_attributes Sets string parameters (name1 value1 name2 value2 ...) for the next query to pick up.
ssl_session_data_print Serializes the current SSL session data to stdout or file

For server side help, type 'help contents'


```

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.
```text
ysql> status
--------------
mysql  Ver 8.0.29 for Linux on x86_64 (MySQL Community Server - GPL)

Connection id:		19
Current database:	
Current user:		root@localhost
SSL:			Not in use
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		8.0.29 MySQL Community Server - GPL
Protocol version:	10
Connection:		Localhost via UNIX socket
Server characterset:	utf8mb4
Db     characterset:	utf8mb4
Client characterset:	latin1
Conn.  characterset:	latin1
UNIX socket:		/var/run/mysqld/mysqld.sock
Binary data as:		Hexadecimal
Uptime:			22 min 13 sec

Threads: 2  Questions: 54  Slow queries: 0  Opens: 156  Flush tables: 3  Open tables: 74  Queries per second avg: 0.040
--------------



```
Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.
```test

mysql> select count(*) from orders where  `price` > 300;
+----------+
| count(*) |
+----------+
|        1 |
+----------+
```

В следующих заданиях мы будем продолжать работу с данным контейнером.

## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"
```text
CREATE USER 'test'@'localhost'
  IDENTIFIED WITH mysql_native_password BY 'test-pass' 
  WITH MAX_QUERIES_PER_HOUR 100 
  password expire INTERVAL 180 day 
  FAILED_LOGIN_ATTEMPTS 3 
  ATTRIBUTE '{"fname": "James", "lname": "Pretty"}';
```
Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
```text
GRANT SELECT ON test_db.* TO 'test'@'localhost';
```    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.
```text
select * from information_schema.USER_ATTRIBUTES where user = 'test';
+------+-----------+---------------------------------------+
| USER | HOST      | ATTRIBUTE                             |
+------+-----------+---------------------------------------+
| test | localhost | {"fname": "James", "lname": "Pretty"} |
+------+-----------+---------------------------------------+
1 row in set (0.00 sec)

```
## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.
```text
SHOW PROFILES;
+----------+------------+----------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                  |
+----------+------------+----------------------------------------------------------------------------------------+
|        1 | 0.00021525 | SET profiling = 1                                                                      |
|        2 | 0.00200200 | SELECT TABLE_NAME,ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'test_db' |
+----------+------------+----------------------------------------------------------------------------------------+
2 rows in set, 1 warning (0.00 sec)

```

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.
```text
SELECT TABLE_NAME,ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0.00 sec)

```

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
- на `InnoDB`
```text
9 | 0.63893250 | ALTER TABLE test_db.orders ENGINE = MyISAM 
10 | 1.00194400 | ALTER TABLE test_db.orders ENGINE = InnoDB  
```
## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.
```text
    [mysqld]
    pid-file        = /var/run/mysqld/mysqld.pid
    socket          = /var/run/mysqld/mysqld.sock
    datadir         = /var/lib/mysql
    secure-file-priv= NULL
    
    
    
    innodb_flush_log_at_trx_commit = 2
    innodb_log_buffer_size = 1M
    innodb_buffer_pool_size = 15G
    innodb_log_buffer_size = 1М
    # Custom config should go here
    !includedir /etc/mysql/conf.d/  

```

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
