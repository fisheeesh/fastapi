from typing import Any


class City:
    def __init__(self, name, location):
        self.name = name
        self.location = location


text: str = "value"
pert: int = 90
temp: float = 37.5

number: int | float = 12

digits: list[int] = [1, 2, 3, 4, 5]

table_5: tuple[int, ...] = (5, 10, 15, 20, 25)

chiangrai = City("chiang rai", 57100)
city_temp: tuple[City, float] = (chiangrai, 20.5)

shipment: dict[str, Any] = {
    "id": 12701,
    "weight": 1.2,
    "content": "wooden table",
    "status": "in trnasit",
}


def root(num: int | float, exp: float | None = 0.5) -> float:
    return pow(num, 0.5 if exp is None else exp)


root_25 = root(25)
