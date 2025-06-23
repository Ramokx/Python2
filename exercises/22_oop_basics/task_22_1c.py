# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

"""

class Topology:
    def __init__(self, topology_dict):
        self.topology = {}
        self.topology = self._normalize(topology_dict)


    def _normalize(self, topology_dict):
        for key, value in topology_dict.items():
            if key not in self.topology.keys() and key not in self.topology.values():
                self.topology[key] = value
        return self.topology

    def delete_link(self, from_port, to_port):
        if self.topology.get(from_port) == to_port:
            del self.topology[from_port]
        elif self.topology.get(to_port) == from_port:
            del self.topology[to_port]
        else:
            print("Такого соединения нет")

    def delete_node(self, device):
        tmp = {}
        for key, value in self.topology.items():
            if device in key or device in value:
                for key, value in self.topology.items():
                    if key[0] != device and value[0] != device:
                        tmp[key] = value
                self.topology = tmp
                break
        else:
            print("Такого устройства нет")


        # вариант с итерацией по списку из ключей и значений словаря
        # original_length = len(self.topology)
        # for key, value in list(self.topology.items()):
        #     if key[0] == device:
        #         del self.topology[key]
        #     elif value[0] == device:
        #         del self.topology[key]
        # if original_length == len(self.topology):
        #     print('Такого устройства нет')

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

if __name__ == "__main__":
    top = Topology(topology_example)
    top.delete_node('SW1')
    print(top.topology)
    top.delete_node('SW1')