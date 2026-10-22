# While12. Дано целое число N (> 1). 
# Вывести наибольшее целое K, для которого 1 + 2 + ... + K <= N, и саму эту сумму.
n = int(input())
total = 0
k = 0
while total + (k + 1) <= n:
    k += 1
    total += k
print(k)
print(total)
