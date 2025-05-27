# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""

import re

def get_ints_without_description(filename):
    result = []
    with open(filename, 'r') as file:
        data = re.finditer(r'interface (?P<intf>\S+)\n(?P<all>(.+\n)+?)!', file.read())
        for match in data:
            if 'description' not in match.group('all'):
                result.append(match.group('intf'))

    # вариант с построчным считыванием файла
        # for line in file:
        #     flag_of_descrition = False
        #     if line.startswith('interface'):
        #         interface = re.search(r'interface (\S+)', line).group(1)
        #     elif line.startswith(' description'):
        #         flag_of_descrition = True
        #     elif line.startswith('!') and flag_of_descrition is False:
        #         result.append(interface)

    return result

if __name__ == "__main__":
    print(get_ints_without_description('config_r1.txt'))
