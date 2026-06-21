# State Pattern

## Intent
Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

## The Problem
An object behaves differently depending on its current state. Without State pattern, you end up with large `if/elif` ladders in every method:

```python
def enter(self):
    if self.state == "locked":
        raise Exception("locked!")
    elif self.state == "unlocked":
        self.state = "locked"
    elif self.state == "processing":
        raise Exception("processing!")
```

Every new state means modifying every method. Adding states becomes risky and messy.

## The Solution
Extract each state into its own class. Each state class handles all events for that state. The context delegates to the current state object. Transitions happen by swapping the state object.

## Structure

```
Gate (Context)
└── state: IGateState
      ├── LockedState
      ├── UnlockedState
      └── ProcessingState
```

Each state holds a reference back to the context so it can trigger transitions.

## Components

| Component | Role |
|---|---|
| **Context** | Holds current state. Delegates all events to it. Exposes `changeState()`. |
| **State Interface** | Defines all events the context can receive |
| **Concrete State** | Implements behavior for each event in that state. Triggers transitions. |

## Key Mechanics

```python
from __future__ import annotations   # fixes forward reference — states defined before Gate

class IGateState(ABC):
    def __init__(self, gate: Gate):   # Gate referenced before defined — needs __future__
        self.gate = gate

    @abstractmethod
    def pay(self): pass
    @abstractmethod
    def enter(self): pass


class LockedState(IGateState):
    def pay(self):
        print("Starting payment...")
        self.gate.changeState(ProcessingState(self.gate))   # triggers transition

    def enter(self):
        raise Exception("Gate locked!")


class Gate:
    def __init__(self):
        self.state = LockedState(self)   # initial state

    def pay(self):   self.state.pay()    # delegate to current state
    def enter(self): self.state.enter()

    def changeState(self, state: IGateState):
        self.state = state               # swap state object
```

## State Transition Diagram

```
                 pay()
    ┌─────────────────────────────►  ProcessingState
    │                                  │          │
LockedState  ◄─────────────────────────┘          │
    ▲              payFailed()                     │ payOk()
    │                                              │
    └──────────────────────────────────────────────┘
    enter()                        UnlockedState
                                       │
                               enter() │
                                       ▼
                                  LockedState
```

## Forward Reference Fix
States reference `Gate` in their `__init__`, but `Gate` is defined after the states. Fix with:

```python
from __future__ import annotations
```

This makes all annotations strings lazily evaluated — no `NameError` at class definition time. The alternative is string annotations:
```python
def __init__(self, gate: 'Gate'):
```

## State vs Strategy

Structurally identical — both use composition and swap behavior objects. The intent differs:

| | State | Strategy |
|---|---|---|
| **Who changes behavior** | Object changes itself | Client swaps from outside |
| **Transitions** | Automatic, driven by state logic | Manual, client decides |
| **States aware of each other** | Yes — LockedState creates ProcessingState | No — strategies are independent |
| **Hollywood Principle** | Yes — state drives transitions | No |

## Handling Invalid Transitions
Two approaches:

**Raise exception** — illegal action in current state is an error:
```python
def enter(self):   # in LockedState
    raise Exception("Gate is locked!")
```

**Ignore silently** — illegal action just does nothing:
```python
def pay(self):    # in UnlockedState
    print("Already unlocked, ignoring")
```

Choose based on whether the invalid action represents a bug (raise) or expected user behavior (ignore).

## When to Use
- Object behavior depends heavily on its state and changes at runtime
- Large conditional blocks checking state in every method
- State transitions need to be explicit and auditable
- Adding new states should not require modifying existing ones

## Real-World Analogies
- **Metro gate** — locked, processing, unlocked. Each state handles coin insert and push differently
- **Traffic light** — red, yellow, green. Each state has a timer and transitions automatically
- **Order lifecycle** — placed, confirmed, shipped, delivered, cancelled. Each state allows different actions
- **TCP connection** — listen, syn-sent, established, close-wait, closed

## Python Note
`from __future__ import annotations` is the cleanest fix for forward references in type hints. It defers evaluation of all annotations to runtime, so classes can reference types defined later in the file.

## Relation to Other Patterns
- **Strategy** — same structure, different intent. Strategy is chosen by client; State transitions itself
- **Singleton** — State objects are often Singletons since they carry no instance-specific data
- **Flyweight** — State objects with no instance data can be shared (same as Singleton approach)
