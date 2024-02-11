from dataclasses import dataclass


@dataclass
class Drink:
    name: str
    price: float
    color: str = "Colorless"
    description: str = "No description."
