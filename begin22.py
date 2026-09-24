# Begin22. Поменять местами содержимое переменных A и B.

a = float(input())
b = float(input())

temp = a
a = b
b = temp

print(a)
print(b)