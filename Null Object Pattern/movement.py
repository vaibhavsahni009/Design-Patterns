from abc import ABC, abstractmethod


class IMovementBehaviour(ABC):
    
    
    @abstractmethod
    def moveUp(self):
        pass
    
    @abstractmethod
    def moveDown(self):
        pass
    
    @abstractmethod
    def moveLeft(self):
        pass
    
    @abstractmethod
    def moveRight(self):
        pass
    
    
    
class WalkMovementBehaviour(IMovementBehaviour):
    
    
    def moveUp(self):
        print("Walking Up")
    
    
    def moveDown(self):
        print("Walking Down")
    
    
    def moveLeft(self):
        print("Walking Left")
    
    
    def moveRight(self):
        print("Walking Right")
    
    
class RunMovementBehaviour(IMovementBehaviour):
    
    
    def moveUp(self):
        print("Running Up")
    
    
    def moveDown(self):
        print("Running Down")
    
    
    def moveLeft(self):
        print("Running Left")
    
    
    def moveRight(self):
        print("Running Right")



class NoMovementBehaviour(IMovementBehaviour):
    
    
    def moveUp(self):
        pass
    
    
    def moveDown(self):
        pass
    
    
    def moveLeft(self):
        pass
    
    
    def moveRight(self):
        pass
        
        
        
class User:
    
    def __init__(self, movementB : IMovementBehaviour):
        self.movementB=movementB
    
    
    def setMovementB(self, movementB : IMovementBehaviour):
        self.movementB=movementB
        
    def movement(self):
        self.movementB.moveUp()
        self.movementB.moveDown()
        self.movementB.moveLeft()
        self.movementB.moveRight()
        
        
user=User(WalkMovementBehaviour())
user.movement()
user.setMovementB(RunMovementBehaviour())
user.movement()
user.setMovementB(NoMovementBehaviour())
user.movement()