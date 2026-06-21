from abc import ABC, abstractmethod


class IGateState(ABC):

    def __init__(self, gate: Gate):  
        self.gate = gate

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def payOk(self):
        pass

    @abstractmethod
    def payFailed(self):
        pass

    @abstractmethod
    def enter(self):
        pass


class LockedState(IGateState):

    def pay(self):
        print("[Locked]    Initiating payment processing...")
        self.gate.changeState(ProcessingState(self.gate))

    def payOk(self):
        print("[Locked]    Payment confirmed, unlocking gate")
        self.gate.changeState(UnlockedState(self.gate))

    def payFailed(self):
        print("[Locked]    Payment failed, gate stays locked")

    def enter(self):
        raise Exception("Gate is locked! Calling metro police.")


class UnlockedState(IGateState):

    def pay(self):
        print("[Unlocked]  Gate already unlocked, no need to pay")

    def payOk(self):
        raise Exception("Unexpected payment on unlocked gate — initiating refund")

    def payFailed(self):
        print("[Unlocked]  Unknown payment failure, no action needed")

    def enter(self):
        print("[Unlocked]  Passenger entered, locking gate")
        self.gate.changeState(LockedState(self.gate))


class ProcessingState(IGateState):

    def pay(self):
        print("[Processing] Payment already in progress, please wait")

    def payOk(self):
        print("[Processing] Payment succeeded, unlocking gate")
        self.gate.changeState(UnlockedState(self.gate))

    def payFailed(self):
        print("[Processing] Payment failed, locking gate")
        self.gate.changeState(LockedState(self.gate))

    def enter(self):
        raise Exception("Gate is processing payment! Calling metro police.")


class Gate:

    def __init__(self):
        self.state = LockedState(self)

    def pay(self):       self.state.pay()
    def payOk(self):     self.state.payOk()
    def payFailed(self): self.state.payFailed()
    def enter(self):     self.state.enter()

    def changeState(self, state: IGateState):
        self.state = state


# -------------------------------------------------------
# DEMO
# -------------------------------------------------------

def safe_enter(gate):
    """Helper to catch illegal entry attempts"""
    try:
        gate.enter()
    except Exception as e:
        print(f"[EXCEPTION]  {e}")

gate = Gate()
print("=== Scenario 1: Happy path — pay, succeed, enter ===")
gate.pay()         # Locked → Processing
gate.payOk()       # Processing → Unlocked
gate.enter()       # Unlocked → Locked

print("\n=== Scenario 2: Pay, fail, try to enter illegally ===")
gate.pay()         # Locked → Processing
gate.payFailed()   # Processing → Locked
safe_enter(gate)   # Locked → exception

print("\n=== Scenario 3: Try to enter without paying ===")
safe_enter(gate)   # Locked → exception

print("\n=== Scenario 4: Double pay while processing ===")
gate.pay()         # Locked → Processing
gate.pay()         # Processing → still Processing (message shown)
gate.payOk()       # Processing → Unlocked
gate.enter()       # Unlocked → Locked

print("\n=== Scenario 5: Pay while already unlocked ===")
gate.pay()         # Locked → Processing
gate.payOk()       # Processing → Unlocked
gate.pay()         # Unlocked → still Unlocked (message shown)
gate.enter()       # Unlocked → Locked

print("\n=== Scenario 6: Try to enter while payment processing ===")
gate.pay()         # Locked → Processing
safe_enter(gate)   # Processing → exception
gate.payOk()       # Processing → Unlocked
gate.enter()       # Unlocked → Locked
