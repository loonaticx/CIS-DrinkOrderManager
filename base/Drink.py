from dataclasses import dataclass


@dataclass
class Drink:
    """
    A local "Drink" object, not dependent on the database.
    """
    name: str
    price: float
    color: str = "Colorless"
    description: str = "No description."
