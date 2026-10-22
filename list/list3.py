A = [1, 2, 3, 4, 5]
total_sum = sum(A)

even_product = 1
for i in range(0, len(A), 2):
    even_product *= A[i]

print(f"Сумма всех элементов: {total_sum}")
print(f"Произведение элементов с чётными индексами: {even_product}")