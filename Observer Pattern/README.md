# Observer Pattern

## Intent
Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

## The Problem
Multiple objects need to stay in sync with another object's state. Polling (constantly asking "did anything change?") is wasteful and creates tight coupling.

## The Solution
The subject maintains a list of observers and notifies them automatically when state changes. Observers register themselves — the subject doesn't need to know who they are specifically.

## Structure

```
Subject (Publisher)
├── subscribers: list[IObserver]
├── add(observer)
├── remove(observer)
└── notify()  ──────────────────► IObserver
                                   └── update(data)
                                        ├── ConcreteObserverA
                                        └── ConcreteObserverB
```

## Components

| Component | Role |
|---|---|
| **Subject** | Maintains observer list, notifies on state change |
| **Observer Interface** | Contract that all observers must implement (`update`) |
| **Concrete Observer** | Reacts to notifications in its own way |

## Push vs Pull

### Push (preferred)
Subject sends data directly to `update()`. Observer needs no reference to the subject.
```python
def notify(self):
    data = self.get_state()
    for obs in self.subscribers:
        obs.update(data)        # subject pushes data

def update(self, data):         # observer receives it
    self.display(data)
```

### Pull
Observer holds a reference to the subject and fetches data itself.
```python
def update(self):
    data = self.subject.get_state()   # observer pulls data
```

**Push is preferred** — looser coupling, observer doesn't need to know the subject's API.

## Key Mechanics

```python
class Subject(ABC):
    def __init__(self):
        self.subscribers = []

    def add(self, obs: IObserver):
        self.subscribers.append(obs)

    def remove(self, obs: IObserver):
        self.subscribers.remove(obs)

    @abstractmethod
    def notify(self):
        pass
```

## When to Use
- Changes to one object require updating others, and you don't know how many
- Objects should be able to notify others without knowing who they are
- Loose coupling between related objects is needed

## Real-World Analogies
- YouTube subscriptions — channel notifies all subscribers on upload
- Group chat — message sent to group, all members notified
- Event listeners in UI frameworks

## Python Note
Python's `list.remove()` raises `ValueError` if the element isn't found. Guard your `remove()` if needed:
```python
def remove(self, obs):
    if obs in self.subscribers:
        self.subscribers.remove(obs)
```

## Relation to Other Patterns
- **Mediator** — Observer has subjects notify observers directly; Mediator centralizes communication through a middle object
- **Event-driven systems** — Observer is the foundation of most event/callback systems
