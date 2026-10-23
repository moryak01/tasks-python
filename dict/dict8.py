# Dict8. Словарь из N пар и число V. Вывести True, если V встречается среди значений, и False иначе.
n = int(input())
d = {}
for i in range(n):
    key = input()
    value = int(input())
    d[key] = value
v = int(input())
print(v in d.values())
