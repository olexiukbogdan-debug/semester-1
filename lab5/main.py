"""Console entry point for the alchemist RPG."""

from game import Game
from potions import POTIONS


def read_integer(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Введіть ціле число.")
        return None
    except EOFError:
        return 0


def show_inventory(game):
    inventory = game.inventory
    print(
        f"\nІнгредієнти ({len(inventory.ingredients)}/"
        f"{inventory.INGREDIENT_SLOT_LIMIT} слотів):"
    )
    if inventory.ingredients:
        for name, count in sorted(inventory.ingredients.items()):
            print(f"  {name}: {count}/{inventory.INGREDIENT_STACK_LIMIT}")
    else:
        print("  Порожньо")

    print(
        f"\nЗілля ({len(inventory.potions)}/"
        f"{inventory.POTION_SLOT_LIMIT} слотів):"
    )
    if inventory.potions:
        for name, count in sorted(inventory.potions.items()):
            print(f"  {name}: {count}/{inventory.POTION_STACK_LIMIT}")
    else:
        print("  Порожньо")


def show_potions():
    print("\nКаталог зіль і рецепти (для кожного зілля потрібні будь-які 2 з 4):")
    for potion in POTIONS:
        ingredients = ", ".join(potion.ingredients)
        print(
            f"{potion.number}. {potion.name} — {potion.price} золотих; "
            f"інгредієнти: {ingredients}"
        )


def craft_potion(game):
    number = read_integer("Номер зілля з каталогу: ")
    if number is None:
        return
    amount = read_integer("Скільки виготовити: ")
    if amount is None:
        return
    crafted = game.craft_potion(number, amount)
    if crafted:
        print(f"Виготовлено зіль: {crafted}.")
    else:
        print("Не вистачає двох потрібних інгредієнтів або місця в інвентарі.")


def sell_potions(game):
    if not game.inventory.potions:
        print("Немає зіль для продажу.")
        return
    sold, earned = game.sell_potions()
    print(f"Продано зіль: {sold}. Отримано {earned} золотих.")
    print(f"Баланс: {game.gold} золотих.")


def show_daily_reward(game):
    print(f"\nДень {game.day}/{game.MAX_DAYS} | Золото: {game.gold}")
    print(f"Сьогодні отримано інгредієнтів: {len(game.daily_ingredients)}/"
          f"{game.DAILY_INGREDIENTS}")
    if game.daily_ingredients:
        for name in game.daily_ingredients:
            print(f"  + {name}")
    if len(game.daily_ingredients) < game.DAILY_INGREDIENTS:
        print("  Не всі інгредієнти помістилися: інвентар інгредієнтів заповнений.")


def main():
    game = Game()
    print("АЛХІМІК: ШЛЯХ ДО КОРОЛІВСЬКОГО ДВОРУ")
    print(
        f"Збери {game.WINNING_GOLD} золотих за {game.MAX_DAYS} днів, "
        "щоб стати королівським алхіміком!"
    )
    show_daily_reward(game)

    while not game.won and not game.lost:
        print(
            "\n1. Інвентар | 2. Каталог зіль | 3. Варити зілля | "
            "4. Продати зілля | 5. Завершити день | 0. Вийти"
        )
        try:
            choice = input("Твій вибір: ").strip()
            if choice == "1":
                show_inventory(game)
            elif choice == "2":
                show_potions()
            elif choice == "3":
                craft_potion(game)
            elif choice == "4":
                sell_potions(game)
            elif choice == "5":
                rewards = game.finish_day()
                if rewards:
                    show_daily_reward(game)
                elif game.lost:
                    break
                if not game.won and not game.lost and game.day == game.MAX_DAYS:
                    print("Настав останній ігровий день!")
            elif choice == "0":
                print("Ти залишив алхімічну майстерню. Гру завершено.")
                return
            else:
                print("Невідомий пункт меню.")
        except (EOFError, KeyboardInterrupt):
            print("\nГру завершено.")
            return

    if game.won:
        print(
            f"\nПеремога! Ти заробив {game.gold} золотих і став "
            "королівським алхіміком!"
        )
    elif game.lost:
        print(
            f"\nПоразка: за {game.MAX_DAYS} днів ти зібрав лише "
            f"{game.gold} із {game.WINNING_GOLD} потрібних золотих. "
            "Королівський двір найняв іншого алхіміка."
        )


if __name__ == "__main__":
    main()
