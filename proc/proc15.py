# Proc15. Функция shift_left3(a, b, c) возвращает тройку после левого циклического сдвига:
# a переходит на место c, c — на место b, b — на место a. Сдвинуть два набора.
def shift_left3(a, b, c):
    return b, c, a


for i in range(2):
    a = float(input())
    b = float(input())
    c = float(input())
    a, b, c = shift_left3(a, b, c)
    print(a)
    print(b)
    print(c)
