# Proc8. Функция add_right_digit(d, k) возвращает число k с приписанной справа цифрой d (0-9).
# Приписать к данному K справа D1 и D2, печатая результат каждого шага.
def add_right_digit(d, k):
    return k * 10 + d


k = int(input())
d1 = int(input())
d2 = int(input())
k = add_right_digit(d1, k)
print(k)
k = add_right_digit(d2, k)
print(k)
