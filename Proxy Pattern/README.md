# Proxy Pattern

## Intent
Provide a surrogate or placeholder for another object to control access to it. The proxy implements the same interface as the real object — the client doesn't know it's talking to a proxy.

## The Problem
Direct access to an object may be undesirable or impractical — it might be expensive to create, require access control, need caching, or live on a remote server.

## The Solution
Introduce a proxy that sits between the client and the real object. The proxy implements the same interface, intercepts calls, and decides whether/how to forward them.

## Structure

```
Client ──► ISubject
               ├── RealSubject    ← does the actual work
               └── Proxy          ← controls access to RealSubject
                     └── has-a RealSubject
```

## Components

| Component | Role |
|---|---|
| **Subject Interface** | Common interface for RealSubject and Proxy |
| **RealSubject** | The actual object that does the work |
| **Proxy** | Implements Subject, wraps RealSubject, adds control logic |
| **Client** | Works with Subject interface, unaware it's talking to a Proxy |

## Key Mechanics

```python
class ISubject(ABC):
    @abstractmethod
    def request(self):
        pass

class RealSubject(ISubject):
    def request(self):
        return "real result"

class Proxy(ISubject):
    def __init__(self):
        self.real = RealSubject()

    def request(self):
        # add control logic here (cache, auth, lazy load, log...)
        return self.real.request()
```

## Types of Proxy

### Virtual Proxy — Lazy Loading
Don't create the expensive object until it's actually needed:
```python
class Proxy(ISubject):
    def __init__(self):
        self._real = None           # not created yet

    def request(self):
        if self._real is None:
            self._real = RealSubject()   # created on first use
        return self._real.request()
```

### Caching Proxy
Store results of expensive calls, return cached result on repeat calls:
```python
class CachingProxy(ISubject):
    def __init__(self):
        self.cache = {}
        self.real = RealSubject()

    def request(self, key):
        if key not in self.cache:
            self.cache[key] = self.real.request(key)   # cache miss
        return self.cache[key]                          # cache hit
```

### Protection Proxy — Access Control
Check permissions before forwarding:
```python
class ProtectionProxy(ISubject):
    def __init__(self, user_role):
        self.role = user_role
        self.real = RealSubject()

    def request(self):
        if self.role != "admin":
            raise PermissionError("Access denied")
        return self.real.request()
```

### Remote Proxy
Represents an object in a different address space. Handles network communication transparently. Common in RPC frameworks.

## Proxy vs Decorator vs Facade

| | Proxy | Decorator | Facade |
|---|---|---|---|
| **Same interface?** | Yes | Yes | No — new simplified one |
| **Wraps** | One object | One object | Multiple objects |
| **Intent** | Control access | Add behavior | Simplify complexity |
| **Client aware?** | No | No | Yes |

Proxy and Decorator are structurally identical. The difference is **intent**:
- Decorator adds behavior the client *wants*
- Proxy controls access the client may not even know about

## Making Proxy Behavior Visible
Add logging to the real object to see when proxy intercepts vs forwards:

```
[DB HIT] running expensive query: SELECT * FROM users
result for query: SELECT * FROM users
[DB HIT] running expensive query: SELECT * FROM orders
result for query: SELECT * FROM orders
result for query: SELECT * FROM users   ← cache hit, no DB HIT
```

## When to Use
- **Lazy initialization** — delay expensive object creation until needed
- **Access control** — check permissions before allowing operations
- **Caching** — avoid repeated expensive calls with same inputs
- **Logging/monitoring** — record calls without changing real object
- **Remote access** — local representative for a remote object

## Real-World Analogies
- **Cheque/Demand Draft** — represents money, controls when actual transaction happens
- **Credit card** — proxy for your bank account, adds fraud protection layer
- **CDN** — proxy for your origin server, caches content closer to users
- **Security guard** — proxy for building access, checks credentials before letting through

## Python Note
Python's `__getattr__` can be used to build a transparent proxy that forwards all attribute access automatically:
```python
class TransparentProxy:
    def __init__(self, real):
        self._real = real

    def __getattr__(self, name):
        return getattr(self._real, name)   # forwards everything
```

## Relation to Other Patterns
- **Decorator** — same structure, different intent. Decorator adds; Proxy controls.
- **Facade** — Facade simplifies multiple classes; Proxy controls one class
- **Adapter** — Adapter changes the interface; Proxy keeps the same interface
