# For15. Дано вещественное число A и целое число N (> 0). Найти A в степени N: A^N = A · A · ... · A
# (число A перемножается N раз). Возведение в степень не используем.
a = float(input())
n = int(input())
result = 1.0
for _ in range(n):
    result *= a
print(result)
