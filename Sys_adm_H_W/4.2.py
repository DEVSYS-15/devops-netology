
#!/usr/bin/env python
import sys
import json
import yaml

#filename="host_file1.json"

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



