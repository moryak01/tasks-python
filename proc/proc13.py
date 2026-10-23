# Proc13. Функция sort_dec3(a, b, c) возвращает три значения по убыванию. Упорядочить два набора.
def sort_dec3(a, b, c):
    if a < b:
        a, b = b, a
    if b < c:
        b, c = c, b
    if a < b:
        a, b = b, a
    return a, b, c


for i in range(2):
    a = float(input())
    b = float(input())
    c = float(input())
    x, y, z = sort_dec3(a, b, c)
    print(x)
    print(y)
    print(z)
