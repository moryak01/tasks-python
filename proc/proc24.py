# Proc24. Функция even(k) возвращает True для чётного k. Найти количество чётных в наборе из 10 чисел.
def even(k):
    return k % 2 == 0


count = 0
for i in range(10):
    if even(int(input())):
        count += 1
print(count)
