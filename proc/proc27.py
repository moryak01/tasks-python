# Proc27. Функция is_power_n(k, n) возвращает True, если k (> 0) — степень n (> 1).
# Даны n и набор из 10 чисел: найти количество степеней.
def is_power_n(k, n):
    while k % n == 0:
        k //= n
    return k == 1


n = int(input())
count = 0
for i in range(10):
    if is_power_n(int(input()), n):
        count += 1
print(count)
