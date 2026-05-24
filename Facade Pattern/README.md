# Facade Pattern

## Intent
Provide a simplified interface to a complex subsystem. Facade doesn't add new functionality — it makes the subsystem easier to use by hiding its complexity.

## The Problem
A subsystem is made up of many classes that must be coordinated in the right order. Clients shouldn't need to know about all these classes or their interactions — that's too much coupling and too much knowledge burden on the client.

## The Solution
Create a Facade class that wraps the subsystem and exposes only the high-level operations the client needs. The subsystem classes still exist and can be used directly if needed — the Facade just provides a simpler entry point.

## Structure

```
Client
  └── HomeTheaterFacade
        ├── Amplifier
        ├── DVDPlayer
        ├── Projector
        └── Lights
```

Client talks only to the Facade. Facade orchestrates the subsystem.

## Components

| Component | Role |
|---|---|
| **Facade** | Simplified interface over the subsystem. Delegates to subsystem classes. |
| **Subsystem Classes** | Do the actual work. Unaware of the Facade. Can still be used directly. |
| **Client** | Uses only the Facade. Decoupled from subsystem internals. |

## Key Mechanics

```python
class HomeTheaterFacade:
    def __init__(self):
        # Facade owns or receives subsystem instances
        self.amplifier = Amplifier()
        self.dvd = DVDPlayer()
        self.projector = Projector()
        self.lights = Lights()

    def watch_movie(self, movie):
        # Orchestrates multiple subsystem calls in the right order
        self.lights.dim(10)
        self.amplifier.on()
        self.amplifier.set_volume(5)
        self.dvd.on()
        self.projector.on()
        self.projector.set_input("DVD")
        self.dvd.play(movie)

    def end_movie(self):
        self.dvd.off()
        self.projector.off()
        self.amplifier.off()
        self.lights.on()
```

Client code:
```python
theater = HomeTheaterFacade()
theater.watch_movie("Inception")   # one call, six subsystems coordinated
theater.end_movie()
```

## Facade vs Encapsulation
Similar idea, different scope:

| | Encapsulation | Facade |
|---|---|---|
| **Scope** | Single class/object | Subsystem of multiple classes |
| **Hides** | Internal state | Subsystem complexity and interactions |
| **OOP concept** | Principle | Design pattern |

Facade is encapsulation applied at the **subsystem level**.

## Facade vs Adapter

| | Facade | Adapter |
|---|---|---|
| **Purpose** | Simplify a subsystem | Make incompatible interfaces work together |
| **Interface** | New simplified one | Converts existing one |
| **Subsystem** | Multiple classes | Usually one class |

## Subsystem Still Accessible
Facade doesn't lock you out of the subsystem. Advanced users can still use subsystem classes directly for fine-grained control. Facade is a convenience, not a restriction.

## When to Use
- Complex subsystem needs a simple entry point for common use cases
- Too many dependencies between client and subsystem internals
- Layering a system — Facade defines the entry point to each layer
- Migrating legacy systems — Facade wraps old code, new code talks to Facade

## Real-World Analogies
- **Car** — `start()` hides engine ignition, fuel pump, electronics initialization
- **API Gateway** — single endpoint orchestrates auth, user, payment microservices
- **Home automation** — "movie mode" button dims lights, closes blinds, turns on TV
- **Compiler** — `compile(source)` hides lexer, parser, semantic analyzer, code generator

## Python Note
Facade has no abstract base class requirement — it's just a class that wraps other classes. No ABCs needed unless you want multiple facade implementations.

## Relation to Other Patterns
- **Adapter** — Adapter makes incompatible interfaces work; Facade simplifies a compatible but complex subsystem
- **Mediator** — both decouple objects, but Mediator centralizes communication *between* subsystem objects; Facade provides a simplified interface *to* the subsystem from outside
- **Abstract Factory** — can be used with Facade to provide an interface for creating subsystem objects
