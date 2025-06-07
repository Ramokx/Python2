# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""
import yaml
from concurrent.futures import ThreadPoolExecutor
import netmiko

#commands = {
    #"192.168.100.3": ["sh ip int br", "sh ip route | ex -"],
    #"192.168.100.1": ["sh ip int br", "sh int desc"],
    #"192.168.100.2": ["sh int desc"],
#}

#devices = [{'device_type': 'cisco_ios',
  #'host': '192.168.100.1',
  #'username': 'cisco',
  #'password': 'cisco',
  #'secret': 'cisco',
  #'timeout': 10}]
commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

def send_command(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()
        output = ssh.send_command(command)
        return f"{prompt}{command}\n{output}\n"

def send_config(device, config):
    output = ""
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()
        for command in config:
            result = ssh.send_config_set(config, strip_command=False)
            output += f"{prompt}{result}\n"
        return output
        
            
def send_commands_to_devices(devices, filename, *, show=None, config=None, limit=3):
    future_list = []
    if show and config:
        raise ValueError("Можно передавать только один аргумент show или config")
        
    command = show if show else config
    function = send_command if show else send_config
    with ThreadPoolExecutor(max_workers=limit) as executor:
        for device in devices:
            result = executor.submit(function, device, command)
            future_list.append(result)
        with open(filename, 'w') as output_file:
            for f in future_list:
                output_file.write(f.result())
    #elif show:
        #with ThreadPoolExecutor(max_workers=limit) as executor:
            #for device in devices:
                #result = executor.submit(send_command, device, show)
                #future_list.append(result)
            #with open(filename, 'w') as output_file:
                #for f in future_list:
                    #output_file.write(f.result())
    #elif config:
        #with ThreadPoolExecutor(max_workers=limit) as executor:
            #for device in devices:
                #result = executor.submit(send_config, device, config)
                #future_list.append(result)
            #with open(filename, 'w') as output_file:
                #for f in future_list:
                    #print(f)
                    #output_file.write(f.result())
        
                    
if __name__ == "__main__":
    with open('devices.yaml', 'r') as input:
        data = yaml.safe_load(input)

    send_commands_to_devices(data, 'result.txt', show='sh clock')
