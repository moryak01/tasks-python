# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ДРЕВНИЕ ШАХТЫ»
# Запас сил = здоровье // 10 + выносливость.
# Критический удар — каждый третий (номер удара делится на 3).
# ================================================

# --- Заголовок ------------------------------------
title = "ПОДЗЕМЕЛЬЕ: ЗАБРОШЕННЫЕ ШАХТЫ"
frame = "=" * 31

print(frame)
print(" " + title + " ")
print(frame)
print()

# --- Знакомство с героем --------------------------
print("Как зовут героя?")
hero_name = input()
print(f"Приветствую, {hero_name}!")
print("Ты попадаешь в древние шахты. Пахнет сыростью и углём.")
print()

# --- Настройка героя -------------------------------
print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")
health = int(input())
strength = int(input())
agility = int(input())
endurance = int(input())
print()
# --- Расчёт урона ----------------------------------
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // 10 + endurance

# --- Формуляр героя --------------------------------
print("Характеристики героя:")
print(f"Здоровье: {health}")
print(f"Сила: {strength}")
print(f"Ловкость: {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас сил: {stamina}")
print()

# --- Меню действий ---------------------------------
print("Что делаешь?")
print("1 - осмотреться")
print("2 - идти вперёд")
print("3 - отдохнуть")
print("4 - прислушаться")
print("5 - зажечь факел")
print("6 - тренировка")
print()

# --- Выбор действия --------------------------------
choice = input()
print()

match choice:
    case "1":
        print("Вы осматриваетесь. Гнилые подпорки держат низкий свод, на рельсах лежит перевёрнутая вагонетка.")

    case "2":
        stamina = stamina - 2
        print("Вы пробираетесь по штольне. Под ногами хрустит угольная крошка.")

    case "3":
        stamina = stamina + 3
        print("Вы садитесь на пустой ящик из-под динамита и переводите дух. Силы возвращаются.")

    case "4":
        print("Вы замираете и прислушиваетесь. Где-то в глубине скрипят старые балки, и снова тишина.")

    case "5":
        stamina = stamina - 1
        print("Вы зажигаете факел. На стенах вспыхивают прожилки руды.")

    case "6":
        strikes = 6
        training_cost = 3
        total_damage = 0
        crit_count = 0
        print("Вы находите мешок с песком, подвешенный к балке.")
        print("Похоже, на нём шахтёры когда-то отрабатывали удары киркой.")
        print()
        print(f"Наносите {strikes} ударов.")
        for i in range(1, strikes + 1):
            is_crit = i % 3 == 0
            if is_crit:
                hit_damage = crit_damage
                print(f"Удар {i}: {hit_damage:.1f} — критический!")
                crit_count += 1
            else:
                hit_damage = damage
                print(f"Удар {i}: {hit_damage:.1f}")
            total_damage += hit_damage
        average_damage = total_damage / strikes
        print()
        print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
        print(f"Общий урон: {total_damage:.1f}")
        print(f"Средний урон: {average_damage:.1f}")
        stamina -= training_cost
        if stamina < 0:
            stamina = 0

    case _:
        print("Такого действия нет.")

# --- Состояние героя -------------------------------
print()
print(f"Здоровье: {health} Запас сил: {stamina}")

# --- Прощание --------------------------------------
print()
print(frame)
print(f"Береги факел, {hero_name}!")
print(frame)
