# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
from task_20_1 import generate_config
import yaml
import netmiko
import re
from task_20_5 import create_vpn_config

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}




def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    print(vpn_data_dict)
    with netmiko.ConnectHandler(**src_device_params) as src, netmiko.ConnectHandler(**dst_device_params) as dst:
        src.enable()
        dst.enable()
        
        interfaces1 = src.send_command("show ip interface brief | include Tunnel")
        interfaces2 = dst.send_command("show ip interface brief | include Tunnel")
        
        tunnel_nums = [int(num) for num in re.findall(r'Tunnel(\d+)', interfaces1 + interfaces2)]
        print(tunnel_nums)
        
        if not tunnel_nums:
            tunnel = 0
        else:
            diff = set(range(min(tunnel_nums), max(tunnel_nums) + 1)) - set(tunnel_nums)
            if diff:
                tunnel = min(diff)
            else:
                tunnel = max(tunnel_nums) + 1
        print(tunnel)
        vpn_data_dict["tun_num"] = tunnel
        
        
        vpn_config1, vpn_config2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
        result1 = src.send_config_set(vpn_config1.split('\n'))
        result2 = dst.send_config_set(vpn_config2.split('\n'))
        
        return result1, result2
        
    

if __name__ == "__main__":
    with open("devices.yaml", 'r') as devices_file:
        data_devices = yaml.safe_load(devices_file)
    device1, device2 = data_devices[0], data_devices[1]
    print(configure_vpn(device1, device2, "templates/gre_ipsec_vpn_1.txt", "templates/gre_ipsec_vpn_2.txt", data))
        
