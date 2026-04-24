from abc import ABC, abstractmethod

class IQuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        pass
    
class IFlyBehavior(ABC):
    @abstractmethod
    def fly(self):
        pass
    
class IDisplayBehavior(ABC):
    @abstractmethod
    def display(self):
        pass


class Duck:
    
    def __init__(self, qb:IQuackBehavior, db:IDisplayBehavior, fb:IFlyBehavior):
        self.QuackBehaviour = qb
        self.DisplayBehaviour = db
        self.FlyBehaviour = fb
        
    def fly(self):
        self.FlyBehaviour.fly()
        
    def quack(self):
        self.QuackBehaviour.quack()
    
    def display(self):
        self.DisplayBehaviour.display()
        
    def setDisplayBehaviour(self, db:IDisplayBehavior):
        self.DisplayBehaviour = db


class HomeFlyBehaviour(IFlyBehavior):
    def fly(self):
        print("Can't fly homeschooled")
        
        
class SilentQuackBehaviour(IQuackBehavior):
    def quack(self):
        print("shhh should'nt quack")
        
class StillDisplayBehaviour(IDisplayBehavior):
    def display(self):
        print("Conserving energy staying still")
        
        
class ActiveDisplayBehaviour(IDisplayBehavior):
    def display(self):
        print("Party")


# -------------------------------------------------------
# ERROR DEMO 1: Forgetting to implement an abstract method
# -------------------------------------------------------
# BrokenDisplay inherits IDisplayBehavior but doesn't implement display()
# With ABC, Python catches this at instantiation, not at call time
class BrokenDisplay(IDisplayBehavior):
    pass  # forgot display()

print("--- Error Demo 1: Missing method implementation ---")
try:
    broken = BrokenDisplay()  # <-- ERROR HERE, not when you call display()
except TypeError as e:
    print(f"TypeError: {e}")


# -------------------------------------------------------
# ERROR DEMO 2: Instantiating the abstract class directly
# -------------------------------------------------------
print("\n--- Error Demo 2: Instantiating abstract class directly ---")
try:
    behavior = IFlyBehavior()  # can't instantiate ABC directly
except TypeError as e:
    print(f"TypeError: {e}")


# -------------------------------------------------------
# ERROR DEMO 3: Partially implementing abstract methods
# -------------------------------------------------------
# If a class has multiple abstract methods and only implements some
class PartialQuack(IQuackBehavior):
    pass  # quack() not implemented

print("\n--- Error Demo 3: Partial implementation ---")
try:
    pq = PartialQuack()
except TypeError as e:
    print(f"TypeError: {e}")


# -------------------------------------------------------
# WORKING CASE: Everything correct
# -------------------------------------------------------
print("\n--- Working case ---")
rubberDuck = Duck(SilentQuackBehaviour(), StillDisplayBehaviour(), HomeFlyBehaviour())
rubberDuck.display()
rubberDuck.fly()
rubberDuck.quack()

rubberDuck.setDisplayBehaviour(ActiveDisplayBehaviour())
rubberDuck.display()
