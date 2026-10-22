# While13. Дано число A (> 1). Вывести наименьшее целое K, для которого 1 + 1/2 + ... + 1/K > A,
# и саму эту сумму.
a = float(input())
total = 0.0
k = 0
while total <= a:
    k += 1
    total += 1 / k
print(k)
print(total)
