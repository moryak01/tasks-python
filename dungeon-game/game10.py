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

# --- Правила и состояние ---------------------------
enemies = ["скелет", "упырь", "паук", "летучая мышь"]
log = []
gold_total = 0        # состояние забега
ability_bonus = 0     # боевой эликсир: прибавка к урону до конца забега
max_health = health
max_stamina = stamina


# --- Функции ---------
def hero_hit(strike_n):
    """Урон героя на ударе номер strike_n.
    Возвращает пару (hit, crit): урон и признак критического удара.
    Читает глобальные правила damage и crit_damage, ничего не меняет.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0):
    """Бой с enemy до гибели одного из двоих.
    bonus — надбавка к каждому удару героя ПОСЛЕ удвоения критом
    (критический удар получает +bonus, а не +2*bonus); по умолчанию 0.
    Печатает строки раундов.
    Возвращает (rounds, won, hero_health, loot).
    """
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"Скрипучая клеть опускает вас на нижний ярус. Из темноты выходит {enemy}!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        hit = hit + bonus
        enemy_hp -= hit
        line = f"Раунд {round_n}: герой бьёт на {hit:.1f}"
        if crit:
            line += " — критический!"
        else:
            line += "."
        if enemy_hp <= 0:
            line += " Враг падает."
            rounds.append([round_n, hit, 0])
        else:
            blow = random.randint(2, 6)
            hero_health -= blow
            line += f" {enemy.capitalize()}: здоровье {enemy_hp:.1f}. {enemy.capitalize()} бьёт на {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
    won = enemy_hp <= 0
    if won:
        loot = 10 + 5 * round_n
    else:
        loot = 0
    return rounds, won, hero_health, loot


def buy(price, gold, quantity=1):
    """Покупает quantity штук товара ценой price за золото gold.
    quantity по умолчанию 1. Возвращает (gold_left, ok): остаток
    золота и признак успешной покупки. Ничего не печатает.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


def read_quantity():
    """Спрашивает количество. Пустой Enter означает «одна штука».
    Возвращает целое >= 1 или None, если ввод не подходит как количество.
    """
    print("Количество (Enter — одна штука):")
    line = input().strip()
    if line == "":
        return 1
    try:
        qty = int(line)
    except ValueError:
        return None
    if qty < 1:
        return None
    return qty


def print_leaderboard(log):
    """Печатает топ-3 раундов по урону героя и самый сильный удар врага.
    Возвращает None: контракт функции — печать, а не данные.
    """
    if not log:
        print("Вы ещё ни с кем не сражались в шахтах.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Таблица лидеров (урон героя):")
    for i in range(len(top)):
        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
    worst = max(log, key=lambda r: r[2])
    print(f"Самый сильный удар врага: {worst[2]} (раунд {worst[0]}).")


def print_run_summary(log):
    """Печатает итог забега: суммарный и средний урон героя.
    Возвращает None. Не падает на пустом журнале.
    """
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Суммарный урон: {total:.1f}, раундов: {rounds}, средний: {total / rounds:.1f}.")
    else:
        print("В этом забеге боёв не было.")


# --- Главный цикл игры -----------------------------
running = True
actions = 0
menu_last = 9
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
        print("9 - магазин")
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
                stamina = min(stamina + 3, max_stamina)
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
                    hit_damage, crit = hero_hit(i)
                    if crit:
                        crit_count += 1
                        print(f"Удар {i}: {hit_damage:.1f} — критический!")
                    else:
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
                    rounds, won, health, loot = fight(enemy, health, bonus=ability_bonus)
                    for r in rounds:
                        log.append(r)
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()}: враг повержен. Врагов осталось в шахтах: {len(enemies)}. Трофей — золото: {loot}.")
                        if not enemies:
                            print("Последний враг повержен — шахты очищены! Это победа. Можно подниматься на поверхность.")
                    print(f"Бой, раундов: {len(rounds)}.")

            case "8":
                print_leaderboard(log)

            case "9":
                print("Лавка старого шахтёра:")
                print("1 - зелье (+10 здоровья): цена 10")
                print("2 - масло для факела (+5 сил): цена 15")
                print("3 - боевой эликсир (+2 к урону до конца забега): цена 40")
                print("Номер товара (0 — ничего не покупать):")
                item = input().strip()
                prices = (10, 15, 40)
                names = ("зелье", "масло", "эликсир")
                if item in ("1", "2", "3"):
                    price = prices[int(item) - 1]
                    name = names[int(item) - 1]
                    qty = read_quantity()
                    if qty is None:
                        print("Это не подходящее количество.")
                    else:
                        if qty == 1:
                            gold_total, ok = buy(price, gold_total) 
                        else:
                            gold_total, ok = buy(price, gold_total, quantity=qty)
                        if ok:
                            if item == "1":
                                health = min(health + 10 * qty, max_health)
                            elif item == "2":
                                stamina = min(stamina + 5 * qty, max_stamina)
                            else:
                                ability_bonus += 2 * qty
                            print(f"Куплено: {name}, {qty} шт. за {price * qty}. Золота осталось: {gold_total}.")
                        else:
                            print(f"Не хватает золота: нужно {price * qty}, есть {gold_total}.")
                elif item != "0":
                    print("Такого товара в лавке нет.")

            case "0":
                print("Клеть со скрипом поднимает вас на поверхность. Шахты остаются позади.")
                outcome = "выход"
                running = False

            case _:
                print("Такого действия нет.")

        if running:
            actions += 1
            print()
            print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)} Золото: {gold_total}")

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
    print_run_summary(log)
    print(frame)