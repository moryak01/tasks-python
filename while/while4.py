# While4. Дано целое число N (> 0). Если оно является степенью числа 3, вывести True, иначе False.
n = int(input())
rest = n
while rest % 3 == 0:
    rest //= 3
print(rest == 1)
