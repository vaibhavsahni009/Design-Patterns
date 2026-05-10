# Decorator Pattern

## Intent
Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

## The Problem
You need to add behavior to objects in various combinations. Subclassing leads to a combinatorial explosion of classes — one for every possible combination of features.

## The Solution
Wrap objects in decorator objects that share the same interface. Each decorator adds its behavior and delegates to the wrapped object. Decorators can be stacked in any order.

> The decorated object still IS-A the base type. Its identity doesn't change — only its behavior is extended.

## Structure

```
Component (ABC)
├── ConcreteComponent          ← the real object
└── BaseDecorator (ABC)        ← extends Component, wraps a Component
     ├── ConcreteDecoratorA
     └── ConcreteDecoratorB
```

## Components

| Component | Role |
|---|---|
| **Component** | Abstract base — defines the interface |
| **ConcreteComponent** | The base object being decorated |
| **BaseDecorator** | Extends Component AND holds a Component reference (is-a + has-a) |
| **ConcreteDecorator** | Adds specific behavior, delegates the rest to wrapped object |

## Key Mechanics

```python
class BaseDecorator(Component):
    def __init__(self, component: Component):
        self.component = component      # has-a

    # is-a Component, so it satisfies the same interface
```

```python
class ConcreteDecoratorA(BaseDecorator):
    def operation(self):
        result = self.component.operation()   # delegate first
        return result + self.added_behavior() # then add own behavior
```

## Stacking

```python
obj = ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent()))
obj.operation()
# execution order: B → A → ConcreteComponent → A → B
```

## Order Matters (Sometimes)
- **Commutative operations** (addition, concatenation): order doesn't affect the final value
- **Non-commutative operations** (compression+encryption, auth+logging): order changes behavior significantly

Always think about whether your decorators have dependencies on each other.

## When to Use
- Add behavior to objects without affecting other objects of the same class
- Extension by subclassing is impractical due to combinatorial explosion
- Behavior needs to be added/removed at runtime

## When NOT to Use
- Order of wrapping is hard to reason about — consider a different pattern
- Too many small decorator classes become hard to debug

## Python Note
Python has a built-in `@decorator` syntax for functions, but that's different from the Decorator *pattern*. The pattern applies to objects/classes and uses composition. Don't confuse the two.

## Relation to Other Patterns
- **Strategy** — both use composition, but Strategy replaces the core algorithm; Decorator wraps and extends it
- **Composite** — both use recursive composition; Decorator adds responsibilities, Composite treats groups as single objects
