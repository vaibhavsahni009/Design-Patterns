# Composite Pattern

## Intent
Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

## The Problem
You have a tree structure where individual items and groups of items need to be treated the same way. Writing separate handling logic for leaves and composites leads to complex, coupled client code.

## The Solution
Define a common interface for both leaves and composites. The client calls the same methods on both — the leaf handles it directly, the composite delegates to its children recursively.

## Structure

```
ITask (Component)
├── Task (Leaf)          ← no children, does actual work
└── TaskGroup (Composite)  ← has children, delegates to them
      └── children: list[ITask]   ← can contain Tasks or TaskGroups
```

## Components

| Component | Role |
|---|---|
| **Component** | Common interface for both leaf and composite |
| **Leaf** | Has no children. Implements behavior directly. |
| **Composite** | Has children (list of Components). Delegates behavior to children. |
| **Client** | Works only with the Component interface — doesn't know if it's leaf or composite |

## Key Mechanics

```python
class ITask(ABC):
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def get_cost(self): pass

    @abstractmethod
    def show(self, indent=0): pass


class Task(ITask):              # Leaf
    def __init__(self, title, cost):
        super().__init__(title)
        self.cost = cost

    def get_cost(self):
        return self.cost        # returns own cost directly

    def show(self, indent=0):
        print(" " * indent + f"- {self.title} (cost: {self.cost})")


class TaskGroup(ITask):         # Composite
    def __init__(self, title):
        super().__init__(title)
        self.tasks = []

    def add(self, task: ITask):
        self.tasks.append(task)

    def remove(self, task: ITask):
        self.tasks.remove(task)

    def get_cost(self):
        return sum(t.get_cost() for t in self.tasks)  # recursive delegation

    def show(self, indent=0):
        print(" " * indent + f"+ {self.title} (total: {self.get_cost()})")
        for t in self.tasks:
            t.show(indent + 2)  # recursive tree print
```

## Recursive Tree Output

```
+ Project (total cost: 6)
  - t1 (cost: 1)
  + Epic (total cost: 5)
    - t2 (cost: 2)
    - t3 (cost: 3)
```

## is-a vs has-a in Composite

| | is-a Component | has-a Component |
|---|---|---|
| **Leaf** | ✅ | ❌ |
| **Composite** | ✅ | ✅ (list of children) |

The composite's power comes from this dual relationship — it's a component AND contains components.

## Where to Put add()/remove()

Two approaches, each with tradeoffs:

**On Composite only (cleaner)**
```python
class TaskGroup(ITask):
    def add(self, task): ...    # only composite has this
```
Client must know if it has a composite to call `add()`. Cleaner design.

**On Component interface (uniform)**
```python
class ITask(ABC):
    def add(self, task):
        raise NotImplementedError("Leaves cannot have children")
```
Uniform interface but leaf has a meaningless method. Trades safety for uniformity.

## Mutable vs Immutable
`add()` and `remove()` make `TaskGroup` mutable — appropriate for task management where hierarchy changes at runtime. For immutable composites, pass all children in the constructor and remove `add()`/`remove()`.

## When to Use
- Part-whole hierarchies — file systems, UI component trees, org charts
- Client should treat leaf and composite objects uniformly
- Recursive structures where operations need to propagate down the tree

## Real-World Analogies
- **File system** — files (leaf) and folders (composite). `get_size()` on a folder sums all children recursively
- **Jira/Kanban** — Epics contain Stories contain Tasks. `get_total_points()` works at any level
- **UI components** — a Panel contains Buttons and other Panels. `render()` propagates down
- **Org chart** — employees and managers. `get_total_salary()` on a department sums recursively

## Python Note
Using `set()` for children works but loses ordering and requires hashable objects. Prefer `list` unless you specifically need uniqueness guarantees — task hierarchies are typically ordered.

## Relation to Other Patterns
- **Decorator** — both use recursive composition, but Decorator adds responsibilities to one object; Composite builds tree structures
- **Iterator** — often used with Composite to traverse the tree
- **Visitor** — often used with Composite to perform operations across the tree without modifying node classes
- **Flyweight** — can be used with Composite to share leaf nodes and save memory in large trees
