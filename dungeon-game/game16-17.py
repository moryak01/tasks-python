# ================================================
# ИГРА "ПОДЗЕМЕЛЬЕ: ДРЕВНИЕ ШАХТЫ"
# Правила в dungeon.py, сюжет — здесь.
# Решение: «выпить» работает только для зелья; масло для факела и боевой
# эликсир действуют сразу при покупке (зелье идёт в рюкзак).
# ================================================
import json
import os
import random

import etap16_17_dungeon as dungeon

VERSION = "1.0"

# Цвета не обязательны: без colorama текст обычный.
try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False


def paint(text, color):
    """Возвращает текст, окрашенный в зелёный или жёлтый; без colorama — обычный текст."""
    if not COLOR:
        return text
    if color == "green":
        return Fore.GREEN + text + Style.RESET_ALL
    return Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL


# --- Правила и таблицы -------------------------------
MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
    ["#", "#", "#", "#", "#"],
]
DIRECTIONS = {"север": (-1, 0), "юг": (1, 0), "запад": (0, -1), "восток": (0, 1)}
LOOT = {(1, 1): "каска шахтёра", (2, 3): "медный самородок", (3, 3): "кристалл из глубин"}

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
    "заново - удалить сохранение",
    "0 - выйти из шахт (выход)",
]

commands = [
    "смотреть", "идти [направление]", "отдых", "слушать", "факел", "тренировка", "спуск",
    "лидеры", "магазин", "рюкзак", "выпить зелье", "купить <товар> [количество]",
    "карта", "разведка", "заново", "выход",
]

num_to_verb = {"1": "смотреть", "2": "идти", "3": "отдых", "4": "слушать", "5": "факел",
               "6": "тренировка", "7": "спуск", "8": "лидеры", "9": "магазин",
               "10": "рюкзак", "11": "выпить", "0": "выход"}


# --- Функции ---
def parse_command(line):
    """Возвращает пару (verb, words): команду и слова строки.
    Строка нормализуется (strip + lower); номера превращаются в команды через
    num_to_verb. Пустая строка даёт ("", []).
    """
    cmd = line.strip().lower()
    words = cmd.split()
    if not words:
        return "", []
    verb = words[0]
    if cmd in num_to_verb:
        verb = num_to_verb[cmd]
    return verb, words


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
    """Печатает итог забега: суммарный и средний урон героя. Возвращает None."""
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Суммарный урон: {total:.1f}, раундов: {rounds}, средний: {total / rounds:.1f}.")
    else:
        print("В этом забеге боёв не было.")


def scout(r, c, seen):
    """Рекурсией считает комнаты, доступные из (r, c).
    seen — множество уже посчитанных комнат. Базовый случай: посчитана или стена -> 0.
    """
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


def write_save():
    """Собирает состояние забега и записывает его в save.json.
    Герой сохраняет себя сам через hero.to_dict(); кортежи и множества становятся списками.
    Возвращает None.
    """
    save = {}
    save["hero"] = hero.to_dict()
    save["gold"] = gold_total
    save["actions"] = actions
    save["ability_bonus"] = ability_bonus
    save["max_health"] = max_health
    save["max_stamina"] = max_stamina
    save["enemies"] = enemies
    save["log"] = log
    save["inventory"] = inventory
    save["position"] = [hero_r, hero_c]
    save["visited"] = [list(p) for p in sorted(visited)]
    save["loot"] = sorted(found_loot)
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)


# --- Заголовок ------------------------------------
title = "ПОДЗЕМЕЛЬЕ: ДРЕВНИЕ ШАХТЫ"
frame = "=" * (len(title) + 6)

print(frame)
print(" " + title + " ")
print(f" v{VERSION}")
print(frame)
print()

# --- Есть ли сохранение? ---------------------------
loaded = None
if os.path.exists("save.json"):
    print("Найдено сохранение. Продолжить забег? (да/нет)")
    answer = input().strip().lower()
    if answer == "да":
        try:
            with open("save.json", encoding="utf-8") as f:
                loaded = json.load(f)
        except (ValueError, OSError):
            print("Сохранение повреждено. Начинаем новый забег.")
            loaded = None
print()

if loaded is None:
    # --- Новый забег: знакомство с героем и настройка --
    print("Как зовут героя?")
    hero_name = input()
    print(f"Приветствую, {hero_name}!")
    print("Ты попадаешь в древние шахты. Пахнет сыростью и углём.")
    print()

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

    hero = dungeon.Hero(hero_name, health, strength, agility, endurance)
    print(hero)
    print()

    enemies = ["скелет", "упырь", "паук", "летучая мышь"]
    log = []
    gold_total = 0
    ability_bonus = 0
    max_health = hero.health
    max_stamina = hero.stamina
    inventory = {}
    actions = 0
    hero_r, hero_c = 4, 2
    visited = {(4, 2)}
    found_loot = set()
else:
    # --- Продолжение: состояние берётся с сохранения ----
    hero = dungeon.Hero.from_dict(loaded["hero"])
    gold_total = loaded["gold"]
    actions = loaded["actions"]
    ability_bonus = loaded["ability_bonus"]
    max_health = loaded["max_health"]
    max_stamina = loaded["max_stamina"]
    enemies = loaded["enemies"]
    log = loaded["log"]
    inventory = loaded["inventory"]
    hero_r, hero_c = loaded["position"]
    visited = {tuple(p) for p in loaded["visited"]}
    found_loot = set(loaded["loot"])
    print(f"Забег продолжен: {hero}, золото {gold_total}, врагов осталось {len(enemies)}.")
    print()

# --- Главный цикл игры -----------------------------
running = True
outcome = "прерывание"

try:
    while running:
        print("\n".join(MENU))
        print()

        verb, words = parse_command(input())
        while verb == "":
            print("Пустая команда. Введи команду или номер.")
            verb, words = parse_command(input())
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
                    if hero.spend_stamina(2):
                        print("Силы на исходе — вы бредёте по штольне, держась за мокрую стену.")
                    else:
                        print("Вы пробираетесь по штольне. Под ногами хрустит угольная крошка.")

            case "отдых":
                hero.restore_stamina(3, max_stamina)
                print("Вы садитесь на пустой ящик из-под динамита и переводите дух. Силы возвращаются.")

            case "слушать":
                print("Вы замираете и прислушиваетесь. Где-то в глубине скрипят старые балки, и снова тишина.")

            case "факел":
                hero.spend_stamina(1, hurt=False)
                print("Вы зажигаете факел. На стенах вспыхивают прожилки руды.")

            case "тренировка":
                strikes = 6
                total_damage = 0
                crit_count = 0
                print("Вы находите мешок с песком, подвешенный к балке.")
                print("Похоже, на нём шахтёры когда-то отрабатывали удары киркой.")
                print()
                print(f"Наносите {strikes} ударов.")
                for i in range(1, strikes + 1):
                    hit_damage, crit = hero.strike(i)
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
                hero.spend_stamina(3, hurt=False)

            case "спуск":
                if not enemies:
                    print("Клеть опускается на нижний ярус, но там тихо: шахты очищены от врагов. Победа! Можно подниматься на поверхность.")
                else:
                    name = random.choice(enemies)
                    foe = dungeon.Enemy(name, dungeon.enemy_stats[name])
                    rounds, won, loot = dungeon.fight(foe, hero, ability_bonus)
                    for r in rounds:
                        log.append(r)
                    if won:
                        gold_total += loot
                        enemies.remove(name)
                        print(paint(f"{name.capitalize()}: враг повержен. Врагов осталось в шахтах: {len(enemies)}. Трофей — золото: {loot}.", "yellow"))
                        if not enemies:
                            print("Последний враг повержен — шахты очищены! Это победа. Можно подниматься на поверхность.")
                    print(f"Бой, раундов: {len(rounds)}.")

            case "лидеры":
                print_leaderboard(log)

            case "магазин":
                print("Лавка старого шахтёра (цены; покупка командой: купить <товар> [количество]):")
                for name, price in dungeon.prices.items():
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
                if item not in dungeon.prices:
                    print("Такого товара в лавке нет.")
                    continue
                if qty < 1:
                    print("Количество должно быть не меньше 1.")
                    continue
                gold_total, ok = dungeon.buy(dungeon.prices[item], gold_total, quantity=qty)
                if not ok:
                    print(f"Не хватает золота: нужно {dungeon.prices[item] * qty}, есть {gold_total}.")
                    continue
                if item == "зелье":
                    inventory[item] = inventory.get(item, 0) + qty
                elif item == "масло":
                    hero.restore_stamina(5 * qty, max_stamina)
                else:
                    ability_bonus += 2 * qty
                print(f"Куплено: {item}, {qty} шт. за {dungeon.prices[item] * qty}. Золота осталось: {gold_total}.")

            case "рюкзак":
                if not inventory:
                    print("Рюкзак пуст — только угольная пыль.")
                else:
                    print("Рюкзак:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} шт.")

            case "выпить":
                item = " ".join(words[1:]) or "зелье"
                if item != "зелье":
                    print(f"Это нельзя выпить: {item}.")
                    continue
                if inventory.get("зелье", 0) == 0:
                    print("В рюкзаке нет зелья.")
                    continue
                if hero.health >= max_health:
                    print("Здоровье и так полное — зелье лучше приберечь.")
                    continue
                hero.heal(10, max_health)
                inventory["зелье"] -= 1
                if inventory["зелье"] == 0:
                    del inventory["зелье"]
                print(f"Вы выпиваете зелье, по телу разливается тепло. Здоровье: {hero.health}. Зелий осталось: {inventory.get('зелье', 0)}.")

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

            case "заново":
                if os.path.exists("save.json"):
                    os.remove("save.json")
                    print("Сохранение удалено. Следующий забег начнётся с чистого листа.")
                else:
                    print("Нет сохранения, которое можно удалить.")
                continue

            case "выход":
                print("Клеть со скрипом поднимает вас на поверхность. Шахты остаются позади.")
                write_save()
                print("Прогресс сохранён.")
                outcome = "выход"
                running = False

            case _:
                print(f"Не понимаю команду: '{' '.join(words)}'. Введи «помощь».")
                continue

        if running:
            actions += 1
            print()
            print(paint(f"Здоровье: {hero.health} Запас сил: {hero.stamina} Врагов осталось: {len(enemies)} Золото: {gold_total}", "green"))

        if hero.health <= 0:
            print(f"{hero.name} падает без сил. Шахты забирают ещё одного искателя.")
            if os.path.exists("save.json"):
                os.remove("save.json")
            outcome = "смерть"
            running = False
except KeyboardInterrupt:
    print()
    print("Игрок прервал сеанс.")
    write_save()
finally:
    print()
    print(frame)
    if outcome == "смерть":
        print(f"Ты не выбрался, {hero.name}. Действий совершено: {actions}.")
    elif outcome == "выход":
        print(f"Смена окончена, {hero.name}. Действий совершено: {actions}.")
    else:
        print(f"Сеанс прерван, {hero.name}. Действий совершено: {actions}.")
    print_run_summary(log)
    if inventory:
        print("В рюкзаке остаётся:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} шт.")
    else:
        print("В рюкзаке остаётся: ничего.")
    print(frame)