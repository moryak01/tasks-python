# List23. Список A из N чисел. Вывести элементы в порядке убывания модуля.
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
print(sorted(a, key=abs, reverse=True))
