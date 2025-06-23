# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Соединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Соединение с одним из портов существует


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

    def add_link(self, from_port, to_port):
        keys_and_values = set(self.topology) | set(self.topology.values())
        if self.topology.get(from_port) == to_port or self.topology.get(to_port) == from_port:
            print("Такое соединение существует")
        elif from_port in keys_and_values or to_port in keys_and_values: # подковырка, нужно проверять еще и значениях, просто проверить, что они есть в ключах недостаточно, так как один из портов может быть просто в значениях
            print('Соединение с одним из портов существует')
        else:
            self.topology[from_port] = to_port


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
    print(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    print(top.topology)
    top.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    top.add_link(('R1', 'Eth0/4'), ('R0', 'Eth0/0'))
    top.add_link(("R5", "Eth0/0"), ('R10', 'Eth0/0'))
    print(top.topology)
