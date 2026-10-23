# Proc25. Функция is_square(k) возвращает True, если k (> 0) — квадрат целого числа.
# Найти количество квадратов в наборе из 10 чисел.
def is_square(k):
    r = int(k ** 0.5)
    return r * r == k or (r + 1) * (r + 1) == k


count = 0

for i in range(10):
    if is_square(int(input())):
        count += 1
print(count)
