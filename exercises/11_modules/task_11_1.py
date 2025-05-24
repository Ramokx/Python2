# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент
вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое
файла в строку, а затем передать строку как аргумент функции (как передать вывод
команды показано в коде ниже).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

В словаре интерфейсы должны быть записаны без пробела между типом и именем.
То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt. При этом функция должна
работать и на других файлах (тест проверяет работу функции на выводе
из sh_cdp_n_sw1.txt и sh_cdp_n_r3.txt).

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def parse_cdp_neighbors(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде
    будет получен вывод команды с оборудования. Принимая как аргумент вывод
    команды, вместо имени файла, мы делаем функцию более универсальной: она может
    работать и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """
    neighbors_dict = dict()
    main_device = command_output[:command_output.find('>')].strip()
    commands = command_output.strip().replace('\n\n', '\n')
    for command in commands.split('\n')[4:]:
        command = command.split()
        neighbor = command[0]
        local_intf = command[1] + command[2]
        port_id = command[-2] + command[-1]
        neighbors_dict[(main_device, local_intf)] = (neighbor, port_id)
    return neighbors_dict

if __name__ == "__main__":
    with open("sh_cdp_n_r1.txt") as f:
        print(parse_cdp_neighbors(f.read()))







# def parse_cdp_neighbors(command_output):
#     """
#     Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
#     получен вывод команды с оборудования. Принимая как аргумент вывод команды,
#     вместо имени файла, мы делаем функцию более универсальной: она может работать
#     и с файлами и с выводом с оборудования.
#     Плюс учимся работать с таким выводом.
#     """
#     result = dict()
#     commands = [command.lstrip() for command in command_output.replace('\n\n','\n').strip().split('\n')]
#     root = commands[0][0:commands[0].find('>')] # название устройства на котором вводили команду
#     for command in commands[4:]:
#         command = command.split()
#         locan_intf = f"{command[1]}{command[2]}"
#         device_id, port_id = command[0], f"{command[-2]}{command[-1]}"
#         result[(root, locan_intf)] = (device_id, port_id)
#     return result
#
#
# if __name__ == "__main__":
#     with open("sh_cdp_n_sw1.txt") as f:
#         print(parse_cdp_neighbors(f.read()))
