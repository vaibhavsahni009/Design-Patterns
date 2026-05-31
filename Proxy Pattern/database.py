from abc import ABC, abstractmethod



class IDatabaseQuery(ABC):
    
    @abstractmethod
    def getQuery(self,query:str):
        pass
    
    
    
class DatabaseQuery(IDatabaseQuery):
    
    def getQuery(self,query):
        print(f"  [DB HIT] running expensive query: {query}")
        for _ in range(10000):
            pass
        
        return f"result for query: {query}"
    
    
    
class DatabaseQueryProxy(IDatabaseQuery):
    
    def __init__(self):
        self.cache={}
        self.dbQuery=DatabaseQuery()
        
    def getQuery(self,query):
        if query not in self.cache:
            self.cache[query]=self.dbQuery.getQuery(query)
            
        return self.cache[query]
        
        
        
        
dbQuery=DatabaseQueryProxy()


print(dbQuery.getQuery("1"))
print(dbQuery.getQuery("2"))
print(dbQuery.getQuery("3"))
print(dbQuery.getQuery("1"))
print(dbQuery.getQuery("1"))
print(dbQuery.getQuery("2"))