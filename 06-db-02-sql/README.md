# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.
```text
docker run --name postgres -e POSTGRES_PASSWORD=postgres -it --rm -v db-data:/var/lib/postgresql/data -v db-backup:/backup -p 5432:5432 -d postgres:12

```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
  - postgres=# create database test_db;
  - postgres=# create user "test-admin-user" with password '123';
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
  ```postgres-sql
  test_db=# \d clients
                                    Table "public.clients"
        Column       |  Type   | Collation | Nullable |               Default               
  -------------------+---------+-----------+----------+-------------------------------------
   id                | integer |           | not null | nextval('clients_id_seq'::regclass)
   фамилия           | text    |           |          | 
   страна проживания | text    |           |          | 
   заказ             | integer |           |          | 
  Indexes:
      "clients_pkey" PRIMARY KEY, btree (id)
  Foreign-key constraints:
      "заказ_fk" FOREIGN KEY ("заказ") REFERENCES orders(id)
  
  test_db=# \d orders
                                 Table "public.orders"
      Column    |  Type   | Collation | Nullable |              Default               
  --------------+---------+-----------+----------+------------------------------------
   id           | integer |           | not null | nextval('orders_id_seq'::regclass)
   наименование | text    |           |          | 
   цена         | integer |           |          | 
  Indexes:
      "orders_pkey" PRIMARY KEY, btree (id)
  Referenced by:
      TABLE "clients" CONSTRAINT "заказ_fk" FOREIGN KEY ("заказ") REFERENCES orders(id)
  

   ```
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
  - GRANT ALL PRIVILEGES ON DATABASE  test_db to "test-admin-user"  
- создайте пользователя test-simple-user 
  - create user "test-simple-user" with password '123';
  - CREATE SCHEMA test_schema
  - SET search_path TO test_schema, public;
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db
  - GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES  IN SCHEMA test_schema  to "test-simple-user"

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
  ```postgres-psql
    List of databases
     Name    |  Owner   | Encoding |  Collate   |   Ctype    |       Access privileges        
  -----------+----------+----------+------------+------------+--------------------------------
   postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
   template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
             |          |          |            |            | postgres=CTc/postgres
   template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres                   +
             |          |          |            |            | postgres=CTc/postgres
   test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/postgres                  +
             |          |          |            |            | postgres=CTc/postgres         +
             |          |          |            |            | "test-admin-user"=CTc/postgres
  (4 rows)
    ```
- описание таблиц (describe)
  ```postgres-sql
    test_db=# \d clients
                                      Table "public.clients"
          Column       |  Type   | Collation | Nullable |               Default               
    -------------------+---------+-----------+----------+-------------------------------------
     id                | integer |           | not null | nextval('clients_id_seq'::regclass)
     фамилия           | text    |           |          | 
     страна проживания | text    |           |          | 
     заказ             | integer |           |          | 
    Indexes:
        "clients_pkey" PRIMARY KEY, btree (id)
    Foreign-key constraints:
        "заказ_fk" FOREIGN KEY ("заказ") REFERENCES orders(id)
  
    test_db=# \d orders
                                   Table "public.orders"
        Column    |  Type   | Collation | Nullable |              Default               
    --------------+---------+-----------+----------+------------------------------------
     id           | integer |           | not null | nextval('orders_id_seq'::regclass)
     наименование | text    |           |          | 
     цена         | integer |           |          | 
    Indexes:
        "orders_pkey" PRIMARY KEY, btree (id)
    Referenced by:
        TABLE "clients" CONSTRAINT "заказ_fk" FOREIGN KEY ("заказ") REFERENCES orders(id)
  

   ```

- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
  - SELECT * FROM information_schema.table_privileges where table_name = 'order' or table_name = 'clients'
- список пользователей с правами над таблицами test_db
```text
     grantor  |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy 
----------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 postgres | postgres         | test_db       | test_schema  | clients    | INSERT         | YES          | NO
 postgres | postgres         | test_db       | test_schema  | clients    | SELECT         | YES          | YES
 postgres | postgres         | test_db       | test_schema  | clients    | UPDATE         | YES          | NO
 postgres | postgres         | test_db       | test_schema  | clients    | DELETE         | YES          | NO
 postgres | postgres         | test_db       | test_schema  | clients    | TRUNCATE       | YES          | NO
 postgres | postgres         | test_db       | test_schema  | clients    | REFERENCES     | YES          | NO
 postgres | postgres         | test_db       | test_schema  | clients    | TRIGGER        | YES          | NO
 postgres | test-simple-user | test_db       | test_schema  | clients    | INSERT         | NO           | NO
 postgres | test-simple-user | test_db       | test_schema  | clients    | SELECT         | NO           | YES
 postgres | test-simple-user | test_db       | test_schema  | clients    | UPDATE         | NO           | NO
 postgres | test-simple-user | test_db       | test_schema  | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | test_schema  | clients    | INSERT         | NO           | NO
 postgres | test-admin-user  | test_db       | test_schema  | clients    | SELECT         | NO           | YES
 postgres | test-admin-user  | test_db       | test_schema  | clients    | UPDATE         | NO           | NO
 postgres | test-admin-user  | test_db       | test_schema  | clients    | DELETE         | NO           | NO
 postgres | test-admin-user  | test_db       | test_schema  | clients    | TRUNCATE       | NO           | NO
 postgres | test-admin-user  | test_db       | test_schema  | clients    | REFERENCES     | NO           | NO
 postgres | test-admin-user  | test_db       | test_schema  | clients    | TRIGGER        | NO           | NO

    
   ```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.
      - select count(*) from order          - 5 
      - select count(*) from clients        - 5 
## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.
```postgres-psql
UPDATE clients SET заказ = 5 WHERE id = 3;
UPDATE clients SET заказ = 4 HERE id = 2
UPDATE clients SET заказ = 3 HERE id = 1
```

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
```postgres-psql
SELECT r.фамилия ,f.наименование       From test_schema.clients AS r
JOIN test_schema.orders as f ON (r.заказ = f.id)

```

Подсказк - используйте директиву `UPDATE`.

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.
```text
explain SELECT r.фамилия ,f.наименование       From test_schema.clients AS r
JOIN test_schema.orders as f ON (r.заказ = f.id)
;
                               QUERY PLAN                                
-------------------------------------------------------------------------
 Hash Join  (cost=37.00..57.24 rows=810 width=64)
   Hash Cond: (r."заказ" = f.id)
   ->  Seq Scan on clients r  (cost=0.00..18.10 rows=810 width=36)
   ->  Hash  (cost=22.00..22.00 rows=1200 width=36)
         ->  Seq Scan on orders f  (cost=0.00..22.00 rows=1200 width=36)
(5 rows)
Это означает последовательное, блок за блоком, чтение данных таблицы.
cost - некое понятия. призванное оченить затратность операции. 
rows — приблизительное количество возвращаемых строк при выполнении операции Seq Scan. Это значение возвращает планировщик.
width — средний размер одной строки в байтах.

```


## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 
```text
    
pg_dump -f /backup/test_db.dump -Upostgres test_db -сохраняем БД на примонтированый volume и останавливаем контейнер

Запускаем контейнер с новымми volume
docker run --name postgres -e POSTGRES_PASSWORD=postgres -it --rm -v newdb-data:/var/lib/postgresql/data -v db-backup:/backup -p 5432:5432 postgres:12
Восстановление БД
create database test_db OWNER 'postgres' ENCODING 'UTF8' - создаем БД
psql -Upostgres test_db < /backup/test_db.dump - восстанавливаем БД из примонтированного volume
```

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
