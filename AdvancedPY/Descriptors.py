
class Descriptors:
    def __init__(self):
        self.__bmi = 0
    def __get__(self, instance, owner):
        return self.__bmi
    def __set__(self, instance, value):
        if isinstance(value, int):
            print(value)
        else:
            raise TypeError("Bmi can only be an integer")
        if value<0:
            raise ValueError("Bmi can never be less than Zero") 
        self.__bmi = value

    def __delete__(self, instance):
        del self.__bmi

## new class
class Person:
    ## here directly assign descriptor to the attribute itself, will apply all checking and get, set, delete on that attribute
    ###***************####
    bmi = Descriptors()
    def __init__(self, name, age, bmi):
        self.name = name
        self.age = age
        self.bmi = bmi
    
    def __str__(self):
        return "{0} age {1} with a bmi of {2}".format(self.name, self.age, self.bmi)         

### Old class        
class Personal:
    def __init__(self, name, age, bmi):
        self.name = name
        self.age = age
        self.bmi = bmi
        if self.bmi < 0:
            raise ValueError("Bmi can never be less than zero")
        if isinstance(self.name, str):
            print(self.name)
        else:
            raise ValueError("Name of the person can not be an integer")

    def __str__(self):
        return "{0} age {1} with a bmi of {2}".format(self.name, self.age, self.bmi)

person1 = Person("John", "25", 17)            
print(person1)
person1.name=10
print(person1)
person2 = Person("John", "25", -17)            
print(person2)
person1.bmi=-10
print(person1)

person2 = Person("John", "25", 48)            
print(person2)


## using Descriptor in Property
class Person:
    def __init__(self, name):
        self._name = name
    
    def getName(self):
        print('Getting the Name')
        return self._name

    def setName(self, name):
        print('Setting the name to : '+ self.name)
        self._name = name

    def delName(self, name):
        print('Deleting the name')
        del self._name

    # use functions in the property
    '''The line "name = property(getName, setName, delName)" is creating a property called "name" for the Person class.
    The property function takes three arguments: the getter method ("getName"), the setter method ("setName"), and the deleter method ("delName").
    By using the property function, we are able to access the "name" attribute of an instance of the Person class as if it were a regular attribute, using dot notation (e.g., person.name).
    The getter, setter, and deleter methods specified in the property function are called automatically when we try to get, set, or delete the value of the "name" attribute respectively.
    name = property(getName, setName, delName)'''

name = Person('John')
print(name.name)
name.name='Price'
del name.name

## using class method to create the descriptor
##################################################################
class Descriptors:
    def __init__(self, x=''):
        self.x = x
    def __get__(self, object, objtype):
        return '{} for {}'.format(self.x, self.x)
    def __set__(self, obj, x):
        if isinstance(x, str):
            self.x=x
        else:
            raise TypeError("X should always be a string") 

class Person:
    ## here directly assign descriptor to the attribute itself, will apply all checking and get, set, delete on that attribute
    ###***************####
    x = Descriptors()

y = Person()
y.x='John'
print(y.x)



