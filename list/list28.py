# List28. Список из N строк и буква. Генератором вывести строки, начинающиеся с этой буквы.
n = int(input())
s = []
for i in range(n):
    s.append(input())
letter = input()
print([word for word in s if word[:1] == letter])
