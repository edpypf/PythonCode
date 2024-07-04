from abc import ABC

# class decorator is the clss that used other class as argument, which is the decorator of base classes
class Shape(ABC):
    def __str__(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def resize(self, factor):
        self.radius *= factor
        
    def __str__(self):
        return f'A circle with Radius of {self.radius}'
    
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return "A square with the side of {self.side}"
    
class ColoredShape(Shape):
    def __init__(self, shape, color):
        if isinstance(shape, ColoredShape):
            raise Exception(f'cannot apply the same shape twice')
        self.shape = shape
        self.color = color

    def __str__(self):
        return f'Shape of {self.shape} has color of {self.color}'
    
class TransparentShape(Shape):
    def __init__(self, shape, transparent):
        self.shape = shape
        self.transparent = transparent

    def __str__(self):
        return f'Shape of {self.shape} has transparent ratio of {self.transparent*100.0}% transparency'
    
if __name__ == '__main__':
    circle = Circle(2)
    print(circle)
    redCircle = ColoredShape(circle, 'Red')
    print(redCircle)
    transparencyCircle = TransparentShape(circle, 0.5)
    print(redCircle)

    red_half_transparent_circle = TransparentShape(redCircle, 0.5)
    print(red_half_transparent_circle)
        
    rc = ColoredShape(ColoredShape(Square(3), 'red'), 'green')
    print(rc)
