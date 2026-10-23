# Proc20. Функция triangle_p(a, h) возвращает периметр равнобедренного треугольника по основанию a
# и высоте h к основанию (боковая сторона b² = (a/2)² + h²). Найти периметры трёх треугольников.
import math


def triangle_p(a, h):
    b = math.sqrt((a / 2) ** 2 + h ** 2)
    return a + 2 * b


for i in range(3):
    a = float(input())
    h = float(input())
    print(triangle_p(a, h))
