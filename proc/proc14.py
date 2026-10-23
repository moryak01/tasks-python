# Proc14. Функция shift_right3(a, b, c) возвращает тройку после правого циклического сдвига:
# a переходит на место b, b — на место c, c — на место a. Сдвинуть два набора.
def shift_right3(a, b, c):
    return c, a, b


for i in range(2):
    a = float(input())
    b = float(input())
    c = float(input())
    a, b, c = shift_right3(a, b, c)
    print(a)
    print(b)
    print(c)
