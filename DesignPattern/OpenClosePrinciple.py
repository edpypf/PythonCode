from enum import Enum

from colorama import init

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE =3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3    

class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

### ***************************************************************************************************
# OCP = open for extension, closed for modification, means encourage to extend, but better not modify
# Solution: to have base filter class - using abstract methods, then override it with inherited class
### ***************************************************************************************************

class ProductionFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color: yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size: yield p

    def filter_by_size_and_color(self, products, size, color):
        """there could be more and more required filters, which needs to modify again and again"""
        for p in products:
            if p.color == color and p.size == size: yield p

### ***************************************************************************************************
# Enterprise solutions: 1-Specification
### ***************************************************************************************************

class Specification:
    '''base class'''
    def is_satisfied(self, item):
        pass

    def __and__(self, other):
        """docstring"""
        return AndSpecification(self, other)

class Filter:
    def filter(self, items, spec):
        """base filter"""
        pass

class ColorSpecification(Specification):
    """Inherited class"""
    def __init__(self, color):
        self.color = color
        
    def is_satisfied(self, item):
        """docstring"""
        return item.color == self.color        

class SizeSpecification(Specification):
    """Inherited class"""
    def __init__(self, size):
        self.size = size
        
    def is_satisfied(self, item):
        """docstring"""
        return item.size == self.size
    
class BetterFilter(Filter):
    def filter(self, items, spec):
        for p in items:
           if spec.is_satisfied(p): yield p

class AndSpecification(Specification):
    """multi specification are provided"""
    def __init__(self, *args):
        self.args = args
    def is_satisfied(self, item):
        """docstring"""
        return all(map(lambda spec: spec.is_satisfied(item), self.args))           

if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)                
    tree = Product('Tree', Color.GREEN, Size.LARGE)                
    house = Product('House', Color.BLUE, Size.LARGE)       

    products = [apple, tree, house]         

    # old way of fitering
    pf = ProductionFilter()
    print('Green products (old): ')
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f' - {p.name} is green')

    # new way of filtering through filter class
    bf = BetterFilter()
    green = ColorSpecification(Color.GREEN)
    blue = ColorSpecification(Color.BLUE)
    large = SizeSpecification(Size.LARGE)
    # largeblue = AndSpecification(large, blue)
    large_blue=large & blue

    print('Green products (new):')
    for p in bf.filter(products, green):
        print(f' - {p.name} is green')

    print('Large products (new):')
    for p in bf.filter(products, large):
        print(f' - {p.name} is large')

    print('Large Blue products (new):')
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is large and blue')    
