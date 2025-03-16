# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]
my_dict = {'access': access_template, 'trunk': trunk_template}
vlan_template = {'access': access_template[1], 'trunk': trunk_template[-1]}
questions = {'access': "Введите номер VLAN: ", 'trunk': "Введите разрешенные VLANы: "}
mode = input("Введите режим работы интерфейса(access/trunk): ")
type_number = input("Введите тип и номер интерфейса: ")
vlan_number = input(questions[mode])

vlan_template = {'access': access_template[1].format(vlan_number), 'trunk': trunk_template[-1].format(vlan_number)}
my_dict['access'][1] = vlan_template['access']
my_dict['trunk'][-1] = vlan_template['trunk']


print(f"interface {type_number}")
print(*my_dict[mode], sep='\n')