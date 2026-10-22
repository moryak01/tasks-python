# List21. Список A из N чисел. Генератором с фильтром вывести положительные элементы и их количество.
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
positive = [x for x in a if x > 0]
print(positive)
print(len(positive))
