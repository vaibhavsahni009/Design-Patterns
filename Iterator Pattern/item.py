from abc import ABC, abstractmethod


class Inventory(ABC):
    
    
    @abstractmethod
    def getIterator(self):
        pass
    
    
class InventoryIterator(ABC):
    
    @abstractmethod
    def is_done(self):
        pass
    
    @abstractmethod
    def get_item(self):
        pass
    
    @abstractmethod
    def next(self):
        pass
    
    
    
class HandheldInventory(Inventory):
    
    
    def __init__(self,lItem,rItem):
        self.left_hand_item=lItem
        self.right_hand_item=rItem
        
        
    def get_left_hand_item(self):
        return self.left_hand_item
        
    
    def get_right_hand_item(self):
        return self.right_hand_item
    
    def getIterator(self):
        
        return HandheldInventoryIterator(self)
    
    
    
class HandheldInventoryIterator(InventoryIterator):
    
    
    def __init__(self,i):
        self.handheld_inventory=i
        self.idx=0
        
    def is_done(self):
        return self.idx>1
    
    def get_item(self):
        if self.idx==0:
            return self.handheld_inventory.get_left_hand_item()
        elif self.idx==1:
            return self.handheld_inventory.get_right_hand_item()
        
        else:
            raise StopIteration("We have only two hands")
        
        
    def next(self):
        self.idx+=1
        
class SpellbookInventory(Inventory):
    
    
    def __init__(self,*args):
        self.spells=args
        
        
    def get_spells(self):
        return self.spells
        
    

    
    def getIterator(self):
        
        return SpellbookInventoryIterator(self)
    
    
    
class SpellbookInventoryIterator(InventoryIterator):
    
    
    def __init__(self,i):
        self.spellbook_inventory=i
        self.idx=0
        
    def is_done(self):
        return self.idx>=len(self.spellbook_inventory.get_spells())
    
    def get_item(self):
        
        try:
            return self.spellbook_inventory.get_spells()[self.idx]
        except IndexError:
        
            raise StopIteration("We have these many spells only")
        
        
    def next(self):
        self.idx+=1
        
        
        
        
handheldInventory=HandheldInventory("Map","Sword")
hiterator=handheldInventory.getIterator()

spellbookInventory=SpellbookInventory("Fireball","Watersplash","Heal")
spiterator=spellbookInventory.getIterator()


def iterating(it):
    while not it.is_done():
        print(it.get_item())
        it.next()
        
        
iterating(hiterator)
iterating(spiterator)