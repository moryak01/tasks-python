# Известно, что X кг конфет стоит A рублей. 
# Определить, сколько стоит 1 кг и Y кг этих же конфет.

x = float(input('введите кол-во конфет X в кг - '))
a = float(input('введите стоимость A конфет в рублях - '))
y = float(input('введите кол-во конфет Y для расчета результата - '))

price_per_kg= a/x

total_for_y = price_per_kg*y

print(price_per_kg)
print(total_for_y)