# List26. Список A из N чисел. Генератором вывести элементы, большие среднего, и само среднее.
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
average = sum(a) / len(a)
print([x for x in a if x > average])
print(average)
