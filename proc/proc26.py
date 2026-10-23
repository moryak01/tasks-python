# Proc26. Функция is_power5(k) возвращает True, если k (> 0) — степень пятёрки.
# Найти количество таких в наборе из 10 чисел.
def is_power5(k):
    while k % 5 == 0:
        k //= 5
    return k == 1


count = 0
for i in range(10):
    if is_power5(int(input())):
        count += 1
print(count)
