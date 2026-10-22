# Err11. Прочитать два числа и вывести их частное. Обе ошибки — одним кортежем в except
# («Посчитать не удалось»); при успехе в else вывести частное с двумя знаками после точки.
try:
    a = float(input())
    b = float(input())
    result = a / b
except (ValueError, ZeroDivisionError):
    print("Посчитать не удалось")
else:
    print(f"{result:.2f}")
