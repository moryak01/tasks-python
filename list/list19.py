# List19. Список из N строк. Вывести строки по возрастанию длины и отдельно самую длинную.
n = int(input())
s = []
for i in range(n):
    s.append(input())
print(sorted(s, key=len))
print(max(s, key=len))
