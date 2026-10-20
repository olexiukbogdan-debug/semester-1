import random
import unittest

from game import Game
from ingredients import INGREDIENTS
from inventory import Inventory
from potions import POTIONS


class InventoryTests(unittest.TestCase):
    def test_catalogs_have_required_unique_item_counts(self):
        self.assertEqual(len(INGREDIENTS), 200)
        self.assertEqual(len(set(INGREDIENTS)), 200)
        self.assertEqual(len(POTIONS), 50)
        self.assertEqual(len({potion.name for potion in POTIONS}), 50)

    def test_ingredient_slot_and_stack_limits(self):
        inventory = Inventory()
        for index in range(25):
            self.assertTrue(inventory.add_ingredient(f"ingredient-{index}"))
        self.assertFalse(inventory.add_ingredient("ingredient-25"))
        inventory.ingredients["ingredient-0"] = 25
        self.assertFalse(inventory.add_ingredient("ingredient-0"))

    def test_potion_slot_and_stack_limits(self):
        inventory = Inventory()
        for index in range(10):
            self.assertEqual(inventory.add_potion(f"potion-{index}", 10), 10)
        self.assertEqual(inventory.add_potion("potion-10"), 0)
        self.assertEqual(inventory.add_potion("potion-0"), 0)


class GameTests(unittest.TestCase):
    def test_daily_reward_gives_five_distinct_ingredients(self):
        game = Game(rng=random.Random(4))
        self.assertEqual(len(game.daily_ingredients), 5)
        self.assertEqual(len(set(game.daily_ingredients)), 5)
        self.assertEqual(sum(game.inventory.ingredients.values()), 5)

    def test_crafting_consumes_two_recipe_ingredients_and_selling_awards_gold(self):
        game = Game(rng=random.Random(4))
        potion = POTIONS[0]
        game.inventory.ingredients[potion.ingredients[0]] = 1
        game.inventory.ingredients[potion.ingredients[1]] = 1

        self.assertEqual(game.craft_potion(potion.number), 1)
        self.assertEqual(game.inventory.potions[potion.name], 1)
        sold, earned = game.sell_potions(potion.number)
        self.assertEqual((sold, earned), (1, potion.price))
        self.assertEqual(game.gold, game.STARTING_GOLD + potion.price)

    def test_game_is_lost_after_last_day_if_goal_is_not_met(self):
        game = Game(rng=random.Random(2))
        for _ in range(game.MAX_DAYS - 1):
            game.finish_day()
        self.assertFalse(game.lost)
        game.finish_day()
        self.assertTrue(game.lost)
        self.assertEqual(game.day, game.MAX_DAYS)

    def test_winning_gold_ends_game_successfully(self):
        game = Game(rng=random.Random(3))
        game.gold = game.WINNING_GOLD - POTIONS[0].price
        game.inventory.add_potion(POTIONS[0].name)
        self.assertEqual(game.sell_potions(POTIONS[0].number), (1, POTIONS[0].price))
        self.assertTrue(game.won)

    def test_full_potion_stack_does_not_consume_ingredients(self):
        game = Game(rng=random.Random(5))
        potion = POTIONS[0]
        game.inventory.ingredients[potion.ingredients[0]] = 1
        game.inventory.ingredients[potion.ingredients[1]] = 1
        game.inventory.potions[potion.name] = game.inventory.POTION_STACK_LIMIT

        self.assertEqual(game.craft_potion(potion.number), 0)
        self.assertEqual(game.inventory.ingredients[potion.ingredients[0]], 1)
        self.assertEqual(game.inventory.ingredients[potion.ingredients[1]], 1)


if __name__ == "__main__":
    unittest.main()
