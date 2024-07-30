'''This code demonstrates the Monostate (Borg) design pattern, which ensures that all instances of a class share the same state. 
This pattern differs from the Singleton pattern because it allows multiple instances of a class but ensures they all share the same state.

Here's a detailed explanation of each part:
CEO Class:
The CEO class has a shared state stored in the class-level dictionary __shared_state.
In the __init__ method, self.__dict__ is set to point to __shared_state, ensuring that all instances share the same attributes.
The __str__ method provides a string representation of the CEO's name and age.
Monostate Class:
The Monostate class is designed to share state among its instances.
The class-level dictionary _shared_state stores the shared state.
The __new__ method sets obj.__dict__ to _shared_state, ensuring that all instances share the same attributes.
CFO Class:
The CFO class inherits from Monostate, so all instances share the same state.
The __init__ method initializes name and money_managed attributes.
The __str__ method provides a string representation of the CFO's name and the amount of money managed.
Testing the Monostate:
Instances of the CEO class (ceo1, ceo2, ceo3) are created and their shared state is manipulated to demonstrate that all instances reflect the same state.
Instances of the CFO class (cfo1, cfo2) are created and their shared state is manipulated similarly to show that all instances share the same state.
'''
class CEO:
    __shared_state = {
        'name': 'Steve',
        'age': 55
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return f'{self.name} is {self.age} years old'


class Monostate:
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Monostate, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj


class CFO(Monostate):
    def __init__(self):
        self.name = ''
        self.money_managed = 0

    def __str__(self):
        return f'{self.name} manages ${self.money_managed}bn'


if __name__ == '__main__':
    ceo1 = CEO()
    print(ceo1)  # Output: Steve is 55 years old

    ceo1.age = 66

    ceo2 = CEO()
    ceo2.age = 77
    print(ceo1)  # Output: Steve is 77 years old
    print(ceo2)  # Output: Steve is 77 years old

    ceo2.name = 'Tim'

    ceo3 = CEO()
    print(ceo1)  # Output: Tim is 77 years old
    print(ceo2)  # Output: Tim is 77 years old
    print(ceo3)  # Output: Tim is 77 years old

    cfo1 = CFO()
    cfo1.name = 'Sheryl'
    cfo1.money_managed = 1

    print(cfo1)  # Output: Sheryl manages $1bn

    cfo2 = CFO()
    cfo2.name = 'Ruth'
    cfo2.money_managed = 10
    print(cfo1)  # Output: Ruth manages $10bn
    print(cfo2)  # Output: Ruth manages $10bn
