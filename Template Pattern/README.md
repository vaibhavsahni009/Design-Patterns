# Template Method Pattern

## Intent
Define the skeleton of an algorithm in a base class, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing its overall structure.

## The Problem
Multiple classes share the same algorithm structure but differ in specific steps. Duplicating the overall flow in each subclass leads to code repetition and makes it hard to change the algorithm consistently.

## The Solution
Put the algorithm skeleton in a base class as a **template method**. Extract the varying steps as abstract or virtual methods. Subclasses implement or override only those steps.

> Hollywood Principle: "Don't call us, we'll call you." The base class calls the subclass methods, not the other way around.

## Structure

```
DataProcessor (ABC)
├── process()           ← template method — owns the flow, final
├── read_data()         ← concrete — shared default behavior
├── process_data()      ← abstract — subclasses MUST implement
├── before_process()    ← hook (virtual) — subclasses CAN override
└── save_result()       ← concrete — shared default behavior

CSVProcessor(DataProcessor)
└── process_data()      ← implements the abstract step

JSONProcessor(DataProcessor)
├── process_data()      ← implements the abstract step
└── before_process()    ← overrides the hook for extra validation
```

## Components

| Component | Role |
|---|---|
| **Template Method** | Defines the algorithm flow. Calls abstract and hook methods. |
| **Abstract Method** | Step that MUST be implemented by subclasses (`@abstractmethod`) |
| **Hook Method** | Step with a default (usually empty) implementation. Subclasses CAN override. |
| **Concrete Method** | Shared behavior in the base class. Subclasses inherit as-is. |

## Key Mechanics

```python
class DataProcessor(ABC):

    def process(self):          # template method — skeleton of the algorithm
        self.read_data()
        self.before_process()   # hook — optional
        self.process_data()     # abstract — required
        self.save_result()

    def read_data(self):        # concrete — shared default
        print("Reading data")

    def save_result(self):      # concrete — shared default
        print("Saving results")

    def before_process(self):   # hook (virtual) — empty default, can override
        pass

    @abstractmethod
    def process_data(self):     # abstract — must override
        pass
```

## Abstract Method vs Hook (Virtual Method)

| | Abstract Method | Hook (Virtual Method) |
|---|---|---|
| **Has body?** | No (`pass` + `@abstractmethod`) | Yes (default implementation) |
| **Must override?** | Yes — enforced by Python | No — optional |
| **Use when** | Step is mandatory and varies | Step is optional or has a sensible default |

In Python, every method is virtual by default. `@abstractmethod` is the only explicit marker — it forces subclasses to implement the method.

## Template Method vs Strategy

Both solve varying behavior, but with different mechanisms:

| | Template Method | Strategy |
|---|---|---|
| **Mechanism** | Inheritance | Composition |
| **Varies** | Steps within an algorithm | The entire algorithm |
| **Flexibility** | Less — locked into base class structure | More — swap behavior at runtime |
| **Hollywood Principle** | Yes — base calls subclass | No — client calls strategy |

Template Method is simpler but less flexible. Strategy allows runtime swapping but requires more setup.

## When to Use
- Multiple classes share the same algorithm structure but differ in specific steps
- Common behavior should be factored into a single place to avoid duplication
- You want to control which parts of an algorithm subclasses can change
- Framework defines the flow, applications fill in the steps (Django views, JUnit lifecycle)

## Real-World Analogies
- **Frameworks** — Django class-based views define `dispatch()` flow, you implement `get()` and `post()`
- **JUnit** — test lifecycle: `setUp()` → `test()` → `tearDown()`. You implement `test()`, JUnit calls the rest
- **Recipe** — cooking steps are fixed (prepare, cook, serve), specific ingredients vary per dish
- **Build pipeline** — CI/CD: checkout → build → test → deploy. Each project fills in the steps differently

## Python Note
Python has no `virtual` keyword — all methods are overridable by default. The distinction between abstract and virtual (hook) is:
- `@abstractmethod` → abstract, must override
- Regular method with a body → virtual/hook, can override

## Relation to Other Patterns
- **Strategy** — both vary behavior, but Template Method uses inheritance; Strategy uses composition
- **Factory Method** — Factory Method is a specialization of Template Method for object creation
- **Hook** — hooks in Template Method are the same concept as hooks in frameworks and event systems
