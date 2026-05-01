from abc import abstractmethod,ABC
from random import randint
from datetime import datetime

class ISubscriber(ABC):
    
    
    
    @abstractmethod
    def update(self,data):
        pass
    
class IPublisher(ABC):
    def __init__(self):
        self.subscribers=[]
        
    def add(self,subscriber:ISubscriber):
        self.subscribers.append(subscriber)
        
    def remove(self,subscriber:ISubscriber):
        self.subscribers.remove(subscriber)
        
    @abstractmethod
    def notify(self):
        pass
    
    
    
    
    
    
class WeatherStation(IPublisher):
    def notify(self):
        data=self.getTemp()
        for sub in self.subscribers:
            sub.update(data)
            
    def getTemp(self):
        return f"Temperature: {str(randint(1,100))} at Time: {datetime.now()}"
            
            
class PhoneDisplay(ISubscriber):

    def update(self,data):
        print("Getting latest data on PhoneDisplay")
        print(data)
        

class TvDisplay(ISubscriber):

        
    def update(self,data):
        print("Getting latest data on TVDisplay")
        print(data)
        
        
ws=WeatherStation()
pd=PhoneDisplay()
td=TvDisplay()

ws.add(pd)
ws.add(td)

ws.notify()

ws.remove(td)

ws.notify()