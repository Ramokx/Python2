# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

while True:
    ip = input("Введите ip адрес: ")
    octs = ip.split('.')
    correct_ip = True
    if len(octs) == 4:
        for oct in octs:
            if not (oct.isdigit() and 0 <= int(oct) <= 255):
                correct_ip = False
    else:
        correct_ip = False
    if correct_ip:
        break
    print('Неправильный IP-адрес')

if 1 <= int(octs[0]) <= 223:
    print('unicast')
elif 224 <= int(octs[0]) <= 239:
    print('multicast')
elif ip == "255.255.255.255":
    print("local broadcast")
elif ip == "0.0.0.0":
    print("unassigned")
else:
    print('unused')