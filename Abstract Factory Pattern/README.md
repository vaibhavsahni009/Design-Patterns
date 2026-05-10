# Abstract Factory Pattern

## Intent
Provide an interface for creating **families of related objects** without specifying their concrete classes. Guarantees that products from the same factory are compatible with each other.

## The Problem
You need to create groups of related objects that must work together. Using individual factories risks mixing incompatible products (e.g., laser ink with an inkjet printer).

## The Solution
One factory interface produces an entire family of related products. Swap the factory, get a different but internally consistent family.

## Structure

```
AbstractFactory (ABC)
├── create_product_a() → AbstractProductA
└── create_product_b() → AbstractProductB

ConcreteFactory1                    ConcreteFactory2
├── create_product_a() → ProductA1  ├── create_product_a() → ProductA2
└── create_product_b() → ProductB1  └── create_product_b() → ProductB2

Client
└── uses AbstractFactory (never knows which concrete factory it has)
```

## Components

| Component | Role |
|---|---|
| **AbstractFactory** | Interface declaring creation methods for each product type |
| **ConcreteFactory** | Creates a specific family of products |
| **AbstractProduct** | Interface for each product type |
| **ConcreteProduct** | A specific product belonging to one family |
| **Client** | Uses only abstract factory and product interfaces |

## Key Mechanics

```python
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class Client:
    def __init__(self, factory: AbstractFactory):
        self.product_a = factory.create_product_a()   # doesn't know concrete type
        self.product_b = factory.create_product_b()   # guaranteed compatible
```

## Swapping Families

```python
# Entire product family changes by swapping one factory
client = Client(ConcreteFactory1())   # gets Family 1
client = Client(ConcreteFactory2())   # gets Family 2 — client code unchanged
```

## Factory Method vs Abstract Factory

| | Factory Method | Abstract Factory |
|---|---|---|
| **Creates** | One product type | A family of related products |
| **How** | Subclass overrides one method | Separate factory class with multiple methods |
| **Use when** | One thing to create | Multiple related things to create together |

Abstract Factory is essentially a collection of Factory Methods grouped by product family.

## When to Use
- System needs to be independent of how its products are created
- Products must be used together and compatibility must be enforced
- You want to swap entire product families at once

## Real-World Analogies
- UI theme kits — dark theme factory creates dark buttons, dark inputs, dark modals (all consistent)
- Printer + ink — laser factory gives laser printer + laser ink; inkjet factory gives inkjet printer + inkjet ink
- Cross-platform UI — Windows factory creates Windows-style widgets; Mac factory creates Mac-style widgets

## Relation to Other Patterns
- **Factory Method** — Abstract Factory is built from multiple Factory Methods
- **Singleton** — Concrete factories are often Singletons since only one instance is needed
