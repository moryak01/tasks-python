# Proc2. Функция power_a234(a) возвращает вторую, третью и четвёртую степени числа a.
# Найти три степени пяти данных чисел.
def power_a234(a):
    return a ** 2, a ** 3, a ** 4


for i in range(5):
    a = float(input('введите число - '))
    p2, p3, p4 = power_a234(a)
    print(p2)
    print(p3)
    print(p4)
