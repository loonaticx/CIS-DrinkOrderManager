"""
Generates arbitrary drinks
"""
import random
from dataclasses import dataclass

from base.DatabaseManager import *

# Random colors
drinkColors = [
    "Red",
    "Blue",
    "Purple",
    "Green",
    "Rainbow",
    "Orange",
    "Blueberry",
    "Salmon",
    "Invisible"
]

drinkNames = [
    "Mojito",
    "Martini",
    "Cosmopolitan",
    "Whiskey Sour",
    "Margarita",
    "Pina Colada",
    "Long Island Iced Tea",
    "Old Fashioned",
    "Gamer Juice",
    "Daiquiri",
    "Bloody Mary",
    "Moscow Mule",
    "Mai Tai",
    "Manhattan",
    "Gin and Tonic",
    "Screwdriver",
    "Russian",
    "Tequila Sunrise",
    "Lagoon",
    "Mimosa",
    "Irish Coffee",
    "Tom Collins",
    "Sazerac",
    "Singapore Sling",
    "Bellini",
    "Hurricane",
    "Sangria",
    "Caipirinha",
    "Hot Toddy",
    "Pisco Sour",
    "Coca-Cola",
    "Pepsi",
    "Sprite",
    "Dr Pepper",
    "Mountain Dew",
    "Fanta",
    "7UP",
    "Root Beer",
    "Ginger Ale",
    "Orange Crush",
    "Cream Soda",
    "Sunkist",
    "Barq's",
    "Canada Dry",
    "A&W",
    "Schweppes",
    "Mug Root Beer",
    "Crush",
    "Sierra Mist",
    "Water",
]


def generateDrinkDescription():
    adjectives = [
        "Refreshing",
        "Tangy",
        "Fruity",
        "Citrusy",
        "Smooth",
        "Creamy",
        "Bubbly",
        "Spicy",
        "Exotic",
        "Soothing",
        "Zesty",
        "Satisfying",
        "Elegant",
        "Aromatic",
        "Bold",
        "Tropical",
        "Icy",
        "Warm",
        "Velvety",
        "Seductive"
    ]

    flavors = [
        "with hints of lime",
        "infused with ginger",
        "featuring a touch of mint",
        "bursting with tropical fruit flavors",
        "accentuated by a splash of coconut",
        "balanced with a twist of lemon",
        "enhanced by a dash of cinnamon",
        "highlighted by a zing of orange",
        "complemented by a sprig of rosemary",
        "featuring a burst of pineapple",
        "tingling with a hint of chili",
        "elevated with a drop of honey",
        "accented by a touch of vanilla",
        "rounded out with a hint of nutmeg",
        "spiced with a touch of cardamom",
        "perfumed with a dash of lavender",
        "tinged with a hint of berries",
        "infused with a splash of cranberry",
        "enlivened by a dash of grenadine",
        "perfected with a squeeze of grapefruit"
    ]

    adjective = random.choice(adjectives)
    flavor = random.choice(flavors)

    return f"A {adjective.lower()} drink {flavor}."


@dataclass
class DrinkGenerator:

    # 60% chance to have a color
    colorChance: int = 60

    # 90% chance to have a description
    descChance: int = 90

    # cheapest price to most expensive price
    costBounds = (0.01, 420.69)

    def _generateDrinkEntry(self) -> DrinkDBEntry:
        cost = round(random.uniform(*self.costBounds), 2)
        color = ""
        if random.random() * 100 <= self.colorChance:
            color = random.choice(drinkColors)

        drink = Drink(name = random.choice(drinkNames), price = cost, color = color)

        if random.random() * 100 <= self.descChance:
            drink.description = generateDrinkDescription()
        return DrinkDBEntry(drink)

    def generateDrinks(self, drinksAmt: int):
        generatedDrinks = []
        for _ in range(drinksAmt):
            generatedDrinks.append(self._generateDrinkEntry())
        return generatedDrinks


if __name__ == "__main__":
    """
    Driver code; when ran, will insert arbitrary drink entries into the database.
    """
    drinksAmt = 10

    DrinkGenerator().generateDrinks(drinksAmt)
    print(f"Generated {drinksAmt} drinks!")
