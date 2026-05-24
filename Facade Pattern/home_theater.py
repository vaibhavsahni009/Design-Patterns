


class Amplifier:
    
    def on(self):
        print("Turning on Amplifier")
        
        
    def off(self):
        print("Turning off Amplifier")
        
    def set_volume(self,level):
        print(f"Setting volume to {level}")


class DVDPlayer:
    
    def on(self):
        print("Turning on DVDPlayer")
        
        
    def off(self):
        print("Turning off DVDPlayer")
        
    def play(self,movie):
        print(f"Playing {movie}")



class Projector:
    
    def on(self):
        print("Turning on Projector")
        
        
    def off(self):
        print("Turning off Projector")
        
    def set_input(self,source):
        print(f"Setting source to {source}")


class Lights:
    
    def on(self):
        print("Turning on Lights")
        
        
    def off(self):
        print("Turning off Lights")
        
    def dim(self,level):
        print(f"Setting lights at {level}")
        
        
class HomeTheaterFacade:
    
    def __init__(self):
        self.amplifier=Amplifier()
        self.dvd_player=DVDPlayer()
        self.projector=Projector()
        self.lights=Lights()
    
    def watch_movie(self,movie):
        self.amplifier.on()
        self.dvd_player.on()
        self.projector.on()
        self.projector.set_input("DVD")
        self.lights.on()
        self.lights.dim("10")
        self.dvd_player.play(movie)
        
    def end_movie(self):
        self.lights.dim("80")
        self.dvd_player.off()
        self.projector.off()
        self.amplifier.off()
        
        
HTFacade=HomeTheaterFacade()

HTFacade.watch_movie("Lords of the ring")
HTFacade.end_movie()
        



    