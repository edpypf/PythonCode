import random

class Database:
    initialized = False

    def __init__(self):
        # self.id = random.randint(1,101)
        # print('Generated an id of ', self.id)
        # print('Loading database from file')
        pass

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls)\
                .__new__(cls, *args, **kwargs)

        return cls._instance


database = Database()

if __name__ == '__main__':
    d1 = Database()
    d2 = Database()

    print(d1.id, d2.id)
    print(d1 == d2)
    print(database == d1)
'''
Singleton Design Pattern:
The __new__ method is overridden to control the object creation process. 
It checks if an instance already exists (cls._instance). If not, it creates a new instance. 
This ensures only one instance of the Database class is created.
Initialization:
The __init__ method is present but does not perform any actions since it's commented out. 
This method is called after __new__ to initialize the object.
Testing the Singleton:
Two Database objects (d1 and d2) are created and their IDs are compared. The commented-out 
id generation and print statements are meant to show that both objects should have the same 
ID, demonstrating that only one instance exists.    
'''
