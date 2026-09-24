#  Даны два ненулевых числа. 
# Найти сумму, разность, произведение и частное их модулей.

a = float(input())
b = float(input())
absa = abs(a)
absb = abs(b)

sum_abs = absa+absb
diff_abs = absa-absb
prod_abs =  absa*absb
quot_abs = absa/absb

print(sum_abs)
print(diff_abs)
print(prod_abs)
print(quot_abs)