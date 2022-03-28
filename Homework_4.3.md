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
      "ip": "7.1.7.5"
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
```python
#!/usr/bin/env python
import sys
import json
import yaml

file_data={}
def file_write(self):
    FILE_NAME = ("1{0}.{1}".format((filename.split('.'))[0], 'json'))
    with open(FILE_NAME, "w") as write_filej:
        json.dump(self, write_filej)
    FILE_NAME = ("1{0}.{1}".format((filename.split('.'))[0], 'yaml'))
    with open(FILE_NAME, "w") as write_filey:
        yaml.dump(self, write_filey)


def is_exist_file(self):
    try:
        open(self)
        if TYPE_FILE != "yaml" and TYPE_FILE != "json":
            exit(1)
    except IOError as err:
        print(err)
        exit(1)
    return True


def is_json_file(self):
    try:
        with open(self, "r") as read_file:
            global file_data
            file_data = json.load(read_file)
        return True,file_data
    except json.decoder.JSONDecodeError as err:
        return False, err

def is_yaml_file(self):
    try:
        with open(self, "r") as write_file:
            global file_data
            file_data = yaml.safe_load(write_file)
            return True, file_data
    except yaml.scanner.ScannerError  as err:
        return False, err
    except yaml.parser.ParserError as err:
        return False, err
if len(sys.argv) > 1 :
    filename=sys.argv[1]
    TYPE_FILE = (filename.split('.'))[-1]
    if is_exist_file(filename):
        if is_yaml_file(filename)[0] is False and is_json_file(filename)[0] is False:
            if TYPE_FILE == "yaml":
                    print(is_yaml_file(filename)[1])
                    exit(0)
            if TYPE_FILE == "json":
                    print(is_json_file(filename)[1])
                    exit(0)
    if TYPE_FILE == "yaml":
        if is_json_file(filename)[0] is False:
            print(is_yaml_file(filename)[1])
        else:
            is_yaml_file(filename)
            file_write(file_data)
    if TYPE_FILE == "json":
        if is_yaml_file(filename)[0] is False:
            print(is_json_file(filename)[1])
        else:
            is_json_file(filename)
            file_write(file_data)
else:
    print('missing 1 required positional argument')



```
---

### Как сдавать задания

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---