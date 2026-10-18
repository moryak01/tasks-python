import random
title = "НЕЗАБЫВАЕМОЕ ПРИКЛЮЧЕНИЕ"
frame = "=" * 20

print(frame)
print(" " + title + " ")
print(frame)
print()

# знакомство с героем
print("Как зовут героя?")
hero_name = input()

print(f"Добро пожаловать, {hero_name}!")
print("Ты появляешься на пустом поле.")
print()

# настройки героя
print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")

while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
        if health <= 0:
            raise ValueError(f"Здоровье должно быть больше, а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Характеристики не могут быть меньше 0")
        break
    except ValueError:
        print("Одна из строк не число. Введите все четыре снова: ")

# расчёт урона и энергии
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = endurance // agility

max_health = health
max_stamina = stamina

# формуляр героя
print("Характеристики героя:")
print(f"Здоровье: {health} (макс: {max_health})")
print(f"Сила: {strength}")
print(f"Ловкость: {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Стамина: {stamina:.1f} (макс: {max_stamina})")
print()

# состояние забега
enemies = ["ghoul", "skeleton", "spider", "bat"]
log = []
gold_total = 0
ability_bonus = 0
prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}
inventory = {}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "ghoul":    {"hp": 30, "damage": 4, "loot": 15},
    "spider":   {"hp": 20, "damage": 3, "loot": 10},
    "bat":      {"hp": 12, "damage": 2, "loot": 5},
}

# задание функций

def hero_hit(strike_n):
    """Рассчитывается урон героя в зависимости от номера удара.
    
    Принимает:
        strike_n (int) — порядковый номер удара.
    Возвращает:
        tuple (float, bool) — пару (урон, признак критического удара).
    Описание:
        Ничего не печатает. Читает глобальные правила игры damage и crit_damage.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0):
    """Идёт пошаговый автоматический бой с врагом до гибели одного из участников.
    
    Принимает:
        enemy (str) — имя врага (должно быть в глобальном словаре enemy_stats).
        hero_health (int) — текущее здоровье героя на момент начала боя.
        bonus (int/float, по умолчанию 0) — постоянная надбавка к урону героя.
    Возвращает:
        tuple (list, bool, int, int) — кортеж из четырех элементов по именам:
            - rounds (list): таблица раундов боя для журнала.
            - won (bool): True, если враг пал, иначе False.
            - hero_health (int): обновленное здоровье героя после боя.
            - loot (int): фиксированное золото из карточки врага.
    Описание:
        Карточка параметров врага извлекается из enemy_stats по имени.
        Обязательно наличие в карточке ключей: 'hp', 'damage', 'loot'.
        Активно печатает ход сражения по раундам в консоль через f-строки.
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0
    print(f"Вы спускаетесь по лестнице. Из темноты появляется {enemy}!")
    
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        hit += bonus
        enemy_hp -= hit
        line = f"Round {round_n}: hero deals {hit:.1f}"
        if crit:
            line += " - Критический урон!"
            
        if enemy_hp <= 0:
            line += " Враг падает."
            rounds.append([round_n, hit, 0])
        else:
            blow = stats["урон"]
            hero_health -= blow
            line += f" {enemy} Здоровье: {enemy_hp:.1f}. {enemy.capitalize()} хиты - {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
        
    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0
        
    return rounds, won, hero_health, loot


def buy(price, gold, quantity=1):
    """Проводится транзакция покупки предметов за золото.
    
    Принимается:
        price (int) — цена одной штуки товара.
        gold (int) — текущий запас золота у героя.
        quantity (int, по умолчанию 1) — количество покупаемого товара.
    Возвращается:
        tuple (int, bool) — пару (gold_left, ok): остаток золота и признак успешности покупки.
    Описание:
        Ничего не печатает. Чек и сообщения об ошибках выводятся вызывающей веткой меню.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


def print_leaderboard(log):
    """Выводится на экран три лучших раунда героя по урону и сильнейший удар врага.
    
    Принимается:
        log — глобальный журнал таблицы чисел всех раундов.
    Возвращается:
        None — контракт функции подразумевает исключительно вывод текста в консоль.
    Описание:
        Безопасно прерывает работу через пустой return, если журнал пуст.
        Выполняет устойчивую сортировку и поиск максимума по ключам через lambda.
    """
    if not log:
        print("You haven't fought yet.")
        return
        
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Таблица лидеров (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
        
    worst = max(log, key=lambda r: r[2])
    print(f"Удар по сильнейшему противнику: {worst[2]} (round {worst[0]}).")


def print_run_summary(log):
    """Рассчитывается и выводится суммарный и средний нанесенный героем урон за весь забег.
    
    Принимается:
        log — глобальный журнал таблицы чисел всех раундов.
    Возвращается:
        None — контракт функции подразумевает только вывод текста.
    Описание:
        Безопасна на пустом журнале: защищена ветвлением от ZeroDivisionError.
        Вынимает колонку урона героя напрямую через генератор в функцию sum().
    """
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")

running = True
actions = 0

try:
    while running:
        print("Что ты делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - копать")
        print("5 - отжаться")
        print("6 - тренировка")
        print("7 - зайти глубже в лес")
        print("8 - leaderboard")
        print("9 - shop")
        print("10 - backpack")
        print("11 - drink potion")
        print("0 - выйти из подземелья")
        print()
        
        menu_last = 11
        while True:
            choice = input()
            try:
                menu_number = int(choice)
            except ValueError:
                print("Такого пункта нет. Введи номер пункта из меню.")
                continue
            if 0 <= menu_number <= menu_last:
                break
            print("Такого пункта нет. Введи номер пункта из меню.")
            
        match choice:
            case "1":
                print("Вы осмотрелись. Впереди виден лес.")
            case "2":
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
                else:
                    health -= cost - stamina
                    stamina = 0
                    print("Сил больше нет — вы идёте на одном упорстве.")
            case "3":
                stamina = min(stamina + 2, max_stamina)
                print("Вы успешно отдохнули и набрались сил!")
            case "4":
                stamina = stamina - 7
                print("Вы успешно покопали.")
            case "5":
                stamina = stamina - 8
                strength = strength + 2
                print("Вы отжались и стали сильнее!")
            case "6":
                strikes = 5
                total_damage = 0
                crit_count = 0
                print("Вы подходите к дереву.")
                print(f"Вы нанесли {strikes} ударов.")
                
                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i)
                    if crit:
                        crit_count += 1
                        print(f"Удар {i}: {hit_damage:.1f} — критический!")
                    else:
                        print(f"Удар {i}: {hit_damage:.1f}")
                    total_damage += hit_damage
                print(f"Всего нанесено урона на тренировке: {total_damage:.1f} (Критов: {crit_count})")
                print()
                
            case "7":
                if not enemies:
                    print("Вы спустились по лестницк. Но подземелье пусто.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health, loot = fight(enemy, health, bonus=ability_bonus)
                    
                    for r in rounds:
                        log.append(r)
                        
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                    print(f"Battle: {len(rounds)} rounds.")
                    
            case "8":
                print_leaderboard(log)
                
            case "9":
                print("Магазин:")
                for name, price in prices.items():
                    print(f"{name}: {price} золото")
                print("Название предмета (пустая строка - не покупается):")
                name = input()
                if name != "":
                    if name in prices:
                        price = prices[name]
                        print("Количество (Enter для одного):")
                        qty_line = input()
                        if qty_line == "":
                            qty = 1
                            gold_total, ok = buy(price, gold_total)
                        else:
                            qty = int(qty_line)
                            gold_total, ok = buy(price, gold_total, quantity=qty)
                        
                        if ok:
                            inventory[name] = inventory.get(name, 0) + qty
                            print(f"Куплено {qty} {name} за {price * qty} золото. Золота осталось: {gold_total}.")
                        else:
                            print(f"Недостаточно голды: need {price * qty}, have {gold_total}.")
                    else:
                        print("Нет такого предмета в магазине.")
                        
            case "10":
                if not inventory:
                    print("Рюкзак пуст.")
                else:
                    print("Рюкзак:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} пкс")
                        
            case "11":
                if inventory.get("potion", 0) == 0:
                    print("Отстутствуют зелья в рюкзаке")
                else:
                    health = min(health + 10, max_health)
                    inventory["potion"] -= 1
                    if inventory["potion"] == 0:
                        del inventory["potion"]
                    print(f"Ты выпил зелье. Твое здоровье: {health}. Зелей осталось: {inventory.get('potion', 0)}")
                    
            case "0":
                print("Вы решили выйти.")
                running = False
                
            case _:
                print("Такого действия нет.")
                
        if health <= 0:
            print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
            running = False
            
        if running:
            actions += 1

finally:
    print()
    print(frame)
    if health <= 0:
        print(f"Ты не дошёл до места назначения, {hero_name}. Действий совершено: {actions}.")
    else:
        print(f"Забег был завершен, {hero_name}. Действий совершено: {actions}.")
        
    print_run_summary(log)
    print(f"Здоровье: {health}/{max_health} Выносливость: {stamina}/{max_stamina} Осталось врагов: {len(enemies)} Золото: {gold_total}")
    
    if inventory:
        print("Оставлено в рюкзаке; ")
        for name, qty in inventory.items():
            print(f"{name}: {qty} pcs")
    else:
        print("Оставлено в рюкзаке: Ничего.")
    print(frame)
