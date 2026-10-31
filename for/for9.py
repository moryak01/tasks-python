# For9. Даны два целых числа A и B (A < B). Найти сумму квадратов всех целых чисел от A до B включительно.
a = int(input())
b = int(input())
total = 0
for i in range(a, b + 1):
    total += i * i
print(total)
