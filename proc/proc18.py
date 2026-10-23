# Proc18. Функция circle_s(r) возвращает площадь круга радиуса r (π = 3.14). Найти площади трёх кругов.
def circle_s(r):
    return 3.14 * r * r


for i in range(3):
    r = float(input())
    print(circle_s(r))
