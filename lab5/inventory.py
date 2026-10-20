"""Bounded potion and ingredient inventories."""

from collections import Counter


class Inventory:
    INGREDIENT_SLOT_LIMIT = 25
    INGREDIENT_STACK_LIMIT = 25
    POTION_SLOT_LIMIT = 10
    POTION_STACK_LIMIT = 10

    def __init__(self):
        self.ingredients = Counter()
        self.potions = Counter()

    def add_ingredient(self, name):
        if name not in self.ingredients and len(self.ingredients) >= self.INGREDIENT_SLOT_LIMIT:
            return False
        if self.ingredients[name] >= self.INGREDIENT_STACK_LIMIT:
            return False
        self.ingredients[name] += 1
        return True

    def add_potion(self, name, amount=1):
        if amount <= 0:
            return 0
        if name not in self.potions and len(self.potions) >= self.POTION_SLOT_LIMIT:
            return 0
        accepted = min(amount, self.POTION_STACK_LIMIT - self.potions[name])
        if accepted:
            self.potions[name] += accepted
        return accepted

    def available_ingredients(self, names):
        return [name for name in names if self.ingredients[name] > 0]

    def consume_ingredients(self, names):
        for name in names:
            if self.ingredients[name] <= 0:
                raise ValueError(f"Недостатньо інгредієнта: {name}")
        for name in names:
            self.ingredients[name] -= 1
            if self.ingredients[name] == 0:
                del self.ingredients[name]

    def remove_potions(self, name, amount):
        if amount <= 0 or self.potions[name] < amount:
            return False
        self.potions[name] -= amount
        if self.potions[name] == 0:
            del self.potions[name]
        return True
