# Null Object Pattern

## Intent
Provide a default object with do-nothing behavior as a substitute for `None`. Eliminates null checks by making "absence of behavior" an explicit, safe object.

## The Problem
When an object is optional, you end up with null checks scattered everywhere:

```python
def movement(self):
    if self.behavior is not None:   # repeated everywhere
        self.behavior.moveUp()
    if self.behavior is not None:
        self.behavior.moveDown()
    ...
```

With `None`, any forgotten check throws an `AttributeError` at runtime.

## The Solution
Instead of `None`, use a Null Object that implements the same interface but does nothing. The caller never needs to check — it always has a valid object.

```python
def movement(self):
    self.behavior.moveUp()    # always safe — real or null object
    self.behavior.moveDown()
    self.behavior.moveLeft()
    self.behavior.moveRight()
```

## Structure

```
IMovementBehaviour (interface)
├── WalkMovementBehaviour   ← real behavior
├── RunMovementBehaviour    ← real behavior
└── NoMovementBehaviour     ← null object — does nothing silently
```

## Components

| Component | Role |
|---|---|
| **Interface** | Defines the contract all implementations must follow |
| **Real Object** | Implements actual behavior |
| **Null Object** | Implements interface with empty/no-op methods — safe default |
| **Client** | Uses interface, never checks for None |

## Key Mechanics

```python
class IMovementBehaviour(ABC):
    @abstractmethod
    def moveUp(self): pass
    # ... other directions


class NoMovementBehaviour(IMovementBehaviour):
    def moveUp(self):    pass   # silent — no print, no error, nothing
    def moveDown(self):  pass
    def moveLeft(self):  pass
    def moveRight(self): pass


class User:
    def __init__(self, behavior: IMovementBehaviour):
        self.behavior = behavior

    def movement(self):
        self.behavior.moveUp()      # no null check needed
        self.behavior.moveDown()
        self.behavior.moveLeft()
        self.behavior.moveRight()
```

## The Key Rule — True Silence
A Null Object must do **nothing** — no output, no side effects, no exceptions. If it prints "No movement" it's no longer transparent.

```python
# WRONG — not a true null object
class NoMovementBehaviour(IMovementBehaviour):
    def moveUp(self):
        print("No Up")   # caller can detect this — defeats the purpose

# CORRECT — truly silent
class NoMovementBehaviour(IMovementBehaviour):
    def moveUp(self): pass
```

## Without Null Object vs With

```python
# Without — null checks everywhere, easy to forget one
if user.behavior is not None:
    user.behavior.moveUp()

# With Null Object — always safe, no checks
user.behavior.moveUp()
```

## Null Object vs None

| | None | Null Object |
|---|---|---|
| **Calling methods** | AttributeError | Works silently |
| **Null checks needed** | Yes, everywhere | No |
| **Polymorphism** | No | Yes |
| **Explicit intent** | No | Yes — "no behavior" is intentional |

## When to Use
- An object is optional and its absence should be a safe no-op
- Null checks are scattered across the codebase
- "Doing nothing" is a valid, expected behavior worth making explicit
- Testing — inject a NullLogger, NullCache, NullNotifier instead of mocking

## Common Use Cases
- **NullLogger** — no-op logger for tests or silent environments
- **NullCache** — always misses, returns nothing — for environments without caching
- **NullNotifier** — swallows all notifications silently
- **NoMovementBehaviour** — frozen/stunned characters in games
- **NullEventHandler** — default handler that ignores events

## Python Note
Python's `None` is a common source of `AttributeError` bugs. Null Object is the pattern-level fix. For simple cases, Python's `or` operator can provide defaults:

```python
behavior = user.behavior or NoMovementBehaviour()
```

But this still requires the check at the assignment site. True Null Object eliminates it at the source by never assigning `None` in the first place.

## Relation to Other Patterns
- **Strategy** — Null Object is often a "do nothing" Strategy. NoMovementBehaviour is a Strategy with empty implementation.
- **Proxy** — structurally similar, but Proxy controls access; Null Object provides safe default behavior
- **State** — Null Object can represent a neutral/inactive state in a State machine
