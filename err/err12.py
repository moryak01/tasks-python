# Err12. Прочитать целое число. При ошибке вывести текст исключения и его тип отдельными строками.
# При успехе вывести само число.
try:
    number = int(input())
except ValueError as e:
    print(e)
    print(type(e))
else:
    print(number)
