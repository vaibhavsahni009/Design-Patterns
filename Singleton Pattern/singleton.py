from datetime import datetime


class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            
        return cls._instance
    
    
    def __init__(self):
        if not hasattr(self,"initAt"):
            self.initAt=datetime.now()
    
    def log(self,str):
        print(f"{str} from logger initialized at {self.initAt}")
        
        
        
loggerA=Logger()
loggerA.log("this is log from loggerA")
loggerB=Logger()
loggerB.log("this is log from loggerB")

print(loggerA is loggerB)