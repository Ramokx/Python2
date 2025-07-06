# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

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

    def add_link(self, from_port, to_port):
        keys_and_values = set(self.topology) | set(self.topology.values())
        if self.topology.get(from_port) == to_port or self.topology.get(to_port) == from_port:
            print("Такое соединение существует")
        elif from_port in keys_and_values or to_port in keys_and_values: # подковырка, нужно проверять еще и значениях, просто проверить, что они есть в ключах недостаточно, так как один из портов может быть просто в значениях
            print('Соединение с одним из портов существует')
        else:
            self.topology[from_port] = to_port

    def __add__(self, other):
        sum_topology = self.topology.copy()
        sum_topology.update(other.topology)
        return Topology(sum_topology)

    def __iter__(self):
        return iter(self.topology.items())


if __name__ == "__main__":
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
    top = Topology(topology_example)
    for link in top:
        print(link)