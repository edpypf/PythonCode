class Square:
    def __init__(self, side=0):
        self.side = side

class Rect:
    def __init__(self, height=0, width=0):
        self.height = height
        self.width = width

def calculate_area(rc):
    return rc.width * rc.height

class SquareToRectangleAdapter:
    def __init__(self, square):
        self.width = square.side
        self.height = square.side
    def toRec(self):
        return Rect(self.height, self.width)
    
s = Square(11)
a = calculate_area(SquareToRectangleAdapter(s))
print(a)

# ------------ standard answer ------------------------#
from unittest import TestCase

class Square:
    def __init__(self, side=0):
        self.side = side

def calculate_area(rc):
    return rc.width * rc.height

class SquareToRectangleAdapter:
    def __init__(self, square):
        self.square = square

    @property
    def width(self):
        return self.square.side

    @property
    def height(self):
        return self.square.side

class Evaluate(TestCase):
    def test_exercise(self):
        sq = Square(11)
        adapter = SquareToRectangleAdapter(sq)
        self.assertEqual(121, calculate_area(adapter))
        sq.side = 10
        self.assertEqual(100, calculate_area(adapter))



