# List17. Список A из N чисел. Вывести элементы по возрастанию (sorted), затем исходный список без изменений.
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
print(sorted(a))
print(a)
