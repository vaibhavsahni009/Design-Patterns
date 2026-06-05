# Bridge Pattern

## Intent
Decouple an abstraction from its implementation so that the two can vary independently. Prevents a combinatorial explosion of subclasses when two dimensions of variation exist.

## The Problem
When a class has two independent dimensions of variation, inheritance creates a class explosion:

```
2 shapes × 2 renderers = 4 classes
3 shapes × 3 renderers = 9 classes
4 shapes × 4 renderers = 16 classes
```

Every new shape requires new renderer-specific subclasses and vice versa. The hierarchies are tightly coupled.

## The Solution
Separate the two dimensions into independent hierarchies and **bridge them with composition**. One hierarchy holds a reference to the other.

```
Shapes (abstraction)        Renderers (implementation)
├── Circle                  ├── VectorRenderer
└── Square                  └── RasterRenderer
     └── has-a ──────────────────────────────►
```

Now adding a new shape or renderer doesn't affect the other hierarchy. Combinations are achieved at runtime by composing:
```python
Circle(VectorRenderer())
Circle(RasterRenderer())
Square(VectorRenderer())   # no new classes needed
```

## Components

| Component | Role |
|---|---|
| **Abstraction** | High-level interface (Shape). Holds reference to Implementation. |
| **Refined Abstraction** | Concrete subclasses of Abstraction (Circle, Square) |
| **Implementation Interface** | Interface for the implementation hierarchy (IRenderer) |
| **Concrete Implementation** | Specific implementations (VectorRenderer, RasterRenderer) |

## Key Mechanics

```python
class Shape(ABC):
    def __init__(self, renderer: IRenderer):
        self.renderer = renderer        # bridge — holds implementation reference

    @abstractmethod
    def renderShape(self, color):
        pass


class Circle(Shape):
    def __init__(self, renderer: IRenderer):
        super().__init__(renderer)      # delegates storage to base class

    def renderShape(self, color):
        self.renderer.render("Circle", color)   # delegates rendering to implementation
```

## Abstract Class vs Interface

In Bridge, the abstraction side typically uses an **abstract class** (not a pure interface) because it has:
- Shared state (`self.renderer`)
- Shared initialization logic (`__init__`)

The implementation side uses a **pure interface** (ABC with only abstract methods) because it's a contract with no shared state.

In Java:
```java
abstract class Shape {           // abstract class — has state
    protected IRenderer renderer;
    public Shape(IRenderer r) { this.renderer = r; }
}

interface IRenderer {            // interface — pure contract
    void render(String name, String color);
}
```

## Bridge vs Strategy
Both use composition and look structurally similar:

| | Bridge | Strategy |
|---|---|---|
| **Dimensions** | Two hierarchies varying independently | One behavior swapped in context |
| **Intent** | Decouple abstraction from implementation | Make algorithms interchangeable |
| **Design time** | Planned upfront for two varying dimensions | Can be applied to existing class |

Bridge is designed into the architecture from the start. Strategy is applied when you need swappable algorithms.

## When to Use
- Class has two or more independent dimensions of variation
- Both abstraction and implementation should be extensible via subclassing
- Changes in implementation should not affect the abstraction and vice versa
- Want to hide implementation details from clients completely

## Real-World Analogies
- **TV remote and TV** — remote (abstraction) works with any TV brand (implementation). Samsung remote and LG remote both control TVs, but the TV internals vary independently
- **Device and OS** — same app abstraction runs on different OS implementations
- **Shape and renderer** — same shape logic, different rendering backends (OpenGL, DirectX, SVG)

## Python Note
Python's duck typing means the bridge often works without formal interfaces — any object with the right methods works as an implementation. However, using `ABC + @abstractmethod` makes the contract explicit and catches missing implementations early.

## Relation to Other Patterns
- **Strategy** — similar structure, but Strategy has one varying dimension; Bridge has two
- **Adapter** — Adapter makes incompatible interfaces work together after the fact; Bridge is designed upfront to allow both sides to vary
- **Abstract Factory** — can be used to create and configure a Bridge
