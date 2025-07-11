# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации
на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
"""

import yaml
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import paramiko

def send_show_command(device, command):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print (error)
        
if __name__ == "__main__":
    command = "sh ip int br" 
    with open("devices.yaml", 'r') as f:
        devices = yaml.safe_load(f)
        
    for device in devices:
        print(send_show_command(device, command))
