"""
Pythonic Iterator — uses __iter__ and __next__ protocol.
This is what powers Python's built-in for loops.
No has_next() needed — StopIteration signals the end.
"""


# --- List-backed collection ---

class Bag:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __iter__(self):
        return BagIterator(self.items)   # returns the iterator object


class BagIterator:
    def __init__(self, items: list):
        self.items = items
        self.idx = 0

    def __iter__(self):
        return self    # iterator is its own iterable

    def __next__(self):
        if self.idx >= len(self.items):
            raise StopIteration    # signals end of iteration to for loop
        item = self.items[self.idx]
        self.idx += 1
        return item


# --- Dict-backed collection ---

class SpellBook:
    def __init__(self):
        self.spells = {}    # {name: power}

    def add(self, name: str, power: int):
        self.spells[name] = power

    def __iter__(self):
        return SpellBookIterator(list(self.spells.items()))


class SpellBookIterator:
    def __init__(self, items: list):
        self.items = items
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx >= len(self.items):
            raise StopIteration
        item = self.items[self.idx]
        self.idx += 1
        return item


# --- Client code — native for loop works directly ---

bag = Bag()
bag.add("Sword")
bag.add("Shield")
bag.add("Potion")

spellbook = SpellBook()
spellbook.add("Fireball", 80)
spellbook.add("Heal", 50)
spellbook.add("Freeze", 65)

print("--- Bag (list) ---")
for item in bag:
    print(item)

print("\n--- SpellBook (dict) ---")
for name, power in spellbook:
    print(f"{name}: power {power}")

print("\n--- Python also supports list() and unpacking on iterables ---")
print(list(bag))
first, *rest = bag
print(f"First item: {first}, Rest: {rest}")

print("\n--- Generator shortcut (even more Pythonic) ---")
# For simple cases, a generator expression is often enough
class BagSimple:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return (item for item in self.items)   # generator — one line!

simple = BagSimple(["Axe", "Rope", "Torch"])
for item in simple:
    print(item)
