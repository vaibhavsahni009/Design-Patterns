# Iterator Pattern

## Intent
Provide a way to sequentially access elements of a collection without exposing its underlying structure.

## The Problem
Collections can be stored internally as lists, dicts, trees, graphs, or custom structures. Clients shouldn't need to know the internal structure to traverse them. Writing different traversal logic per collection couples the client to the implementation.

## The Solution
Extract traversal logic into an iterator object. The client calls the same interface regardless of the underlying collection type.

## Structure

```
Client ──► IIterator
               ├── BagIterator        ← iterates a list
               └── SpellBookIterator  ← iterates a dict

ICollection
├── Bag          ── get_iterator() → BagIterator
└── SpellBook    ── get_iterator() → SpellBookIterator
```

## Three Approaches

### Approach 1: 3-Method Style (explicit, clear separation)
```python
class InventoryIterator(ABC):
    def is_done(self) -> bool: ...   # are we finished?
    def get_item(self):  ...         # what are we looking at?
    def next(self): ...              # move forward

while not iterator.is_done():
    print(iterator.get_item())
    iterator.next()
```
Most readable. `get_item()` has no side effects. Must remember to call `next()` manually.

### Approach 2: GoF Style (has_next + next combined)
```python
class IIterator(ABC):
    def has_next(self) -> bool: ...  # is there a next element?
    def next(self): ...              # return current AND advance

while iterator.has_next():
    print(iterator.next())
```
Classic GoF pattern. `next()` advances AND returns — slight side effect, but common in Java/C#.

### Approach 3: Python Native Protocol (most Pythonic)
```python
class Collection:
    def __iter__(self):          # returns iterator object
        return MyIterator(self)

class MyIterator:
    def __iter__(self): return self
    def __next__(self):
        if done: raise StopIteration
        # return next item
```
Powers Python's `for` loop. `StopIteration` signals the end. Enables `list()`, unpacking, `zip()`, etc.

```python
for item in collection:    # just works
    print(item)
```

## Comparison

| | 3-Method | GoF (has_next) | Python Native |
|---|---|---|---|
| **Clarity** | High | Medium | High |
| **Side effects** | None in get_item | next() advances | __next__ advances |
| **for loop support** | No | No | Yes |
| **Python idioms** | No | No | Yes (list, zip, unpack) |
| **Interview recognition** | Good | Good (classic) | Best for Python |

## Key Insight — Same Client, Different Structures

```python
# List-backed and dict-backed collections, same client loop
def print_all(iterator):
    while iterator.has_next():
        print(iterator.next())

print_all(bag.get_iterator())        # list internally
print_all(spellbook.get_iterator())  # dict internally
```

Client doesn't know or care about the internal structure. That's the pattern's value.

## Generator Shortcut
For simple cases in Python, a generator is often enough:

```python
class Bag:
    def __iter__(self):
        return (item for item in self.items)   # one line!
```

Generators implement the iterator protocol automatically. Use them for simple sequential iteration. Use custom iterator classes when you need stateful, complex, or reusable traversal logic.

## When to Use
- Need to traverse a collection without exposing its structure
- Multiple traversal strategies needed for the same collection (forward, backward, filtered)
- Uniform interface needed for different collection types
- Decoupling traversal logic from the collection

## Real-World Analogies
- **Game inventory** — bag, spellbook, equipped slots all iterated the same way by the game loop
- **File system** — iterate files in a directory regardless of OS-level storage structure
- **Database cursor** — traverse query results without knowing the fetch strategy
- **Playlist** — next track regardless of shuffle or sequential mode

## Python Note
In Python, prefer the native `__iter__`/`__next__` protocol over GoF-style `has_next()`/`next()`. It integrates with the entire Python ecosystem — `for` loops, `list()`, `zip()`, `enumerate()`, comprehensions, and more all work automatically.

## Relation to Other Patterns
- **Composite** — Iterator is commonly used to traverse Composite trees
- **Factory Method** — collections often use Factory Method to create the right iterator
- **Visitor** — Iterator traverses, Visitor performs operations on each element during traversal
