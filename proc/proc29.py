# Proc29. Функция digit_count(k) возвращает количество цифр k (> 0). Найти количество цифр пяти чисел.
def digit_count(k):
    count = 0
    while k > 0:
        count += 1
        k //= 10
    return count


for i in range(5):
    print(digit_count(int(input())))
