# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import os, ipaddress
import subprocess


def ping_ip_addresses(list_ip):
    available_ip = []
    unknown_ip = []
    for ip in list_ip:
        result = subprocess.run(['ping', '-c', '3', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print(result.returncode)
        if result.returncode == 0:
            available_ip.append(ip)
        else:
            unknown_ip.append(ip)
    return (available_ip, unknown_ip)

