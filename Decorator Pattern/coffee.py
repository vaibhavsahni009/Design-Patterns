from abc import ABC,abstractmethod


class Beverage(ABC):
    
    @abstractmethod
    def getCost(self):
        pass
    
    @abstractmethod
    def getDescription(self):
        pass
    
    
class BeverageAddOnDecorator(Beverage):
    
    def __init__(self,b:Beverage):
        self.beverage=b
        
        
        
class Expresso(Beverage):
    
    def getCost(self):
        return 1
    
    def getDescription(self):
        return "Expresso"
    
    
class SoyMilk(BeverageAddOnDecorator):
    
    def getCost(self):
        return self.beverage.getCost() + 2
    
    def getDescription(self):
        return self.beverage.getDescription() + " + Soy Milk"
    
    
class Sugar(BeverageAddOnDecorator):
    
    def getCost(self):
        return self.beverage.getCost() + 1
    
    def getDescription(self):
        return self.beverage.getDescription() + " + Sugar"
    
    
myOrder = Sugar(SoyMilk(Expresso()))

print(f"My Order of {myOrder.getDescription()} costed me {myOrder.getCost()}")
    
    