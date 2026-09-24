# Найти длину окружности L и площадь круга S заданного радиуса R: 
# L = 2·π·R, S = π·R2. В качестве значения π использовать 3.14.

R = float(input())

pi = 3.14
length = 2 * pi * R

area = pi * (R**2)
print(length)
print(area)