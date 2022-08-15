from enum import Enum, auto
from decimal import Decimal

from yasf import sf, structured_sentinel


def test_simple():

    s = sf("user", name="James", id=123)
    print(s)
    assert s == 'user ' + structured_sentinel + ' {"name": "James", "id": 123} ' + structured_sentinel


def test_complex():
    class Material(Enum):
        wood = auto()
        paper = auto()

    s = sf("user", "person", name="James", id=123, exists=True, balance=Decimal(2.48), material=Material.wood)
    print(s)
    assert s == 'user,person ' + structured_sentinel + ' {"name": "James", "id": 123, "exists": true, "balance": 2.48, "material": "wood"} ' + structured_sentinel
