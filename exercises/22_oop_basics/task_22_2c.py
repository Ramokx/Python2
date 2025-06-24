# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
import telnetlib
from textfsm import clitable
import re

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
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
    
    def _error_in_command(self, command, output, strict):
        regex = r'(?P<command>.*)\n(.*\n)*?% (?P<error>.*)'
        template = 'При выполнении команды "{}" на устройстве {} возникла ошибка -> {}'
        
        error_match = re.search(regex, output.replace('\r\n', '\n'))
        if error_match:
            message = template.format(error_match.group('command'), self.ip, error_match.group('error'))
            if strict:
                raise ValueError(message)
            else:
                print(message)
                
    def send_config_commands(self, command, strict=True):
        output = ""
        commands = [command] if isinstance(command,  str) else command
        
        self._write_line('conf t')
        output += self.connection.read_until(b'(config)#', timeout=5).decode('utf-8')
        
        for cmd_i in commands:
            self._write_line(cmd_i)
            current_output = self.connection.read_until(b'(config)#', timeout=5).decode('utf-8')
            self._error_in_command(command, current_output, strict=strict)
            output += current_output
        
        self._write_line('end')
        output += self.connection.read_until(b'#', timeout=5).decode('utf-8')
        
        
        return output

r1_params = {'ip': '192.168.100.1','username': 'cisco','password': 'cisco','secret': 'cisco'}


if __name__ == "__main__":
    r1 = CiscoTelnet(**r1_params)
    commands = ['logging 0255.255.1', 'logging']
    print(r1.send_config_commands('logging 10.1.1.1'))
