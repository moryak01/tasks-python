# While5. Дано целое число N (> 0), являющееся степенью числа 2: N = 2^K. Найти показатель K.
n = int(input())
rest = n
k = 0
while rest > 1:
    rest //= 2
    k += 1
print(k)
