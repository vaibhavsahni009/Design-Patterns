# Adapter Pattern

## Intent
Convert the interface of a class into another interface that clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

## The Problem
You have existing client code that expects a specific interface, and a class (often third-party) that does what you need but exposes a different interface. You can't change either side.

## The Solution
Create an adapter that implements the target interface and wraps the incompatible class, translating calls between the two.

## Structure

```
Client ──► Target Interface
                └── Adapter (implements Target, wraps Adaptee)
                          └── Adaptee.specific_method()
```

## Components

| Component | Role |
|---|---|
| **Target** | The interface the client expects to work with |
| **Adaptee** | The existing class with the incompatible interface (e.g. third-party library) |
| **Adapter** | Implements Target, wraps Adaptee, translates calls |
| **Client** | Works only with the Target interface, unaware of Adaptee |

## Key Mechanics

```python
class Target(ABC):
    @abstractmethod
    def request(self):
        pass


class Adaptee:
    def specific_request(self):   # incompatible method name/signature
        return "adaptee result"


class Adapter(Target):
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee

    def request(self):                          # target interface
        return self.adaptee.specific_request()  # translated to adaptee call


# client never touches Adaptee directly
client_code(Adapter(Adaptee()))
```

## Who Implements the Target Interface

Only the **Adapter** implements the Target interface — that's its job.

The **Client** uses the Target interface but doesn't implement it. The client is the consumer, the adapter is the translator.

```
IMediaPlayer (Target)
    └── MediaAdapter implements it   ✅

AudioPlayer uses it                  ✅ (client)
AudioPlayer implements it            ❌ (wrong — blurs roles)
```

## Adapter vs Decorator

Both wrap an object, but the intent is different:

| | Adapter | Decorator |
|---|---|---|
| **Purpose** | Convert interface | Add behavior |
| **Interface** | Changes it (A → B) | Preserves it (A → A) |
| **Client knows?** | No — sees Target only | No — sees same interface |
| **Use when** | Incompatible interfaces | Extending functionality |

## When to Use
- You want to use an existing class but its interface doesn't match what you need
- Migrating from one library to another without changing client code
- Integrating third-party code into your system
- Legacy code that can't be modified

## Real-World Analogies
- Electric plug adapter — plug and socket are incompatible, adapter bridges them
- Library migration — old code calls `OldLibrary.fetch()`, new library has `NewLibrary.get()`, adapter translates
- Payment gateway — your system calls `pay()`, Stripe expects `charge()`, adapter in between

## Python Note
Interface naming should describe the **capability**, not the pattern role. Prefer `IMediaPlayer` over `IMediaPlayerAdapter` — the interface represents what something *can do*, not how it fits into the pattern.

## Relation to Other Patterns
- **Decorator** — same wrapping structure, different intent. Decorator adds behavior, Adapter converts interface
- **Facade** — Facade simplifies a complex subsystem; Adapter makes two incompatible interfaces work together
- **Proxy** — Proxy controls access to an object with the same interface; Adapter changes the interface
