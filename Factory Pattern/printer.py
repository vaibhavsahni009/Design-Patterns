from abc import ABC, abstractmethod



class Printer(ABC):
    
    
    @abstractmethod
    def printPaper(self):
        pass
    
    
class Ink(ABC):
    
    
    @abstractmethod
    def isEmpty(self):
        pass
    
    
    
class PrinterFactory(ABC):
    
    @abstractmethod
    def getPrinter(self):
        pass
    
    @abstractmethod
    def getInk(self):
        pass
    
    
class LaserPrinter(Printer):
    
    def printPaper(self):
        print("Printing on Laser Printer")
        
        
class LaserInk(Ink):
    
    def isEmpty(self):
        print("Not empty yet")
        
        
class InkjetPrinter(Printer):
    
    def printPaper(self):
        print("Printing on Inkjet Printer")
        
        
class InkjetInk(Ink):
    
    def isEmpty(self):
        print("Not empty yet")
        
        
        
class LaserPrinterFactory(PrinterFactory):
    
    def getPrinter(self):
        return LaserPrinter()
    
    def getInk(self):
        return LaserInk()
    
    
class InkjetPrinterFactory(PrinterFactory):
    
    def getPrinter(self):
        return InkjetPrinter()
    
    def getInk(self):
        return InkjetInk()
    
    
myPrinterFactory= LaserPrinterFactory()

myPrinterFactory.getPrinter().printPaper()
myPrinterFactory.getInk().isEmpty()