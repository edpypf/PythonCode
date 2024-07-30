'''The singleton decorator you provided is a clean and reusable way to implement 
the Singleton design pattern. This decorator ensures that only one instance of the 
decorated class is created. Here’s an explanation of how it works and the expected
output when you run the script:

Decorator Definition:
singleton(class_) defines the decorator, which takes a class as its argument.
Inside the decorator, instances is a dictionary that stores instances of classes.
Instance Retrieval:
get_instance(*args, **kwargs) is a nested function that checks if an instance of the class already exists in the instances dictionary.
If the class is not in instances, it creates a new instance and stores it in the dictionary.
It returns the instance (either newly created or retrieved from the dictionary).
Applying the Decorator:
@singleton is used to decorate the Database class, ensuring that only one instance is created.
Testing the Singleton:
Two Database objects (d1 and d2) are created, and their identity is checked to confirm they are the same instance.
'''
def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Database:
    def __init__(self):
        print('Loading database')


if __name__ == '__main__':
    d1 = Database()
    d2 = Database()
    print(d1 == d2)
