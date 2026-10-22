# For2. Даны два целых числа A и B (A < B). Вывести в порядке возрастания все целые
# числа между A и B (включая A и B), а также количество N этих чисел.
a = int(input('Введите число a: '))
b = int(input('Введите число b: '))
count = 0
for i in range(a, b + 1):
    print(i)
    count += 1
print(count)
