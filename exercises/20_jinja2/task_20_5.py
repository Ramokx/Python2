# -*- coding: utf-8 -*-
"""
Задание 20.5

Создать шаблоны templates/gre_ipsec_vpn_1.txt и templates/gre_ipsec_vpn_2.txt,
которые генерируют конфигурацию IPsec over GRE между двумя маршрутизаторами.

Шаблон templates/gre_ipsec_vpn_1.txt создает конфигурацию для одной стороны туннеля,
а templates/gre_ipsec_vpn_2.txt - для второй.

Примеры итоговой конфигурации, которая должна создаваться на основе шаблонов в файлах:
cisco_vpn_1.txt и cisco_vpn_2.txt.

Шаблоны надо создавать вручную, скопировав части конфига в соответствующие шаблоны.

Создать функцию create_vpn_config, которая использует эти шаблоны
для генерации конфигурации VPN на основе данных в словаре data.

Параметры функции:
* template1 - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* template2 - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна возвращать кортеж с двумя конфигурациями (строки),
которые получены на основе шаблонов.

Примеры конфигураций VPN, которые должна возвращать функция create_vpn_config в файлах
cisco_vpn_1.txt и cisco_vpn_2.txt.
"""
from jinja2 import Environment, FileSystemLoader
import os

data = {
    "tun_num": 10,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}


def create_vpn_config(template1, template2, data_dict):
    template_dir1, template_file1 = os.path.split(template1)
    template_dir2, template_file2 = os.path.split(template2)
    
    env1 = Environment(loader=FileSystemLoader(template_dir1), trim_blocks=True, lstrip_blocks=True)
    temp1 = env1.get_template(template_file1)
    
    env2 = Environment(loader=FileSystemLoader(template_dir2), trim_blocks=True, lstrip_blocks=True)
    temp2 = env2.get_template(template_file2)
    
    return temp1.render(data_dict), temp2.render(data_dict)
    
if __name__ == "__main__":
    print(create_vpn_config("templates/gre_ipsec_vpn_1.txt", "templates/gre_ipsec_vpn_2.txt", data))
