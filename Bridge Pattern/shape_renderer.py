from abc import ABC, abstractmethod

class IRenderer(ABC):
    
    @abstractmethod
    def render(self,shape_name,color):
        pass


class Shape(ABC):
    
    def __init__(self, r: IRenderer):
        self.renderer = r       # shared state — stored once for all subclasses

    @abstractmethod
    def renderShape(self, color):
        pass
    
    
class VectorRenderer(IRenderer):
    
    def render(self,shape_name,color):
        print(f"Drawing {shape_name} as smooth vector with {color} color")
        
        
class RasterRenderer(IRenderer):
    
    def render(self,shape_name,color):
        print(f"Drawing {shape_name} as pixel grid with {color} color")
        
        
        
        
class Circle(Shape):
    
    def __init__(self, r: IRenderer):
        super().__init__(r)
        
    def renderShape(self, color):
        self.renderer.render("Circle", color)


class Square(Shape):
    
    def __init__(self, r: IRenderer):
        super().__init__(r)
        
    def renderShape(self, color):
        self.renderer.render("Square", color)
        
rRenderer=RasterRenderer()
vRenderer=VectorRenderer()

rCircle=Circle(rRenderer)
vCircle=Circle(vRenderer)

rSquare=Square(rRenderer)
vSquare=Square(vRenderer)

rCircle.renderShape("Blue")
vCircle.renderShape("Pink")
rSquare.renderShape("Purple")
vSquare.renderShape("Red")
