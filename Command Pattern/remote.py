from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def unexecute(self):
        pass
    
    
class Light:
    def __init__(self):
        self.lightOn=False
        
    def turn_on(self):
        if not self.lightOn:
            print("Light Turned On")
            self.lightOn=True
        else:
            print("Already Turned On")
    def turn_off(self):
        if self.lightOn:
            self.lightOn=False
            print("Light Turned Off")
        else:
            print("Already Turned Off")
        
        
class LightOnCommand(ICommand):
    
    def __init__(self,light:Light):
        self.light=light
    
    def execute(self):
        self.light.turn_on()
        
    def unexecute(self):
        self.light.turn_off()
        
class LightOffCommand(ICommand):
    
    def __init__(self,light:Light):
        self.light=light
    
    def unexecute(self):
        self.light.turn_on()
        
    def execute(self):
        self.light.turn_off()

        
        
        
class Remote:
    
    
    def __init__(self,turnOnCommand:ICommand,turnOffCommand:ICommand):
        self.turnOnCommand=turnOnCommand
        self.turnOffCommand=turnOffCommand
        
    def press_on_button(self):
        self.turnOnCommand.execute()
        
    def press_on_undo(self):
        self.turnOnCommand.unexecute()
    
    def press_off_button(self):
        self.turnOffCommand.execute()
        
    def press_off_undo(self):
        self.turnOffCommand.unexecute()
        
        
myLight=Light()
myRemote=Remote(LightOnCommand(myLight),LightOffCommand(myLight))

myRemote.press_on_button()
myRemote.press_on_undo()
myRemote.press_off_button()
myRemote.press_off_undo()

myRemote.press_on_button()


# -------------------------------------------------------
# Generic Remote — supports any command on any button
# with multi-level undo via history stack
# -------------------------------------------------------

class GenericRemote:
    def __init__(self):
        self.slots: dict[str, ICommand] = {}
        self.history: list[ICommand] = []

    def set_command(self, button: str, command: ICommand):
        self.slots[button] = command

    def press(self, button: str):
        if button in self.slots:
            self.slots[button].execute()
            self.history.append(self.slots[button])
        else:
            print(f"No command assigned to button: {button}")

    def undo(self):
        if self.history:
            last = self.history.pop()
            last.unexecute()
        else:
            print("Nothing to undo")


# demo — same light, but now fan could be added without touching Remote
print("\n--- Generic Remote Demo ---")
light = Light()
generic = GenericRemote()
generic.set_command("on", LightOnCommand(light))
generic.set_command("off", LightOffCommand(light))

generic.press("on")
generic.press("off")
generic.press("on")

print("-- undo last 2 --")
generic.undo()  # undoes LightOnCommand -> turns off
generic.undo()  # undoes LightOffCommand -> turns on
generic.undo()  # undoes LightOnCommand -> turns off

print("-- nothing left --")
generic.undo()  # nothing to undo
