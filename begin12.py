# Даны катеты прямоугольного треугольника a и b. 
# Найти его гипотенузу c и периметр P: c = √(a2 + b2), P = a + b + c.
import math

a = float(input())
b = float(input())

c = math.sqrt(a*a + b*b)
P = a+b+c

print(c)
print(P)