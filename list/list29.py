# List29. Список A из N чисел и число K. Вывести K наибольших элементов в порядке убывания (сортировка + срез).
n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
k = int(input())
print(sorted(a, reverse=True)[:k])
