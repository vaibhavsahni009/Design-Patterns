"""
GoF-style Iterator — classic has_next() + next() approach.
next() both advances AND returns the current item (side effect).
"""
from abc import ABC, abstractmethod


class IIterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self):
        pass


class ICollection(ABC):
    @abstractmethod
    def get_iterator(self) -> IIterator:
        pass


# --- List-backed collection ---

class Bag(ICollection):
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get_iterator(self) -> IIterator:
        return BagIterator(self.items)


class BagIterator(IIterator):
    def __init__(self, items: list):
        self.items = items
        self.idx = 0

    def has_next(self) -> bool:
        return self.idx < len(self.items)

    def next(self):
        item = self.items[self.idx]
        self.idx += 1          # advance AND return — GoF style
        return item


# --- Dict-backed collection ---

class SpellBook(ICollection):
    def __init__(self):
        self.spells = {}       # {name: power}

    def add(self, name: str, power: int):
        self.spells[name] = power

    def get_iterator(self) -> IIterator:
        return SpellBookIterator(self.spells)


class SpellBookIterator(IIterator):
    def __init__(self, spells: dict):
        self.items = list(spells.items())   # convert to list of (name, power) tuples
        self.idx = 0

    def has_next(self) -> bool:
        return self.idx < len(self.items)

    def next(self):
        item = self.items[self.idx]
        self.idx += 1
        return item


# --- Client code — same loop for both collections ---

def print_all(iterator: IIterator):
    while iterator.has_next():
        print(iterator.next())


bag = Bag()
bag.add("Sword")
bag.add("Shield")
bag.add("Potion")

spellbook = SpellBook()
spellbook.add("Fireball", 80)
spellbook.add("Heal", 50)
spellbook.add("Freeze", 65)

print("--- Bag (list) ---")
print_all(bag.get_iterator())

print("\n--- SpellBook (dict) ---")
print_all(spellbook.get_iterator())
