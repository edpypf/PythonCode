# Factory is to move too many factory method out to be another group of methods, which is another class
from cmath import cos, sin

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'        

class PointFactory:
    @staticmethod
    def new_cartesian_point(x, y):
        p = Point()
        p.x = x
        p.y = y
        return p
    
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * cos(theta), rho * sin(theta))

if __name__ == '__main__':
    p = Point(2, 3)
    p2 = PointFactory.new_polar_point(1, 2)
    print(p, p2)

### ************************* Moving the factory inside ***************#
# Factory is to move too many factory method out to be another group of methods, which is another class
from cmath import cos, sin

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'        
        
    '''and basically you can move the whole PointFactory inside of Point class
    and then calling it using: Point.PointFactory.new_polar_point(1,2)'''
    class PointFactory:
        # @staticmethod
        def new_cartesian_point(self, x, y):
            p = Point()
            p.x = x
            p.y = y
            return p

        @staticmethod
        def new_polar_point(self, rho, theta):
            return Point(rho * cos(theta), rho * sin(theta))

if __name__ == '__main__':
    p = Point(2, 3)
    p2 = Point.PointFactory.new_polar_point(1, 2)
    print(p, p2)
