# Dict9. Словари из N и M пар. Слить второй в первый через update. Вывести размер результата
# и значение ключа, который был в обоих словарях.
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
common = None
for key in second:           # ищем общий ключ ДО слияния
    if key in first and common is None:
        common = key
first.update(second)         # совпавший ключ получит значение второго словаря
print(len(first))
print(first[common])
