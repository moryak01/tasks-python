# String15. Дана строка. Подсчитать общее количество строчных латинских и русских букв в ней.
latin = "".join(chr(ord("a") + i) for i in range(26))
russian = "".join(chr(ord("а") + i) for i in range(32)) + "ё"   # «ё» стоит в таблице отдельно
alphabet = latin + russian
s = input()
count = 0
for ch in s:
    if ch in alphabet:
        count += 1
print(count)
