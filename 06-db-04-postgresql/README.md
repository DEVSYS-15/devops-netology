# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
  - postgres=# \l 
- подключения к БД
  -  postgres=# \c
- вывода списка таблиц
  -  postgres-# \dt
- вывода описания содержимого таблиц
  - postgres-# \d[S+] 
- выхода из psql
  - postgres-# \q
## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.
- psql -Upostgres test_database < /backup/test_database.dump

Перейдите в управляющую консоль `psql` внутри контейнера.
-  psql -U postgres -h 172.18.0.2

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.
- elect avg_width from pg_stats where tablename = 'orders';
 avg_width 
-----------
         4
        16
         4


## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.
-     
    create table orders_1 (
        check (price > 499)
    ) inherits (orders);
    
    create table orders_2 (
        check (price <= 499)
    ) inherits (orders);

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?
-  Да можно если при изначальном проектировании таблиц сделать ее секционированной.
## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.
-  pg_dump -U postgres test_database > /backup/test_database_new.dump

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.
-    Необходимо добавить строку
    ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_title_key UNIQUE (title);

---
