# String4. Дано N (1 <= N <= 26). Вывести строку из N первых заглавных латинских букв.
n = int(input())
print("".join(chr(ord("A") + i) for i in range(n)))
