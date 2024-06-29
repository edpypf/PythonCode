# LSP - Liskov Substitution Principle: when use parent's setter property, it could invalid the initial value of parameter, which causes
'''One approach to addressing this Liskov Substitution Principle violation is to avoid using inheritance where 
the subclass changes the behavior of the parent class in unexpected ways. Instead, you could use composition 
or provide a more specific interface.'''
class Rectangle:
    """docstring"""
    def __init__(self, width, height):
        self._height = height
        self._width = width

    @property
    def width(self):
        """docstring"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        
    @property
    def height(self):
        """docstring"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def area(self):
        return self._height * self._width
    
    def __str__(self) -> str:
        return f'width: {self._width}, height: {self._height}'
    
class Square(Rectangle):
    def __init__(self, size):
        Rectangle.__init__(self, size,size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._height = self._width = value        
        
def use_it(rc):
    """the function to use the new class above"""
    w = rc.width
    h = rc.height = 10
    print(f'height: {h}, width: {w}')
    expected = int(w*10)
    print(f'Expected an area of {expected}, got {rc.area}')

rc = Rectangle(2,3)
# rc.width=9
use_it(rc)
print(rc.area)

'''Redesigning with Composition
Instead of having Square inherit from Rectangle, you can design separate classes and use a factory pattern to create the correct type of shape.'''
class Shape:
    @property
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    """docstring"""
    def __init__(self, width, height):
        self._height = height
        self._width = width

    @property
    def width(self):
        """docstring"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        
    @property
    def height(self):
        """docstring"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def area(self):
        return self._height * self._width
    
    def __str__(self) -> str:
        return f'width: {self._width}, height: {self._height}'

class Square(Shape):
    def __init__(self, size):
        self._size = size
    
    @property
    def size(self):
        """docstring"""
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
    
    @property
    def width(self):
        return self._size

    @width.setter
    def width(self, value):
        self._size = value
    
    @property
    def height(self):
        return self._size

    @height.setter
    def height(self, value):
        self._size = value

    @property
    def area(self):
        return self._size * self._size

    def __str__(self) -> str:
        return f'size: {self._size}'

def shape_factory(shape_type, *args):
    """Factory function to create shapes"""
    if shape_type == "rectangle":
        return Rectangle(*args)
    elif shape_type == "square":
        return Square(*args)
    else:
        raise ValueError(f"Unknown shape type: {shape_type}")

def use_it(shape):
    """the function to use the new class above"""
    if isinstance(shape, Rectangle):
        w = shape.width
        shape.height = 10
        print(f'height: {shape.height}, width: {w}')
        expected = int(w * 10)
    elif isinstance(shape, Square):
        size = shape.size
        shape.size = 10
        print(f'size: {shape.size}, width: {size}')
        expected = int(size * 10)
    
    print(f'Expected an area of {expected}, got {shape.area}')

# Example usage
rc = shape_factory("rectangle", 2, 3)
use_it(rc)

sq = shape_factory("square", 5)
use_it(sq)


sq = Square(5)
use_it(sq)

## ************************* How to fix it **************************** ##
