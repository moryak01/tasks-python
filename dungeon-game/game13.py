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

# --- Настройка героя ----
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
gold_total = 0
ability_bonus = 0
max_health = health
max_stamina = stamina
prices = {"зелье": 10, "масло": 15, "эликсир": 40}
enemy_stats = {
    "скелет": {"hp": 45, "damage": 6, "loot": 25},
    "упырь": {"hp": 30, "damage": 4, "loot": 15},
    "паук": {"hp": 20, "damage": 3, "loot": 10},
    "летучая мышь": {"hp": 12, "damage": 2, "loot": 5},
}
inventory = {}

# Карта: "#" — стена, "." — комната, "S" — старт.
MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
    ["#", "#", "#", "#", "#"],
]
DIRECTIONS = {"север": (-1, 0), "юг": (1, 0), "запад": (0, -1), "восток": (0, 1)}
hero_r, hero_c = 4, 2   # позиция героя: строка, столбец
visited = {(4, 2)}   # множество кортежей: старт уже посещён
LOOT = {(1, 1): "каска шахтёра", (2, 3): "медный самородок", (3, 3): "кристалл из глубин"}
found_loot = set()

MENU = [
    "Что делаешь? (номер или команда; «помощь» — справка)",
    "1 - осмотреться (смотреть)",
    "2 - идти вперёд (идти)",
    "3 - отдохнуть (отдых)",
    "4 - прислушаться (слушать)",
    "5 - зажечь факел (факел)",
    "6 - тренировка (тренировка)",
    "7 - спуститься на нижний ярус (спуск)",
    "8 - таблица лидеров (лидеры)",
    "9 - магазин (магазин)",
    "10 - рюкзак (рюкзак)",
    "11 - выпить зелье (выпить)",
    "карта - показать карту",
    "разведка - сколько комнат доступно",
    "0 - выйти из шахт (выход)",
]

commands = [
    "смотреть", "идти [направление]", "отдых", "слушать", "факел", "тренировка", "спуск",
    "лидеры", "магазин", "рюкзак", "выпить зелье", "купить <товар> [количество]",
    "карта", "разведка", "выход"]

num_to_verb = {"1": "смотреть", "2": "идти", "3": "отдых", "4": "слушать", "5": "факел",
               "6": "тренировка", "7": "спуск", "8": "лидеры", "9": "магазин",
               "10": "рюкзак", "11": "выпить", "0": "выход"}


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
    Карточка врага берётся из enemy_stats по имени; нужны ключи hp, damage, loot.
    bonus — надбавка к каждому удару героя (по умолчанию 0).
    Печатает строки раундов. Возвращает (rounds, won, hero_health, loot).
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
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
            blow = stats["damage"]
            hero_health -= blow
            line += f" {enemy.capitalize()}: здоровье {enemy_hp:.1f}. {enemy.capitalize()} бьёт на {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0
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


def scout(r, c, seen):
    """Рекурсией считает комнаты, доступные из (r, c).
    seen — множество уже посчитанных комнат (одно на весь обход).
    Базовый случай: комната уже посчитана или это стена -> 0.
    """
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


# --- Главный цикл игры -----------------------------
running = True
actions = 0
outcome = "прерывание"
try:
    while running:
        print("\n".join(MENU))
        print()

        line = input()
        cmd = line.strip().lower()
        while cmd == "":
            print("Пустая команда. Введи команду или номер.")
            line = input()
            cmd = line.strip().lower()
        words = cmd.split()
        verb = words[0]
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]
        print()

        match verb:
            case "смотреть":
                print("Вы осматриваетесь. Гнилые подпорки держат низкий свод, на рельсах лежит перевёрнутая вагонетка.")

            case "идти":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"Вы нашли: {item}! Уникальных находок: {len(found_loot)}.")
                        print(f"Вы идёте по штольне: {words[1]}. Комната ({hero_r}, {hero_c}).")
                    else:
                        print(f"Туда не пройти: {words[1]}: там завал или край шахты.")
                elif len(words) > 1:
                    print(f"Неизвестное направление: '{words[1]}'. Используй: север, юг, запад, восток.")
                    continue
                else:
                    cost = 2
                    if stamina >= cost:
                        stamina -= cost
                        print("Вы пробираетесь по штольне. Под ногами хрустит угольная крошка.")
                    else:
                        health -= cost - stamina
                        stamina = 0
                        print("Силы на исходе — вы бредёте по штольне, держась за мокрую стену.")

            case "отдых":
                stamina = min(stamina + 3, max_stamina)
                print("Вы садитесь на пустой ящик из-под динамита и переводите дух. Силы возвращаются.")

            case "слушать":
                print("Вы замираете и прислушиваетесь. Где-то в глубине скрипят старые балки, и снова тишина.")

            case "факел":
                stamina -= 1
                if stamina < 0:
                    stamina = 0
                print("Вы зажигаете факел. На стенах вспыхивают прожилки руды.")

            case "тренировка":
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


            case "спуск":
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

            case "лидеры":
                print_leaderboard(log)

            case "магазин":
                print("Лавка старого шахтёра (цены; покупка командой: купить <товар> [количество]):")
                for name, price in prices.items():
                    print(f"{name}: цена {price}")

            case "купить":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])
                if item == "":
                    print("Что купить? Введи: купить <товар>.")
                    continue
                if item not in prices:
                    print("Такого товара в лавке нет.")
                    continue
                if qty < 1:
                    print("Количество должно быть не меньше 1.")
                    continue
                gold_total, ok = buy(prices[item], gold_total, quantity=qty)
                if ok:
                    if item == "зелье":
                        inventory[item] = inventory.get(item, 0) + qty
                    elif item == "масло":
                        stamina = min(stamina + 5 * qty, max_stamina)
                    else:
                        ability_bonus += 2 * qty
                    print(f"Куплено: {item}, {qty} шт. за {prices[item] * qty}. Золота осталось: {gold_total}.")
                else:
                    print(f"Не хватает золота: нужно {prices[item] * qty}, есть {gold_total}.")
                    continue

            case "рюкзак":
                if not inventory:
                    print("Рюкзак пуст — только угольная пыль.")
                else:
                    print("Рюкзак:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} шт.")

            case "выпить":
                item = " ".join(words[1:]) or "зелье"    # просто «выпить» означает зелье
                if item != "зелье":
                    print(f"Это нельзя выпить: {item}.")
                    continue
                if inventory.get("зелье", 0) == 0:
                    print("В рюкзаке нет зелья.")
                    continue
                if health >= max_health:
                    print("Здоровье и так полное — зелье лучше приберечь.")
                    continue
                health = min(health + 10, max_health)
                inventory["зелье"] -= 1
                if inventory["зелье"] == 0:
                    del inventory["зелье"]
                print(f"Вы выпиваете зелье, по телу разливается тепло. Здоровье: {health}. Зелий осталось: {inventory.get('зелье', 0)}.")

            case "помощь":
                print("Команды: " + ", ".join(commands) + ".")
                print("Номера 0–11 работают как раньше.")
                actions += 1
                continue

            case "карта":
                print("Карта шахт:")
                for i in range(len(MAP)):
                    cells = []
                    for j in range(len(MAP[i])):
                        cell = "@" if (i, j) == (hero_r, hero_c) else MAP[i][j]
                        cells.append(cell)
                    print(" ".join(cells))

            case "разведка":
                seen = set()
                print(f"Разведка: {scout(hero_r, hero_c, seen)} комнат доступно.")

            case "выход":
                print("Клеть со скрипом поднимает вас на поверхность. Шахты остаются позади.")
                outcome = "выход"
                running = False

            case _:
                print(f"Не понимаю команду: '{line.strip()}'. Введи «помощь».")
                continue

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
    if inventory:
        print("В рюкзаке остаётся:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} шт.")
    else:
        print("В рюкзаке остаётся: ничего.")
    print(frame)