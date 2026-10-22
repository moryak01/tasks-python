# List25. Список A из N различных чисел. Вывести второй по величине элемент.
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
ordered = sorted(a, reverse=True)
print(ordered[1])
