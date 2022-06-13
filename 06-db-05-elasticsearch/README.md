# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
  - ```shell
    FROM bluedata/centos7:latest
    EXPOSE 9200
    
    
    
    RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.2-linux-x86_64.tar.gz \
        && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.2-linux-x86_64.tar.gz.sha512 
    RUN yum install perl-Digest-SHA -y 
    RUN shasum -a 512 -c elasticsearch-8.2.2-linux-x86_64.tar.gz.sha512 \ 
        && tar -xzf elasticsearch-8.2.2-linux-x86_64.tar.gz \
        && yum upgrade -y \
        && rm -f elasticsearch-8.2.2-linux-x86_64.tar.gz elasticsearch-8.2.2-linux-x86_64.tar.gz.sha512
        
    ADD elasticsearch.yml /elasticsearch-8.2.2/config/
    ENV ES_HOME=/elasticsearch-8.2.2
    RUN groupadd elasticsearch \
        && useradd -g elasticsearch elasticsearch
        
    RUN mkdir /var/lib/logs /var/lib/data  \
        && chown elasticsearch:elasticsearch /var/lib/logs \
        && chown elasticsearch:elasticsearch /var/lib/data \
        && chown -R elasticsearch:elasticsearch /elasticsearch-8.2.2/
    
    RUN mkdir /elasticsearch-8.2.2/snapshots &&\
    chown elasticsearch:elasticsearch /elasticsearch-8.2.2/snapshots
        
    USER elasticsearch
    CMD ["/elasticsearch-8.2.2/bin/elasticsearch"]
    ``` 
- ссылку на образ в репозитории dockerhub
  - [dockerhub](https://hub.docker.com/repository/docker/devsys15/elastic)
- ответ `elasticsearch` на запрос пути `/` в json виде
  - ```text
    /elasticsearch-8.2.2/bin/elasticsearch-reset-password -b -u elastic
    Password for the [elastic] user successfully reset.
    New value: Sk=VqvPyTPFDjzV-KbEn

    curl -k   -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200
    {
      "name" : "netology_test",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "67I8w7ZJQeC9jOTOnt4-9g",
      "version" : {
        "number" : "8.2.2",
        "build_flavor" : "default",
        "build_type" : "tar",
        "build_hash" : "9876968ef3c745186b94fdabd4483e01499224ef",
        "build_date" : "2022-05-25T15:47:06.259735307Z",
        "build_snapshot" : false,
        "lucene_version" : "9.1.0",
        "minimum_wire_compatibility_version" : "7.17.0",
        "minimum_index_compatibility_version" : "7.0.0"
      },
      "tagline" : "You Know, for Search"
    }
    ``` 

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.
  - ```shell
    curl -k -X GET -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/_cat/indices?v
    health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   ind-2 nu380veXSgCfz5trbKOHPA   2   1          0            0       450b           450b
    green  open   ind-1 GJg1iV1kR7mYWCgD2m3obg   1   0          0            0       225b           225b
    yellow open   ind-3 yWJSYjPBQxyv6vDUnkNXhg   4   2          0            0       900b           900b
    curl -k -X GET -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/_cluster/health/ind-1?pretty
    {
      "cluster_name" : "elasticsearch",
      "status" : "green",
      "timed_out" : false,
      "number_of_nodes" : 1,
      "number_of_data_nodes" : 1,
      "active_primary_shards" : 1,
      "active_shards" : 1,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 0,
      "delayed_unassigned_shards" : 0,
      "number_of_pending_tasks" : 0,
      "number_of_in_flight_fetch" : 0,
      "task_max_waiting_in_queue_millis" : 0,
      "active_shards_percent_as_number" : 100.0
    }
    curl -k -X GET -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/_cluster/health/ind-2?pretty
    {
      "cluster_name" : "elasticsearch",
      "status" : "yellow",
      "timed_out" : false,
      "number_of_nodes" : 1,
      "number_of_data_nodes" : 1,
      "active_primary_shards" : 2,
      "active_shards" : 2,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 2,
      "delayed_unassigned_shards" : 0,
      "number_of_pending_tasks" : 0,
      "number_of_in_flight_fetch" : 0,
      "task_max_waiting_in_queue_millis" : 0,
      "active_shards_percent_as_number" : 47.368421052631575
    }
    curl -k -X GET -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/_cluster/health/ind-3?pretty
    {
      "cluster_name" : "elasticsearch",
      "status" : "yellow",
      "timed_out" : false,
      "number_of_nodes" : 1,
      "number_of_data_nodes" : 1,
      "active_primary_shards" : 4,
      "active_shards" : 4,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 8,
      "delayed_unassigned_shards" : 0,
      "number_of_pending_tasks" : 0,
      "number_of_in_flight_fetch" : 0,
      "task_max_waiting_in_queue_millis" : 0,
      "active_shards_percent_as_number" : 47.368421052631575
    }


    ``` 

Получите состояние кластера `elasticsearch`, используя API.
- ```shell
  curl -k -X GET -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/_cluster/health/ind-3?pretty
  {
    "cluster_name" : "elasticsearch",
    "status" : "yellow",
    "timed_out" : false,
    "number_of_nodes" : 1,
    "number_of_data_nodes" : 1,
    "active_primary_shards" : 4,
    "active_shards" : 4,
    "relocating_shards" : 0,
    "initializing_shards" : 0,
    "unassigned_shards" : 8,
    "delayed_unassigned_shards" : 0,
    "number_of_pending_tasks" : 0,
    "number_of_in_flight_fetch" : 0,
    "task_max_waiting_in_queue_millis" : 0,
    "active_shards_percent_as_number" : 47.368421052631575
  }
  ```

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
- ```text
  Индексы находятся в статусе Yellow потому что у них указано число реплик, а по факту руплицировать некуда, т.к. нет других серверов.   
  ``` 

Удалите все индексы.
- ```shell
   curl -k -X DELETE -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/ind-1?pretty
  {
    "acknowledged" : true
  }
   curl -k -X DELETE -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/ind-2?pretty
  {
    "acknowledged" : true
  }
   curl -k -X DELETE -u elastic:Sk=VqvPyTPFDjzV-KbEn https://localhost:9200/ind-3?pretty
  {
  "acknowledged" : true
  }     
  ``` 

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.
- ```text
  curl -k -X PUT -u elastic:yYn7p6ig5HOw_xHP2XZD https://localhost:9200/_snapshot/netology_backup?pretty -H 'Content-Type: application/json' -d'{"type": "fs", "settings": { "location":"myrepo" }}'
  {
    "acknowledged" : true
  }

  ```


Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.
- ```text
  curl -k -X GET -u elastic:yYn7p6ig5HOw_xHP2XZD https://localhost:9200/test?pretty
  {
    "test" : {
      "aliases" : { },
      "mappings" : { },
      "settings" : {
        "index" : {
          "routing" : {
            "allocation" : {
              "include" : {
                "_tier_preference" : "data_content"
              }
            }
          },
          "number_of_shards" : "1",
          "provided_name" : "test",
          "creation_date" : "1655078261537",
          "number_of_replicas" : "0",
          "uuid" : "ljG8XHUTQ1Wmntui2vkXhw",
          "version" : {
            "created" : "8020299"
          }
        }
      }
    }
  }

  ```

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.
- ```text
  ls   /elasticsearch-8.2.2/snapshots/myrepo/
  index-0  index.latest  indices  meta-Aq49bILkTWiBXNXmWMXWgw.dat  snap-Aq49bILkTWiBXNXmWMXWgw.dat

  ```

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.
- ```text
  curl -k -X GET -u elastic:yYn7p6ig5HOw_xHP2XZD https://localhost:9200/_cat/indices?v
  health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
  green  open   test-2 de4s707GQkuqu_S5uAxKtA   1   0          0            0       225b           225b
  ```

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.
- ```text
  curl -k -X POST -u elastic:yYn7p6ig5HOw_xHP2XZD https://localhost:9200/_snapshot/netology_backup/elasticsearch/_restore?pretty -H 'Content-Type: application/json' -d'{"include_global_state":true}'
  curl -k -X GET -u elastic:yYn7p6ig5HOw_xHP2XZD https://localhost:9200/_cat/indices?v
  health status index  uuid                   pri rep docs.count docs.deleted store.size pri.store.size
  yellow open   test   4QJx727nRnejdwyYMIwmLw   1   0                                                  
  green  open   test-2 de4s707GQkuqu_S5uAxKtA   1   0          0            0       225b           225b
   ```
Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
