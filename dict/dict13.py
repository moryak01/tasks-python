# Dict13. Словарь из N троек: название, цена, количество (значение — список из двух чисел).
# Вывести суммарную стоимость склада и название самого дорогого по стоимости предмета.
n = int(input())
d = {}
for i in range(n):
    name = input()
    price = int(input())
    qty = int(input())
    d[name] = [price, qty]
total = 0
best = None
best_cost = 0
for name, pair in d.items():
    price, qty = pair
    cost = price * qty
    total += cost
    if best is None or cost > best_cost:
        best = name
        best_cost = cost
print(total)
print(best)
