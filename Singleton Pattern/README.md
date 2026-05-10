# Singleton Pattern

## Intent
Ensure a class has only one instance and provide a global point of access to it.

## The Problem
Some resources should exist exactly once — a database connection pool, a logger, a config manager. Multiple instances would cause conflicts, wasted resources, or inconsistent state.

## The Solution
Control instantiation so only one object is ever created. Return the same instance on every subsequent request.

## Structure

```
Singleton
├── _instance: Singleton = None    ← class-level, shared across all calls
├── __new__(cls)                   ← intercepts creation, returns existing if present
└── some_method()
```

## Two Approaches in Python

### Approach 1: Override `__new__` (Pythonic)

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)   # create once
        return cls._instance                        # always return same

    def __init__(self):
        if not hasattr(self, 'initialized'):        # guard: __init__ runs every time
            self.initialized = True
            self.value = "set once"
```

Called like a normal class — no special method needed:
```python
a = Singleton()
b = Singleton()
print(a is b)   # True
```

### Approach 2: `getInstance()` classmethod (Java-style)

```python
class Singleton:
    _instance = None

    def __init__(self, config):
        self.config = config

    @classmethod
    def getInstance(cls, config=None):
        if cls._instance is None:
            cls._instance = cls(config)    # create with params only once
        return cls._instance
```

```python
s1 = Singleton.getInstance("config_value")
s2 = Singleton.getInstance()               # config ignored, returns existing
print(s1 is s2)   # True
```

## The `__new__` vs `__init__` Gotcha

`__new__` creates the object. `__init__` initializes it. Both are called on every `ClassName()` call — even when `__new__` returns the existing instance.

Without a guard, `__init__` will **reinitialize** the singleton on every call:

```python
# BAD — state gets reset every time
def __init__(self, url):
    self.url = url   # overwrites on every call!

# GOOD — initialize only once
def __init__(self, url):
    if not hasattr(self, 'url'):
        self.url = url
```

## Verification

```python
a = Singleton()
b = Singleton()
print(a is b)        # True  — same object in memory
print(id(a) == id(b))  # True  — same memory address
```

## When to Use
- Exactly one instance must coordinate actions across the system
- Shared resource: logger, config, connection pool, cache, thread pool
- Global state that must be consistent

## When NOT to Use
- Introduces global state — makes testing harder (hard to reset between tests)
- Hides dependencies — classes that use a singleton don't declare it as a dependency
- Violates Single Responsibility — manages its own lifecycle AND does its job

> Singleton is one of the most overused patterns. Prefer dependency injection where possible.

## Python Note
Python modules are singletons by nature — a module is only imported once and cached. For simple cases, a module-level variable is often enough instead of a Singleton class.

## Relation to Other Patterns
- **Abstract Factory / Builder / Prototype** — these are often implemented as Singletons
- **Flyweight** — similar goal of sharing instances, but Flyweight manages many shared objects; Singleton manages exactly one
