'''This code demonstrates another way to implement the Singleton design pattern using a metaclass. 
By defining a Singleton metaclass, you ensure that any class using this metaclass can only have
one instance. Here’s an explanation of how it works:
Singleton Metaclass Definition:
The Singleton class inherits from type.
_instances is a class-level dictionary that stores instances of classes using this metaclass.
The __call__ method is overridden to control the instantiation process. It checks if an instance 
of the class already exists in _instances. If not, it creates a new instance and stores it in _instances.
Database Class:
The Database class uses the Singleton metaclass.
The __init__ method prints "Loading database" to indicate when the database is loaded.
Testing the Singleton:
Two Database objects (d1 and d2) are created, and their identity is checked to confirm they are the same instance.
'''
class Singleton(type):
    """ Metaclass that creates a Singleton base type when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print('Loading database')

if __name__ == '__main__':
    d1 = Database()
    d2 = Database()
    print(d1 == d2)
