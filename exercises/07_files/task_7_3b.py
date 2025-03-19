# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
vlan_number = int(input("Enter VLAN number:"))
template = "{:<9}{}{:>11}"

with open('CAM_table.txt', 'r') as file:
    for line in file:
        line = line.strip().split()
        if line and line[0].isdigit():
            vlan, mac, interface = int(line[0]), line[1], line[-1]
            if vlan_number == vlan:
                print(template.format(vlan, mac, interface))
