# List22. Список A из N чисел и число D. Генератором вывести элементы, умноженные на D, и количество элементов, равных D.
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
d = int(input())
print([x * d for x in a])
print(len([x for x in a if x == d]))
