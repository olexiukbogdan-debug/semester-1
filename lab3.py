from decimal import Decimal


class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = Decimal(price)
        self.stock = stock


class Shop:
    def __init__(self):
        self.products = {
            1: Product("Хліб", "32.50", 12),
            2: Product("Молоко", "45.90", 8),
            3: Product("Яблука", "68.00", 15),
        }
        self.cart = {}

    def catalog(self):
        for number, product in sorted(self.products.items(), key=lambda item: item[1].name):
            print(f"{number}. {product.name} — {product.price:.2f}грн ({product.stock} шт.)")

    def add(self, number, amount):
        product = self.products.get(number)
        if product and 0 < amount <= product.stock - self.cart.get(number, 0):
            self.cart[number] = self.cart.get(number, 0) + amount
            print("Товар додано.")
        else:
            print("Перевірте номер товару, кількість і залишок.")

    def show_cart(self):
        total = Decimal("0")
        for number, amount in self.cart.items():
            product = self.products[number]
            cost = product.price * amount
            total += cost
            print(f"{product.name}: {amount} шт. — {cost:.2f}грн")
        print(f"Разом: {total:.2f}грн" if self.cart else "Кошик порожній.")

    def remove(self, number, amount):
        if number in self.cart and amount > 0:
            self.cart[number] -= amount
            if self.cart[number] <= 0:
                del self.cart[number]
            print("Кошик оновлено.")
        else:
            print("Такого товару немає у кошику.")

    def buy(self):
        if not self.cart:
            print("Кошик порожній.")
            return
        self.show_cart()
        for number, amount in self.cart.items():
            self.products[number].stock -= amount
        self.cart.clear()
        print("Покупку оформлено!")


def number(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        return 0


def main():
    shop = Shop()
    while True:
        print("\n1 Каталог | 2 Додати | 3 Кошик | 4 Видалити | 5 Купити | 6 Адмін | 0 Вихід")
        choice = input("Вибір: ")
        if choice == "1":
            shop.catalog()
        elif choice == "2":
            shop.add(number("Номер товару: "), number("Кількість: "))
        elif choice == "3":
            shop.show_cart()
        elif choice == "4":
            shop.remove(number("Номер товару: "), number("Кількість: "))
        elif choice == "5":
            shop.buy()
        elif choice == "6":
            if input("Логін: ") == "admin" and input("Пароль: ") == "1234":
                for product in shop.products.values():
                    print(f"{product.name}: {product.stock} шт.")
            else:
                print("Неправильний логін або пароль.")
        elif choice == "0":
            break
        else:
            print("Невідомий пункт меню.")


if __name__ == "__main__":
    main()