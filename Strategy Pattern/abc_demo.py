"""
Demonstration of all 4 permutations of ABC + @abstractmethod usage.

Permutation 1: No ABC, No @abstractmethod       -> plain class, no enforcement at all
Permutation 2: ABC, No @abstractmethod          -> abstract class but no method enforcement
Permutation 3: No ABC, with @abstractmethod     -> decorator has no effect without ABC
Permutation 4: ABC + @abstractmethod            -> full enforcement (correct approach)
"""

from abc import ABC, abstractmethod


# ==============================================================
# PERMUTATION 1: No ABC, No @abstractmethod
# Plain class — zero enforcement
# ==============================================================
print("=" * 60)
print("PERMUTATION 1: No ABC, No @abstractmethod")
print("=" * 60)

class IFly_P1:
    def fly(self):
        pass  # just a placeholder, no contract enforced

# Problem 1: Can instantiate the "interface" directly — meaningless object
base = IFly_P1()
base.fly()  # runs the empty pass, no error, no output — silent and confusing
print(f"Instantiated base interface directly: {base}")

# Problem 2: Subclass can skip implementing fly() entirely
class BrokenFly_P1(IFly_P1):
    pass  # forgot fly()

obj = BrokenFly_P1()  # no error here
print(f"Created broken subclass: {obj}")

# Problem 3: Error only surfaces at call time, deep in your code
try:
    obj.fly()  # calls parent's empty pass — NO ERROR, just silent wrong behavior!
    print("Called fly() on broken subclass — no error, but got empty behavior (silent bug!)")
except Exception as e:
    print(f"Error: {e}")

# Problem 4: Completely wrong type, no enforcement
class NotAFlyBehavior_P1:
    def swim(self):
        print("swimming")

wrong = NotAFlyBehavior_P1()
wrong.fly = None  # accidentally set fly to None
try:
    wrong.fly()  # TypeError only now, at call time
except TypeError as e:
    print(f"TypeError at call time (too late): {e}")


# ==============================================================
# PERMUTATION 2: ABC but No @abstractmethod
# Can't instantiate ABC directly, but subclasses have no enforcement
# ==============================================================
print("\n" + "=" * 60)
print("PERMUTATION 2: ABC, No @abstractmethod")
print("=" * 60)

class IFly_P2(ABC):
    def fly(self):
        pass  # no @abstractmethod — just a regular method in an ABC

# Slight improvement: can't instantiate the ABC directly... wait, actually you CAN
# because there are no abstract methods declared. ABC alone doesn't block instantiation.
base2 = IFly_P2()  # no error! ABC without abstractmethod is instantiable
print(f"Instantiated ABC directly (no abstractmethod): {base2}")

# Subclass still has no enforcement
class BrokenFly_P2(IFly_P2):
    pass  # forgot fly() — still no error

obj2 = BrokenFly_P2()
obj2.fly()  # calls parent's empty pass — silent wrong behavior again
print("Called fly() on broken P2 subclass — silent empty behavior again")


# ==============================================================
# PERMUTATION 3: No ABC, but @abstractmethod decorator used
# The decorator has NO EFFECT without ABC — completely ignored
# ==============================================================
print("\n" + "=" * 60)
print("PERMUTATION 3: No ABC, @abstractmethod present (useless)")
print("=" * 60)

class IFly_P3:
    @abstractmethod          # looks right, but ABC is missing — this does nothing
    def fly(self):
        pass

# Can still instantiate the "interface" directly — decorator was ignored
base3 = IFly_P3()
print(f"Instantiated directly despite @abstractmethod (no ABC): {base3}")

# Subclass can still skip implementation — no enforcement
class BrokenFly_P3(IFly_P3):
    pass

obj3 = BrokenFly_P3()  # no error
obj3.fly()             # calls parent's pass — silent wrong behavior
print("Called fly() on broken P3 subclass — @abstractmethod had zero effect")


# ==============================================================
# PERMUTATION 4: ABC + @abstractmethod
# Full enforcement — the correct approach
# ==============================================================
print("\n" + "=" * 60)
print("PERMUTATION 4: ABC + @abstractmethod (correct)")
print("=" * 60)

class IFly_P4(ABC):
    @abstractmethod
    def fly(self):
        pass

# Cannot instantiate the abstract class directly
try:
    base4 = IFly_P4()
except TypeError as e:
    print(f"Cannot instantiate ABC directly -> TypeError: {e}")

# Cannot instantiate a subclass that skips implementation
class BrokenFly_P4(IFly_P4):
    pass  # forgot fly()

try:
    obj4 = BrokenFly_P4()  # ERROR HERE at instantiation, not at call time
except TypeError as e:
    print(f"Cannot instantiate incomplete subclass -> TypeError: {e}")

# Correct implementation works fine
class GoodFly_P4(IFly_P4):
    def fly(self):
        print("Flying correctly!")

obj5 = GoodFly_P4()
obj5.fly()


# ==============================================================
# SUMMARY
# ==============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
| Permutation | ABC | @abstractmethod | Blocks direct instantiation | Enforces subclass impl | Error timing     |
|-------------|-----|-----------------|-----------------------------|------------------------|------------------|
| 1           | No  | No              | No                          | No                     | Call time / never|
| 2           | Yes | No              | No (no abstract methods)    | No                     | Call time / never|
| 3           | No  | Yes             | No (decorator ignored)      | No                     | Call time / never|
| 4           | Yes | Yes             | Yes                         | Yes                    | Instantiation    |
""")
