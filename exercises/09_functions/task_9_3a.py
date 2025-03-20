# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    trunk = dict()
    access = dict()
    with open(config_filename, 'r') as config:
        for line in config:
            line = line.strip()
            if line.startswith('interface'):
                intf = line.split()[-1]
            if line.startswith('switchport trunk allowed'):
                vlan = line.split()[-1].split(',')
                trunk[intf] = [int(vl) for vl in vlan]
            elif line.startswith('switchport access'):
                vlan = line.split()[-1]
                access[intf] = int(vlan)
            elif line == 'switchport mode access':
                access[intf] = 1
    return (access, trunk)
