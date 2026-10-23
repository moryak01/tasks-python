# Dict15. Словари из N и M пар. Добавить в первый пары второго без update: только ключи, которых нет.
# Совпавшие ключи игнорируются. Вывести размер и число проигнорированных.
n = int(input())
first = {}
for i in range(n):
    key = input()
    value = int(input())
    first[key] = value
m = int(input())
second = {}
for i in range(m):
    key = input()
    value = int(input())
    second[key] = value
ignored = 0
for key, value in second.items():
    if key in first:
        ignored += 1
    else:
        first[key] = value
print(len(first))
print(ignored)
