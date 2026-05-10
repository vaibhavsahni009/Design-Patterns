# Command Pattern

## Intent
Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

## The Problem
You want to decouple the object that sends a request (invoker) from the object that handles it (receiver). You also want to support undo, queuing, or logging of operations.

## The Solution
Wrap each request in a Command object. The invoker only knows about the command interface — it never talks to the receiver directly.

## Structure

```
Client
└── creates ──► ConcreteCommand(receiver)
                     │
                     ▼
Invoker ──► ICommand.execute() ──► Receiver.action()
        └── ICommand.undo()   ──► Receiver.reverse_action()
```

## Components

| Component | Role |
|---|---|
| **ICommand** | Interface with `execute()` and `undo()` |
| **ConcreteCommand** | Implements ICommand, holds receiver reference, calls receiver methods |
| **Receiver** | The object that actually does the work |
| **Invoker** | Holds and triggers commands, knows nothing about receiver |
| **Client** | Creates commands, wires receiver into command, gives command to invoker |

## Key Mechanics

```python
class ICommand(ABC):
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def undo(self): pass


class ConcreteCommand(ICommand):
    def __init__(self, receiver: Receiver):
        self.receiver = receiver            # dependency injected

    def execute(self):
        self.receiver.action()

    def undo(self):
        self.receiver.reverse_action()


class Invoker:
    def __init__(self, command: ICommand):
        self.command = command

    def press(self):
        self.command.execute()

    def press_undo(self):
        self.command.undo()
```

## Multi-Level Undo (History Stack)

```python
class Invoker:
    def __init__(self):
        self.slots: dict[str, ICommand] = {}
        self.history: list[ICommand] = []

    def set_command(self, button: str, command: ICommand):
        self.slots[button] = command

    def press(self, button: str):
        self.slots[button].execute()
        self.history.append(self.slots[button])   # record

    def undo(self):
        if self.history:
            self.history.pop().undo()             # reverse last action
```

Each executed command is pushed onto a stack. Undo pops and reverses. This gives you unlimited undo depth.

## Specific vs Generic Invoker

### Specific Invoker
Hardcoded slots for known commands. Good for dedicated devices (TV remote with fixed buttons).
```python
class TVRemote:
    def __init__(self, on_cmd, off_cmd):
        self.on_cmd = on_cmd
        self.off_cmd = off_cmd
```

### Generic Invoker
Dynamic slots, any command on any button. Good for extensible systems (text editor, game input).
```python
class GenericRemote:
    def __init__(self):
        self.slots = {}
```

## What Command Pattern Unlocks

| Feature | How |
|---|---|
| **Undo/Redo** | Store executed commands in a stack, call `undo()` to reverse |
| **Queuing** | Store commands and execute later (job queues, task schedulers) |
| **Logging** | Serialize commands to disk, replay after crash |
| **Macro commands** | A command that contains and executes a list of commands |

## When to Use
- Need undo/redo functionality
- Need to queue, schedule, or log operations
- Want to parameterize objects with operations
- Invoker should be decoupled from what it triggers

## Real-World Analogies
- Restaurant order slip — waiter (invoker) takes order (command), passes to kitchen (receiver)
- Text editor — every edit is a command object, Ctrl+Z pops the history stack
- Job queue — tasks are command objects queued and executed by workers

## Relation to Other Patterns
- **Strategy** — both encapsulate behavior in objects, but Command encapsulates a *request* (with undo/history); Strategy encapsulates an *algorithm*
- **Memento** — often used with Command for undo; Memento captures state, Command captures the action
- **Chain of Responsibility** — commands can be chained; each handler decides whether to handle or pass on
