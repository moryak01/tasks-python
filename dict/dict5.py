# Dict5. Словарь из N пар. Удалить ключ K через pop с default. Вывести размер после удаления.
n = int(input())
d = {}
for i in range(n):
    key = input()
    value = int(input())
    d[key] = value
k = input()
d.pop(k, None)    # нет ключа — словарь не меняется, ошибки нет
print(len(d))
