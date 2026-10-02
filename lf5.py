a = int(input(''))
b = int(input(''))
c = int(input(''))

count = 0

for num in [a,b,c]:
    match num:
        case _ if num < 0:
            count += 1
            pass
        case _:
            pass
print(f'количество отрицательных чисел - {count}')