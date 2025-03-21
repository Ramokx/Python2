# -*- coding: utf-8 -*-
"""
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
- ключи: имена интерфейсов, вида 'FastEthernet0/1'
- значения: список команд, который надо
  выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

Пример итогового словаря, который должна возвращать функция (перевод строки
после каждого элемента сделан для удобства чтения):
{
    "FastEthernet0/1": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 10,20,30",
    ],
    "FastEthernet0/2": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 11,30",
    ],
    "FastEthernet0/4": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 17",
    ],
}

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}


def generate_trunk_config(intf_vlan_mapping, trunk_template):
    """
        intf_vlan_mapping - словарь с соответствием интерфейс-VLAN такого вида:
            {'FastEthernet0/12':10,
             'FastEthernet0/14':11,
             'FastEthernet0/16':17}
        trunk_template - список команд для порта в режиме trunk

        Возвращает список всех портов в режиме trunk с конфигурацией на основе шаблона
    """
    trunk_config = dict()
    for intf, vlan in intf_vlan_mapping.items():
        trunk_config[intf] = []
        for command in trunk_template:
            if command.endswith("allowed vlan"):
                trunk_config[intf].append(f"{command} {','.join([str(vl) for vl in vlan])}")
            else:
                trunk_config[intf].append(command)
    return trunk_config