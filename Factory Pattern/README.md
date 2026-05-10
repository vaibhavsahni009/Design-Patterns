# Factory Patterns

## Simple Factory

### Intent
Encapsulate object creation logic in one place. The client asks for an object by type without knowing the concrete class.

### Structure

```
Client ──► SimpleFactory.create(type) ──► ConcreteProductA
                                     └──► ConcreteProductB
```

### Key Mechanics

```python
class SimpleFactory:
    @staticmethod
    def create(type: str) -> Product:
        if type == "A":
            return ConcreteProductA()
        elif type == "B":
            return ConcreteProductB()
        else:
            raise ValueError(f"Unknown type: {type}")
```

### Tradeoff
Adding a new type requires modifying `SimpleFactory` — violates the **Open/Closed Principle**. Every new product = open the factory and add an `elif`.

---

## Factory Method Pattern

### Intent
Define an interface for creating objects, but let subclasses decide which class to instantiate. The creation is deferred to subclasses.

### Structure

```
Creator (ABC)
├── create_product() → abstract    ← subclasses override this
└── some_operation()               ← uses create_product(), works for all subclasses
     ├── ConcreteCreatorA → creates ProductA
     └── ConcreteCreatorB → creates ProductB
```

### Key Mechanics

```python
class Creator(ABC):
    @abstractmethod
    def create_product(self) -> Product:
        pass

    def describe(self):                     # concrete method
        p = self.create_product()           # calls the factory method
        p.do_something()                    # works without knowing concrete type


class ConcreteCreatorA(Creator):
    def create_product(self) -> Product:
        return ProductA()
```

### Open/Closed Compliance
Adding a new product = add a new `ConcreteCreator` subclass. Existing code untouched.

### Client Code Comparison

```python
# Simple Factory — client passes a string
product = SimpleFactory.create("A")

# Factory Method — client picks a creator class
product = ConcreteCreatorA().create_product()
```

---

## Comparison

| | Simple Factory | Factory Method |
|---|---|---|
| **Structure** | One class, if/elif | Abstract creator + concrete subclasses |
| **Adding new type** | Modify existing factory | Add new subclass |
| **Open/Closed** | ❌ Violated | ✅ Respected |
| **Client knows** | String type | Which creator to use |
| **GoF Pattern** | No (common idiom) | Yes |

---

## When to Use
- **Simple Factory** — small number of types, unlikely to change, just want to centralize creation logic
- **Factory Method** — types will grow over time, want to follow Open/Closed, subclasses should control what gets created

## Relation to Other Patterns
- **Abstract Factory** — uses multiple Factory Methods to create families of related objects
- **Template Method** — Factory Method is a specialization of Template Method applied to object creation
