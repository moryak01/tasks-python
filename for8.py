# For8. Даны два целых числа A и B (A < B). Найти произведение всех целых чисел от A до B включительно.
a = int(input())
b = int(input())
product = 1   # произведение начинается с единицы
for i in range(a, b + 1):
    product *= i
print(product)
