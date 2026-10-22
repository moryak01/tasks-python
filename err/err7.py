# Err7. Читать ввод, пока не будет введено целое число.
# Некорректный ввод не считается и не роняет программу.
while True:
    try:
        number = int(input())
        break
    except ValueError:
        print("Это не число. Попробуй ещё:")
print(number)
