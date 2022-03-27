# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
	```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
	```
  Нужно найти и исправить все ошибки, которые допускает наш сервис
```json
{"info": "Sample JSON output from our service",
 "elements": [
     {"name": "first",
      "type": "server",
      "ip": 7175
      },
     {"name": "second",
      "type": "proxy",
      "ip" : "71.78.22.43"
      }
    ]
}


```
2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.
```python
#!/usr/bin/env python
import socket as s
import time as t
import datetime as dt
import json
import yaml

###############################################################
srv={}
def_file_tyope='json'
filename="host_file1"

host = {'drive.google.com':'0.0.0.0',
             'mail.google.com':'0.0.0.0',
             'google.com':'0.0.0.0'}
###############################################################

def file_host_write(host_data,FILENAME=filename):
    FILE = ("{0}.{1}".format(FILENAME, 'json'))
    with open(FILE, "w") as write_filej:
        json.dump(host_data, write_filej)
    FILE = ("{0}.{1}".format(FILENAME, 'yaml'))
    with open(FILE, "w") as write_filey:
        yaml.dump(host_data, write_filey)




def file_host(host, FILETYPE=def_file_tyope, FILENAME=filename): # если фаил есть взять данные из необходимого
        FILE = ("{0}.{1}".format(FILENAME,FILETYPE))
        data = host
        try:
            if FILETYPE == 'json':
                open(FILE)
                with open(FILE, "r") as write_file:
                    data = json.load(write_file)
            if FILETYPE == 'yaml':
                open(FILE)
                with open(FILE, "r") as write_file:
                    data = yaml.safe_load(write_file)
        except IOError:
            file_host_write(data)
        global srv
        file_host_write(data)
        srv = data

def host_ip(self):
    ip = s.gethostbyname(self)
    if srv[self] == ip:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' ' + self +' '+ip )
    if srv[self] != ip:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +' [ERROR] ' + self +' IP mistmatch: '+srv[self]+' '+ip)
        srv[self] = ip
        file_host_write(srv)
c = 0
file_host(host)
while c != 3:
    for i in srv:
        host_ip(i)
        t.sleep(1)
    c += 1



```
## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

---

### Как сдавать задания

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---