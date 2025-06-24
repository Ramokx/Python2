# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'
c
"""
import telnetlib
from textfsm import clitable


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.connection = telnetlib.Telnet(ip)
        self.connection.read_until(b'Username')
        self._write_line(username)
        self.connection.read_until(b'Password')
        self._write_line(password)
        self._write_line('enable')
        self.connection.read_until(b'Password')
        self._write_line(secret)
        self.connection.read_until(b'#')
        self._write_line('terminal length 0')
        self.connection.read_until(b"#", timeout=5)
        
        
    def _write_line(self, line):
        self.connection.write(line.encode('utf-8') + b'\n')
        
        
    def send_show_command(self, show, parse=True, templates='templates', index='index'):
        self._write_line(show)
        command_output = self.connection.read_until(b'#', timeout=5).decode('utf-8').replace('\r\n', '\n')
        if parse:
            #output = {}
            self._write_line(show)
            command_output = self.connection.read_until(b'#', timeout=5).decode('utf-8').replace('\r\n', '\n')
            attributes_dict = {'Command': show, 'Vendor': 'cisco_ios'}
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(command_output, attributes_dict)
            data_rows = [list(row) for row in cli_table]
            header = list(cli_table.header)
            output = [{key: value for key, value in zip(header, value)} for value in data_rows]
        else:
            output = command_output
        return output
    
    def send_config_commands(self, command):
        output = ""
        commands = [command] if isinstance(command,  str) else command
        
        self._write_line('conf t')
        output += self.connection.read_until(b'(config)#', timeout=5).decode('utf-8')
        
        for cmd_i in commands:
            self._write_line(cmd_i)
            output += self.connection.read_until(b'(config)#', timeout=5).decode('utf-8')
        
        self._write_line('end')
        output += self.connection.read_until(b'#', timeout=5).decode('utf-8')
        
        
        return output

r1_params = {'ip': '192.168.100.1','username': 'cisco','password': 'cisco','secret': 'cisco'}


if __name__ == "__main__":
    r1 = CiscoTelnet(**r1_params)
    print(r1.send_config_commands('logging 10.1.1.1'))
