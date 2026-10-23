# Dict14. Словарь из N пар и число V. Удалить все пары со значением меньше V (не меняя словарь во время перебора).
n = int(input())
d = {}
for i in range(n):
    key = input()
    value = int(input())
    d[key] = value
v = int(input())
for key in list(d):          # снимок ключей: безопасно удалять внутри цикла
    if d[key] < v:
        del d[key]
print(len(d))
