"""Game rules for the alchemist RPG."""

import random

from ingredients import INGREDIENTS
from inventory import Inventory
from potions import POTIONS_BY_NUMBER


class Game:
    DAILY_INGREDIENTS = 5
    MAX_DAYS = 20
    STARTING_GOLD = 50
    WINNING_GOLD = 300

    def __init__(self, rng=None):
        self.day = 1
        self.gold = self.STARTING_GOLD
        self.inventory = Inventory()
        self.rng = rng if rng is not None else random.Random()
        self.won = False
        self.lost = False
        self.daily_ingredients = self.receive_daily_ingredients()

    def receive_daily_ingredients(self):
        received = []
        for name in self.rng.sample(INGREDIENTS, self.DAILY_INGREDIENTS):
            if self.inventory.add_ingredient(name):
                received.append(name)
        return received

    def craft_potion(self, number, amount=1):
        potion = POTIONS_BY_NUMBER.get(number)
        if potion is None:
            return 0
        crafted = 0
        for _ in range(max(0, amount)):
            if self.inventory.potions[potion.name] >= self.inventory.POTION_STACK_LIMIT:
                break
            if potion.name not in self.inventory.potions and (
                len(self.inventory.potions) >= self.inventory.POTION_SLOT_LIMIT
            ):
                break
            available = self.inventory.available_ingredients(potion.ingredients)
            if len(available) < 2:
                break
            try:
                self.inventory.consume_ingredients(available[:2])
            except ValueError:
                break
            if self.inventory.add_potion(potion.name) != 1:
                raise RuntimeError("Не вдалося додати виготовлене зілля до інвентаря.")
            crafted += 1
        return crafted

    def sell_potions(self, number=None, amount=None):
        if number is None:
            sold = 0
            earned = 0
            for potion_name, count in list(self.inventory.potions.items()):
                potion = next(
                    potion for potion in POTIONS_BY_NUMBER.values()
                    if potion.name == potion_name
                )
                earned += potion.price * count
                sold += count
                self.inventory.remove_potions(potion_name, count)
        else:
            potion = POTIONS_BY_NUMBER.get(number)
            if potion is None:
                return 0, 0
            count = self.inventory.potions[potion.name]
            quantity = count if amount is None else amount
            if quantity <= 0 or quantity > count:
                return 0, 0
            if not self.inventory.remove_potions(potion.name, quantity):
                return 0, 0
            sold = quantity
            earned = potion.price * quantity
        self.gold += earned
        if self.gold >= self.WINNING_GOLD:
            self.won = True
        return sold, earned

    def finish_day(self):
        if self.won or self.lost:
            return []
        if self.day >= self.MAX_DAYS:
            self.won = self.gold >= self.WINNING_GOLD
            self.lost = not self.won
            return []
        self.day += 1
        self.daily_ingredients = self.receive_daily_ingredients()
        return self.daily_ingredients
