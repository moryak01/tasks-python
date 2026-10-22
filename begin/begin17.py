# Даны три точки A, B, C на числовой оси. 
# Найти длины отрезков AC и BC и их сумму.

a = float(input())
b = float(input())
c = float(input())

ac = abs(c - a)
bc = abs(c - b)

print(ac, bc)