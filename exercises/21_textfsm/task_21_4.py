# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

from textfsm import clitable
from netmiko import ConnectHandler
import yaml


def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    with ConnectHandler(**device_dict) as connect:
        connect.enable()
        command_output = connect.send_command(command)
    attributes_dict = {'Command': command, 'Vendor': device_dict['device_type']}
    cli_table = clitable.CliTable(index, templates_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    data_rows = [list(row) for row in cli_table]
    header = list(cli_table.header)
    result = [{key: value for key, value in zip(header, value)} for value in data_rows]
    return result 
    

command = 'sh ip int br'

if __name__ == "__main__":
    
    with open('devices.yaml', 'r') as device_file:
        devices = yaml.safe_load(device_file)
    for device in devices: 
        print(send_and_parse_show_command(device, 'sh ip int br', 'templates'))
