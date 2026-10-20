"""Potion catalog and their ingredient requirements."""

from dataclasses import dataclass

from ingredients import INGREDIENTS


@dataclass(frozen=True)
class Potion:
    number: int
    name: str
    ingredients: tuple[str, ...]
    price: int


_EFFECTS = (
    "зцілення",
    "сили",
    "спритності",
    "мудрості",
    "захисту",
    "нічного зору",
    "вогню",
    "крижаного подиху",
    "удачі",
    "невидимості",
)

_RARITIES = ("Мале", "Звичайне", "Міцне", "Рідкісне", "Королівське")

POTIONS = tuple(
    Potion(
        number=index + 1,
        name=f"{rarity} зілля {effect}",
        ingredients=INGREDIENTS[index * 4:index * 4 + 4],
        price=20 + (index % 5) * 5,
    )
    for index, (rarity, effect) in enumerate(
        (rarity, effect)
        for rarity in _RARITIES
        for effect in _EFFECTS
    )
)

POTIONS_BY_NUMBER = {potion.number: potion for potion in POTIONS}
