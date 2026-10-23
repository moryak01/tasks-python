# Dict2. Словарь из N пар. Дан ключ K: вывести его значение, если K есть, иначе «нет такого ключа».
n = int(input())
d = {}
for i in range(n):
    key = input()
    value = int(input())
    d[key] = value
k = input()
if k in d:
    print(d[k])
else:
    print("нет такого ключа")
