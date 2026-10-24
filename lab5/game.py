import config  # підключаємо файл з налаштуваннями (config.RENT, config.GOAL_GOLD і т.д.)
from ingradiens import random_ingredient  # функція вибору випадкового інгредієнта
from inventory import (add_item, remove_item, count_type, remove_by_type,  # підключаємо функції роботи з інвентарем
                       can_add, count_item, print_inventory)  # решта потрібних функцій інвентаря


def new_game(ingredient_pool):  # створює нову гру і повертає її стан
    state = {"gold": config.START_GOLD, "day": 1, "ingredients": [], "potions": []}  # стан гри: золото, день, два порожні інвентарі
    try:  # пробуємо виконати код
        give_daily_ingredients(state, ingredient_pool)  # у перший день теж даємо 5 інгредієнтів
    except Exception as e:  # якщо сталась помилка
        print("Помилка створення гри:", e)  # виводимо повідомлення про помилку
    return state  # повертаємо стан гри


def give_daily_ingredients(state, ingredient_pool):  # видає щоденні інгредієнти
    try:  # пробуємо виконати код
        print("Ти знайшов нові інгредієнти:")  # повідомлення гравцю
        for _ in range(config.DAILY_INGREDIENTS):  # повторюємо 5 разів (змінна _ не потрібна нам)
            name = random_ingredient(ingredient_pool)  # вибираємо випадковий інгредієнт
            left = add_item(state["ingredients"], name, 1,  # пробуємо додати 1 штуку в інвентар інгредієнтів
                            config.INGREDIENT_SLOTS, config.INGREDIENT_STACK)  # передаємо ліміти слотів і стака
            if left == 0:  # якщо все влізло
                print("  + " + name)  # показуємо, що додали
            else:  # якщо не влізло
                print("  (немає місця, " + name + " викинуто)")  # повідомляємо, що інгредієнт пропав
    except Exception as e:  # якщо сталась помилка
        print("Помилка видачі інгредієнтів:", e)  # виводимо повідомлення про помилку


def show_status(state):  # показує день, золото та інвентарі
    try:  # пробуємо виконати код
        print("\n=== День " + str(state["day"]) + "/" + str(config.MAX_DAYS) +  # перша частина рядка: поточний день з максимуму
              " | Золото: " + str(state["gold"]) + "/" + str(config.GOAL_GOLD) + " ===")  # друга частина: золото з цілі
        print_inventory(state["ingredients"], "Інгредієнти", config.INGREDIENT_SLOTS)  # виводимо інвентар інгредієнтів
        print_inventory(state["potions"], "Зілля", config.POTION_SLOTS)  # виводимо інвентар зілль
    except Exception as e:  # якщо сталась помилка
        print("Помилка показу статусу:", e)  # виводимо повідомлення про помилку


def show_recipes(potion_pool):  # показує список усіх зілль з рецептами
    try:  # пробуємо виконати код
        print("--- Рецепти (потрібні типи інгредієнтів) ---")  # заголовок списку
        for i in range(len(potion_pool)):  # перебираємо зілля за номерами
            p = potion_pool[i]  # беремо одне зілля зі списку
            print(str(i + 1) + ". " + p["name"] + " | " + p["recipe"][0] + " + " +  # номер, назва, перший тип рецепта
                  p["recipe"][1] + " | ціна: " + str(p["price"]))  # другий тип рецепта і ціна
    except Exception as e:  # якщо сталась помилка
        print("Помилка показу рецептів:", e)  # виводимо повідомлення про помилку


def craft_potion(state, potion_pool):  # варіння зілля
    try:  # пробуємо виконати код
        show_recipes(potion_pool)  # спочатку показуємо список зілль
        choice = int(input("Номер зілля (0 - назад): "))  # просимо ввести номер і перетворюємо текст на число
        if choice == 0:  # якщо гравець ввів 0
            return  # виходимо з функції (назад в меню)
        if choice < 1 or choice > len(potion_pool):  # якщо номер за межами списку
            print("Немає такого зілля!")  # повідомляємо про помилку
            return  # виходимо з функції
        potion = potion_pool[choice - 1]  # беремо вибране зілля (мінус 1, бо список починається з 0)

        need = {}  # словник: який тип інгредієнта і скільки штук треба
        for t in potion["recipe"]:  # перебираємо два типи з рецепта
            if t in need:  # якщо цей тип вже є в словнику (рецепт з двох однакових типів)
                need[t] += 1  # збільшуємо кількість на 1
            else:  # якщо типу ще немає
                need[t] = 1  # додаємо його з кількістю 1

        for t in need:  # перебираємо всі потрібні типи
            if count_type(state["ingredients"], t) < need[t]:  # якщо в інвентарі менше, ніж треба
                print("Не вистачає: " + t + " (треба " + str(need[t]) + ")")  # повідомляємо чого не вистачає
                return  # виходимо з функції

        if not can_add(state["potions"], potion["name"], config.POTION_SLOTS, config.POTION_STACK):  # якщо в інвентарі зілль немає місця
            print("Інвентар зілль повний! Продай зілля.")  # повідомляємо гравцю
            return  # виходимо з функції

        for t in potion["recipe"]:  # перебираємо типи з рецепта
            remove_by_type(state["ingredients"], t)  # забираємо з інвентаря по 1 інгредієнту кожного типу
        add_item(state["potions"], potion["name"], 1, config.POTION_SLOTS, config.POTION_STACK)  # додаємо зварене зілля в інвентар зілль
        print("Ти зварив: " + potion["name"] + "!")  # повідомляємо про успіх
    except ValueError:  # якщо гравець ввів не число (int() видає ValueError)
        print("Треба ввести число!")  # просимо ввести число
    except Exception as e:  # будь-яка інша помилка
        print("Помилка варіння:", e)  # виводимо повідомлення про помилку


def sell_potions(state, potion_pool):  # продає всі зілля
    try:  # пробуємо виконати код
        prices = {}  # словник цін: назва зілля -> ціна
        for p in potion_pool:  # перебираємо всі зілля гри
            prices[p["name"]] = p["price"]  # записуємо ціну під назвою зілля

        earned = 0  # скільки золота заробили, поки нуль
        while len(state["potions"]) > 0:  # поки в інвентарі зілль є хоч один слот
            slot = state["potions"].pop(0)  # забираємо перший слот зі списку через pop
            earned += prices[slot["name"]] * slot["count"]  # додаємо до заробітку: ціна помножена на кількість
        state["gold"] += earned  # додаємо заробіток до золота гравця
        print("Продано зілля на " + str(earned) + " золота.")  # повідомляємо скільки заробили
    except Exception as e:  # якщо сталась помилка
        print("Помилка продажу:", e)  # виводимо повідомлення про помилку


def check_ending(state):  # перевіряє, чи гра закінчилась: повертає "win", "lose" або None
    try:  # пробуємо виконати код
        if state["gold"] >= config.GOAL_GOLD:  # якщо золота досить для цілі
            return "win"  # перемога
        if state["day"] > config.MAX_DAYS:  # якщо дні закінчились
            return "lose"  # поразка
        return None  # інакше гра триває
    except Exception as e:  # якщо сталась помилка
        print("Помилка перевірки кінця:", e)  # виводимо повідомлення про помилку
        return None  # вважаємо, що гра триває


def end_day(state, potion_pool, ingredient_pool):  # завершення дня: продаж, оренда, новий день
    try:  # пробуємо виконати код
        print("\n--- Кінець дня " + str(state["day"]) + " ---")  # повідомлення про кінець дня
        answer = input("Продати всі зілля? (y/n): ").lower()  # питаємо гравця, .lower() робить літери маленькими
        if answer == "y":  # якщо відповів "y"
            sell_potions(state, potion_pool)  # продаємо зілля
        elif answer == "n":  # якщо відповів "n"
            print("Зілля залишаються в інвентарі.")  # зілля не продаємо
        else:  # якщо ввів щось інше
            print("Не зрозумів, зілля не продаю.")  # зілля теж не продаємо

        if check_ending(state) == "win":  # якщо після продажу вже вистачає золота
            return "win"  # повертаємо перемогу

        if state["gold"] < config.RENT:  # якщо не вистачає золота на оренду
            print("Не вистачило золота на оренду лабораторії...")  # повідомляємо гравцю
            return "lose"  # поразка
        state["gold"] -= config.RENT  # віднімаємо оренду від золота
        print("Сплачено оренду: " + str(config.RENT) + " золота.")  # повідомляємо про оплату

        state["day"] += 1  # наступний день
        if check_ending(state) == "lose":  # якщо дні вичерпались
            return "lose"  # поразка

        give_daily_ingredients(state, ingredient_pool)  # даємо нові інгредієнти на новий день
        return None  # гра продовжується
    except Exception as e:  # якщо сталась помилка
        print("Помилка завершення дня:", e)  # виводимо повідомлення про помилку
        return None  # гра продовжується


def show_ending(result, state):  # показує текст кінцівки
    try:  # пробуємо виконати код
        if result == "win":  # якщо перемога
            print("\n*** ПЕРЕМОГА! ***")  # заголовок перемоги
            print("Ти назбирав " + str(state["gold"]) + " золота за " + str(state["day"]) +  # скільки золота і днів
                  " днів і купив найкращу лабораторію в місті. Ти став Великим Алхіміком!")  # фінальний текст перемоги
        elif result == "lose":  # якщо поразка
            print("\n*** ПОРАЗКА ***")  # заголовок поразки
            print("Золота не вистачило: " + str(state["gold"]) + "/" + str(config.GOAL_GOLD) +  # скільки золота з цілі
                  ". Лабораторію забрали за борги, а ти пішов збирати трави в лісі...")  # фінальний текст поразки
    except Exception as e:  # якщо сталась помилка
        print("Помилка показу кінцівки:", e)  # виводимо повідомлення про помилку


def game_loop(ingredient_pool, potion_pool):  # головний цикл гри
    state = new_game(ingredient_pool)  # створюємо нову гру
    result = None  # результат гри, поки його немає
    while result is None:  # крутимо цикл, поки гра не закінчилась
        try:  # пробуємо виконати код
            show_status(state)  # показуємо день, золото та інвентарі
            print("\n1 - Рецепти | 2 - Зварити зілля | 3 - Закінчити день | 0 - Вийти")  # виводимо меню
            choice = input("> ")  # читаємо вибір гравця
            if choice == "1":  # якщо вибрав 1
                show_recipes(potion_pool)  # показуємо рецепти
            elif choice == "2":  # якщо вибрав 2
                craft_potion(state, potion_pool)  # варимо зілля
            elif choice == "3":  # якщо вибрав 3
                result = end_day(state, potion_pool, ingredient_pool)  # завершуємо день, зберігаємо результат (win/lose/None)
            elif choice == "0":  # якщо вибрав 0
                print("Вихід з гри.")  # прощаємось
                return  # виходимо з функції, гра закінчена
            else:  # якщо ввів щось інше
                print("Невірна команда!")  # повідомляємо про помилку
        except Exception as e:  # якщо сталась помилка
            print("Помилка в головному циклі:", e)  # виводимо повідомлення про помилку
    show_ending(result, state)  # коли цикл закінчився - показуємо кінцівку