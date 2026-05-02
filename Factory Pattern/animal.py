from abc import ABC, abstractmethod


class Animal(ABC):
    
    @abstractmethod
    def speak(self):
        pass
    
class Dog(Animal):
    
    def speak(self):
        print("Bark")
    

    

class Cat(Animal):
    
    def speak(self):
        print("Meow")
        
        
class SimpleAnimalFactory:
    
    @staticmethod
    def createAnimal(animalType:str) -> Animal:
        if animalType=="Cat":
            return Cat()
        elif animalType=="Dog":
            return Dog()
        else:
            raise ValueError(f"Invalid Animal {animalType}")
 
 
 
 # test simple factory
 
myDog = SimpleAnimalFactory.createAnimal("Dog")

myDog.speak()


class AnimalFactory(ABC):
    
    @abstractmethod
    def createAnimal(self) -> Animal:
        pass
    
    def describe(self):
        animal = self.createAnimal()
        print("I have created an animal that says: ", end="")
        animal.speak()




class DogFactory(AnimalFactory):
    def createAnimal(self) -> Animal:
        return Dog()           
           

class CatFactory(AnimalFactory):
    def createAnimal(self) -> Animal:
        return Cat()
    
    
# test factory method

myCat = CatFactory().createAnimal()

myCat.speak()  

CatFactory().describe()         
