# Proc5. Функция rect_ps(x1, y1, x2, y2) возвращает периметр и площадь прямоугольника со сторонами,
# параллельными осям, по противоположным вершинам. Найти P и S трёх прямоугольников.
def rect_ps(x1, y1, x2, y2):
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return 2 * (width + height), width * height


for i in range(3):
    x1 = float(input())
    y1 = float(input())
    x2 = float(input())
    y2 = float(input())
    p, s = rect_ps(x1, y1, x2, y2)
    print(p)
    print(s)
