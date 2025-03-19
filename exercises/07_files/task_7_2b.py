# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
import sys

ignore = ["duplex", "alias", "configuration"]

with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'a') as output:
    for line in input:
        if not line.startswith('!') and ignore[0] not in line and ignore[1] not in line and ignore[2] not in line:
            output.write(line)