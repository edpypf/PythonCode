import copy

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start=Point(), end=Point()):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'Line starts from ({self.start.x}, {self.start.y}) and ends at ({self.end.x}, {self.end.y})'

    def deep_copy(self):
        new_start = copy.deepcopy(self.start)
        new_end = copy.deepcopy(self.end)
        return Line(new_start, new_end)

# Create points and a line
s = Point(100, 10)
e = Point(11, 21)
l1 = Line(s, e)

# Perform a deep copy of the line
l2 = l1.deep_copy()

# Print both lines
print(l1)
print(l2)
