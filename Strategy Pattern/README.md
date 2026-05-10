# Strategy Pattern

## Intent
Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from the clients that use it.

## The Problem
Inheritance breaks down when behaviors cut across class hierarchies in different combinations. You end up duplicating code or creating an explosion of subclasses.

## The Solution
Extract behaviors into separate classes and **compose** them into the context object rather than inheriting them.

> Favor composition over inheritance.

## Structure

```
Context
├── has-a → BehaviorA (interface)
│            ├── ConcreteA1
│            └── ConcreteA2
└── has-a → BehaviorB (interface)
             ├── ConcreteB1
             └── ConcreteB2
```

## Components

| Component | Role |
|---|---|
| **Context** | Holds references to behavior objects. Delegates work to them. |
| **Strategy Interface** | Defines the contract for a behavior (ABC + @abstractmethod) |
| **Concrete Strategy** | A specific implementation of the behavior |

## Key Mechanics

```python
class Context:
    def __init__(self, behavior: IBehavior):
        self.behavior = behavior        # composed in, not inherited

    def do_something(self):
        self.behavior.execute()         # delegates to strategy

    def set_behavior(self, b: IBehavior):
        self.behavior = b               # swap at runtime
```

## Runtime Behavior Change
A key feature — behaviors can be swapped at runtime without changing the context:

```python
ctx = Context(ConcreteA1())
ctx.do_something()          # uses A1

ctx.set_behavior(ConcreteA2())
ctx.do_something()          # now uses A2, same context object
```

## When to Use
- Multiple classes differ only in their behavior
- You need different variants of an algorithm
- You want to avoid conditional logic (`if type == X: ... elif type == Y: ...`)
- Behavior needs to change at runtime

## When NOT to Use
- Only one or two behaviors that never change — overkill
- Simple functions work fine — in Python, passing a function is often enough

## Python Note
Python has no formal interfaces. Use `ABC + @abstractmethod` to simulate them. Without `ABC`, the decorator has no effect and enforcement is lost.

## Relation to Other Patterns
- **Similar to Decorator** — both use composition, but Strategy changes the *core behavior* while Decorator *adds* behavior on top
- **Similar to State** — same structure, different intent. Strategy is chosen by the client; State changes itself based on internal conditions
