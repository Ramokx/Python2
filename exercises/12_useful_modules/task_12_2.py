# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""
import ipaddress
def convert_ranges_to_ip_list(list_ip):
    '''
    конвертирует список IP-адресов в разных форматах в список,
    где каждый IP-адрес указан отдельно
    '''
    new_ip_list = []
    for ip in list_ip:
        if ('-') in ip: # если в айпи есть дефис - значит диапазон
            ip = ip.split('-') # делим на первый и последний айпи диапазона
            first_ip = ipaddress.ip_address(ip[0])
            last_ip = '.'.join(ip[0].split('.')[:3]) + '.' + ip[1].split('.')[-1] # собираем айпи из 3 октетов первого в диапазоне и последнего октета последнего айпи( не важно как указан диапазон)
            last_ip = ipaddress.ip_address(last_ip)
            while first_ip <= last_ip:
                new_ip_list.append(str(first_ip))
                first_ip += 1
        else:
            new_ip_list.append(ip)
    return new_ip_list

if __name__ == '__main__':
    print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']))