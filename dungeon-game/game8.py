# ================================================
# ИГРА "ПОДЗЕМЕЛЬЕ: ДРЕВНИЕ ШАХТЫ"
# Запас сил = здоровье // 10 + выносливость.
# Критический удар — каждый третий (номер удара делится на 3).
# ================================================

import random

# --- Заголовок ------------------------------------
title = "ПОДЗЕМЕЛЬЕ: ДРЕВНИЕ ШАХТЫ"
frame = "=" * (len(title) + 6)

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

# --- Настройка героя -----
print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")
while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
        if health <= 0:
            raise ValueError(f"Здоровье должно быть положительным, а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Характеристики не могут быть отрицательными")
        if strength > 50:
            raise ValueError(f"Сила не может быть больше 50, а введено {strength}")
        break
    except ValueError as e:
        if str(e).startswith("invalid literal"):
            print("Ой: одна из строк не число. Введите все четыре снова:")
        else:
            print(f"{e}. Введите все четыре снова:")
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

# --- Состояние шахт --------------------------------
enemies = ["скелет", "упырь", "паук", "летучая мышь"]
log = []

# --- Главный цикл игры -----------------------------
running = True
actions = 0
menu_last = 8
outcome = "прерывание"

try:
    while running:
        print("Что делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - прислушаться")
        print("5 - зажечь факел")
        print("6 - тренировка")
        print("7 - спуститься на нижний ярус")
        print("8 - таблица лидеров")
        print("0 - выйти из шахт")

        while True:
            choice = input()
            try:
                menu_number = int(choice)
            except ValueError:
                print("Такого пункта нет. Введи номер пункта из меню.")
                continue
            if 0 <= menu_number <= menu_last:
                choice = str(menu_number)
                break
            print("Такого пункта нет. Введи номер пункта из меню.")
        print()

        match choice:
            case "1":
                print("Вы осматриваетесь. Гнилые подпорки держат низкий свод, на рельсах лежит перевёрнутая вагонетка.")

            case "2":
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("Вы пробираетесь по штольне. Под ногами хрустит угольная крошка.")
                else:
                    health -= cost - stamina
                    stamina = 0
                    print("Силы на исходе — вы бредёте по штольне, держась за мокрую стену.")

            case "3":
                stamina += 3
                print("Вы садитесь на пустой ящик из-под динамита и переводите дух. Силы возвращаются.")

            case "4":
                print("Вы замираете и прислушиваетесь. Где-то в глубине скрипят старые балки, и снова тишина.")

            case "5":
                stamina -= 1
                if stamina < 0:
                    stamina = 0
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
                    if i % 3 == 0:
                        hit_damage = crit_damage
                        print(f"Удар {i}: {hit_damage:.1f} — критический!")
                        crit_count += 1
                    else:
                        hit_damage = damage
                        print(f"Удар {i}: {hit_damage:.1f}")
                    total_damage += hit_damage
                print()
                print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
                print(f"Общий урон: {total_damage:.1f}")
                print(f"Средний урон: {total_damage / strikes:.1f}")
                stamina -= training_cost
                if stamina < 0:
                    stamina = 0

            case "7":
                if not enemies:
                    print("Клеть опускается на нижний ярус, но там тихо: шахты очищены от врагов. Победа! Можно подниматься на поверхность.")
                else:
                    enemy = random.choice(enemies)
                    enemy_hp = 45.0
                    round_n = 0
                    print(f"Скрипучая клеть опускает вас на нижний ярус. Из темноты выходит {enemy}!")
                    while enemy_hp > 0 and health > 0:
                        round_n += 1
                        if round_n % 3 == 0:
                            hit = crit_damage
                            crit = True
                        else:
                            hit = damage
                            crit = False
                        enemy_hp -= hit
                        line = f"Раунд {round_n}: герой бьёт на {hit:.1f}"
                        if crit:
                            line += " — критический!"
                        else:
                            line += "."
                        if enemy_hp <= 0:
                            line += " Враг падает."
                            log.append([round_n, hit, 0])
                        else:
                            blow = random.randint(2, 6)
                            health -= blow
                            line += f" {enemy.capitalize()}: здоровье {enemy_hp:.1f}. {enemy.capitalize()} бьёт на {blow}."
                            log.append([round_n, hit, blow])
                        print(line)
                    if enemy_hp <= 0:
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()}: враг повержен. Врагов осталось в шахтах: {len(enemies)}.")
                        if not enemies:
                            print("Последний враг повержен — шахты очищены! Это победа. Можно подниматься на поверхность.")
                    print(f"Бой, раундов: {round_n}.")

            case "8":
                if not log:
                    print("Вы ещё ни с кем не сражались в шахтах.")
                else:
                    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
                    print("Таблица лидеров (урон героя):")
                    for i in range(len(top)):
                        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
                    worst = max(log, key=lambda r: r[2])    # из равных побеждает первый
                    print(f"Самый сильный удар врага: {worst[2]} (раунд {worst[0]}).")

            case "0":
                print("Клеть со скрипом поднимает вас на поверхность. Шахты остаются позади.")
                outcome = "выход"
                running = False

            case _:
                print("Такого действия нет.")

        if running:
            actions += 1
            print()
            print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)}")

        if health <= 0:
            print(f"{hero_name} падает без сил. Шахты забирают ещё одного искателя.")
            outcome = "смерть"
            running = False
except KeyboardInterrupt:
    print()
    print("Игрок прервал сеанс.")
finally:
    print()
    print(frame)
    if outcome == "смерть":
        print(f"Ты не выбрался, {hero_name}. Действий совершено: {actions}.")
    elif outcome == "выход":
        print(f"Смена окончена, {hero_name}. Действий совершено: {actions}.")
    else:
        print(f"Сеанс прерван, {hero_name}. Действий совершено: {actions}.")
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Суммарный урон: {total:.1f}, раундов: {rounds}, средний: {total / rounds:.1f}.")
    else:
        print("В этом забеге боёв не было.")
    print(frame)
