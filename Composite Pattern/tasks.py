from abc import ABC, abstractmethod


class ITask(ABC):
    
    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def show(self, indent=0):
        pass
    
    def __init__(self, title):
        self.title = title
        

        
        
        
class Task(ITask):
    
    def __init__(self,title,cost):
        super().__init__(title)
        self.cost=cost
        
        
    def get_cost(self):
        return self.cost

    def show(self, indent=0):
        print(" " * indent + f"- {self.title} (cost: {self.cost})")
    
    
class TaskGroup(ITask):
    
    def __init__(self,title):
        super().__init__(title)
        self.tasks=set()
        
        
    def add(self,task):
        self.tasks.add(task)
        
        
    def remove(self,task):
        self.tasks.remove(task)
        
    def get_cost(self):
        cost = 0
        for t in list(self.tasks):
            cost += t.get_cost()
        return cost

    def show(self, indent=0):
        print(" " * indent + f"+ {self.title} (total cost: {self.get_cost()})")
        for t in list(self.tasks):
            t.show(indent + 2)
    
    
t1=Task("t1",1)
t2=Task("t2",2)
t3=Task("t3",3)

tg1=TaskGroup("tg1")
tg2=TaskGroup("tg2")


tg1.add(t1)
tg1.add(tg2)

tg2.add(t2)
tg2.add(t3)

print("T1 cost", t1.get_cost())
print("TG1 cost", tg1.get_cost())
print("TG2 cost", tg2.get_cost())

print("\n--- Tree Structure ---")
tg1.show()