# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re
import json
from re import finditer


def parse_sh_cdp_neighbors(command_output):
    result = {}
    command_output = command_output.strip()
    #for line in command_output:
    root = re.search(r'^(?P<root>.+)>', command_output).group('root')
    #print(command_output)
    matches = finditer(r'(?P<neighb>\S+) +(?P<localintf>.+?) {2,} \d+\s+.+ (?P<portid>\w+ .+)', command_output)
    for match in matches:
        neighb, local_intf, port_id = match.groups()
        result.setdefault(root, {}).update({local_intf: {neighb: port_id}})
    return result

if __name__ == "__main__":
    with open('sh_cdp_n_r1.txt', 'r') as file:
        print(parse_sh_cdp_neighbors(file.read()))
