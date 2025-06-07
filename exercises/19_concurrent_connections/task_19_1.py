# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""


from concurrent.futures import ThreadPoolExecutor
import logging

import subprocess
import yaml


ip_list = ['8.8.8.8', '1.1.1.1', '30.04']

def ping_ip_address(ip):
    result = subprocess.run(['ping', '-c', '3', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    return result.returncode
    
        


def ping_ip_addresses(ip_list, limit=3):
    reachable, unreachable = [], []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip_address, ip_list)
        for ip, code in zip(ip_list, result):
            if code == 0:
                reachable.append(ip)
            else:
                unreachable.append(ip)
    return reachable, unreachable
        
if __name__ == "__main__":
    print(ping_ip_addresses(ip_list))
