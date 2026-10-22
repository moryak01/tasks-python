# List30. Список из N строк. Генератором вывести список длин строк и суммарную длину всех строк.
n = int(input())
s = []
for i in range(n):
    s.append(input())
lengths = [len(word) for word in s]
print(lengths)
print(sum(lengths))
