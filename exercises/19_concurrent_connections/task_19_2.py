# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
from concurrent.futures import ThreadPoolExecutor
import os
import netmiko
from itertools import repeat
import yaml

#logging.basicConfig(format='%(threadName)s %(name)s %(levelname)s: %(message)s',level=logging.INFO)

def send_show(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        device = ssh.find_prompt()
        result = ssh.send_command(command, strip_command=False)
        return f"{device}{result}\n"


def send_show_command_to_devices(devices, command, filename, limit=3):
    with open(filename, 'w') as output_file:
        with ThreadPoolExecutor(max_workers=limit) as executor:
            result = executor.map(send_show, devices, repeat(command))
            for output in result:
                #output_file.write(device)
                output_file.write(output)
                #output_file.write('\n')
                
devices = [{'device_type': 'cisco_ios',
  'host': '192.168.100.1',
  'username': 'cisco',
  'password': 'cisco',
  'secret': 'cisco',
  'timeout': 10}]


if __name__ == "__main__":
    #with open('devices.yaml', 'r') as read_file:
        #data = yaml.safe_load(read_file)
    send_show_command_to_devices(devices, 'sh ip int br | include up +up', 'test.txt')
